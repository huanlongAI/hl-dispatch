#!/usr/bin/env ruby
# encoding: UTF-8
# frozen_string_literal: true

require "json"
require "date"
require "digest"
require "open3"
require "optparse"
require "yaml"

Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

class DirectMessageError < StandardError; end

DEFAULT_TEAM_PATH = File.expand_path("../TEAM.yml", __dir__)
GITHUB_URL_RE = %r{https://github\.com/huanlongAI/[^\s，。；、）)]+}
FEISHU_UUID_SAFE_RE = /\A[A-Za-z0-9_-]{1,50}\z/.freeze
TASK_CONTEXT_TERMS = %w[背景 上下文 目标 为什么 来源]
TASK_ACTION_TERMS = %w[请在 请执行 请回复 请查看 请处理 下一步 要做 回复]
TASK_BOUNDARY_TERMS = [
  "GitHub 是唯一事实源",
  "GitHub 仍是唯一事实源",
  "GitHub 是 SSOT",
  "唯一事实源",
  "飞书只是提醒",
  "飞书只是投影",
  "不授权",
  "不是授权"
].freeze
BLACK_BOX_PHRASES = [
  "收到，继续",
  "收到 / 已知 / 继续推进",
  "继续推进整体治理",
  "需要进一步确认",
  "当前上下文显示",
  "可能已经处理过",
  "runtime 那个",
  "HPRD 已确认但无证据"
].freeze

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
  idempotency_key = normalized_idempotency_key(options[:idempotency_key])
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

  command += ["--idempotency-key", idempotency_key] if idempotency_key
  command
end

def redact_command(command)
  command.map { |part| part.to_s.start_with?("ou_") ? "OPEN_ID_REDACTED" : part }
end

def parse_options(argv)
  options = {
    team: DEFAULT_TEAM_PATH,
    lark_cli: ENV.fetch("LARK_CLI", "lark-cli"),
    execute: false,
    max_attempts: positive_integer_env("LARK_DM_MAX_ATTEMPTS", 5),
    retry_sleep_seconds: positive_float_env("LARK_DM_RETRY_SLEEP_SECONDS", 1.0)
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
  options[:text] = normalized_message_body(options[:text]) if options[:text]
  options[:markdown] = normalized_message_body(options[:markdown]) if options[:markdown]

  options
end

def normalized_message_body(value)
  value.to_s
       .gsub("\\r\\n", "\n")
       .gsub("\\n", "\n")
       .gsub("\\r", "\n")
end

def message_body(options)
  options[:text] || options[:markdown] || ""
end

def include_any?(text, terms)
  terms.any? { |term| text.include?(term) }
end

def validate_message_quality!(text)
  body = text.to_s
  normalized = body.downcase
  errors = []

  errors << "message_missing_github_url" unless body.match?(GITHUB_URL_RE)
  errors << "message_missing_context" unless include_any?(body, TASK_CONTEXT_TERMS)
  errors << "message_missing_action" unless include_any?(body, TASK_ACTION_TERMS)
  errors << "message_missing_authorization_boundary" unless include_any?(body, TASK_BOUNDARY_TERMS)

  BLACK_BOX_PHRASES.each do |phrase|
    errors << "message_contains_black_box_phrase:#{phrase}" if normalized.include?(phrase.downcase)
  end

  return if errors.empty?

  raise DirectMessageError, "direct message lacks required task context: #{errors.join(", ")}"
end

def positive_integer_env(name, default)
  value = ENV.fetch(name, default.to_s).to_i
  value.positive? ? value : default
end

def positive_float_env(name, default)
  value = Float(ENV.fetch(name, default.to_s))
  value.positive? ? value : default
rescue ArgumentError
  default
end

def retryable_transport_error?(text)
  normalized = text.to_s.downcase
  [
    '"type": "network"',
    '"subtype": "transport"',
    "socket is not connected",
    "connection reset",
    "connection refused",
    "read tcp",
    "timed out",
    "timeout",
    "eof"
  ].any? { |marker| normalized.include?(marker) }
end

def normalized_idempotency_key(value)
  raw = value.to_s.strip
  return nil if raw.empty?
  return raw if raw.match?(FEISHU_UUID_SAFE_RE)

  "hl-dm-#{Digest::SHA256.hexdigest(raw)[0, 32]}"
end

def capture_with_retry(command, max_attempts:, retry_sleep_seconds:)
  attempt = 0
  last_stdout = +""
  last_stderr = +""
  last_status = nil

  loop do
    attempt += 1
    last_stdout, last_stderr, last_status = Open3.capture3(*command)
    return [last_stdout, last_stderr, last_status, attempt] if last_status.success?

    combined_error = "#{last_stdout}\n#{last_stderr}"
    break unless attempt < max_attempts && retryable_transport_error?(combined_error)

    warn "warning: transient lark-cli transport failure; retrying #{attempt + 1}/#{max_attempts}"
    sleep(retry_sleep_seconds)
  end

  [last_stdout, last_stderr, last_status, attempt]
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

def lark_cli_config_path
  ENV.fetch("LARK_DM_CONFIG_PATH", File.expand_path("~/.lark-cli/config.json"))
end

def load_lark_app_credentials(config_path = lark_cli_config_path)
  env_app_id = ENV["FEISHU_BOT_APP_ID"].to_s.empty? ? ENV["LARK_BOT_APP_ID"].to_s : ENV["FEISHU_BOT_APP_ID"].to_s
  env_app_secret = ENV["FEISHU_BOT_APP_SECRET"].to_s.empty? ? ENV["LARK_BOT_APP_SECRET"].to_s : ENV["FEISHU_BOT_APP_SECRET"].to_s
  return [env_app_id, env_app_secret] if !env_app_id.empty? && !env_app_secret.empty?

  config = JSON.parse(File.read(config_path))
  apps = Array(config["apps"])
  apps = [config] if apps.empty?
  app = apps.find { |item| item["appId"].to_s == config["profile"].to_s } || apps.first
  raise DirectMessageError, "lark config has no app entry" unless app

  app_id = app["appId"].to_s
  secret_config = app["appSecret"]
  app_secret =
    if secret_config.is_a?(Hash) && secret_config["source"].to_s == "file"
      File.read(secret_config.fetch("id")).strip
    else
      secret_config.to_s
    end

  raise DirectMessageError, "lark app credential missing appId" if app_id.empty?
  raise DirectMessageError, "lark app credential missing appSecret" if app_secret.empty?

  [app_id, app_secret]
end

def curl_post_json(url, payload, headers = {})
  args = [
    "curl",
    "-sS",
    "-X",
    "POST",
    url,
    "-H",
    "Content-Type: application/json",
    "--data-binary",
    "@-"
  ]
  headers.each do |name, value|
    args += ["-H", "#{name}: #{value}"]
  end

  stdout, stderr, status = Open3.capture3(*args, stdin_data: JSON.generate(payload))
  unless status.success?
    diagnostic = stderr.strip.empty? ? "exit #{status.exitstatus}" : stderr.lines.first.to_s.strip
    raise DirectMessageError, "curl request failed: #{diagnostic}"
  end

  JSON.parse(stdout)
rescue JSON::ParserError => e
  raise DirectMessageError, "curl response was not JSON: #{e.message}"
end

def direct_message_payload(options, open_id)
  content =
    if options[:text]
      {"text" => options[:text]}
    else
      {"text" => options[:markdown]}
    end

  payload = {
    "receive_id" => open_id,
    "msg_type" => "text",
    "content" => JSON.generate(content)
  }
  idempotency_key = normalized_idempotency_key(options[:idempotency_key])
  payload["uuid"] = idempotency_key if idempotency_key
  payload
end

def curl_direct_message(options, open_id)
  app_id, app_secret = load_lark_app_credentials
  token_response = curl_post_json(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    {
      "app_id" => app_id,
      "app_secret" => app_secret
    }
  )
  unless token_response["code"] == 0 && !token_response["tenant_access_token"].to_s.empty?
    raise DirectMessageError, "tenant token request failed with code #{token_response["code"]}"
  end

  message_response = curl_post_json(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    direct_message_payload(options, open_id),
    "Authorization" => "Bearer #{token_response.fetch("tenant_access_token")}"
  )
  unless message_response["code"] == 0
    message = message_response["msg"].to_s
    suffix = message.empty? ? "" : ": #{message}"
    raise DirectMessageError, "direct message request failed with code #{message_response["code"]}#{suffix}"
  end

  data = message_response["data"].is_a?(Hash) ? message_response["data"] : {}
  {
    "transport" => "curl_direct_message",
    "message_id_present" => !data["message_id"].to_s.empty?,
    "create_time" => data["create_time"]
  }
end

def main(argv)
  options = parse_options(argv)
  validate_message_quality!(message_body(options))
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

  stdout, stderr, status, attempts = capture_with_retry(
    command,
    max_attempts: options[:max_attempts],
    retry_sleep_seconds: options[:retry_sleep_seconds]
  )
  unless status.success?
    combined_error = "#{stdout}\n#{stderr}"
    if retryable_transport_error?(combined_error) && ENV.fetch("LARK_DM_CURL_FALLBACK", "1") != "0"
      warn "warning: lark-cli transport failed after #{attempts} attempt(s); using curl direct-message fallback"
      result = curl_direct_message(options, open_id)
      print_json(base_payload.merge("write_performed" => true, "result" => result.merge("lark_cli_attempts" => attempts)))
      return 0
    end

    raise DirectMessageError, "lark-cli send failed after #{attempts} attempt(s): #{stderr.strip.empty? ? "exit #{status.exitstatus}" : stderr.strip}"
  end

  print_json(base_payload.merge("write_performed" => true, "result" => sanitized_result(stdout).merge("attempts" => attempts)))
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
