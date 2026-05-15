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
  failures << "#{label}: webhook empty guard missing" unless run.include?('[ -n "$WEBHOOK" ]')
  failures << "#{label}: curl response is not captured" unless run.include?('response="$(curl')
  failures << "#{label}: Feishu response code is not checked" unless run.match?(/jq\s+-e\s+'.*\.code\s*==\s*0/m)
  failures << "#{label}: direct jq-to-curl pipeline can hide jq failures" if run.match?(/\}'\s*\|\s*curl/m)
  failures << "#{label}: jq string concatenation in content must be parenthesized" if run.match?(/content:\s+\$[A-Za-z0-9_]+\s*\+/)
end

if notification_steps.empty?
  failures << "no notification steps found"
end

if failures.any?
  warn failures.join("\n")
  exit 1
end

puts "feishu-notify workflow checks passed: #{notification_steps.size} notification steps"
