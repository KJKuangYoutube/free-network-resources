#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KJKuang科技狂 - Clash/Mihomo 多订阅与 WireGuard 聚合生成脚本
功能：
1. 读取 config.yaml (若无则读取 config.example.yaml)
2. 将多个机场订阅解析为 proxy-providers
3. 注入 Cloudflare WARP 与 Proton VPN WireGuard 节点
4. 根据配置自动开启/关闭 dialer-proxy 链式中继
5. 组装 Loyalsoldier 权威分流规则集，输出为标准 dist/clash.yaml
"""

import os
import re
import sys

def parse_simple_yaml(filepath):
    """简易 YAML 解析器（支持基础的嵌套结构与列表，无需第三方依赖）"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    airports = []
    standalone_nodes = {}
    chain_enable = True
    
    current_section = None
    current_node = None
    current_airport = None
    
    for line in lines:
        raw_line = line.rstrip()
        # 跳过空行和纯注释
        if not raw_line or raw_line.strip().startswith("#"):
            continue
            
        indent = len(raw_line) - len(raw_line.lstrip())
        stripped = raw_line.strip()
        
        # 顶级段落
        if indent == 0:
            if stripped.startswith("airports:"):
                current_section = "airports"
            elif stripped.startswith("standalone_nodes:"):
                current_section = "standalone_nodes"
            elif stripped.startswith("chain_proxy:"):
                current_section = "chain_proxy"
            continue
            
        # airports 段落
        if current_section == "airports":
            if stripped.startswith("- name:"):
                match = re.search(r'- name:\s*["\']?(.*?)["\']?$', stripped)
                name = match.group(1) if match else "未命名订阅"
                current_airport = {"name": name, "url": ""}
                airports.append(current_airport)
            elif stripped.startswith("url:") and current_airport:
                match = re.search(r'url:\s*["\']?(.*?)["\']?$', stripped)
                if match:
                    current_airport["url"] = match.group(1)
                    
        # standalone_nodes 段落
        elif current_section == "standalone_nodes":
            if indent == 2 and ":" in stripped:
                node_type = stripped.split(":")[0].strip()
                current_node = {}
                standalone_nodes[node_type] = current_node
            elif indent >= 4 and ":" in stripped and current_node is not None:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].split("#")[0].strip().strip('"').strip("'")
                if val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                elif val.isdigit():
                    val = int(val)
                current_node[key] = val
                
        # chain_proxy 段落
        elif current_section == "chain_proxy":
            if stripped.startswith("enable:"):
                val = stripped.split(":", 1)[1].split("#")[0].strip().lower()
                chain_enable = (val == "true")
                
    return airports, standalone_nodes, chain_enable

