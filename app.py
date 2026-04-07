import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import json
import os

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(
    page_title="Juskvi Engine v4.0", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 {color: #00583E !important; font-family: 'Helvetica Neue', sans-serif;}
    
    div[data-testid="stExpander"] {
        border: 2px solid #00583E !important; 
        border-radius: 12px; 
        margin-bottom: 15px; 
    }
    div[data-testid="stExpander"] summary {
        background-color: #00583E !important; 
        border-radius: 10px; 
        padding: 15px !important;
    }
    div[data-testid="stExpander"] summary p {
        color: white !important;
        font-size: 1.2rem !important; 
        font-weight: bold !important;
    }
    
    input[type="number"] {
        text-align: center !important; 
        font-size: 1.4rem !important; 
        font-weight: bold !important; 
    }

    .stButton>button {
        background-color: #DF1934 !important; 
        color: white !important; 
        border-radius: 10px; 
        font-weight: bold; 
        font-size: 1.1rem !important; 
        padding: 15px !important; 
        width: 100%; 
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button[kind="secondary"] {
        background-color: #6c757d !important;
        color: white !important;
        border: none !important;
        height: 50px !important;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MULTIPLAYER DATABASE LOGIC ---
DB_FILE = 'live_inventory.json'

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

if 'db' not in st.session_state:
    st.session_state.db = load_db()

def update_val(key):
    # Triggers on every keystroke to save globally
    st.session_state.db[key] = st.session_state[key]
    save_db(st.session_state.db)

# --- 3. SECURITY & STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

ordered_sections = [
    "Soda back of store", "Dry Goods (Rack 1)", "Dry Goods (Rack 2)", "Dry Goods (Rack 3)",
    "Boxes", "Cut Table Section", "Walk-in Section", "Prep Rack", "Makeline Section (Top)", 
    "Makeline Section (Bottom)", "Dough Station", "Front of store soda", "Storage by office desk"
]

if 'folder_versions' not in st.session_state:
    st.session_state['folder_versions'] = {sec: 0 for sec in ordered_sections}

if not st.session_state['logged_in']:
    st.title("Papa John's Inventory System")
    st.caption("Store 04185 | Authorized Personnel Only")
    st.divider()
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("SECURE LOGIN"):
        if username == "MGR" and password == "Papa4185":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Access Denied: Invalid Credentials")
    st.stop()

# --- 4. THE MASTER DATA DICTIONARY ---
master_inventory = [
    # 1. SODA BACK OF STORE
    [6200, "2L Pepsi", "Each", "Soda back of store", 1.0, 0.0],
    [6202, "2L Pepsi Zero", "Each", "Soda back of store", 1.0, 0.0],
    [6661, "2L Starry", "Each", "Soda back of store", 1.0, 0.0],
    [6203, "2L Mountain Dew", "Each", "Soda back of store", 1.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Soda back of store", 1.0, 0.0],
    [6000, "20oz Pepsi", "Each", "Soda back of store", 1.0, 0.0],
    [6002, "20oz Pepsi Zero", "Each", "Soda back of store", 1.0, 0.0],
    [6660, "20oz Starry", "Each", "Soda back of store", 1.0, 0.0],
    [6006, "20oz Aquafina", "Each", "Soda back of store", 1.0, 0.0],

    # 2. RACK 1
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

    # 3. RACK 2
    [1005, "PIZZA SAUCE(POUCH)", "Pouch", "Dry Goods (Rack 2)", 6.0, 3.0],

    # 4. RACK 3
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

    # 5. BOXES
    [2146, "Sandwich Box", "Each", "Boxes", 1.0, 1.0],
    [2043, "8 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2005, "10 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2007, "12 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2010, "14 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2025, "16 inch Box", "Each", "Boxes", 1.0, 1.0],

    # 6. CUT TABLE
    [2047, "CHICKEN BOX (Individual)", "Each", "Cut Table Section", 1.0, 1.0],
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

    # 7. WALK-IN SECTION
    [1085, "Crust, Parbaked Pan Pizza", "Bag", "Walk-in Section", 4.0, 0.0],
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

    # 8. PREP RACK (UPDATED TO PURE LEXAN/BOTTLE)
    [1002, "Ranch (Lexan)", "Lexan", "Prep Rack", 8.0, 1.0],
    [1218, "Alfredo (Lexan)", "Lexan", "Prep Rack", 3.0, 1.0],
    [1148, "BBQ Sauce (Lexan)", "Lexan", "Prep Rack", 8.0, 1.0],
    [1052, "Spinach (Lexan)", "Lexan", "Prep Rack", 4.0, 1.0],
    [1051, "Mushrooms (Lexan)", "Lexan", "Prep Rack", 2.0, 0.5],
    [1066, "Italian Sausage (Lexan)", "Lexan", "Prep Rack", 4.0, 0.5],
    [1065, "Sausage (Lexan)", "Lexan", "Prep Rack", 4.0, 0.5],
    [1064, "Beef (Lexan)", "Lexan", "Prep Rack", 2.0, 0.5],
    [1178, "Philly Steak (Lexan)", "Lexan", "Prep Rack", 4.0, 0.5],
    [1167, "Canadian Bacon (Lexan)", "Lexan", "Prep Rack", 2.0, 1.0],
    [1049, "Bacon (Lexan)", "Lexan", "Prep Rack", 4.0, 1.0],
    [1241, "Pepperoncini (Lexan)", "Lexan", "Prep Rack", 6.0, 1.0],
    [1031, "Black Olives (Lexan)", "Lexan", "Prep Rack", 6.0, 1.0],
    [1047, "Pineapple (Lexan)", "Lexan", "Prep Rack", 6.0, 0.5],
    [1095, "Chicken (Lexan)", "Lexan", "Prep Rack", 2.0, 0.5],
    [1159, "2 Cheese (Lexan)", "Lexan", "Prep Rack", 2.0, 0.33],
    [1257, "Three Cheese (Lexan)", "Lexan", "Prep Rack", 2.0, 0.5],
    [1019, "Tomato (Lexan)", "Lexan", "Prep Rack", 2.0, 0.5],
    [1016, "Green Pepper (Lexan)", "Lexan", "Prep Rack", 4.0, 0.5],
    [1017, "Onion (Lexan)", "Lexan", "Prep Rack", 4.0, 0.5],
    [1209, "Banana Pepper (Lexan)", "Lexan", "Prep Rack", 8.0, 0.25],
    [1210, "Jalapeno (Lexan)", "Lexan", "Prep Rack", 8.0, 0.25],
    [1150, "Garlic Parm (Bottle)", "Bottle", "Prep Rack", 12.0, 0.5],
    [1135, "Buffalo Sauce (Bottle)", "Bottle", "Prep Rack", 8.0, 1.0],
    [1140, "Honey Chipotle (Bottle)", "Bottle", "Prep Rack", 10.0, 1.0],
    [1104, "Garlic Sauce Jug (Bottle)", "Bottle", "Prep Rack", 10.0, 1.0],
    [1152, "Pizza Ranch (Bottle)", "Bottle", "Prep Rack", 12.0, 0.5],
    [1092, "Roasted Wings (Lexan)", "Lexan", "Prep Rack", 4.0, 1.0],
    [1093, "Boneless Wings (Lexan)", "Lexan", "Prep Rack", 2.0, 1.0],
    [1040, "Pepperoni (Lexan)", "Lexan", "Prep Rack", 2.0, 0.25],

    # 9. MAKELINE TOP
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

    # 10. MAKELINE BOTTOM
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

    # 11. DOUGH STATION
    [1075, "Dough Tray 10", "Tray", "Dough Station", 1.0, 0.0],
    [1076, "DOUGH M, 12 INCH", "Tray", "Dough Station", 1.0, 0.0],
    [1080, "Dough Tray 14", "Tray", "Dough Station", 1.0, 0.0],
    [1082, "Dustinator", "Lexan", "Dough Station", 1.0, 1.0],
    [1148, "Barbecue Sauce (Lexan)", "Bag", "Dough Station", 8.0, 1.0],
    [1005, "Pizza Sauce (Pouch)", "Pouch", "Dough Station", 6.0, 3.0],
    [1104, "Garlic Sauce Jug", "Bottle", "Dough Station", 10.0, 0.0],
    [1150, "Garlic Parmesean (Bottle)", "Bottle", "Dough Station", 12.0, 0.5],

    # 12. FRONT OF STORE SODA
    [6000, "20oz Pepsi", "Unit", "Front of store soda", 1.0, 1.0],
    [6003, "20oz Mountain Dew", "Unit", "Front of store soda", 1.0, 1.0],
    [6660, "20oz Starry", "Unit", "Front of store soda", 1.0, 1.0],
    [6002, "20oz Pepsi Zero", "Unit", "Front of store soda", 1.0, 1.0],
    [6200, "2L Pepsi", "Unit", "Front of store soda", 1.0, 1.0],
    [6203, "2L Mountain Dew", "Unit", "Front of store soda", 1.0, 1.0],
    [6661, "2L Starry", "Unit", "Front of store soda", 1.0, 1.0],
    [6202, "2L Pepsi Zero", "Unit", "Front of store soda", 1.0, 1.0],

    # OFFICE
    [2031, "Blaster Labels", "Roll", "Storage by office desk", 16.0, 0.0]
]

df = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult'])

# --- 5. THE UI RENDER ENGINE (DATABASE ENABLED) ---
def clean_input(label, key, step=1.0):
    # Reads from DB initially. Triggers update_val on change.
    existing_val = st.session_state.db.get(key, None)
    val = st.number_input(label, min_value=0.0, step=step, value=existing_val, key=key, on_change=update_val, args=(key,))
    return val if val is not None else 0.0

st.title("Inventory Count Engine v4.0")
st.caption("🚀 MULTIPLAYER ACTIVE | Live Sync Enabled")

progress_bar = st.progress(0.0, text="🔥 Inventory Completion: 0%")
st.markdown("<br>", unsafe_allow_html=True) 

inventory_totals = []

for section in ordered_sections:
    section_data = df[df['Section'] == section]
    if not section_data.empty:
        folder_key = f"exp_{section}_{st.session_state.folder_versions[section]}"
        
        with st.expander(f"📁 {section}", expanded=False, key=folder_key):
            for index, row in section_data.iterrows():
                item_desc = f"{row['Item_Num']} - {row['Description']}"
                unit, case_mult, lexan_mult = row['Unit'], row['Case_Mult'], row['Lexan_Mult']
                
                with st.container(border=True):
                    st.markdown(f"**{item_desc}**")
                    
                    if section == "Walk-in Section":
                        if "Pepperoni" in row['Description']:
                            total = clean_input("Cases", key=f"c_{index}_{section}", step=0.5) * case_mult
                        elif "Anchovies" in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: cn = clean_input("Cans", key=f"i_{index}_{section}")
                            total = cs + (cn / 25.0)
                        elif "Bulk Ranch" in row['Description'] or "Alfredo" in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: ps = clean_input("Pouches", key=f"p_{index}_{section}")
                            total = (cs * case_mult) + ps
                        elif lexan_mult == 1.0:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: bs = clean_input("Loose Bags", key=f"b_{index}_{section}")
                            total = (cs * case_mult) + bs
                        elif "Crust" in row['Description'] and "Pan" not in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: sl = clean_input("Sleeves", key=f"s_{index}_{section}")
                            total = cs + (sl * 0.25)
                        elif "Cups" in row['Description'] and "Case" in row['Unit']:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: ind = clean_input("Units", key=f"i_{index}_{section}")
                            total = cs + (ind / row['Case_Mult'])
                        elif "Roll" in row['Description'] or "String" in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Case", key=f"c_{index}_{section}")
                            with c2: lx = clean_input("Lexan", key=f"l_{index}_{section}", step=0.25)
                            total = (cs * case_mult) + (lx * (lexan_mult if lexan_mult > 0 else 1.0))
                        else:
                            total = clean_input(f"Total {unit}", key=f"t_{index}_{section}")
                    
                    elif section == "Prep Rack":
                        lbl = "Bottle Count" if "Bottle" in row['Description'] else "Lexan Count"
                        step_val = 0.5 if "Bottle" in row['Description'] else 0.25
                        total = clean_input(lbl, key=f"pr_{index}_{section}", step=step_val) * lexan_mult

                    elif section == "Makeline Section (Top)":
                        total = clean_input("Lexan Count", key=f"l_{index}_{section}", step=0.25) * lexan_mult
                    
                    elif section == "Makeline Section (Bottom)":
                        if "Cup" in row['Description']: total = clean_input("Individual Count", key=f"i_{index}_{section}")
                        elif "Bottle" in row['Description']: total = clean_input("Bottle Count", key=f"b_{index}_{section}", step=0.5) * lexan_mult
                        elif "Pan Crust" in row['Description'] or "PIZZA CHEESE" in row['Description']: total = clean_input("Total Bags", key=f"tb_{index}_{section}")
                        else: total = clean_input("Lexan Count", key=f"l_{index}_{section}", step=0.25) * lexan_mult

                    elif section == "Cut Table Section" or section == "Boxes":
                        if any(x in row['Description'] for x in ["Box", "Tray", "Cup", "Sleeve"]): total = clean_input("Individual Units", key=f"i_{index}_{section}")
                        elif "Bottle" in row['Description']: total = clean_input("Bottle Count", key=f"b_{index}_{section}", step=0.5) * lexan_mult
                        elif "Pepperoncini" in row['Description']: total = clean_input("Lexan Count", key=f"l_{index}_{section}", step=0.25)
                        else: total = clean_input(f"Total {unit}", key=f"t_{index}_{section}")
                    
                    elif section == "Dough Station":
                        if "Tray" in row['Description']: 
                            total = clean_input("Total Trays", key=f"t_{index}_{section}")
                        elif "Dustinator" in row['Description'] or "Lexan" in row['Description']: 
                            total = clean_input("Lexan Count", key=f"l_{index}_{section}", step=0.25) * (lexan_mult if lexan_mult > 0 else 1.0)
                        elif "Pouch" in row['Description']: 
                            total = clean_input("Pouches", key=f"p_{index}_{section}")
                        elif "Jug" in row['Description']: 
                            total = clean_input("Jugs", key=f"j_{index}_{section}")
                        elif "Bottle" in row['Description']: 
                            total = clean_input("Bottle Count", key=f"b_{index}_{section}", step=0.5) * lexan_mult
                        else: 
                            total = clean_input(f"Total {unit}", key=f"tot_{index}_{section}")

                    elif "soda" in section.lower():
                        total = clean_input(f"Individual {unit}", key=f"s_{index}_{section}")

                    elif section == "Dry Goods (Rack 1)":
                        if lexan_mult > 0:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: bg = clean_input("Loose Bags/Pouches", key=f"b_{index}_{section}")
                            total = (cs * case_mult) + bg
                        else: total = clean_input("Cases", key=f"c_{index}_{section}") * case_mult

                    else:
                        if case_mult > 1:
                            c1, c2 = st.columns(2)
                            with c1: cs = clean_input("Cases", key=f"c_{index}_{section}")
                            with c2: mid = clean_input(f"Loose {unit}s", key=f"m_{index}_{section}")
                            total = (cs * case_mult) + mid
                        else: total = clean_input("Count", key=f"t_{index}_{section}")

                    inventory_totals.append({"Item #": row['Item_Num'], "Description": row['Description'], "Total Count": round(total, 2)})
            
            if st.button(f"✅ FINISH & COLLAPSE {section}", key=f"btn_close_{section}", type="secondary", use_container_width=True):
                st.session_state.folder_versions[section] += 1
                st.rerun()

# --- 6. OUTPUT & RESET LAYER ---
total_tasks = len(inventory_totals)
completed_tasks = sum(1 for item in inventory_totals if item["Total Count"] > 0)
if total_tasks > 0:
    progress_bar.progress(completed_tasks / total_tasks, text=f"🔥 Inventory Completion: {int((completed_tasks/total_tasks)*100)}%")

st.divider()
if st.button("GENERATE FINAL CORPORATE VALUES", type="primary"):
    final_df = pd.DataFrame(inventory_totals).groupby(['Item #', 'Description'], as_index=False)['Total Count'].sum()
    st.dataframe(final_df.sort_values(by="Item #"), use_container_width=True, hide_index=True, height=600)
    st.success("Sorted by Item #. Ready for Corporate data entry.")

st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🚨 WIPE DATA FOR NEW SHIFT", type="secondary"):
    save_db({})
    st.session_state.db = {}
    st.rerun()

components.html("""<script>
    const inputs = window.parent.document.querySelectorAll('input[type=number]');
    inputs.forEach(input => { input.setAttribute('inputmode', 'decimal'); input.setAttribute('pattern', '[0-9]*'); });
    </script>""", height=0, width=0)
