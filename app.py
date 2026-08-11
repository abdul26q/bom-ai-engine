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
    st.info("🔒 8-Layer Master Nomenclature Audit: Active")
    st.markdown("---")
    st.caption("• **Active (🟢):** Production-ready. No substitution suggested.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs. Modern alternative provided.")
    st.caption("• **Obsolete/EOL (🔴):** Discontinued. Active drop-in provided.")

# 3. High-Precision Groq AI Core Engine
def analyze_components_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an elite Semiconductor Sourcing Engineer, Component Quality Assurance Lead, and Product Change Notification (PCN) Database Specialist.
        Your task is to audit the given electronic component query with 100% deterministic, zero-hallucination accuracy using an EXHAUSTIVE 8-LAYER HIERARCHICAL DECISION TREE.

        {bom_data_str}

        ========================================================================================
        EXHAUSTIVE 8-LAYER HIERARCHICAL NOMENCLATURE & LIFECYCLE DECISION TREE
        ========================================================================================

        LAYER 1: COMPONENT BASE FAMILY & ARCHITECTURE AUDIT
        1. LEGACY POWER DRIVERS & H-BRIDGES:
           - L298 / L298N / L293 / L293D / L298P: Mark as 'NRND' or 'Obsolete'. Legacy bipolar Darlington drivers suffer from extreme heat loss (2-3V drop) and outdated Multiwatt/DIP packaging. Recommending a replacement is MANDATORY: Toshiba TB6612FNG, TI DRV8833, or Maxim MAX14870.
        2. LINEAR REGULATORS & POWER MANAGEMENT:
           - LM7805CT / LM7805T / LM317T (Legacy non-RoHS/non-NOPB TO-220 through-hole variants): Mark as 'Obsolete' or 'NRND'. Recommend active lead-free replacements: onsemi MC7805CTG, TI LM7805CT/NOPB, or surface-mount TO-263 equivalents (LM7805S).
        3. MEMS & MOTION TRACKING SENSORS:
           - InvenSense/TDK MPU-6050, MPU-6000, MPU-6500, MPU-9250: Mark as 'Obsolete' / 'EOL'. InvenSense officially discontinued these. Recommend active replacements: TDK ICM-42688-P, Bosch BMI270, or ST LSM6DSOX.
           - Analog Devices ADXL335 / ADXL345 (legacy variants): Mark as 'NRND' / 'Obsolete'. Recommend ADXL355 or ADXL372.
        4. OP-AMPS & ANALOG FRONT-ENDS:
           - UA741 / LM741 / UA741CN / UA741CP / LM741J: Mark as 'NRND' or 'Obsolete'. Legacy 1960s bipolar op-amps in PDIP-8/CDIP are phased out for new designs. Recommend active PDIP-8 alternatives: LM358N, NE5532, or TL071CP.
           - TLE2426CLP / TLE2426CLPR: Mark as 'Obsolete' / 'EOL'. Texas Instruments discontinued the 3-pin TO-92 plastic package ('LP' / 'LPR' suffix). Recommend active SOIC-8 versions TLE2426CD / TLE2426CDR with explicit PCB redesign warning.
        5. MICROCONTROLLERS & DIGITAL LOGIC:
           - ATMEGA328-PU / ATMEGA328P-PU (Through-hole DIP-28): Mark as 'NRND' / 'EOL'. Recommend surface-mount TQFP-32 (ATMEGA328P-AU) or ATmega328PB.
           - STMicroelectronics STM32F103 / STM32F103C8T6 (Cortex-M3 "Blue Pill" IC): Mark as 'NRND'. Replaced by STM32G071CBT6 or STM32F4 series.

        LAYER 2: PACKAGE SUFFIX DECODING & FORM-FACTOR PARSING
        - Inspect the exact package suffix code:
          * 'CT' or 'T' = TO-220 Through-Hole 3-pin package.
          * 'LP' or 'LPR' = TO-92 Through-Hole 3-pin plastic package ('R' = Tape & Reel). Never classify LP/LPR as SSOP or SOIC!
          * 'N' or 'PU' or 'P' = DIP / PDIP Through-Hole package.
          * 'CN' or 'CP' or 'J' = Legacy PDIP-8 or Ceramic CDIP package.
          * 'D' or 'DR' or 'BD' or 'EWE' = SOIC Surface Mount package.
          * 'M' or 'SD' = Optocoupler specific DIP-8 / SMD-8 package.

        LAYER 3: ROHS & ENVIRONMENTAL COMPLIANCE SUFFIX AUDIT
        - Check for lead-free / RoHS compliance markers:
          * Maxim / Analog Devices: Lacking '+' suffix (e.g., MAX7219CNG, MAX232CPE, MAX232EWE) = Non-RoHS leaded variant -> Mark as 'Obsolete' / 'NRND' and recommend '+' version (e.g., MAX7219CNG+).
          * onsemi / Motorola: Lacking 'G' suffix (e.g., MC14069UBD, MC14011BD) = Non-RoHS leaded variant -> Mark as 'Obsolete' / 'NRND' and recommend 'G' version (e.g., MC14069UBDG).
          * Texas Instruments: Lacking 'NOPB' finish on legacy packages -> Mark as 'NRND' / 'Obsolete'.

        LAYER 4: DETERMINISTIC LIFECYCLE CLASSIFICATION MATRIX
        - A part is classified as 'Obsolete' if: The package is officially discontinued, non-RoHS compliant, or PCN states EOL.
        - A part is classified as 'NRND' if: The manufacturer officially recommends newer chip families (e.g., STM32G0 replacing STM32F1, or MOSFET drivers replacing Darlington BJTs).
        - A part is classified as 'Active' ONLY IF: It is in current mass production, fully supported, RoHS compliant, and has no active PCN replacement notices (e.g., MC7805CTG, MAX7219CNG+, NE555P, 6N137M, XC7K325T-2FFG90C, TB6612FNG, ICM-42688-P).

        LAYER 5: STRICT SUBSTITUTION POLICY
        - CONDITION A: IF STATUS IS 'Obsolete' OR 'NRND':
          1. Set "status" to "Obsolete" or "NRND".
          2. You MUST provide an explicit, orderable, active substitute MPN in "substitute".
          3. Detail exact technical differences, pinout changes, or efficiency gains in "key_differences".
          4. If replacing a through-hole component with a surface-mount variant, set "pin_compatible" to: "No (PCB Layout Redesign Required: Surface-Mount replacing Through-Hole)".
        - CONDITION B: IF AND ONLY IF STATUS IS 'Active':
          1. Set "status" to "Active".
          2. Set "substitute" to "None required (Component is Active)".
          3. Set "substitute_mfr" to "N/A".
          4. Set "pin_compatible" to "N/A (Component is Active)".
          5. Set "key_differences" to "No replacement required. The component is active, in mass production, and fully safe for design use."
          6. Set "analysis" to "Component is Active and fully supported by manufacturer. No replacement or substitution is necessary."

        LAYER 6: MULTI-DISTRIBUTOR URL GENERATION
        - Populate 'supplier_links' with valid query URLs for DigiKey, Mouser, Octopart, and Element14 targeting the recommended substitute MPN (or original MPN if Active).

        LAYER 7: JSON STRUCTURE MANDATE
        - Output strictly in raw JSON array format matching the schema below. No markdown backticks, explanations, or conversational text.

        ========================================================================================
        JSON OUTPUT SCHEMA EXAMPLE
        ========================================================================================
        [
          {{
            "mpn": "L298N",
            "manufacturer": "STMicroelectronics",
            "status": "NRND",
            "substitute": "TB6612FNG / DRV8833",
            "substitute_mfr": "Toshiba / Texas Instruments",
            "pin_compatible": "No (PCB Layout Redesign Required: Surface-Mount MOSFET Driver replacing Through-Hole Multiwatt-15)",
            "key_differences": "TB6612FNG and DRV8833 use high-efficiency MOSFET H-bridges instead of L298N's outdated Darlington BJT architecture, eliminating severe 2-3V thermal voltage losses and bulky heatsinks.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=TB6612FNG",
              "mouser": "https://www.mouser.com/c/?q=TB6612FNG",
              "octopart": "https://octopart.com/search?q=TB6612FNG",
              "element14": "https://in.element14.com/search?st=TB6612FNG"
            }},
            "analysis": "L298N in Multiwatt-15 packaging is Not Recommended for New Designs (NRND). Its legacy bipolar transistors cause extreme power waste and heat generation. Upgrading to modern MOSFET drivers like Toshiba TB6612FNG or TI DRV8833 drastically improves power efficiency and reduces board space."
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
        search_mpn = st.text_input("Enter Manufacturer Part Number (MPN):", placeholder="e.g. L298N, MPU-6050, LM7805CT, UA741CN, MAX7219CNG", label_visibility="collapsed")
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
