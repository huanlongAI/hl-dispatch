#!/usr/bin/env ruby
# encoding: UTF-8
# frozen_string_literal: true

require "yaml"
require "json"
require "date"
require "open3"

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

def load_yaml(path)
  YAML.load_file(path, permitted_classes: [Date])
rescue ArgumentError
  YAML.load_file(path)
end

workflow_path = File.expand_path("../.github/workflows/feishu-notify.yml", __dir__)
workflow = load_yaml(workflow_path)
jobs = workflow.fetch("jobs")

notification_steps = []
jobs.each do |job_name, job|
  Array(job["steps"]).each do |step|
    run = step["run"]
    next unless run
    next unless step.fetch("name", "").match?(/Notification|Channel/)

    notification_steps << [job_name, step.fetch("name"), run, step["env"] || {}]
  end
end

failures = []

notification_steps.each do |job_name, step_name, run, env|
  label = "#{job_name} / #{step_name}"

  failures << "#{label}: missing strict shell mode" unless run.include?("set -euo pipefail")
  unless run.include?('if [ -z "$WEBHOOK" ]; then') &&
         run.include?("Feishu webhook is empty; notification skipped") &&
         run.include?("Merge gate impact: none.") &&
         run.include?("exit 0")
    failures << "#{label}: webhook empty guard must fail open with warning and step summary"
  end
  failures << "#{label}: curl response is not captured" unless run.include?('response="$(curl')
  unless run.include?('if ! response="$(curl') &&
         run.include?("Feishu provider request failed; notification failure is observer-only") &&
         run.include?("Feishu notification failed open")
    failures << "#{label}: provider request failure must fail open with warning"
  end
  unless run.match?(/if\s+!\s+echo\s+"\$\{response\}"\s+\|\s+jq\s+-e\s+'.*\.code\s*==\s*0/m) &&
         run.include?("Feishu provider returned non-success response; notification failure is observer-only") &&
         run.include?("Feishu notification provider warning")
    failures << "#{label}: Feishu response code check must fail open with warning"
  end
  failures << "#{label}: notification steps must not hard fail with exit 1" if run.include?("exit 1")
  failures << "#{label}: direct jq-to-curl pipeline can hide jq failures" if run.match?(/\}'\s*\|\s*curl/m)
  failures << "#{label}: jq string concatenation in content must be parenthesized" if run.match?(/content:\s+\$[A-Za-z0-9_]+\s*\+/)

  if run.include?("PM_WEBHOOK")
    failures << "#{label}: pm-labeled notifications must not silently fall back to task webhook" if run.include?(']] && [ -n "${PM_WEBHOOK:-}" ]; then')
    failures << "#{label}: pm-labeled notifications must require PM_WEBHOOK" unless run.include?('WEBHOOK="${PM_WEBHOOK:-}"')
  end

  if job_name == "notify-issue-task"
    failures << "#{label}: mainline issue notifications must use engineering webhook" unless env["ENGINEERING_WEBHOOK"].to_s.include?("FEISHU_WEBHOOK_ENGINEERING") && run.include?("ENGINEERING_WEBHOOK")
    failures << "#{label}: mainline issue notifications must not use task webhook" if env.key?("TASK_WEBHOOK") || env.values.any? { |value| value.to_s.include?("FEISHU_WEBHOOK_TASK") } || run.include?("TASK_WEBHOOK") || run.include?("FEISHU_WEBHOOK_TASK")
    failures << "#{label}: engineering cards must identify the engineering channel" unless run.include?("[hl-dispatch][工程通知]")
    failures << "#{label}: assigned issues must prefer direct message routing" unless run.include?('ACTION" = "assigned"') && run.include?("DIRECT_OPEN_ID")
    failures << "#{label}: direct messages must use bot app credentials" unless run.include?("FEISHU_BOT_APP_ID") && run.include?("FEISHU_BOT_APP_SECRET")
    failures << "#{label}: direct messages must target open_id" unless run.include?("receive_id_type=open_id")
    failures << "#{label}: successful direct message must skip group webhook" unless run.include?("Direct message sent; skipping group webhook")
    failures << "#{label}: personal progress must suppress group fallback" unless run.include?("Personal progress notification is DM-only; group webhook suppressed")
    failures << "#{label}: TEAM.yml loader must permit Date on GitHub runner Ruby" unless run.include?('require "date"') && run.include?("permitted_classes: [Date]")
    unless run.include?('if [ "$ACTION" = "assigned" ]; then') &&
           run.include?("Direct message bot credentials missing; group webhook suppressed")
      failures << "#{label}: missing direct-message credentials must skip group notification"
    end
    unless run.include?('if ! token_response="$(curl') &&
           run.include?("Direct message token request failed; group webhook suppressed")
      failures << "#{label}: direct message token request failure must skip group notification"
    end
    unless run.include?('if ! tenant_token="$(echo "${token_response}" | jq -er') &&
           run.include?("Direct message token parse failed; group webhook suppressed")
      failures << "#{label}: direct message token parse failure must skip group notification"
    end
    unless run.include?('if ! dm_response="$(curl') &&
           run.include?("Direct message provider request failed; group webhook suppressed")
      failures << "#{label}: direct message provider request failure must skip group notification"
    end
    failures << "#{label}: direct message non-success response must skip group notification" unless run.include?("Direct message provider returned non-success response; group webhook suppressed")
  end

  if job_name == "notify-comment"
    failures << "#{label}: mainline comment notifications must use engineering webhook" unless env["ENGINEERING_WEBHOOK"].to_s.include?("FEISHU_WEBHOOK_ENGINEERING") && run.include?("ENGINEERING_WEBHOOK")
    failures << "#{label}: mainline comment notifications must not use task webhook" if env.key?("TASK_WEBHOOK") || env.values.any? { |value| value.to_s.include?("FEISHU_WEBHOOK_TASK") } || run.include?("TASK_WEBHOOK") || run.include?("FEISHU_WEBHOOK_TASK")
    failures << "#{label}: engineering comment cards must identify the engineering channel" unless run.include?("[hl-dispatch][工程通知]")
    if run.include?("PM_WEBHOOK")
      failures << "#{label}: mainline comments must not route to PM webhook"
    end
  end

  if job_name == "notify-issue-task"
    if run.include?("falling back to group webhook")
      failures << "#{label}: personal progress must not fall back to group webhook"
    end
  end
end

if notification_steps.empty?
  failures << "no notification steps found"
end

direct_message_path = File.expand_path("feishu-direct-message.rb", __dir__)
team_path = File.expand_path("../TEAM.yml", __dir__)
team = load_yaml(team_path)
notification_policy = team.fetch("notification_policy")

unless notification_policy.fetch("mainline_process", "").include?("AI native工程通知") &&
       notification_policy.fetch("mainline_process", "").include?("FEISHU_WEBHOOK_ENGINEERING")
  failures << "TEAM.yml notification_policy must route mainline_process to AI native工程通知 via FEISHU_WEBHOOK_ENGINEERING"
end

unless notification_policy.fetch("personal_progress", "") == "direct_message_only"
  failures << "TEAM.yml notification_policy must mark personal_progress as direct_message_only"
end

unless notification_policy.fetch("group_fallback", "").include?("suppressed")
  failures << "TEAM.yml notification_policy must suppress group fallback for personal progress"
end

if notification_policy.fetch("fallback", "").match?(/Feishu group|飞书群|group/i)
  failures << "TEAM.yml notification_policy must not preserve group fallback for personal progress"
end

if !File.exist?(direct_message_path)
  failures << "direct-message helper missing: scripts/feishu-direct-message.rb"
else
  helper = File.read(direct_message_path)
  failures << "direct-message helper must use lark-cli im +messages-send" unless helper.include?("+messages-send")
  failures << "direct-message helper must target --user-id for P2P delivery" unless helper.include?("--user-id")
  failures << "direct-message helper must not default to group --chat-id delivery" if helper.include?("--chat-id")
  failures << "direct-message helper must require --execute for writes" unless helper.include?("--execute")
  failures << "direct-message helper TEAM.yml loader must permit Date on GitHub runner Ruby" unless helper.include?("permitted_classes: [Date]")

  stdout, stderr, status = Open3.capture3(
    "ruby",
    direct_message_path,
    "--team",
    team_path,
    "--github",
    "wp159951",
    "--text",
    "dry run"
  )

  if !status.success?
    failures << "direct-message helper dry-run failed: #{stderr.strip}"
  else
    begin
      payload = JSON.parse(stdout)
      failures << "direct-message helper dry-run must not perform writes" unless payload["write_performed"] == false
      failures << "direct-message helper must report direct_message delivery" unless payload["delivery"] == "direct_message"
      failures << "direct-message helper must resolve GitHub recipient" unless payload.dig("recipient", "github") == "wp159951"
      failures << "direct-message helper dry-run must redact open_id" if stdout.include?("ou_")
      planned = Array(payload["planned_command_redacted"])
      failures << "direct-message helper planned command must use --user-id" unless planned.include?("--user-id")
      failures << "direct-message helper planned command must not use --chat-id" if planned.include?("--chat-id")
    rescue JSON::ParserError => e
      failures << "direct-message helper dry-run did not emit JSON: #{e.message}"
    end
  end
end

if failures.any?
  warn failures.join("\n")
  exit 1
end

puts "feishu-notify workflow checks passed: #{notification_steps.size} notification steps; direct-message helper checks passed"
