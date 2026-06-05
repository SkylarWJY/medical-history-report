<div align="center">

# 🩺 Medical History Report · 病历全景报告

[中文](README.md) · **English**

### Someone in your family is ill — or you want to stay on top of your own health. Turn a pile of confusing reports into ONE report you can actually read and track over time.

*For caregivers AND self-trackers: turn messy medical records into one clear, longitudinal health report.*

<br>

**Built for two kinds of people 👇**

| | Who | What you get |
|---|---|---|
| 🏥 | **Caring for a sick family member** | A decade of **messy scans** (handwritten / rotated / mixed Chinese-English) → a **report the family can understand** ＋ **per-site tumor size tracking** ＋ **which exam is missing & what to do next** |
| 💪 | **Managing your own health** | Turn years of checkups / labs into **trends**, **auto-flag values that stay abnormal or are getting worse**, plus a **recheck calendar** — catch problems early instead of tossing the lab sheet in a drawer |

> The market is either clinic-grade EHRs, aggregators that pull **clean structured data** from hospital portals, or membership apps that **sell you blood tests**.
> **Almost no one** does "a pile of confusing old reports → something both you and your family can read, and keep tracking." That's why this exists.

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-D97757)
![Zero deps](https://img.shields.io/badge/HTML%20generator-zero%20dependencies-16a34a)
![Sample data](https://img.shields.io/badge/sample%20data-100%25%20fictional-7c3aed)

<br>

<img src="docs/demo.gif" width="720" alt="Scrolling report demo">

<sub>↑ A real generated report (data is a <b>fully fictional</b> sample patient "Lin Anran"; not a real person)</sub>

</div>

---

## ⚡ How it works: drop it in → get a report

This is a **Claude Skill**. Once installed, you **fill out nothing** —

```
①  Hand the reports to Claude          ②  Say one line              ③  Get the report
   (a patient's records, or your   →  "make me a health report" →   one HTML (export long image / PDF)
    own years of checkups)
```

Claude automatically: **reads each scan → extracts every lesion's size & date → consolidates → builds the report**.
Hundreds of files? No problem — it fans out multiple agents in parallel and finishes in minutes.

---

## 🎯 Two halves: understand the condition, then know what to do

> Exactly what a family needs: **first understand what's going on, then know what to do about it.**

### 📖 Part 1 — Understand the condition (what they "have", and how it changed)

| Section | What it gives you |
|---|---|
| 📍 **30-second read** | One-line verdict + a green/yellow/red split (better / unchanged / worse — each item appears only once) |
| 📜 **Diagnosis evolution** | How the diagnosis changed step by step, in one table |
| 📈 **Per-lesion size trail** | Each nodule is compared **only to itself**, every point labeled with **year-month + exam type** |
| 🫀 **By organ system** | Grouped by lung, thyroid, cardiovascular… |

### 🎯 Part 2 — Know what to do ("the action")

| Section | What it gives you |
|---|---|
| ⚠️ **Data gaps** | Which site is **missing a current exam** — never done, or just not found — and **which one to get now** |
| 🔬 **One exam per site + how often** | Why sizes never line up; what a proper follow-up / checkup should actually include |
| 🩺 **Examine first, decide surgery later** | Get the missing imaging first; surgery is decided after results are in |
| 📅 **Recheck calendar** | For each site: when next, which exam — a reminder list |
| ✅ **Questions for the doctor** | Print it and bring it to the visit |

> 🔒 **Hard rules**: everything is grounded in the source records, **nothing invented**; uncertainty is marked "needs doctor confirmation"; serious signals are flagged red.
> **It helps you understand and talk to doctors — it never replaces one.**

### 🆕 Health-tracking mode — not just for patients, but for staying healthy

Turn the **key markers from many checkups into one trend table**, automatically **flagging anything that stays abnormal or is trending worse** (e.g. "total cholesterol persistently high and slowly rising"), with a **recheck calendar** alongside.
Even if you're not sick, keep cholesterol, glucose, liver/kidney, thyroid, and tumor markers **tracked year over year** — catch issues early instead of forgetting last year's results.

---

## 🌟 Three things that set it apart from a generic "record summary"

1. **Same-site only, exam type labeled** — it won't mix "lung nodule" and "lymph node" in one table. Every number says which year-month and whether it's CT / ultrasound / PET, because **different machines simply don't measure the same way**.
2. **It tells you what exam is missing** — names each site's last standard exam and whether it was rechecked, answering the question families ask most: "is it not found, or was it never done?"
3. **"Examine first, decide surgery later"** — it doesn't push surgery without current imaging; get the exams first, let the doctor decide.

---

## 🖼️ A full report looks like this

<div align="center">
<img src="docs/full-report.png" width="620" alt="Full report">
<br><sub>One page, self-styled, works offline, looks good on a phone (sample is fictional data)</sub>
</div>

---

## 🚀 Or use it as a plain command-line tool

```bash
# Structured JSON → one HTML report (zero dependencies, ready to run)
python3 scripts/build_report.py examples/sample_patient.json out.html

# (optional) export a long image + PDF, easy to share
python3 scripts/export_pdf.py out.html out      # → out-long.png  +  out.pdf
```

## 🤖 Install as a Claude Skill

```bash
git clone https://github.com/SkylarWJY/medical-history-report \
  ~/.claude/skills/medical-history-report
```

Then hand your records to Claude and say "make me a health report." Claude follows the flow in [`SKILL.md`](SKILL.md).

## 📦 Repository layout

```
medical-history-report/
├─ SKILL.md                    # The workflow for Claude (incl. "same-site only / examine-first" rules)
├─ assets/schema.json          # Data spec for lesions / diagnoses / data-gaps / exam plan
├─ scripts/
│  ├─ build_report.py          # JSON → mobile-friendly HTML (zero deps, tested)
│  └─ export_pdf.py            # HTML → long PNG + PDF (Chrome + Pillow)
└─ examples/
   ├─ sample_patient.json      # Fictional sample data
   └─ sample_report.html       # A generated sample report
```

## 🔐 Privacy first

Medical records are the most sensitive personal data. This tool **processes locally by default — no upload, no public deployment**;
to view on a phone, just send the single file and open it offline. **Any demo / public example uses fictional data only.**

## 📄 License

[MIT](LICENSE) · Use it freely, and take good care of your family. ❤️

<div align="center"><sub>Built with Claude · If it helps you or your family, a ⭐ is appreciated</sub></div>
