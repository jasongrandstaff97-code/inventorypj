import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. BRANDING & MOBILE OPTIMIZATION ---
st.set_page_config(page_title="Store 04185 Inventory", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 {color: #00583E !important; font-family: 'Helvetica Neue', sans-serif;}
    div[data-testid="stExpander"] {border: none !important; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); border-radius: 10px; margin-bottom: 12px;}
    div[data-testid="stExpander"] summary {background-color: #00583E !important; border-radius: 10px; padding: 12px !important;}
    div[data-testid="stExpander"] summary p {color: white !important; font-size: 1.1rem !important; font-weight: 600 !important; margin-bottom: 0px !important;}
    .stButton>button {background-color: #DF1934 !important; color: white !important; border-radius: 8px; border: none; font-weight: bold; font-size: 1.2rem !important; padding: 15px !important; width: 100%; box-shadow: 0px 4px 10px rgba(223, 25, 52, 0.3); transition: all 0.3s ease;}
    .stButton>button:hover {background-color: #9c0c20 !important;}
    input[type="number"] {text-align: center !important; font-size: 1.3rem !important; font-weight: bold !important;}
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Papa John's Inventory")
    st.caption("Store 04185 | Authorized Personnel Only")
    u = st.text_input("User ID")
    p = st.text_input("Password", type="password")
    if st.button("Secure Login"):
        if u == "MGR" and p == "Papa4185":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()
    # --- 3. MASTER DATA DICTIONARY ---
# [Item_Num, Description, Unit, Section, Case_Mult, Lexan_Mult, Is_Cup]
master_inventory = [
    # --- Walk-in (Bulk Focused) ---
    [1218, "Alfredo Sauce", "Pouch", "Walk-in", 3.0, 0.0, False],
    [1002, "Bulk Ranch Sauce", "Pouch", "Walk-in", 8.0, 0.0, False],
    [1178, "Philly Cheesesteak", "Bag", "Walk-in", 4.0, 0.0, False],
    [1064, "Beef", "Bag", "Walk-in", 2.0, 0.0, False],
    [1331, "STRING CHEESE (20LB)", "Bag", "Walk-in", 1.0, 0.25, False],
    [1040, "Pepperoni", "Bag", "Walk-in", 2.0, 0.0, False],
    [1104, "Jug Garlic Sauce", "Bottle", "Walk-in", 10.0, 0.0, False],
    [1152, "Pizza Ranch Sauce", "Bag", "Walk-in", 12.0, 0.0, False],
    
    # --- Prep Rack (Lexans Only) ---
    [1040, "Pepperoni", "Bag", "Prep Rack", 2.0, 0.25, False],
    [1064, "Beef", "Bag", "Prep Rack", 2.0, 0.5, False],
    [1065, "Sausage", "Bag", "Prep Rack", 4.0, 0.5, False],
    [1031, "Black Olives", "Pouch", "Prep Rack", 6.0, 1.0, False],
    [1150, "Garlic Truffle", "Pouch", "Prep Rack", 12.0, 0.5, False],
    
    # --- Makeline (Lexans & Special Logic) ---
    [1331, "STRING CHEESE", "Bag", "Makeline", 1.0, 0.25, False],
    [1111, "7\" Sandwich Bread", "Bag", "Makeline", 4.0, 1.0, False],
    [1251, "American Cheese Slice", "Bag", "Makeline", 4.0, 0.33, False],
    [1005, "PIZZA SAUCE (POUCH)", "Pouch", "Makeline", 6.0, 1.0, False],
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline", 1.0, 0.0, False],
    
    # --- Cut Table (Individual Counts / 160) ---
    [1105, "Garlic Sauce Cups", "Case", "Cut Table", 160.0, 0.0, True],
    [1118, "BBQ Sauce Cups", "Case", "Cut Table", 160.0, 0.0, True],
    [1117, "Buffalo Sauce Cups", "Case", "Cut Table", 160.0, 0.0, True],
    [2039, "Pop Up Foil", "Case", "Cut Table", 6.0, 0.0, False],
    [2307, "Corrugated Pizza Sleeve", "Case", "Cut Table", 100.0, 0.0, False],
    
    # --- Dough Station (Patty Counts) ---
    [1075, "Small Dough", "Patty", "Dough Station", 1.0, 0.0, False],
    [1076, "Medium Dough", "Patty", "Dough Station", 1.0, 0.0, False],
    [1080, "Large Dough", "Patty", "Dough Station", 1.0, 0.0, False]
]

df_master = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult', 'Is_Cup'])
# --- 4. THE UI ENGINE ---
st.title("Inventory Count Engine")
st.caption("Store 04185 | Logic over Syntax")

inventory_totals = []
sections = df_master['Section'].unique()

for sec in sections:
    with st.expander(f"📁 {sec}", expanded=False):
        sec_data = df_master[df_master['Section'] == sec]
        for idx, row in sec_data.iterrows():
            item_label = f"{row['Item_Num']} - {row['Description']}"
            
            with st.container(border=True):
                st.markdown(f"**{item_label}**")
                total = 0.0
                
                # CASE 1: Individual Cup Counts (Cut Table Only)
                if row['Is_Cup'] and sec == "Cut Table":
                    cups = st.number_input("Count Indiv. Cups", key=f"ind_{idx}", step=1.0, value=None, placeholder="...")
                    if cups: total = cups / row['Case_Mult']
                
                # CASE 2: Prep/Makeline (Lexan Focused)
                elif sec in ["Prep Rack", "Makeline"]:
                    if row['Lexan_Mult'] > 0:
                        lx = st.number_input("Lexans", key=f"l_{idx}", step=0.25, value=None, placeholder="0.0")
                        total = (lx if lx else 0) * row['Lexan_Mult']
                    else:
                        v = st.number_input(f"Total ({row['Unit']})", key=f"t_{idx}")
                        total = v if v else 0
                
                # CASE 3: General Walk-in / Bulk
                else:
                    c1, c2 = st.columns(2)
                    with c1: cs = st.number_input("Cases/Bags", key=f"c_{idx}", value=None, placeholder="0")
                    with c2:
                        if row['Lexan_Mult'] > 0:
                            lx = st.number_input("Lexans", key=f"lx_{idx}", step=0.25, value=None, placeholder="0.0")
                            total = (cs if cs else 0) + ((lx if lx else 0) * row['Lexan_Mult'])
                        else:
                            total = (cs if cs else 0)

                inventory_totals.append({"Item #": row['Item_Num'], "Description": row['Description'], "Count": round(total, 2)})

# --- 5. EXPORT & KEYPAD INJECTION ---
st.markdown("---")
if st.button("Finalize Shift Counts", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    final_df = final_df.groupby(['Item #', 'Description'], as_index=False)['Count'].sum()
    st.dataframe(final_df, use_container_width=True, hide_index=True)
    csv = final_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="pj_inventory.csv", mime="text/csv")

components.html("<script>const inputs = window.parent.document.querySelectorAll('input[type=number]'); inputs.forEach(input => { input.setAttribute('inputmode', 'decimal'); });</script>", height=0)


    
