import streamlit as st
import pandas as pd
from groq import Groq
import json
import os

# 1. Page Configuration & Custom Theme
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

# Custom Styling
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

# Header Section
if os.path.exists("logo.png"):
    st.image("logo.png", width=160)

st.markdown('<div class="main-header">TraceGuard AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enterprise Hierarchical MPN Nomenclature Parsing & Component Lifecycle Engine</div>', unsafe_allow_html=True)

# 2. Sidebar Navigation
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    st.title("System Status")
    st.success("⚡ TraceGuard AI Core: Active")
    st.info("🔒 Strict Active Part Policy: Enabled")
    st.markdown("---")
    st.caption("• **Active (🟢):** Production-ready. No substitution suggested.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs. Modern alternative provided.")
    st.caption("• **Obsolete/EOL (🔴):** Discontinued. Active drop-in provided.")

# 3. High-Precision Groq AI Core Engine
def analyze_components_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an elite Semiconductor Sourcing Engineer and PCN (Product Change Notification) Database Audit Specialist.
        Analyze the following component query by evaluating part nomenclature hierarchy and lifecycle status:

        {bom_data_str}

        CRITICAL HIERARCHICAL NOMENCLATURE PARSING PROCESS:
        For every MPN, analyze its structure in order:
        1. Base Family Identification (e.g., UA741, MAX7219, TLE2426, STM32F103, ATMEGA328, MC14069).
        2. Package & Pin Count Suffix Parsing (e.g., 'CN' = PDIP-8 legacy op-amp, 'LP' = TO-92 3-pin, 'D' = SOIC-8, 'PU' = DIP-28, 'J' = Ceramic CDIP).
        3. RoHS / Lead-Free Suffix Verification (e.g., Maxim '+' suffix, onsemi 'G' suffix).
        4. Speed / Temperature Grade Suffix Parsing (e.g., '-166AXC' vs '-200AXC').

        CRITICAL LIFECYCLE CLASSIFICATION & SUBSTITUTION RULES:

        RULE 1: LEGACY OP-AMPS & DISCONTINUED DIP PACKAGES (NRND / OBSOLETE)
        - UA741 SERIES (e.g. UA741CN, UA741CP, LM741CN, LM741J):
          * Legacy 741 op-amps in PDIP-8 ('CN' suffix) or Ceramic DIP ('J' suffix) are NRND or OBSOLETE for new hardware designs due to outdated bipolar technology, high input bias currents, and non-rail-to-rail operation.
          * Set status to "NRND" or "Obsolete".
          * Recommend modern pin-compatible or functional alternatives such as LM358N, NE5532, or TL071CP.
        - OTHER DISCONTINUED PACKAGES & ARCHITECTURES:
          * Texas Instruments 'LP' / 'LPR' TO-92 packages (e.g., TLE2426CLP) are OBSOLETE. Suggest active SOIC-8 versions (TLE2426CD/CDR) with explicit PCB redesign warning.
          * Microchip DIP-28 packages (e.g., ATMEGA328-PU) are NRND/EOL. Suggest surface-mount TQFP-32 (ATMEGA328P-AU) or ATmega328PB.
          * STMicroelectronics STM32F103 series (e.g., STM32F103C8T6) is NRND. Suggest STM32G071CBT6 or STM32F4.
          * Non-RoHS variants lacking '+' (MAX7219CNG, MAX232CPE) or 'G' (MC14069UBD) are OBSOLETE. Suggest '+' or 'G' versions.

        RULE 2: GENUINELY ACTIVE COMPONENTS (NO SUBSTITUTION SUGGESTED)
        - IF AND ONLY IF A COMPONENT IS TRULY ACTIVE IN MODERN MASS PRODUCTION (e.g., NE555P, 6N137M, GRM188R71H104KA93D, MAX7219CNG+, MAX232CPE+, MC14069UBDG, XC7K325T-2FFG90C):
          * Set "status" to "Active".
          * Set "substitute" to "None required (Component is Active)".
          * Set "substitute_mfr" to "N/A".
          * Set "pin_compatible" to "N/A (Component is Active)".
          * Set "key_differences" to "No replacement required. The component is active, in mass production, and fully safe for design use."
          * Set "analysis" to "Component is Active and fully supported by manufacturer. No replacement or substitution is necessary."
          * DO NOT suggest any alternative MPNs for truly Active components!

        Respond STRICTLY in valid raw JSON array format as a list of objects like this:
        [
          {{
            "mpn": "UA741CN",
            "manufacturer": "Texas Instruments / STMicroelectronics",
            "status": "NRND",
            "substitute": "LM358N / TL071CP",
            "substitute_mfr": "Texas Instruments / STMicroelectronics",
            "pin_compatible": "Yes (Direct PDIP-8 Drop-in)",
            "key_differences": "LM358N / TL071CP offer significantly lower power consumption, wider supply voltage range, and superior frequency response compared to the legacy UA741CN architecture.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=LM358N",
              "mouser": "https://www.mouser.com/c/?q=LM358N",
              "octopart": "https://octopart.com/search?q=LM358N",
              "element14": "https://in.element14.com/search?st=LM358N"
            }},
            "analysis": "UA741CN is based on legacy 1960s bipolar architecture and is Not Recommended for New Designs (NRND). Transitioning to modern op-amps like the LM358N or TL071CP in PDIP-8 is strongly recommended for new production designs."
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

# Helper Function to Render Result Card
def render_component_card(item):
    status = str(item.get("status", "Active"))
    mpn = str(item.get("mpn", "Unknown"))
    mfr = str(item.get("manufacturer", "N/A"))
    substitute = str(item.get("substitute", "None required (Component is Active)"))
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
        search_mpn = st.text_input("Enter Manufacturer Part Number (MPN):", placeholder="e.g. UA741CN, MAX7219CNG, TLE2426CLP, 6N137M, STM32F103C8T6", label_visibility="collapsed")
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
