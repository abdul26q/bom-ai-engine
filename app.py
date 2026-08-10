import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Component Obsolescence Engine", layout="wide")

st.title("⚡ AI Component Obsolescence & Substitute Engine")
st.write("Upload a Bill of Materials (CSV) to analyze lifecycle risks and generate verified engineering replacement recommendations.")

st.sidebar.header("🔑 Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def evaluate_component_with_ai(part_info, api_key):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an expert Electronics Hardware Engineer. 
    Analyze the following electronic component flagged as at-risk ({part_info['Status']}):

    - Component MPN: {part_info['MPN']}
    - Category: {part_info.get('Category', 'N/A')}
    - Package: {part_info.get('Package', 'N/A')}
    - Pins: {part_info.get('Pin_Count', 'N/A')}
    - Voltage: {part_info.get('Voltage_V', 'N/A')}V
    - Current: {part_info.get('Current_A', 'N/A')}A

    Provide an engineering evaluation:
    1. **Suggested Active Alternative:** Give an exact MPN for an active drop-in or functional substitute.
    2. **Pin-Compatibility:** State whether it is a direct drop-in replacement or requires PCB layout redesign.
    3. **Key Technical Differences:** List any differences in operating voltage, current handling, or package footprint.
    
    Keep the output concise, structured, and factual.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

uploaded_file = st.file_uploader("Upload BOM File (CSV format)", type=["csv"])

if uploaded_file:
    bom_df = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Bill of Materials")
    st.dataframe(bom_df, use_container_width=True)

    if st.button("Run AI Lifecycle Audit", type="primary"):
        if not openai_api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
            st.stop()

        results = []
        progress_bar = st.progress(0)
        total_items = len(bom_df)

        for idx, row in bom_df.iterrows():
            mpn = str(row.get("MPN") or row.get("Part Number")).strip()
            status = str(row.get("Status") or row.get("Lifecycle_Status", "Active")).strip()

            if status.upper() in ["OBSOLETE", "NRND", "EOL", "NOT RECOMMENDED"]:
                part_payload = {
                    "MPN": mpn,
                    "Status": status,
                    "Category": row.get("Category", "N/A"),
                    "Package": row.get("Package", "N/A"),
                    "Pin_Count": row.get("Pin_Count", "N/A"),
                    "Voltage_V": row.get("Voltage_V", "N/A"),
                    "Current_A": row.get("Current_A", "N/A")
                }
                
                with st.spinner(f"Analyzing replacement for {mpn}..."):
                    ai_recommendation = evaluate_component_with_ai(part_payload, openai_api_key)
            else:
                ai_recommendation = "✅ Part is Active. No replacement required."

            results.append({
                "Part Number": mpn,
                "Lifecycle Status": status,
                "AI Engineering Analysis": ai_recommendation
            })

            progress_bar.progress((idx + 1) / total_items)

        st.divider()
        st.subheader("Audit & Substitute Recommendations")
        
        for res in results:
            status = res["Lifecycle Status"]
            badge = "🔴" if status.upper() in ["OBSOLETE", "EOL"] else ("🟡" if status.upper() == "NRND" else "🟢")
            
            with st.expander(f"{badge} {res['Part Number']} — Status: {status}"):
                st.markdown(res["AI Engineering Analysis"])
