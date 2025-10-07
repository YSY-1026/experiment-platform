import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from typing import Dict, List, Tuple
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import seaborn as sns
from PIL import Image
import io

# Record the original Streamlit function references for fallback use
_BASE_ST_TITLE = st.title
_BASE_ST_HEADER = st.header
_BASE_ST_SUBHEADER = st.subheader
_BASE_ST_MARKDOWN = st.markdown
_BASE_ST_WRITE = st.write
_BASE_ST_TEXT = st.text
_BASE_ST_METRIC = st.metric
_BASE_ST_SELECTBOX = st.selectbox
_BASE_ST_SLIDER = st.slider
_BASE_ST_BUTTON = st.button
_BASE_ST_TABS = st.tabs
_BASE_ST_PLOTLY_CHART = st.plotly_chart
try:
    _BASE_SB_SELECTBOX = st.sidebar.selectbox
    _BASE_SB_SLIDER = st.sidebar.slider
    _BASE_SB_BUTTON = st.sidebar.button
    _BASE_SB_MARKDOWN = st.sidebar.markdown
    _BASE_SB_METRIC = st.sidebar.metric if hasattr(st.sidebar, 'metric') else None
except Exception:
    _BASE_SB_SELECTBOX = None
    _BASE_SB_SLIDER = None
    _BASE_SB_BUTTON = None
    _BASE_SB_MARKDOWN = None
    _BASE_SB_METRIC = None

# Set matplotlib font for proper display
plt.rcParams['font.sans-serif'] = ['Arial']  # For proper label display
plt.rcParams['axes.unicode_minus'] = False  # For proper minus sign display
st.set_page_config(page_title="Molecular Biology Experiment Simulation System", layout="wide")


class MolecularBiologySimulator:
    def __init__(self):
        self.experiment_data = {
            'current_step': 0,
            'materials_used': [],
            'time_elapsed': 0,
            'temperature': 25,
            'ph_level': 7.0,
            'bacterial_growth': 0,
            'dna_concentration': 0,
            'pcr_cycles': 0,
            'gel_recovery_step': 0,
            'heat_shock_step': 0,
            'prep_step': 0,
            'electro_step': 0,
            'bacterial_od': 0.0,
            'plasmid_yield': 0.0,
            'pcr_product': 0.0
        }

    def reset_experiment(self):
        self.experiment_data = {
            'current_step': 0,
            'materials_used': [],
            'time_elapsed': 0,
            'temperature': 25,
            'ph_level': 7.0,
            'bacterial_growth': 0,
            'dna_concentration': 0,
            'pcr_cycles': 0,
            'gel_recovery_step': 0,
            'heat_shock_step': 0,
            'prep_step': 0,
            'electro_step': 0,
            'bacterial_od': 0.0,
            'plasmid_yield': 0.0,
            'pcr_product': 0.0
        }


# Initialize simulator
if 'simulator' not in st.session_state:
    st.session_state.simulator = MolecularBiologySimulator()


def is_kids_mode() -> bool:
    return st.session_state.get('app_mode', "Professional") == "Kids"


def is_pro_mode() -> bool:
    return st.session_state.get('app_mode') == "Professional"


