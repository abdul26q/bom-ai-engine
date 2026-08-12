import re

# Update analyze_components_with_groq function
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
            temperature=0.0
        )
        
        raw_text = response.choices[0].message.content.strip()
        
        # 1. Strip Markdown Code Fences
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.MULTILINE)
        raw_text = re.sub(r"\s*```$", "", raw_text, flags=re.MULTILINE)
        raw_text = raw_text.strip()

        # 2. Extract strictly the JSON array [] portion using Regex
        array_match = re.search(r"\[\s*\{.*\}\s*\]", raw_text, re.DOTALL)
        if array_match:
            raw_text = array_match.group(0)

        # 3. Clean up common LLM malformed JSON issues (trailing commas, unescaped newlines)
        raw_text = re.sub(r",\s*([\]}])", r"\1", raw_text)  # Remove trailing commas

        return json.loads(raw_text)
        
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None
