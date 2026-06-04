<div align="center">

# 🩺 病历全景报告 · Medical History Report

### 把一摞看不懂的病历，变成一页家人能看懂的健康地图。

*Turn years of scattered medical records into one clear, mobile-friendly health story —
a timeline, per-lesion size tracking, lab trends, and a checklist to bring to the doctor.*

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757)
![Zero deps](https://img.shields.io/badge/HTML%20generator-zero%20dependencies-16a34a)
![Mobile friendly](https://img.shields.io/badge/📱-mobile%20friendly-2563eb)
![Sample data](https://img.shields.io/badge/sample%20data-100%25%20fictional-7c3aed)

<br>

<img src="docs/preview-hero.png" width="760" alt="报告预览：健康概览仪表盘 + 最需关注的问题">

</div>

---

## 😣 这个问题，太多家庭都遇到过

家里老人病了十年，攒下**一整箱**化验单、CT 片、出院小结、PET-CT 报告……
每一张你都看不太懂，更别说连起来看：

> *"那个结节到底是变大了还是没变？"*
> *"这病是越来越重，还是已经稳定了？"*
> *"下次去医院，我该问医生什么？"*

医生没时间帮你把十年病历从头捋一遍。**这个工具帮你捋。**

## ✨ 它能做什么

把一个人多年的病历（体检 / 化验 / 超声 / CT / MRI / PET-CT / 病理 / 出院诊断 / 用药）
读进来，自动生成**一份自带样式、断网也能开、手机也好看的 HTML 健康报告**：

| | 模块 | 一句话价值 |
|---|---|---|
| 📊 | **健康概览仪表盘** | 整体风险一眼定级（绿/黄/橙/红）|
| 🎯 | **Top 问题排序** | 最该操心的事，排在最前面 |
| 📜 | **病情变化史** | 诊断怎么一步步演变，一张表看懂 |
| 📈 | **病灶尺寸逐年轨迹** | "结节 2015→2025 到底长了多少"——精确到每次检查 |
| 🧪 | **指标趋势图** | LDH / 肿瘤标志物 / 血压…… 逐年连线 |
| 🫀 | **器官系统分类** | 按肺、甲状腺、妇科… 分门别类 |
| 🟢🔴 | **变好 / 变差 / 稳定** | 四象限，带证据，不含糊 |
| 💬 | **家属大白话版** | 不用懂医学，也能看明白 |
| ✅ | **问医生清单** | 直接打印带去医院 |

> 🔒 **铁律**：一切结论基于病历原文，**不编造**；不确定的写"需医生确认"；
> 严重信号标红。**它帮你理解病情、和医生沟通——但永远不替代医生。**

<div align="center">
<table><tr>
<td align="center"><b>📱 手机视图</b><br><img src="docs/preview-mobile.png" width="240"></td>
<td align="center"><b>🖥️ 完整报告</b><br><img src="docs/preview-full.png" width="430"></td>
</tr></table>
<sub>以上预览均使用<b>完全虚构</b>的示例病人「林安然(化名)」数据——与任何真实病人无关。</sub>
</div>

---

## 🚀 30 秒上手

```bash
# 1) 结构化 JSON → 一页 HTML 报告（零依赖，开箱即用）
python3 scripts/build_report.py examples/sample_patient.json out.html

# 2) （可选）导出长图 + PDF，直接发微信给家人
python3 scripts/export_pdf.py out.html out      # → out-long.png  +  out.pdf
```

打开 `out.html` 就是上面那张报告。换成你自己的 `patient.json` 就是你家人的报告。

## 🤖 作为 Claude Skill 使用（推荐）

真正的魔法在这里——你不用手填 JSON。把 skill 装进 Claude：

```bash
git clone https://github.com/SkylarWJY/medical-history-report \
  ~/.claude/skills/medical-history-report
```

然后直接对 Claude 说：**"帮我把这箱病历整理成一份健康报告。"**
Claude 会照着 [`SKILL.md`](SKILL.md) 的 5 步走：

```
清点资料  →  并行多智能体逐张读取/提取病灶尺寸  →  汇总结构化  →  生成 HTML  →  导出长图/PDF
```

> 💡 资料量大也不怕：上百份扫描件时，skill 会**为每份就诊档案派一个提取智能体并行处理**——
> 几小时的活儿压缩到几分钟。

## 📦 仓库结构

```
medical-history-report/
├─ SKILL.md                    # 给 Claude 的工作流指令（5 步法）
├─ assets/schema.json          # 病灶/诊断/指标的结构化数据规范
├─ scripts/
│  ├─ build_report.py          # JSON → 手机自适应 HTML（零依赖，已测试）
│  └─ export_pdf.py            # HTML → 长图 PNG + PDF（Chrome + Pillow）
└─ examples/
   ├─ sample_patient.json      # 虚构示例数据
   └─ sample_report.html       # 生成好的样例报告
```

数据怎么填？看 [`assets/schema.json`](assets/schema.json)（每个模块都是可选的，
你给什么它画什么）和 [`examples/sample_patient.json`](examples/sample_patient.json) 的完整范例。

## 🔐 隐私优先

病历是最敏感的个人数据。本工具**默认本地处理、不上传、不部署公网**。
想在手机看？优先把单文件 HTML/PDF 发到手机离线打开；确需共享给异地家人时，
建议用**密码加密**方案并先确认。**任何演示 / 公开示例，一律使用虚构数据。**

## 📄 License

[MIT](LICENSE) · 用得上就拿去用，记得善待你的家人。❤️

<div align="center"><sub>Built with Claude · 如果它帮到了你或你的家人，欢迎点个 ⭐</sub></div>
