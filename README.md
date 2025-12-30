# 📘 OpenAI Deep Research Agent

A **multi-agent, web-scale research assistant** that performs deep web research, evaluates source credibility, generates **academically rigorous research reports**, and proposes **high-quality follow-up research questions** using **OpenAI Agents SDK**, **Firecrawl**, and **Streamlit**.

This project goes beyond simple web search or summarization by:

- Crawling and synthesizing information across multiple sources  
- Scoring source credibility (authority, recency, bias, evidence quality)  
- Producing enhanced, structured, and defensible research reports  
- Identifying research gaps and generating follow-up research questions  

---

## 🚀 Features

### 🔍 Deep Web Research
- Uses Firecrawl’s **Deep Research API** to crawl and analyze multiple authoritative sources  
- Configurable crawl depth, time limits, and URL budgets  
- Real-time crawling updates displayed in the UI  

---

### 🧠 Multi-Agent Architecture

The system is built as a **modular, multi-agent pipeline**, where each agent has a clearly defined responsibility:

- **Research Agent**  
  Conducts deep web research and synthesizes findings into an initial academic report  

- **Source Evaluation Agent**  
  Evaluates the credibility of cited sources  

- **Elaboration Agent**  
  Enhances clarity, depth, structure, and academic rigor  

- **Follow-Up Question Agent (NEW)**  
  Identifies gaps, unresolved debates, and future directions, and generates structured follow-up research questions  

This separation improves interpretability, extensibility, and research quality.

---

### 📊 Source Credibility Evaluation

Each cited source is evaluated on:

- **Authority** (publisher / author expertise)  
- **Recency**  
- **Evidence quality**  
- **Bias risk**  
- **Overall credibility score (0–10)**  

Results are displayed in a **sortable, interactive Streamlit table**, making source quality explicit rather than implicit.

---

### 📝 Enhanced Research Reports

Final reports include:

- Structured academic writing  
- Expanded explanations of complex concepts  
- Real-world examples and case studies  
- Trends, future directions, and implications  
- Explicit prioritization of **high-credibility sources**  
- Flagging of weak or biased evidence when relevant  

---

### ❓ Follow-Up Research Questions (NEW)

After generating the final enhanced report, the system automatically proposes **high-quality follow-up research questions**, categorized into:

- **Open Research Problems**  
- **Methodological / Evaluation Questions**  
- **Practical or Policy Implications**  
- **Future Research Directions**  

These questions are:
- Non-generic  
- Grounded in identified gaps or weak evidence  
- Suitable for academic research, proposals, or exploratory work  

They are displayed in the UI and appended to the final report.

---

### ⬇️ Export & Reproducibility

- Download final reports as **Markdown**  
- Deterministic pipeline given the same inputs and parameters  
- Clear intermediate outputs for transparency and debugging  

---

### 🖥️ Demo UI

Built with **Streamlit**, featuring:

- Secure API key input (not stored)  
- Topic-driven research workflow  
- Expandable sections for:
  - Initial research report  
  - Source credibility evaluation  
  - Follow-up research questions  
- Interactive source credibility table  

---

## 🧩 System Architecture

```text
User Input (Research Topic)
        |
        v
+-------------------------+
| Research Agent          |
| (Firecrawl Deep Crawl)  |
+-------------------------+
        |
        v
+-------------------------+
| Source Evaluation Agent |
+-------------------------+
        |
        v
+-------------------------+
| Elaboration Agent       |
+-------------------------+
        |
        v
+-------------------------+
| Follow-Up Question      |
| Generation Agent        |
+-------------------------+
        |
        v
Final Enhanced Report
+ Follow-Up Research Questions
