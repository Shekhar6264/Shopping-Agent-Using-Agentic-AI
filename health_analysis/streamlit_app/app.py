from dotenv import load_dotenv
import streamlit as st
import os
import html

from langchain_groq import ChatGroq

# Load environment variables
load_dotenv(
    r"C:\Users\shekh\OneDrive\Desktop\Tutorial Agentic AI\.env",
    override=True
)

# Configure Streamlit
st.set_page_config(
    page_title="Blood Work Analyzer",
    layout="wide"
)

# Initialize Groq LLM
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    max_retries=0
)

# Custom CSS
st.markdown("""
<style>
.scroll-box {
    height: 230px;
    overflow-y: auto;
    padding: 12px 16px;
    border: 1px solid #444;
    border-radius: 8px;
    background-color: #1e1e1e;
    font-size: 0.9rem;
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}
.section-label {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 6px;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Page title
st.title("🩸 Blood Work Analyzer")
st.caption("Extract blood test results and generate a general health summary.")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Blood Work Report")

    blood_report = st.text_area(
        label="Paste your report below",
        height=500,
        placeholder="Paste your blood work report here...",
        label_visibility="collapsed"
    )

    analyze_clicked = st.button(
        "Analyze",
        type="primary",
        use_container_width=True
    )

with right_col:
    st.subheader("Health Summary")
    health_box = st.empty()
    health_box.markdown(
        '<div class="scroll-box"></div>',
        unsafe_allow_html=True
    )

    st.subheader("Suggested Diet Plan")
    diet_box = st.empty()
    diet_box.markdown(
        '<div class="scroll-box"></div>',
        unsafe_allow_html=True
    )

# Analyze report
if analyze_clicked:

    if not blood_report.strip():
        st.warning("Please paste a blood work report before analyzing.")

    else:
        try:
            with st.spinner("Analyzing your blood work..."):

                # ==========================================
                # STAGE 1: EXTRACT AND FLAG ABNORMAL VALUES
                # ==========================================

                extraction_prompt = f"""
You are a medical data extraction assistant.

Extract ALL test results from the blood report below.

For each test:
- Extract the test name and measured value.
- Use the reference range provided in the report.
- Classify the result as HIGH, LOW, or NORMAL.
- If the reference range is missing or classification is
  unclear, use UNDETERMINED.
- Do not invent test values or reference ranges.

Format:
- Test Name: value | Status: HIGH/LOW/NORMAL/UNDETERMINED
  | Reference: range

Blood Report:
{blood_report}
"""

                extraction_response = llm.invoke(extraction_prompt)

                extracted_values = extraction_response.content

                # ==========================================
                # STAGE 2: HEALTH SUMMARY AND DIET PLAN
                # ==========================================

                diet_prompt = f"""
You are a health information assistant familiar with
Indian dietary habits.

Use ONLY the blood work analysis below.

Produce exactly these two sections:

SECTION 1 - HEALTH SUMMARY:
Write 4-5 short lines explaining the results in simple,
non-technical language.

Mention important abnormal results and their possible
significance. Do not diagnose a disease from blood results
alone. Do not invent missing information.

SECTION 2 - INDIAN DIET PLAN:

Foods to avoid:
- List relevant foods to limit or avoid.

Foods to eat more of:
- Suggest practical Indian foods such as dal, sabzi,
  vegetables, fruits, whole grains, and other suitable
  foods according to the reported results.

Keep recommendations relevant to the actual results.
Do not prescribe medication or supplements.

If the report does not provide enough information for a
specific recommendation, state this clearly.

Blood Work Analysis:
{extracted_values}
"""

                diet_response = llm.invoke(diet_prompt)

                full_response = diet_response.content

            # ==========================================
            # SPLIT THE OUTPUT INTO TWO SECTIONS
            # ==========================================

            if "SECTION 2" in full_response:

                parts = full_response.split("SECTION 2", 1)

                health_summary = (
                    parts[0]
                    .replace("SECTION 1 - HEALTH SUMMARY:", "")
                    .replace("SECTION 1:", "")
                    .replace("SECTION 1", "")
                    .strip()
                )

                diet_plan = (
                    parts[1]
                    .replace("- INDIAN DIET PLAN:", "")
                    .replace(" - INDIAN DIET PLAN:", "")
                    .strip()
                )

            else:
                health_summary = full_response
                diet_plan = (
                    "The response could not be separated into "
                    "the expected sections. Please analyze again."
                )

            # ==========================================
            # DISPLAY RESULTS SAFELY
            # ==========================================

            health_box.markdown(
                f'<div class="scroll-box">'
                f'{html.escape(health_summary)}</div>',
                unsafe_allow_html=True
            )

            diet_box.markdown(
                f'<div class="scroll-box">'
                f'{html.escape(diet_plan)}</div>',
                unsafe_allow_html=True
            )

            # Optional: show Stage 1 output for verification
            with st.expander("View extracted blood test values"):
                st.text(extracted_values)

            st.caption(
                "Educational information only. "
                "Consult a qualified healthcare professional "
                "for medical interpretation."
            )

        except Exception as e:
            st.error(
                "An error occurred while analyzing the report. "
                "Check your Groq model availability, API quota, "
                "and connection."
            )
            st.code(f"{type(e).__name__}: {e}")