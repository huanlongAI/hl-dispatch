#!/usr/bin/env ruby
# encoding: UTF-8
# frozen_string_literal: true

require "yaml"
require "json"
require "open3"

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

workflow_path = File.expand_path("../.github/workflows/feishu-notify.yml", __dir__)
workflow = YAML.load_file(workflow_path)
jobs = workflow.fetch("jobs")

notification_steps = []
jobs.each do |job_name, job|
  Array(job["steps"]).each do |step|
    run = step["run"]
    next unless run
    next unless step.fetch("name", "").match?(/Notification|Channel/)

    notification_steps << [job_name, step.fetch("name"), run]
  end
end

failures = []

notification_steps.each do |job_name, step_name, run|
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
    failures << "#{label}: assigned issues must prefer direct message routing" unless run.include?('ACTION" = "assigned"') && run.include?("DIRECT_OPEN_ID")
    failures << "#{label}: direct messages must use bot app credentials" unless run.include?("FEISHU_BOT_APP_ID") && run.include?("FEISHU_BOT_APP_SECRET")
    failures << "#{label}: direct messages must target open_id" unless run.include?("receive_id_type=open_id")
    failures << "#{label}: successful direct message must skip group webhook" unless run.include?("Direct message sent; skipping group webhook")
    unless run.include?('if ! token_response="$(curl') &&
           run.include?("Direct message token request failed; falling back to group webhook")
      failures << "#{label}: direct message token request failure must fall back to group webhook"
    end
    unless run.include?('if ! tenant_token="$(echo "${token_response}" | jq -er') &&
           run.include?("Direct message token parse failed; falling back to group webhook")
      failures << "#{label}: direct message token parse failure must fall back to group webhook"
    end
    unless run.include?('if ! dm_response="$(curl') &&
           run.include?("Direct message provider request failed; falling back to group webhook")
      failures << "#{label}: direct message provider request failure must fall back to group webhook"
    end
    failures << "#{label}: direct message non-success response must fall back to group webhook" unless run.include?("Direct message provider returned non-success response; falling back to group webhook")
  end
end

if notification_steps.empty?
  failures << "no notification steps found"
end

direct_message_path = File.expand_path("feishu-direct-message.rb", __dir__)
team_path = File.expand_path("../TEAM.yml", __dir__)

if !File.exist?(direct_message_path)
  failures << "direct-message helper missing: scripts/feishu-direct-message.rb"
else
  helper = File.read(direct_message_path)
  failures << "direct-message helper must use lark-cli im +messages-send" unless helper.include?("+messages-send")
  failures << "direct-message helper must target --user-id for P2P delivery" unless helper.include?("--user-id")
  failures << "direct-message helper must not default to group --chat-id delivery" if helper.include?("--chat-id")
  failures << "direct-message helper must require --execute for writes" unless helper.include?("--execute")

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