def translate_for_professional(text: str) -> str:
    if not isinstance(text, str):
        return text
    mapping = {
        # Basic terminology
        "瀹為獙": "Experiment",
        "鍒嗗瓙鐢熺墿瀛�": "Molecular Biology",
        "宸ョ▼鑿�": "Engineered Bacteria",
        "鏋勫缓": "Construction",
        "CRISPR-Cas9": "CRISPR-Cas9",
        "鍩哄洜": "Gene",
        "鏁村悎": "Integration",
        "缁撴灉": "Results",
        "鍒嗘瀽": "Analysis",
        "鑳屾櫙": "Background",
        "鎿嶄綔": "Procedure",
        "妯℃嫙": "Simulation",
        "鍩瑰吇": "Culture",
        "璐ㄧ矑": "Plasmid",
        "鎵╁": "Amplification",
        "PCR": "PCR",
        "鐞艰剛绯栧嚌鑳剁數娉�": "Agarose Gel Electrophoresis",
        "鍑濊兌鐢垫吵": "Gel Electrophoresis",
        "鑳跺洖鏀�": "Gel Extraction",
        "鐑縺杞寲": "Heat Shock Transformation",
        "鐢靛嚮": "Electroporation",
        "鎰熷彈鎬�": "Competent State",
        "闃虫€�": "Positive",
        "闃存€�": "Negative",
        "鍙傛暟": "Parameters",
        "缁嗚優": "Cells",
        "鑲跨槫": "Tumor",
        "姣掓€�": "Cytotoxicity",
        "鐢熷瓨鏈�": "Survival",
        "娴撳害": "Concentration",
        "Specific Activity ": "Specific Activity",
        "杞寲鐜�": "Conversion Rate",
        "琛ㄨ揪": "Expression",
        "浠ｈ阿": "Metabolism",
        "閫氳矾": "Pathway",
        "鐑浘": "Heatmap",
        "鍥捐氨": "Map",
        "娉抽亾": "Lane",
        "鏉″甫": "Band",
        "妯℃澘": "Template",
        "寮曠墿": "Primer",
        "閫€鐏�": "Annealing",
        "寤朵几": "Extension",
        "鍙樻€�": "Denaturation",
        "鐢靛帇": "Voltage",
        "鏃堕棿": "Time",
        "娓╁害": "Temperature",
        "pH": "pH",
        "宸ョ▼鑿屾瀯寤�": "Engineered Bacteria Construction",
        "瀹為獙鑳屾櫙浠嬬粛": "Background Introduction",
        "鍩虹瀹為獙鎿嶄綔": "Basic Laboratory Procedures",
        "鍩哄洜鏁村悎绯荤粺": "Gene Integration System",
        "瀹為獙缁撴灉缁煎悎鍒嗘瀽": "Comprehensive Results Analysis",
        "閫夋嫨瀹為獙妯″潡": "Select Module",
        # Extended terminology
        "ATRA": "ATRA",
        "宸ョ▼鑿屾瀯寤轰笌鑲濈檶娌荤枟鐮旂┒瀹為獙妯℃嫙": "ATRA Engineered Bacteria Construction and Liver Cancer Treatment Research Simulation",
        "鍒嗗瓙鐢熺墿瀛﹀疄楠屽湪绾垮姩鐢绘ā鎷熺郴缁�": "Online Molecular Biology Experiment Animation Simulation System",
        "鐢熺墿瀹為獙灏忚鍫�": "Little Biology Lab",
        "绠€鍗曞ソ鐜╃殑瀹為獙鍔ㄧ敾": "Fun and Simple Experiment Animations",
        "鑲濈粏鑳炵檶娌荤枟鎸戞垬": "Hepatocellular Carcinoma Treatment Challenges",
        "鍏ㄧ悆鍙戠梾鐜�": "Global Incidence Rate",
        "绗叚澶у父瑙佹伓鎬ц偪鐦�": "Sixth Most Common Malignant Tumor",
        "涓浗鎯呭喌": "China Statistics",
        "姣忓勾39涓囨浜＄梾渚�": "390,000 Annual Deaths",
        "娌荤枟闅剧偣": "Treatment Challenges",
        "鎮ｈ€呭彂鐜版椂宸蹭腑鏅氭湡": "Patients Diagnosed at Advanced Stage",
        "寮鸿€愯嵂鎬ч檺鍒跺寲鐤楀簲鐢�": "Strong Drug Resistance Limits Chemotherapy",
        "FOLFOX4鏂规瀹㈣缂撹В鐜囦粎9.1%": "FOLFOX4 Regimen Objective Response Rate Only 9.1%",
        "ATRA浣滅敤鏈哄埗鍔ㄧ敾": "ATRA Mechanism of Action Animation",
        "璇卞鍒嗗寲": "Induce Differentiation",
        "鏈垎鍖栬偪鐦ょ粏鑳�": "Undifferentiated Tumor Cells",
        "ATRA鍒嗗瓙": "ATRA Molecule",
        "鍒嗗寲鍚庣粏鑳�": "Differentiated Cells",
        "ATRA娌荤枟閲岀▼纰�": "ATRA Treatment Milestones",
        "鍙戠幇ATRA": "ATRA Discovery",
        "APL娌荤枟绐佺牬": "APL Treatment Breakthrough",
        "瀹炰綋鐦ょ爺绌�": "Solid Tumor Research",
        "鑲濈檶涓村簥璇曢獙": "Liver Cancer Clinical Trials",
        "宸ョ▼鑿屽紑鍙�": "Engineered Bacteria Development",
        "鎬ユ€ф棭骞肩矑缁嗚優鐧借鐥�": "Acute Promyelocytic Leukemia",
        "5骞寸敓瀛樼巼": "5-Year Survival Rate",
        "绐佺牬鎬ц繘灞�": "Breakthrough Progress",
        "鑲濈檶鑱斿悎FOLFOX4": "Liver Cancer Combined with FOLFOX4",
        "涓綅鐢熷瓨鏈�": "Median Survival",
        "鏄捐憲鏀瑰杽": "Significant Improvement",
        "宸ョ▼鑿岀敓浜ф晥鐜�": "Engineered Bacteria Production Efficiency",
        "鎻愰珮300%": "300% Increase",
        "鎶€鏈潻鏂�": "Technological Innovation",
        "閫夋嫨瀹為獙椤圭洰": "Select Experiment",
        "LB鍩瑰吇鍩哄埗澶�": "LB Medium Preparation",
        "璐ㄧ矑鎻愬彇": "Plasmid Extraction",
        "PCR鎵╁": "PCR Amplification",
        "鐞艰剛绯栧嚌鑳剁數娉�": "Agarose Gel Electrophoresis",
        "鑳跺洖鏀�": "Gel Extraction",
        "鐑縺杞寲": "Heat Shock Transformation",
        "鐢靛嚮鎰熷彈鎬佸埗澶�": "Electrocompetent Cell Preparation",
        "瀹為獙鏉愭枡": "Materials",
        "瀹為獙姝ラ": "Procedure",
        "瀹炴椂鐩戞祴": "Real-time Monitoring",
        "寮€濮嬮厤鍒�": "Start Preparation",
        "涓嬩竴姝�": "Next Step",
        "璋冭妭pH鍊�": "Adjust pH",
        "姝ｅ湪璋冭妭pH鍊�": "Adjusting pH",
        "pH鍊煎凡璋冭妭鑷�7.4": "pH Adjusted to 7.4",
        "鐏弻娓╁害": "Sterilization Temperature",
        "楂樻俯鐏弻涓�": "High Temperature Sterilization",
        "褰撳墠娓╁害": "Current Temperature",
        "瀹為獙娴佺▼": "Protocol",
        "杩涜涓嬩竴姝ユ彁鍙�": "Next Extraction Step",
        "姝ｅ湪杩涜姝ラ": "Executing Step",
        "璐ㄧ矑鎻愬彇瀹屾垚": "Plasmid Extraction Complete",
        "璐ㄧ矑璐ㄩ噺妫€娴�": "Plasmid Quality Detection",
        "璐ㄧ矑娴撳害": "Plasmid Concentration",
        "璐ㄧ矑鐢垫吵鍒嗘瀽": "Plasmid Electrophoresis Analysis",
        "DNA Marker": "DNA Marker",
        "瓒呰灪鏃�": "Supercoiled",
        "绾挎€�": "Linear",
        "寮€鐜�": "Open Circular",
        "璇峰畬鎴愯川绮掓彁鍙栨楠や互鏌ョ湅缁撴灉": "Complete Plasmid Extraction Steps to View Results",
        "PCR鍙嶅簲浣撶郴": "PCR Reaction System",
        "PCR绋嬪簭": "PCR Program",
        "棰勫彉鎬�": "Pre-denaturation",
        "鍙樻€�": "Denaturation",
        "閫€鐏�": "Annealing",
        "寤朵几": "Extension",
        "鏈€缁堝欢浼�": "Final Extension",
        "寰幆娆℃暟": "Number of Cycles",
        "瀹炴椂鎵╁鏇茬嚎": "Real-time Amplification Curve",
        "寮€濮婸CR鎵╁": "Start PCR Amplification",
        "PCR鎵╁杩涜涓�": "PCR Amplification in Progress",
        "姝ｅ湪杩涜绗�": "Executing Cycle",
        "涓惊鐜�": "Cycle",
        "鎵╁鏁堢巼": "Amplification Efficiency",
        "浜х墿娴撳害": "Product Concentration",
        "PCR鍒嗗瓙杩囩▼妯℃嫙": "PCR Molecular Process Simulation",
        "PCR鍒嗗瓙杩囩▼绀烘剰鍥�": "PCR Molecular Process Diagram",
        "鍑濊兌鍒跺": "Gel Preparation",
        "鐞艰剛绯栨祿搴�": "Agarose Concentration",
        "鐢垫吵鐢靛帇": "Electrophoresis Voltage",
        "鐢垫吵鏃堕棿": "Electrophoresis Time",
        "寮€濮嬬數娉�": "Start Electrophoresis",
        "鐢垫吵杩涜涓�": "Electrophoresis in Progress",
        "鐢垫吵瀹屾垚": "Electrophoresis Complete",
        "鐢垫吵缁撴灉鍒嗘瀽": "Electrophoresis Results Analysis",
        "鏈€缁堢數娉冲浘璋�": "Final Electrophoresis Pattern",
        "鍚勬吵閬撴潯甯﹀己搴�": "Lane Band Intensity",
        "鏍峰搧": "Sample",
        "鐩稿寮哄害": "Relative Intensity",
        "DNA鑳跺洖鏀跺疄楠�": "DNA Gel Extraction Experiment",
        "杩涜涓嬩竴姝�": "Next Step",
        "鎵ц姝ラ": "Executing Step",
        "鑳跺洖鏀跺畬鎴�": "Gel Extraction Complete",
        "鍥炴敹鏁堢巼": "Recovery Efficiency",
        "DNA娴撳害": "DNA Concentration",
        "绾害妫€娴�": "Purity Detection",
        "鍥炴敹浜х墿楠岃瘉": "Recovery Product Validation",
        "鍘熷PCR浜х墿": "Original PCR Product",
        "鑳跺洖鏀朵骇鐗�": "Gel Extraction Product",
        "鑳跺洖鏀跺墠鍚庡姣�": "Before/After Gel Extraction Comparison",
        "鍑濊兌婧惰В鐘舵€�": "Gel Dissolution Status",
        "婧惰В杩涘害": "Dissolution Progress",
        "鐑縺杞寲瀹為獙": "Heat Shock Transformation Experiment",
        "鎵ц涓嬩竴姝�": "Execute Next Step",
        "鐑縺杞寲瀹屾垚": "Heat Shock Transformation Complete",
        "杞寲瀛愭暟": "Transformant Count",
        "杞寲鏁堢巼": "Transformation Efficiency",
        "闃虫€у厠闅嗙巼": "Positive Clone Rate",
        "杞寲瀛愮敓闀挎儏鍐�": "Transformant Growth Status",
        "杞寲瀛愯繃澶滅敓闀挎洸绾�": "Transformant Overnight Growth Curve",
        "鑿岃惤鏁伴噺": "Colony Count",
        "鐢靛嚮鎰熷彈鎬佸埗澶囦笌杞寲": "Electrocompetent Cell Preparation and Transformation",
        "鎰熷彈鎬佸埗澶�": "Competent Cell Preparation",
        "鐢靛嚮杞寲": "Electroporation Transformation",
        "鐢靛嚮鎰熷彈鎬佺粏鑳炲埗澶�": "Electrocompetent Cell Preparation",
        "杩涜鍒跺姝ラ": "Execute Preparation Step",
        "缁嗚弻鐢熼暱鐩戞祴": "Bacterial Growth Monitoring",
        "缁嗚弻鐢熼暱鏇茬嚎": "Bacterial Growth Curve",
        "褰撳墠OD600": "Current OD600",
        "鐢靛嚮杞寲瀹為獙": "Electroporation Transformation Experiment",
        "鐢靛嚮鍙傛暟璁剧疆": "Electroporation Parameter Settings",
        "鐢靛帇": "Voltage",
        "鐢靛": "Capacitance",
        "鐢甸樆": "Resistance",
        "鎵ц涓嬩竴姝ヨ浆鍖�": "Execute Next Transformation Step",
        "姝ｅ湪杩涜鐢靛嚮": "Electroporation in Progress",
        "鐢靛嚮瀹屾垚": "Electroporation Complete",
        "鐢靛嚮杞寲瀹為獙瀹屾垚": "Electroporation Transformation Complete",
        "鐢靛嚮杞寲瀛愭暟": "Electroporation Transformant Count",
        "鐢靛嚮杞寲鏁堢巼": "Electroporation Transformation Efficiency",
        "杞寲鏂规硶瀵规瘮": "Transformation Method Comparison",
        "鐑縺杞寲": "Heat Shock Transformation",
        "鐢靛嚮杞寲": "Electroporation Transformation",
        "杞寲瀛愭暟": "Transformant Count",
        "杞寲鏁堢巼": "Transformation Efficiency",
        "涓嶅悓杞寲鏂规硶鏁堢巼瀵规瘮": "Different Transformation Method Efficiency Comparison",
        "宸ョ▼鑿屾瀯寤哄疄楠�": "Engineered Bacteria Construction Experiment",
        "涓嬫父璐ㄧ矑鏋勫缓": "Downstream Plasmid Construction",
        "涓婃父璐ㄧ矑鏋勫缓": "Upstream Plasmid Construction",
        "鍩哄洜鏁村悎楠岃瘉": "Gene Integration Validation",
        "21a-raldh-IIdR-blh璐ㄧ矑鏋勫缓": "21a-raldh-IIdR-blh Plasmid Construction",
        "瀹為獙鐩爣": "Objective",
        "鍚湁raldh銆両IdR銆乥lh鍩哄洜鐨勯噸缁勮川绮�": "Recombinant Plasmid Containing raldh, IIdR, blh Genes",
        "raldh": "raldh",
        "瑙嗙綉鑶滈啗鑴辨阿閰跺熀鍥�": "Retinal Aldehyde Dehydrogenase Gene",
        "IIdR": "IIdR",
        "杞綍璋冩帶鍥犲瓙": "Transcriptional Regulatory Factor",
        "blh": "blh",
        "尾-鑳¤悵鍗滅礌缇熷寲閰跺熀鍥�": "尾-Carotene Hydroxylase Gene",
        "鍩哄洜鐗囨鎵╁楠岃瘉": "Gene Fragment Amplification Validation",
        "鍩哄洜鎵╁": "Gene Amplification",
        "鍚屾簮閲嶇粍鏋勫缓": "Homologous Recombination Construction",
        "杩涜鍚屾簮閲嶇粍鏋勫缓": "Execute Homologous Recombination Construction",
        "鍚屾簮閲嶇粍杩涜涓�": "Homologous Recombination in Progress",
        "绾挎€у寲pET-21a杞戒綋": "Linearize pET-21a Vector",
        "娣峰悎涓変釜鍩哄洜鐗囨": "Mix Three Gene Fragments",
        "鍔犲叆C115閲嶇粍Enzyme": "Add C115 Recombinase",
        "50鈩冨弽搴�30鍒嗛挓": "50°C Reaction for 30 Minutes",
        "杞寲鎰熷彈鎬佺粏鑳�": "Transform Competent Cells",
        "绛涢€夐槼鎬у厠闅�": "Screen Positive Clones",
        "閲嶇粍璐ㄧ矑21a-raldh-IIdR-blh鏋勫缓鎴愬姛": "Recombinant Plasmid 21a-raldh-IIdR-blh Construction Successful",
        "閲嶇粍璐ㄧ矑鍥捐氨": "Recombinant Plasmid Map",
        "21a-raldh-IIdR-blh 閲嶇粍璐ㄧ矑鍥捐氨": "21a-raldh-IIdR-blh Recombinant Plasmid Map",
        "21a-crtEBIY璐ㄧ矑鏋勫缓": "21a-crtEBIY Plasmid Construction",
        "鍚湁crtE銆乧rtB銆乧rtI銆乧rtY鍩哄洜绨囩殑閲嶇粍璐ㄧ矑": "Recombinant Plasmid Containing crtE, crtB, crtI, crtY Gene Cluster",
        "crtE": "crtE",
        "鐗荤墰鍎垮熀鐗荤墰鍎垮熀鐒︾７閰稿悎鎴愰叾": "Geranylgeranyl Pyrophosphate Synthase",
        "crtB": "crtB",
        "鍏阿鐣寗绾㈢礌鍚堟垚Enzyme": "Phytoene Synthase",
        "crtI": "crtI",
        "鍏阿鐣寗绾㈢礌鑴辨阿Enzyme": "Phytoene Desaturase",
        "crtY": "crtY",
        "鐣寗绾㈢礌鐜寲Enzyme": "Lycopene Cyclase",
        "crtEBIY鍩哄洜绨囨墿澧�": "crtEBIY Gene Cluster Amplification",
        "鍩哄洜绨囩粨鏋�": "Gene Cluster Structure",
        "鍩哄洜浣嶇疆": "Gene Position",
        "鏋勫缓21a-crtEBIY璐ㄧ矑": "Construct 21a-crtEBIY Plasmid",
        "璐ㄧ矑鏋勫缓涓�": "Plasmid Construction in Progress",
        "PCR鎵╁crtEBIY鐗囨": "PCR Amplify crtEBIY Fragment",
        "鑳跺洖鏀剁函鍖�": "Gel Extraction and Purification",
        "绾挎€у寲pET-21a杞戒綋": "Linearize pET-21a Vector",
        "鍚屾簮閲嶇粍杩炴帴": "Homologous Recombination Ligation",
        "杞寲绛涢€�": "Transformation and Screening",
        "闃虫€у厠闅嗛獙璇�": "Positive Clone Validation",
        "21a-crtEBIY璐ㄧ矑鏋勫缓鎴愬姛": "21a-crtEBIY Plasmid Construction Successful",
        "鍩哄洜鏁村悎楠岃瘉": "Gene Integration Validation",
        "鑿岃惤PCR楠岃瘉": "Colony PCR Validation",
        "閲庣敓鍨�": "Wild Type",
        "鏁村悎鏍�": "Integration Strain",
        "闃存€у鐓�": "Negative Control",
        "鍩哄洜鏁村悎鑿岃惤PCR楠岃瘉": "Gene Integration Colony PCR Validation",
        "鍒嗗瓙閲�": "Molecular Weight",
        "鏁村悎鏁堢巼缁熻": "Integration Efficiency Statistics",
        "Experiment Batch": "Experiment Batch",
        "Positive Clones": "Positive Clone Count",
        "Total Clones": "Total Clone Count",
        "Integration Efficiency %": "Integration Efficiency %",
        "鍩哄洜鏁村悎鏁堢巼缁熻": "Gene Integration Efficiency Statistics",
        "鍏嬮殕绛涢€夌粨鏋滃垎甯�": "Clone Screening Results Distribution",
        "CRISPR-Cas9鍩哄洜鏁村悎绯荤粺": "CRISPR-Cas9 Gene Integration System",
        "sgRNA璁捐涓庨獙璇�": "sgRNA Design and Validation",
        "sgRNA搴忓垪璁捐": "sgRNA Sequence Design",
        "闈跺悜搴忓垪": "Target Sequence",
        "PAM搴忓垪": "PAM Sequence",
        "楠岃瘉sgRNA璁捐": "Validate sgRNA Design",
        "GC鍚噺": "GC Content",
        "鑴遍澏棰勬祴鍒嗘暟": "Off-target Prediction Score",
        "sgRNA璁捐浼樿壇": "sgRNA Design Excellent",
        "GC鍚噺涓嶅湪鐞嗘兂鑼冨洿": "GC Content Not in Ideal Range",
        "sgRNA闀垮害蹇呴』涓�20bp": "sgRNA Length Must Be 20bp",
        "CRISPR-Cas9宸ヤ綔鍘熺悊": "CRISPR-Cas9 Working Principle",
        "闈禗NA": "Target DNA",
        "Cas9": "Cas9",
        "sgRNA": "sgRNA",
        "鍒囧壊浣嶇偣": "Cleavage Site",
        "CRISPR-Cas9鍩哄洜缂栬緫鍘熺悊": "CRISPR-Cas9 Gene Editing Principle",
        "渚涗綋鐗囨鏋勫缓 - 铻嶅悎PCR": "Donor Fragment Construction - Fusion PCR",
        "绗竴杞甈CR": "First Round PCR",
        "鎵╁涓婃父鍚屾簮鑷�": "Amplify Upstream Homology Arm",
        "绗簩杞甈CR": "Second Round PCR",
        "鎵╁涓嬫父鍚屾簮鑷�": "Amplify Downstream Homology Arm",
        "绗笁杞甈CR": "Third Round PCR",
        "鎵╁绛涢€夋爣璁�": "Amplify Selection Marker",
        "閲嶅彔寤朵几PCR": "Overlap Extension PCR",
        "鐗囨铻嶅悎": "Fragment Fusion",
        "鑳跺洖鏀剁函鍖栦緵浣撶墖娈�": "Gel Extraction and Purification of Donor Fragment",
        "杩涜涓嬩竴姝CR": "Next PCR Step",
        "杩涜": "Executing",
        "鐢靛嚮杞寲涓庣瓫閫�": "Electroporation Transformation and Screening",
        "杩涜鐢靛嚮杞寲": "Execute Electroporation Transformation",
        "鐢靛嚮杞寲杩涜涓�": "Electroporation Transformation in Progress",
        "鍒跺鐢靛嚮鎰熷彈鎬佺粏鑳�": "Prepare Electrocompetent Cells",
        "娣峰悎渚涗綋鐗囨涓巗gRNA璐ㄧ矑": "Mix Donor Fragment with sgRNA Plasmid",
        "鍐版荡10鍒嗛挓": "Ice Bath for 10 Minutes",
        "鐢靛嚮杞寲(2.5kV, 5ms)": "Electroporation Transformation (2.5kV, 5ms)",
        "澶嶈嫃鍩瑰吇1灏忔椂": "Recovery Culture for 1 Hour",
        "娑傚竷鍙屾姉骞虫澘": "Plate on Double Antibiotic Plate",
        "37鈩冨煿鍏昏繃澶�": "37°C Overnight Culture",
        "鐢靛嚮杞寲瀹屾垚": "Electroporation Transformation Complete",
        "寮€濮嬬瓫閫夐槼鎬у厠闅�": "Start Screening Positive Clones",
        "闃虫€у厠闅嗙瓫閫夌粨鏋�": "Positive Clone Screening Results",
        "绛涢€夎疆娆�": "Screening Round",
        "Total Clones": "Total Clone Count",
        "Positive Clones": "Positive Clone Count",
        "闃虫€х巼%": "Positive Rate %",
        "闃虫€у厠闅嗙瓫閫夋晥鐜�": "Positive Clone Screening Efficiency",
        "瀹為獙缁撴灉缁煎悎鍒嗘瀽": "Comprehensive Experimental Results Analysis",
        "鍩哄洜琛ㄨ揪楠岃瘉": "Gene Expression Validation",
        "铔嬬櫧鍔熻兘鍒嗘瀽": "Protein Function Analysis",
        "浠ｈ阿浜х墿妫€娴�": "Metabolite Detection",
        "娌荤枟鏁堟灉璇勪及": "Therapeutic Effect Evaluation",
        "瀹炴椂鑽у厜瀹氶噺PCR": "Real-time Quantitative PCR",
        "宸ョ▼鑿屽熀鍥犺〃杈炬按骞�": "Engineered Bacteria Gene Expression Level",
        "鐩稿琛ㄨ揪閲�": "Relative Expression Level",
        "杞綍缁勫垎鏋�": "Transcriptome Analysis",
        "閲庣敓鍨�": "Wild Type",
        "宸ョ▼鑿�": "Engineered Bacteria",
        "浠ｈ阿閫氳矾鍩哄洜琛ㄨ揪鐑浘": "Metabolic Pathway Gene Expression Heatmap",
        "SDS-PAGE铔嬬櫧鐢垫吵": "SDS-PAGE Protein Electrophoresis",
        "铔嬬櫧鐢垫吵鍒嗘瀽": "Protein Electrophoresis Analysis",
        "閰舵椿鎬у垎鏋�": "Enzyme Activity Analysis",
        "閰舵椿鎬ф祴瀹�": "Enzyme Activity Assay",
        "Specific Activity ": "Specific Activity",
        "杞寲鐜�": "Conversion Rate",
        "鍏抽敭閰舵椿鎬т笌杞寲鐜囧叧绯�": "Key Enzyme Activity and Conversion Rate Relationship",
        "ATRA浜ч噺鍒嗘瀽": "ATRA Production Analysis",
        "HPLC妫€娴� - ATRA鏍囧噯鍝�": "HPLC Detection - ATRA Standard",
        "淇濈暀鏃堕棿": "Retention Time",
        "淇″彿寮哄害": "Signal Intensity",
        "浜ч噺缁熻": "Production Statistics",
        "鍩瑰吇鏃堕棿": "Culture Time",
        "ATRA浜ч噺": "ATRA Production",
        "缁嗚優瀵嗗害": "Cell Density",
        "ATRA鍙戦叺鐢熶骇鍔ㄥ姏瀛�": "ATRA Fermentation Production Kinetics",
        "浠ｈ阿鐗╃粍瀛﹀垎鏋�": "Metabolomics Analysis",
        "浠ｈ阿鐗╃粍瀛︽瘮杈冨垎鏋�": "Metabolomics Comparative Analysis",
        "钁¤悇绯�": "Glucose",
        "涔抽吀": "Lactate",
        "涔欓吀": "Acetate",
        "涔欓唶": "Ethanol",
        "ATP": "ATP",
        "NADH": "NADH",
        "閲庣敓鍨�": "Wild Type",
        "宸ョ▼鑿�": "Engineered Bacteria",
        "浣撳鎶楄偪鐦ゆ椿鎬�": "In Vitro Antitumor Activity",
        "鍔ㄧ墿妯″瀷鐤楁晥": "Animal Model Efficacy",
        "娌荤枟缁�": "Treatment Group",
        "鑲跨槫浣撶Н": "Tumor Volume",
        "鐢熷瓨鏈�": "Survival",
        "浣撻噸鍙樺寲": "Body Weight Change",
        "娌荤枟4鍛ㄥ悗鑲跨槫浣撶Н": "Tumor Volume After 4 Weeks of Treatment",
        "涓綅鐢熷瓨鏈熸瘮杈�": "Median Survival Comparison",
        "瀵圭収缁�": "Control Group",
        "FOLFOX4": "FOLFOX4",
        "ATRA鏍囧噯": "ATRA Standard",
        "宸ョ▼鑿孉TRA": "Engineered Bacteria ATRA",
        "閫夋嫨鐗堟湰": "Select Version",
        "涓撲笟鐗�": "Professional",
        "鍎跨鐗�": "Kids",
        "閲嶇疆鎵€鏈夊疄楠�": "Reset All Experiments",
        "鎵€鏈夊疄楠屽凡閲嶇疆": "All Experiments Reset",
        "褰撳墠瀹為獙鐘舵€�": "Current Experiment Status",
        "缁嗚弻OD600": "Bacterial OD600",
        "鍢匡紝灏忕瀛﹀锛佽繖閲屾槸鏁呬簨鏃堕棿锝炴垜浠竴璧风湅鐪嬪皬鍒嗗瓙鏄浣曞府浜轰滑瀵规姉鐢熺梾鐨勫惂锛侌煣戔€嶐煍湪": "Hey little scientist! It's story time~ Let's see how tiny molecules help people fight diseases!",
        "鍔ㄦ墜鍋氬仛鐪嬶紒杩欎簺鏄疄楠屽閲屾渶甯歌鐨勫皬姝ラ锛屽氨鍍忓仛铔嬬硶鍓嶈鍏堝噯澶囨潗鏂欎竴鏍峰摝锝烉煣侌煣�": "Let's get hands-on! These are the most common little steps in the lab, just like preparing ingredients before making a cake~",
        "鎶婂ソ鍩哄洜鎷煎湪涓€璧凤紝灏卞儚鎼Н鏈紒璁╁皬缁嗚弻鎷ユ湁鏂版湰棰嗭紝鍋氬嚭鏈夌敤鐨勪笢瑗匡綖馃П馃К": "Put good genes together, just like building blocks! Let little bacteria gain new abilities and make useful things~",
        "CRISPR灏卞儚涓€鎶婅秴绮惧噯鐨勫皬鍓垁锛屽府鎴戜滑鍦―NA涓�'鍓壀璐磋创'锛佲渹锔忦煋�": "CRISPR is like super precise little scissors, helping us 'cut and paste' on DNA!",
        "鐪嬬湅鎴愭灉鍚э紒鐢ㄥ浘鐗囧拰鏁板瓧鍛婅瘔鎴戜滑锛氬疄楠屾湁娌℃湁鎴愬姛锝烉煋堭煄�": "Let's see the results! Pictures and numbers tell us: did the experiment succeed~",
    }
    out = text
    for k, v in mapping.items():
        out = out.replace(k, v)
    return out


