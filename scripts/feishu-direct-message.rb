#!/usr/bin/env ruby
# encoding: UTF-8
# frozen_string_literal: true

require "json"
require "date"
require "open3"
require "optparse"
require "yaml"

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

class DirectMessageError < StandardError; end

DEFAULT_TEAM_PATH = File.expand_path("../TEAM.yml", __dir__)

def public_recipient(entry)
  {
    "role" => entry["role"],
    "name" => entry["name"],
    "github" => entry["github"],
    "status" => entry["status"].to_s.empty? ? "active" : entry["status"]
  }
end

def active_entry?(entry)
  status = entry["status"].to_s
  return false if status.match?(/vacant|pending|departed|inactive|离职|清理|不作为|待确认/i)

  true
end

def normalize_lark(entry)
  lark = entry["lark"]
  lark.is_a?(Hash) ? lark : {}
end

def team_entries(team)
  roles = team.fetch("roles")
  entries = []

  roles.each do |role_id, role|
    if role.is_a?(Hash)
      entries << {
        "role" => role_id,
        "name" => role["name"],
        "github" => role["github"],
        "lark" => role["lark"],
        "status" => role["status"]
      }

      Array(role["members"]).each do |member|
        next unless member.is_a?(Hash)

        entries << {
          "role" => role_id,
          "name" => member["name"] || member["github"],
          "github" => member["github"],
          "lark" => member["lark"],
          "status" => member["status"] || role["status"]
        }
      end
    end
  end

  entries
end

def load_team(path)
  YAML.load_file(path, permitted_classes: [Date])
rescue ArgumentError
  YAML.load_file(path)
end

def resolve_recipient(team, options)
  entries = team_entries(team)
  entry =
    if options[:github]
      entries.find { |item| item["github"].to_s.casecmp(options[:github]).zero? }
    elsif options[:role]
      entries.find { |item| item["role"].to_s == options[:role].to_s && item["github"].to_s != "" }
    end

  target = options[:github] || options[:role]
  raise DirectMessageError, "recipient not found in TEAM.yml: #{target}" unless entry
  raise DirectMessageError, "recipient is not an active notification target: #{target}" unless active_entry?(entry)

  open_id = normalize_lark(entry)["open_id"].to_s
  raise DirectMessageError, "recipient missing Feishu open_id: #{target}" if open_id.empty?

  [entry, open_id]
end

def build_command(options, open_id)
  command = [
    options[:lark_cli],
    "im",
    "+messages-send",
    "--as",
    "bot",
    "--user-id",
    open_id
  ]

  if options[:text]
    command += ["--text", options[:text]]
  elsif options[:markdown]
    command += ["--markdown", options[:markdown]]
  end

  command += ["--idempotency-key", options[:idempotency_key]] if options[:idempotency_key]
  command
end

def redact_command(command)
  command.map { |part| part.to_s.start_with?("ou_") ? "OPEN_ID_REDACTED" : part }
end

def parse_options(argv)
  options = {
    team: DEFAULT_TEAM_PATH,
    lark_cli: ENV.fetch("LARK_CLI", "lark-cli"),
    execute: false
  }

  parser = OptionParser.new do |opts|
    opts.banner = "Usage: feishu-direct-message.rb (--github HANDLE | --role ROLE) (--text TEXT | --markdown TEXT) [--execute]"
    opts.on("--team PATH", "Path to TEAM.yml") { |value| options[:team] = value }
    opts.on("--github HANDLE", "Resolve recipient by GitHub handle") { |value| options[:github] = value }
    opts.on("--role ROLE", "Resolve recipient by role id") { |value| options[:role] = value }
    opts.on("--text TEXT", "Plain text body") { |value| options[:text] = value }
    opts.on("--markdown TEXT", "Markdown body") { |value| options[:markdown] = value }
    opts.on("--idempotency-key KEY", "Optional message idempotency key") { |value| options[:idempotency_key] = value }
    opts.on("--lark-cli PATH", "lark-cli executable path") { |value| options[:lark_cli] = value }
    opts.on("--execute", "Send the direct message") { options[:execute] = true }
  end

  parser.parse!(argv)

  unless options[:github] || options[:role]
    raise DirectMessageError, "provide --github or --role"
  end
  if options[:github] && options[:role]
    raise DirectMessageError, "provide only one of --github or --role"
  end
  unless options[:text] || options[:markdown]
    raise DirectMessageError, "provide --text or --markdown"
  end
  if options[:text] && options[:markdown]
    raise DirectMessageError, "provide only one of --text or --markdown"
  end

  options
end

def print_json(payload)
  puts JSON.pretty_generate(payload)
end

def sanitized_result(stdout)
  parsed = JSON.parse(stdout)
  {
    "message_id_present" => !parsed["message_id"].to_s.empty?,
    "create_time" => parsed["create_time"]
  }
rescue JSON::ParserError
  {
    "raw_stdout_present" => !stdout.to_s.empty?
  }
end

def main(argv)
  options = parse_options(argv)
  team = load_team(options[:team])
  recipient, open_id = resolve_recipient(team, options)
  command = build_command(options, open_id)

  base_payload = {
    "delivery" => "direct_message",
    "recipient" => public_recipient(recipient),
    "planned_command_redacted" => redact_command(command)
  }

  unless options[:execute]
    print_json(base_payload.merge("write_performed" => false))
    return 0
  end

  stdout, stderr, status = Open3.capture3(*command)
  unless status.success?
    raise DirectMessageError, "lark-cli send failed: #{stderr.strip.empty? ? "exit #{status.exitstatus}" : stderr.strip}"
  end

  print_json(base_payload.merge("write_performed" => true, "result" => sanitized_result(stdout)))
  0
end

if __FILE__ == $PROGRAM_NAME
  begin
    raise SystemExit, main(ARGV)
  rescue DirectMessageError => e
    warn "error: #{e.message}"
    raise SystemExit, 2
  end
end
