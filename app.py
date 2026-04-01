import streamlit as st
import pandas as pd
import conversions 

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(page_title="Juskvi Inventory Engine", layout="centered", initial_sidebar_state="collapsed")

# Injecting Enterprise UI CSS
st.markdown("""
    <style>
    /* 1. HIDE STREAMLIT DEFAULT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2. PAPA JOHN'S BRANDING */
    h1, h2, h3 {
        color: #00583E !important; 
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 3. SLEEK ACCORDION TABS */
    div[data-testid="stExpander"] {
        border: none !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        border-radius: 10px;
        margin-bottom: 12px;
    }
    div[data-testid="stExpander"] summary {
        background-color: #00583E !important;
        border-radius: 10px;
        padding: 12px !important;
    }
    div[data-testid="stExpander"] summary p {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0px !important;
    }
    
    /* 4. MODERN RED CALCULATION BUTTON */
    .stButton>button {
        background-color: #DF1934 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        font-size: 1.2rem !important;
        padding: 15px !important;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(223, 25, 52, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #9c0c20 !important;
        box-shadow: 0px 6px 15px rgba(223, 25, 52, 0.5);
    }
    
    /* 5. INPUT BOX POLISH */
    input[type="number"] {
        text-align: center !important;
        font-size: 1.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Digital Walk-in Engine")
st.caption("🚀 Shelf-to-Sheet Architecture | Papa John's Edition")

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    return pd.read_csv("locations.csv", encoding="utf-8-sig")

df = load_data()
inventory_totals = []

current_section = ""
current_expander = None

# --- 3. THE USER INTERFACE ---
for index, row in df.iterrows():
    section = row['Section']
    item_name = row['Item_Name']
    count_type = row['Count_Type']
    corp_order = row['Corporate_Order']
    
    if section != current_section:
        current_expander = st.expander(f"📁 {section}", expanded=False)
        current_section = section
        
    with current_expander:
        with st.container(border=True):
            st.markdown(f"**{item_name}**")
            
            if count_type == "Prep":
                col1, col2, col3 = st.columns(3)
                with col1:
                    cases = st.number_input("Cases", min_value=0.0, step=1.0, key=f"cases_{index}")
                with col2:
                    bags = st.number_input("Bags", min_value=0.0, step=1.0, key=f"bags_{index}")
                with col3:
                    lexans = st.number_input("Lexans", min_value=0.0, step=0.25, key=f"lexans_{index}")
                
                total_count = conversions.calculate_total(item_name, cases, bags, lexans)
                
            else:
                total_count = st.number_input("Total Count", min_value=0.0, step=1.0, key=f"single_{index}")

            inventory_totals.append({
                "Corporate_Order": corp_order,
                "Item": item_name,
                "Total Count": total_count
            })

# --- 4. THE CORPORATE OUTPUT LAYER ---
st.markdown("---")
st.header("Inventory Summary")

# Updated red box button text
if st.button("Generate Final Count Values", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    consolidated_df = final_df.groupby(['Corporate_Order', 'Item'], as_index=False)['Total Count'].sum()
    sorted_df = consolidated_df.sort_values(by="Corporate_Order").reset_index(drop=True)
    display_df = sorted_df[['Item', 'Total Count']]
    
    st.toast("Totals Generated!", icon="🍕")
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
