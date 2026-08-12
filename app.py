The error `Expecting property name enclosed in double quotes` occurs because the LLM returned JSON with non-standard formatting (such as single quotes, trailing commas, or markdown wrapper remnants) when evaluating batch inputs.

Here is the complete, corrected code with robust JSON extraction and parsing to handle LLM output quirks without changing any of your UI, layout, or design logic:

```python
import json
import os
import re
import pandas as pd
import streamlit as st
from groq import Groq

# 1. Page Configuration & Custom Theme
st.set_page_config(
    page_title="Protect the Trace. Power the Design.",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
)


def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return BACKEND_GROQ_KEY


# Custom Styling
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# Header Section
if os.path.exists("logo.png"):
    st.image("logo.png", width=500)

st.markdown(
    '<div class="main-header">Protect the Trace. Power the Design.</div>',
    unsafe_allow_html=True,
)


# 2. Sidebar Navigation
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=500)
    st.title("System Status")
    st.success("⚡ TraceGuard AI Core: Active")
    st.info("🔒 Structured MPN Parsing & Resilient CSV Parser: Active")
    st.markdown("---")
    st.caption("• **Active (🟢):** Production-ready. No substitution suggested.")
    st.caption(
        "• **NRND (🟡):** Not Recommended for New Designs. Modern alternative"
        " provided."
    )
    st.caption(
        "• **Obsolete/EOL (🔴):** Discontinued. Active drop-in provided."
    )


# 3. Combined Master Groq AI Core Engine
def analyze_components_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert Hardware Component Sourcing and Lifecycle Intelligence AI, Component Quality Manager, and Product Change Notification (PCN) Audit Specialist.
        Your task is to analyze Manufacturer Part Numbers (MPNs) submitted in a Bill of Materials (BOM), evaluate their current lifecycle status, find optimal alternative components when necessary, and analyze pinout and architectural compatibility.

        {bom_data_str}

        ====================================================================================================
        0. MANDATORY STRUCTURED MPN PARSING PROTOCOL (PREVENT MIDWAY HALLUCINATIONS)
        ====================================================================================================
        Before making any lifecycle or substitution decision, you MUST mentally deconstruct each MPN in a strict 4-step sequence:
        - STEP 1 (BASE PREFIX): Extract the exact base family (e.g., 'MAX232', 'FT232R', 'LM7805', 'UA741', 'TLE2426', 'MPU-6050', 'L298').
        - STEP 2 (PACKAGE SUFFIX): Decode physical form factor (e.g., 'N'/'P'/'PU' = PDIP, 'D'/'DR'/'EWE' = SOIC, 'LP'/'LPR' = TO-92, 'T'/'CT' = TO-220, 'REEL'/'R' = Tape & Reel packaging format).
        - STEP 3 (ENVIRONMENTAL SUFFIX): Check for active RoHS/Lead-Free indicators (e.g., Maxim '+', onsemi 'G', TI 'NOPB'). Missing compliance indicators on legacy parts automatically flag high supply chain risk.
        - STEP 4 (CHANNEL & ARCHITECTURE SPEC): Count channels (Single vs Dual vs Quad) and underlying technology (BJT Darlington vs MOSFET, Bipolar vs CMOS). Never hallucinate package or channel conversions midway through parsing.

        ====================================================================================================
        1. PERMITTED LIFECYCLE STATUSES
        ====================================================================================================
        Classify each component into strictly one of these three categories:
        - Active: Mass production; full lifecycle availability. No alternative required unless requested.
        - NRND (Not Recommended for New Designs): Available for legacy builds/repairs, but nearing phase-out or superseded by newer architecture. Flag a warning and recommend a modern alternative.
        - Obsolete: Discontinued by the manufacturer. High supply chain risk; a drop-in or redesign alternative is mandatory.

        ====================================================================================================
        2. REPLACEMENT SOURCING & ARCHITECTURAL RULES
        ====================================================================================================
        - PRESERVE ARCHITECTURE & CHANNEL COUNT:
          * Never cross-reference a single-channel component with a multi-channel variant without matching pinouts/channel specs.
          * For example, do NOT substitute a single op-amp (e.g., LM301AH or UA741CN) with a dual op-amp (e.g., LM358N) unless explicitly warning that it is a multi-channel architecture shift requiring PCB redesign. Prefer single-channel active drop-ins (e.g., TL071CP or NE5534).
        - PRIORITIZE DIRECT DROP-IN REPLACEMENTS:
          * If a direct drop-in alternative exists with the same package footprint (e.g., upgrading a non-RoHS leaded part like MAX232CPE to its lead-free variant MAX232CPE+, or MC14069UBD to MC14069UBDG), prioritize it and set pinout compatibility to "Yes (Direct drop-in replacement)".
          * Only recommend package transitions (e.g., DIP to SOIC/QFN, or TO-92 to SOIC-8) if through-hole parts are entirely obsolete or unavailable, and explicitly flag the package change.
        - PINOUT COMPATIBILITY CHECK:
          * Explicitly state whether the alternative requires a PCB layout redesign or allows a direct drop-in replacement.

        ====================================================================================================
        3. UNIVERSAL FIRST-PRINCIPLES HARDWARE TAXONOMY
        ====================================================================================================
        STAGE 1: USB-TO-SERIAL BRIDGES & INTERFACE ICS
        - FTDI FT232R / FT232RL / FT232RL-REEL -> NRND. Recommend FT230X series or Silicon Labs CP2102N.
        - Prolific PL2303 / PL2303HX -> Obsolete/NRND. Recommend CP2102N or FT230X.

        STAGE 2: LEGACY POWER DRIVERS & REGULATORS
        - L298N / L293D / L298P (Darlington BJT drivers with 2-3V thermal losses) -> NRND/Obsolete. Recommend modern MOSFET drivers: Toshiba TB6612FNG or TI DRV8833.
        - LM7805CT / LM7805T / LM317T (Non-G / Non-NOPB legacy TO-220) -> Obsolete/NRND. Recommend onsemi MC7805CTG or TI LM7805CT/NOPB.

        STAGE 3: MEMS & MOTION TRACKING SENSORS
        - InvenSense/TDK MPU-6050, MPU-6000, MPU-6500, MPU-9250 -> Obsolete/EOL. Recommend TDK ICM-42688-P or Bosch BMI270.

        STAGE 4: OP-AMPS & ANALOG FRONT-ENDS
        - UA741 / LM741 / UA741CN / LM741J -> NRND/Obsolete. Recommend single-channel active equivalents like TL071CP or NE5534 (preserve single-channel architecture).
        - TLE2426CLP / TLE2426CLPR -> Obsolete (TO-92 through-hole package discontinued). Recommend TLE2426CD / TLE2426CDR in SOIC-8.

        STAGE 5: ROHS & ENVIRONMENTAL COMPLIANCE
        - Maxim / Analog Devices parts without '+' (MAX7219CNG, MAX232CPE) -> Obsolete/NRND. Recommend '+' version (MAX7219CNG+).
        - onsemi parts without 'G' (MC14069UBD) -> Obsolete/NRND. Recommend 'G' version (MC14069UBDG).

        ====================================================================================================
        4. STRICT SUBSTITUTION OUTPUT POLICY
        ====================================================================================================
        - IF COMPONENT IS 'Obsolete' OR 'NRND':
          1. Set "status" to "Obsolete" or "NRND".
          2. Provide explicit, orderable active substitute MPN in "substitute".
          3. Detail technical differences, pinout compatibility, or efficiency gains in "key_differences" and "analysis".
        - IF AND ONLY IF COMPONENT IS TRULY 'Active':
          1. Set "status" to "Active".
          2. Set "substitute" to "None required (Component is Active)".
          3. Set "substitute_mfr" to "N/A".
          4. Set "pin_compatible" to "N/A (Component is Active)".
          5. Set "key_differences" to "No replacement required. The component is active, in mass production, and fully safe for design use."
          6. Set "analysis" to "Component is Active and fully supported by manufacturer. No replacement or substitution is necessary."

        ====================================================================================================
        5. REQUIRED OUTPUT JSON SCHEMA
        ====================================================================================================
        Respond STRICTLY in valid raw JSON array format matching this exact schema:
        [
          {{
            "mpn": "MAX232CPE",
            "manufacturer": "Maxim Integrated / Analog Devices",
            "status": "Obsolete",
            "substitute": "MAX232CPE+",
            "substitute_mfr": "Analog Devices",
            "pin_compatible": "Yes (Direct drop-in replacement)",
            "key_differences": "MAX232CPE+ is the lead-free (RoHS-compliant) direct drop-in replacement for the discontinued non-RoHS MAX232CPE in PDIP-16 package.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=MAX232CPE%2B",
              "mouser": "https://www.mouser.com/c/?q=MAX232CPE%2B",
              "octopart": "https://octopart.com/search?q=MAX232CPE%2B",
              "element14": "https://in.element14.com/search?st=MAX232CPE%2B"
            }},
            "analysis": "MAX232CPE is obsolete due to non-RoHS leaded packaging. The RoHS-compliant MAX232CPE+ is active, production-ready, and a direct drop-in replacement."
          }}
        ]
        Do not wrap in triple backticks or write conversational text. Output pure JSON only.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )

        text = response.choices[0].message.content.strip()

        # Isolate JSON array from potential extra text or markdown wrappers
        match = re.search(r"\[\s*\{.*\}\s*\]", text, re.DOTALL)
        if match:
            text = match.group(0)
        else:
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
            text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

        # Remove invalid trailing commas before closing braces/brackets
        text = re.sub(r",\s*([\]}])", r"\1", text)

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback for single-quoted strings or escape sequence issues
            import ast

            return ast.literal_eval(text.strip())

    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None


# Helper Function to Render Result Card
def render_component_card(item):
    status = str(item.get("status", "Active"))
    mpn = str(item.get("mpn", "Unknown"))
    mfr = str(item.get("manufacturer", "N/A"))
    substitute = str(
        item.get("substitute", "None required (Component is Active)")
    )
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

    digikey_url = links.get(
        "digikey", f"https://www.digikey.com/en/products/result?keywords={mpn}"
    )
    mouser_url = links.get("mouser", f"https://www.mouser.com/c/?q={mpn}")
    octopart_url = links.get("octopart", f"https://octopart.com/search?q={mpn}")
    element14_url = links.get(
        "element14", f"https://in.element14.com/search?st={mpn}"
    )

    with st.expander(f"{badge}  |  Part Number: {mpn}", expanded=True):
        c_left, c_right = st.columns(2)

        with c_left:
            left_box = (
                '<div class="comp-box-original"><div class="box-title'
                ' title-orig">Current BOM Component</div>'
                f'<div class="part-mpn">{mpn}</div><p style="margin-bottom:'
                f' 4px;"><b>Manufacturer:</b> {mfr}</p><p style="margin-bottom:'
                f' 0px;"><b>Status:</b> {status}</p></div>'
            )
            st.markdown(left_box, unsafe_allow_html=True)

        with c_right:
            right_box = (
                '<div class="comp-box-recommended"><div class="box-title'
                ' title-rec">TraceGuard Recommended Alternative</div>'
                f'<div class="part-mpn">{substitute}</div><p'
                ' style="margin-bottom: 4px;"><b>Manufacturer:</b>'
                f' {sub_mfr}</p><p style="margin-bottom: 0px;"><b>Pinout'
                f' Compatibility:</b> {pin_compat}</p></div>'
            )
            st.markdown(right_box, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Key Specification & Functional Differences:**")
        st.info(diffs)

        st.markdown("**Engineering Sourcing Analysis:**")
        st.write(analysis)

        st.markdown("**Distributor Verification Links:**")
        st.markdown(
            f"[📦 DigiKey]({digikey_url}) &nbsp;|&nbsp; [🏬 Mouser"
            f" Electronics]({mouser_url}) &nbsp;|&nbsp; [🔍 Octopart"
            f" Aggregator]({octopart_url}) &nbsp;|&nbsp; [🌐 Element14 /"
            f" Farnell]({element14_url})"
        )


# 4. Interface Tabs
tab1, tab2 = st.tabs(["🔍 Instant Part Search", "📁 Batch BOM Upload Audit"])

# TAB 1: INSTANT SEARCH
with tab1:
    st.subheader("Search Component Lifecycle & Substitutes")
    st.caption(
        "Type any Manufacturer Part Number (MPN) to perform an instant risk and"
        " cross-reference lookup."
    )

    col_input, col_btn_search = st.columns([3, 1])
    with col_input:
        search_mpn = st.text_input(
            "Enter Manufacturer Part Number (MPN):",
            placeholder=(
                "e.g. MAX232CPE, FT232RL-REEL, L298N, MPU-6050, LM7805CT,"
                " UA741CN"
            ),
            label_visibility="collapsed",
        )
    with col_btn_search:
        btn_search = st.button(
            "🔎 Search Substitute", type="primary", use_container_width=True
        )

    if btn_search and search_mpn.strip():
        active_key = get_api_key()
        with st.spinner(
            f"🤖 Searching lifecycle and cross-references for"
            f" {search_mpn.strip()}..."
        ):
            query_str = f"MPN: {search_mpn.strip()} | Single Part Search Query"
            search_results = analyze_components_with_groq(
                query_str, active_key
            )

        if search_results:
            st.markdown("---")
            st.subheader("🔍 Component Search Results")
            for item in search_results:
                render_component_card(item)

# TAB 2: BATCH BOM UPLOAD AUDIT
with tab2:
    uploaded_file = st.file_uploader(
        "Upload Bill of Materials (CSV)",
        type=["csv"],
        help="Upload CSV containing MPN, Description, or Manufacturer columns.",
    )

    if uploaded_file:
        bom_df = None
        uploaded_file.seek(0)

        encodings_to_try = ["utf-8", "utf-8-sig", "latin1", "cp1252"]

        for enc in encodings_to_try:
            try:
                uploaded_file.seek(0)
                bom_df = pd.read_csv(
                    uploaded_file, encoding=enc, on_bad_lines="skip"
                )
                break
            except Exception:
                continue

        if bom_df is None:
            try:
                uploaded_file.seek(0)
                bom_df = pd.read_csv(
                    uploaded_file, engine="python", on_bad_lines="skip"
                )
            except Exception as e:
                st.error(
                    "❌ Could not parse the CSV file. Please ensure it is a"
                    f" valid CSV format. Details: {e}"
                )

        if bom_df is not None and not bom_df.empty:
            with st.expander("📄 Raw Uploaded BOM Data Preview", expanded=False):
                st.dataframe(bom_df, use_container_width=True)

            col_btn_audit, _ = st.columns([1, 3])
            with col_btn_audit:
                run_audit = st.button(
                    "🚀 Run Full BOM Risk Audit",
                    type="primary",
                    use_container_width=True,
                )

            if run_audit:
                active_key = get_api_key()

                with st.spinner(
                    "🤖 TraceGuard AI analyzing component lifecycles &"
                    " cross-referencing drop-in substitutes..."
                ):
                    bom_summary = []
                    for _, row in bom_df.iterrows():
                        mpn = str(
                            row.get("MPN")
                            or row.get("Part Number")
                            or row.get("Item Number")
                            or row.get("Item")
                            or ""
                        ).strip()
                        desc = str(row.get("Description", "")).strip()
                        mfr = str(row.get("Manufacturer", "")).strip()
                        if mpn:
                            bom_summary.append(
                                f"MPN: {mpn} | Manufacturer: {mfr} |"
                                f" Description: {desc}"
                            )

                    bom_data_str = "\n".join(bom_summary)
                    results = analyze_components_with_groq(
                        bom_data_str, active_key
                    )

                st.markdown("---")

                if results:
                    total_parts = len(results)
                    nrnd_count = sum(
                        1
                        for x in results
                        if "NRND" in str(x.get("status", "")).upper()
                    )
                    obsolete_count = sum(
                        1
                        for x in results
                        if any(
                            term in str(x.get("status", "")).upper()
                            for term in ["OBSOLETE", "EOL"]
                        )
                    )
                    active_count = total_parts - (nrnd_count + obsolete_count)

                    risk_index = round(
                        (
                            (obsolete_count * 1.0 + nrnd_count * 0.5)
                            / max(total_parts, 1)
                        )
                        * 100,
                        1,
                    )

                    # Executive KPI Cards
                    st.subheader("📊 Executive Risk Overview")

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Total Line Items", total_parts)
                    m2.metric(
                        "Active Components",
                        active_count,
                        delta="Mass Production Ready",
                        delta_color="normal",
                    )
                    m3.metric(
                        "At-Risk Items",
                        nrnd_count + obsolete_count,
                        delta=f"{obsolete_count} EOL | {nrnd_count} NRND",
                        delta_color="inverse",
                    )
                    m4.metric(
                        "BOM Risk Index",
                        f"{risk_index}%",
                        delta=(
                            "Critical Action Needed"
                            if risk_index > 15
                            else "Low Risk"
                        ),
                        delta_color="inverse",
                    )

                    st.markdown("---")
                    st.subheader(
                        "🔍 Component Comparison & Substitute Matrix"
                    )

                    export_rows = []

                    for item in results:
                        render_component_card(item)

                        export_rows.append({
                            "Original MPN": str(item.get("mpn", "")),
                            "Current Status": str(item.get("status", "")),
                            "Recommended Substitute": str(
                                item.get("substitute", "")
                            ),
                            "Pin Compatible": str(
                                item.get("pin_compatible", "")
                            ),
                            "Key Differences": str(
                                item.get("key_differences", "")
                            ),
                            "Engineering Analysis": str(
                                item.get("analysis", "")
                            ),
                        })

                    # CSV Download Section
                    st.markdown("---")
                    export_df = pd.DataFrame(export_rows)
                    csv_data = export_df.to_csv(index=False).encode("utf-8")

                    st.download_button(
                        label="📥 Export Audited Risk Report (CSV)",
                        data=csv_data,
                        file_name="TraceGuard_BOM_Risk_Report.csv",
                        mime="text/csv",
                        type="primary",
                    )

```
