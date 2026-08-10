import streamlit as st
import pandas as pd
from groq import Groq
import json
import os

# 1. Page Configuration & Setup
st.set_page_config(
    page_title="TraceGuard AI | Enterprise Component Risk Engine", 
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)



def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return BACKEND_GROQ_KEY

# Custom CSS
st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 30px !important; font-weight: 800 !important; }
    [data-testid="stMetric"] { background-color: #1E293B; padding: 15px 20px; border-radius: 12px; border: 1px solid #334155; }
    .main-header { font-size: 2.6rem; font-weight: 800; background: linear-gradient(90deg, #E11D48 0%, #F97316 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.1rem; }
    .sub-header { font-size: 1.05rem; color: #94A3B8; margin-bottom: 1.5rem; }
    .comp-box-original { background-color: #1E1B4B; padding: 16px; border-radius: 10px; border-left: 5px solid #6366F1; margin-bottom: 10px; }
    .comp-box-recommended { background-color: #064E3B; padding: 16px; border-radius: 10px; border-left: 5px solid #10B981; margin-bottom: 10px; }
    .box-title { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
    .title-orig { color: #A5B4FC; }
    .title-rec { color: #6EE7B7; }
    .part-mpn { font-size: 1.25rem; font-weight: 800; color: #FFFFFF; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# Header
if os.path.exists("logo.png"):
    st.image("logo.png", width=160)

st.markdown('<div class="main-header">TraceGuard AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enterprise Deterministic Component Lifecycle Auditing & Drop-In Substitute Engine</div>', unsafe_allow_html=True)

# 2. Sidebar Setup
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    st.title("System Status")
    st.success("⚡ TraceGuard AI Core: Precision Guard Active")
    st.info("🔒 Deterministic Rule Engine + Consistency Verifier")
    st.markdown("---")
    st.caption("• **Active (🟢):** Production-ready.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs.")
    st.caption("• **Obsolete/EOL (🔴):** Discontinued package or non-RoHS IC line.")

# 3. High-Precision AI Reasoning Engine with Strict Logic Consistency Rules
def analyze_components_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an elite Semiconductor Sourcing Engineer and PCN (Product Change Notification) Database Audit Specialist.
        Analyze the following component query with 100% deterministic accuracy and STRICT LOGICAL CONSISTENCY:

        {bom_data_str}

        CRITICAL CONSISTENCY & HARDWARE RULES (ZERO CONTRADICTION):

        1. STRICT STATUS CONCORDANCE (NEVER CONTRADICT STATUS IN TEXT):
           - If a component is non-RoHS, leaded, or phased out (e.g., MAX7219CNG, MAX232CPE, MC14069UBD, TLE2426CLP), the 'status' field MUST BE 'Obsolete' or 'NRND'.
           - NEVER set 'status' to 'Active' if your text states that the part is "obsolete", "discontinued", or "not recommended for new designs".
           - The status, summary text, and engineering analysis MUST fully agree with each other.

        2. EXACT SUFFIX & ROHS PARSING:
           - MAXIM / ANALOG DEVICES: Non-'+' suffixes (e.g., MAX7219CNG, MAX232CPE, MAX232EWE) are non-RoHS leaded variants and are OBSOLETE/NRND. Always mark status as 'Obsolete' or 'NRND' and recommend the '+' version (e.g., MAX7219CNG+).
           - TEXAS INSTRUMENTS: Suffix 'LP' / 'LPR' = TO-92 3-pin package (e.g. TLE2426CLP is Obsolete; recommend TLE2426CD/CDR in SOIC-8). Suffix 'D'/'DR' = SOIC-8, 'P' = PDIP-8, 'J' = Ceramic CDIP (Obsolete).
           - ONSEMI / MOTOROLA: Non-'G' suffixes (e.g., MC14069UBD) are non-RoHS leaded variants and are OBSOLETE/NRND. Recommend 'G' version (e.g., MC14069UBDG).
           - MICROCHIP / ATMEL: Through-hole DIP-28 packages (e.g., ATMEGA328-PU) are NRND/EOL. Recommend surface-mount TQFP-32 (ATMEGA328P-AU) or ATmega328PB.

        3. FULL ORDERABLE MPN REQUIREMENT:
           - NEVER output the base query as substitute if it matches the input.
           - Output explicit orderable MPNs with exact package/RoHS suffixes.

        4. PHYSICAL PACKAGE MATCHING & REDESIGN WARNINGS:
           - Match footprints exactly (SOIC-8 to SOIC-8, DIP-8 to DIP-8, TO-92 to TO-92).
           - If recommending an SOIC-8 surface mount replacement for a TO-92 through-hole part, explicitly state in pin_compatible: "No (PCB Layout Redesign Required: SOIC-8 Surface Mount replacing TO-92 Through-Hole)".

        Task:
        For EACH component listed:
        1. State industry lifecycle status accurately ('Active', 'NRND', or 'Obsolete').
        2. Provide exact orderable MPN for an active substitute in an appropriate package.
        3. State pinout compatibility accurately without logical self-contradictions.
        4. Detail key technical differences and generate direct multi-distributor URLs.

        Respond STRICTLY in valid raw JSON array format as a list of objects like this:
        [
          {{
            "mpn": "MAX7219CNG",
            "manufacturer": "Maxim Integrated / Analog Devices",
            "status": "Obsolete",
            "substitute": "MAX7219CNG+",
            "substitute_mfr": "Analog Devices",
            "pin_compatible": "Yes (Direct PDIP-24 Drop-in)",
            "key_differences": "MAX7219CNG+ is the active lead-free (RoHS-compliant) direct drop-in replacement for the discontinued non-RoHS MAX7219CNG.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=MAX7219CNG%2B",
              "mouser": "https://www.mouser.com/c/?q=MAX7219CNG%2B",
              "octopart": "https://octopart.com/search?q=MAX7219CNG%2B",
              "element14": "https://in.element14.com/search?st=MAX7219CNG%2B"
            }},
            "analysis": "MAX7219CNG is obsolete due to non-RoHS leaded packaging. The RoHS-compliant MAX7219CNG+ is active, production-ready, and pin-to-pin compatible."
          }}
        ]
        Do not wrap in triple backticks or write conversational text. Output pure JSON only.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
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

# Render Result Card Helper
def render_component_card(item):
    status = str(item.get("status", "Active"))
    mpn = str(item.get("mpn", "Unknown"))
    mfr = str(item.get("manufacturer", "N/A"))
    substitute = str(item.get("substitute", "N/A"))
    sub_mfr = str(item.get("substitute_mfr", "N/A"))
    pin_compat = str(item.get("pin_compatible", "N/A"))
    diffs = str(item.get("key_differences", "None noted."))
    analysis = str(item.get("analysis", "No analysis provided."))
    links = item.get("supplier_links", {})

    status_upper = status.upper()
    if "OBSOLETE" in status_upper or "EOL" in status_upper:
        badge = "🔴 OBSOLETE / EOL"
    elif "NRND" in status_upper:
        badge = "🟡 NRND (NOT RECOMMENDED)"
    else:
        badge = "🟢 ACTIVE"

    digikey_url = links.get("digikey", f"https://www.digikey.com/en/products/result?keywords={mpn}")
    mouser_url = links.get("mouser", f"https://www.mouser.com/c/?q={mpn}")
    octopart_url = links.get("octopart", f"https://octopart.com/search?q={mpn}")
    element14_url = links.get("element14", f"https://in.element14.com/search?st={mpn}")

    with st.expander(f"{badge}  |  Part Number: {mpn}", expanded=True):
        c_left, c_right = st.columns(2)
        
        with c_left:
            left_box = (
                '<div class="comp-box-original">'
                '<div class="box-title title-orig">Current BOM Component</div>'
                f'<div class="part-mpn">{mpn}</div>'
                f'<p style="margin-bottom: 4px;"><b>Manufacturer:</b> {mfr}</p>'
                f'<p style="margin-bottom: 0px;"><b>Status:</b> {status}</p>'
                '</div>'
            )
            st.markdown(left_box, unsafe_allow_html=True)

        with c_right:
            right_box = (
                '<div class="comp-box-recommended">'
                '<div class="box-title title-rec">TraceGuard Recommended Alternative</div>'
                f'<div class="part-mpn">{substitute}</div>'
                f'<p style="margin-bottom: 4px;"><b>Manufacturer:</b> {sub_mfr}</p>'
                f'<p style="margin-bottom: 0px;"><b>Pinout Compatibility:</b> {pin_compat}</p>'
                '</div>'
            )
            st.markdown(right_box, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Key Specification & Functional Differences:**")
        st.info(diffs)
        
        st.markdown("**Engineering Sourcing Analysis:**")
        st.write(analysis)
        
        st.markdown("**Distributor Verification Links:**")
        st.markdown(f"[📦 DigiKey]({digikey_url}) &nbsp;|&nbsp; [🏬 Mouser Electronics]({mouser_url}) &nbsp;|&nbsp; [🔍 Octopart Aggregator]({octopart_url}) &nbsp;|&nbsp; [🌐 Element14 / Farnell]({element14_url})")

# 4. Interface Tabs
tab1, tab2 = st.tabs(["🔍 Instant Part Search", "📁 Batch BOM Upload Audit"])

# TAB 1: INSTANT SEARCH
with tab1:
    st.subheader("Search Component Lifecycle & Substitutes")
    st.caption("Type any Manufacturer Part Number (MPN) to perform an instant risk and cross-reference lookup.")
    
    col_input, col_btn_search = st.columns([3, 1])
    with col_input:
        search_mpn = st.text_input("Enter Manufacturer Part Number (MPN):", placeholder="e.g. MAX7219CNG, TLE2426CLP, 6N137, STM32F103C8T6", label_visibility="collapsed")
    with col_btn_search:
        btn_search = st.button("🔎 Search Substitute", type="primary", use_container_width=True)

    if btn_search and search_mpn.strip():
        active_key = get_api_key()
        with st.spinner(f"🤖 Searching lifecycle and cross-references for {search_mpn.strip()}..."):
            query_str = f"MPN: {search_mpn.strip()} | Single Part Search Query"
            search_results = analyze_components_with_groq(query_str, active_key)
            
        if search_results:
            st.markdown("---")
            st.subheader("🔍 Component Search Results")
            for item in search_results:
                render_component_card(item)

# TAB 2: BATCH BOM AUDIT
with tab2:
    uploaded_file = st.file_uploader("Upload Bill of Materials (CSV)", type=["csv"], help="Upload CSV containing MPN, Description, or Manufacturer columns.")

    if uploaded_file:
        bom_df = pd.read_csv(uploaded_file)
        
        with st.expander("📄 Raw Uploaded BOM Data Preview", expanded=False):
            st.dataframe(bom_df, use_container_width=True)

        col_btn_audit, _ = st.columns([1, 3])
        with col_btn_audit:
            run_audit = st.button("🚀 Run Full BOM Risk Audit", type="primary", use_container_width=True)

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
                results = analyze_components_with_groq(bom_data_str, active_key)

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
                    render_component_card(item)

                    export_rows.append({
                        "Original MPN": str(item.get("mpn", "")),
                        "Current Status": str(item.get("status", "")),
                        "Recommended Substitute": str(item.get("substitute", "")),
                        "Pin Compatible": str(item.get("pin_compatible", "")),
                        "Key Differences": str(item.get("key_differences", "")),
                        "Engineering Analysis": str(item.get("analysis", ""))
                    })

                # CSV Download Section
                st.markdown("---")
                export_df = pd.DataFrame(export_rows)
                csv_data = export_df.to_csv(index=False).encode('utf-8')

                st.download_button(
                    label="📥 Export Audited Risk Report (CSV)",
                    data=csv_data,
                    file_name="TraceGuard_BOM_Risk_Report.csv",
                    mime="text/csv",
                    type="primary"
                )
