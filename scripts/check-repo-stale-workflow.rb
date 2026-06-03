#!/usr/bin/env ruby
# encoding: UTF-8
# frozen_string_literal: true

require "yaml"
require "date"

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

def load_yaml(path)
  YAML.load_file(path, permitted_classes: [Date])
rescue ArgumentError
  YAML.load_file(path)
end

workflow_path = File.expand_path("../.github/workflows/repo-stale-check.yml", __dir__)
workflow = load_yaml(workflow_path)
job = workflow.fetch("jobs").fetch("check")
step = Array(job.fetch("steps")).find { |candidate| candidate.fetch("name", "") == "Check repo staleness" }

failures = []

if step.nil?
  failures << "repo-stale workflow must keep a Check repo staleness step"
else
  run = step.fetch("run", "")

  failures << "stale alert title prefix must use one space after [自动]" if run.include?('startswith("[自动]  仓库同步滞后")')
  failures << "stale alert duplicate detection must match generated title prefix" unless run.include?('startswith("[自动] 仓库同步滞后")')

  unless run.match?(/if\s+!\s+gh issue create\s+\\/m)
    failures << "stale alert issue creation must be guarded with fail-open handling"
  end

  unless run.include?("Stale alert issue creation failed; observer-only") &&
         run.include?("Stale alert issue creation failed open") &&
         run.include?("Merge gate impact: none.") &&
         run.include?("exit 0")
    failures << "stale alert issue creation failure must warn and fail open"
  end
end

if failures.any?
  warn failures.join("\n")
  exit 1
end

puts "repo-stale workflow checks passed"