def translate_for_kids_en(text: str) -> str:
    if not isinstance(text, str):
        return text
    mapping = {
        # Basic terminology - Cute version
        "瀹為獙": "Little Experiment",
        "鍒嗗瓙鐢熺墿瀛�": "Tiny Molecule Science",
        "宸ョ▼鑿�": "Helpful Little Bacteria",
        "鏋勫缓": "Build-Up",
        "CRISPR-Cas9": "CRISPR Magic Scissors",
        "鍩哄洜": "DNA Instructions",
        "鏁村悎": "Stick Together",
        "缁撴灉": "What We Got",
        "鍒嗘瀽": "Let's Look",
        "鑳屾櫙": "Story",
        "鎿嶄綔": "Steps",
        "妯℃嫙": "Cartoon Demo",
        "鍩瑰吇": "Grow-Grow",
        "璐ㄧ矑": "Tiny Ring DNA",
        "鎵╁": "Copy More",
        "PCR": "PCR",
        "鐞艰剛绯栧嚌鑳剁數娉�": "Jelly Run",
        "鍑濊兌鐢垫吵": "Jelly Run",
        "鑳跺洖鏀�": "Scoop from Jelly",
        "鐑縺杞寲": "Hot-Cold Magic",
        "鐢靛嚮": "Zap-Zap",
        "鎰熷彈鎬�": "DNA-Eating Mode",
        "闃虫€�": "Success",
        "闃存€�": "Not Yet",
        "鍙傛暟": "Settings",
        "缁嗚優": "Little Cells",
        "鑲跨槫": "Bad Guys",
        "姣掓€�": "Fighting Power",
        "鐢熷瓨鏈�": "How Long to Live",
        "娴撳害": "How Much",
        "Specific Activity ": "Working Power",
        "杞寲鐜�": "Change-to-Success %",
        "琛ㄨ揪": "Make How Much",
        "浠ｈ阿": "Energy Factory",
        "閫氳矾": "Little Route",
        "鐑浘": "Color Map",
        "鍥捐氨": "Circle Map",
        "娉抽亾": "Runway",
        "鏉″甫": "Little Stripes",
        "妯℃澘": "Original Sample",
        "寮曠墿": "Starter Piece",
        "閫€鐏�": "Hug-Hug",
        "寤朵几": "Grow Longer",
        "鍙樻€�": "Split Apart",
        "鐢靛帇": "Little Voltage",
        "鏃堕棿": "Time",
        "娓╁害": "Temperature",
        "pH": "Acidity",
        "宸ョ▼鑿屾瀯寤�": "Build Helpful Bacteria",
        "瀹為獙鑳屾櫙浠嬬粛": "Story Time",
        "鍩虹瀹為獙鎿嶄綔": "Easy Lab Steps",
        "鍩哄洜鏁村悎绯荤粺": "DNA Scissors Show",
        "瀹為獙缁撴灉缁煎悎鍒嗘瀽": "Look at Our Results",
        "閫夋嫨瀹為獙妯″潡": "Pick a Module",
        # Extended terminology - Cute version
        "ATRA": "ATRA",
        "宸ョ▼鑿屾瀯寤轰笌鑲濈檶娌荤枟鐮旂┒瀹為獙妯℃嫙": "ATRA Helpful Bacteria Building and Liver Bad Guy Fighting Research Cartoon",
        "鍒嗗瓙鐢熺墿瀛﹀疄楠屽湪绾垮姩鐢绘ā鎷熺郴缁�": "Online Tiny Molecule Science Cartoon Show System",
        "鐢熺墿瀹為獙灏忚鍫�": "Little Biology Lab",
        "绠€鍗曞ソ鐜╃殑瀹為獙鍔ㄧ敾": "Fun and Simple Experiment Cartoons",
        "鑲濈粏鑳炵檶娌荤枟鎸戞垬": "Liver Bad Guy Fighting Challenges",
        "鍏ㄧ悆鍙戠梾鐜�": "Worldwide Sick Rate",
        "绗叚澶у父瑙佹伓鎬ц偪鐦�": "Sixth Most Common Bad Guy",
        "涓浗鎯呭喌": "China Stats",
        "姣忓勾39涓囨浜＄梾渚�": "390,000 Deaths Each Year",
        "娌荤枟闅剧偣": "Fighting Challenges",
        "鎮ｈ€呭彂鐜版椂宸蹭腑鏅氭湡": "People Found Sick Too Late",
        "寮鸿€愯嵂鎬ч檺鍒跺寲鐤楀簲鐢�": "Strong Resistance Stops Medicine",
        "FOLFOX4鏂规瀹㈣缂撹В鐜囦粎9.1%": "FOLFOX4 Medicine Only Works 9.1%",
        "ATRA浣滅敤鏈哄埗鍔ㄧ敾": "ATRA Magic Action Cartoon",
        "璇卞鍒嗗寲": "Make Change",
        "鏈垎鍖栬偪鐦ょ粏鑳�": "Bad Guy Cells",
        "ATRA鍒嗗瓙": "ATRA Molecule",
        "鍒嗗寲鍚庣粏鑳�": "Good Guy Cells",
        "ATRA娌荤枟閲岀▼纰�": "ATRA Fighting Milestones",
        "鍙戠幇ATRA": "ATRA Discovery",
        "APL娌荤枟绐佺牬": "APL Fighting Breakthrough",
        "瀹炰綋鐦ょ爺绌�": "Solid Bad Guy Research",
        "鑲濈檶涓村簥璇曢獙": "Liver Bad Guy Tests",
        "宸ョ▼鑿屽紑鍙�": "Helpful Bacteria Development",
        "鎬ユ€ф棭骞肩矑缁嗚優鐧借鐥�": "Acute Promyelocytic Leukemia",
        "5骞寸敓瀛樼巼": "5-Year Living Rate",
        "绐佺牬鎬ц繘灞�": "Big Breakthrough",
        "鑲濈檶鑱斿悎FOLFOX4": "Liver Bad Guy + FOLFOX4",
        "涓綅鐢熷瓨鏈�": "Middle Living Time",
        "鏄捐憲鏀瑰杽": "Big Improvement",
        "宸ョ▼鑿岀敓浜ф晥鐜�": "Helpful Bacteria Making Power",
        "鎻愰珮300%": "300% More",
        "鎶€鏈潻鏂�": "Tech Revolution",
        "閫夋嫨瀹為獙椤圭洰": "Pick Experiment",
        "LB鍩瑰吇鍩哄埗澶�": "LB Food Making",
        "璐ㄧ矑鎻愬彇": "Tiny Ring DNA Taking",
        "PCR鎵╁": "PCR Copying",
        "鐞艰剛绯栧嚌鑳剁數娉�": "Jelly Run",
        "鑳跺洖鏀�": "Scoop from Jelly",
        "鐑縺杞寲": "Hot-Cold Magic",
        "鐢靛嚮鎰熷彈鎬佸埗澶�": "Zap-Zap Mode Making",
        "瀹為獙鏉愭枡": "Materials",
        "瀹為獙姝ラ": "Steps",
        "瀹炴椂鐩戞祴": "Live Watching",
        "寮€濮嬮厤鍒�": "Start Making",
        "涓嬩竴姝�": "Next Step",
        "璋冭妭pH鍊�": "Fix Acidity",
        "姝ｅ湪璋冭妭pH鍊�": "Fixing Acidity",
        "pH鍊煎凡璋冭妭鑷�7.4": "Acidity Fixed to 7.4",
        "鐏弻娓╁害": "Kill-Germ Temperature",
        "楂樻俯鐏弻涓�": "Hot Kill-Germ Time",
        "褰撳墠娓╁害": "Now Temperature",
        "瀹為獙娴佺▼": "Recipe",
        "杩涜涓嬩竴姝ユ彁鍙�": "Next Taking Step",
        "姝ｅ湪杩涜姝ラ": "Doing Step",
        "璐ㄧ矑鎻愬彇瀹屾垚": "Tiny Ring DNA Taking Done",
        "璐ㄧ矑璐ㄩ噺妫€娴�": "Tiny Ring DNA Quality Check",
        "璐ㄧ矑娴撳害": "Tiny Ring DNA Amount",
        "璐ㄧ矑鐢垫吵鍒嗘瀽": "Tiny Ring DNA Jelly Run Check",
        "DNA Marker": "DNA Marker",
        "瓒呰灪鏃�": "Super Twisty",
        "绾挎€�": "Straight Line",
        "寮€鐜�": "Open Circle",
        "璇峰畬鎴愯川绮掓彁鍙栨楠や互鏌ョ湅缁撴灉": "Finish Tiny Ring DNA Steps to See Results",
        "PCR鍙嶅簲浣撶郴": "PCR Mix",
        "PCR绋嬪簭": "PCR Recipe",
        "棰勫彉鎬�": "Pre-Split",
        "鍙樻€�": "Split Apart",
        "閫€鐏�": "Hug-Hug",
        "寤朵几": "Grow Longer",
        "鏈€缁堝欢浼�": "Final Grow",
        "寰幆娆℃暟": "Round Count",
        "瀹炴椂鎵╁鏇茬嚎": "Live Copying Line",
        "寮€濮婸CR鎵╁": "Start PCR Copying",
        "PCR鎵╁杩涜涓�": "PCR Copying Going",
        "姝ｅ湪杩涜绗�": "Doing Round",
        "涓惊鐜�": "Round",
        "鎵╁鏁堢巼": "Copying Power",
        "浜х墿娴撳害": "Product Amount",
        "PCR鍒嗗瓙杩囩▼妯℃嫙": "PCR Tiny Molecule Cartoon",
        "PCR鍒嗗瓙杩囩▼绀烘剰鍥�": "PCR Tiny Molecule Picture",
        "鍑濊兌鍒跺": "Jelly Making",
        "鐞艰剛绯栨祿搴�": "Jelly Amount",
        "鐢垫吵鐢靛帇": "Jelly Run Power",
        "鐢垫吵鏃堕棿": "Jelly Run Time",
        "寮€濮嬬數娉�": "Start Jelly Run",
        "鐢垫吵杩涜涓�": "Jelly Run Going",
        "鐢垫吵瀹屾垚": "Jelly Run Done",
        "鐢垫吵缁撴灉鍒嗘瀽": "Jelly Run Results Check",
        "鏈€缁堢數娉冲浘璋�": "Final Jelly Run Picture",
        "鍚勬吵閬撴潯甯﹀己搴�": "Each Lane Stripe Power",
        "鏍峰搧": "Sample",
        "鐩稿寮哄害": "Relative Power",
        "DNA鑳跺洖鏀跺疄楠�": "DNA Jelly Scoop Experiment",
        "杩涜涓嬩竴姝�": "Next Step",
        "鎵ц姝ラ": "Do Step",
        "鑳跺洖鏀跺畬鎴�": "Jelly Scoop Done",
        "鍥炴敹鏁堢巼": "Scoop Power",
        "DNA娴撳害": "DNA Amount",
        "绾害妫€娴�": "Clean Check",
        "鍥炴敹浜х墿楠岃瘉": "Scoop Product Check",
        "鍘熷PCR浜х墿": "Original PCR Product",
        "鑳跺洖鏀朵骇鐗�": "Jelly Scoop Product",
        "鑳跺洖鏀跺墠鍚庡姣�": "Before/After Jelly Scoop",
        "鍑濊兌婧惰В鐘舵€�": "Jelly Melt Status",
        "婧惰В杩涘害": "Melt Progress",
        "鐑縺杞寲瀹為獙": "Hot-Cold Magic Experiment",
        "鎵ц涓嬩竴姝�": "Do Next Step",
        "鐑縺杞寲瀹屾垚": "Hot-Cold Magic Done",
        "杞寲瀛愭暟": "Magic Change Count",
        "杞寲鏁堢巼": "Magic Change Power",
        "闃虫€у厠闅嗙巼": "Success Clone Rate",
        "杞寲瀛愮敓闀挎儏鍐�": "Magic Change Growth",
        "杞寲瀛愯繃澶滅敓闀挎洸绾�": "Magic Change Overnight Growth Line",
        "鑿岃惤鏁伴噺": "Colony Count",
        "鐢靛嚮鎰熷彈鎬佸埗澶囦笌杞寲": "Zap-Zap Mode Making and Changing",
        "鎰熷彈鎬佸埗澶�": "Mode Making",
        "鐢靛嚮杞寲": "Zap-Zap Change",
        "鐢靛嚮鎰熷彈鎬佺粏鑳炲埗澶�": "Zap-Zap Mode Cell Making",
        "杩涜鍒跺姝ラ": "Do Making Step",
        "缁嗚弻鐢熼暱鐩戞祴": "Bacteria Growth Watching",
        "缁嗚弻鐢熼暱鏇茬嚎": "Bacteria Growth Line",
        "褰撳墠OD600": "Now OD600",
        "鐢靛嚮杞寲瀹為獙": "Zap-Zap Change Experiment",
        "鐢靛嚮鍙傛暟璁剧疆": "Zap-Zap Settings",
        "鐢靛帇": "Voltage",
        "鐢靛": "Capacitance",
        "鐢甸樆": "Resistance",
        "鎵ц涓嬩竴姝ヨ浆鍖�": "Do Next Change Step",
        "姝ｅ湪杩涜鐢靛嚮": "Zap-Zap Going",
        "鐢靛嚮瀹屾垚": "Zap-Zap Done",
        "鐢靛嚮杞寲瀹為獙瀹屾垚": "Zap-Zap Change Experiment Done",
        "鐢靛嚮杞寲瀛愭暟": "Zap-Zap Change Count",
        "鐢靛嚮杞寲鏁堢巼": "Zap-Zap Change Power",
        "杞寲鏂规硶瀵规瘮": "Change Method Compare",
        "鐑縺杞寲": "Hot-Cold Magic",
        "鐢靛嚮杞寲": "Zap-Zap Change",
        "杞寲瀛愭暟": "Change Count",
        "杞寲鏁堢巼": "Change Power",
        "涓嶅悓杞寲鏂规硶鏁堢巼瀵规瘮": "Different Change Method Power Compare",
        "宸ョ▼鑿屾瀯寤哄疄楠�": "Helpful Bacteria Building Experiment",
        "涓嬫父璐ㄧ矑鏋勫缓": "Downstream Tiny Ring DNA Building",
        "涓婃父璐ㄧ矑鏋勫缓": "Upstream Tiny Ring DNA Building",
        "鍩哄洜鏁村悎楠岃瘉": "DNA Instructions Stick Check",
        "21a-raldh-IIdR-blh璐ㄧ矑鏋勫缓": "21a-raldh-IIdR-blh Tiny Ring DNA Building",
        "瀹為獙鐩爣": "Goal",
        "鍚湁raldh銆両IdR銆乥lh鍩哄洜鐨勯噸缁勮川绮�": "Tiny Ring DNA with raldh, IIdR, blh Instructions",
        "raldh": "raldh",
        "瑙嗙綉鑶滈啗鑴辨阿閰跺熀鍥�": "Eye Vitamin Making Instructions",
        "IIdR": "IIdR",
        "杞綍璋冩帶鍥犲瓙": "Control Instructions",
        "blh": "blh",
        "尾-鑳¤悵鍗滅礌缇熷寲閰跺熀鍥�": "Carrot Color Making Instructions",
        "鍩哄洜鐗囨鎵╁楠岃瘉": "DNA Instructions Piece Copy Check",
        "鍩哄洜鎵╁": "DNA Instructions Copy",
        "鍚屾簮閲嶇粍鏋勫缓": "Same Family Stick Building",
        "杩涜鍚屾簮閲嶇粍鏋勫缓": "Do Same Family Stick Building",
        "鍚屾簮閲嶇粍杩涜涓�": "Same Family Stick Going",
        "绾挎€у寲pET-21a杞戒綋": "Make pET-21a Straight",
        "娣峰悎涓変釜鍩哄洜鐗囨": "Mix Three DNA Instructions",
        "鍔犲叆C115閲嶇粍Enzyme": "Add C115 Stick Enzyme",
        "50鈩冨弽搴�30鍒嗛挓": "50°C Mix for 30 Minutes",
        "杞寲鎰熷彈鎬佺粏鑳�": "Change Mode Cells",
        "绛涢€夐槼鎬у厠闅�": "Pick Success Clones",
        "閲嶇粍璐ㄧ矑21a-raldh-IIdR-blh鏋勫缓鎴愬姛": "Tiny Ring DNA 21a-raldh-IIdR-blh Building Success",
        "閲嶇粍璐ㄧ矑鍥捐氨": "Tiny Ring DNA Map",
        "21a-raldh-IIdR-blh 閲嶇粍璐ㄧ矑鍥捐氨": "21a-raldh-IIdR-blh Tiny Ring DNA Map",
        "21a-crtEBIY璐ㄧ矑鏋勫缓": "21a-crtEBIY Tiny Ring DNA Building",
        "鍚湁crtE銆乧rtB銆乧rtI銆乧rtY鍩哄洜绨囩殑閲嶇粍璐ㄧ矑": "Tiny Ring DNA with crtE, crtB, crtI, crtY Instructions Group",
        "crtE": "crtE",
        "鐗荤墰鍎垮熀鐗荤墰鍎垮熀鐒︾７閰稿悎鎴愰叾": "Color Making Enzyme 1",
        "crtB": "crtB",
        "鍏阿鐣寗绾㈢礌鍚堟垚Enzyme": "Color Making Enzyme 2",
        "crtI": "crtI",
        "鍏阿鐣寗绾㈢礌鑴辨阿Enzyme": "Color Making Enzyme 3",
        "crtY": "crtY",
        "鐣寗绾㈢礌鐜寲Enzyme": "Color Making Enzyme 4",
        "crtEBIY鍩哄洜绨囨墿澧�": "crtEBIY Instructions Group Copy",
        "鍩哄洜绨囩粨鏋�": "Instructions Group Structure",
        "鍩哄洜浣嶇疆": "Instructions Position",
        "鏋勫缓21a-crtEBIY璐ㄧ矑": "Build 21a-crtEBIY Tiny Ring DNA",
        "璐ㄧ矑鏋勫缓涓�": "Tiny Ring DNA Building Going",
        "PCR鎵╁crtEBIY鐗囨": "PCR Copy crtEBIY Piece",
        "鑳跺洖鏀剁函鍖�": "Jelly Scoop Clean",
        "绾挎€у寲pET-21a杞戒綋": "Make pET-21a Straight",
        "鍚屾簮閲嶇粍杩炴帴": "Same Family Stick Connect",
        "杞寲绛涢€�": "Change and Pick",
        "闃虫€у厠闅嗛獙璇�": "Success Clone Check",
        "21a-crtEBIY璐ㄧ矑鏋勫缓鎴愬姛": "21a-crtEBIY Tiny Ring DNA Building Success",
        "鍩哄洜鏁村悎楠岃瘉": "DNA Instructions Stick Check",
        "鑿岃惤PCR楠岃瘉": "Colony PCR Check",
        "閲庣敓鍨�": "Wild Type",
        "鏁村悎鏍�": "Stick Strain",
        "闃存€у鐓�": "No Control",
        "鍩哄洜鏁村悎鑿岃惤PCR楠岃瘉": "DNA Instructions Stick Colony PCR Check",
        "鍒嗗瓙閲�": "Tiny Molecule Size",
        "鏁村悎鏁堢巼缁熻": "Stick Power Stats",
        "Experiment Batch": "Experiment Batch",
        "Positive Clones": "Success Clone Count",
        "Total Clones": "Total Clone Count",
        "Integration Efficiency %": "Stick Power %",
        "鍩哄洜鏁村悎鏁堢巼缁熻": "DNA Instructions Stick Power Stats",
        "鍏嬮殕绛涢€夌粨鏋滃垎甯�": "Clone Pick Results Spread",
        "CRISPR-Cas9鍩哄洜鏁村悎绯荤粺": "CRISPR Magic Scissors DNA Instructions Stick System",
        "sgRNA璁捐涓庨獙璇�": "sgRNA Design and Check",
        "sgRNA搴忓垪璁捐": "sgRNA Sequence Design",
        "闈跺悜搴忓垪": "Target Sequence",
        "PAM搴忓垪": "PAM Sequence",
        "楠岃瘉sgRNA璁捐": "Check sgRNA Design",
        "GC鍚噺": "GC Amount",
        "鑴遍澏棰勬祴鍒嗘暟": "Wrong Target Guess Score",
        "sgRNA璁捐浼樿壇": "sgRNA Design Great",
        "GC鍚噺涓嶅湪鐞嗘兂鑼冨洿": "GC Amount Not Perfect",
        "sgRNA闀垮害蹇呴』涓�20bp": "sgRNA Length Must Be 20bp",
        "CRISPR-Cas9宸ヤ綔鍘熺悊": "CRISPR Magic Scissors How It Works",
        "闈禗NA": "Target DNA",
        "Cas9": "Cas9",
        "sgRNA": "sgRNA",
        "鍒囧壊浣嶇偣": "Cut Spot",
        "CRISPR-Cas9鍩哄洜缂栬緫鍘熺悊": "CRISPR Magic Scissors DNA Instructions Edit How",
        "渚涗綋鐗囨鏋勫缓 - 铻嶅悎PCR": "Donor Piece Building - Mix PCR",
        "绗竴杞甈CR": "First Round PCR",
        "鎵╁涓婃父鍚屾簮鑷�": "Copy Upstream Same Arm",
        "绗簩杞甈CR": "Second Round PCR",
        "鎵╁涓嬫父鍚屾簮鑷�": "Copy Downstream Same Arm",
        "绗笁杞甈CR": "Third Round PCR",
        "鎵╁绛涢€夋爣璁�": "Copy Pick Marker",
        "閲嶅彔寤朵几PCR": "Overlap Grow PCR",
        "鐗囨铻嶅悎": "Piece Mix",
        "鑳跺洖鏀剁函鍖栦緵浣撶墖娈�": "Jelly Scoop Clean Donor Piece",
        "杩涜涓嬩竴姝CR": "Next PCR Step",
        "杩涜": "Doing",
        "鐢靛嚮杞寲涓庣瓫閫�": "Zap-Zap Change and Pick",
        "杩涜鐢靛嚮杞寲": "Do Zap-Zap Change",
        "鐢靛嚮杞寲杩涜涓�": "Zap-Zap Change Going",
        "鍒跺鐢靛嚮鎰熷彈鎬佺粏鑳�": "Make Zap-Zap Mode Cells",
        "娣峰悎渚涗綋鐗囨涓巗gRNA璐ㄧ矑": "Mix Donor Piece with sgRNA Tiny Ring DNA",
        "鍐版荡10鍒嗛挓": "Ice Bath 10 Minutes",
        "鐢靛嚮杞寲(2.5kV, 5ms)": "Zap-Zap Change (2.5kV, 5ms)",
        "澶嶈嫃鍩瑰吇1灏忔椂": "Wake Up Grow 1 Hour",
        "娑傚竷鍙屾姉骞虫澘": "Spread Double Anti Plate",
        "37鈩冨煿鍏昏繃澶�": "37°C Grow Overnight",
        "鐢靛嚮杞寲瀹屾垚": "Zap-Zap Change Done",
        "寮€濮嬬瓫閫夐槼鎬у厠闅�": "Start Pick Success Clones",
        "闃虫€у厠闅嗙瓫閫夌粨鏋�": "Success Clone Pick Results",
        "绛涢€夎疆娆�": "Pick Round",
        "Total Clones": "Total Clone Count",
        "Positive Clones": "Success Clone Count",
        "闃虫€х巼%": "Success Rate %",
        "闃虫€у厠闅嗙瓫閫夋晥鐜�": "Success Clone Pick Power",
        "瀹為獙缁撴灉缁煎悎鍒嗘瀽": "Experiment Results All Check",
        "鍩哄洜琛ㄨ揪楠岃瘉": "DNA Instructions Show Check",
        "铔嬬櫧鍔熻兘鍒嗘瀽": "Protein Work Check",
        "浠ｈ阿浜х墿妫€娴�": "Energy Factory Product Check",
        "娌荤枟鏁堟灉璇勪及": "Fighting Effect Check",
        "瀹炴椂鑽у厜瀹氶噺PCR": "Live Glow Count PCR",
        "宸ョ▼鑿屽熀鍥犺〃杈炬按骞�": "Helpful Bacteria DNA Instructions Show Level",
        "鐩稿琛ㄨ揪閲�": "Relative Show Amount",
        "杞綍缁勫垎鏋�": "Copy Group Check",
        "閲庣敓鍨�": "Wild Type",
        "宸ョ▼鑿�": "Helpful Bacteria",
        "浠ｈ阿閫氳矾鍩哄洜琛ㄨ揪鐑浘": "Energy Factory Route DNA Instructions Show Heat Map",
        "SDS-PAGE铔嬬櫧鐢垫吵": "SDS-PAGE Protein Jelly Run",
        "铔嬬櫧鐢垫吵鍒嗘瀽": "Protein Jelly Run Check",
        "閰舵椿鎬у垎鏋�": "Enzyme Work Check",
        "閰舵椿鎬ф祴瀹�": "Enzyme Work Test",
        "Specific Activity ": "Specific Work",
        "杞寲鐜�": "Change Rate",
        "鍏抽敭閰舵椿鎬т笌杞寲鐜囧叧绯�": "Key Enzyme Work and Change Rate Link",
        "ATRA浜ч噺鍒嗘瀽": "ATRA Making Amount Check",
        "HPLC妫€娴� - ATRA鏍囧噯鍝�": "HPLC Check - ATRA Standard",
        "淇濈暀鏃堕棿": "Keep Time",
        "淇″彿寮哄害": "Signal Power",
        "浜ч噺缁熻": "Making Stats",
        "鍩瑰吇鏃堕棿": "Grow Time",
        "ATRA浜ч噺": "ATRA Making",
        "缁嗚優瀵嗗害": "Cell Thickness",
        "ATRA鍙戦叺鐢熶骇鍔ㄥ姏瀛�": "ATRA Ferment Making Power",
        "浠ｈ阿鐗╃粍瀛﹀垎鏋�": "Energy Factory Product Group Check",
        "浠ｈ阿鐗╃粍瀛︽瘮杈冨垎鏋�": "Energy Factory Product Group Compare Check",
        "钁¤悇绯�": "Glucose",
        "涔抽吀": "Lactate",
        "涔欓吀": "Acetate",
        "涔欓唶": "Ethanol",
        "ATP": "ATP",
        "NADH": "NADH",
        "閲庣敓鍨�": "Wild Type",
        "宸ョ▼鑿�": "Helpful Bacteria",
        "浣撳鎶楄偪鐦ゆ椿鎬�": "Outside Fight Bad Guy Power",
        "鍔ㄧ墿妯″瀷鐤楁晥": "Animal Model Effect",
        "娌荤枟缁�": "Fight Group",
        "鑲跨槫浣撶Н": "Bad Guy Size",
        "鐢熷瓨鏈�": "Living Time",
        "浣撻噸鍙樺寲": "Body Weight Change",
        "娌荤枟4鍛ㄥ悗鑲跨槫浣撶Н": "Bad Guy Size After 4 Weeks Fighting",
        "涓綅鐢熷瓨鏈熸瘮杈�": "Middle Living Time Compare",
        "瀵圭収缁�": "Control Group",
        "FOLFOX4": "FOLFOX4",
        "ATRA鏍囧噯": "ATRA Standard",
        "宸ョ▼鑿孉TRA": "Helpful Bacteria ATRA",
        "閫夋嫨鐗堟湰": "Pick Version",
        "涓撲笟鐗�": "Professional",
        "鍎跨鐗�": "Kids",
        "閲嶇疆鎵€鏈夊疄楠�": "Reset All Experiments",
        "鎵€鏈夊疄楠屽凡閲嶇疆": "All Experiments Reset",
        "褰撳墠瀹為獙鐘舵€�": "Now Experiment Status",
        "缁嗚弻OD600": "Bacteria OD600",
        "鍢匡紝灏忕瀛﹀锛佽繖閲屾槸鏁呬簨鏃堕棿锝炴垜浠竴璧风湅鐪嬪皬鍒嗗瓙鏄浣曞府浜轰滑瀵规姉鐢熺梾鐨勫惂锛侌煣戔€嶐煍湪": "Hey little scientist! It's story time~ Let's see how tiny molecules help people fight diseases!",
        "鍔ㄦ墜鍋氬仛鐪嬶紒杩欎簺鏄疄楠屽閲屾渶甯歌鐨勫皬姝ラ锛屽氨鍍忓仛铔嬬硶鍓嶈鍏堝噯澶囨潗鏂欎竴鏍峰摝锝烉煣侌煣�": "Let's get hands-on! These are the most common little steps in the lab, just like preparing ingredients before making a cake~",
        "鎶婂ソ鍩哄洜鎷煎湪涓€璧凤紝灏卞儚鎼Н鏈紒璁╁皬缁嗚弻鎷ユ湁鏂版湰棰嗭紝鍋氬嚭鏈夌敤鐨勪笢瑗匡綖馃П馃К": "Put good genes together, just like building blocks! Let little bacteria gain new abilities and make useful things~",
        "CRISPR灏卞儚涓€鎶婅秴绮惧噯鐨勫皬鍓垁锛屽府鎴戜滑鍦―NA涓�'鍓壀璐磋创'锛佲渹锔忦煋�": "CRISPR is like super precise little scissors, helping us 'cut and paste' on DNA!",
        "鐪嬬湅鎴愭灉鍚э紒鐢ㄥ浘鐗囧拰鏁板瓧鍛婅瘔鎴戜滑锛氬疄楠屾湁娌℃湁鎴愬姛锝烉煋堭煄�": "Let's see the results! Pictures and numbers tell us: did the experiment succeed~",
    }
    out = text
    for k, v in mapping.items():
        out = out.replace(k, v)
    return out


