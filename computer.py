import streamlit as st
from computer import compute_ArtName, compute_name, compute_barcode, compute_internal_reference, compute_shape, compute_height, compute_width, compute_depth,compute_ratio
import itertools
import pandas as pd
from io import BytesIO

# Constants
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
    'Package used for delivery': '',
    'ratio': ''
}

dynamic_params = {
    'Subfamily': '',
    'Number of Irises': '',
    'Finishing Effects': '',
    'Background': '',
    'Mount Type': '',
    'Format': '',
}

# Fixed parameters with text input fields
fixed_params = {
    'Family Type': '',
    'Short Family Type': '',
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
    'Is Round': False
}


# Dropdown selectors with choices
Selectors = {
    'Product Category': ['MANUFACTURED FINISHED PRODUCTS', 'RAW MATERIALS', 'FINISHED PRODUCTS'],
    'Product Type': ['Storable Product', 'Consumable', 'Service'],
    'Routes': ['Replenish on Order (MTO)', 'Manufacture'],
    'Unit of Measure': ['Unit(s)', 'Box(es)', 'Pallet(s)', 'Kg(s)', 'm(s)']
}


# Function to generate product variations
def generate_products(fixed_params, dynamic_params):
    # Split dynamic parameters into lists of values
    dynamic_values = {}
    for param, value in dynamic_params.items():
        # Split by commas and strip whitespace, treating '-' as empty
        dynamic_values[param] = [v.strip() if v.strip() != '-' else '' for v in value.split(',')]

    # Generate all combinations of dynamic parameters
    dynamic_combinations = list(itertools.product(*dynamic_values.values()))

    # Prepare the final product list (with the structure of Final_df)
    product_list = []
    inc = 456
    for combo in dynamic_combinations:
        # Start with a copy of Final_df for each product
        product = Final_df.copy()
        
        # Update fixed parameters in the product
        for key, value in fixed_params.items():
            product[key] = value
        
        # Update dynamic parameters in the product
        for i, param in enumerate(dynamic_values.keys()):
            product[param] = combo[i]
        artname = compute_ArtName(product)
        product['Name'] = compute_name(product, artname)
        product['ratio'] = compute_ratio(product)
        product['Short'] = product['Name']
        product['Barcode'] = compute_barcode(product)
        product['Internal Reference'] = compute_internal_reference(product, inc)
        # Increment for internal reference to fix
        inc += 1
        product['Shape'] = compute_shape(product['Format'], product['Number of Irises'], product['Is Round'])
        product['Height (unpacked)'] = compute_height(product)
        product['Width (unpacked)'] = compute_width(product)
        product['Depth (unpacked)'] = compute_depth(product)
        # Add this product variant to the list
        product_list.append(product)

    # Convert the product list to a DataFrame
    df = pd.DataFrame(product_list)
    ## Drop lines where shape = Rectangle and ratio = integer
    df_filtered = df[~((df['Shape'] == 'Rectangle') & (df['ratio'] == df['ratio'].astype(int)))]
    return df


def main():
    st.title("Product Declinations")

    # Section for fixed parameters
    # Divider
    st.markdown("---")
    st.subheader("Fixed Product Parameters")
    # Section for Family Type
    st.subheader("Define the Family Type")

    for key in TextInputs:
        fixed_params[key] = st.text_input(key, value=fixed_params[key])

    # Section for checkboxes
    st.subheader("Production Checkboxes")
    for key in Checkboxes:
        fixed_params[key] = st.checkbox(key, value=Checkboxes[key])

    # Section for dropdown selectors
    st.subheader("Define following selectors")
    selector_values = {}
    for key, options in Selectors.items():
        fixed_params[key] = st.selectbox(key, options)

    # Section for dynamic parameters 
    st.markdown("---")
    st.subheader("Dynamic Product Parameters")
    st.write("To be defined with coma separated values, please add '-' for empty values and if an empty value is needed")
    
    for idx, param in enumerate(dynamic_params.keys()):
        if param == 'Subfamily':
            st.write("Short for Subfamily Type will be computed with its initials")
        if param == 'Format':
            st.write("Format example : '10x20, 20x30, 30x40'")
        dynamic_params[param] = st.text_input(f"{param}", dynamic_params[param], key=f"dynamic_{idx}")

    ## Generate the different product declinations    
    st.markdown("---")
    if st.button("Generate Products"):
        df = generate_products(fixed_params, dynamic_params)
        if not df.empty:
            st.write("Generated Products Data")
            st.dataframe(df)
            download_csv(df)
        else:
            st.warning("No data generated. Please check your inputs.")

def download_csv(df):
    # Create a BytesIO buffer
    output = BytesIO()
    
    # Write the DataFrame to the buffer as a CSV file
    df.to_csv(output, index=False)
    # Set the buffer's position to the start
    output.seek(0)
    # Provide the download button with the CSV file
    st.download_button(
        label="Download as CSV",
        data=output,
        file_name="products.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()
