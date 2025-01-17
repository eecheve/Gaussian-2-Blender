import pandas as pd
import json

# Load the existing bond lengths from the JSON file
with open('C://Documents//Gaussian-2-Blender//external_data//covalent_radii.json', 'r') as json_file:
    bond_lengths = json.load(json_file)

# Load the Excel file
excel_file = pd.read_excel('C://Documents//Gaussian-2-Blender//external_data//covalent_bond_radii.xlsx', 
                           header=0, engine='openpyxl')

# Map the Excel data to the JSON structure
for index, row in excel_file.iterrows():
    element = row['Element']
    single_bond = row['Single']
    double_bond = row['Double']
    triple_bond = row['Triple']
    bond_lengths[element] = [
        single_bond if single_bond != '-' else None,
        double_bond if double_bond != '-' else None,
        triple_bond if triple_bond != '-' else None
    ]

# Save the JSON data to a file
with open('C://Documents//Gaussian-2-Blender//external_data//covalent_radii.json', 'w') as json_file:
    json.dump(bond_lengths, json_file, indent=4)

print("The covalent radii data has been successfully populated and saved to covalent_radii.json.")