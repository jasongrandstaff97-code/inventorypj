import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. PAGE SETUP & BRANDING ---
# We use a centered layout to keep the inputs focused on the S25 Ultra screen.
st.set_page_config(page_title="Juskvi Inventory Master", layout="centered", initial_sidebar_state="collapsed")

# --- 2. THE SURGICAL CSS LAYER ---
# This hides the Streamlit "bloat" and specifically kills the +/- buttons on number inputs.
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1, h2, h3 {color: #00583E !important; font-family: 'Helvetica Neue', sans-serif;}
    
    /* Expander Styling */
    div[data-testid="stExpander"] {border: none !important; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); border-radius: 10px; margin-bottom: 12px;}
    div[data-testid="stExpander"] summary {background-color: #00583E !important; border-radius: 10px; padding: 12px !important;}
    div[data-testid="stExpander"] summary p {color: white !important; font-size: 1.1rem !important; font-weight: 600 !important; margin-bottom: 0px !important;}
    
    /* Primary Red Button Styling */
    .stButton>button {background-color: #DF1934 !important; color: white !important; border-radius: 8px; border: none; font-weight: bold; font-size: 1.2rem !important; padding: 15px !important; width: 100%; box-shadow: 0px 4px 10px rgba(223, 25, 52, 0.3); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px;}
    .stButton>button:hover {background-color: #9c0c20 !important; box-shadow: 0px 6px 15px rgba(223, 25, 52, 0.5);}
    
    /* HIDING THE +/- INCREMENT BUTTONS FOR A CLEANER LOOK */
    button[data-testid="stNumberInputStepUp"], 
    button[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    div[data-testid="stNumberInputContainer"] {
        background-color: #f9f9f9 !important;
        border: 1px solid #ddd !important;
        border-radius: 8px !important;
    }
    input[type="number"] {
        text-align: center !important; 
        font-size: 1.4rem !important; 
        font-weight: bold !important;
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SECURITY AUTHENTICATION ---
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

# --- 4. THE ABSOLUTE MASTER DATA DICTIONARY ---
# Restored to 100% completeness.
master_inventory = [
    # --- MAKELINE TOP: THE ELITE 20 SPEED-RUN ---
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
    [1047, "Pineapple - Pouch", "Pouch", "Makeline Section (Top)", 6.0, 0.5],
    [1040, "Pepperoni", "Bag", "Makeline Section (Top)", 2.0, 0.25],
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Top)", 1.0, 1.0],
    [1159, "Two Cheese P/R", "Bag", "Makeline Section (Top)", 2.0, 0.33],
    [1257, "Three Cheese Blend", "Bag", "Makeline Section (Top)", 2.0, 0.5],
    [1210, "Jalapeno Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],
    [1209, "Banana Peppers", "Bag", "Makeline Section (Top)", 8.0, 0.25],

    # --- WALK-IN SECTION (RESTORED) ---
    [1085, "Crust, Parbaked Pan Pizza", "Bag", "Walk-in Section", 4.0, 0.0],
    [1075, "Dough Tray 10", "Tray", "Walk-in Section", 1.0, 0.0],
    [1076, "DOUGH M, 12 INCH", "Tray", "Walk-in Section", 1.0, 0.0],
    [1080, "Dough Tray 14", "Tray", "Walk-in Section", 1.0, 0.0],
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
    [1074, "Frozen Thin Crust 14\"", "Case", "Walk-in Section", 1.0, 0.0],
    [1105, "Garlic Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1102, "Spicy Garlic Dipping Cup", "Case", "Walk-in Section", 1.0, 0.0],
    [1114, "Ranch Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1213, "Cheese Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1119, "Blue Cheese Sauce Cups", "Case", "Walk-in Section", 1.0, 0.0],
    [1251, "Sliced American Cheese", "Bag", "Walk-in Section", 4.0, 0.33],
    [1111, "7\" Sandwich Roll", "Bag", "Walk-in Section", 4.0, 0.0],
    [1150, "Garlic Parm Truffle Sc", "Pouch", "Walk-in Section", 12.0, 0.5],
    [1331, "STRING CHEESE 20 LB", "Bag", "Walk-in Section", 1.0, 0.25], 
    [1104, "Jug Garlic Sauce", "Bottle", "Walk-in Section", 10.0, 0.0],
    [1057, "20lb PIZZA CHEESE", "Each", "Walk-in Section", 1.0, 0.0],
    [1152, "Sauce, Pizza Ranch", "Bag", "Walk-in Section", 12.0, 0.5],
    [1040, "Pepperoni", "Bag", "Walk-in Section", 2.0, 0.25],

    # --- PREP RACK (RESTORED) ---
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

     # --- MAKELINE SECTION (BOTTOM) 
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Bottom)", 1.0, 0.0], # EXCEPTION: Counted by Each
    [1218, "Alfredo Sauce", "Pouch", "Makeline Section (Bottom)", 3.0, 1.0],
    [1002, "Bulk Ranch Sauce", "Pouch", "Makeline Section (Bottom)", 8.0, 1.0],
    [1148, "Barbecue Sauce", "Bag", "Makeline Section (Bottom)", 8.0, 1.0],
    [1251, "Sliced American Cheese", "Bag", "Makeline Section (Bottom)", 4.0, 0.33],
    [1052, "Fresh Spinach", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1331, "String Cheese", "Bag", "Makeline Section (Bottom)", 1.0, 0.25],
    [1152, "Pizza Ranch (Bottle)", "Bottle", "Makeline Section (Bottom)", 12.0, 0.5],
    [1150, "Garlic Truffle (Bottle)", "Bottle", "Makeline Section (Bottom)", 12.0, 0.5],
    [1085, "Parbaked Pan Crust", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1111, "7\" Sandwich Roll", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1092, "Roasted Wings", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1093, "Boneless Wings", "Bag", "Makeline Section (Bottom)", 2.0, 1.0],
    [1114, "Ranch Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1119, "Blue Cheese Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1105, "Garlic Sauce Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1102, "Spicy Garlic Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1213, "Cheese Sauce Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1040, "Pepperoni (Lexan)", "Bag", "Makeline Section (Bottom)", 2.0, 0.25],

    # --- MAKELINE SECTION (BOTTOM) 
    [1057, "20lb PIZZA CHEESE", "Each", "Makeline Section (Bottom)", 1.0, 0.0], # EXCEPTION: Counted by Each
    [1218, "Alfredo Sauce", "Pouch", "Makeline Section (Bottom)", 3.0, 1.0],
    [1002, "Bulk Ranch Sauce", "Pouch", "Makeline Section (Bottom)", 8.0, 1.0],
    [1148, "Barbecue Sauce", "Bag", "Makeline Section (Bottom)", 8.0, 1.0],
    [1251, "Sliced American Cheese", "Bag", "Makeline Section (Bottom)", 4.0, 0.33],
    [1052, "Fresh Spinach", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1331, "String Cheese", "Bag", "Makeline Section (Bottom)", 1.0, 0.25],
    [1152, "Pizza Ranch (Bottle)", "Bottle", "Makeline Section (Bottom)", 12.0, 0.5],
    [1150, "Garlic Truffle (Bottle)", "Bottle", "Makeline Section (Bottom)", 12.0, 0.5],
    [1085, "Parbaked Pan Crust", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1111, "7\" Sandwich Roll", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1092, "Roasted Wings", "Bag", "Makeline Section (Bottom)", 4.0, 1.0],
    [1093, "Boneless Wings", "Bag", "Makeline Section (Bottom)", 2.0, 1.0],
    [1114, "Ranch Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1119, "Blue Cheese Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1105, "Garlic Sauce Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1102, "Spicy Garlic Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1213, "Cheese Sauce Cups (INDIVIDUAL)", "Unit", "Makeline Section (Bottom)", 1.0, 0.0],
    [1040, "Pepperoni (Lexan)", "Bag", "Makeline Section (Bottom)", 2.0, 0.25],
    
    # --- BACKUP BOXES (RESTORED) ---
    [2043, "Pizza Box 8", "Each", "Backup Boxes", 50.0, 0.0],
    [2005, "Pizza Box 10", "Each", "Backup Boxes", 50.0, 0.0],
    [2007, "Pizza Box 12", "Each", "Backup Boxes", 50.0, 0.0],
    [2010, "Pizza Box 14", "Each", "Backup Boxes", 50.0, 0.0],
    [2025, "Pizza Box 16 In", "Each", "Backup Boxes", 50.0, 0.0],
    [2146, "Sandwich Box", "Each", "Backup Boxes", 50.0, 0.0],
    [2047, "CHICKEN BOX", "Each", "Backup Boxes", 240.0, 0.0],
    
    # --- CUT TABLE (RESTORED) ---
    [2146, "Sandwich Box", "Each", "Cut Table Section", 50.0, 0.0],
    [2047, "CHICKEN BOX", "Each", "Cut Table Section", 240.0, 0.0], 
    [2043, "Pizza Box 8", "Each", "Cut Table Section", 50.0, 0.0],
    [2005, "Pizza Box 10", "Each", "Cut Table Section", 50.0, 0.0],
    [2007, "Pizza Box 12", "Each", "Cut Table Section", 50.0, 0.0],
    [2010, "Pizza Box 14", "Each", "Cut Table Section", 50.0, 0.0],
    [2025, "Pizza Box 16 In", "Each", "Cut Table Section", 50.0, 0.0],
    [2071, "Garlic Knot Tray", "Each", "Cut Table Section", 125.0, 0.0],
    [2065, "Tray, Garlic Breadstick", "Each", "Cut Table Section", 150.0, 0.0],
    [2305, "Medium Weight Plastic fork", "Case", "Cut Table Section", 1000.0, 0.0],
    [1118, "BBQ Sauce Cups", "Case", "Cut Table Section", 1.0, 0.0],
    [1117, "Buffalo Sauce Cups", "Case", "Cut Table Section", 1.0, 0.0],
    [2039, "Pop Up Foil", "Case", "Cut Table Section", 6.0, 0.0],
    [2307, "Corrugated Pizza Sleeve", "Case", "Cut Table Section", 100.0, 0.0],
    [1241, "Pepperoncini Peppers", "Bag", "Cut Table Section", 6.0, 1.0],
    [1105, "Garlic Sauce Cups", "Case", "Cut Table Section", 1.0, 0.0],
    [1222, "Season Pkt", "Case", "Cut Table Section", 1.0, 0.0],
    [1135, "Buffalo Sauce (Pouch)", "Pouch", "Cut Table Section", 8.0, 1.0],
    [1148, "BBQ Bulk", "Bag", "Cut Table Section", 8.0, 1.0],
    [1140, "Pouch Honey Chptl", "Pouch", "Cut Table Section", 10.0, 1.0],
    [1150, "Garlic Parm Truffle Sc", "Pouch", "Cut Table Section", 12.0, 0.5],

    # --- CUSTOMER SERVICE ---
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

    # --- FRONT SODA ---
    [6000, "20oz Pepsi", "Each", "Front of Store Soda", 24.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Front of Store Soda", 24.0, 0.0],
    [6660, "20oz Starry", "Each", "Front of Store Soda", 24.0, 0.0],
    [6006, "20oz Aquafina", "Each", "Front of Store Soda", 24.0, 0.0],
    [6002, "20oz Pepsi ZeroSug", "Each", "Front of Store Soda", 24.0, 0.0],
    [6200, "2Ltr Pepsi", "Each", "Front of Store Soda", 8.0, 0.0],
    [6203, "2Ltr Mountain Dew", "Each", "Front of Store Soda", 8.0, 0.0],
    [6661, "2Ltr Starry", "Each", "Front of Store Soda", 8.0, 0.0],
    [6202, "2Ltr Pepsi ZeroSug", "Each", "Front of Store Soda", 8.0, 0.0],

    # --- BACK SODA ---
    [6202, "2Ltr Pepsi ZeroSug", "Each", "Soda back of store", 8.0, 0.0],
    [6200, "2Ltr Pepsi", "Each", "Soda back of store", 8.0, 0.0],
    [6661, "2Ltr Starry", "Each", "Soda back of store", 8.0, 0.0],
    [6203, "2Ltr Mountain Dew", "Each", "Soda back of store", 8.0, 0.0],
    [6000, "20oz Pepsi", "Each", "Soda back of store", 24.0, 0.0],
    [6003, "20oz Mountain Dew", "Each", "Soda back of store", 24.0, 0.0],
    [6660, "20oz Starry", "Each", "Soda back of store", 24.0, 0.0],
    [6002, "20oz Pepsi ZeroSug", "Each", "Soda back of store", 24.0, 0.0],

    # --- DRY GOODS ---
    [3007, "Cup 22oz Cold", "Case", "Dry Goods (Rack 1)", 20.0, 0.0],
    [1135, "Buffalo Sauce (Pouch)", "Pouch", "Dry Goods (Rack 1)", 8.0, 1.0],
    [1140, "Pouch Honey Chptl", "Pouch", "Dry Goods (Rack 1)", 10.0, 1.0],
    [1150, "Garlic Parm Truffle Sc", "Pouch", "Dry Goods (Rack 1)", 12.0, 0.5],
    [1148, "BBQ Bulk", "Bag", "Dry Goods (Rack 1)", 8.0, 1.0],
    [1241, "Pepperoncini Peppers", "Bag", "Dry Goods (Rack 1)", 6.0, 1.0],
    [1031, "Black Olives", "Pouch", "Dry Goods (Rack 1)", 6.0, 1.0],
    [1209, "Banana Peppers", "Bag", "Dry Goods (Rack 1)", 8.0, 0.25],
    [1210, "Jalapeno Peppers", "Bag", "Dry Goods (Rack 1)", 8.0, 0.25],
    [1191, "IT Seasoning", "Bag", "Dry Goods (Rack 1)", 1.0, 0.0],
    [1047, "PINEAPPLE - POUCH", "Pouch", "Dry Goods (Rack 1)", 6.0, 0.5],
    [1005, "PIZZA SAUCE(POUCH)", "Pouch", "Dry Goods (Rack 2 - Pizza Sauce)", 6.0, 3.0], 
    [1118, "BBQ Sauce Cups", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [1117, "Buffalo Sauce Cups", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [2065, "Tray, Garlic Breadstick", "Each", "Dry Goods (Rack 3)", 150.0, 0.0],
    [2071, "Garlic Knot Tray", "Each", "Dry Goods (Rack 3)", 125.0, 0.0],
    [2307, "Corrugated Pizza Sleeve", "Case", "Dry Goods (Rack 3)", 100.0, 0.0],
    [3044, "Dessert Bag", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3042, "10in Baking Sheet", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [3040, "14in Baking Sheet", "Case", "Dry Goods (Rack 3)", 1.0, 0.0],
    [2039, "Pop Up Foil", "Case", "Dry Goods (Rack 3)", 6.0, 0.0],
    [3012, "SOUFFLE CUP, HINGED LID", "Case", "Dry Goods (Rack 3)", 40.0, 0.0],
    [2305, "Medium Weight Plastic fork", "Case", "Dry Goods (Rack 3)", 1000.0, 0.0],
    [2047, "CHICKEN BOX", "Each", "Dry Goods (Rack 3)", 240.0, 0.0],
    [3065, "Logo Napkins (Sleeve)", "Case", "Dry Goods (Rack 3)", 32.0, 0.0],
    [2031, "Blaster Labels", "Roll", "Storage by office desk", 16.0, 0.0]
]

# Convert the dictionary into a DataFrame for the Engine to process.
df = pd.DataFrame(master_inventory, columns=['Item_Num', 'Description', 'Unit', 'Section', 'Case_Mult', 'Lexan_Mult'])

# --- 5. THE UI RENDER ENGINE ---
# This function handles the "Clean" input boxes without the +/- clutter.
def clean_input(label, key):
    try:
        val = st.number_input(label, min_value=0.0, value=None, placeholder="0.0", key=key)
        return val if val is not None else 0.0
    except Exception:
        return 0.0

st.title("Inventory Count Engine Master")
st.caption("🚀 Fully Loaded Unabridged Version | Store 04185")

# The Gamified Progress Bar for psychological momentum.
progress_bar = st.progress(0.0, text="🔥 Inventory Completion: 0%")
st.markdown("<br>", unsafe_allow_html=True) 

inventory_totals = []

# DEFINING THE OPTIMIZED WALK ORDER
sections = [
    "Makeline Section (Top)", "Makeline Section (Bottom)", "Prep Rack", "Walk-in Section", 
    "Backup Boxes", "Cut Table Section", "Customer Service Counter", "Soda back of store", 
    "Front of Store Soda", "Dry Goods (Rack 1)", "Dry Goods (Rack 2 - Pizza Sauce)", 
    "Dry Goods (Rack 3)", "Storage by office desk"
]

for section in sections:
    section_data = df[df['Section'] == section]
    if not section_data.empty:
        # Preserve the manual order defined in the list.
        section_data = section_data.reset_index() 
        with st.expander(f"📁 {section}", expanded=(section == "Makeline Section (Top)")):
            for index, row in section_data.iterrows():
                item_desc = f"{row['Item_Num']} - {row['Description']}"
                unit = row['Unit']
                case_mult = row['Case_Mult']
                lexan_mult = row['Lexan_Mult']
                
                with st.container(border=True):
                    st.markdown(f"**{item_desc}**")
                    
                    # LOGIC BRANCH 1: MAKELINE TOP SPEED-RUN (LEXAN ONLY)
                    if section == "Makeline Section (Top)":
                        lexans = clean_input(f"Total Lexans", key=f"l_{index}_{section}")
                        total = lexans * lexan_mult

                    # LOGIC BRANCH 2: THIN CRUST FRACTIONAL LOGIC
                    elif "Thin Crust" in row['Description']:
                        col1, col2 = st.columns(2)
                        with col1: cases = clean_input(f"Cases", key=f"c_{index}_{section}")
                        with col2: sleeves = clean_input(f"Sleeves", key=f"s_{index}_{section}")
                        total = cases + (sleeves * 0.25)

                    # LOGIC BRANCH 3: PREP RACK DUAL-COUNT (UNITS + LEXANS)
                    elif section == "Prep Rack":
                        col1, col2 = st.columns(2)
                        with col1: mid = clean_input(f"Backups ({unit}s)", key=f"m_{index}_{section}")
                        with col2: lexans = clean_input(f"Lexans", key=f"l_{index}_{section}")
                        total = mid + (lexans * lexan_mult)

                    # LOGIC BRANCH 4: FULL TRIPLE COUNT (CASE/UNIT/LEXAN)
                    elif lexan_mult > 0:
                        col1, col2, col3 = st.columns(3)
                        with col1: cases = clean_input(f"Cases", key=f"c_{index}_{section}")
                        with col2: mid = clean_input(f"{unit}s", key=f"m_{index}_{section}")
                        with col3: lexans = clean_input(f"Lexans", key=f"l_{index}_{section}")
                        total = (cases * case_mult) + mid + (lexans * lexan_mult)

                    # LOGIC BRANCH 5: STANDARD CASE/UNIT DUAL COUNT
                    elif case_mult > 1:
                        col1, col2 = st.columns(2)
                        with col1: cases = clean_input(f"Bulk", key=f"c_{index}_{section}")
                        with col2: mid = clean_input(f"Loose {unit}s", key=f"m_{index}_{section}")
                        total = (cases * case_mult) + mid

                    # LOGIC BRANCH 6: SINGLE UNIT ENTRY
                    else:
                        total = clean_input(f"Total Count ({unit})", key=f"t_{index}_{section}")

                    inventory_totals.append({
                        "Item #": row['Item_Num'],
                        "Description": row['Description'],
                        "Total Count": round(total, 2)
                    })

# PROGRESS BAR CALCULATION
total_tasks = len(inventory_totals)
completed_tasks = sum(1 for item in inventory_totals if item["Total Count"] > 0)
if total_tasks > 0:
    progress_fraction = completed_tasks / total_tasks
    progress_bar.progress(progress_fraction, text=f"🔥 Inventory Completion: {int(progress_fraction * 100)}% ({completed_tasks}/{total_tasks} counted)")

# --- 6. THE AGGREGATION & SORTING LAYER ---
st.markdown("---")
st.header("Inventory Summary")
if st.button("Generate Final Count Values", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    # This groups multiple locations (e.g., Pepp in Walk-in + Pepp on Makeline) into one total.
    consolidated_df = final_df.groupby(['Item #', 'Description'], as_index=False)['Total Count'].sum()
    # Sort by Item # to match the corporate data entry screen.
    sorted_df = consolidated_df.sort_values(by="Item #").reset_index(drop=True)
    st.toast("Corporate Data Generated!", icon="🍕")
    st.dataframe(sorted_df, use_container_width=True, hide_index=True, height=600)

# --- 7. THE S25 ULTRA KEYBOARD INJECTION ---
# This forces the decimal pad to appear instantly on touch.
components.html(
    """
    <script>
    const inputs = window.parent.document.querySelectorAll('input[type=number]');
    inputs.forEach(input => {
        input.setAttribute('inputmode', 'decimal');
        input.setAttribute('pattern', '[0-9]*');
    });
    </script>
    """,
    height=0,
    width=0,
)