def translate_display(text: str) -> str:
    if not isinstance(text, str):
        return text
    if is_kids_mode():
        return translate_for_kids_en(text)
    if is_pro_mode():
        return translate_for_professional(text)
    return text


def patch_streamlit_for_kids():
    patched = hasattr(st, '_kids_patched') and getattr(st, '_kids_patched', False)

    if not is_kids_mode():
        if not patched:
            return
        # Unpatch main functions
        st.title = st._orig_title
        st.header = st._orig_header
        st.subheader = st._orig_subheader
        st.markdown = st._orig_markdown
        st.write = st._orig_write
        st.text = st._orig_text
        st.metric = st._orig_metric
        st.selectbox = st._orig_selectbox
        st.slider = st._orig_slider
        st.button = st._orig_button
        st.tabs = st._orig_tabs
        st.plotly_chart = st._orig_plotly_chart
        # Unpatch sidebar functions if they were patched
        if hasattr(st, '_orig_sb_selectbox'):
            st.sidebar.selectbox = st._orig_sb_selectbox
        if hasattr(st, '_orig_sb_slider'):
            st.sidebar.slider = st._orig_sb_slider
        if hasattr(st, '_orig_sb_button'):
            st.sidebar.button = st._orig_sb_button
        if hasattr(st, '_orig_sb_markdown'):
            st.sidebar.markdown = st._orig_sb_markdown
        if hasattr(st, '_orig_sb_metric'):
            if st._orig_sb_metric is not None:
                st.sidebar.metric = st._orig_sb_metric
        st._kids_patched = False
        return

    if patched:
        return

    # Save original functions
    st._orig_title = getattr(st, '_orig_title', _BASE_ST_TITLE)
    st._orig_header = getattr(st, '_orig_header', _BASE_ST_HEADER)
    st._orig_subheader = getattr(st, '_orig_subheader', _BASE_ST_SUBHEADER)
    st._orig_markdown = getattr(st, '_orig_markdown', _BASE_ST_MARKDOWN)
    st._orig_write = getattr(st, '_orig_write', _BASE_ST_WRITE)
    st._orig_text = getattr(st, '_orig_text', _BASE_ST_TEXT)
    st._orig_metric = getattr(st, '_orig_metric', _BASE_ST_METRIC)
    st._orig_selectbox = getattr(st, '_orig_selectbox', _BASE_ST_SELECTBOX)
    st._orig_slider = getattr(st, '_orig_slider', _BASE_ST_SLIDER)
    st._orig_button = getattr(st, '_orig_button', _BASE_ST_BUTTON)
    st._orig_tabs = getattr(st, '_orig_tabs', _BASE_ST_TABS)
    st._orig_plotly_chart = getattr(st, '_orig_plotly_chart', _BASE_ST_PLOTLY_CHART)

    # Wrappers
    def w_title(label, *args, **kwargs):
        orig = getattr(st, '_orig_title', _BASE_ST_TITLE)
        if not is_kids_mode():
            return orig(translate_display(label), *args, **kwargs)
        return orig(translate_display(label), *args, **kwargs)

    def w_header(label, *args, **kwargs):
        orig = getattr(st, '_orig_header', _BASE_ST_HEADER)
        return orig(translate_display(label), *args, **kwargs)

    def w_subheader(label, *args, **kwargs):
        orig = getattr(st, '_orig_subheader', _BASE_ST_SUBHEADER)
        return orig(translate_display(label), *args, **kwargs)

    def w_markdown(body, *args, **kwargs):
        orig = getattr(st, '_orig_markdown', _BASE_ST_MARKDOWN)
        try:
            if isinstance(body, str) and "<style" in body:
                # CSS and styles are not translated, use base function directly to avoid wrapping
                return orig(body, *args, **kwargs)
        except Exception:
            pass
        return orig(translate_display(body), *args, **kwargs)

    def w_write(*args, **kwargs):
        orig = getattr(st, '_orig_write', _BASE_ST_WRITE)
        new_args = [translate_display(a) if isinstance(a, str) else a for a in args]
        return orig(*new_args, **kwargs)

    def w_text(body, *args, **kwargs):
        orig = getattr(st, '_orig_text', _BASE_ST_TEXT)
        return orig(translate_display(body), *args, **kwargs)

    def w_metric(label, value, *args, **kwargs):
        orig = getattr(st, '_orig_metric', _BASE_ST_METRIC)
        return orig(translate_display(label), value, *args, **kwargs)

    def w_selectbox(label, options, *args, **kwargs):
        orig = getattr(st, '_orig_selectbox', _BASE_ST_SELECTBOX)
        new_label = translate_display(label)
        # Only translate display, don't modify option values, ensure return value is still original string
        fmt = kwargs.get('format_func')
        if fmt is None:
            kwargs['format_func'] = lambda x: translate_display(x) if isinstance(x, str) else x
        else:
            kwargs['format_func'] = (lambda f: (lambda x: translate_display(f(x)) if isinstance(f(x), str) else f(x)))(
                fmt)
        return orig(new_label, options, *args, **kwargs)

    def w_slider(label, *args, **kwargs):
        orig = getattr(st, '_orig_slider', _BASE_ST_SLIDER)
        return orig(translate_display(label), *args, **kwargs)

    def w_button(label, *args, **kwargs):
        orig = getattr(st, '_orig_button', _BASE_ST_BUTTON)
        return orig(translate_display(label), *args, **kwargs)

    def w_tabs(tabs_list, *args, **kwargs):
        orig = getattr(st, '_orig_tabs', _BASE_ST_TABS)
        new_list = [translate_display(t) if isinstance(t, str) else t for t in tabs_list]
        return orig(new_list, *args, **kwargs)

    def w_plotly_chart(fig, *args, **kwargs):
        orig = getattr(st, '_orig_plotly_chart', _BASE_ST_PLOTLY_CHART)
        try:
            if hasattr(fig, 'layout'):
                if getattr(fig.layout, 'title', None) and getattr(fig.layout.title, 'text', None):
                    fig.layout.title.text = translate_display(fig.layout.title.text)
                if getattr(fig.layout, 'xaxis', None) and getattr(fig.layout.xaxis, 'title', None):
                    if getattr(fig.layout.xaxis.title, 'text', None):
                        fig.layout.xaxis.title.text = translate_display(fig.layout.xaxis.title.text)
                if getattr(fig.layout, 'yaxis', None) and getattr(fig.layout.yaxis, 'title', None):
                    if getattr(fig.layout.yaxis.title, 'text', None):
                        fig.layout.yaxis.title.text = translate_display(fig.layout.yaxis.title.text)
        except Exception:
            pass
        return orig(fig, *args, **kwargs)

    # Apply to st
    st.title = w_title
    st.header = w_header
    st.subheader = w_subheader
    st.markdown = w_markdown
    st.write = w_write
    st.text = w_text
    st.metric = w_metric
    st.selectbox = w_selectbox
    st.slider = w_slider
    st.button = w_button
    st.tabs = w_tabs
    st.plotly_chart = w_plotly_chart

    # Sidebar common controls (use closure to save original functions, avoid adding custom attributes to sidebar)
    try:
        st._orig_sb_selectbox = _BASE_SB_SELECTBOX or st.sidebar.selectbox
        st._orig_sb_slider = _BASE_SB_SLIDER or st.sidebar.slider
        st._orig_sb_button = _BASE_SB_BUTTON or st.sidebar.button
        st._orig_sb_markdown = _BASE_SB_MARKDOWN or st.sidebar.markdown
        st._orig_sb_metric = _BASE_SB_METRIC if _BASE_SB_METRIC else (
            st.sidebar.metric if hasattr(st.sidebar, 'metric') else None)

        def sb_selectbox(label, options, *args, **kwargs):
            new_label = translate_display(label)
            fmt = kwargs.get('format_func')
            if fmt is None:
                kwargs['format_func'] = lambda x: translate_display(x) if isinstance(x, str) else x
            else:
                kwargs['format_func'] = (
                    lambda f: (lambda x: translate_display(f(x)) if isinstance(f(x), str) else f(x)))(fmt)
            return st._orig_sb_selectbox(new_label, options, *args, **kwargs)

        def sb_slider(label, *args, **kwargs):
            return st._orig_sb_slider(translate_display(label), *args, **kwargs)

        def sb_button(label, *args, **kwargs):
            return st._orig_sb_button(translate_display(label), *args, **kwargs)

        def sb_metric(label, value, *args, **kwargs):
            if st._orig_sb_metric:
                return st._orig_sb_metric(translate_display(label), value, *args, **kwargs)
            # In rare cases where sidebar doesn't have metric, fall back to main area
            base_metric = getattr(st, '_orig_metric', _BASE_ST_METRIC)
            return base_metric(translate_display(label), value, *args, **kwargs)

        def sb_markdown(body, *args, **kwargs):
            if isinstance(body, str) and "<style" in body:
                return st._orig_sb_markdown(body, *args, **kwargs)
            return st._orig_sb_markdown(translate_display(body), *args, **kwargs)

        st.sidebar.selectbox = sb_selectbox
        st.sidebar.slider = sb_slider
        st.sidebar.button = sb_button
        if st._orig_sb_metric:
            st.sidebar.metric = sb_metric
        st.sidebar.markdown = sb_markdown
    except Exception:
        pass

    st._kids_patched = True


