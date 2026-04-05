import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(page_title="Juskvi Engine v3.0", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    h1, h2, h3 {color: #00583E !important; font-family: 'Helvetica Neue', sans-serif;}
    
    /* Section Header Button (The Folder Tab) */
    .stButton > button[kind="primary"] {
        background-color: #00583E !important;
        color: white !important;
        border: none !important;
        height: 60px !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-align: left !important;
        padding-left: 20px !important;
        border-radius: 10px !important;
        margin-bottom: 5px !important;
    }

    /* Red Action Buttons */
    .stButton > button[kind="secondary"] {
        background-color: #DF1934 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        box-shadow: 0px 4px 10px rgba(223, 25, 52, 0.3) !important;
    }

    /* Input Numbers */
    input[type="number"] {
        text-align: center !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        color: #00583E !important;
    }
    
    /* Container Background */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 2px solid #eee !important;
        padding: 10px !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. SECURITY & VISIBILITY STATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'open_section' not in st.session_state: st.session_state['open_section'] = None

if not st.session_state['auth']:
    st.title("Store 04185 Inventory")
    u, p = st.text_input("User ID"), st.text_input("Password", type="password")
    if st.button("SECURE LOGIN", kind="secondary"):
        if u == "MGR" and p == "Papa4185":
            st.session_state['auth'] = True
            st.rerun()
    st.stop()

# --- 3. MASTER DATA ---
master_inventory = [
    # WALK-IN
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
    # MAKELINE TOP
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
    # MAKELINE BOTTOM
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
    # CUT TABLE
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
    # SODA & RACKS
    [6200, "2L Pepsi", "Each", "Soda back of store", 1.0, 0.0],
    [6202, "2L Pepsi Zero", "Each", "Soda back of store", 1.0, 0.0],
    [6661, "2L Starry", "Each", "Soda back of store", 1.0, 0.0],
    [6203, "2L Mountain Dew", "Each", "Soda back of store", 1.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Soda back of store", 1.0, 0.0],
    [6000, "20oz Pepsi", "Each", "Soda back of store", 1.0, 0.0],
    [6002, "20oz Pepsi Zero", "Each", "Soda back of store", 1.0, 0.0],
    [6660, "20oz Starry", "Each", "Soda back of store", 1.0, 0.0],
    [6006, "20oz Aquafina", "Each", "Soda back of store", 1.0, 0.0],
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
    [1005, "PIZZA SAUCE(POUCH)", "Pouch", "Dry Goods (Rack 2 - Pizza Sauce)", 6.0, 3.0],
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

df = pd.DataFrame(master_inventory, columns=['ID', 'Desc', 'Unit', 'Sec', 'CM', 'LM'])

# --- 4. THE UI ENGINE ---
def ci(l, k, s=1.0):
    val = st.number_input(l, min_value=0.0, step=s, value=None, placeholder="", key=k)
    return val if val is not None else 0.0

st.title("Juskvi Inventory Engine v3.0")
inventory_totals = []
sections = df['Sec'].unique()

for sec in sections:
    # This button acts as the Folder Header
    if st.button(f"📁 {sec}", key=f"hdr_{sec}", type="primary", use_container_width=True):
        st.session_state.open_section = sec if st.session_state.open_section != sec else None

    # This container ONLY appears if the section is open
    if st.session_state.open_section == sec:
        with st.container(border=True):
            sec_data = df[df['Sec'] == sec]
            for i, r in sec_data.iterrows():
                st.markdown(f"**{r['ID']} - {r['Desc']}**")
                
                # LOGIC BRANCHES
                if sec == "Walk-in Section":
                    if "Pepperoni" in r['Desc']: total = ci("Cases", f"c{i}", 0.5) * r['CM']
                    elif "Anchov" in r['Desc']: 
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: cn = ci("Cans", f"n{i}")
                        total = cs + (cn / 25.0)
                    elif "Bulk Ranch" in r['Desc'] or "Alfredo" in r['Desc']:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: ph = ci("Pouches", f"p{i}")
                        total = (cs * r['CM']) + ph
                    elif r['LM'] == 1.0:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: bs = ci("Bags", f"b{i}")
                        total = (cs * r['CM']) + bs
                    elif "Crust" in r['Desc'] and "Pan" not in r['Desc']:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: sl = ci("Sleeves", f"s{i}")
                        total = cs + (sl * 0.25)
                    elif "Cups" in r['Desc']:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: id = ci("Individual", f"id{i}")
                        total = cs + (id / r['CM'])
                    elif "Roll" in r['Desc'] or "String" in r['Desc']:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Case", f"c{i}")
                        with c2: lx = ci("Lexan", f"l{i}", 0.25)
                        total = (cs * r['CM']) + (lx * (r['LM'] if r['LM'] > 0 else 1.0))
                    else: total = ci(f"Total {r['Unit']}", f"t{i}")
                
                elif "Makeline Section (Top)" in sec:
                    total = ci("Lexan Count", f"l{i}", 0.25) * r['LM']
                
                elif "Makeline Section (Bottom)" in sec or "Cut Table" in sec:
                    lbl = "Individual" if any(x in r['Desc'] for x in ["Box", "Tray", "Cup", "Sleeve"]) else ("Bottle" if "Bottle" in r['Desc'] else "Lexan")
                    v = ci(lbl, f"v{i}", 0.25 if lbl != "Individual" else 1.0)
                    total = v * r['LM'] if lbl != "Individual" else v
                
                elif "Soda" in sec: total = ci("Bottle Count", f"s{i}")
                
                elif "Rack 1" in sec:
                    if r['LM'] > 0:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: bg = ci("Pouches", f"b{i}")
                        total = (cs * r['CM']) + bg
                    else: total = ci("Total Cases", f"c{i}") * r['CM']
                
                else:
                    if r['CM'] > 1:
                        c1, c2 = st.columns(2)
                        with c1: cs = ci("Cases", f"c{i}")
                        with c2: md = ci("Loose Units", f"m{i}")
                        total = (cs * r['CM']) + md
                    else: total = ci("Total Count", f"t{i}")

                inventory_totals.append({"Item #": r['ID'], "Description": r['Desc'], "Total": round(total, 2)})
            
            if st.button("✅ FINISH & COLLAPSE SECTION", key=f"cls_{sec}", type="secondary", use_container_width=True):
                st.session_state.open_section = None
                st.rerun()

# --- 5. OUTPUT ---
total_tasks = len(inventory_totals)
completed_tasks = sum(1 for item in inventory_totals if item["Total"] > 0)
if total_tasks > 0:
    st.progress(completed_tasks / total_tasks, text=f"🔥 Count Progress: {int((completed_tasks/total_tasks)*100)}%")

if st.button("GENERATE FINAL CORPORATE VALUES", type="secondary", use_container_width=True):
    final_df = pd.DataFrame(inventory_totals).groupby(['Item #', 'Description'], as_index=False)['Total'].sum()
    st.dataframe(final_df.sort_values(by="Item #"), use_container_width=True, hide_index=True, height=600)
    st.success("Sorted numerically for Corporate Upload.")

components.html("""<script>
    const inputs = window.parent.document.querySelectorAll('input[type=number]');
    inputs.forEach(input => { input.setAttribute('inputmode', 'decimal'); input.setAttribute('pattern', '[0-9]*'); });
    </script>""", height=0, width=0)
