import streamlit as st
import pandas as pd
from conversions import conversions_dict

st.set_page_config(page_title="Papa John's Inventory", page_icon="🍕", layout="wide")

# Load data
@st.cache_data
def load_csv():
    return pd.read_csv("locations.csv")

df = load_csv()

st.title("🍕 Store 04185 Inventory Count")

# Use a form so the page doesn't refresh every single time you hit a "+" button
with st.form("inventory_form"):
    locations = df['Location'].unique()
    
    # Dictionary to hold all user inputs
    inputs = {}
    
    # Build out the visual layout
    for loc in locations:
        st.subheader(loc)
        items = df[df['Location'] == loc]['Description'].tolist()
        
        for item in items:
            key = f"{loc}|{item}"
            # Standard number input for easy tapping on mobile
            inputs[key] = st.number_input(item, min_value=0.0, step=1.0, key=key)
            
        st.divider()
        
    submitted = st.form_submit_button("Calculate Final Totals", type="primary")

# The math engine that runs when you hit the calculate button
if submitted:
    st.header("📋 Final Calculated Case/Unit Counts")
    
    final_totals = {}
    
    for key, count in inputs.items():
        if count > 0:
            loc, item = key.split("|")
            
            # Default multiplier is 1 (direct count) unless defined in conversions.py
            multiplier = 1.0 
            
            if item in conversions_dict:
                # If counted on makeline/cut table, apply the prep fraction. Else, use the storage fraction.
                if "Makeline" in loc or "Cut Table" in loc:
                    multiplier = conversions_dict[item].get("prep_multiplier", 1.0)
                else:
                    multiplier = conversions_dict[item].get("storage_multiplier", 1.0)
            
            if item not in final_totals:
                final_totals[item] = 0.0
            
            final_totals[item] += (count * multiplier)
            
    # Display the final, clean, consolidated totals
    result_df = pd.DataFrame(list(final_totals.items()), columns=["Item", "Total Count"])
    
    # Format the decimals nicely
    result_df['Total Count'] = result_df['Total Count'].apply(lambda x: f"{x:.4f}".rstrip('0').rstrip('.'))
    
    st.dataframe(result_df, hide_index=True, use_container_width=True)