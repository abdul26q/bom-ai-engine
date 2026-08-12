import json
import os
import re
import time
import pandas as pd
import streamlit as st
from groq import Groq

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TraceGuard AI | Enterprise Component Risk Engine",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

def get_api_key():
    """Safely fetch API Key from Streamlit Secrets or Environment Variables."""
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    
    env_key = os.getenv("GROQ_API_KEY")
    if env_key:
        return env_key
        
    st.error("🔑 Groq API Key missing! Add `GROQ_API_KEY` to `.streamlit/secrets.toml` or set it as an environment variable.")
    st.stop()

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
st.markdown('<div class="sub-header">Enterprise Component Sourcing & Lifecycle Intelligence Engine</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Sidebar Navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
    st.title("System Status")
    st.success("⚡ TraceGuard AI Core: Active")
    st.info("🔒 Structured MPN Parsing & Sourcing Rules: Active")
    st.markdown("---")
    st.caption("• **Active (🟢):** Production-ready. No substitution suggested.")
    st.caption("• **NRND (🟡):** Not Recommended for New Designs. Modern alternative provided.")
    st.caption("• **Obsolete/EOL (🔴):** Discontinued. Active drop-in provided.")

# -----------------------------------------------------------------------------
# 3. AI Engine Core Functions
# -----------------------------------------------------------------------------
def analyze_components_with_groq(bom_data_str, api_key):
    try:
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert Hardware Component Sourcing and Lifecycle Intelligence AI, Component Quality Manager, and Product Change Notification (PCN) Audit Specialist.
        Your task is to analyze Manufacturer Part Numbers (MPNs) submitted in a Bill of Materials (BOM), evaluate their current lifecycle status, find optimal alternative components when necessary, and analyze pinout and architectural compatibility.

        {bom_data_str}

        ====================================================================================================
        0. MANDATORY STRUCTURED MPN PARSING PROTOCOL
        ====================================================================================================
        Before making any lifecycle or substitution decision, mentally deconstruct each MPN in a strict sequence:
        - STEP 1 (BASE PREFIX): Extract exact base family (e.g., 'MAX232', 'FT232R', 'LM7805', 'UA741', 'TLE2426', 'MPU-6050').
        - STEP 2 (PACKAGE SUFFIX): Decode physical form factor (e.g., 'N'/'P'/'PU' = PDIP, 'D'/'DR' = SOIC, 'T'/'CT' = TO-220, 'GQFN' = QFN).
        - STEP 3 (ENVIRONMENTAL SUFFIX): Check RoHS/Lead-Free indicators (Maxim '+', onsemi 'G', TI 'NOPB').
        - STEP 4 (CHANNEL & ARCHITECTURE): Count channels (Single vs Dual vs Quad) and technology (BJT vs MOSFET, Bipolar vs CMOS).

        ====================================================================================================
        1. PERMITTED LIFECYCLE STATUSES
        ====================================================================================================
        Classify each component into strictly one of these three categories:
        - Active: Mass production; full lifecycle availability.
        - NRND (Not Recommended for New Designs): Available for legacy builds, but nearing phase-out. Recommend modern alternative.
        - Obsolete: Discontinued by manufacturer. Active drop-in or redesign alternative is mandatory.

        ====================================================================================================
        2. REPLACEMENT SOURCING & ARCHITECTURAL RULES
        ====================================================================================================
        - PRESERVE ARCHITECTURE & CHANNEL COUNT: Never replace single-channel with multi-channel without warning.
        - PRIORITIZE DIRECT DROP-IN REPLACEMENTS: Prefer lead-free package equivalents (e.g., MAX232CPE to MAX232CPE+).
        - PINOUT COMPATIBILITY CHECK: Explicitly state whether layout redesign is required.

        ====================================================================================================
        3. STRICT OUTPUT POLICY & JSON SCHEMA
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
            "key_differences": "MAX232CPE+ is the lead-free (RoHS-compliant) direct drop-in replacement.",
            "supplier_links": {{
              "digikey": "https://www.digikey.com/en/products/result?keywords=MAX232CPE%2B",
              "mouser": "https://www.mouser.com/c/?q=MAX232CPE%2B",
              "octopart": "https://octopart.com/search?q=MAX232CPE%2B",
              "element14": "https://in.element14.com/search?st=MAX232CPE%2B"
            }},
            "analysis": "MAX232CPE is obsolete due to non-RoHS leaded packaging. MAX232CPE+ is active and a direct drop-in replacement."
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

        # Clean markdown code wrappers
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            json_match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise ValueError("Failed to parse valid JSON from AI response.")

    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None

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

# -----------------------------------------------------------------------------
# 4. Interface Tabs
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["🔍 Instant Part Search", "📁 Batch BOM Upload Audit"])

# TAB 1: INSTANT SEARCH
with tab1:
    st.subheader("Search Component Lifecycle & Substitutes")
    st.caption("Type any Manufacturer Part Number (MPN) to perform an instant risk and cross-reference lookup.")

    col_input, col_btn_search = st.columns([3, 1])
    with col_input:
        search_mpn = st.text_input("Enter Manufacturer Part Number (MPN):", placeholder="e.g. MAX232CPE, FT232RL-REEL, L298N, MPU-6050, LM7805CT, UA741CN", label_visibility="collapsed")
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