def generate_clash_yaml(airports, standalone_nodes, chain_enable, output_path):
    """生成标准完整 Mihomo YAML 配置文件"""
    
    # 1. 独立节点 (Proxies)
    proxies_yaml = []
    dialer_str = '    dialer-proxy: "🛫 前置中转选择"\n' if chain_enable else ''
    
    warp = standalone_nodes.get("cloudflare_warp", {})
    if warp.get("enable"):
        name = warp.get("name", "Cloudflare-WARP")
        proxies_yaml.append(f"""  - name: "🛡️ {name} (落地出口)"
    type: wireguard
    server: {warp.get('server', 'engage.cloudflareclient.com')}
    port: {warp.get('port', 2408)}
    ip: {warp.get('ip', '172.16.0.2')}
    ipv6: {warp.get('ipv6', '2606:4700:110:8f0b:cdc5:6d26:f24b:5396')}
    private-key: {warp.get('private_key', '')}
    public-key: {warp.get('public_key', '')}
    udp: true
    mtu: {warp.get('mtu', 1280)}
    remote-dns-resolve: true
    dns:
      - 1.1.1.1
      - 1.0.0.1
{dialer_str}""")

    proton = standalone_nodes.get("proton_wireguard", {})
    if proton.get("enable"):
        name = proton.get("name", "Proton-VPN")
        proxies_yaml.append(f"""  - name: "🛡️ {name} (瑞士纯净落地)"
    type: wireguard
    server: {proton.get('server', 'nl-free-01.protonvpn.net')}
    port: {proton.get('port', 51820)}
    ip: {proton.get('ip', '10.2.0.2')}
    private-key: {proton.get('private_key', '')}
    public-key: {proton.get('public_key', '')}
    udp: true
    mtu: {proton.get('mtu', 1420)}
    remote-dns-resolve: true
    dns:
      - 1.1.1.1
      - 1.0.0.1
{dialer_str}""")

    # 2. 机场订阅 (Proxy-Providers)
    providers_yaml = []
    provider_names = []
    for idx, ap in enumerate(airports, 1):
        pid = f"sub-{idx}"
        provider_names.append(pid)
        providers_yaml.append(f"""  {pid}:
    type: http
    url: "{ap.get('url', '')}"
    interval: 86400
    path: ./proxy_providers/{pid}.yaml
    health-check:
      enable: true
      interval: 600
      url: http://www.gstatic.com/generate_204""")

    # 3. 策略组 (Proxy-Groups)
    use_lines = "\n".join([f"      - {p}" for p in provider_names]) if provider_names else "      - DIRECT"
    
    # 落地节点名字集合
    landing_proxies = []
    if warp.get("enable"):
        landing_proxies.append(f'      - "🛡️ {warp.get("name", "Cloudflare-WARP")} (落地出口)"')
    if proton.get("enable"):
        landing_proxies.append(f'      - "🛡️ {proton.get("name", "Proton-VPN")} (瑞士纯净落地)"')
    landing_proxies_str = "\n".join(landing_proxies) if landing_proxies else ""

    # 组装完整的 YAML 文本
    content = f"""# ==============================================================================
# KJKuang科技狂 - 全能多订阅聚合与纯净分流配置 (All-in-One Clash/Mihomo Profile)
# 由自动化聚合脚本生成，支持全协议驱动、自动测速优选与权威分流
# ==============================================================================

port: 7890
socks-port: 7891
mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
ipv6: false
external-controller: 127.0.0.1:9090
secret: ""

# ------------------------------------------------------------------------------
# 1. 高性能 DNS 模块 (Fake-IP 防泄漏架构)
# ------------------------------------------------------------------------------
dns:
  enable: true
  listen: 0.0.0.0:1053
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter:
    - "*.lan"
    - "*.local"
    - "*.localhost"
    - "stun.*"
    - "time.*"
    - "ntp.*"
    - "+.msftconnecttest.com"
    - "+.msftncsi.com"
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - https://1.1.1.1/dns-query
    - https://dns.google/dns-query
    - tls://8.8.8.8
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 240.0.0.0/4

# ------------------------------------------------------------------------------
# 2. 独立纯净出口节点 (WireGuard)
# ------------------------------------------------------------------------------
proxies:
{"".join(proxies_yaml) if proxies_yaml else "  []"}

# ------------------------------------------------------------------------------
# 3. 多订阅集合提供商 (Proxy Providers)
# ------------------------------------------------------------------------------
proxy-providers:
{"\n".join(providers_yaml) if providers_yaml else "  {}"}

# ------------------------------------------------------------------------------
# 4. 智能策略组编排 (Proxy Groups)
# ------------------------------------------------------------------------------
proxy-groups:
  # 总控主选择器
  - name: "🚀 节点选择"
    type: select
    proxies:
{landing_proxies_str}
      - "⚡ 自动优选 (全部订阅自动测速)"
      - "DIRECT"
    use:
{use_lines}

  # 链式代理前置中转选择池
  - name: "🛫 前置中转选择"
    type: select
    proxies:
      - "⚡ 自动优选 (全部订阅自动测速)"
    use:
{use_lines}

  # 全局并发低延迟自动优选
  - name: "⚡ 自动优选 (全部订阅自动测速)"
    type: url-test
    url: "http://www.gstatic.com/generate_204"
    interval: 300
    tolerance: 50
    use:
{use_lines}

  # AI 平台专属通道 (ChatGPT/Claude/Gemini)
  - name: "🤖 AI专属 (ChatGPT/Claude/Gemini)"
    type: select
    proxies:
{landing_proxies_str}
      - "🚀 节点选择"
      - "⚡ 自动优选 (全部订阅自动测速)"

  # 国际流媒体加速通道 (YouTube/Netflix)
  - name: "📺 国际流媒体"
    type: select
    proxies:
      - "🚀 节点选择"
      - "⚡ 自动优选 (全部订阅自动测速)"
{landing_proxies_str}

  # 兜底未知流量
  - name: "🐟 漏网之鱼"
    type: select
    proxies:
      - "🚀 节点选择"
      - "DIRECT"

# ------------------------------------------------------------------------------
# 5. 权威规则集提供商 (Rule Providers - Loyalsoldier)
# ------------------------------------------------------------------------------
rule-providers:
  reject:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

  icloud:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/icloud.txt"
    path: ./ruleset/icloud.yaml
    interval: 86400

  apple:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/apple.txt"
    path: ./ruleset/apple.yaml
    interval: 86400

  google:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/google.txt"
    path: ./ruleset/google.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400

  direct:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt"
    path: ./ruleset/direct.yaml
    interval: 86400

  private:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/private.txt"
    path: ./ruleset/private.yaml
    interval: 86400

  gfw:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/gfw.txt"
    path: ./ruleset/gfw.yaml
    interval: 86400

  tld-not-cn:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/tld-not-cn.txt"
    path: ./ruleset/tld-not-cn.yaml
    interval: 86400

  telegramcidr:
    type: http
    behavior: ipcidr
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/telegramcidr.txt"
    path: ./ruleset/telegramcidr.yaml
    interval: 86400

  cncidr:
    type: http
    behavior: ipcidr
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/cncidr.txt"
    path: ./ruleset/cncidr.yaml
    interval: 86400

  lancidr:
    type: http
    behavior: ipcidr
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/lancidr.txt"
    path: ./ruleset/lancidr.yaml
    interval: 86400

  applications:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/applications.txt"
    path: ./ruleset/applications.yaml
    interval: 86400

# ------------------------------------------------------------------------------
# 6. 精细化分流规则体系 (从高到低逐级匹配)
# ------------------------------------------------------------------------------
rules:
  # 应用与私网直连
  - RULE-SET,applications,DIRECT
  - RULE-SET,private,DIRECT

  # 广告拦截
  - RULE-SET,reject,REJECT

  # AI 平台专属通道
  - DOMAIN-SUFFIX,openai.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,chatgpt.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,oaistatic.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,oaiusercontent.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,anthropic.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,claude.ai,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,aistudio.google.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,generativelanguage.googleapis.com,🤖 AI专属 (ChatGPT/Claude/Gemini)
  - DOMAIN-SUFFIX,deepseek.com,DIRECT

  # 国际流媒体
  - DOMAIN-SUFFIX,youtube.com,📺 国际流媒体
  - DOMAIN-SUFFIX,googlevideo.com,📺 国际流媒体
  - DOMAIN-SUFFIX,netflix.com,📺 国际流媒体
  - DOMAIN-SUFFIX,netflix.net,📺 国际流媒体
  - DOMAIN-SUFFIX,nflximg.net,📺 国际流媒体
  - DOMAIN-SUFFIX,spotify.com,📺 国际流媒体

  # 苹果服务直连
  - RULE-SET,icloud,DIRECT
  - RULE-SET,apple,DIRECT

  # 海外服务走代理
  - RULE-SET,google,🚀 节点选择
  - RULE-SET,proxy,🚀 节点选择
  - RULE-SET,gfw,🚀 节点选择
  - RULE-SET,tld-not-cn,🚀 节点选择
  - RULE-SET,telegramcidr,🚀 节点选择,no-resolve

  # 大陆直连与局域网
  - RULE-SET,direct,DIRECT
  - RULE-SET,lancidr,DIRECT
  - RULE-SET,cncidr,DIRECT
  - GEOIP,LAN,DIRECT
  - GEOIP,CN,DIRECT

  # 兜底
  - MATCH,🐟 漏网之鱼
"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 成功生成全能 Clash 配置文件: {output_path}")

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(root_dir, "config.yaml")
    example_file = os.path.join(root_dir, "config.example.yaml")
    output_file = os.path.join(root_dir, "dist", "clash.yaml")
    
    target_config = config_file if os.path.exists(config_file) else example_file
    print(f"📖 读取配置文件: {target_config}")
    
    airports, standalone_nodes, chain_enable = parse_simple_yaml(target_config)
    print(f"✈️  已解析机场订阅数量: {len(airports)}")
    print(f"🛡️  已识别独立节点: {list(standalone_nodes.keys())}")
    print(f"⛓️  链式中继 (dialer-proxy) 状态: {'已激活' if chain_enable else '未启用'}")
    
    generate_clash_yaml(airports, standalone_nodes, chain_enable, output_file)

if __name__ == "__main__":
    main()
