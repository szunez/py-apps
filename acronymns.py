import re
import pandas as pd
from docx import Document
from nltk.corpus import words

# Ensure you have the NLTK words corpus
import nltk
nltk.download('words')

def scan_document_for_acronyms(doc_path, start_page=1, end_page=None):
    try:
        doc = Document(doc_path)
    except Exception as e:
        print(f"Error opening document: {e}")
        return []

    text = ""
    current_page = 1
    for para in doc.paragraphs:
        if start_page <= current_page <= (end_page or float('inf')):
            text += para.text + "\n"
        if '\f' in para.text:  # Page break character
            current_page += 1
    
    # Load the list of English words
    english_words = set(words.words())
    
    # Regex to find potential acronyms (words with more than one capital letter or single letters)
    acronym_regex = re.compile(r'\b[A-Za-z]\b|\b[A-Za-z]*[A-Z][a-z]*[A-Z][A-Za-z]*\b')
    matches = acronym_regex.findall(text)
    
    acronyms = []
    
    # First, scan for predefined acronyms (case-insensitive)
    for acronym, meaning in predefined_acronyms.items():
        if re.search(rf'\b{acronym}\b', text, re.IGNORECASE):
            acronyms.append({"Acronym": acronym, "Meaning": meaning})
    
    # Then, use the current method to find additional acronyms
    for acronym in matches:
        if acronym not in ignore_list and acronym.lower() not in english_words:
            if acronym not in predefined_acronyms:
                meaning_regex = re.compile(rf'\b([\w\s]+)\s+\({acronym.rstrip("s")}\)', re.IGNORECASE)
                meaning_match = meaning_regex.search(text)
                meaning = meaning_match.group(1) if meaning_match else ""
                acronyms.append({"Acronym": acronym.rstrip('s'), "Meaning": meaning})
    
    # Remove duplicates
    unique_acronyms = {acronym['Acronym']: acronym for acronym in acronyms}
    
    acronyms = list(unique_acronyms.values())
    acronyms.sort(key=lambda x: x['Acronym'])
    
    return acronyms

def save_acronyms_to_csv(acronyms, output_path):
    df = pd.DataFrame(acronyms)
    df.to_csv(output_path, index=False)

def find_single_letter_acronyms(text):
    single_letter_acronyms = []
    for letter in predefined_acronyms:
        if len(letter) == 1 and letter in text:
            single_letter_acronyms.append({"Acronym": letter, "Meaning": predefined_acronyms[letter]})
    return single_letter_acronyms

# List of strings to ignore
ignore_list = ["XX", "XXX", "XXXX", "HOLD", "HOLDS"]

