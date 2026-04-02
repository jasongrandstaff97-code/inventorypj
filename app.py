import streamlit as st
import pandas as pd

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(page_title="Juskvi Inventory Engine", layout="centered", initial_sidebar_state="collapsed")

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
    input[type="number"] {text-align: center !important; font-size: 1.1rem !important;}
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

# --- 3. THE MASTER DATA DICTIONARY ---
# Format: [Item_Number, Description, Target_Unit, Section, Case_Multiplier, Lexan_Multiplier]
# Order matches the printed sheets exactly.

master_inventory = [
    [1002, "Bulk Ranch Sauce", "Pouch", "Walk-in Section", 8.0, 1.0],
    [1005, "PIZZA SAUCE(POUCH)", "Pouch", "Walk-in Section", 6.0, 3.0], # 1 tub = 3 pouches
    [1016, "Green Peppers, Sliced", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1017, "Onions, Sliced", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1019, "Tomatoes, Diced Roma", "Tray", "Makeline Section (Top)", 2.0, 0.5],
    [1028, "Dustinator", "Bag", "Makeline Section (Bottom)", 1.0, 0.0],
    [1031, "Black Olives", "Pouch", "Makeline Section (Top)", 6.0, 1.0],
    [1040, "Pepperoni", "Bag", "Makeline Section (Top)", 2.0, 0.25],
    [1047, "PINEAPPLE - POUCH", "Pouch", "Makeline Section (Top)", 6.0, 0.5],
    [1049, "Bacon", "Bag", "Makeline Section (Top)", 4.0, 1.0],
    [1051, "Mushrooms-fresh", "Pail", "Makeline Section (Top)", 2.0, 0.5],
    [1052, "Fresh Spinach", "Bag", "Walk-in Section", 4.0, 1.0],
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Bottom)", 1.0, 0.0],
    [1064, "Beef", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1065, "Sausage", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1066, "Italian Sausage", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1071, "Anchovies", "Can", "Makeline Section (Top)", 25.0, 0.0],
    [1074, "Frozen Thin Crust 14\"", "Case", "Walk-in Section", 1.0, 0.0],
    [1075, "Dough Tray 10", "Tray", "Walk-in Section", 1.0, 0.0],
    [1076, "DOUGH M, 12 INCH", "Tray", "Walk-in Section", 1.0, 0.0],
    [1080, "Dough Tray 14", "Tray", "Walk-in Section", 1.0, 0.0],
    [1085, "Crust, Parbaked Pan Pizza", "Bag", "Walk-in Section", 4.0, 0.0],
    [1086, "Frozen Gluten Free Crust", "Case", "Walk-in Section", 1.0, 0.0],
    [1090, "Deli Pepperoni", "Bag", "Makeline Section (Top)", 1.0, 0.0],
    [1092, "WING, ROASTED 20 LB", "Bag", "Walk-in Section", 4.0, 1.0],
    [1093, "WINGS, BONELESS", "Bag", "Walk-in Section", 2.0, 1.0],
    [1095, "Grilled Chicken", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1102, "Spicy Garlic Dipping Cup", "Case", "Customer Service Counter", 1.0, 0.0],
    [1104, "Jug Garlic Sauce", "Bottle", "Customer Service Counter", 10.0, 0.0], # 1 case = 2 jugs = 10 bottles
    [1105, "Garlic Sauce Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1111, "7\" Sandwich Roll", "Bag", "Walk-in Section", 4.0, 0.0],
    [1114, "Ranch Sauce Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1119, "Blue Cheese Sauce Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1122, "Parmesan Sauce Jug", "Bottle", "Customer Service Counter", 10.0, 0.0], # 1 case = 10 bottles
    [1135, "Buffalo Sauce (Pouch)", "Pouch", "Walk-in Section", 8.0, 1.0],
    [1140, "Pouch Honey Chptl", "Pouch", "Walk-in Section", 10.0, 1.0],
    [1148, "BBQ Bulk", "Bag", "Walk-in Section", 8.0, 1.0],
    [1150, "Garlic Parm Truffle Sc", "Pouch", "Walk-in Section", 12.0, 0.5],
    [1152, "Sauce, Pizza Ranch", "Bag", "Walk-in Section", 12.0, 0.5],
    [1159, "Two Cheese P/R", "Bag", "Makeline Section (Bottom)", 2.0, 0.33], # 1 pouch = 3 lexans
    [1167, "Canadian Bacon", "Bag", "Makeline Section (Top)", 2.0, 1.0],
    [1178, "Philly Cheesesteak", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1209, "Banana Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],
    [1210, "Jalapeno Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],
    [1213, "Cheese Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1218, "Alfredo Sauce", "Pouch", "Walk-in Section", 3.0, 1.0],
    [1222, "Season Pkt", "Case", "Customer Service Counter", 1.0, 0.0],
    [1224, "CRP Packets", "Case", "Customer Service Counter", 1.0, 0.0],
    [1225, "Parmesan Packet", "Case", "Customer Service Counter", 1.0, 0.0],
    [1241, "Pepperoncini Peppers", "Bag", "Makeline Section (Top)", 6.0, 1.0],
    [1251, "Sliced American Cheese", "Bag", "Makeline Section (Top)", 4.0, 0.33], # 1 bag = 3 lexans
    [1257, "Three Cheese Blend", "Bag", "Makeline Section (Bottom)", 2.0, 0.5],
    [1331, "STRING CHEESE 20 LB", "Bag", "Makeline Section (Bottom)", 1.0, 0.25],
    [1406, "Chocolate Chip Cookie", "Each", "Walk-in Section", 24.0, 0.0],
    [1407, "Choc Chip Brownie", "Each", "Walk-in Section", 18.0, 0.0],
    [1505, "Cinnamon Pull Apart", "Each", "Walk-in Section", 16.0, 0.0],
    [2005, "Pizza Box 10", "Each", "Cut Table Section", 50.0, 0.0], # sleeve = 50
    [2007, "Pizza Box 12", "Each", "Cut Table Section", 50.0, 0.0],
    [2010, "Pizza Box 14", "Each", "Cut Table Section", 50.0, 0.0],
    [2025, "Pizza Box 16 In", "Each", "Cut Table Section", 50.0, 0.0],
    [2031, "Blaster Labels", "Roll", "Storage by office desk", 16.0, 0.0],
    [2039, "Pop Up Foil", "Case", "Back of store/Dry goods", 6.0, 0.0],
    [2043, "Pizza Box 8", "Each", "Cut Table Section", 50.0, 0.0],
    [2047, "CHICKEN BOX", "Each", "Cut Table Section", 240.0, 0.0],
    [2065, "Tray, Garlic Breadstick", "Each", "Back of store/Dry goods", 150.0, 0.0],
    [2071, "Garlic Knot Tray", "Each", "Back of store/Dry goods", 125.0, 0.0],
    [2146, "Sandwich Box", "Each", "Cut Table Section", 50.0, 0.0],
    [2305, "Medium Weight Plastic fork", "Case", "Back of store/Dry goods", 1000.0, 0.0],
    [2307, "Corrugated Pizza Sleeve", "Case", "Cut Table Section", 100.0, 0.0],
    [3007, "Cup 22oz Cold", "Case", "Back of store/Dry goods", 20.0, 0.0],
    [3012, "SOUFFLE CUP, HINGED LID", "Case", "Back of store/Dry goods", 40.0, 0.0], # 40 sleeves per case
    [3040, "14in Baking Sheet", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3041, "6.5in Baking Sheet", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3042, "10in Baking Sheet", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3044, "Dessert Bag", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3065, "Logo Napkins (Sleeve)", "Case", "Customer Service Counter", 32.0, 0.0],
    [6000, "20oz Pepsi", "Each", "Front of Store Soda", 24.0, 0.0],
    [6002, "20oz Pepsi ZeroSug", "Each", "Front of Store Soda", 24.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Front of Store Soda", 24.0, 0.0],
    [6004, "20oz Diet Mtn Dew", "Each", "Front of Store Soda", 24.0, 0.0],
    [6006, "20oz Aquafina", "Each", "Front of Store Soda", 24.0, 0.0],
    [6200, "2Ltr Pepsi", "Each", "Soda back of store", 8.0, 0.0],
    [6202, "2Ltr Pepsi ZeroSug", "Each", "Soda back of store", 8.0, 0.0],
    [6203, "2Ltr Mountain Dew", "Each", "Soda back of store", 8.0, 0.0],
    [6204, "2Ltr Diet Mtn Dew", "Each", "Soda back of store", 8.0, 0.0],
    [6660, "20oz Starry", "Each", "Front of Store Soda", 24.0, 0.0],
    [6661, "2Ltr Starry", "Each", "Soda back of store", 8.0, 0.0],
    [7013, "20oz Starry Zero", "Each", "Front of Store Soda", 24.0, 0.0],
    [7015, "2Ltr Starry Zero", "Each", "Soda back of store", 8.0, 0.0]
]

# Convert dictionary into a working dataframe
df = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult'])
df['Corporate_Order'] = df.index + 1 # Locks in the exact top-to-bottom printed sheet order

# --- 4. THE UI RENDER ENGINE ---
st.title("Inventory Count Engine")
st.caption("🚀 Secured Architecture | Papa John's Store 04185")

inventory_totals = []

# Group the items logically for the Walk-Path UI
sections = [
    "Walk-in Section", "Makeline Section (Top)", "Makeline Section (Bottom)",
    "Cut Table Section", "Customer Service Counter", "Soda back of store", 
    "Front of Store Soda", "Back of store/Dry goods", "Storage by office desk"
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
                    
                    # If item requires Lexan math (3 columns)
                    if lexan_mult > 0:
                        col1, col2, col3 = st.columns(3)
                        with col1: cases = st.number_input(f"Cases", step=1.0, key=f"c_{row['Item_Num']}")
                        with col2: mid = st.number_input(f"{unit}s", step=1.0, key=f"m_{row['Item_Num']}")
                        with col3: lexans = st.number_input(f"Lexans", step=0.25, key=f"l_{row['Item_Num']}")
                        
                        total = (cases * case_mult) + mid + (lexans * lexan_mult)
                    
                    # If item requires Case/Sleeve/Flat math (2 columns)
                    elif case_mult > 1:
                        col1, col2 = st.columns(2)
                        with col1: cases = st.number_input(f"Bulk (Cases/Sleeves)", step=1.0, key=f"c_{row['Item_Num']}")
                        with col2: mid = st.number_input(f"Loose {unit}s", step=1.0, key=f"m_{row['Item_Num']}")
                        
                        total = (cases * case_mult) + mid
                        
                    # Direct Single Count (1 column)
                    else:
                        total = st.number_input(f"Total Count ({unit})", step=1.0, key=f"t_{row['Item_Num']}")

                    # Store background math mapped perfectly to printed sheet
                    inventory_totals.append({
                        "Order": row['Corporate_Order'],
                        "Item #": row['Item_Num'],
                        "Description": row['Description'],
                        f"Final {unit}s": round(total, 2)
                    })

# --- 5. THE CORPORATE OUTPUT LAYER ---
st.markdown("---")
st.header("Inventory Summary")

if st.button("Generate Final Count Values", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    sorted_df = final_df.sort_values(by="Order").reset_index(drop=True)
    
    # Hide the internal order logic for clean display
    display_df = sorted_df.drop(columns=['Order'])
    
    st.toast("Totals Generated & Sorted!", icon="🍕")
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=600)
    
    st.success("List is sorted in the exact 3-page order of the Corporate System.")
    