# TAB 2: BATCH BOM AUDIT (HANDLES 100+ ITEMS SAFELY WITH PARSER FALLBACKS)
with tab2:
    uploaded_file = st.file_uploader("Upload Bill of Materials (CSV/XLSX)", type=["csv", "xlsx", "xls"], help="Upload CSV or Excel containing MPN, Description, or Manufacturer columns.")

    if uploaded_file:
        bom_df = None
        
        # Multi-engine fallback parser to prevent pandas ParserError
        try:
            bom_df = pd.read_csv(uploaded_file)
        except Exception:
            try:
                uploaded_file.seek(0)
                bom_df = pd.read_csv(uploaded_file, sep=None, engine="python", on_bad_lines="skip")
            except Exception:
                try:
                    uploaded_file.seek(0)
                    bom_df = pd.read_excel(uploaded_file)
                except Exception as parse_err:
                    st.error(f"❌ Unable to parse file structure: {str(parse_err)}. Ensure file is valid CSV/XLSX.")
                    st.stop()

        col_map = {str(col).strip().lower(): col for col in bom_df.columns}

        with st.expander(f"📄 Raw Uploaded BOM Data Preview ({len(bom_df)} Total Rows)", expanded=False):
            st.dataframe(bom_df, use_container_width=True)

        col_btn_audit, _ = st.columns([1, 3])
        with col_btn_audit:
            run_audit = st.button("🚀 Run Full BOM Risk Audit", type="primary", use_container_width=True)

        if run_audit:
            active_key = get_api_key()

            bom_summary = []
            for _, row in bom_df.iterrows():
                mpn = str(
                    row.get(col_map.get("mpn", "")) or
                    row.get(col_map.get("part number", "")) or
                    row.get(col_map.get("item number", "")) or
                    row.get(col_map.get("item", "")) or ""
                ).strip()

                desc = str(row.get(col_map.get("description", ""), "")).strip()
                mfr = str(row.get(col_map.get("manufacturer", ""), "")).strip()

                if mpn and mpn.lower() != "nan":
                    bom_summary.append(f"MPN: {mpn} | Manufacturer: {mfr} | Description: {desc}")

            if not bom_summary:
                st.error("❌ No valid MPNs detected! Ensure columns like 'MPN' or 'Part Number' exist in your file.")
            else:
                total_items = len(bom_summary)
                CHUNK_SIZE = 15  # Optimal batch size to stay within Groq TPM limits
                bom_chunks = [bom_summary[i:i + CHUNK_SIZE] for i in range(0, total_items, CHUNK_SIZE)]
                total_chunks = len(bom_chunks)

                st.info(f"📦 Processing **{total_items} items** across **{total_chunks} batch requests** (15 parts/batch) to maintain speed and API stability...")

                progress_bar = st.progress(0)
                status_text = st.empty()
                all_results = []

                for idx, chunk in enumerate(bom_chunks):
                    status_text.text(f"⏳ Auditing Batch {idx + 1} of {total_chunks} ({len(chunk)} parts)...")
                    
                    bom_data_str = "\n".join(chunk)
                    chunk_results = analyze_components_with_groq(bom_data_str, active_key)

                    if chunk_results and isinstance(chunk_results, list):
                        all_results.extend(chunk_results)
                    else:
                        st.warning(f"⚠️ Batch {idx + 1} returned incomplete results. Continuing processing remaining items.")

                    progress_bar.progress((idx + 1) / total_chunks)

                    # 1.0 second pause between requests prevents rate limit spikes
                    if idx < total_chunks - 1:
                        time.sleep(1.0)

                status_text.success("✅ Complete BOM Risk Audit Finished!")

                st.markdown("---")
                if all_results:
                    total_parts = len(all_results)
                    nrnd_count = sum(1 for x in all_results if "NRND" in str(x.get("status", "")).upper())
                    obsolete_count = sum(1 for x in all_results if any(term in str(x.get("status", "")).upper() for term in ["OBSOLETE", "EOL"]))
                    active_count = total_parts - (nrnd_count + obsolete_count)

                    risk_index = round(((obsolete_count * 1.0 + nrnd_count * 0.5) / max(total_parts, 1)) * 100, 1)

                    # Executive KPI Summary Dashboard
                    st.subheader("📊 Executive Risk Overview")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Total Line Items Audited", total_parts)
                    m2.metric("Active Components", active_count, delta="Mass Production Ready", delta_color="normal")
                    m3.metric("At-Risk Items", nrnd_count + obsolete_count, delta=f"{obsolete_count} EOL | {nrnd_count} NRND", delta_color="inverse")
                    m4.metric("BOM Risk Index", f"{risk_index}%", delta="Critical Action Needed" if risk_index > 15 else "Low Risk", delta_color="inverse")

                    st.markdown("---")
                    st.subheader("🔍 Component Comparison & Substitute Matrix")

                    export_rows = []
                    for item in all_results:
                        render_component_card(item)

                        export_rows.append({
                            "Original MPN": str(item.get("mpn", "")),
                            "Current Status": str(item.get("status", "")),
                            "Recommended Substitute": str(item.get("substitute", "")),
                            "Pin Compatible": str(item.get("pin_compatible", "")),
                            "Key Differences": str(item.get("key_differences", "")),
                            "Engineering Analysis": str(item.get("analysis", ""))
                        })

                    st.markdown("---")
                    export_df = pd.DataFrame(export_rows)
                    csv_data = export_df.to_csv(index=False).encode('utf-8')

                    st.download_button(
                        label=f"📥 Export Full Audited Risk Report ({len(export_df)} Items CSV)",
                        data=csv_data,
                        file_name="TraceGuard_Full_BOM_Risk_Report.csv",
                        mime="text/csv",
                        type="primary"
                    )
