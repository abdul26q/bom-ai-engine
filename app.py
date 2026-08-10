import streamlit as st
import pandas as pd
from openai import OpenAI

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
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# 3. AI Hardware Reasoning Function
def evaluate_component_with_ai(part_info, api_key):
    """
    Sends component information to the LLM to verify lifecycle status 
    and recommend active parametric replacements.
    """
    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an expert Electronics Hardware and Sourcing Engineer.
    Analyze the following component from a Bill of Materials:

    - MPN (Part Number): {part_info['MPN']}
    - Manufacturer: {part_info.get('Manufacturer', 'N/A')}
    - Description: {part_info.get('Description', 'N/A')}
    - Category: {part_info.get('Category', 'N/A')}
    - Current File Status: {part_info.get('Status', 'Unknown')}

    Task:
    1. Determine or confirm the current industry lifecycle status (Active, NRND, or Obsolete/EOL).
    2. If the component is **Active**, explicitly state that it is safe to use.
    3. If the component is **NRND**, **Obsolete**, or **EOL**:
       - Provide an exact Manufacturer Part Number (MPN) for an active drop-in or functional substitute.
       - State whether the replacement is Pin-Compatible (Direct drop-in) or requires PCB layout redesign.
       - Detail any key technical differences (operating voltage, current rating, or package footprint).

    Keep the output concise, structured, and strictly factual.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2  # Low temperature prevents hallucinations
    )

    return response.choices[0].message.content

# 4. File Upload & Processing Interface
uploaded_file = st.file_uploader("Upload BOM File (CSV format)", type=["csv"])

if uploaded_file:
    bom_df = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Bill of Materials Data")
    st.dataframe(bom_df, use_container_width=True)

    if st.button("Run AI Lifecycle Audit", type="primary"):
        if not openai_api_key:
            st.error("Please enter your OpenAI API key in the sidebar configuration.")
            st.stop()

        results = []
        progress_bar = st.progress(0)
        total_items = len(bom_df)

        for idx, row in bom_df.iterrows():
            # Flexible column detection for different CSV formats
            mpn = str(
                row.get("MPN") or 
                row.get("Part Number") or 
                row.get("PartNumber") or 
                row.get("Item") or ""
            ).strip()

            # Check if status exists in CSV; if absent, flag for AI analysis
            status_in_file = str(
                row.get("Status") or 
                row.get("Lifecycle_Status") or 
                row.get("Lifecycle") or 
                "Check_AI"
            ).strip()

            part_payload = {
                "MPN": mpn,
                "Status": status_in_file,
                "Manufacturer": row.get("Manufacturer", "N/A"),
                "Description": row.get("Description", "N/A"),
                "Category": row.get("Category", "N/A"),
                "Package": row.get("Package", "N/A")
            }

            with st.spinner(f"Analyzing component [{idx + 1}/{total_items}]: {mpn}..."):
                # If explicit status is Active, skip AI; otherwise run full evaluation
                if status_in_file.upper() == "ACTIVE":
                    ai_recommendation = "✅ Component is Active according to uploaded BOM data. No replacement required."
                    detected_status = "Active"
                else:
                    ai_recommendation = evaluate_component_with_ai(part_payload, openai_api_key)
                    
                    # Inspect AI response to determine badge color
                    rec_upper = ai_recommendation.upper()
                    if "OBSOLETE" in rec_upper or "EOL" in rec_upper:
                        detected_status = "Obsolete / EOL"
                    elif "NRND" in rec_upper or "NOT RECOMMENDED" in rec_upper:
                        detected_status = "NRND"
                    else:
                        detected_status = "Active"

            results.append({
                "Part Number": mpn,
                "Lifecycle Status": detected_status,
                "AI Engineering Analysis": ai_recommendation
            })

            progress_bar.progress((idx + 1) / total_items)

        st.divider()
        st.subheader("Audit & Substitute Recommendations")

        # Display results in structured collapsible expanders
        for res in results:
            status = res["Lifecycle Status"]
            
            if status == "Obsolete / EOL":
                badge = "🔴"
            elif status == "NRND":
                badge = "🟡"
            else:
                badge = "🟢"

            with st.expander(f"{badge} {res['Part Number']} — Status: {status}"):
                st.markdown(res["AI Engineering Analysis"])
