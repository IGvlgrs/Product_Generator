Customer_Lead_Time = 21

Final_df = {
    'Name': '',
    'Internal Reference': '',
    'Product Type': '',
    'Can Be Sold': '',
    'Can Be Purchased': '',
    'Custmer Lead Time': Customer_Lead_Time,
    'Depth (unpacked)': '',
    'Width (unpacked)': '',
    'Height (unpacked)': '',
    'Weight unit of measurment': 'KG',
    'Weight (unpacked)': '',
    'Product Category': '',
    'Short': '',
    'Mount Type': '',
    'Background': 'Black',
    'Shape': '',
    'Effect': '',
    'Is Round': '',
    'Unit of Measure': '',
    'Routes': '',
    'Family': '',
    'Subfamily': '',
    'Format': '',
    'Finishing Effects': '',
    'Number of Irises': '',
    'Barcode': '',
    'Production WW': '',
    'Production OTHERS': '',
    'Production at IGP': '',
    'Height (packed)': '',
    'Width (packed)': '',
    'Depth (packed)': '',
    'Weight (packed)': '',
    'HS Code': '',
    'Package used for delivery': ''
}


# Fixed parameters with text input fields
fixed_params = {
    'Family Name': '',
    'Family Short Name': '',
    'Can Be Sold': '',
    'Can Be Purchased': '',
    'Product Type': '',
    'Production WW': '',
    'Production OTHERS': '',
    'Production at IGP': '',
    'Customer Lead Time': Customer_Lead_Time,
    'HS Code': '',
    'Product Category': '',
    'Product Type': '',
    'Routes': '',
    'Unit of Measure': ''
}

# Text input fields for static parameters
TextInputs = {
        'Family Type': '',
        'Short Family Type': ''
}

# Checkboxes for boolean inputs
Checkboxes = {
    'Can Be Sold': False,
    'Can Be Purchased': False,
    'Production at IGP': False,
    'Production WW': False,
    'Production OTHERS': False,
}


# Dropdown selectors with choices
Selectors = {
    'Product Category': ['MANUFACTURED FINISHED PRODUCTS', 'RAW MATERIALS', 'FINISHED PRODUCTS'],
    'Product Type': ['Storable Product', 'Consumable', 'Service'],
    'Routes': ['Replenish on Order (MTO)', 'Manufacture'],
    'Unit of Measure': ['Unit(s)', 'Box(es)', 'Pallet(s)', 'Kg(s)', 'm(s)']
}
