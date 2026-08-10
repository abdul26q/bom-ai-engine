import streamlit as st
import pandas as pd
from groq import Groq
import json

# 1. Page Configuration
st.set_page_config(
    page_title="AI Component Obsolescence & Substitute Engine", 
    layout="wide",
    page_icon="⚡"
)

st.title("⚡ AI Component Obsolescence & Substitute Engine")
st.write("Upload a Bill of Materials (CSV) to analyze lifecycle risks and generate verified engineering replacement recommendations.")

# 2. Sidebar Configuration
st.sidebar.header("🔑 Configuration")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get a free API key at console.groq.com")

# 3. Batch Analysis Function using Groq
def analyze_entire_bom_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

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
           - Detail key technical differences (voltage rating, current rating, footprint, or package).

        Respond STRICTLY in valid raw JSON array format as a list of objects like this:
        [
          {{
            "mpn": "STM32F103C8T6",
            "status": "Active",
            "analysis": "Markdown detailed analysis text"
          }}
        ]
        Do not wrap in code blocks or include conversational text. Output pure JSON only.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        text = response.choices[0].message.content.strip()
        
        # Clean JSON formatting wrappers if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
        
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None

# 4. Upload & UI Processing Interface
uploaded_file = st.file_uploader("Upload BOM File (CSV format)", type=["csv"])

if uploaded_file:
    bom_df = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Bill of Materials Data")
    st.dataframe(bom_df, use_container_width=True)

    if st.button("Run AI Lifecycle Audit", type="primary"):
        if not groq_api_key:
            st.error("Please enter your Groq API key in the sidebar configuration.")
            st.stop()

        with st.spinner("Analyzing full BOM using Groq Llama-3.3-70B in a single request..."):
            bom_summary = []
            for _, row in bom_df.iterrows():
                mpn = str(
                    row.get("MPN") or 
                    row.get("Part Number") or 
                    row.get("Item Number") or 
                    row.get("Item") or ""
                ).strip()
                desc = str(row.get("Description", "")).strip()
                mfr = str(row.get("Manufacturer", "")).strip()
                bom_summary.append(f"MPN: {mpn} | Manufacturer: {mfr} | Description: {desc}")

            bom_data_str = "\n".join(bom_summary)
            results = analyze_entire_bom_with_groq(bom_data_str, groq_api_key)

        st.divider()
        st.subheader("Audit & Substitute Recommendations")

        if results:
            for item in results:
                status = item.get("status", "Active")
                mpn = item.get("mpn", "Unknown")
                analysis = item.get("analysis", "No analysis provided.")

                if "Obsolete" in status or "EOL" in status:
                    badge = "🔴"
                elif "NRND" in status:
                    badge = "🟡"
                else:
                    badge = "🟢"

                with st.expander(f"{badge} {mpn} — Status: {status}"):
                    st.markdown(analysis)
