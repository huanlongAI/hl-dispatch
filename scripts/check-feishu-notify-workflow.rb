#!/usr/bin/env ruby
# encoding: UTF-8
# frozen_string_literal: true

require "yaml"

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
end

if notification_steps.empty?
  failures << "no notification steps found"
end

if failures.any?
  warn failures.join("\n")
  exit 1
end

puts "feishu-notify workflow checks passed: #{notification_steps.size} notification steps"
