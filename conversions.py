# conversions.py

# =====================================================================
# THE BAG MULTIPLIER
# How much of a full case is ONE bag, pouch, or tray?
# =====================================================================
bag_conversions = {
    # --- Original Makeline Meats ---
    "Pepperoni": 0.5,    
    "Sausage": 0.33,
    "Beef": 0.25,
    
    # --- New Prepped / Back-of-House Items ---
    "Garlic Knots": 0.00,          # REPLACE: How much of a case is 1 Tray of Knots?
    "Prepped Ranch (Lexan)": 0.00, # REPLACE: How much of a case is 1 bulk pouch?
    "Prepped Spinach": 0.00,       # REPLACE: How much of a case is 1 bag of spinach?
    "Prepped Mushrooms": 0.00,     # REPLACE: How much of a case is 1 bag/pail?
    "Prepped Black Olives": 0.00,  # REPLACE: How much of a case is 1 pouch?
    "Prepped Pineapple": 0.00,     # REPLACE: How much of a case is 1 pouch?
    "Prepped Pepperoni": 0.5       # Assuming the prepped backup is standard bag weight
}

# =====================================================================
# THE LEXAN MULTIPLIER
# How much of a full case is ONE Lexan?
# =====================================================================
lexan_conversions = {
    # --- Original Makeline Meats ---
    "Pepperoni": 0.25,
    "Sausage": 0.165,
    "Beef": 0.125,
    
    # --- New Prepped / Back-of-House Items ---
    "Garlic Knots": 0.00,          # Leave 0.00 if Knots don't go in Lexans
    "Prepped Ranch (Lexan)": 0.00, # REPLACE: How much of a case is 1 Lexan of Ranch?
    "Prepped Spinach": 0.00,       # REPLACE: How much of a case is 1 Lexan of Spinach?
    "Prepped Mushrooms": 0.00,     # REPLACE: How much of a case is 1 Lexan of Mushrooms?
    "Prepped Black Olives": 0.00,  # REPLACE: How much of a case is 1 Lexan of Olives?
    "Prepped Pineapple": 0.00,     # REPLACE: How much of a case is 1 Lexan of Pineapple?
    "Prepped Pepperoni": 0.25      # Standard Makeline Lexan weight
}

# =====================================================================
# THE CONVERSION ENGINE
# =====================================================================
def calculate_total(item_name, cases, bags, lexans):
    """
    Takes the physical count from the Streamlit UI and applies 
    Jason's specific mathematical yield constants to get total cases.
    """
    
    # Fetch the specific multiplier for the item.
    # If the item isn't in the dictionary (like a box of gloves), it defaults to 0.0
    bag_mult = bag_conversions.get(item_name, 0.0)
    lexan_mult = lexan_conversions.get(item_name, 0.0)
    
    # The Master Equation: Cases + (Bags * Bag_Multiplier) + (Lexans * Lexan_Multiplier)
    total = cases + (bags * bag_mult) + (lexans * lexan_mult)
    
    # Round to 2 decimal places to match the corporate software requirements
    return round(total, 2)