def create_bacterial_growth_animation():
    """Create bacterial growth animation"""
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 10, 100)

    def animate(frame):
        ax.clear()
        y = 0.001 * np.exp(0.8 * x + frame * 0.1)
        ax.plot(x, y, 'g-', linewidth=2)
        ax.set_ylim(0, 1.5)
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('OD600')
        ax.set_title('Bacterial Growth Curve (Real-time Simulation)')
        ax.grid(True, alpha=0.3)

        # Add current growth point
        current_x = min(frame * 0.1, 10)
        current_y = 0.001 * np.exp(0.8 * current_x)
        ax.plot(current_x, current_y, 'ro', markersize=8)

        return ax

    return fig, animate


def create_pcr_animation():
    """Create PCR process molecular animation"""
    fig, ax = plt.subplots(figsize=(10, 6))

    def animate(frame):
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_title('PCR Amplification Process Molecular Simulation')
        ax.axis('off')

        # Draw DNA double strand
        x_dna = np.linspace(1, 9, 100)
        y_dna1 = 4 + 0.3 * np.sin(2 * np.pi * x_dna)
        y_dna2 = 4 - 0.3 * np.sin(2 * np.pi * x_dna)
        ax.plot(x_dna, y_dna1, 'b-', linewidth=2, label='DNA Template')
        ax.plot(x_dna, y_dna2, 'b-', linewidth=2)

        # Display different stages based on frame number
        if frame < 10:
            # Denaturation stage - DNA double strand separation
            separation = frame * 0.1
            ax.plot(x_dna, y_dna1 + separation, 'r-', linewidth=2, alpha=0.7)
            ax.plot(x_dna, y_dna2 - separation, 'r-', linewidth=2, alpha=0.7)
            ax.text(5, 6, 'Denaturation: 95°C', ha='center', fontsize=12, color='red')

        elif frame < 20:
            # Annealing stage - primer binding
            ax.text(5, 6, 'Annealing: 55-65°C', ha='center', fontsize=12, color='orange')
            # Draw primers
            for i in range(3):
                x_primer = 3 + i * 2
                ax.plot([x_primer, x_primer + 0.5], [4.5, 4.5], 'g-', linewidth=3)

        else:
            # Extension stage - new strand synthesis
            ax.text(5, 6, 'Extension: 72°C', ha='center', fontsize=12, color='green')
            # Draw newly synthesized DNA strand
            x_new = np.linspace(2, 8, 50)
            y_new = 5 + 0.2 * np.sin(2 * np.pi * x_new)
            ax.plot(x_new, y_new, 'm-', linewidth=2, label='Newly Synthesized Strand')

        ax.legend()
        return ax

    return fig, animate


def create_gel_electrophoresis_animation():
    """Create gel electrophoresis animation"""
    fig, ax = plt.subplots(figsize=(8, 6))

    def animate(frame):
        ax.clear()

        # Draw gel
        gel = patches.Rectangle((1, 1), 8, 4, linewidth=2, edgecolor='black',
                                facecolor='lightblue', alpha=0.5)
        ax.add_patch(gel)

        # Draw sample wells
        wells_x = [2, 3, 4, 5, 6, 7]
        for x in wells_x:
            well = patches.Circle((x, 4.5), 0.2, facecolor='white', edgecolor='black')
            ax.add_patch(well)

        # Display DNA migration based on frame number
        migration_distance = min(frame * 0.2, 3.5)

        # Draw DNA bands
        bands_data = [
            (2, 0.8, 'Marker'), (3, 0.3, 'Sample1'), (4, 0.6, 'Sample2'),
            (5, 0.9, 'Sample3'), (6, 0.2, 'Negative'), (7, 0.7, 'Positive')
        ]

        for x, intensity, label in bands_data:
            band_height = intensity * 0.3
            band = patches.Rectangle((x - 0.15, 4.5 - migration_distance - band_height / 2),
                                     0.3, band_height, facecolor='red', alpha=intensity)
            ax.add_patch(band)
            ax.text(x, 4.5 - migration_distance - 0.4, label, ha='center', fontsize=8)

        ax.set_xlim(0, 9)
        ax.set_ylim(0, 6)
        ax.set_title('Agarose Gel Electrophoresis Simulation')
        ax.text(4.5, 0.5, f'Electrophoresis Progress: {min(frame * 10, 100):.0f}%', ha='center', fontsize=12)

        return ax

    return fig, animate


import streamlit as st


def main():
    # 版本选择
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = "Professional"

    app_mode = st.sidebar.radio("Select Version", ["Professional", "Kids"], key="app_mode")

    # 显示标题
    if app_mode == "Professional":
        st.title("🧬 Online Molecular Biology Experiment Animation Simulation System")
        st.markdown("### ATRA Engineered Bacteria Construction and Liver Cancer Treatment Research Simulation")

        # 使用 GitHub Releases 中的视频 - 正确文件名
        video_url = "https://github.com/YSY-1026/experiment-platform/releases/download/w/LBMediaPreparationAnimation.mp4"
        st.video(video_url)

        module_options = ["Background Introduction", "Basic Laboratory Procedures", "Engineered Bacteria Construction",
                          "CRISPR-Cas9 Gene Integration", "Results Analysis"]
    else:
        st.title("🔬 Little Biology Lab")
        st.markdown("### Fun and Simple Experiment Simulations")
        module_options = ["Story Time", "Lab Steps", "Bacteria Building", "DNA Scissors", "Results Show"]

    # 其他代码保持不变...

    # Sidebar navigation
    experiment_type = st.sidebar.selectbox(
        "Select Module",
        module_options
    )

    # Add experiment controls to sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Experiment Control")
    if st.sidebar.button("Reset All Experiments"):
        st.session_state.simulator.reset_experiment()
        st.success("All experiments have been reset!")

    # Display current experiment status
    st.sidebar.markdown("### Current Experiment Status")
    data = st.session_state.simulator.experiment_data
    st.sidebar.metric("Temperature", f"{data['temperature']}°C")
    st.sidebar.metric("pH Level", f"{data['ph_level']:.1f}")
    st.sidebar.metric("Bacterial OD600", f"{data['bacterial_od']:.3f}")

    if experiment_type == "Background Introduction":
        show_background()
    elif experiment_type == "Basic Laboratory Procedures":
        show_basic_experiments()
    elif experiment_type == "Engineered Bacteria Construction":
        show_engineering_bacteria()
    elif experiment_type == "CRISPR-Cas9 Gene Integration":
        show_crispr_cas9()
    else:
        show_results_analysis()

    # 娣诲姞JavaScript鏉ュ姩鎬佽缃簲鐢ㄦā寮忓睘鎬э紝鐢ㄤ簬CSS鏍峰紡鍒囨崲
    st.markdown("""
    <script>
        // 璁剧疆body鐨刣ata-app-mode灞炴€т互渚緾SS鏍峰紡鍒囨崲
        document.body.setAttribute('data-app-mode', '""" + ("Professional" if app_mode == "Professional" else "Kids") + """');
        console.log('Initial app mode set to: ' + document.body.getAttribute('data-app-mode'));

        // 鐩戝惉Streamlit閲嶆柊娓叉煋鏃舵洿鏂版ā寮忓睘鎬�
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' || mutation.type === 'attributes') {
                    // 鏌ユ壘渚ц竟鏍忎腑鐨勫崟閫夋寜閽粍
                    const sidebarRadios = document.querySelectorAll('[data-testid="stSidebar"] input[type="radio"]');
                    sidebarRadios.forEach(function(radio) {
                        if (radio.checked) {
                            const mode = radio.value === 'Professional' ? 'Professional' : 'Kids';
                            document.body.setAttribute('data-app-mode', mode);
                            console.log('App mode changed to: ' + mode);
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'style']
        });

        // 娣诲姞鐐瑰嚮鐩戝惉鍣ㄥ埌鍗曢€夋寜閽�
        setTimeout(function() {
            const radios = document.querySelectorAll('input[type="radio"]');
            radios.forEach(function(radio) {
                radio.addEventListener('change', function() {
                    const mode = this.value === 'Professional' ? 'Professional' : 'Kids';
                    document.body.setAttribute('data-app-mode', mode);
                    console.log('Radio changed, app mode set to: ' + mode);
                });
            });
        }, 1000);
    </script>
    """, unsafe_allow_html=True)


