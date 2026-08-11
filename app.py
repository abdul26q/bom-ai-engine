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
    st.info("🔒 Universal First-Principles Taxonomy: Active")
    st.markdown("---")
    st.caption("• **Active (🟢):** Production-ready. No substitution suggested.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs. Modern alternative provided.")
    st.caption("• **Obsolete/EOL (🔴):** Discontinued. Active drop-in provided.")

# 3. High-Precision Groq AI Core Engine
def analyze_components_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an elite Lead Semiconductor Sourcing Engineer, Component Quality Manager, and Product Change Notification (PCN) Database Auditor.
        Your objective is to audit the given electronic component query with 100% deterministic, zero-hallucination accuracy.
        You must evaluate every component by applying a FIRST-PRINCIPLES HARDWARE TAXONOMY & ARCHITECTURAL REASONING FRAMEWORK.

        {bom_data_str}

        ====================================================================================================
        UNIVERSAL 8-STAGE FIRST-PRINCIPLES SEMICONDUCTOR AUDIT PROTOCOL
        ====================================================================================================

        STAGE 1: ARCHITECTURAL & GENERATIONAL EVALUATION
        Deconstruct the component's core technology and classify its lifecycle:
        1. LEGACY BJT & DARLINGTON POWER ICS:
           - Components using legacy Darlington BJT H-bridges (e.g., L298N, L293D) suffer from severe thermal dissipation and 2V–3V collector-emitter saturation losses ($V_{{CE(sat)}}$). Mark as 'NRND' or 'Obsolete'. Recommend modern, high-efficiency MOSFET H-bridges (e.g., TB6612FNG, DRV8833, MAX14870).
        2. LEGACY USB-TO-SERIAL & PERIPHERAL BRIDGES:
           - Early-generation USB 2.0 full-speed bridge ICs (e.g., FT232RL, PL2303, CP2102 non-N) carry high counterfeit risks, legacy driver issues, and outdated packaging. Mark as 'NRND' or 'Obsolete'. Recommend modern active architectures (e.g., FT230X, CP2102N, CH340E).
        3. LEGACY BIPOLAR OP-AMPS & LINEAR REGULATORS:
           - First-generation 1960s/1970s bipolar operational amplifiers (e.g., UA741, LM741) in DIP packages suffer from high input bias currents and poor frequency response. Mark as 'NRND' or 'Obsolete'. Recommend modern precision/rail-to-rail op-amps (e.g., LM358N, TL071CP, NE5532).
           - Non-RoHS or legacy through-hole 3-terminal regulators (e.g., LM7805CT, LM317T) without modern lead-free finishes must be audited for active lead-free replacements (e.g., MC7805CTG, LM7805CT/NOPB).
        4. DISCONTINUED MEMS & MOTION SENSORS:
           - Legacy 6-axis/9-axis IMUs and accelerometers officially discontinued by manufacturers (e.g., InvenSense MPU-6050, MPU-6000, MPU-6500, MPU-9250) MUST be marked as 'Obsolete' or 'EOL'. Recommend active next-generation sensors (e.g., ICM-42688-P, BMI270, LSM6DSOX).

        STAGE 2: PACKAGE FORM-FACTOR & SUFFIX DECODING
        Decode the exact physical packaging codes from the MPN suffix:
        - Through-Hole Codes:
          * 'CT', 'T' = TO-220 (3-pin Power Package).
          * 'LP', 'LPR' = TO-92 (3-pin Plastic Package). NEVER confuse TO-92 ('LP') with SSOP or SOIC!
          * 'PU', 'P', 'N' = Plastic Dual In-Line Package (PDIP).
          * 'J', 'CJ' = Ceramic CDIP (Military / Legacy Grade).
        - Surface-Mount Codes:
          * 'D', 'DR', 'BD', 'EWE' = SOIC / Small Outline Package.
          * 'M', 'SD' = Optocoupler specific DIP / SMD packages.
          * 'QFN', 'LGA', 'TQFP' = Modern Surface-Mount packages.

        STAGE 3: ENVIRONMENTAL & ROHS COMPLIANCE SUFFIX AUDIT
        Inspect MPNs for required lead-free / RoHS compliance suffix markers:
        - Maxim / Analog Devices: Non-'+' variants (e.g., MAX7219CNG, MAX232CPE, MAX232EWE) are non-RoHS leaded parts -> Mark as 'Obsolete' or 'NRND'. Recommend the '+' suffix variant (e.g., MAX7219CNG+).
        - onsemi / Motorola: Non-'G' variants (e.g., MC14069UBD, MC14011BD) are non-RoHS leaded parts -> Mark as 'Obsolete' or 'NRND'. Recommend the 'G' suffix variant (e.g., MC14069UBDG).
        - Texas Instruments: Lacking 'NOPB' on legacy family components -> Mark as 'NRND' or 'Obsolete'.

        STAGE 4: LIFECYCLE DECISION MATRIX
        - Mark 'Obsolete' / 'EOL' if: The physical package is discontinued, PCN indicates end-of-life, or the non-RoHS variant is phased out.
        - Mark 'NRND' if: The manufacturer officially recommends a newer product family (e.g., STM32G0 replacing STM32F1, or MOSFET drivers replacing Darlington BJTs).
        - Mark 'Active' ONLY IF: The part is in active mass production, fully supported, RoHS compliant, and has no active PCN replacement notices (e.g., MC7805CTG, MAX7219CNG+, NE555P, 6N137M, XC7K325T-2FFG90C, TB6612FNG, ICM-42688-P, CP2102N).

        STAGE 5: SUBSTITUTION & FOOTPRINT COMPATIBILITY POLICY
        - IF COMPONENT IS 'Obsolete' OR 'NRND':
          1. Set "status" to "Obsolete" or "NRND".
          2. Provide an explicit, orderable, active substitute MPN in "substitute".
          3. Detail specific technical advantages, efficiency gains, or electrical differences in "key_differences".
          4. Pinout Compatibility Rules:
             * If the substitute is a direct physical drop-in, set "pin_compatible" to "Yes (Direct Drop-in)".
             * If replacing a through-hole package with a surface-mount variant (or a different package footprint), set "pin_compatible" to "No (PCB Layout Redesign Required: [New Package] replacing [Old Package])".
        - IF AND ONLY IF COMPONENT IS TRULY 'Active':
          1. Set "status" to "Active".
          2. Set "substitute" to "None required (Component is Active)".
          3. Set "substitute_mfr" to "N/A".
          4. Set "pin_compatible" to "N/A (Component is Active)".
          5. Set "key_differences" to "No replacement required. The component is active, in mass production, and fully safe for design use."
          6. Set "analysis" to "Component is Active and fully supported by manufacturer. No replacement or substitution is necessary."

        STAGE 6: MULTI-DISTRIBUTOR URL GENERATION
        Generate direct query URLs for major distributors (DigiKey, Mouser, Octopart, Element14) targeting the recommended substitute MPN (or the original MPN if Active).

        STAGE 7: RAW JSON OUTPUT MANDATE
        Respond STRICTLY in valid raw JSON array format matching the exact structure below. Do not wrap in markdown code blocks or add introductory/concluding prose.

        ========================================================================================
        EXPECTED JSON STRUCTURE EXAMPLE
        ========================================================================================
        [
          {{
            "mpn": "FT232RL-REEL",
            "manufacturer": "FTDI (Future Technology Devices International)",
            "status": "NRND",
            "substitute": "FT230XQ-R / CP2102N-A02-GQ24",
            "substitute_mfr": "FTDI / Silicon Labs",
            "pin_compatible": "No (PCB Layout Redesign Required: Modern QFN/DFN package replacing SSOP-28)",
            "key_differences": "FT232RL is Not Recommended for New Designs due to legacy architecture and market clone risks. Modern alternatives like FT230X or Silicon Labs CP2102N offer lower power consumption, smaller PCB footprint, and lower unit cost.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=CP2102N",
              "mouser": "https://www.mouser.com/c/?q=CP2102N",
              "octopart": "https://octopart.com/search?q=CP2102N",
              "element14": "https://in.element14.com/search?st=CP2102N"
            }},
            "analysis": "FT232RL-REEL is a legacy USB-to-UART interface IC classified as Not Recommended for New Designs (NRND). Manufacturers recommend transitioning to the newer FT230X series or Silicon Labs CP2102N for long-term production."
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
        search_mpn = st.text_input("Enter Manufacturer Part Number (MPN):", placeholder="e.g. FT232RL-REEL, L298N, MPU-6050, LM7805CT, UA741CN, MAX7219CNG", label_visibility="collapsed")
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
