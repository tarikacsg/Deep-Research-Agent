import asyncio
import json
import streamlit as st
from typing import Dict, Any

# OpenAI Agents SDK imports
from agents import Agent, Runner
from agents.tool import function_tool
from agents import set_default_openai_key

# Firecrawl for deep web research
from firecrawl import FirecrawlApp


# ======================================================
# Streamlit Page Configuration
# ======================================================
st.set_page_config(
    page_title="Deep Research Assistant",
    page_icon="📘",
    layout="wide"
)


# ======================================================
# Session State Initialization
# (Persists API keys across reruns)
# ======================================================
if "openai_key" not in st.session_state:
    st.session_state.openai_key = ""

if "firecrawl_key" not in st.session_state:
    st.session_state.firecrawl_key = ""


# ======================================================
# Sidebar – API Key Configuration
# ======================================================
with st.sidebar:
    st.title("🔑 API Configuration")

    openai_key_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.openai_key,
        type="password"
    )

    firecrawl_key_input = st.text_input(
        "Firecrawl API Key",
        value=st.session_state.firecrawl_key,
        type="password"
    )

    # Store keys in session state
    if openai_key_input:
        st.session_state.openai_key = openai_key_input
        set_default_openai_key(openai_key_input)

    if firecrawl_key_input:
        st.session_state.firecrawl_key = firecrawl_key_input


# ======================================================
# Main UI
# ======================================================
st.title("📘 Deep Research Assistant")
st.markdown(
    """
    This application performs **deep web research**, evaluates **source credibility**,
    produces a **high-quality research report**, and generates **follow-up research questions**.
    """
)

user_topic = st.text_input(
    "Enter a research topic:",
    placeholder="e.g., Interpretability methods for large language models"
)


# ======================================================
# Firecrawl Deep Research Tool
# ======================================================
@function_tool
async def perform_deep_research(
    query: str,
    crawl_depth: int,
    time_budget: int,
    url_limit: int
) -> Dict[str, Any]:
    """
    Calls Firecrawl's deep research endpoint.
    """
    try:
        firecrawl_client = FirecrawlApp(
            api_key=st.session_state.firecrawl_key
        )

        research_params = {
            "maxDepth": crawl_depth,
            "timeLimit": time_budget,
            "maxUrls": url_limit
        }

        # Optional callback for live crawl updates
        def activity_callback(activity):
            st.write(f"[{activity['type']}] {activity['message']}")

        with st.spinner("🌐 Crawling and analyzing the web..."):
            crawl_result = firecrawl_client.deep_research(
                query=query,
                params=research_params,
                on_activity=activity_callback
            )

        return {
            "analysis": crawl_result["data"]["finalAnalysis"],
            "sources": crawl_result["data"]["sources"],
            "success": True
        }

    except Exception as err:
        return {"success": False, "error": str(err)}


# ======================================================
# Agent 1 – Research Synthesis Agent
# ======================================================
research_synthesis_agent = Agent(
    name="research_synthesis_agent",
    instructions="""
You are a professional research assistant.

1. Use the deep research tool with:
   - crawl_depth = 3
   - time_budget = 180 seconds
   - url_limit = 10
2. Synthesize findings into a structured academic report.
3. Cite sources clearly.
4. Highlight key insights and consensus.
""",
    tools=[perform_deep_research]
)


# ======================================================
# Agent 2 – Source Credibility Evaluator
# ======================================================
source_quality_agent = Agent(
    name="source_quality_agent",
    instructions="""
You are an academic source evaluator.

From the research report:
- Identify all cited sources
- Score each source on:
  - Authority
  - Recency
  - Evidence quality
  - Bias risk

Return STRICT JSON in this format:
[
  {
    "title": "...",
    "url": "...",
    "credibility_score": 0-10,
    "strengths": "...",
    "weaknesses": "...",
    "justification": "..."
  }
]
"""
)


# ======================================================
# Agent 3 – Research Enhancement Agent
# ======================================================
research_expansion_agent = Agent(
    name="research_expansion_agent",
    instructions="""
You are a senior academic editor.

Enhance the research report by:
- Adding deeper explanations
- Including examples and case studies
- Incorporating trends and future outlooks
- Prioritizing high-credibility sources
- Flagging weak or biased evidence

Preserve academic rigor and structure.
"""
)