def show_background():
    st.header("🎯 Background Introduction")
    if is_kids_mode():
        st.info("Hey little scientist! It's story time~ Let's see how tiny molecules help people fight diseases!")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Hepatocellular Carcinoma Treatment Challenges")
        st.markdown("""
        - **Global Incidence**: Sixth most common malignant tumor
        - **China Statistics**: 390,000 annual deaths
        - **Treatment Challenges**: 
          - 70-80% of patients diagnosed at advanced stage
          - Strong drug resistance limits chemotherapy application
          - FOLFOX4 regimen objective response rate only 9.1%
        """)

        # Liver cancer incidence animation
        fig = go.Figure()
        cancers = ['Liver Cancer', 'Pancreatic Cancer', 'Leukemia', 'Other Solid Tumors']
        survival_rates = [16.2, 10.9, 90, 25]

        fig.add_trace(go.Bar(
            x=cancers,
            y=survival_rates,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=survival_rates,
            textposition='auto',
        ))
        fig.update_layout(
            title="Median Survival Time of ATRA in Different Cancers (months)",
            yaxis_title="Survival Time (months)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # ATRA mechanism of action dynamic diagram
        st.subheader("ATRA Mechanism of Action Animation")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("**1. Induce Differentiation**")
            st.image("https://imgur.la/image/Tumor-Cell.6giPAy",
                     caption="Undifferentiated Tumor Cells")

        with col_b:
            st.markdown("**2. ATRA Action**")
            st.image("https://imgur.la/image/ATRA.6gi4kv",
                     caption="ATRA Molecule")

        with col_c:
            st.markdown("**3. Differentiation Maturation**")
            st.image("https://imgur.la/image/TC%28differentiated%29.6giQfK",
                     caption="Differentiated Cells")

    with col2:
        st.subheader("ATRA Treatment Milestones")

        timeline_data = {
            'Year': [1980, 1990, 2000, 2010, 2020],
            'Event': ['ATRA Discovery', 'APL Treatment Breakthrough', 'Solid Tumor Research',
                      'Liver Cancer Clinical Trials', 'Engineered Bacteria Development'],
            'Importance': [1, 10, 3, 7, 8]
        }

        fig = px.scatter(timeline_data, x='Year', y='Importance', size='Importance',
                         text='Event', size_max=20)
        fig.update_traces(textposition='top center')
        fig.update_layout(title='ATRA Research Development Timeline', height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Acute Promyelocytic Leukemia", "5-Year Survival Rate >90%", "Breakthrough Progress")
        st.metric("Liver Cancer Combined with FOLFOX4", "Median Survival 16.2 months", "Significant Improvement")
        st.metric("Engineered Bacteria Production Efficiency", "300% Increase", "Technological Innovation")


def show_basic_experiments():
    st.header("🔬 Basic Laboratory Procedures Simulation")
    if is_kids_mode():
        st.info(
            "Let's get hands-on! These are the most common little steps in the lab, just like preparing ingredients before making a cake~")

    # Experiment selection
    experiment = st.selectbox(
        "Select Experiment",
        ["LB Medium Preparation", "Plasmid Extraction", "PCR Amplification", "Agarose Gel Electrophoresis",
         "Gel Extraction", "Heat Shock Transformation", "Electrocompetent Cell Preparation"]
    )

    if experiment == "LB Medium Preparation":
        simulate_lb_preparation()
    elif experiment == "Plasmid Extraction":
        simulate_plasmid_extraction()
    elif experiment == "PCR Amplification":
        simulate_pcr()
    elif experiment == "Agarose Gel Electrophoresis":
        simulate_gel_electrophoresis()
    elif experiment == "Gel Extraction":
        simulate_gel_recovery()
    elif experiment == "Heat Shock Transformation":
        simulate_heat_shock()
    else:
        simulate_electroporation()


def simulate_lb_preparation():
    st.subheader("🧪 LB Medium Preparation")

    # Display experiment materials
    materials = {
        "Tryptone": "10g",
        "Yeast Extract": "5g",
        "NaCl": "10g",
        "Agar": "3g/200ml",
        "Deionized Water": "1000ml"
    }

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write("### Materials")
        for material, amount in materials.items():
            st.checkbox(f"{material}: {amount}", value=True)

        if st.button("Start Preparation", key="start_lb"):
            st.session_state.simulator.experiment_data['current_step'] = 1
            st.rerun()

    with col2:
        st.write("### Procedure")
        steps = [
            "Accurately weigh each chemical",
            "Measure 1000ml tap water and add to beaker",
            "Add chemicals (except agar) and stir to dissolve",
            "Adjust pH to 7.2-7.6",
            "Distribute into Erlenmeyer flasks",
            "Sterilize at 121°C for 30 minutes"
        ]

        current_step = st.session_state.simulator.experiment_data['current_step']
        for i, step in enumerate(steps, 1):
            if i <= current_step:
                st.success(f"{step}")
            else:
                st.info(f"{i}. {step}")

        if current_step > 0 and current_step < len(steps):
            if st.button("Next Step", key="next_lb_step"):
                st.session_state.simulator.experiment_data['current_step'] += 1
                st.rerun()

    with col3:
        st.write("### Real-time Monitoring")

        # pH adjustment simulation
        current_ph = st.session_state.simulator.experiment_data['ph_level']

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_ph,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "pH"},
            delta={'reference': 7.4},
            gauge={
                'axis': {'range': [6.5, 8.5]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [6.5, 7.2], 'color': "lightgray"},
                    {'range': [7.2, 7.6], 'color': "lightgreen"},
                    {'range': [7.6, 8.5], 'color': "lightgray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7.4}}
        ))
        st.plotly_chart(fig, use_container_width=True)

        if st.button("Adjust pH"):
            with st.spinner("Adjusting pH..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                # Simulate pH adjustment to ideal range
                st.session_state.simulator.experiment_data['ph_level'] = 7.4
                st.session_state.simulator.experiment_data['current_step'] += 1
                st.success("pH adjusted to 7.4!")
                st.rerun()

        # Temperature monitoring
        current_temp = st.session_state.simulator.experiment_data['temperature']
        if st.session_state.simulator.experiment_data['current_step'] >= 6:
            st.metric("Sterilization Temperature", "121°C", "High Temperature Sterilization")
        else:
            st.metric("Current Temperature", f"{current_temp}°C")


def simulate_plasmid_extraction():
    st.subheader("🧬 Plasmid Extraction Experiment")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### Protocol")

        steps = [
            "Collect bacterial cells (OD600 ≥ 2.0)",
            "Add Solution I for resuspension",
            "Add Solution II for lysis",
            "Add Solution III for neutralization",
            "Centrifuge and collect supernatant",
            "Column adsorption purification",
            "Elute plasmid DNA"
        ]

        completed_steps = st.session_state.simulator.experiment_data.get('plasmid_steps', 0)

        for i, step in enumerate(steps, 1):
            if i <= completed_steps:
                st.success(f"✓ {step}")
            else:
                st.info(f"{i}. {step}")

        if completed_steps < len(steps):
            if st.button("Next Extraction Step"):
                st.session_state.simulator.experiment_data['plasmid_steps'] = completed_steps + 1

                # Simulate extraction process
                with st.spinner(f"Executing Step {completed_steps + 1}..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)

                if completed_steps + 1 == len(steps):
                    # Complete extraction, generate random results
                    st.session_state.simulator.experiment_data['plasmid_yield'] = np.random.normal(150, 20)
                    st.success("🎉 Plasmid Extraction Complete!")

                st.rerun()

    with col2:
        st.write("### Plasmid Quality Detection")

        if st.session_state.simulator.experiment_data.get('plasmid_steps', 0) >= len(steps):
            # 鏄剧ず璐ㄧ矑娴撳害缁撴灉
            concentration = st.session_state.simulator.experiment_data['plasmid_yield']
            purity_260_280 = np.random.normal(1.8, 0.05)

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Plasmid concentration", f"{concentration:.1f} ng/μl")
            with col_b:
                st.metric("A260/A280", f"{purity_260_280:.2f}")

            # 璐ㄧ矑鐢垫吵妯℃嫙
            st.write("#### Plasmid Electrophoresis Analysis")
            fig = go.Figure()

            # 鏍囧噯鍒嗗瓙閲�
            sizes = [10000, 8000, 6000, 5000, 4000, 3000, 2000, 1000, 500]
            intensities = [0.1, 0.2, 0.15, 0.3, 0.25, 0.4, 0.35, 0.5, 0.2]

            fig.add_trace(go.Scatter(
                x=sizes, y=intensities,
                mode='lines',
                name='DNA Marker',
                line=dict(color='blue', width=3)
            ))

            # 鎻愬彇鐨勮川绮� - 妯℃嫙瓒呰灪鏃嬨€佺嚎鎬с€佸紑鐜舰寮�
            plasmid_forms = [
                (4500, 0.8, 'supercoiled'),
                (4500, 0.6, 'linear'),
                (4500, 0.4, 'open-ring')
            ]

            for size, intensity, name in plasmid_forms:
                fig.add_trace(go.Scatter(
                    x=[size], y=[intensity],
                    mode='markers+text',
                    name=name,
                    marker=dict(size=15, color='red'),
                    text=name,
                    textposition='top center'
                ))

            fig.update_layout(
                title="Plasmid Electrophoresis Analysis",
                xaxis_title="Molecular Weight (bp)",
                yaxis_title="Fluorescence Intensity",
                xaxis_type="log",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Please complete the plasmid extraction steps to view the results.")


def simulate_pcr():
    st.subheader("🔁 PCR Amplification Experiment")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### PCR reaction system")

        components = {
            "10×PCR Buffer": "2 μl",
            "dNTPs": "2 μl",
            "Primers": "1 μl each",
            "DNA template": "1 μl",
            "DNA polymerase": "0.5 μl",
            "ddH₂O": "12.5 μl",
            "Total volume": "20 μl"
        }

        for component, volume in components.items():
            st.text_input(component, volume, disabled=True)

        # PCR绋嬪簭璁剧疆
        st.write("### PCR Program")
        pcr_program = [
            ("Pre-denaturation", "95℃", "5 min"),
            ("Denaturation", "95℃", "45 s"),
            ("Annealing", "55-65℃", "45 s"),
            ("Extension", "72℃", "1 min/kb"),
            ("Final Extension", "72℃", "10 min")
        ]

        for step, temp, time1 in pcr_program:
            st.text(f"{step}: {temp} - {time1}")

        cycles = st.slider("Number of cycles", 20, 50, 30)
        st.session_state.simulator.experiment_data['pcr_cycles'] = cycles

    with col2:
        st.write("### Real-time amplification curve")

        if st.button("Initiate PCR amplification"):
            with st.spinner("PCR amplification in progress..."):
                progress_bar = st.progress(0)
                status_text = st.empty()

                # 妯℃嫙瀹炴椂鎵╁鏁版嵁
                cycles_data = []
                fluorescence_data = []

                placeholder = st.empty()
                # 寮€濮嬫ā鎷烶CR鎵╁
                for cycle in range(cycles + 1):
                    status_text.text(f"The {cycle}th iteration is currently in progress...")
                    progress_bar.progress(cycle / cycles)

                    # 鐢熸垚鎵╁鏇茬嚎鏁版嵁
                    if cycle <= 15:
                        # 鍩虹嚎鏈�
                        fluorescence = 1 + 0.1 * cycle + np.random.normal(0, 0.05)
                    elif cycle <= 25:
                        # 鎸囨暟鏈�
                        fluorescence = 1 + 2 ** ((cycle - 15) / 3) + np.random.normal(0, 0.1)
                    else:
                        # 骞冲彴鏈�
                        fluorescence = 50 + (cycle - 25) * 0.5 + np.random.normal(0, 0.2)

                    cycles_data.append(cycle)
                    fluorescence_data.append(fluorescence)

                    # 瀹炴椂鏇存柊鍥捐〃
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=cycles_data, y=fluorescence_data,
                        mode='lines+markers',
                        name='Fluorescent Signal',
                        line=dict(color='green', width=3)
                    ))

                    fig.update_layout(
                        title="Real-time PCR amplification curve",
                        xaxis_title="Cycle count",
                        yaxis_title="Fluorescence Intensity (RFU)",
                        height=300
                    )

                    placeholder.plotly_chart(fig, use_container_width=True)
                    time.sleep(0.5)

                st.session_state.simulator.experiment_data['pcr_product'] = fluorescence_data[-1]

            st.success("PCR amplification complete!")

            # 鏄剧ず鎵╁缁撴灉
            col_a, col_b = st.columns(2)
            with col_a:
                efficiency = np.random.normal(95, 2)
                st.metric("Amplification efficiency", f"{efficiency:.1f}%")
            with col_b:
                concentration = np.random.normal(50, 5)
                st.metric("Product concentration", f"{concentration:.1f} ng/μl")

            # PCR鍒嗗瓙杩囩▼鍔ㄧ敾
            st.write("#### PCR Molecular Process Simulation")
            fig, animate_func = create_pcr_animation()

            # 鍒涘缓鍔ㄧ敾棰勮
            frames = 30
            for i in range(frames):
                animate_func(i)
                plt.pause(0.1)

            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            st.image(buf, caption="Schematic Diagram of the PCR Molecular Process")


def simulate_gel_electrophoresis():
    st.subheader("🌊 Agarose Gel Electrophoresis")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### Gel Preparation")

        gel_conc = st.slider("Agarose concentration(%)", 0.5, 3.0, 1.0, 0.1)
        voltage = st.slider("Electrophoresis voltage(V)", 50, 150, 110)
        run_time = st.slider("Electrophoresis time(min)", 10, 60, 30)

        if st.button("Start electrophoresis"):
            with st.spinner("Electrophoresis in progress..."):
                progress_bar = st.progress(0)

                # 鍒涘缓鐢垫吵鍔ㄧ敾
                fig, animate_func = create_gel_electrophoresis_animation()
                placeholder = st.empty()

                for i in range(run_time + 1):
                    progress = i / run_time
                    progress_bar.progress(progress)

                    # 鏇存柊鍔ㄧ敾
                    animate_func(int(i * 30 / run_time))  # 缂╂斁甯ф暟
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', dpi=100)
                    buf.seek(0)
                    placeholder.image(buf, caption=f"Electrophoresis Progress: {progress * 100:.0f}%")

                    time.sleep(0.1)

                st.success("Electrophoresis complete!")

    with col2:
        st.write("### Analysis of Electrophoresis Results")

        # 鏈€缁堢數娉崇粨鏋�
        st.write("#### Final Electrophoresis Pattern")

        # 鍒涘缓妯℃嫙鐨勫嚌鑳跺浘鍍�
        fig, ax = plt.subplots(figsize=(8, 6))

        # 缁樺埗鍑濊兌鑳屾櫙
        gel = patches.Rectangle((1, 1), 8, 4, linewidth=2, edgecolor='black',
                                facecolor='lightblue', alpha=0.3)
        ax.add_patch(gel)

        # 缁樺埗鏍峰搧瀛�
        wells_x = [2, 3, 4, 5, 6, 7]
        well_labels = ['Marker', 'PCR product', 'negative control', 'positive control', 'Sample 1', 'Sample 2']
        for x, label in zip(wells_x, well_labels):
            well = patches.Circle((x, 4.5), 0.2, facecolor='white', edgecolor='black')
            ax.add_patch(well)
            ax.text(x, 4.8, label, ha='center', fontsize=8)

        # 缁樺埗DNA鏉″甫
        bands_data = [
            (2, [3.8, 3.2, 2.5, 1.8], 'Marker'),
            (3, [3.5], 'Target strip'),
            (4, [], 'negative'),
            (5, [3.5], 'positive'),
            (6, [3.6, 2.8], 'Sample 1'),
            (7, [3.4], 'Sample 2')
        ]

        for x, positions, label in bands_data:
            for pos in positions:
                band = patches.Rectangle((x - 0.15, pos - 0.1), 0.3, 0.2,
                                         facecolor='red', alpha=0.8)
                ax.add_patch(band)

        ax.set_xlim(0, 9)
        ax.set_ylim(0, 6)
        ax.set_title('Agarose Gel Electrophoresis Results')
        ax.set_xlabel('Lane')
        ax.set_ylabel('Migration Distance')

        st.pyplot(fig)

        # 鏉″甫鍒嗘瀽
        st.write("#### Band Intensity Analysis")
        samples = ['Marker', 'PCR product', 'negative control', 'positive control', 'Sample 1', 'Sample 2']
        intensities = [0.8, 0.9, 0.05, 0.95, 0.7, 0.75]

        fig_bar = px.bar(x=samples, y=intensities,
                         title='Band Intensity by Lane',
                         labels={'x': 'Sample', 'y': 'Relative Intensity'})
        st.plotly_chart(fig_bar, use_container_width=True)


def simulate_gel_recovery():
    st.subheader("🔍 DNA Gel Recovery Experiment")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Experimental Procedure")

        steps = [
            "Excise target DNA band",
            "Weigh gel fragment",
            "Add binding solution",
            "Incubate at 50-60°C for dissolution",
            "Transfer to recovery column",
            "Centrifuge to adsorb DNA",
            "Wash to remove impurities",
            "Elute purified DNA"
        ]

        current_step = st.session_state.simulator.experiment_data.get('gel_recovery_step', 0)

        for i, step in enumerate(steps, 1):
            if i <= current_step:
                st.success(f"✓ {step}")
            else:
                st.info(f"{i}. {step}")

        if st.button("Next Step") and current_step < len(steps):
            with st.spinner(f"Executing step {current_step + 1}..."):
                time.sleep(2)
                st.session_state.simulator.experiment_data['gel_recovery_step'] = current_step + 1
            st.rerun()

    with col2:
        st.write("### Gel Recovery Efficiency Monitoring")

        current_step = st.session_state.simulator.experiment_data.get('gel_recovery_step', 0)

        # DNA recovery efficiency simulation
        if current_step >= len(steps):
            st.success("🎉 Gel recovery complete!")

            # Display recovery results
            recovery_efficiency = np.random.normal(75, 5)
            dna_concentration = np.random.normal(45, 3)

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Recovery Efficiency", f"{recovery_efficiency:.1f}%")
            with col_b:
                st.metric("DNA Concentration", f"{dna_concentration:.1f} ng/μl")

            # Purity detection
            purity_260_280 = np.random.normal(1.8, 0.05)
            st.metric("A260/A280 Ratio", f"{purity_260_280:.2f}")

            # Recovered product quality verification
            st.write("#### Recovered Product Validation")
            fig = go.Figure()

            # Original PCR product vs recovered product
            samples = ['Original PCR Product', 'Gel-recovered Product']
            concentrations = [80, dna_concentration]
            purities = [1.75, purity_260_280]

            fig.add_trace(go.Bar(name='Concentration (ng/μl)', x=samples, y=concentrations,
                                 marker_color='lightblue'))
            fig.add_trace(go.Scatter(name='A260/A280 Ratio', x=samples, y=purities,
                                     yaxis='y2', marker=dict(size=10, color='red')))

            fig.update_layout(
                title='Comparison Before and After Gel Recovery',
                yaxis=dict(title='Concentration (ng/μl)'),
                yaxis2=dict(title='A260/A280 Ratio', overlaying='y', side='right'),
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            # Gel dissolution process visualization
            st.write("#### Gel Dissolution Status")
            dissolution_progress = min(current_step / len(steps), 1.0)

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=dissolution_progress * 100,
                number={'font': {'size': 48, 'color': '#1E90FF', 'family': 'Arial Black'}},
                delta={'reference': 100, 'increasing': {'color': '#00C851'}, 'decreasing': {'color': '#ff4444'}},
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Dissolution Progress"},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': '#1E90FF',
                             'tickfont': {'color': '#37474f'}},
                    'bar': {'color': 'rgba(30,144,255,0.8)', 'thickness': 0.25},
                    'bgcolor': 'rgba(240,248,255,0.5)',
                    'borderwidth': 3,
                    'bordercolor': '#1E90FF',
                    'steps': [
                        {'range': [0, 30], 'color': '#ffebee'},
                        {'range': [30, 70], 'color': '#fff9c4'},
                        {'range': [70, 100], 'color': '#e8f5e9'}],
                    'threshold': {'line': {'color': '#0d47a1', 'width': 6}, 'thickness': 0.8,
                                  'value': dissolution_progress * 100},

                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(255,255,255,0)',
                font={'color': '#0d47a1', 'family': 'Microsoft YaHei'},
                margin=dict(l=30, r=30, t=60, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)


def simulate_heat_shock():
    st.subheader("🔥 Heat Shock Transformation Experiment")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Experimental Protocol")

        steps = [
            "Prepare competent cells",
            "Ice bath for 30 minutes",
            "Add plasmid DNA",
            "Ice bath for 30 minutes",
            "Heat shock at 42°C for 90 seconds",
            "Rapid ice bath for 2-3 minutes",
            "Add LB medium for recovery",
            "Plate on selective media"
        ]

        current_step = st.session_state.simulator.experiment_data.get('heat_shock_step', 0)

        for i, step in enumerate(steps, 1):
            if i <= current_step:
                st.success(f"✓ {step}")
            else:
                st.info(f"{i}. {step}")

        if current_step < len(steps):
            if st.button("Execute Next Step"):
                # 鐗规畩澶勭悊鐑縺姝ラ
                if current_step == 4:  # 鐑縺鍓�
                    st.session_state.simulator.experiment_data['temperature'] = 0
                elif current_step == 5:  # 鐑縺
                    st.session_state.simulator.experiment_data['temperature'] = 42
                elif current_step == 6:  # 鍐版荡
                    st.session_state.simulator.experiment_data['temperature'] = 0

                with st.spinner(f"Executing step {current_step + 1}..."):
                    time.sleep(2)
                    st.session_state.simulator.experiment_data['heat_shock_step'] = current_step + 1
                st.rerun()

    with col2:
        st.write("### Real-time Monitoring")

        current_step = st.session_state.simulator.experiment_data.get('heat_shock_step', 0)
        current_temp = st.session_state.simulator.experiment_data.get('temperature', 0)

        # 娓╁害鏄剧ず
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_temp,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Temperature (°C)"},
            gauge={
                'axis': {'range': [0, 50]},
                'bar': {'color': "red" if current_temp > 40 else "blue"},
                'steps': [
                    {'range': [0, 4], 'color': "lightblue"},
                    {'range': [4, 37], 'color': "lightgreen"},
                    {'range': [37, 50], 'color': "lightcoral"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 42}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # 杞寲鏁堢巼璁＄畻
        if current_step >= len(steps):
            st.success("✅ Heat shock transformation complete!")

            # 妯℃嫙杞寲缁撴灉
            colonies = np.random.poisson(150)
            efficiency = colonies / 0.1  # 鍋囪浣跨敤0.1渭g DNA

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Transformant Count: ", f"{colonies}")
            with col_b:
                st.metric("Transformation Efficiency: ", f"{efficiency:,.0f} CFU/μg")

            # 闃虫€у厠闅嗛獙璇�
            positive_rate = np.random.normal(85, 5)
            st.metric("Positive Clone Rate", f"{positive_rate:.1f}%")

            # 鑿岃惤鐢熼暱妯℃嫙
            st.write("#### Transformant Growth Status")
            time_points = np.linspace(0, 16, 100)
            growth_curve = colonies * (1 - np.exp(-0.3 * time_points))

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time_points, y=growth_curve,
                mode='lines',
                name='Colony growth',
                line=dict(color='green', width=3)
            ))
            fig.update_layout(
                title='Transformant Overnight Growth Curve',
                xaxis_title='Time (hours)',
                yaxis_title='Colony Count'
            )
            st.plotly_chart(fig, use_container_width=True)


def simulate_electroporation():
    st.subheader("⚡ Electrocompetent Cell Preparation and Transformation")

    tab1, tab2 = st.tabs(["Electrocompetent Cell Preparation", "Electroporation Transformation"])

    with tab1:
        st.write("### Electrocompetent Cell Preparation")

        preparation_steps = [
            "Inoculate single colony on LB medium",
            "Incubate at 37°C for overnight culture",
            "Transfer to fresh medium",
            "Grow to OD600=0.5",
            "Cool on ice for 15 minutes",
            "Centrifuge to collect cells",
            "Pre-cool 10% glycerol wash",
            "Store at -80°C"
        ]

        prep_step = st.session_state.simulator.experiment_data.get('prep_step', 0)

        for i, step in enumerate(preparation_steps, 1):
            if i <= prep_step:
                st.success(f"✓ {step}")
            else:
                st.info(f"{i}. {step}")

        if prep_step < len(preparation_steps):
            if st.button("Execute Preparation Step"):
                with st.spinner(f"Executing step {prep_step + 1}..."):
                    time.sleep(2)
                    st.session_state.simulator.experiment_data['prep_step'] = prep_step + 1

                    # 鏇存柊缁嗚弻OD鍊�
                    if prep_step + 1 == 4:  # 鍩瑰吇鑷砄D600=0.5
                        st.session_state.simulator.experiment_data['bacterial_od'] = 0.5

                st.rerun()

        # 缁嗚弻鐢熼暱鏇茬嚎
        if prep_step >= 2:
            st.write("#### Bacterial Growth Monitoring")

            # 鍒涘缓鐢熼暱鏇茬嚎鍔ㄧ敾
            fig, animate_func = create_bacterial_growth_animation()

            # 鏄剧ず褰撳墠鐢熼暱鐘舵€�
            animate_func(min(prep_step * 5, 30))  # 鏍规嵁姝ラ鏄剧ず鐩稿簲鐢熼暱闃舵
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            st.image(buf, caption="Bacterial Growth Curve")

            current_od = st.session_state.simulator.experiment_data.get('bacterial_od', 0)
            st.metric("Current OD600", f"{current_od:.3f}")

    with tab2:
        st.write("### Electroporation Transformation")

        electro_steps = [
            "Melt electrocompetent cells",
            "Add DNA sample",
            "Ice bath for 10 minutes",
            "Transfer to electroporation cuvette",
            "Set electroporation parameters",
            "Perform electroporation",
            "Quickly add recovery medium",
            "Incubate at 37°C for 1-2 hours",
            "Plate on selective media"
        ]

        electro_step = st.session_state.simulator.experiment_data.get('electro_step', 0)

        for i, step in enumerate(electro_steps, 1):
            if i <= electro_step:
                st.success(f"✓ {step}")
            else:
                st.info(f"{i}. {step}")

        # 鐢靛嚮鍙傛暟璁剧疆
        if electro_step >= 4 and electro_step <= 6:
            st.write("#### Electroporation Parameters")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                voltage = st.slider("Voltage (kV)", 1.0, 3.0, 2.5, 0.1)
            with col_b:
                capacitance = st.slider("Capacitance (μF)", 10, 50, 25)
            with col_c:
                resistance = st.slider("Resistance (Ω)", 100, 400, 200)

        if electro_step < len(electro_steps):
            if st.button("Execute Next Transformation Step"):
                # 鐗规畩澶勭悊鐢靛嚮姝ラ
                if electro_step == 5:  # 鐢靛嚮
                    with st.spinner("Performing electroporation..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        st.success("⚡ Electroporation completed!")

                st.session_state.simulator.experiment_data['electro_step'] = electro_step + 1
                st.rerun()

        # 杞寲缁撴灉灞曠ず
        if electro_step >= len(electro_steps):
            st.success("🎉 Electroporation experiment completed!")

            # 妯℃嫙鐢靛嚮杞寲鏁堢巼
            colonies_electro = np.random.poisson(5000)  # 鐢靛嚮杞寲鏁堢巼鏇撮珮
            efficiency_electro = colonies_electro / 0.01  # 鍋囪浣跨敤0.01渭g DNA

            col_x, col_y = st.columns(2)
            with col_x:
                st.metric("Electroporation Transformant Count", f"{colonies_electro:,}")
            with col_y:
                st.metric("Electroporation Efficiency", f"{efficiency_electro:,.0f} CFU/μg")

            # 涓庣儹婵€杞寲瀵规瘮
            st.write("#### Transformation Method Comparison")
            methods = ['Heat Shock Transformation', 'Electroporation Transformation']
            heat_shock_colonies = np.random.poisson(150)
            heat_shock_efficiency = heat_shock_colonies / 0.1

            comparison_data = {
                'Methods': methods * 2,
                'Types': ['Number of Conversion Subunits'] * 2 + ['Conversion Efficiency'] * 2,
                'Value': [heat_shock_colonies, colonies_electro,
                          heat_shock_efficiency, efficiency_electro]
            }

            df = pd.DataFrame(comparison_data)
            fig = px.bar(df, x='Methods', y='Value', color='Types', barmode='group',
                         title='Efficiency Comparison of Different Conversion Methods')
            st.plotly_chart(fig, use_container_width=True)


def show_engineering_bacteria():
    st.header("🧫 Engineering Bacteria Construction Experiment")
    if is_kids_mode():
        st.info(
            "Let's build super bacteria together! We'll put the best genes together like building blocks to make tiny factories that create amazing things! ✓")

    tab1, tab2, tab3 = st.tabs(
        ["Downstream Plasmid Construction", "Upstream Plasmid Construction", "Gene Integration Validation"])

    with tab1:
        st.subheader("21a-raldh-IIdR-blh Plasmid Construction")

        # 瀹為獙姒傝堪
        st.markdown("""
        **Experimental Objective**: Construct a recombinant plasmid containing the raldh, IIdR, and blh genes
        - **raldh**: Retinal aldehyde dehydrogenase gene
        - **IIdR**: Transcription regulatory factor   
        - **blh**: β-carotene hydroxylase gene
        """)

        # 鍩哄洜鐗囨鎵╁
        st.write("### Gene Fragment Amplification Validation")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**blh gene amplification**")
            # 妯℃嫙鐢垫吵缁撴灉
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.barh([0], [0.8], color='red', alpha=0.7)
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)
            ax.set_title('blh gene (~1.2 kb)')
            ax.axis('off')
            st.pyplot(fig)

        with col2:
            st.write("**IIdR gene amplification**")
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.barh([0], [0.6], color='green', alpha=0.7)
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)
            ax.set_title('IIdR gene (~0.8 kb)')
            ax.axis('off')
            st.pyplot(fig)

        with col3:
            st.write("**rald gene amplification**")
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.barh([0], [0.9], color='blue', alpha=0.7)
            ax.set_xlim(0, 1)
            ax.set_ylim(-1, 1)
            ax.set_title('raldh gene (~1.5 kb)')
            ax.axis('off')
            st.pyplot(fig)

        # 鍚屾簮閲嶇粍妯℃嫙
        st.write("### Homologous Recombination Construction")

        if st.button("Execute Homologous Recombination Construction"):
            with st.spinner("Homologous Recombination in progress..."):
                steps = [
                    "Linearize pET-21a Vector",
                    "Mix Three Gene Fragments",
                    "Add C115 Recombinase",
                    "Incubate at 50°C for 30 minutes",
                    "Transform Competent Cells",
                    "Screen Positive Clones"
                ]

                progress_bar = st.progress(0)
                status_text = st.empty()

                for i, step in enumerate(steps):
                    status_text.text(f"Step {i + 1}/{len(steps)}: {step}")
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(1.5)

                st.success("🎉 Recombinant Plasmid 21a-raldh-IIdR-blh Construction Successful!")

        # 璐ㄧ矑鍥捐氨
        st.write("### Recombinant Plasmid Map")
        fig, ax = plt.subplots(figsize=(10, 6))

        # 缁樺埗绠€鍖栫殑璐ㄧ矑鍥捐氨
        circle = plt.Circle((0.5, 0.5), 0.4, fill=False, edgecolor='black', linewidth=3)
        ax.add_patch(circle)

        # 鏍囪鍩哄洜浣嶇疆
        genes = [
            (0, 'AmpR', 'red'),
            (90, 'ori', 'blue'),
            (180, 'raldh', 'green'),
            (240, 'IIdR', 'orange'),
            (300, 'blh', 'purple')
        ]

        for angle, name, color in genes:
            rad = np.radians(angle)
            x = 0.5 + 0.35 * np.cos(rad)
            y = 0.5 + 0.35 * np.sin(rad)
            ax.plot([0.5, x], [0.5, y], color=color, linewidth=2)
            ax.text(x * 1.1, y * 1.1, name, ha='center', va='center',
                    fontsize=10, color=color, weight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('21a-raldh-IIdR-blh Recombinant Plasmid Map', fontsize=14)

        st.pyplot(fig)

    with tab2:
        st.subheader("21a-crtEBIY Plasmid Construction")

        st.markdown("""
        **Experimental Objectives**: Construct a recombinant plasmid containing the crTE, crTB, crTI, and crY gene clusters.
        - **crtE**: Bovine Calcium-Manganese Pyrophosphate Synthase
        - **crtB**: Octahydrolycopene synthase
        - **crtI**: Octahydrolycopene dehydrogenase
        - **crtY**: Lycopene Cyclase
        """)

        st.write("### crtEBIY Gene Cluster Amplification")

        # 鍩哄洜绨囩粨鏋勫彲瑙嗗寲
        fig, ax = plt.subplots(figsize=(12, 3))

        genes = [
            (0, 2, 'crtE', '#FF6B6B'),
            (2.2, 4, 'crtB', '#4ECDC4'),
            (4.2, 6, 'crtI', '#45B7D1'),
            (6.2, 8, 'crtY', '#96CEB4')
        ]

        for start, end, name, color in genes:
            ax.barh(0, end - start, left=start, height=0.6, color=color, alpha=0.8)
            ax.text((start + end) / 2, 0, name, ha='center', va='center',
                    fontsize=12, weight='bold')

        ax.set_xlim(0, 8)
        ax.set_ylim(-1, 1)
        ax.set_xlabel('Gene Position (kb)')
        ax.set_title('crtEBIY Gene Cluster Structure')
        ax.axis('off')

        st.pyplot(fig)

        # 鏋勫缓杩囩▼妯℃嫙
        if st.button("Construct 21a-crtEBIY Plasmid"):
            with st.spinner("Plasmid construction in progress..."):
                progress_bar = st.progress(0)

                construction_steps = [
                    "PCR Amplify crtEBIY Fragment",
                    "Gel Extraction and Purification",
                    "Linearize pET-21a Vector",
                    "Homologous Recombination Ligation",
                    "Transformation and Screening",
                    "Positive Clone Validation"
                ]

                for i, step in enumerate(construction_steps):
                    st.write(f"🔧 {step}")
                    progress_bar.progress((i + 1) / len(construction_steps))
                    time.sleep(1.5)

                st.success("🎉 21a-crtEBIY Plasmid Construction Successful!")

    with tab3:
        st.subheader("Gene Integration Validation")

        st.write("### Colony PCR Validation")

        # 妯℃嫙鑿岃惤PCR缁撴灉
        fig, ax = plt.subplots(figsize=(10, 4))

        # 娉抽亾鏁版嵁
        lanes = [
            ('Marker', [], True),
            ('Wild-type', [2223], False),
            ('Transgene 1', [3552], True),
            ('Transgene 2', [3552], True),
            ('Transgene 3', [3552], True),
            ('Negative Control', [], False)
        ]

        for i, (label, sizes, is_positive) in enumerate(lanes):
            # 缁樺埗娉抽亾
            ax.plot([i, i], [0, 4000], 'k-', linewidth=2)
            ax.text(i, -200, label, ha='center', fontsize=10)

            # 缁樺埗鏉″甫
            for size in sizes:
                intensity = 0.8 if is_positive else 0.3
                ax.bar(i, 100, bottom=size - 50, width=0.3,
                       color='red', alpha=intensity)
                if is_positive:
                    ax.text(i, size, f'{size} bp', ha='center',
                            va='bottom', fontsize=8)

        ax.set_ylim(0, 4000)
        ax.set_xlim(-0.5, len(lanes) - 0.5)
        ax.set_ylabel('Molecular Weight (bp)')
        ax.set_title('Gene Integration Colony PCR Validation')
        ax.invert_yaxis()  # 鐢垫吵鍥句粠涓婂埌涓�

        st.pyplot(fig)

        # 鏁村悎鏁堢巼缁熻
        st.write("### Integration Efficiency Statistics")

        integration_data = {
            'Experiment Batch': ['Batch 1', 'Batch 2', 'Batch 3', 'Batch 4'],
            'Positive Clones': [8, 12, 15, 11],
            'Total Clones': [24, 30, 32, 28],
            'Integration Efficiency %': [33.3, 40.0, 46.9, 39.3]
        }

        df = pd.DataFrame(integration_data)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(df, x='Experiment Batch', y='Integration Efficiency %',
                         title='Gene Integration Efficiency Statistics',
                         color='Integration Efficiency %', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.scatter(df, x='Total Clones', y='Positive Clones',
                             size='Integration Efficiency %', color='Experiment Batch',
                             title='Clone Screening Distribution')
            st.plotly_chart(fig, use_container_width=True)


def show_crispr_cas9():
    st.header("⚡ CRISPR-Cas9 Gene Integration System")
    if is_kids_mode():
        st.info(
            "CRISPR is like a super-precise pair of scissors that helps us 'cut and paste' on DNA! It's like editing a recipe to make something even more delicious!")

    st.write("### sgRNA Design and Validation")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**sgRNA Sequence Design**")
        target_sequence = st.text_input("Target Sequence (20bp)", "cgtagagtgggaacacgtcg")
        pam_sequence = st.text_input("PAM Sequence", "CGG", disabled=True)

        if st.button("Validate sgRNA Design"):
            if len(target_sequence) == 20:
                # 璁＄畻sgRNA鐗规€�
                gc_content = (target_sequence.count('G') + target_sequence.count('C')) / 20 * 100
                off_target_score = np.random.normal(0.85, 0.05)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("GC Content", f"{gc_content:.1f}%")
                with col_b:
                    st.metric("Off-target Prediction Score", f"{off_target_score:.2f}")

                if gc_content >= 40 and gc_content <= 60:
                    st.success("✅ sgRNA Design Excellent")
                else:
                    st.warning("⚠️ GC Content not in ideal range (40-60%)")
            else:
                st.error("❌ sgRNA Length must be 20bp")

    with col2:
        st.write("**CRISPR-Cas9 Working Principle**")

        # 鍒涘缓CRISPR宸ヤ綔鍘熺悊鍔ㄧ敾
        fig, ax = plt.subplots(figsize=(8, 6))

        # 缁樺埗DNA
        x_dna = np.linspace(1, 7, 100)
        y_dna = 5 + 0.2 * np.sin(2 * np.pi * x_dna)
        ax.plot(x_dna, y_dna, 'b-', linewidth=3, label='Target DNA')

        # 缁樺埗Cas9铔嬬櫧
        cas9_x, cas9_y = 4, 6
        cas9 = patches.Circle((cas9_x, cas9_y), 0.3, facecolor='orange', alpha=0.8)
        ax.add_patch(cas9)
        ax.text(cas9_x, cas9_y, 'Cas9', ha='center', va='center', fontsize=10)

        # 缁樺埗sgRNA
        ax.plot([cas9_x, 4.5], [cas9_y, 5.2], 'g-', linewidth=2)
        ax.text(4.7, 5.0, 'sgRNA', fontsize=10, color='green')

        # 缁樺埗鍒囧壊浣嶇偣
        ax.plot([4.5, 4.5], [4.8, 5.2], 'r--', linewidth=2, label='Cleavage Site')

        ax.set_xlim(0, 8)
        ax.set_ylim(4, 7)
        ax.set_title('CRISPR-Cas9 Gene Editing Principle')
        ax.legend()
        ax.axis('off')

        st.pyplot(fig)

    # 铻嶅悎PCR妯℃嫙
    st.write("### Donor Fragment Construction - Fusion PCR")

    pcr_steps = [
        "First Round PCR: Amplify Upstream Homology Arm",
        "Second Round PCR: Amplify Downstream Homology Arm",
        "Third Round PCR: Amplify Selection Marker",
        "Overlap Extension PCR: Fragment Fusion",
        "Gel Extraction and Purification of Donor Fragment"
    ]

    current_pcr_step = st.session_state.simulator.experiment_data.get('fusion_pcr_step', 0)

    for i, step in enumerate(pcr_steps, 1):
        if i <= current_pcr_step:
            st.success(f"✓ {step}")
        else:
            st.info(f"{i}. {step}")

    if current_pcr_step < len(pcr_steps):
        if st.button("Execute Next PCR"):
            with st.spinner(f"Executing {pcr_steps[current_pcr_step]}..."):
                time.sleep(2)
                st.session_state.simulator.experiment_data['fusion_pcr_step'] = current_pcr_step + 1
            st.rerun()

    # 鐢靛嚮杞寲妯℃嫙
    if current_pcr_step >= len(pcr_steps):
        st.write("### Electroporation Transformation and Screening")

        if st.button("Execute Electroporation Transformation"):
            with st.spinner("Electroporation transformation in progress..."):
                steps = [
                    "Prepare Electrocompetent Cells",
                    "Mix Donor Fragment with sgRNA Plasmid",
                    "Ice bath for 10 minutes",
                    "Electroporation Transformation (2.5kV, 5ms)",
                    "Recovery Culture for 1 Hour",
                    "Spread Double Antibiotic Plate",
                    "Incubate at 37°C for Overnight Culture"
                ]

                progress_bar = st.progress(0)
                for i, step in enumerate(steps):
                    st.write(f"⚡ {step}")
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(1)

                st.success("🎉 Electroporation transformation completed! Starting to screen positive clones...")

        # 绛涢€夌粨鏋�
        st.write("#### Positive Clone Screening Results")

        screening_data = {
            'Screening Round': ['First Round', 'Second Round', 'Third Round'],
            'Total Clone Count': [156, 89, 45],
            'Positive Clone Count': [23, 15, 12],
            'Positive Rate %': [14.7, 16.9, 26.7]
        }

        df = pd.DataFrame(screening_data)

        fig = px.line(df, x='Screening Round', y='Positive Rate %',
                      title='Positive Clone Screening Efficiency', markers=True)
        st.plotly_chart(fig, use_container_width=True)


def show_results_analysis():
    st.header("📊 Comprehensive Experimental Results Analysis")
    if is_kids_mode():
        st.info(
            "Time to see our results! Let's check if our experiments worked using pictures and numbers that tell us the story of our amazing bacteria!")

    tab1, tab2, tab3, tab4 = st.tabs(["Gene Expression Validation", "Protein Function Analysis", "Metabolite Detection",
                                      "Therapeutic Effect Evaluation"])

    with tab1:
        st.subheader("Gene Expression Validation")

        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Real-time Quantitative PCR")

            # 妯℃嫙qPCR鏁版嵁
            genes = ['raldh', 'IIdR', 'blh', 'crtE', 'crtB', 'crtI', 'crtY']
            expression_levels = np.random.exponential(2, len(genes))
            expression_levels = expression_levels / np.max(expression_levels)  # 褰掍竴鍖�

            fig = px.bar(x=genes, y=expression_levels,
                         title='Engineering Bacteria Gene Expression Levels',
                         labels={'x': 'Gene', 'y': 'Relative Expression Level'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("#### Transcriptome Analysis")

            # 妯℃嫙鐑浘鏁版嵁
            samples = ['Wild-type', 'Engineered Strain 1', 'Engineered Strain 2', 'Engineered Strain 3']
            metabolic_genes = ['Carbohydrate Metabolism', 'Lipid Metabolism', 'Amino Acid Metabolism',
                               'Vitamin Metabolism', 'Pigment Synthesis']
            expression_data = np.random.rand(len(metabolic_genes), len(samples))

            fig = px.imshow(expression_data,
                            x=samples,
                            y=metabolic_genes,
                            title='Metabolic Pathway Gene Expression Heatmap',
                            color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Protein Function Analysis")

        st.write("#### SDS-PAGE Protein Electrophoresis")

        # 妯℃嫙铔嬬櫧鐢垫吵缁撴灉
        fig, ax = plt.subplots(figsize=(10, 6))

        # 铔嬬櫧Marker
        marker_sizes = [180, 130, 100, 70, 55, 40, 35, 25]
        marker_ints = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        for size, intensity in zip(marker_sizes, marker_ints):
            ax.barh(0, 10, left=size - 5, height=0.2, color='black', alpha=intensity)
            ax.text(size, -0.1, f'{size}kDa', ha='center', fontsize=8)

        # 鏍峰搧鏉″甫
        samples = [
            ('Wild-type’', []),
            ('Engineered bacteria - whole protein', [55, 45, 35]),
            ('Engineered bacteria - purified', [55]),
            ('Positive control', [55])
        ]

        for i, (label, bands) in enumerate(samples):
            y_pos = i + 1
            ax.text(-20, y_pos, label, ha='right', va='center', fontsize=10)

            for band in bands:
                ax.barh(y_pos, 10, left=band - 5, height=0.3, color='red', alpha=0.8)

        ax.set_xlim(0, 200)
        ax.set_ylim(-0.5, len(samples) + 0.5)
        ax.set_xlabel('Molecular Weight (kDa)')
        ax.set_title('SDS-PAGE Protein Electrophoresis Analysis')
        ax.invert_yaxis()

        st.pyplot(fig)

        # 閰舵椿鎬у垎鏋�
        st.write("#### Enzyme Activity Assay")

        enzyme_data = {
            'Enzyme': ['RALDH', 'IIdR', 'BLH', 'CRTE', 'CRTB', 'CRTI', 'CRTY'],
            'Specific Activity (U/mg)': [45, 32, 28, 65, 58, 42, 39],
            'Conversion Rate (%)': [88, 75, 82, 92, 89, 85, 78]
        }

        df = pd.DataFrame(enzyme_data)

        fig = px.scatter(df, x='Specific Activity (U/mg)', y='Conversion Rate (%)', size='Specific Activity (U/mg)',
                         color='Enzyme', title='Relationship Between Key Enzyme Activity and Conversion Rate')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Metabolite Detection")

        col1, col2 = st.columns(2)

        with col1:
            st.write("#### ATRA Production Analysis")

            # 妯℃嫙HPLC妫€娴嬬粨鏋�
            time_points = np.linspace(0, 10, 100)
            atra_signal = 5 * np.exp(-0.5 * (time_points - 5) ** 2) + 0.1 * np.random.normal(size=100)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time_points, y=atra_signal,
                mode='lines',
                name='ATRA Peak',
                line=dict(color='blue', width=3)
            ))

            fig.update_layout(
                title='HPLC Detection - ATRA Standard',
                xaxis_title='Retention Time (min)',
                yaxis_title='Signal Intensity'
            )
            st.plotly_chart(fig, use_container_width=True)

            # 浜ч噺缁熻
            production_data = {
                'Culture Time (hours)': [12, 24, 36, 48, 60, 72],
                'ATRA Production (mg/L)': [0.5, 2.3, 5.8, 8.9, 10.2, 9.8],
                'Cell Density (OD600)': [0.8, 2.1, 4.5, 6.8, 8.2, 8.1]
            }

            df_prod = pd.DataFrame(production_data)

            fig = px.line(df_prod, x='Culture Time (hours)', y=['ATRA Production (mg/L)', 'Cell Density (OD600)'],
                          title='ATRA Fermentation Production Kinetics')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("#### Metabolomics Analysis")

            # 妯℃嫙浠ｈ阿鐗╁彉鍖�
            metabolites = ['glucose’', 'lactic acid', 'acetic acid', 'ethanol', 'ATP', 'NADH']
            wild_type = np.random.exponential(1, len(metabolites))
            engineered = wild_type * np.random.uniform(0.5, 2, len(metabolites))

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=wild_type,
                theta=metabolites,
                fill='toself',
                name='Wild-type'
            ))
            fig.add_trace(go.Scatterpolar(
                r=engineered,
                theta=metabolites,
                fill='toself',
                name='Engineered strain'
            ))

            fig.update_layout(
                title='Metabolomics Comparative Analysis',
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Therapeutic Effect Evaluation")

        st.write("#### In Vitro Antitumor Activity")

        # 妯℃嫙缁嗚優姣掓€у疄楠�
        concentrations = [0, 0.1, 1, 10, 100]  # 渭M
        cell_viability = {
            'ATRA Standard': [100, 95, 75, 45, 20],
            'Engineered Bacteria Product': [100, 92, 78, 48, 22],
            'FOLFOX4': [100, 85, 60, 35, 15],
            'Control': [100, 98, 96, 94, 92]
        }

        fig = go.Figure()
        for treatment, viability in cell_viability.items():
            fig.add_trace(go.Scatter(
                x=concentrations, y=viability,
                mode='lines+markers',
                name=treatment
            ))

        fig.update_layout(
            title='ATRA Cytotoxicity to Hepatocellular Carcinoma Cells',
            xaxis_title='Concentration (μM)',
            yaxis_title='Cell Survival Rate (%)',
            xaxis_type='log'
        )

        st.plotly_chart(fig, use_container_width=True)

        # 鍔ㄧ墿瀹為獙鏁堟灉
        st.write("#### Animal Model Efficacy")

        animal_data = {
            'Treatment Group': ['Control Group', 'FOLFOX4', 'ATRA Standard', 'Engineered Bacteria ATRA'],
            'Tumor Volume (mm³)': [1250, 680, 420, 350],
            'Survival (days)': [45, 68, 82, 95],
            'Body Weight Change (%)': [-15, -25, -8, -5]
        }

        df_animal = pd.DataFrame(animal_data)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(df_animal, x='Treatment Group', y='Tumor Volume (mm³)',
                         title='Treatment 4 Weeks Post-Tumor Volume', color='Tumor Volume (mm³)')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(df_animal, x='Treatment Group', y='Survival (days)',
                         title='Median Survival Time Comparison', color='Survival (days)')
            st.plotly_chart(fig, use_container_width=True)


# 🌈 添加儿童版的CSS样式
if is_kids_mode():
    st.markdown("""
        <style>
        /* 整体背景渐变 */
        body[data-app-mode="Kids"] {
            background: linear-gradient(135deg, #FAD0C4 0%, #FFD1FF 100%);
            color: white !important;
            font-family: "Comic Sans MS", "Chalkboard", "Comic Neue", cursive !important;
        }

        /* 侧边栏渐变背景 */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #A1C4FD 0%, #C2E9FB 100%) !important;
            color: white !important;
        }

        /* 侧边栏文字 */
        [data-testid="stSidebar"] * {
            color: gray !important;
            font-family: "Comic Sans MS", "Chalkboard", "Comic Neue", cursive !important;
        }

        /* 标题与子标题样式 */
        h1, h2, h3, h4, h5, h6 {
            color: gray !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            font-family: "Comic Sans MS", "Chalkboard", "Comic Neue", cursive !important;
        }

        /* 按钮样式可爱风 */
        button, .stButton > button {
            background: linear-gradient(90deg, #FF9A9E 0%, #FAD0C4 100%) !important;
            color: white !important;
            border-radius: 15px !important;
            border: none !important;
            font-family: "Comic Sans MS", "Comic Neue", cursive !important;
        }

        button:hover, .stButton > button:hover {
            background: linear-gradient(90deg, #FBC2EB 0%, #A6C1EE 100%) !important;
        }

        /* 调整输入框和下拉菜单的文字颜色 */
        .stSelectbox label, .stSlider label {
            color: white !important;
            font-family: "Comic Sans MS", "Comic Neue", cursive !important;
        }
        </style>
    """, unsafe_allow_html=True)

if is_pro_mode():
    st.markdown("""
        <style>
        body[data-app-mode="Professional"] {
            background: white !important;
            color: black !important;
            font-family: "Arial", "Helvetica", sans-serif !important;
        }
        [data-testid="stSidebar"] {
            background: #f8f9fa !important;
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

# 娣诲姞CSS鏍峰紡
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .experiment-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }

    /* 鍎跨鐗堟ā寮忔牱寮� */
    body[data-app-mode="Kids"] {
        background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888) !important;
        min-height: 100vh;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* 鍎跨鐗堟ā寮忎笅渚ц竟鏍忔牱寮� */
    body[data-app-mode="Kids"] section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d) !important;
    }

    body[data-app-mode="Kids"] * {
        color: white !important;
    }

    /* Exceptions for specific elements that should not be white */
    body[data-app-mode="Kids"] .stButton>button,
    body[data-app-mode="Kids"] .stTextInput>div>div>input,
    body[data-app-mode="Kids"] .stTextArea>textarea {
        color: #333 !important;
    }

    /* 鍎跨鐗堟ā寮忎笅涓诲唴瀹瑰尯鍩熸牱寮� */
    body[data-app-mode="Kids"] section[data-testid="stMain"] {
        background: transparent !important;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    /* 鍎跨鐗堟ā寮忎笅涓诲唴瀹瑰尯鍩熺殑鐩存帴瀛愬厓绱� */
    body[data-app-mode="Kids"] main {
        background: transparent !important;
    }

    /* 鍎跨鐗堟ā寮忎笅瀹為獙鍗＄墖鏍峰紡 */
    body[data-app-mode="Kids"] .experiment-card {
        background: rgba(255, 255, 255, 0.2);
        border-left: 5px solid #98F5F9;
    }

    /* 鍎跨鐗堟ā寮忎笅杩涘害鏉℃牱寮� */
    body[data-app-mode="Kids"] .stProgress > div > div > div > div {
        background-color: #98F5F9;
    }

    /* 涓撲笟鐗堟ā寮忔牱寮� - 淇濇寔鍘熸湁鏍峰紡 */
    body[data-app-mode="Professional"] {
        background: #f0f2f6 !important;
    }

    body[data-app-mode="Professional"] section[data-testid="stSidebar"] {
        background: #f0f2f6 !important;
    }

    body[data-app-mode="Professional"] section[data-testid="stSidebar"] * {
        color: #262730 !important;
    }

    body[data-app-mode="Professional"] .experiment-card {
        background-color: #f0f2f6;
        border-left: 5px solid #1f77b4;
    }

    body[data-app-mode="Professional"] .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    # 璁剧疆榛樿浼氳瘽鐘舵€佷互渚挎祴璇�
    import streamlit as st

    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = "Professional"

    main()