# Predefined acronym table
predefined_acronyms = {
    "AI": "Asphaltene Inhibitor",
    "AOP": "Asphaltene Onset Pressure",
    "API": "American Petroleum Institute",
    "ASD": "Acoustic Sand Detector",
    "bbl": "Barrel",
    "BHP": "Bottom Hole Pressure",
    "BIP": "Binary Interaction Parameters",
    "BoD": "Basis of Design",
    "BOEM": "Bureau of Energy Management",
    "BPD": "Barrel per day",
    "CBcp": "Category B Common Process",
    "CCE": "Constant Compositional Expansion",
    "CGR": "Condensate-Gas Ratio",
    "CI": "Corrosion Inhibitor",
    "CIMV": "Chemical Injection Metering Valve",
    "CP": "Cathodic Protection",
    "Cpen": "Peneloux volume correction constant parameter",
    "CpenT": "Peneloux volume correction temperature dependent coefficient",
    "CRA": "Corrosion Resistant Alloy",
    "DCS": "Distributed Control System",
    "DL": "Differential Liberation",
    "DNV": "Det Norske Veritas",
    "DST": "Downhole String Test",
    "EoS": "Equation of State",
    "ESD": "Emergency Shutdown Valve",
    "ESP": "Electric Submersible Pump",
    "EtOH": "Ethanol",
    "FA": "Flow Assurance",
    "FCV": "Flow Control Valve",
    "FPSO": "Floating Production, Storage and Offloading",
    "ft": "Feet",
    "GI": "Gas Injection",
    "GLV": "Gas Lift Valve",
    "GOR": "Gas-Oil Ratio",
    "HIPPS": "High-Integrity Pressure Protection System",
    "HTGC": "High Temperature Gas Chromatograph",
    "IM": "Integrity Management",
    "in": "Inches",
    "ID": "Inner Diameter",
    "ILS": "In-Line Sled",
    "LAT": "Lowest Astronomical Tide",
    "LSSW": "Low Sulfate Seawater",
    "LDHI": "Low Dosage Hydrate Inhibitor",
    "m": "Meters",
    "MAOP": "Maximum Allowable Operating Pressure",
    "MASP": "Maximum Allowable Surge Pressure",
    "MAWP": "Maximum Allowable Working Pressure",
    "MD": "Measured Depth",
    "MEG": "Mono Ethylene Glycol",
    "MeOH": "Methanol",
    "MMscf": "Million Standard Cubic Feet",
    "MMscfd": "Million Standard Cubic Feet per Day",
    "mol%": "Molar Percent",
    "MPCP": "Major Projects Common Process",
    "MPFM": "Multiphase Flow Meter",
    "Mscf": "Thousand Standard Cubic Feet",
    "Mscfd": "Thousand Standard Cubic Feet per Day",
    "MSDS": "Material Safety Data Sheet",
    "MSL": "Mean Sea Level",
    "MSST": "Multi-Stage Separator Test",
    "Multiflash": "Thermodynamic simulation software provided by KBC",
    "MWP": "Maximum Working Pressure",
    "NTL": "Notice To Leasees",
    "OBM": "Oil-based Mud",
    "OD": "Outer Diameter",
    "OLGA": "Transient multiphase flow simulation software provided by SLB (formerly Schlumberger)",
    "OLI":"OLI Studio ScaleChem scale simulation software provided by OLI Systems",
    "P&ID": "Process and Instrumentation Diagram",
    "Pb": "Bubble Point Pressure",
    "PFD": "Process Flow Diagram",
    "PI": "Productivity Index",
    "PIP": "Pipe-in-Pipe",
    "Pipesim": "Steady-state multiphase flow simultion software provided by SLB (formerly Schlumberger)",
    "PLET": "Pipeline End Terminal",
    "PSH": "Pressure Safety High",
    "PSHH": "Pressure Safety High High",
    "PSV": "Pressure Safety Valve",
    "PVT": "Pressure, Volume, Temperature (thermodynamic relationship)",
    "RKB": "Rig Kelly Bushing",
    "ROV": "Remote Operated Vehicle",
    "RP": "Recommended Practice",
    "RT": "Rotary Table",
    "SARA": "Saturate, Aromatic, Resin and Asphaltene",
    "SCSSV": "Surface-controlled Subsurface Safety Valve",
    "SCV": "Surge Control Valve",
    "SDU": "Subsea Distribution Unit",
    "SC": "Slug Catcher",
    "SG": "Specific Gravity",
    "SI": "Scale Inhibitor",
    "SPS": "Synergy Pipeline Simulator software provided by DNV",
    "stb": "Standard barrel (Liquid)",
    "stbd": "Standard barrel per day (Liquid)",
    "STO": "Stock Tank Oil",
    "TIS": "Tie-in Skid",
    "TPA": "C80+ tetraprotic acids (aka naphthenates)",
    "TVD": "True Vertical Depth",
    "TVDss": "True Vertical Depth (sea surface used as the reference point)",
    "UTA": "Umbilical Termination Assembly",
    "WAT": "Wax Appearance Temperature",
    "WC": "Water Cut",
    "WDT": "Wax Dissolution Temperature",
    "WGM": "Wet Gas Meter",
    "WGFM": "Wet Gas Flow Meter",
    "WGR": "Water-Gas Ratio",
    "WI": "Water Injection",
    "WT": "Wall Thickness",
    "wt%": "Weight Percent"
}

if __name__ == "__main__":
    doc_path = r"C:\Users\stephanos.zunez\OneDrive - Evoleap, LLC\Desktop\000503.002 - PRIO-Wahoo Hydrate Remediation Report.docx"
    output_path = r"P:\000503 PRIO - Wahoo Flow Assurance\6 Deliverables\reports\old\acronyms.csv"
    # start_page = 1  # Change this to your desired start page
    # end_page = 80   # Change this to your desired end page
    
    acronyms = scan_document_for_acronyms(doc_path, start_page=1, end_page=None)
    if acronyms:
        save_acronyms_to_csv(acronyms, output_path)
        print(f"Acronyms saved to {output_path}")
    else:
        print("No acronyms found or error reading document.")
