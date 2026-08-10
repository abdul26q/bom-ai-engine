import streamlit as st
import pandas as pd
from groq import Groq
import json

# 1. Modern Page Setup & Custom Styling
st.set_page_config(
    page_title="BOM Sentinel | AI Obsolescence & Risk Engine", 
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
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 2rem;
    }
    
    /* Result Cards Styling */
    .result-card {
        background-color: #0F172A;
        border-radius: 10px;
        padding: 18px;
        margin-top: 10px;
        border: 1px solid #1E293B;
    }
    .spec-label {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .spec-value {
        font-size: 1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title Section
st.markdown('<div class="main-header">🛡️ BOM Sentinel AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Component Lifecycle Risk Auditing & Drop-in Substitute Intelligence</div>', unsafe_allow_html=True)

# 2. Sidebar Layout
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/circuit.png", width=70)
    st.title("System Status")
    st.success("⚡ Groq Engine: Online & Connected")
    
    st.markdown("---")
    st.markdown("### 📋 Executive Summary Guide")
    st.caption("• **Active (🟢):** Safe for full mass production.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs. Sourcing risk expected.")
    st.caption("• **Obsolete/EOL (🔴):** Out of production. Immediate substitute required.")

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
            "status": "NRND",
            "substitute": "STM32G071CBT6",
            "pin_compatible": "No (PCB Redesign Required)",
            "key_differences": "Lower power consumption, updated ARM Cortex-M0+ core, different pin mapping.",
            "analysis": "Part is flagged as Not Recommended for New Designs by STMicroelectronics. Transitioning to STM32G0 series is recommended for long-term production."
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
        
        # Clean formatting wrappers if present
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
        run_audit = st.button("🚀 Run AI Lifecycle Audit", type="primary", use_container_width=True)

    if run_audit:
        active_key = get_api_key()

        with st.spinner("🤖 Analyzing component lifecycles & cross-referencing drop-in substitutes..."):
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
            m1.metric("Total Components", total_parts)
            m2.metric("Active Components", active_count, delta="Mass Production Ready", delta_color="normal")
            m3.metric("At-Risk Line Items", nrnd_count + obsolete_count, delta=f"{obsolete_count} EOL | {nrnd_count} NRND", delta_color="inverse")
            m4.metric("BOM Risk Index", f"{risk_index}%", delta="Critical Action Needed" if risk_index > 15 else "Low Risk", delta_color="inverse")

            st.markdown("---")
            st.subheader("🔍 Component Breakdown & Substitute Recommendations")

            export_rows = []

            for item in results:
                status = str(item.get("status", "Active"))
                mpn = str(item.get("mpn", "Unknown"))
                substitute = str(item.get("substitute", "N/A"))
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

                search_url = f"https://www.mouser.com/c/?q={mpn}"

                # Expander Card for each component
                with st.expander(f"{badge}  |  Part Number: {mpn}"):
                    c1, c2, c3 = st.columns([1.2, 1.2, 1.6])
                    
                    with c1:
                        st.markdown('<div class="spec-label">Suggested Substitute</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="spec-value"><code>{substitute}</code></div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="spec-label">Sourcing Verification</div>', unsafe_allow_html=True)
                        st.markdown(f'[🔗 Verify Part on Mouser Catalog]({search_url})')

                    with c2:
                        st.markdown('<div class="spec-label">Pinout Compatibility</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="spec-value">{pin_compat}</div>', unsafe_allow_html=True)

                    with c3:
                        st.markdown('<div class="spec-label">Key Spec Differences</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="spec-value" style="font-size:0.95rem; font-weight:500;">{diffs}</div>', unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown('<div class="spec-label">Engineering Risk Analysis</div>', unsafe_allow_html=True)
                    st.write(analysis)

                export_rows.append({
                    "MPN": mpn,
                    "Lifecycle Status": status,
                    "Recommended Substitute": substitute,
                    "Pin Compatible": pin_compat,
                    "Key Differences": diffs,
                    "Engineering Analysis": analysis
                })

            # CSV Download Section
            st.markdown("---")
            export_df = pd.DataFrame(export_rows)
            csv_data = export_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Export Audited Risk Report (CSV)",
                data=csv_data,
                file_name="BOM_Sentinel_Risk_Report.csv",
                mime="text/csv",
                type="primary"
            )
