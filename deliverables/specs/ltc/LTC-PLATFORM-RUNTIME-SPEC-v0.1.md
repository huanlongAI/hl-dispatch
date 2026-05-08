# LTC 平台 Runtime 规格 v0.1

**状态**：R1 平台 runtime 规格草案
**日期**：2026-05-06
**负责人**：NODE-A
**范围**：Windows 优先、Mac 第二平台

## 1. 平台裁决

LTC 强制部署仅限公司固定资产电脑。

平台顺序：

1. Windows。
2. Mac。

不支持：

- Linux。
- 移动端。
- 其他桌面平台。

员工个人电脑不纳入强制范围。员工自愿选择可安装，不作制度规定。

## 2. 安装边界

安装前置工作由行政部门处理完毕。LTC 接入视为前提合规流程已完毕。未处理完成的员工或设备不会进入安装环节。

LTC 不接入 MDM 或类似平台。设备由人工指定和登记。

## 3. Windows runtime

Windows R3 必须支持：

- 安装。
- 设备绑定。
- 员工工程身份绑定。
- 开机自启。
- 常驻运行。
- 签名心跳。
- 健康检查。
- 当前安装电脑硬件配置采集。
- 管理员停用 / 卸载。
- owner view。

Windows R3 不得支持：

- 员工本地退出。
- 员工本地卸载。
- 员工本地绕过。
- raw observation 落盘。
- MDM 接入。
- 资产管理。

### 3.1 Windows Endpoint Alpha 实机化前置 contract

当前 alpha contract 只定义可验证输入和 hash-only 输出，不等价于真实 Windows 服务完成。

允许：

- 生成 Windows service plan、execution contract、verification runner contract。
- 校验外部 Windows runner 提交的 sanitized observation。
- 生成 Windows installer artifact manifest。
- 记录 installer manifest hash 和 service plan hash。

禁止：

- 在非 Windows 环境声明 service registered、startup auto 或 process running 已验证。
- 在 LTC 内执行 `sc.exe`、PowerShell、`Start-Service`、`New-Service` 或安装命令。
- 保存 command output、PowerShell transcript、raw service path、raw local path、service binary path 或完整命令参数。
- 把 installer manifest 说成真实安装包已构建、已签名或已安装。

Windows 实机验证机可用时，必须单独记录 sanitized evidence：service name hash、running status、startup mode、heartbeat signature state / hash、timestamp bucket、service plan hash、runner hash、service registered boolean 和 startup persistence boolean。

## 4. Mac runtime

Mac R3/R4 必须支持：

- 安装。
- 设备绑定。
- 员工工程身份绑定。
- launch daemon 或等价常驻机制。
- 签名心跳。
- 健康检查。
- 当前安装电脑硬件配置采集。
- 管理员停用 / 卸载。
- owner view。

Mac 不得使用：

- 内核级黑箱防篡改。
- 不可审计的系统扩展。
- raw observation 落盘。
- MDM 接入。
- 资产管理。

## 5. 硬件配置采集

允许字段：

- `osName`
- `osVersion`
- `machineModel`
- `cpuModel`
- `memoryGB`
- `diskCapacityGB`
- `gpuModel`
- `hardwareFingerprintHash`

禁止：

- 资产编号，除非来自人工登记台账并另行裁决。
- 用户目录路径。
- 文件列表。
- 设备上的个人内容。

## 6. 断链

以下情况产生断链或合规事件：

- 心跳缺失。
- agent 崩溃。
- 管理员停用。
- 管理员卸载。
- 本地绕过或篡改尝试。

断链只表示证据完整性和合规状态，不自动等价绩效负面。

## 7. Endpoint evidence chain

Endpoint evidence chain summary 可以把 heartbeat、Windows service observation、管理员动作、owner amendment 和 DahuiZi evidence envelope 串成 hash-only 摘要。

必须：

- 输出 chain hash、segment hashes、status、reason codes 和 signature state。
- 支持断链、恢复、管理员动作和员工说明 amendment 并存。
- 员工说明只保存 amendment hash，不覆盖原 evidence。

不得：

- 输出员工说明明文、管理员理由明文、绩效分、员工排名、薪酬建议或纪律处分。
- 把断链自动转成绩效负面。
