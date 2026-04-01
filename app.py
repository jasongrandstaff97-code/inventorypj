import streamlit as st
import pandas as pd
import conversions 

# --- 1. PAGE SETUP & BRANDING ---
st.set_page_config(page_title="Juskvi Inventory Engine", layout="centered")

# Injecting Papa John's Custom Colors (Dark Green & Red)
st.markdown("""
    <style>
    /* Make all major headers Papa John's Green */
    h1, h2, h3 {
        color: #00583E !important; 
        font-family: 'Arial', sans-serif;
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
    }
    
    /* Make the button darker red when you hover over it */
    .stButton>button:hover {
        background-color: #9c0c20 !important;
    }
    
    /* Make the divider lines Papa John's Red */
    hr {
        border-color: #DF1934 !important;
        border-width: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Digital Walk-in & Makeline")
st.markdown("Count Shelf-to-Sheet. The app handles the conversions and sorting.")
st.divider()

# --- 2. DATA LOADING ---
# Reads your physical layout from the locations.csv blueprint
@st.cache_data
def load_data():
    return pd.read_csv("locations.csv")

# Load the CSV into a Pandas DataFrame
df = load_data()

# Dictionary to hold the final calculated numbers quietly in the background
inventory_totals = []

# Tracker to know when to print a new physical Section Header
current_section = ""


# --- 3. THE USER INTERFACE (SHELF-TO-SHEET) ---
for index, row in df.iterrows():
    # Extract the rules from your CSV for this specific row
    section = row['Section']
    item_name = row['Item_Name']
    count_type = row['Count_Type']
    corp_order = row['Corporate_Order']
    
    # If the app moves to a new physical area, create a large Green header
    if section != current_section:
        st.header(section)
        current_section = section
        
    st.markdown(f"**{item_name}**")
    
    # THE LOGIC GATE: Does this item need Lexan math?
    if count_type == "Prep":
        # Create 3 side-by-side boxes for high-speed input
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cases = st.number_input("Cases", min_value=0.0, step=1.0, key=f"cases_{index}_{item_name}")
        with col2:
            bags = st.number_input("Bags", min_value=0.0, step=1.0, key=f"bags_{index}_{item_name}")
        with col3:
            lexans = st.number_input("Lexans", min_value=0.0, step=0.25, key=f"lexans_{index}_{item_name}")
            
        # Send Jason's numbers to the conversion engine
        total_count = conversions.calculate_total(item_name, cases, bags, lexans)
        
    # If it's Dry Storage, Soda, or a 'Single' item, show 1 standard box
    else:
        total_count = st.number_input("Total Count", min_value=0.0, step=1.0, key=f"single_{index}_{item_name}")

    # Save the math to our background list
    inventory_totals.append({
        "Corporate_Order": corp_order,
        "Item": item_name,
        "Total Count": total_count
    })
    
    st.divider()


# --- 4. THE CORPORATE OUTPUT LAYER ---
st.header("Final Output")

if st.button("Generate Corporate Checklist", type="primary"):
    # Convert the background data into a clean data table
    final_df = pd.DataFrame(inventory_totals)
    
    # The Consolidation Engine: 
    # Finds items in multiple places (like Walk-in Spinach + Makeline Spinach) 
    # and adds them together into one master number.
    consolidated_df = final_df.groupby(['Corporate_Order', 'Item'], as_index=False)['Total Count'].sum()
    
    # The Sorting Engine:
    # Forces the app to perfectly match the back-office computer's layout
    sorted_df = consolidated_df.sort_values(by="Corporate_Order").reset_index(drop=True)
    
    # Hide the sorting number from the final display to keep it looking clean
    display_df = sorted_df[['Item', 'Total Count']]
    
    st.success("Calculations Complete. Ready for Data Entry.")
    
    # Display the final, combined, sorted list
    st.dataframe(display_df, use_container_width=True)
