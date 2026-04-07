import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(
    page_title="Juskvi Inventory Engine v3.2", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 {color: #00583E !important; font-family: 'Helvetica Neue', sans-serif;}
    
    /* Expander Styling - The Green Folder Accordion */
    div[data-testid="stExpander"] {
        border: 2px solid #00583E !important; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        background-color: #ffffff;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    div[data-testid="stExpander"] summary {
        background-color: #00583E !important; 
        color: white !important; 
        border-radius: 10px; 
        padding: 18px !important;
    }
    div[data-testid="stExpander"] summary p {
        color: white !important;
        font-size: 1.3rem !important; 
        font-weight: bold !important;
    }
    
    /* Input Box Formatting */
    input[type="number"] {
        text-align: center !important; 
        font-size: 1.5rem !important; 
        font-weight: bold !important; 
        color: #00583E !important;
        background-color: #f0f2f6 !important;
        border-radius: 10px !important;
    }

    /* Primary Red Buttons */
    .stButton>button {
        background-color: #DF1934 !important; 
        color: white !important; 
        border-radius: 10px; 
        font-weight: bold; 
        font-size: 1.2rem !important; 
        padding: 20px !important; 
        width: 100%; 
        border: none;
        text-transform: uppercase;
    }
    
    /* Collapse Button Logic */
    div.stButton > button[kind="secondary"] {
        background-color: #4a4a4a !important;
        color: white !important;
        border: 2px solid #333 !important;
        height: 60px !important;
        font-size: 1.1rem !important;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SECURITY & ACCORDION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Mapping specific folder versions to force-close them on button click
if 'v' not in st.session_state:
    st.session_state['v'] = {
        "Soda back of store": 0, "Dry Goods (Rack 1)": 0, "Dry Goods (Rack 2)": 0, 
        "Dry Goods (Rack 3)": 0, "Boxes": 0, "Cut Table Section": 0, 
        "Walk-in Section": 0, "Prep Rack": 0, "Makeline Section (Top)": 0, 
        "Makeline Section (Bottom)": 0, "Dough Station": 0, "Front of store soda": 0
    }

if not st.session_state['logged_in']:
    st.title("Papa John's Inventory System")
    st.caption("Store 04185 | Authorized Personnel Only")
    u, p = st.text_input("User ID"), st.text_input("Password", type="password")
    if st.button("SECURE LOGIN"):
        if u == "MGR" and p == "Papa4185":
            st.session_state['logged_in'] = True
            st.rerun()
        else: st.error("Access Denied")
    st.stop()

# --- 3. MASTER DATA DICTIONARY (RE-ORGANIZED FLOW) ---
master_inventory = [
    # 1. BACK OF STORE SODA
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

    # 5. BOXES (NEW TAB)
    [2146, "Sandwich Box", "Each", "Boxes", 1.0, 1.0],
    [2043, "8 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2005, "10 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2007, "12 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2010, "14 inch Box", "Each", "Boxes", 1.0, 1.0],
    [2025, "16 inch Box", "Each", "Boxes", 1.0, 1.0],

    # 6. CUT TABLE (MINUS BOXES)
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

    # 8. PREP RACK
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

    # 12. FRONT OF STORE SODA (ORDERED LIST)
    [6000, "20oz Pepsi", "Unit", "Front of store soda", 1.0, 1.0],
    [6003, "20oz Mountain Dew", "Unit", "Front of store soda", 1.0, 1.0],
    [6660, "20oz Starry", "Unit", "Front of store soda", 1.0, 1.0],
    [6002, "20oz Pepsi Zero", "Unit", "Front of store soda", 1.0, 1.0],
    [6200, "2L Pepsi", "Unit", "Front of store soda", 1.0, 1.0],
    [6203, "2L Mountain Dew", "Unit", "Front of store soda", 1.0, 1.0],
    [6661, "2L Starry", "Unit", "Front of store soda", 1.0, 1.0],
    [6202, "2L Pepsi Zero", "Unit", "Front of store soda", 1.0, 1.0],

    # OFFICE / MISC
    [2031, "Blaster Labels", "Roll", "Storage by office desk", 16.0, 0.0]
]

df = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult'])

# --- 4. THE UI RENDER ENGINE ---
def ci(l, k, s=1.0):
    try:
        val = st.number_input(l, min_value=0.0, step=step, value=None, placeholder="", key=k)
        return val if val is not None else 0.0
    except: return 0.0

st.title("Juskvi Engine v3.2")
st.caption("🚀 Navigation Flow: Soda Back -> Racks -> Boxes -> Floor -> Dough -> Soda Front")

progress_bar = st.progress(0.0, text="Count Progress: 0%")
inventory_totals = []

# List of sections in the specific order requested
ordered_sections = [
    "Soda back of store", "Dry Goods (Rack 1)", "Dry Goods (Rack 2)", "Dry Goods (Rack 3)",
    "Boxes", "Cut Table Section", "Walk-in Section", "Prep Rack", "Makeline Section (Top)", 
    "Makeline Section (Bottom)", "Dough Station", "Front of store soda", "Storage by office desk"
]

for section in ordered_sections:
    section_data = df[df['Section'] == section]
    if not section_data.empty:
        folder_key = f"exp_{section}_{st.session_state.v[section]}"
        
        with st.expander(f"📁 {section}", expanded=False, key=folder_key):
            for index, row in section_data.iterrows():
                item_desc = f"{row['Item_Num']} - {row['Description']}"
                unit, case_mult, lexan_mult = row['Unit'], row['Case_Mult'], row['Lexan_Mult']
                
                with st.container(border=True):
                    st.markdown(f"**{item_desc}**")
                    
                    if section == "Walk-in Section":
                        if "Pepperoni" in row['Description']:
                            total = ci("Cases", f"c_{index}", 0.5) * case_mult
                        elif "Anchovies" in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: cn = ci("Cans", f"i_{index}")
                            total = cs + (cn / 25.0)
                        elif "Bulk Ranch" in row['Description'] or "Alfredo" in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: ps = ci("Pouches", f"p_{index}")
                            total = (cs * case_mult) + ps
                        elif lexan_mult == 1.0:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: bs = ci("Loose Bags", f"b_{index}")
                            total = (cs * case_mult) + bs
                        elif "Crust" in row['Description'] and "Pan" not in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: sl = ci("Sleeves", f"s_{index}")
                            total = cs + (sl * 0.25)
                        elif "Cups" in row['Description'] and "Case" in row['Unit']:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: ind = ci("Units", f"i_{index}")
                            total = cs + (ind / case_mult)
                        elif "Roll" in row['Description'] or "String" in row['Description']:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Case", f"c_{index}")
                            with c2: lx = ci("Lexan", f"l_{index}", 0.25)
                            total = (cs * case_mult) + (lx * (lexan_mult if lexan_mult > 0 else 1.0))
                        else: total = ci(f"Total {unit}", f"t_{index}")
                    
                    elif section == "Makeline Section (Top)":
                        total = ci("Lexan Count", f"l_{index}", 0.25) * lexan_mult
                    
                    elif section == "Makeline Section (Bottom)":
                        if "Cup" in row['Description']: total = ci("Individual Count", f"i_{index}")
                        elif "Bottle" in row['Description']: total = ci("Bottle Count", f"b_{index}", 0.5) * lexan_mult
                        elif "Pan Crust" in row['Description'] or "PIZZA CHEESE" in row['Description']: total = ci("Total Bags", f"tb_{index}")
                        else: total = ci("Lexan Count", f"l_{index}", 0.25) * lexan_mult

                    elif section == "Cut Table Section" or section == "Boxes":
                        if any(x in row['Description'] for x in ["Box", "Tray", "Cup", "Sleeve", "Clamshell"]): total = ci("Individual Units", f"i_{index}")
                        elif "Bottle" in row['Description']: total = ci("Bottle Count", f"b_{index}", 0.5) * lexan_mult
                        elif "Pepperoncini" in row['Description']: total = ci("Lexan Count", f"l_{index}", 0.25)
                        else: total = ci(f"Total {unit}", f"t_{index}")
                    
                    elif "soda" in section.lower():
                        total = ci("Individual Bottles", f"s_{index}")
                    
                    elif section == "Dry Goods (Rack 1)":
                        if lexan_mult > 0:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: bg = ci("Loose Bags/Pouches", f"b_{index}")
                            total = (cs * case_mult) + bg
                        else: total = ci("Cases", f"c_{index}") * case_mult
                    else:
                        if case_mult > 1:
                            c1, c2 = st.columns(2)
                            with c1: cs = ci("Cases", f"c_{index}")
                            with c2: mid = ci(f"Loose {unit}s", f"m_{index}")
                            total = (cs * case_mult) + mid
                        else: total = ci("Count", f"t_{index}")

                    inventory_totals.append({"Item #": row['Item_Num'], "Description": row['Description'], "Total Count": round(total, 2)})
            
            if st.button(f"✅ FINISH & COLLAPSE {section}", key=f"btn_reset_{section}", type="secondary", use_container_width=True):
                st.session_state.v[section] += 1
                st.rerun()

# --- 5. OUTPUT LAYER ---
total_tasks = len(inventory_totals)
completed_tasks = sum(1 for item in inventory_totals if item["Total Count"] > 0)
if total_tasks > 0:
    progress_bar.progress(completed_tasks / total_tasks, text=f"🔥 Count Progress: {int((completed_tasks/total_tasks)*100)}%")

st.divider()
if st.button("GENERATE FINAL CORPORATE VALUES", type="primary"):
    final_df = pd.DataFrame(inventory_totals).groupby(['Item #', 'Description'], as_index=False)['Total Count'].sum()
    st.dataframe(final_df.sort_values(by="Item #"), use_container_width=True, hide_index=True, height=600)
    st.success("Sorted by Item #. Ready for Corporate data entry.")

components.html("""<script>
    const inputs = window.parent.document.querySelectorAll('input[type=number]');
    inputs.forEach(input => { input.setAttribute('inputmode', 'decimal'); input.setAttribute('pattern', '[0-9]*'); });
    </script>""", height=0, width=0)
