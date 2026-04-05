import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(page_title="Juskvi Inventory Engine v2.6", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 {color: #00583E !important; font-family: 'Helvetica Neue', sans-serif;}
    div[data-testid="stExpander"] {border: none !important; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); border-radius: 10px; margin-bottom: 12px;}
    div[data-testid="stExpander"] summary {background-color: #00583E !important; border-radius: 10px; padding: 12px !important;}
    div[data-testid="stExpander"] summary p {color: white !important; font-size: 1.1rem !important; font-weight: 600 !important; margin-bottom: 0px !important;}
    .stButton>button {background-color: #DF1934 !important; color: white !important; border-radius: 8px; border: none; font-weight: bold; font-size: 1.2rem !important; padding: 15px !important; width: 100%; box-shadow: 0px 4px 10px rgba(223, 25, 52, 0.3); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px;}
    .stButton>button:hover {background-color: #9c0c20 !important; box-shadow: 0px 6px 15px rgba(223, 25, 52, 0.5);}
    input[type="number"] {text-align: center !important; font-size: 1.3rem !important; font-weight: bold !important;}
    </style>
""", unsafe_allow_html=True)

# --- 2. SECURITY AUTHENTICATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Papa John's Inventory System")
    st.caption("Store 04185 | Authorized Personnel Only")
    st.divider()
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Secure Login"):
        if username == "MGR" and password == "Papa4185":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Access Denied: Invalid Credentials")
    st.stop()

# --- 3. THE MASTER DATA DICTIONARY (COMPLETE v2.6 SYNC) ---
master_inventory = [
    # --- WALK-IN SECTION ---
    [1085, "Crust, Parbaked Pan Pizza", "Bag", "Walk-in Section", 4.0, 0.0],
    [1075, "Dough Tray 10", "Tray", "Walk-in Section", 1.0, 0.0],
    [1076, "DOUGH M, 12 INCH", "Tray", "Walk-in Section", 1.0, 0.0],
    [1080, "Dough Tray 14", "Tray", "Walk-in Section", 1.0, 0.0],
    [1218, "Alfredo Sauce", "Pouch", "Walk-in Section", 3.0, 1.0],
    [1086, "Frozen Gluten Free Crust", "Case", "Walk-in Section", 1.0, 0.0],
    [1002, "Bulk Ranch Sauce", "Pouch", "Walk-in Section", 8.0, 1.0],
    [1071, "Anchovies", "Can", "Walk-in Section", 25.0, 0.0],
    [1178, "Philly Cheesesteak", "Bag", "Walk-in Section", 4.0, 1.0],
    [1064, "Beef", "Bag", "Walk-in Section", 2.0, 1.0],
    [1167, "Canadian Bacon", "Bag", "Walk-in Section", 2.0, 1.0],
    [1049, "Bacon", "Bag", "Walk-in Section", 4.0, 1.0],
    [1095, "Grilled Chicken", "Bag", "Walk-in Section", 2.0, 0.0],
    [1093, "WINGS, BONELESS", "Bag", "Walk-in Section", 2.0, 0.0],
    [1092, "WING, ROASTED 20 LB", "Bag", "Walk-in Section", 4.0, 0.0],
    [1257, "Three Cheese Blend", "Bag", "Walk-in Section", 2.0, 1.0],
    [1159, "Two Cheese P/R", "Bag", "Walk-in Section", 2.0, 1.0],
    [1016, "Green Peppers, Sliced", "Bag", "Walk-in Section", 4.0, 1.0],
    [1017, "Onions, Sliced", "Bag", "Walk-in Section", 4.0, 1.0],
    [1052, "Fresh Spinach", "Bag", "Walk-in Section", 4.0, 1.0],
    [1019, "Tomatoes, Diced Roma", "Tray", "Walk-in Section", 2.0, 0.0],
    [1065, "Sausage", "Bag", "Walk-in Section", 4.0, 1.0],
    [1066, "Italian Sausage", "Bag", "Walk-in Section", 4.0, 1.0],
    [1051, "Mushrooms-fresh", "Pail", "Walk-in Section", 2.0, 0.0],
    [1074, "Frozen Thin Crust 14\"", "Case", "Walk-in Section", 1.0, 0.0],
    [1105, "Garlic Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1102, "Spicy Garlic Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1114, "Ranch Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1213, "Cheese Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1119, "Blue Cheese Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1251, "Sliced American Cheese", "Bag", "Walk-in Section", 4.0, 0.33],
    [1111, "7\" Sandwich Roll", "Bag", "Walk-in Section", 4.0, 1.0],
    [1331, "STRING CHEESE 20 LB", "Bag", "Walk-in Section", 1.0, 0.25], 
    [1104, "Jug Garlic Sauce", "Bottle", "Walk-in Section", 10.0, 0.0],
    [1057, "20lb PIZZA CHEESE", "Each", "Walk-in Section", 1.0, 0.0],
    [1152, "Sauce, Pizza Ranch", "Bag", "Walk-in Section", 12.0, 1.0],
    [1040, "Pepperoni", "Bag", "Walk-in Section", 2.0, 1.0],

    # --- PREP RACK ---
    [1002, "Ranch", "Pouch", "Prep Rack", 8.0, 1.0],
    [1218, "Alfredo", "Pouch", "Prep Rack", 3.0, 1.0],
    [1148, "BBQ Sauce", "Bag", "Prep Rack", 8.0, 1.0],
    [1052, "Spinach", "Bag", "Prep Rack", 4.0, 1.0],
    [1051, "Mushrooms", "Pail", "Prep Rack", 2.0, 0.5],
    [1066, "Italian Sausage", "Bag", "Prep Rack", 4.0, 0.5],
    [1065, "Sausage", "Bag", "Prep Rack", 4.0, 0.5],
    [1064, "Beef", "Bag", "Prep Rack", 2.0, 0.5],
    [1178, "Philly Steak", "Bag", "Prep Rack", 4.0, 0.5],
    [1167, "Canadian Bacon", "Bag", "Prep Rack", 2.0, 1.0],
    [1049, "Bacon", "Bag", "Prep Rack", 4.0, 1.0],
    [1241, "Pepperoncini", "Bag", "Prep Rack", 6.0, 1.0],
    [1031, "Black Olives", "Pouch", "Prep Rack", 6.0, 1.0],
    [1047, "Pineapple", "Pouch", "Prep Rack", 6.0, 0.5],
    [1095, "Chicken", "Bag", "Prep Rack", 2.0, 0.5],
    [1159, "2 Cheese", "Bag", "Prep Rack", 2.0, 0.33],
    [1019, "Tomato", "Tray", "Prep Rack", 2.0, 0.5],
    [1016, "Green Pepper", "Bag", "Prep Rack", 4.0, 0.5],
    [1017, "Onion", "Bag", "Prep Rack", 4.0, 0.5],
    [1209, "Banana Pepper", "Bag", "Prep Rack", 8.0, 0.25],
    [1210, "Jalapeno", "Bag", "Prep Rack", 8.0, 0.25],
    [1150, "Garlic Parm", "Pouch", "Prep Rack", 12.0, 0.5],
    [1135, "Buffalo Sauce", "Pouch", "Prep Rack", 8.0, 1.0],
    [1140, "Honey Chipotle", "Pouch", "Prep Rack", 10.0, 1.0],
    [1104, "Garlic Sauce Jug", "Bottle", "Prep Rack", 10.0, 1.0],
    [1152, "Pizza Ranch", "Bag", "Prep Rack", 12.0, 0.5],
    [1092, "Roasted Wings", "Bag", "Prep Rack", 4.0, 1.0],
    [1093, "Boneless Wings", "Bag", "Prep Rack", 2.0, 1.0],
    [1040, "Pepperoni", "Bag", "Prep Rack", 2.0, 0.25],

    # --- MAKELINE TOP ---
    [1331, "String Cheese", "Bag", "Makeline Section (Top)", 1.0, 0.25],
    [1066, "Italian Sausage", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1178, "Philly Cheesesteak", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1065, "Sausage", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1064, "Beef", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1049, "Bacon", "Bag", "Makeline Section (Top)", 4.0, 1.0],
    [1167, "Canadian Bacon", "Bag", "Makeline Section (Top)", 2.0, 1.0],
    [1051, "Mushrooms-fresh", "Pail", "Makeline Section (Top)", 2.0, 0.5],
    [1017, "Onions, Sliced", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1016, "Green Peppers, Sliced", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1095, "Grilled Chicken", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1019, "Tomatoes, Diced Roma", "Tray", "Makeline Section (Top)", 2.0, 0.5],
    [1031, "Black Olives", "Pouch", "Makeline Section (Top)", 6.0, 1.0],
    [1047, "PINEAPPLE - POUCH", "Pouch", "Makeline Section (Top)", 6.0, 0.5],
    [1040, "Pepperoni", "Bag", "Makeline Section (Top)", 2.0, 0.25],
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Top)", 1.0, 1.0],
    [1159, "Two Cheese P/R", "Bag", "Makeline Section (Top)", 2.0, 0.33],
    [1257, "Three Cheese Blend", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1210, "Jalapeno Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],
    [1209, "Banana Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],

    # --- MAKELINE BOTTOM ---
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Bottom)", 1.0, 1.0],
    [1218, "Alfredo Sauce", "Pouch", "Makeline Section (Bottom)", 3.0, 1.0],
    [1002, "Bulk Ranch Sauce", "Pouch", "Makeline Section (Bottom)", 8.0, 1.0],
    [1251, "Sliced American Cheese", "Bag", "Makeline Section (Bottom)", 4.0, 0.33],
    [1052, "Fresh Spinach", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1331, "String Cheese", "Bag", "Makeline Section (Bottom)", 1.0, 0.25],
    [1152, "Pizza Ranch (Bottle)", "Bottle", "Makeline Section (Bottom)", 12.0, 0.5],
    [1150, "Garlic Truffle (Bottle)", "Bottle", "Makeline Section (Bottom)", 12.0, 0.5],
    [1085, "Parbaked Pan Crust", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1111, "7\" Sandwich Roll", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1092, "Roasted Wings", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1093, "Boneless Wings", "Bag", "Makeline Section (Bottom)", 2.0, 1.0],
    [1114, "Ranch Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 1.0],
    [1119, "Blue Cheese Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 1.0],
    [1105, "Garlic Sauce Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 1.0],
    [1102, "Spicy Garlic Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 1.0],
    [1213, "Cheese Sauce Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 1.0],
    [1040, "Pepperoni (Lexan)", "Bag", "Makeline Section (Bottom)", 2.0, 0.25],

    # --- CUT TABLE ---
    [2146, "Sandwich Box (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
    [2047, "CHICKEN BOX (Individual)", "Each", "Cut Table Section", 1.0, 1.0], 
    [2043, "Pizza Box 8 (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
    [2005, "Pizza Box 10 (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
    [2007, "Pizza Box 12 (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
    [2010, "Pizza Box 14 (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
    [2025, "Pizza Box 16 In (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
    [2071, "Garlic Knot Tray", "Each", "Cut Table Section", 1.0, 1.0],
    [2065, "Tray, Garlic Breadstick", "Each", "Cut Table Section", 1.0, 1.0],
    [1118, "BBQ Sauce Cups (Individual)", "Unit", "Cut Table Section", 1.0, 1.0],
    [1117, "Buffalo Sauce Cups (Individual)", "Unit", "Cut Table Section", 1.0, 1.0],
    [1105, "Garlic Sauce Cups (Individual)", "Unit", "Cut Table Section", 1.0, 1.0],
    [2307, "Corrugated Pizza Sleeve", "Unit", "Cut Table Section", 1.0, 1.0],
    [1241, "Pepperoncini Peppers", "Bag", "Cut Table Section", 6.0, 1.0],
    [1222, "Season Pkt", "Case", "Cut Table Section", 1.0, 0.0],
    [1135, "Buffalo Sauce (Bottle)", "Bottle", "Cut Table Section", 8.0, 1.0],
    [1148, "BBQ Bulk (Bottle)", "Bottle", "Cut Table Section", 8.0, 1.0],
    [1140, "Honey Chptl (Bottle)", "Bottle", "Cut Table Section", 10.0, 1.0],
    [1150, "Garlic Parm (Bottle)", "Bottle", "Cut Table Section", 12.0, 0.5],

    # --- SODA BACK OF STORE ---
    [6200, "2L Pepsi", "Each", "Soda back of store", 1.0, 0.0],
    [6202, "2L Pepsi Zero", "Each", "Soda back of store", 1.0, 0.0],
    [6661, "2L Starry", "Each", "Soda back of store", 1.0, 0.0],
    [6203, "2L Mountain Dew", "Each", "Soda back of store", 1.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Soda back of store", 1.0, 0.0],
    [6000, "20oz Pepsi", "Each", "Soda back of store", 1.0, 0.0],
    [6002, "20oz Pepsi Zero", "Each", "Soda back of store", 1.0, 0.0],
    [6660, "20oz Starry", "Each", "Soda back of store", 1.0, 0.0],
    [6006, "20oz Aquafina", "Each", "Soda back of store", 1.0, 0.0],

    # --- DRY GOODS RACK 1 (BACKUPS) ---
    [3007, "Cup 20oz Cold", "Case", "Dry Goods (Rack 1)", 20.0, 0.0],
    [1135, "Buffalo Sauce (Pouch)", "Pouch", "Dry Goods (Rack 1)", 8.0, 1.0],
    [1140, "Honey Chipotle (Pouch)", "Pouch", "Dry Goods (Rack 1)", 10.0, 1.0],
    [1150, "Garlic Parm Truffle (Pouch)", "Pouch", "Dry Goods (Rack 1)", 12.0, 0.5],
    [1148, "BBQ Sauce (Bag)", "Bag", "Dry Goods (Rack 1)", 8.0, 1.0],
    [1241, "Pepperoncinis (Case/Bag)", "Bag", "Dry Goods (Rack 1)", 6.0, 1.0],
    [1031, "Black Olives (Pouch)", "Pouch", "Dry Goods (Rack 1)", 6.0, 1.0],
    [1209, "Banana Peppers (Bag)", "Bag", "Dry Goods (Rack 1)", 8.0, 0.25],
    [1191, "Italian Seasoning (Bag)", "Bag", "Dry Goods (Rack 1)", 1.0, 0.0],
    [1210, "Jalapeno Peppers (Bag)", "Bag", "Dry Goods (Rack 1)", 8.0, 0.25],
    [1047, "Pineapple Tidbits (Pouch)", "Pouch", "Dry Goods (Rack 1)", 6.0, 0.5],

    # --- DRY GOODS RACK 2 (PIZZA SAUCE) ---
    [1005, "PIZZA SAUCE(POUCH)", "Pouch", "Dry Goods (Rack 2 - Pizza Sauce)", 6.0, 3.0],

    # --- DRY GOODS RACK 3 (SMALLWARES) ---
    [1118, "BBQ Sauce Cup", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [1117, "Buffalo Sauce Cup", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [2065, "Breadstick Tray", "Each", "Dry Goods (Rack 3)", 150.0, 0.0],
    [2071, "Garlic Knot Tray", "Each", "Dry Goods (Rack 3)", 125.0, 0.0],
    [2307, "Pizza Inserts (12/12)", "Case", "Dry Goods (Rack 3)", 100.0, 0.0],
    [3050, "Bleached GVP Bag", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3055, "Liner Bags (9 / 1.5x1.5)", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3042, "Baking Sheets (10/10)", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3040, "Baking Sheets (14/14)", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [2039, "Handy Foil (500 sheets)", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3060, "Paper Plates", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3012, "Souffle Cups (2oz)", "Case", "Dry Goods (Rack 3)", 40.0, 0.0],
    [2305, "Forks", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [2047, "Wing Clamshell (240/cs)", "Each", "Dry Goods (Rack 3)", 240.0, 0.0],
    [3065, "Papa John Logo Napkins", "Case", "Dry Goods (Rack 3)", 32.0, 0.0],
    
    [2031, "Blaster Labels", "Roll", "Storage by office desk", 16.0, 0.0]
]

df = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult'])

# --- 4. THE UI RENDER ENGINE ---
def clean_input(label, key, step=1.0):
    try:
        val = st.number_input(label, min_value=0.0, step=step, value=None, placeholder="", key=key)
        return val if val is not None else 0.0
    except Exception:
        return 0.0

st.title("Inventory Count Engine v2.6")
st.caption("🚀 Fully Synced Store Logic | Store 04185")

progress_bar = st.progress(0.0, text="🔥 Inventory Completion: 0%")
st.markdown("<br>", unsafe_allow_html=True) 

inventory_totals = []
sections = [
    "Walk-in Section", "Prep Rack", "Makeline Section (Top)", "Makeline Section (Bottom)",
    "Cut Table Section", "Soda back of store", "Dry Goods (Rack 1)", 
    "Dry Goods (Rack 2 - Pizza Sauce)", "Dry Goods (Rack 3)", "Storage by office desk"
]

for section in sections:
    section_data = df[df['Section'] == section]
    if not section_data.empty:
        with st.expander(f"📁 {section}", expanded=False):
            for index, row in section_data.iterrows():
                item_desc = f"{row['Item_Num']} - {row['Description']}"
                unit = row['Unit']
                case_mult = row['Case_Mult']
                lexan_mult = row['Lexan_Mult']
                
                with st.container(border=True):
                    st.markdown(f"**{item_desc}**")
                    
                    # 1. WALK-IN LOGIC (Pepperoni/Anchovy/Ranch rules)
                    if section == "Walk-in Section":
                        if "Pepperoni" in row['Description']:
                            cases = clean_input("Cases", key=f"c_{index}_{section}", step=0.5)
                            total = cases * case_mult
                        elif "Anchovies" in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: cans = clean_input("Individual Cans", key=f"i_{index}_{section}")
                            total = cases + (cans / 25.0)
                        elif "Bulk Ranch" in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: pouches = clean_input("Pouches", key=f"p_{index}_{section}")
                            total = (cases * case_mult) + pouches
                        elif lexan_mult == 1.0 and "Ranch Sauce" not in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: bags = clean_input("Loose Bags/Pouches", key=f"b_{index}_{section}")
                            total = (cases * case_mult) + bags
                        elif "Crust" in row['Description'] and "Pan" not in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: sleeves = clean_input("Sleeves", key=f"s_{index}_{section}")
                            total = cases + (sleeves * 0.25)
                        elif "Pan Pizza" in row['Description'] or "Alfredo" in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: loose = clean_input("Loose Bags/Pouches", key=f"l_{index}_{section}")
                            total = (cases * case_mult) + loose
                        elif "Cups" in row['Description'] and "Case" in row['Unit']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: inds = clean_input("Individual Units", key=f"i_{index}_{section}")
                            total = cases + (inds / row['Case_Mult']) if row['Case_Mult'] > 1 else cases + inds
                        elif "Sandwich Roll" in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Case", key=f"c_{index}_{section}")
                            with col2: lexans = clean_input("Lexans", key=f"l_{index}_{section}")
                            total = (cases * case_mult) + lexans
                        elif "STRING CHEESE" in row['Description']:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Case", key=f"c_{index}_{section}")
                            with col2: lexans = clean_input("Lexans", key=f"l_{index}_{section}", step=0.25)
                            total = (cases * case_mult) + (lexans * lexan_mult)
                        elif "Jug Garlic" in row['Description']:
                            total = clean_input("Jugs", key=f"j_{index}_{section}")
                        elif lexan_mult == 0.0 and case_mult > 1.0:
                            total = clean_input("Cases", key=f"c_{index}_{section}") * case_mult
                        else:
                            total = clean_input(f"Total Count ({unit})", key=f"t_{index}_{section}")

                    # 2. MAKELINE TOP: Lexan Only
                    elif section == "Makeline Section (Top)":
                        lexans = clean_input("Lexan Count", key=f"l_{index}_{section}", step=0.25)
                        total = lexans * lexan_mult

                    # 3. MAKELINE BOTTOM: Single Tab
                    elif section == "Makeline Section (Bottom)":
                        if "Cup" in row['Description']:
                            label, step_val, is_unit = "Individual Unit Count", 1.0, True
                        elif "Bottle" in row['Description']:
                            label, step_val, is_unit = "Total Bottles", 0.5, False
                        elif "Pan Crust" in row['Description'] or "PIZZA CHEESE" in row['Description']:
                            label, step_val, is_unit = "Total Bags (Each)", 1.0, True
                        else:
                            label, step_val, is_unit = "Lexan Count", 0.25, False
                        count_val = clean_input(label, key=f"b_{index}_{section}", step=step_val)
                        total = count_val if is_unit else (count_val * lexan_mult)

                    # 4. CUT TABLE: Individual & Bottle
                    elif section == "Cut Table Section":
                        if any(x in row['Description'] for x in ["Box", "Tray", "Cup", "Sleeve"]):
                            label, step_val, is_unit = "Individual Count", 1.0, True
                        elif "Bottle" in row['Description']:
                            label, step_val, is_unit = "Bottle Count", 0.5, False
                        elif "Pepperoncini" in row['Description']:
                            label, step_val, is_unit = "Lexan Count", 0.25, False
                        else:
                            label, step_val, is_unit = f"Total ({row['Unit']})", 1.0, True
                        count_val = clean_input(label, key=f"ct_{index}_{section}", step=step_val)
                        total = count_val if is_unit else (count_val * lexan_mult)

                    # 5. SODA & RACK 1: Dual/Single Logic Sync
                    elif section == "Soda back of store":
                        total = clean_input("Bottle Count (Each)", key=f"s_{index}_{section}")
                    
                    elif section == "Dry Goods (Rack 1)":
                        if lexan_mult > 0:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Cases", key=f"c_{index}_{section}")
                            with col2: loose = clean_input("Bags/Pouches", key=f"b_{index}_{section}")
                            total = (cases * case_mult) + loose
                        else:
                            total = clean_input("Total Cases", key=f"c_{index}_{section}") * case_mult

                    # 6. RACK 3 & OTHERS (Standard Logic)
                    else:
                        if case_mult > 1:
                            col1, col2 = st.columns(2)
                            with col1: cases = clean_input("Bulk/Case", key=f"c_{index}_{section}")
                            with col2: mid = clean_input(f"Loose {unit}s", key=f"m_{index}_{section}")
                            total = (cases * case_mult) + mid
                        else:
                            total = clean_input(f"Total Count ({unit})", key=f"t_{index}_{section}")

                    inventory_totals.append({
                        "Item #": row['Item_Num'],
                        "Description": row['Description'],
                        "Total Count": round(total, 2)
                    })

# --- OUTPUT LAYER ---
total_tasks = len(inventory_totals)
completed_tasks = sum(1 for item in inventory_totals if item["Total Count"] > 0)
if total_tasks > 0:
    progress_bar.progress(completed_tasks / total_tasks, text=f"🔥 Inventory Completion: {int((completed_tasks/total_tasks)*100)}%")

st.markdown("---")
if st.button("Generate Final Count Values", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    consolidated_df = final_df.groupby(['Item #', 'Description'], as_index=False)['Total Count'].sum()
    st.dataframe(consolidated_df.sort_values(by="Item #"), use_container_width=True, hide_index=True, height=600)
    st.success("Sorted by Item # for Corporate Upload.")

components.html("""<script>
    const inputs = window.parent.document.querySelectorAll('input[type=number]');
    inputs.forEach(input => { input.setAttribute('inputmode', 'decimal'); input.setAttribute('pattern', '[0-9]*'); });
    </script>""", height=0, width=0)
