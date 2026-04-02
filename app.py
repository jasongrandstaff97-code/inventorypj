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
    
    /* Clean up the input boxes - remove arrows and center text */
    input[type="number"] {text-align: center !important; font-size: 1.2rem !important; font-weight: bold !important;}
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
# Format: [Item_Number, Description, Target_Unit, Section, Case_Multiplier, Lexan_Bottle_Multiplier]

master_inventory = [
    # --- WALK-IN SECTION (Ordered Exactly per Transcript) ---
    [1085, "Crust, Parbaked Pan Pizza", "Bag", "Walk-in Section", 4.0, 0.0],
    [1075, "Dough Tray 10", "Tray", "Walk-in Section", 1.0, 0.0],
    [1076, "DOUGH M, 12 INCH", "Tray", "Walk-in Section", 1.0, 0.0],
    [1080, "Dough Tray 14", "Tray", "Walk-in Section", 1.0, 0.0],
    [1082, "Dough Tray 16", "Tray", "Walk-in Section", 1.0, 0.0],
    [1218, "Alfredo Sauce", "Pouch", "Walk-in Section", 3.0, 1.0],
    [1086, "Frozen Gluten Free Crust", "Case", "Walk-in Section", 1.0, 0.0],
    [1002, "Bulk Ranch Sauce", "Pouch", "Walk-in Section", 8.0, 1.0],
    [1071, "Anchovies", "Can", "Walk-in Section", 25.0, 0.0],
    [1178, "Philly Cheesesteak", "Bag", "Walk-in Section", 4.0, 0.5],
    [1064, "Beef", "Bag", "Walk-in Section", 2.0, 0.5],
    [1167, "Canadian Bacon", "Bag", "Walk-in Section", 2.0, 1.0],
    [1049, "Bacon", "Bag", "Walk-in Section", 4.0, 1.0],
    [1095, "Grilled Chicken", "Bag", "Walk-in Section", 2.0, 0.5],
    [1093, "WINGS, BONELESS", "Bag", "Walk-in Section", 2.0, 1.0],
    [1092, "WING, ROASTED 20 LB", "Bag", "Walk-in Section", 4.0, 1.0],
    [1257, "Three Cheese Blend", "Bag", "Walk-in Section", 2.0, 0.5],
    [1159, "Two Cheese P/R", "Bag", "Walk-in Section", 2.0, 0.33],
    [1016, "Green Peppers, Sliced", "Bag", "Walk-in Section", 4.0, 0.5],
    [1017, "Onions, Sliced", "Bag", "Walk-in Section", 4.0, 0.5],
    [1052, "Fresh Spinach", "Bag", "Walk-in Section", 4.0, 1.0],
    [1019, "Tomatoes, Diced Roma", "Tray", "Walk-in Section", 2.0, 0.5],
    [1065, "Sausage", "Bag", "Walk-in Section", 4.0, 0.5],
    [1066, "Italian Sausage", "Bag", "Walk-in Section", 4.0, 0.5],
    [1051, "Mushrooms-fresh", "Pail", "Walk-in Section", 2.0, 0.5],
    [1074, "Frozen Thin Crust 14\"", "Case", "Walk-in Section", 1.0, 0.0], # Has special Sleeve logic in UI
    [1105, "Garlic Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1102, "Spicy Garlic Dipping Cup", "Case", "Walk-in Section", 1.0, 0.0],
    [1114, "Ranch Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1213, "Cheese Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1119, "Blue Cheese Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1251, "Sliced American Cheese", "Bag", "Walk-in Section", 4.0, 0.33],
    [1111, "7\" Sandwich Roll", "Bag", "Walk-in Section", 4.0, 0.0],
    [1150, "Garlic Parm Truffle Sc", "Pouch", "Walk-in Section", 12.0, 0.5],
    [1331, "STRING CHEESE 20 LB", "Bag", "Walk-in Section", 1.0, 0.25], # Case and Lexan requested
    [1104, "Jug Garlic Sauce", "Bottle", "Walk-in Section", 10.0, 0.0],
    [1057, "20lb PIZZA CHEESE", "Each", "Walk-in Section", 1.0, 0.0],
    [1152, "Sauce, Pizza Ranch", "Bag", "Walk-in Section", 12.0, 0.5],
    [1040, "Pepperoni", "Bag", "Walk-in Section", 2.0, 0.25],

    # --- PREP RACK SECTION (Lexans & Bottles) ---
    [1002, "Ranch (Lexan)", "Pouch", "Prep Rack", 8.0, 1.0],
    [1218, "Alfredo (Lexan)", "Pouch", "Prep Rack", 3.0, 1.0],
    [1148, "BBQ Sauce (Lexan)", "Bag", "Prep Rack", 8.0, 1.0],
    [1052, "Spinach (Lexan)", "Bag", "Prep Rack", 4.0, 1.0],
    [1051, "Mushrooms (Lexan)", "Pail", "Prep Rack", 2.0, 0.5],
    [1066, "Italian Sausage (Lexan)", "Bag", "Prep Rack", 4.0, 0.5],
    [1065, "Sausage (Lexan)", "Bag", "Prep Rack", 4.0, 0.5],
    [1064, "Beef (Lexan)", "Bag", "Prep Rack", 2.0, 0.5],
    [1178, "Philly Steak (Lexan)", "Bag", "Prep Rack", 4.0, 0.5],
    [1167, "Canadian Bacon (Lexan)", "Bag", "Prep Rack", 2.0, 1.0],
    [1049, "Bacon (Lexan)", "Bag", "Prep Rack", 4.0, 1.0],
    [1241, "Pepperoncini (Lexan)", "Bag", "Prep Rack", 6.0, 1.0],
    [1031, "Black Olives (Lexan)", "Pouch", "Prep Rack", 6.0, 1.0],
    [1047, "Pineapple (Lexan)", "Pouch", "Prep Rack", 6.0, 0.5],
    [1095, "Chicken (Lexan)", "Bag", "Prep Rack", 2.0, 0.5],
    [1159, "2 Cheese (Lexan)", "Bag", "Prep Rack", 2.0, 0.33],
    [1019, "Tomato (Lexan)", "Tray", "Prep Rack", 2.0, 0.5],
    [1016, "Green Pepper (Lexan)", "Bag", "Prep Rack", 4.0, 0.5],
    [1017, "Onion (Lexan)", "Bag", "Prep Rack", 4.0, 0.5],
    [1209, "Banana Pepper (Lexan)", "Bag", "Prep Rack", 8.0, 0.25],
    [1210, "Jalapeno (Lexan)", "Bag", "Prep Rack", 8.0, 0.25],
    [1150, "Garlic Parm (Bottle)", "Pouch", "Prep Rack", 12.0, 0.5],
    [1135, "Buffalo Sauce (Bottle)", "Pouch", "Prep Rack", 8.0, 1.0],
    [1148, "BBQ Sauce (Bottle)", "Bag", "Prep Rack", 8.0, 0.25],
    [1150, "Garlic Truffle (Bottle)", "Pouch", "Prep Rack", 12.0, 0.5],
    [1140, "Honey Chipotle (Bottle)", "Pouch", "Prep Rack", 10.0, 1.0],
    [1104, "Garlic Sauce Jug (Bottle)", "Bottle", "Prep Rack", 10.0, 1.0],
    [1152, "Pizza Ranch (Bottle)", "Bag", "Prep Rack", 12.0, 0.5],
    [1092, "Roasted Wings (Lexan)", "Bag", "Prep Rack", 4.0, 1.0],
    [1093, "Boneless Wings (Lexan)", "Bag", "Prep Rack", 2.0, 1.0],
    [1040, "Pepperoni (Lexan)", "Bag", "Prep Rack", 2.0, 0.25],

    # --- RETAINED MAKELINE & FRONT SECTIONS ---
    [1016, "Green Peppers, Sliced", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1017, "Onions, Sliced", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1019, "Tomatoes, Diced Roma", "Tray", "Makeline Section (Top)", 2.0, 0.5],
    [1028, "Dustinator", "Bag", "Makeline Section (Bottom)", 1.0, 0.0],
    [1031, "Black Olives", "Pouch", "Makeline Section (Top)", 6.0, 1.0],
    [1040, "Pepperoni", "Bag", "Makeline Section (Top)", 2.0, 0.25],
    [1047, "PINEAPPLE - POUCH", "Pouch", "Makeline Section (Top)", 6.0, 0.5],
    [1049, "Bacon", "Bag", "Makeline Section (Top)", 4.0, 1.0],
    [1051, "Mushrooms-fresh", "Pail", "Makeline Section (Top)", 2.0, 0.5],
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Bottom)", 1.0, 0.0],
    [1064, "Beef", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1065, "Sausage", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1066, "Italian Sausage", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1071, "Anchovies", "Can", "Makeline Section (Top)", 25.0, 0.0],
    [1090, "Deli Pepperoni", "Bag", "Makeline Section (Top)", 1.0, 0.0],
    [1095, "Grilled Chicken", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1159, "Two Cheese P/R", "Bag", "Makeline Section (Bottom)", 2.0, 0.33],
    [1167, "Canadian Bacon", "Bag", "Makeline Section (Top)", 2.0, 1.0],
    [1178, "Philly Cheesesteak", "Bag", "Makeline Section (Top)", 4.0, 0.5],
    [1209, "Banana Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],
    [1210, "Jalapeno Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],
    [1241, "Pepperoncini Peppers", "Bag", "Makeline Section (Top)", 6.0, 1.0],
    [1251, "Sliced American Cheese", "Bag", "Makeline Section (Top)", 4.0, 0.33],
    [1257, "Three Cheese Blend", "Bag", "Makeline Section (Bottom)", 2.0, 0.5],
    [1331, "STRING CHEESE 20 LB", "Bag", "Makeline Section (Bottom)", 1.0, 0.25],
    [2005, "Pizza Box 10", "Each", "Cut Table Section", 50.0, 0.0],
    [2007, "Pizza Box 12", "Each", "Cut Table Section", 50.0, 0.0],
    [2010, "Pizza Box 14", "Each", "Cut Table Section", 50.0, 0.0],
    [2025, "Pizza Box 16 In", "Each", "Cut Table Section", 50.0, 0.0],
    [2043, "Pizza Box 8", "Each", "Cut Table Section", 50.0, 0.0],
    [2047, "CHICKEN BOX", "Each", "Cut Table Section", 240.0, 0.0],
    [2146, "Sandwich Box", "Each", "Cut Table Section", 50.0, 0.0],
    [2307, "Corrugated Pizza Sleeve", "Case", "Cut Table Section", 100.0, 0.0],
    [1102, "Spicy Garlic Dipping Cup", "Case", "Customer Service Counter", 1.0, 0.0],
    [1104, "Jug Garlic Sauce", "Bottle", "Customer Service Counter", 10.0, 0.0],
    [1105, "Garlic Sauce Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1114, "Ranch Sauce Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1119, "Blue Cheese Sauce Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1122, "Parmesan Sauce Jug", "Bottle", "Customer Service Counter", 10.0, 0.0],
    [1213, "Cheese Cups", "Case", "Customer Service Counter", 1.0, 0.0],
    [1222, "Season Pkt", "Case", "Customer Service Counter", 1.0, 0.0],
    [1224, "CRP Packets", "Case", "Customer Service Counter", 1.0, 0.0],
    [1225, "Parmesan Packet", "Case", "Customer Service Counter", 1.0, 0.0],
    [3065, "Logo Napkins (Sleeve)", "Case", "Customer Service Counter", 32.0, 0.0],
    [6200, "2Ltr Pepsi", "Each", "Soda back of store", 8.0, 0.0],
    [6202, "2Ltr Pepsi ZeroSug", "Each", "Soda back of store", 8.0, 0.0],
    [6203, "2Ltr Mountain Dew", "Each", "Soda back of store", 8.0, 0.0],
    [6204, "2Ltr Diet Mtn Dew", "Each", "Soda back of store", 8.0, 0.0],
    [6661, "2Ltr Starry", "Each", "Soda back of store", 8.0, 0.0],
    [7015, "2Ltr Starry Zero", "Each", "Soda back of store", 8.0, 0.0],
    [6000, "20oz Pepsi", "Each", "Front of Store Soda", 24.0, 0.0],
    [6002, "20oz Pepsi ZeroSug", "Each", "Front of Store Soda", 24.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Front of Store Soda", 24.0, 0.0],
    [6004, "20oz Diet Mtn Dew", "Each", "Front of Store Soda", 24.0, 0.0],
    [6006, "20oz Aquafina", "Each", "Front of Store Soda", 24.0, 0.0],
    [6660, "20oz Starry", "Each", "Front of Store Soda", 24.0, 0.0],
    [7013, "20oz Starry Zero", "Each", "Front of Store Soda", 24.0, 0.0],
    [2039, "Pop Up Foil", "Case", "Back of store/Dry goods", 6.0, 0.0],
    [2065, "Tray, Garlic Breadstick", "Each", "Back of store/Dry goods", 150.0, 0.0],
    [2071, "Garlic Knot Tray", "Each", "Back of store/Dry goods", 125.0, 0.0],
    [2305, "Medium Weight Plastic fork", "Case", "Back of store/Dry goods", 1000.0, 0.0],
    [3007, "Cup 22oz Cold", "Case", "Back of store/Dry goods", 20.0, 0.0],
    [3012, "SOUFFLE CUP, HINGED LID", "Case", "Back of store/Dry goods", 40.0, 0.0],
    [3040, "14in Baking Sheet", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3041, "6.5in Baking Sheet", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3042, "10in Baking Sheet", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [3044, "Dessert Bag", "Case", "Back of store/Dry goods", 1.0, 0.0],
    [2031, "Blaster Labels", "Roll", "Storage by office desk", 16.0, 0.0]
]

# Convert to DataFrame
df = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult'])
df['Corporate_Order'] = df.index + 1

# --- 4. THE UI RENDER ENGINE ---
# Helper function to create clean, blank inputs
def clean_input(label, key, step=1.0):
    val = st.number_input(label, min_value=0.0, step=step, value=None, placeholder="", key=key)
    return val if val is not None else 0.0

st.title("Inventory Count Engine")
st.caption("🚀 Secured Architecture | Papa John's Store 04185")

inventory_totals = []

sections = [
    "Walk-in Section", "Prep Rack", "Makeline Section (Top)", "Makeline Section (Bottom)",
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
                    
                    # Special Logic for Thin Crust (Cases and Sleeves)
                    if "Thin Crust" in row['Description']:
                        col1, col2 = st.columns(2)
                        with col1: cases = clean_input(f"Cases", key=f"c_{index}")
                        with col2: sleeves = clean_input(f"Sleeves", key=f"s_{index}")
                        total = cases + (sleeves * 0.25) # Adjust multiplier if needed
                        
                    # Prep Rack specific - streamlined input
                    elif section == "Prep Rack":
                        if "(Bottle)" in row['Description']:
                            bottles = clean_input(f"Bottles", key=f"b_{index}")
                            total = bottles * lexan_mult
                        else:
                            lexans = clean_input(f"Lexans", key=f"l_{index}", step=0.25)
                            total = lexans * lexan_mult

                    # Standard Lexan Math (3 columns)
                    elif lexan_mult > 0:
                        col1, col2, col3 = st.columns(3)
                        with col1: cases = clean_input(f"Cases", key=f"c_{index}")
                        with col2: mid = clean_input(f"{unit}s", key=f"m_{index}")
                        with col3: lexans = clean_input(f"Lexans", key=f"l_{index}", step=0.25)
                        total = (cases * case_mult) + mid + (lexans * lexan_mult)
                    
                    # Bulk/Loose Math (2 columns)
                    elif case_mult > 1:
                        col1, col2 = st.columns(2)
                        with col1: cases = clean_input(f"Bulk", key=f"c_{index}")
                        with col2: mid = clean_input(f"Loose {unit}s", key=f"m_{index}")
                        total = (cases * case_mult) + mid
                        
                    # Direct Single Count (1 column)
                    else:
                        total = clean_input(f"Total Count ({unit})", key=f"t_{index}")

                    # Store math for final aggregation
                    inventory_totals.append({
                        "Order": row['Corporate_Order'],
                        "Item #": row['Item_Num'],
                        "Description": row['Description'].replace(" (Lexan)", "").replace(" (Bottle)", ""),
                        f"Final {unit}s": round(total, 2)
                    })

# --- 5. THE CORPORATE OUTPUT LAYER ---
st.markdown("---")
st.header("Inventory Summary")

if st.button("Generate Final Count Values", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    
    # Aggregates Walk-in + Prep Rack + Makeline perfectly based on Item #
    consolidated_df = final_df.groupby(['Item #', 'Description'], as_index=False).agg(
        Order=('Order', 'min'), # Keep the lowest order number for sorting
        Final_Total=(final_df.columns[3], 'sum') # Sum the totals
    )
    
    sorted_df = consolidated_df.sort_values(by="Order").reset_index(drop=True)
    display_df = sorted_df[['Item #', 'Description', 'Final_Total']]
    display_df.rename(columns={'Final_Total': 'Total Count'}, inplace=True)
    
    st.toast("Totals Generated & Sorted!", icon="🍕")
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=600)
    st.success("List is sorted and consolidated for the Corporate System.")
