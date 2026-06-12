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
workflow_source = File.read(workflow_path)
workflow = load_yaml(workflow_path)
triggers = workflow.fetch("on", workflow.fetch(true, {}))
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

if workflow_source.match?(/^\s*issue_comment:\s*$/)
  failures << "feishu-notify workflow must not trigger directly on issue_comment.created"
end

unless workflow_source.match?(/^\s*workflow_dispatch:\s*$/)
  failures << "feishu-notify workflow must keep manual workflow_dispatch trigger"
end

if workflow_source.include?("notify-comment") ||
   workflow_source.include?("Issue 新评论") ||
   workflow_source.include?("issue_comment_v1")
  failures << "feishu-notify workflow must not broadcast ordinary issue comments"
end

issues_trigger = triggers.fetch("issues", {})
issue_types = Array(issues_trigger.fetch("types", []))
unless issue_types == ["labeled"]
  failures << "feishu-notify workflow must only subscribe to issues.labeled for explicit action notifications"
end

if workflow_source.include?("issue_mainline_v1") ||
   workflow_source.include?("assigned_issue_v1") ||
   workflow_source.include?("Personal progress notification") ||
   workflow_source.include?("Direct message sent; skipping group webhook")
  failures << "feishu-notify workflow must remove ordinary issue lifecycle and assignment notification paths"
end

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
  unless run.include?("Feishu delivery ledger") &&
         run.include?("route:") &&
         run.include?("status:") &&
         run.include?("content_template:") &&
         run.include?("target_url:") &&
         run.include?("message_preview:")
    failures << "#{label}: delivery ledger summary must include route/status/template/target/preview"
  end
  unless run.include?("FEISHU_DELIVERY_LEDGER_JSON=") &&
         run.include?("ledger_json=\"$(jq -cn") &&
         run.include?("message_preview")
    failures << "#{label}: delivery ledger must emit jq-built FEISHU_DELIVERY_LEDGER_JSON log line"
  end

  if run.include?("PM_WEBHOOK")
    failures << "#{label}: pm-labeled notifications must not silently fall back to task webhook" if run.include?(']] && [ -n "${PM_WEBHOOK:-}" ]; then')
    failures << "#{label}: pm-labeled notifications must require PM_WEBHOOK" unless run.include?('WEBHOOK="${PM_WEBHOOK:-}"')
  end

  if job_name == "notify-issue-task"
    failures << "#{label}: action label notifications must use engineering webhook" unless env["ENGINEERING_WEBHOOK"].to_s.include?("FEISHU_WEBHOOK_ENGINEERING") && run.include?("ENGINEERING_WEBHOOK")
    failures << "#{label}: action label notifications must not use task webhook" if env.key?("TASK_WEBHOOK") || env.values.any? { |value| value.to_s.include?("FEISHU_WEBHOOK_TASK") } || run.include?("TASK_WEBHOOK") || run.include?("FEISHU_WEBHOOK_TASK")
    failures << "#{label}: engineering cards must identify the engineering channel" unless run.include?("[hl-dispatch][工程通知]")

    failures << "#{label}: labeled issue notifications must expose label name" unless env["LABEL_NAME"].to_s.include?("github.event.label.name")
    unless run.include?('if [ "$ACTION" = "labeled" ]; then') &&
           run.include?("action:decision_required") &&
           run.include?("action:acceptance_ready") &&
           run.include?("action:blocker") &&
           run.include?("action:p0_failure") &&
           run.include?("Label notification skipped")
      failures << "#{label}: labeled issue notifications must be limited to explicit action labels"
    end
    failures << "#{label}: action label notifications must use action_label_v1 template" unless run.include?("action_label_v1")
  end

  if job_name == "notify-comment"
    failures << "#{label}: notify-comment job must be removed; ordinary issue_comment.created must not broadcast to Feishu"
  end

  if job_name == "notify-manual"
    failures << "#{label}: manual notifications must use engineering webhook" unless env["ENGINEERING_WEBHOOK"].to_s.include?("FEISHU_WEBHOOK_ENGINEERING") && run.include?("ENGINEERING_WEBHOOK")
    failures << "#{label}: manual notifications must not use task webhook" if env.key?("TASK_WEBHOOK") || env.values.any? { |value| value.to_s.include?("FEISHU_WEBHOOK_TASK") } || run.include?("TASK_WEBHOOK") || run.include?("FEISHU_WEBHOOK_TASK")
    failures << "#{label}: manual cards must identify the engineering channel" unless run.include?("[hl-dispatch][工程通知]")
    failures << "#{label}: manual ledger must use manual_dispatch_v1 template" unless run.include?("manual_dispatch_v1")
    failures << "#{label}: manual notifications must include target URL input" unless env["NOTIFY_URL"].to_s.include?("github.event.inputs.notify_url") && run.include?("NOTIFY_URL")
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
  failures << "direct-message helper must retry transient lark-cli transport failures" unless helper.include?("LARK_DM_MAX_ATTEMPTS") && helper.include?("retryable_transport_error?")
  failures << "direct-message helper retry path must not include group fallback" if helper.match?(/chat-id|group webhook|fallback to group/i)
  failures << "direct-message helper must support curl fallback for lark-cli transport failures" unless helper.include?("curl_direct_message") && helper.include?("tenant_access_token/internal") && helper.include?("/open-apis/im/v1/messages")
  failures << "direct-message helper curl fallback must prefer node-c bot env credentials" unless helper.include?("FEISHU_BOT_APP_ID") && helper.include?("FEISHU_BOT_APP_SECRET")
  failures << "direct-message helper curl fallback must keep direct open_id delivery" unless helper.include?("receive_id_type=open_id")
  failures << "direct-message helper curl fallback must preserve idempotency uuid" unless helper.include?('"uuid"')
  failures << "direct-message helper curl fallback must pass JSON via stdin to avoid exposing app_secret in process args" unless helper.include?("--data-binary") && helper.include?("@-") && helper.include?("stdin_data: JSON.generate(payload)")
  failures << "direct-message helper must validate task message context before sending" unless helper.include?("validate_message_quality!") && helper.include?("message_missing_github_url") && helper.include?("message_contains_black_box_phrase")

  valid_direct_message = "魏鹏，请执行测试任务。背景：验证飞书私聊必须附上下文。GitHub 是唯一事实源，飞书只是提醒。任务入口：https://github.com/huanlongAI/hl-dispatch/issues/194。请在 GitHub 回复结果。本消息不授权生产。"

  stdout, stderr, status = Open3.capture3(
    "ruby",
    direct_message_path,
    "--team",
    team_path,
    "--github",
    "wp159951",
    "--text",
    valid_direct_message
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

  _bad_stdout, bad_stderr, bad_status = Open3.capture3(
    "ruby",
    direct_message_path,
    "--team",
    team_path,
    "--github",
    "wp159951",
    "--text",
    "收到，继续。"
  )
  failures << "direct-message helper must reject context-free task messages" if bad_status.success?
  unless bad_stderr.include?("direct message lacks required task context") &&
         bad_stderr.include?("message_missing_github_url") &&
         bad_stderr.include?("message_missing_context") &&
         bad_stderr.include?("message_contains_black_box_phrase:收到，继续")
    failures << "direct-message helper context-free rejection must name missing context, GitHub URL, and black-box phrase"
  end
end

if failures.any?
  warn failures.join("\n")
  exit 1
end

puts "feishu-notify workflow checks passed: #{notification_steps.size} notification steps; direct-message helper checks passed"
