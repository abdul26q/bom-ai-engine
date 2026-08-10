import streamlit as st
import pandas as pd
from groq import Groq
import json
import os

# 1. Modern Page Setup & Custom Styling
st.set_page_config(
    page_title="TraceGuard AI | Component Risk Engine", 
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)



def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return BACKEND_GROQ_KEY

# Custom CSS for executive UI polish
st.markdown("""
<style>
    /* Metric Card Styling */
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetric"] {
        background-color: #1E293B;
        padding: 15px 20px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    
    /* Headers & Typography */
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #E11D48 0%, #F97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 2rem;
    }
    
    /* Comparison Boxes */
    .comp-box-original {
        background-color: #1E1B4B;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #6366F1;
        margin-bottom: 10px;
    }
    .comp-box-recommended {
        background-color: #064E3B;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin-bottom: 10px;
    }
    .box-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .title-orig { color: #A5B4FC; }
    .title-rec { color: #6EE7B7; }
    
    .part-mpn {
        font-size: 1.25rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Clean Header Section (Logo Image + Main Header)
if os.path.exists("logo.png"):
    st.image("logo.png", width=160)

st.markdown('<div class="main-header">TraceGuard AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated BOM Lifecycle Risk Auditing & Drop-in Substitute Intelligence</div>', unsafe_allow_html=True)

# 2. Sidebar Layout
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    st.title("System Status")
    st.success("⚡ TraceGuard Core: Online")
    
    st.markdown("---")
    st.markdown("### 📋 Executive Summary Guide")
    st.caption("• **Active (🟢):** Safe for full mass production.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs.")
    st.caption("• **Obsolete/EOL (🔴):** Immediate substitute required.")

# 3. Batch Analysis Engine via Groq
def analyze_entire_bom_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert Electronics Hardware, Component Sourcing, and Supply Chain Engineer.
        Analyze the following list of electronic components from a Bill of Materials:

        {bom_data_str}

        Task:
        For EACH component listed in the BOM:
        1. Determine or confirm the current industry lifecycle status (Active, NRND, or Obsolete/EOL).
        2. If **Active**, confirm it is production-ready.
        3. If **NRND** or **Obsolete/EOL**:
           - Provide an exact Manufacturer Part Number (MPN) for an active drop-in or functional substitute.
           - State whether it is **Pin-Compatible (Direct Drop-in)** or requires **PCB Layout Redesign**.
           - Summarize key technical differences in 1-2 bullet points (voltage, footprint, current rating).

        Respond STRICTLY in valid raw JSON array format as a list of objects like this:
        [
          {{
            "mpn": "STM32F103C8T6",
            "manufacturer": "STMicroelectronics",
            "status": "NRND",
            "substitute": "STM32G071CBT6",
            "substitute_mfr": "STMicroelectronics",
            "pin_compatible": "No (PCB Redesign Required)",
            "key_differences": "Lower power, ARM Cortex-M0+ core, updated pinouts.",
            "analysis": "Part is flagged as Not Recommended for New Designs by STMicroelectronics. Transitioning to STM32G0 series is recommended."
          }}
        ]
        Do not wrap in triple backticks or write conversational text. Output pure JSON only.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        text = response.choices[0].message.content.strip()
        
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

# 4. Upload & Dashboard Interface
uploaded_file = st.file_uploader("Upload Bill of Materials (CSV)", type=["csv"], help="Upload CSV containing MPN, Description, or Manufacturer columns.")

if uploaded_file:
    bom_df = pd.read_csv(uploaded_file)
    
    with st.expander("📄 Raw Uploaded BOM Data Preview", expanded=False):
        st.dataframe(bom_df, use_container_width=True)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run_audit = st.button("🚀 Run TraceGuard Risk Audit", type="primary", use_container_width=True)

    if run_audit:
        active_key = get_api_key()

        with st.spinner("🤖 TraceGuard AI analyzing component lifecycles & cross-referencing drop-in substitutes..."):
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
            results = analyze_entire_bom_with_groq(bom_data_str, active_key)

        st.markdown("---")

        if results:
            total_parts = len(results)
            nrnd_count = sum(1 for x in results if "NRND" in str(x.get("status", "")).upper())
            obsolete_count = sum(1 for x in results if any(term in str(x.get("status", "")).upper() for term in ["OBSOLETE", "EOL"]))
            active_count = total_parts - (nrnd_count + obsolete_count)
            
            risk_index = round(((obsolete_count * 1.0 + nrnd_count * 0.5) / max(total_parts, 1)) * 100, 1)

            # Executive KPI Cards
            st.subheader("📊 Executive Risk Overview")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Line Items", total_parts)
            m2.metric("Active Components", active_count, delta="Mass Production Ready", delta_color="normal")
            m3.metric("At-Risk Items", nrnd_count + obsolete_count, delta=f"{obsolete_count} EOL | {nrnd_count} NRND", delta_color="inverse")
            m4.metric("BOM Risk Index", f"{risk_index}%", delta="Critical Action Needed" if risk_index > 15 else "Low Risk", delta_color="inverse")

            st.markdown("---")
            st.subheader("🔍 Component Comparison & Substitute Matrix")

            export_rows = []

            for item in results:
                status = str(item.get("status", "Active"))
                mpn = str(item.get("mpn", "Unknown"))
                mfr = str(item.get("manufacturer", "N/A"))
                substitute = str(item.get("substitute", "N/A"))
                sub_mfr = str(item.get("substitute_mfr", "N/A"))
                pin_compat = str(item.get("pin_compatible", "N/A"))
                diffs = str(item.get("key_differences", "None noted."))
                analysis = str(item.get("analysis", "No analysis provided."))

                status_upper = status.upper()
                if "OBSOLETE" in status_upper or "EOL" in status_upper:
                    badge = "🔴 OBSOLETE / EOL"
                elif "NRND" in status_upper:
                    badge = "🟡 NRND (NOT RECOMMENDED)"
                else:
                    badge = "🟢 ACTIVE"

                search_url = f"[https://www.mouser.com/c/?q=](https://www.mouser.com/c/?q=){substitute if substitute != 'N/A' else mpn}"

                # Expander Card with Side-by-Side Comparison
                with st.expander(f"{badge}  |  Part Number: {mpn}"):
                    c_left, c_right = st.columns(2)
                    
                    # Left Side: Current Component
                    with c_left:
                        st.markdown(f"""
                        <div class="comp-box-original">
                            <div class="box-title title-orig">Current BOM Component</div>
                            <div class="part-mpn">{mpn}</div>
                            <p style="margin-bottom: 4px;"><b>Manufacturer:</b> {mfr}</p>
                            <p style="margin-bottom: 0px;"><b>Status:</b> {status}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Right Side: TraceGuard Recommended Substitute
                    with c_right:
                        st.markdown(f"""
                        <div class="comp-box-recommended">
                            <div class="box-title title-
