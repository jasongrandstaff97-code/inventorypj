import streamlit as st
import pandas as pd

# --- ARCHITECT'S MASTER DATA ---
# Units: 1.0 = Case/Bag, 0.25 = Lexan (for 1:4 items), 0.5 = Lexan (for 1:2 items)

def get_master_data():
    return {
        "Walk-In": [
            {"item": "Alfredo Sauce", "type": "bulk"},
            {"item": "Bulk Ranch", "type": "bulk"},
            {"item": "String Cheese", "type": "lexan", "mult": 0.25},
            {"item": "Extreme Cheese", "type": "queso_lexan", "mult": 0.5},
            {"item": "Beef", "type": "bulk"},
            {"item": "Philly Steak", "type": "bulk"},
            {"item": "Chicken (Grilled/Roasted)", "type": "bulk"},
            {"item": "Wings (Boneless/Roasted)", "type": "bulk"},
            {"item": "Cheese (3-Blend/2-Cheese)", "type": "bulk"}
        ],
        "Prep Rack": [
            {"item": "Pepperoni", "type": "lexan", "mult": 0.25},
            {"item": "Beef", "type": "lexan", "mult": 0.5},
            {"item": "Sausage / Italian Sausage", "type": "lexan", "mult": 0.5},
            {"item": "Veg (GP/Onion/Mush/Spin/Tom)", "type": "lexan", "mult": 0.5},
            {"item": "Black Olives / Pineapple", "type": "lexan", "mult": 1.0},
            {"item": "Sauces (Buffalo/BBQ/Truffle)", "type": "lexan", "mult": 1.0}
        ]
    }
    def get_extended_data():
    return {
        "Make Line": [
            {"item": "String Cheese", "type": "lexan", "mult": 0.25},
            {"item": "7-inch Sandwich Bread", "type": "lexan", "mult": 1.0},
            {"item": "American Cheese Slice", "type": "indiv_unit"},
            {"item": "Bottled Sauces (Ranch/Truffle/Alfredo)", "type": "lexan", "mult": 1.0},
            {"item": "Proteins (All)", "type": "lexan", "mult": 0.5},
            {"item": "Veg (All)", "type": "lexan", "mult": 0.5}
        ],
        "Cut Table": [
            {"item": "Garlic Sauce Cups", "type": "indiv_unit", "case_qty": 100},
            {"item": "Spicy Garlic Cups", "type": "indiv_unit", "case_qty": 100},
            {"item": "Ranch Cups", "type": "indiv_unit", "case_qty": 100},
            {"item": "Foil / Sleeves / Napkins", "type": "loose_case"}
        ],
        "Dough Station": [
            {"item": "Small Dough", "type": "indiv_unit"},
            {"item": "Medium Dough", "type": "indiv_unit"},
            {"item": "Large Dough", "type": "indiv_unit"},
            {"item": "Thin Crust / Gluten Free", "type": "bulk"}
        ]
    }
    # --- UI SETUP ---
st.set_page_config(page_title="Inventory Engine v2", layout="centered")
st.title("📦 Inventory Count Engine")
st.caption("Systems Architect Mode: Logic Over Syntax")

if 'counts' not in st.session_state:
    st.session_state.counts = {}

all_data = {**get_master_data(), **get_extended_data()}
section = st.sidebar.radio("Navigate Section", list(all_data.keys()))

st.header(f"📍 {section}")
def render_item(item_data):
    name = item_data['item']
    it_type = item_data['type']
    
    st.subheader(name)
    c1, c2 = st.columns(2)
    
    if it_type == "lexan":
        val = c1.number_input("Lexan Count", key=f"lex_{name}", step=1.0)
        total = val * item_data['mult']
        c2.metric("Total Bags/Cases", f"{total:.2f}")
        return total

    elif it_type == "indiv_unit":
        units = c1.number_input("Loose Units", key=f"unit_{name}", step=1)
        cases = c2.number_input("Full Cases", key=f"case_{name}", step=1)
        qty = item_data.get('case_qty', 1)
        total = (cases * qty) + units
        st.info(f"Total Count: {total}")
        return total
            elif it_type == "bulk" or it_type == "loose_case":
        total = c1.number_input("Total Case/Bag Count", key=f"bulk_{name}", step=1.0)
        return total
        
    elif it_type == "queso_lexan":
        queso = c1.number_input("Queso Pouch/Case", key=f"q_{name}", step=1.0)
        lexans = c2.number_input("Lexans", key=f"ql_{name}", step=1.0)
        total = queso + (lexans * item_data['mult'])
        st.info(f"Combined Total: {total:.2f}")
        return total

# Run the render loop for the current section
section_items = all_data[section]
for item in section_items:
    st.session_state.counts[item['item']] = render_item(item)
    st.divider()
# --- EXPORT LOGIC ---
st.sidebar.divider()
if st.sidebar.button("💾 Finalize Inventory"):
    st.balloons()
    summary_df = pd.DataFrame(
        [(k, v) for k, v in st.session_state.counts.items()],
        columns=["Item", "Final Count"]
    )
    
    st.write("### Final Shift Summary")
    st.dataframe(summary_df, use_container_width=True)
    
    csv = summary_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV for Store Records",
        data=csv,
        file_name="papa_johns_inventory.csv",
        mime="text/csv",
)
