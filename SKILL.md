---
name: medical-history-report
description: >-
  For families caring for a patient at home: turn years of scattered medical
  records (scanned reports, labs, ultrasound, CT/MRI, PET-CT, pathology,
  discharge summaries) into ONE clear, mobile-friendly HTML health report —
  a disease-history timeline, a diagnosis-evolution table, per-lesion
  size-tracking where each nodule/mass is compared ONLY to itself over time
  (with the exam type + year-month on every data point), lab-trend charts, a
  "what exam is each site missing / go get it" data-gap table, an
  "认准一种检查 + how often" follow-up plan (what a proper checkup should
  include), risk cards, a plain-language family explanation, and a doctor-visit
  checklist. Enforces a "examine first, decide surgery later" ordering. Use when
  someone provides a folder or zip of medical records (especially many scanned
  images) and wants a clear summary of overall status, what got better / worse /
  stayed the same, what's missing, and what to do next. Always evidence-based,
  flags uncertainty as "需医生确认", never replaces a doctor; can export a long PNG
  and PDF.
---

# 病历 → 健康全景报告（Medical History Report）

把一个人多年的病历资料整理成**一份家属能看懂的、手机友好的 HTML 健康全景报告**：
时间线、诊断演变史、**每个病灶逐年尺寸变化轨迹**、指标趋势图、风险卡片、大白话解释、问医生清单。

> ⚠️ **铁律**：① 一切结论必须基于病历原文，**不编造**；② 不确定处写"需医生确认"；
> ③ 严重/恶性/急需复查信号标红；④ **本报告不替代医生诊断**。

## 何时使用
用户上传/指向一批病历（体检、化验、影像、超声、CT/MRI、PET-CT、病理、出院诊断、用药、住院记录等），
想要一份直观的整体健康梳理、疾病发展轨迹、风险点与下一步建议。

## 工作流程（5 步）

### 1. 清点资料
列出所有文件，按"就诊日期 / 检查"分组（一个文件夹通常 = 一次就诊）。统计总文件数。
扫描件常见格式：JPG/PNG/PDF。注意有些图被旋转（90°/180°）。

### 2. 提取（核心，按需并行）
逐张读取**有文字的报告页**（诊断书、病理、结论、化验单、超声/CT 测量、门诊/出院记录），
跳过纯影像切片（PET/CT/超声的灰阶或彩色图像，无可提取文字）。
**重点提取每一个有尺寸的病灶**：淋巴结 / 结节 / 肿块 / 占位 / 囊肿 / 肌瘤 / 脾大小等——
保留原文数值与单位，PET 报告务必记录 **SUVmax**。同时提取诊断、结论、异常化验（尤其
肿瘤标志物、LDH、β2-微球蛋白、血常规、肝肾功能）。

- 旋转图片处理：`cp 图 /tmp/r.jpg && sips -r 90 /tmp/r.jpg`（macOS）后再读。
- **资料量大时（几十~上百份）务必并行**：用 Workflow / 多个 Agent，**每份就诊档案派一个提取智能体**，
  按 `assets/schema.json` 里的结构返回。这能把大量图片的读取从几小时压缩到几分钟。

把提取结果整理成符合 **`assets/schema.json`** 的一个 JSON（见 `examples/sample_patient.json` 演示）。
关键是 `lesions[]`：把同一病灶历次尺寸**按时间排序**，标注 trend（up/down/flat）+ **每行的检查类型(modality)**，
这样报告里就能呈现"某结节 2015→2025 的精确大小轨迹"。

> ⚠️ **同部位才可比、注明日期与检查类型**：尺寸只在"同一部位 + 同一种检查"之间比较才有意义。
> 不同部位**绝不**放进同一张对比表；每个数据点都要写清 **年-月** 和 **CT/超声/PET/MRI**——
> 因为同一个肿块常被不同设备测，数字本就对不上。

### 3. 汇总成结构化 JSON
按器官系统归类，并填好这些"让家属看懂"的板块：
- `evolution` 诊断演变史 · `lesions` 每个病灶单独一张卡（只和自己比）· `lab_trends`/`markers` 指标趋势
- **`data_gaps` 关键数据缺口**：每个部位最近一次标准检查是什么时候、**有没有复查**、现在该补做什么——
  明确回答家属常问的"是没找到报告，还是根本没做这个检查"。
- **`exam_plan` 每个部位认准一种检查 + 多久查一次**：既解释"为什么尺寸对不上"，
  也相当于一份"正常随访/体检该做哪些检查"的清单（如 肺→薄层CT、甲状腺→超声、盆腔占位→增强MRI）。
- `top_issues` / `changes` 变好-没变-变差（**三类互斥、每件事只出现一次**）/ `risk_matrix` / `family_qa` / `actions` / `doctor_questions` / `conclusion`。

> 🩺 **"先检查、后手术"原则**：凡是缺最新数据的病灶，`actions.now` 一律先写"补做对应检查（认准同一种、和上一次比）"，
> 把"是否手术/治疗"放到 `actions.m1`（拿到结果 + 医生/多学科会诊后再定）。**不要在没有最新检查时就建议手术。**

**所有文字均来自原文或基于原文的克制解读；不确定处写"需医生确认"。**

### 4. 生成 HTML
```bash
python3 scripts/build_report.py patient.json 报告.html
```
生成单文件、自带样式、手机自适应的 HTML（表格可横滑、卡片自动单列）。

### 5.（可选）导出长图 + PDF
```bash
python3 scripts/export_pdf.py 报告.html 报告
# → 报告-long.png（一张长图，可发微信） + 报告.pdf（长图版 PDF）
```
需要 Chrome（无头）+ Python Pillow。

## 隐私（重要）
病历是高度敏感的个人数据。**默认本地处理、不部署公网。**
若用户要"手机打开"，优先建议：①把单文件 HTML/PDF 发到手机离线看；②局域网本地服务器；
③确需公网共享给异地家人时，使用**内容加密 + 密码**方案，并先与用户确认。
做演示 / 公开示例时，**必须使用完全虚构的化名数据**（见本 skill 的 `examples/`）。

## 文件
- `scripts/build_report.py` — JSON → HTML 生成器（渲染引擎，零依赖）
- `scripts/export_pdf.py` — HTML → 长图 PNG + PDF（需 Chrome + Pillow）
- `assets/schema.json` — 提取/汇总用的 JSON 结构
- `examples/sample_patient.json` — **虚构**示例数据
- `examples/sample_report.html` — 由示例数据生成的样例报告

## 配色约定
绿=稳定/低 · 黄=需关注 · 橙=中高 · 红=高/需尽快。务必让风险一眼可辨。
