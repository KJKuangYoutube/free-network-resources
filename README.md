# 全球开源网络测试节点、多协议中继配置与公共服务资源汇编 🌐

<p align="center">
  <a href="https://kjkuang.win/">
    <img src="https://img.shields.io/badge/官方网站-kjkuang.win-orange?style=for-the-badge&logo=safari" alt="Official Website" />
  </a>
  <a href="https://www.youtube.com/@KJKUANG">
    <img src="https://img.shields.io/badge/YouTube-KJKUANG科技狂-red?style=for-the-badge&logo=youtube" alt="YouTube Channel" />
  </a>
  <img src="https://img.shields.io/badge/状态-持续更新维护-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License" />
</p>

本项目由 **[KJKUANG 科技狂](https://kjkuang.win/)** 社区发起并维护，旨在收集、评测与整理公开互联网中高信誉度的**免费网络测试节点、公益中继服务、官方纯净 WireGuard 落地配置与多协议客户端调优方案**。

无论你是跨国科研协作、海外技术开发、AI 大模型调试还是网络协议排错，都能在这里快速找到可用的备用出海中继通道。

> ⚠️ **免责声明与网络安全守则**：  
> 1. 本项目收集整理的节点与公共服务信息均来源于互联网公开社群，仅供计算机网络通信、协议分流调优及学术技术研究参考；  
> 2. **时效性说明**：公共免费节点具备多用户并发使用属性，随时可能发生网络拥堵、限速或节点下线，建议作为应急排错与备用通道；  
> 3. **敏感业务安全红线**：**严禁使用任何第三方公共免费节点登录网络银行、进行加密货币大额交易或传输核心商业敏感机密！** 建议搭配端到端加密与两跳链式代理使用。

---

## 目录 (Table of Contents)

- [一、 公益与免费网络测试服务商精选](#一-公益与免费网络测试服务商精选)
- [二、 国际大厂官方原生纯净 WireGuard 节点提取](#二-国际大厂官方原生纯净-wireguard-节点提取)
- [三、 两跳链式代理 (Relay Proxy) 终极玩法](#三-两跳链式代理-relay-proxy-终极玩法)
- [四、 主流全平台客户端推荐与调优](#四-主流全平台客户端推荐与调优)
- [五、 常见问题排查 (FAQ)](#五-常见问题排查-faq)
- [六、 社区贡献与节点失效反馈](#六-社区贡献与节点失效反馈)

---

## 一、 公益与免费网络测试服务商精选

以下精选平台长期提供免费试用额度、签到机制或公益中转节点，支持导出为标准 Clash / Sing-box / 通用链接：

| 平台名称 | 官网地址 | 协议支持 | 服务特性与使用建议 |
| :--- | :--- | :--- | :--- |
| **iKuuu** | [ikuuu.org ↗](https://ikuuu.org/) | Shadowsocks / V2Ray | 全网知名的老牌公益综合平台，支持每日签到赠送流量，节点覆盖香港、日本、美国等多个地区，稳定性较高。 |
| **GLaDOS** | [glados.vip ↗](https://www.glados.vip/) | VLESS / Clash / WireGuard | 运营多年的学术友好型技术站点，提供长期免费签到计划，对高校教育网、学术检索及开发者协同支持良好。 |
| **101Ghost** | [101ghost.com ↗](https://101ghost.com/) | Shadowsocks / Trojan | 界面现代清爽，提供常规节点与新人试用配额，支持一键导入主流客户端。 |
| **FreeV2** | [b.freev2.net ↗](https://b.freev2.net) | V2Ray / VLESS | 免费公共多节点聚合展示，适合在应急断网时快速提取单节点进行连通性测试。 |
| **End-GFW** | [end-gfw.com ↗](https://end-gfw.com) | 多协议开源隧道 | 开源社区反网络封锁项目，收集整理公开开源中继资源，适合极客研究底层通信机制。 |

> 💡 **小贴士**：部分服务商官网在部分网络环境下可能需要备用域名解析，若遇打不开可尝试使用不同 DNS（如 `1.1.1.1` 或 `8.8.8.8`）访问。

---

## 二、 国际大厂官方原生纯净 WireGuard 节点提取

公共免费节点最大的痛点是 **“IP 机房恶名度高，频繁触发 Cloudflare 盾牌与 ChatGPT/Claude 人机风控”**。  
解决这一问题的最佳方案是直接从国际顶级大厂提取**原生住宅级/企业级纯净 WireGuard 节点**：

### 1. Cloudflare WARP 官方原生出口 (WireGuard Generator)
* **配置文件提取工具**：[lanrat.github.io/wireguard-warp-generator ↗](https://lanrat.github.io/wireguard-warp-generator/)
* **核心优势**：
  * 一键调用 Cloudflare 官方 API 注册专属免费身份；
  * 生成包含专属公钥、私钥与分配 IPv4/IPv6 的标准 `.conf` 配置文件；
  * 依托 Cloudflare 全球 300+ 边缘数据中心，IP 纯净度极佳，顺畅解锁全网服务。

### 2. Proton VPN 官方权威免费节点 (瑞士原生)
* **获取入口**：[account.proton.me/u/1/vpn/WireGuard ↗](https://account.proton.me/u/1/vpn/WireGuard)
* **核心优势**：
  * 瑞士顶尖隐私机构 Proton 官方提供；
  * 严格实行零日志（No-Logs）审计政策，免除隐私泄漏担忧；
  * 后台可直接下载官方 WireGuard 配置文件，导入即用。

---

## 三、 核心配置中心：在线多源生成器、小火箭通用规则与云端聚合流水线

为了让所有用户无论是使用手机还是电脑，都能以最省心的方式享受最高水准的纯净网络体验，本项目同时提供 **纯前端离线多源聚合生成器**、**小火箭通用规则配置** 与 **GitHub Actions 全自动云端订阅聚合器**：

---

### 🌐 1. 纯小白零门槛：站长在线多源聚合生成器 (无需 Fork / 离线零隐私泄露)

如果你不想注册或登录 GitHub Fork 仓库，只希望在网页中粘贴几个机场链接，直接下载现成的 `clash-config.yaml` 导入软件：
* **在线工具直达入口**：👉 **[https://kjkuang.win/tools/clash-merger ↗](https://kjkuang.win/tools/clash-merger)**
* **三大核心优势**：
  * **完全免代码**：只需在网页文本框中粘贴你的 1~5 个机场订阅地址，一键点击「生成并下载」即可获得标准 YAML 配置文件；
  * **WireGuard / WARP 自由选配**：支持纯机场多源合并；如果手里有 Cloudflare WARP 或 Proton 节点，也可按需填入并一键开启 `dialer-proxy` 链式落地；
  * **100% 隐私安全**：纯浏览器前端离线解析，**0 字节上传服务器**，绝不记录你的个人订阅凭据与 Token！

---

### 🚀 2. 小火箭 (Shadowrocket) 通用全能极速配置 (`kjkuang.conf`)

很多朋友在使用小火箭时，经常遇到**“从 GitHub 下载规则一直在转圈、极度缓慢”**、**“国内微信/B站也走代理白白浪费流量”**、**“ChatGPT/Claude 经常报错打不开”** 的问题。

本项目特供一份**极致轻量、纯净零私货、Cloudflare CDN 全球加速**的自适应全能配置：
* 🚀 **官网高速直链 (强烈推荐 · Cloudflare CDN 秒级分发 · 拒绝转圈)**：
  ```text
  https://kjkuang.win/kjkuang.conf
  ```
* 🐙 **GitHub 备用直链**：
  ```text
  https://raw.githubusercontent.com/KJKuangYoutube/free-network-resources/main/profiles/kjkuang.conf
  ```

#### 🛡️ 为什么称其为「全网最干净的配置」？（消除小白核心顾虑）
1. **纯净零私货（绝无第三方节点）**：配置中**不含有任何第三方机场节点**，只负责规则调度大脑，绝不触碰你的账号密码，绝不会冲掉或覆盖你原有导入的节点！
2. **黑科技动态自适应 `select = (.*)`**：无论你在小火箭里添加了 1 个机场还是 10 个机场，它都能自动识别全部节点，并一秒归拢到测速组与各分流通道中，无需手动写代码！
3. **0.1 秒秒级加载（极致加速）**：彻底剔除传统配置动辄 15MB 的 GitHub 外链规则集，深度结合小火箭本地离线 `GEOIP,CN` 数据库与国内大厂白名单，文件仅 3KB，移动网络下也能瞬间秒下！
4. **AI 与国际流媒体专属通道**：ChatGPT、Claude、Grok、Gemini 优先走最稳定通道；国内微信、淘宝、抖音 100% 本地极速直连。

#### 📱 小火箭 10 秒极速导入方法：
1. 复制上方官网直链：`https://kjkuang.win/kjkuang.conf`；
2. 打开小火箭，点击底部 **「配置 (Config)」**；
3. 点击右上角 **「➕ (添加配置)」**，将链接粘贴至输入框中，点击 **「下载」**（瞬间完成，无需等待）；
4. 在「远程文件」列表中找到它，**点击并选择「使用配置」**，搞定！

---

### 🚀 3. Clash / Mihomo 多订阅聚合器 (Fork 即用专属私有云)

如果你手里有多个机场订阅，又想把 Cloudflare WARP 或 Proton VPN 整合进同一个订阅里，并且**绝不向任何第三方转换站泄露自己的私有 Token**，推荐直接 **Fork 本项目**：

#### 🛠️ Fork 即用 3 步走：
1. **Fork 本仓库**：点击本页面右上角的 **`Fork`** 按钮，复制一份到你自己的 GitHub 账号下；
2. **填写你的专属配置**：
   * 在你自己 Fork 的仓库中，新建或复制 `config.example.yaml` 为 **`config.yaml`**；
   * 在里面填入你自己的各个机场订阅链接，可选开启 Cloudflare WARP 或 Proton WireGuard；
3. **自动生成专属订阅直链**：
   * 仓库内置的 GitHub Actions 每天会自动运行，生成标准纯净的 `dist/clash.yaml`；
   * 你专属的永久私有订阅链接即为：
     ```text
     https://raw.githubusercontent.com/你的GitHub用户名/free-network-resources/main/dist/clash.yaml
     ```
   * 复制该链接直接填入 **Clash Verge Rev** 或 **Mihomo Party**，即可实现多机场自动合体、自动测速优选与权威规则分流！

---

### ⚡ 4. 官方预制聚合模板文件 (`all-in-one-relay.yaml`)

如果你不想 Fork，只想本地测试或参考语法：
* **配置源文件**：[`profiles/all-in-one-relay.yaml`](./profiles/all-in-one-relay.yaml)
* 支持原生 `dialer-proxy` 链式代理与多订阅自动合并，可直接在客户端导入或作为本地模板修改。

---

## 四、 主流全平台客户端推荐与调优

| 平台分类 | 推荐客户端 | 官方项目地址 | 核心亮点 |
| :--- | :--- | :--- | :--- |
| **桌面全能机皇 (Win/Mac/Linux)** | **Clash Verge Rev** | [clash-verge-rev ↗](https://github.com/clash-verge-rev/clash-verge-rev) | Tauri+Rust 超轻量架构，Mihomo 原生全协议驱动，支持 TUN 模式与脚本覆写。 |
| **跨平台统一体验 (iOS/Android/PC)** | **Karing** | [Karing 官方 ↗](https://github.com/KaringX/karing) | 原生支持 iOS、Android、Mac、Win，全格式订阅自动识别，图形化两跳链式代理。 |
| **移动极客首选 (iOS/iPadOS)** | **Shadowrocket (小火箭)** | [App Store ↗](https://apps.apple.com/app/shadowrocket/id932747118) | 经典国民级神器，支持首条命中规则流水线、Fallback 策略组与局域网代理共享。 |
| **新一代核心先锋 (多平台)** | **Hiddify** | [hiddify-app ↗](https://github.com/hiddify/hiddify-app) | Sing-box 原生内核驱动，高丢包网络下 Hysteria 2 / TUIC v5 抗干扰能力极强。 |

详细的各客户端配置实战教程，可参阅科技狂官方博客：
- 📖 [Clash Verge Rev 桌面端终极指南](https://kjkuang.win/posts/clash-verge-guide/)
- 📖 [Hiddify 全平台进阶指南](https://kjkuang.win/posts/hiddify-guide/)
- 📖 [Karing 全平台客户端终极指南](https://kjkuang.win/posts/karing-guide/)
- 📖 [小火箭 (Shadowrocket) 从入门到精通](https://kjkuang.win/posts/shadowrocket-guide/)
- 📖 [全平台代理客户端天梯大横评与演进史](https://kjkuang.win/posts/proxy-history/)

---

## 五、 常见问题排查 (FAQ)

#### Q1: 导入订阅后节点连通性测试全部显示超时 (Timeout)？
- **排查步骤**：
  1. 检查本地网络 DNS 是否遭遇运营商劫持，尝试在客户端将本地 DoH 修改为 `https://223.5.5.5/dns-query`，远端修改为 `https://1.1.1.1/dns-query`；
  2. 确认订阅链接是否已过期，可尝试手动在浏览器打开该链接确认是否有有效节点数据返回；
  3. 切换至 TCP 协议节点测试排查是否为本地网络 UDP 封锁。

#### Q2: 为什么访问网页正常，但命令行终端 `git clone` 或部分 App 无法代理？
- **解决方案**：开启客户端内的 **TUN 模式 (TUN Mode)**。传统的“系统代理”仅拦截标准浏览器 HTTP/HTTPS 流量，而 TUN 模式通过底层虚拟网络适配器接管整机所有网络栈，实现透明分流。

---

## 六、 社区贡献与节点失效反馈

欢迎全球开发者与网络极客共同维护本资源库：
- **提交新资源**：欢迎提交 [Pull Request](https://github.com/KJKuangYoutube/free-network-resources/pulls) 分享长期稳定的优质测试节点；
- **失效报告**：如发现某个平台长期无法访问或已停止运营，请随时提交 [Issue](https://github.com/KJKuangYoutube/free-network-resources/issues) 告知更新；
- **Star 支持**：如果这个项目对你的网络开发与学习有所帮助，欢迎点亮右上角的 **Star 🌟** 给予支持！

---

<p align="center">
  <b>KJKUANG 科技狂 官方技术矩阵</b><br>
  <a href="https://kjkuang.win/">官方收藏夹网站</a> · 
  <a href="https://www.youtube.com/@KJKUANG">YouTube 频道</a> · 
  <a href="https://github.com/KJKuangYoutube">GitHub 组织</a>
</p>
