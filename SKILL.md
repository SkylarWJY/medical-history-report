---
name: medical-history-report
description: >-
  Turn a person's multi-year medical records (scanned reports, lab results,
  imaging, ultrasound, CT/MRI, PET-CT, pathology, discharge summaries) into a
  single self-contained, mobile-friendly HTML health dashboard for family
  members — with a disease timeline, a diagnosis-evolution table, per-lesion
  size-tracking tables (how each nodule/mass changed over the years), lab trend
  charts, risk cards, a plain-language family explanation, and a doctor-visit
  checklist. Use when someone provides a folder or zip of medical records
  (especially many scanned images) and wants a clear visual summary of overall
  health status, disease progression, key risks, and next steps. Output is
  always evidence-based, flags uncertainty as "需医生确认", and never replaces a
  doctor. Can also export the report to a long PNG image and a PDF.
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
关键是 `lesions[]`：把同一病灶历次尺寸**按时间排序**，标注 trend（up/down/flat），
这样报告里就能呈现"附件占位 2015→2025 的精确大小轨迹"。

### 3. 汇总成结构化 JSON
按器官系统归类、画出诊断演变史（`evolution`）、整理指标趋势（`lab_trends`/`markers`）、
写 Top 问题、变好/变差/稳定四分类、风险矩阵、家属版解释、行动建议、问医生清单、最终结论。
**所有文字均来自原文或基于原文的克制解读**。

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
