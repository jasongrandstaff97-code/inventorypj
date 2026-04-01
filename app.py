import streamlit as st
import pandas as pd
import conversions 

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(page_title="Juskvi Inventory Engine", layout="centered")

# Injecting Papa John's Custom Colors & Accordion Styling
st.markdown("""
    <style>
    /* Make all major headers Papa John's Green */
    h1, h2, h3 {
        color: #00583E !important; 
        font-family: 'Arial', sans-serif;
    }
    
    /* Style the Accordion/Expander Tabs */
    div[data-testid="stExpander"] summary {
        background-color: #00583E !important;
        border-radius: 5px;
        padding: 10px !important;
    }
    
    /* Make the text inside the Accordion Tab White and Bold */
    div[data-testid="stExpander"] summary p {
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        margin-bottom: 0px !important;
    }
    
    /* Make the Calculate button Papa John's Red */
    .stButton>button {
        background-color: #DF1934 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
        margin-top: 20px;
        padding: 15px !important;
        font-size: 1.1rem !important;
    }
    
    .stButton>button:hover {
        background-color: #9c0c20 !important;
    }
    
    hr {
        border-color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Digital Walk-in & Makeline")
st.markdown("Count Shelf-to-Sheet. Expand a section to begin.")
st.divider()

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    return pd.read_csv("locations.csv", encoding="utf-8-sig")

df = load_data()
inventory_totals = []

# Tracker variables for the Accordion logic
current_section = ""
current_expander = None

# --- 3. THE USER INTERFACE (ACCORDION LAYOUT) ---
for index, row in df.iterrows():
    section = row['Section']
    item_name = row['Item_Name']
    count_type = row['Count_Type']
    corp_order = row['Corporate_Order']
    
    # If the app moves to a new physical area, create a new Accordion drop-down
    if section != current_section:
        # Create the expander (collapsed by default to save space)
        current_expander = st.expander(f"📁 {section}", expanded=False)
        current_section = section
        
    # Everything inside this 'with' block gets stuffed into the current accordion tab
    with current_expander:
        st.markdown(f"**{item_name}**")
        
        if count_type == "Prep":
            col1, col2, col3 = st.columns(3)
            with col1:
                cases = st.number_input("Cases", min_value=0.0, step=1.0, key=f"cases_{index}_{item_name}")
            with col2:
                bags = st.number_input("Bags", min_value=0.0, step=1.0, key=f"bags_{index}_{item_name}")
            with col3:
                lexans = st.number_input("Lexans", min_value=0.0, step=0.25, key=f"lexans_{index}_{item_name}")
                
            total_count = conversions.calculate_total(item_name, cases, bags, lexans)
            
        else:
            total_count = st.number_input("Total Count", min_value=0.0, step=1.0, key=f"single_{index}_{item_name}")

        inventory_totals.append({
            "Corporate_Order": corp_order,
            "Item": item_name,
            "Total Count": total_count
        })
        
        st.divider()

# --- 4. THE CORPORATE OUTPUT LAYER ---
st.header("Final Output")

if st.button("Generate Corporate Checklist", type="primary"):
    final_df = pd.DataFrame(inventory_totals)
    
    consolidated_df = final_df.groupby(['Corporate_Order', 'Item'], as_index=False)['Total Count'].sum()
    sorted_df = consolidated_df.sort_values(by="Corporate_Order").reset_index(drop=True)
    display_df = sorted_df[['Item', 'Total Count']]
    
    st.success("Calculations Complete. Ready for Data Entry.")
    st.dataframe(display_df, use_container_width=True)
