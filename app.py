import json
import os
import re
from openai import OpenAI
import pandas as pd
import streamlit as st

# 1. Page Configuration & Custom Theme
st.set_page_config(
    page_title="Protect the Trace. Power the Design.",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
)


def get_api_key():
    try:
        return st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return os.environ.get("OPENROUTER_API_KEY", os.environ.get("GEMINI_API_KEY", ""))


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
    st.success("⚡ TraceGuard AI Core: Active (OpenRouter Engine)")
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


# 3. Master OpenRouter AI Core Engine
def analyze_components_with_gemini(bom_data_str, api_key):
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://traceguard.ai",
                "X-Title": "TraceGuard AI",
            },
        )

        prompt = f"""
        You are an expert Hardware Component Sourcing and Lifecycle Intelligence AI, Component Quality Manager, and Product Change Notification (PCN) Audit Specialist.
        Your task is to analyze Manufacturer Part Numbers (MPNs) submitted in a Bill of Materials (BOM), evaluate their current lifecycle status, find optimal alternative components when necessary, and analyze pinout and architectural compatibility.

        {bom_data_str}

        ====================================================================================================
        0. MANDATORY STRUCTURED MPN PARSING PROTOCOL
        ====================================================================================================
        Before making any lifecycle or substitution decision, mentally deconstruct each MPN in a strict 4-step sequence:
        - STEP 1 (BASE PREFIX): Extract exact base family (e.g., 'MAX232', 'FT232R', 'LM7805', 'UA741', 'TLE2426', 'MPU-6050', 'L298').
        - STEP 2 (PACKAGE SUFFIX): Decode physical form factor (e.g., 'N'/'P'/'PU' = PDIP, 'D'/'DR'/'EWE' = SOIC, 'LP'/'LPR' = TO-92, 'T'/'CT' = TO-220, 'REEL'/'R' = Tape & Reel format).
        - STEP 3 (ENVIRONMENTAL SUFFIX): Check for active RoHS/Lead-Free indicators (e.g., Maxim '+', onsemi 'G', TI 'NOPB'). Missing compliance indicators flag high supply chain risk.
        - STEP 4 (CHANNEL & ARCHITECTURE SPEC): Count channels (Single vs Dual vs Quad) and underlying technology (BJT Darlington vs MOSFET, Bipolar vs CMOS).

        ====================================================================================================
        1. PERMITTED LIFECYCLE STATUSES
        ====================================================================================================
        Classify each component strictly into one category:
        - Active: Mass production; full lifecycle availability. No alternative required unless requested.
        - NRND (Not Recommended for New Designs): Nearing phase-out or superseded by newer architecture. Flag a warning and recommend a modern alternative.
        - Obsolete: Discontinued by manufacturer. Mandatory active alternative required.

        ====================================================================================================
        2. REPLACEMENT SOURCING & ARCHITECTURAL RULES
        ====================================================================================================
        - PRESERVE ARCHITECTURE & CHANNEL COUNT: Never replace a single-channel part with a dual-channel part without matching specs.
        - PRIORITIZE DIRECT DROP-IN REPLACEMENTS: If a direct drop-in lead-free variant exists (e.g., MAX232CPE -> MAX232CPE+), prioritize it as direct drop-in.

        ====================================================================================================
        3. STRICT SUBSTITUTION OUTPUT POLICY
        ====================================================================================================
        - IF COMPONENT IS 'Obsolete' OR 'NRND':
          1. Set "status" to "Obsolete" or "NRND".
          2. Provide explicit, orderable active substitute MPN in "substitute".
          3. Detail technical differences in "key_differences" and "analysis".
        - IF COMPONENT IS 'Active':
          1. Set "status" to "Active".
          2. Set "substitute" to "None required (Component is Active)".
          3. Set "substitute_mfr" to "N/A".
          4. Set "pin_compatible" to "N/A (Component is Active)".
          5. Set "key_differences" to "No replacement required. The component is active, in mass production, and fully safe for design use."
          6. Set "analysis" to "Component is Active and fully supported by manufacturer. No replacement necessary."

        ====================================================================================================
        4. REQUIRED OUTPUT JSON SCHEMA
        ====================================================================================================
        Respond STRICTLY in a JSON array matching this exact structure:
        [
          {{
            "mpn": "MAX232CPE",
            "manufacturer": "Maxim Integrated / Analog Devices",
            "status": "Obsolete",
            "substitute": "MAX232CPE+",
            "substitute_mfr": "Analog Devices",
            "pin_compatible": "Yes (Direct drop-in replacement)",
            "key_differences": "MAX232CPE+ is the lead-free (RoHS-compliant) direct drop-in replacement for discontinued non-RoHS MAX232CPE in PDIP-16 package.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=MAX232CPE%2B",
              "mouser": "https://www.mouser.com/c/?q=MAX232CPE%2B",
              "octopart": "https://octopart.com/search?q=MAX232CPE%2B",
              "element14": "https://in.element14.com/search?st=MAX232CPE%2B"
            }},
            "analysis": "MAX232CPE is obsolete due to non-RoHS leaded packaging. The RoHS-compliant MAX232CPE+ is active and production-ready."
          }}
        ]
        """

        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content.strip()

        match = re.search(r"\[\s*\{.*\}\s*\]", text, re.DOTALL)
        if match:
            text = match.group(0)
        else:
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
            text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

        return json.loads(text)

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
                '<div class="comp-box-original">'
                '<div class="box-title title-orig">Current BOM Component</div>'
                f'<div class="part-mpn">{mpn}</div>'
                f'<p style="margin-bottom: 4px;"><b>Manufacturer:</b> {mfr}</p>'
                f'<p style="margin-bottom: 0px;"><b>Status:</b> {status}</p>'
                "</div>"
            )
            st.markdown(left_box, unsafe_allow_html=True)

        with c_right:
            right_box = (
                '<div class="comp-box-recommended">'
                '<div class="box-title title-rec">TraceGuard Recommended Alternative</div>'
                f'<div class="part-mpn">{substitute}</div>'
                f'<p style="margin-bottom: 4px;"><b>Manufacturer:</b> {sub_mfr}</p>'
                f'<p style="margin-bottom: 0px;"><b>Pinout Compatibility:</b>'
                f" {pin_compat}</p>"
                "</div>"
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
                "e.g. MAX232CPE, FT232RL-REEL, L298N, MPU-6050, LM7805CT, UA741CN"
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
            search_results = analyze_components_with_gemini(query_str, active_key)

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
                bom_df = pd.read_csv(uploaded_file, encoding=enc, on_bad_lines="skip")
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
                    "❌ Could not parse the CSV file. Please ensure it is a valid CSV"
                    f" format. Details: {e}"
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
                                f"MPN: {mpn} | Manufacturer: {mfr} | Description: {desc}"
                            )

                    bom_data_str = "\n".join(bom_summary)
                    results = analyze_components_with_gemini(bom_data_str, active_key)

                st.markdown("---")

                if results:
                    total_parts = len(results)
                    nrnd_count = sum(
                        1 for x in results if "NRND" in str(x.get("status", "")).upper()
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
                            "Critical Action Needed" if risk_index > 15 else "Low Risk"
                        ),
                        delta_color="inverse",
                    )

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
                            "Engineering Analysis": str(item.get("analysis", "")),
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