# ======================================================
# Agent 4 – Follow-Up Research Question Generator (NEW)
# ======================================================
followup_question_agent = Agent(
    name="followup_question_agent",
    instructions="""
You are a senior research scientist.

Based on the final research report:
1. Identify gaps, open problems, and weak evidence
2. Generate insightful follow-up research questions
3. Categorize them into:
   - Open Research Problems
   - Methodological Questions
   - Practical / Policy Implications
   - Future Research Directions

Return results in STRICT markdown with section headers.
Avoid generic questions.
"""
)


# ======================================================
# Full Research Pipeline
# ======================================================
async def execute_research_pipeline(topic: str) -> str:
    """
    Runs the full multi-agent research pipeline.
    """

    # -------- Step 1: Initial Research --------
    with st.spinner("📚 Conducting deep research..."):
        research_output = await Runner.run(
            research_synthesis_agent,
            topic
        )
        draft_report = research_output.final_output

    with st.expander("📄 Initial Research Report"):
        st.markdown(draft_report)

    # -------- Step 2: Source Credibility Evaluation --------
    with st.spinner("🧪 Evaluating source credibility..."):
        credibility_prompt = f"""
RESEARCH TOPIC:
{topic}

RESEARCH REPORT:
{draft_report}

Evaluate all cited sources.
"""
        credibility_output = await Runner.run(
            source_quality_agent,
            credibility_prompt
        )

    # Parse JSON safely
    try:
        source_scores = json.loads(credibility_output.final_output)
    except Exception:
        source_scores = []

    with st.expander("📊 Source Credibility Assessment"):
        if source_scores:
            st.dataframe(
                [
                    {
                        "Title": s["title"],
                        "URL": s["url"],
                        "Credibility": s["credibility_score"],
                        "Strengths": s["strengths"],
                        "Weaknesses": s["weaknesses"]
                    }
                    for s in source_scores
                ],
                use_container_width=True
            )
        else:
            st.markdown(credibility_output.final_output)

    # -------- Step 3: Report Enhancement --------
    with st.spinner("✨ Enhancing research report..."):
        enhancement_prompt = f"""
RESEARCH TOPIC:
{topic}

INITIAL REPORT:
{draft_report}

SOURCE EVALUATION:
{credibility_output.final_output}

Produce an enhanced academic research report.
"""
        enhanced_output = await Runner.run(
            research_expansion_agent,
            enhancement_prompt
        )
        final_report = enhanced_output.final_output

    # -------- Step 4: Follow-Up Research Questions --------
    with st.spinner("❓ Generating follow-up research questions..."):
        followup_prompt = f"""
RESEARCH TOPIC:
{topic}

FINAL REPORT:
{final_report}

Generate follow-up research questions.
"""
        followup_output = await Runner.run(
            followup_question_agent,
            followup_prompt
        )
        followup_questions = followup_output.final_output

    with st.expander("❓ Follow-Up Research Questions"):
        st.markdown(followup_questions)

    # Append questions to final report
    final_report += "\n\n---\n\n## ❓ Follow-Up Research Questions\n\n"
    final_report += followup_questions

    return final_report


# ======================================================
# Run Button
# ======================================================
if st.button(
    "🚀 Start Research",
    disabled=not (
        st.session_state.openai_key
        and st.session_state.firecrawl_key
        and user_topic
    )
):
    try:
        completed_report = asyncio.run(
            execute_research_pipeline(user_topic)
        )

        st.markdown("## 🧠 Final Research Report")
        st.markdown(completed_report)

        st.download_button(
            label="⬇️ Download Report (Markdown)",
            data=completed_report,
            file_name=f"{user_topic.replace(' ', '_')}_research.md",
            mime="text/markdown"
        )

    except Exception as exc:
        st.error(f"Pipeline failed: {exc}")


# ======================================================
# Footer
# ======================================================
st.markdown("---")
st.markdown("Powered by **OpenAI Agents SDK** and **Firecrawl**")
