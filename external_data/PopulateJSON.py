import json
import pandas as pd

# Load the existing bond lengths from the JSON file
with open('C://Documents//Gaussian-2-Blender//external_data//bond_lengths.json', 'r') as json_file:
    bond_lengths = json.load(json_file)

# Load the Excel file
excel_file = 'C://Documents//Gaussian-2-Blender//external_data//bond_lengths.xlsx'

# Define the sheet to bond type mapping
sheet_to_bond_type = {
    'Single.Bonds': 0,
    'Double.Bonds': 1,
    'Triple.Bonds': 2
}

# Iterate over each sheet and update the bond lengths
for sheet_name, bond_type_index in sheet_to_bond_type.items():
    # Load the sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name, index_col=0)
    
    # Iterate over each row and column in the DataFrame
    for index, row in df.iterrows():
        for col in df.columns:
            if not pd.isna(row[col]):
                # Update the JSON data structure
                bond_lengths[index][col][bond_type_index] = row[col]

# Save the updated bond lengths back to the JSON file
with open('bond_lengths.json', 'w') as json_file:
    json.dump(bond_lengths, json_file, indent=4)
