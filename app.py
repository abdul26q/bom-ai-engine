import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

st.set_page_config(
    page_title="AI Component Obsolescence & Substitute Engine", 
    layout="wide",
    page_icon="⚡"
)

st.title("⚡ AI Component Obsolescence & Substitute Engine")
st.write("Upload a Bill of Materials (CSV) to analyze lifecycle risks and generate verified engineering replacement recommendations.")

# Sidebar Configuration
st.sidebar.header("🔑 Configuration")
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password")

def analyze_entire_bom(bom_data_str, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an expert Electronics Hardware and Sourcing Engineer.
    Analyze the following list of electronic components from a Bill of Materials:

    {bom_data_str}

    Task:
    For EACH component listed in the BOM:
    1. Determine or confirm the current industry lifecycle status (Active, NRND, or Obsolete/EOL).
    2. If **Active**, confirm it is safe to use.
    3. If **NRND** or **Obsolete/EOL**:
       - Provide an exact Manufacturer Part Number (MPN) for an active drop-in or functional substitute.
       - State whether it is Pin-Compatible (Direct drop-in) or requires PCB layout redesign.
       - Detail key technical differences (voltage, current rating, footprint).

    Respond in valid JSON format as a list of objects like this:
    [
      {{
        "mpn": "STM32F103C8T6",
        "status": "Active" | "NRND" | "Obsolete",
        "analysis": "Markdown detailed analysis text"
      }}
    ]
    Do not wrap in backticks or markdown, output pure JSON array.
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean potential markdown formatting
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None

# Upload Interface
uploaded_file = st.file_uploader("Upload BOM File (CSV format)", type=["csv"])

if uploaded_file:
    bom_df = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Bill of Materials Data")
    st.dataframe(bom_df, use_container_width=True)

    if st.button("Run AI Lifecycle Audit", type="primary"):
        if not gemini_api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
            st.stop()

        with st.spinner("Analyzing full BOM with AI in a single batch request..."):
            bom_summary = []
            for _, row in bom_df.iterrows():
                mpn = str(row.get("MPN") or row.get("Part Number") or row.get("Item Number") or "").strip()
                desc = str(row.get("Description", "")).strip()
                mfr = str(row.get("Manufacturer", "")).strip()
                bom_summary.append(f"MPN: {mpn} | Manufacturer: {mfr} | Description: {desc}")

            bom_data_str = "\n".join(bom_summary)
            results = analyze_entire_bom(bom_data_str, gemini_api_key)

        st.divider()
        st.subheader("Audit & Substitute Recommendations")

        if results:
            for item in results:
                status = item.get("status", "Active")
                mpn = item.get("mpn", "Unknown")
                analysis = item.get("analysis", "No data")

                if "Obsolete" in status or "EOL" in status:
                    badge = "🔴"
                elif "NRND" in status:
                    badge = "🟡"
                else:
                    badge = "🟢"

                with st.expander(f"{badge} {mpn} — Status: {status}"):
                    st.markdown(analysis)
