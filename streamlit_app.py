import streamlit as st
import pandas as pd
import itertools
from io import BytesIO

# Define fixed parameters
fixed_params = {
    'Product Type': '',
    'Can be Sold': '',
    'Can be Purchased': '',
    'Product Category': '',
    'Weight unit of measure label': '',
    'Background': '',
    'Routes': '',
    'Purchase UoM': '',
    'Family': '',
    'Subfamily': '',
    'Production WW': '',
    'Production OTHERS': ''
}

# Define dynamic parameters for product declinations (removed 'Family')
dynamic_params = {
    'Name': '',
    'Number of Irises': '',
    'Finishing Effects': '',
    'Shape': '',
    'Depth (unpacked)': '',
    'Width (unpacked)': '',
    'Barcode': '',
    'Width': '',
    'Depth': '',
    'Weight': '',
    'HS Code': ''
}

# Desired output order for the final table and CSV
output_column_order = [
    'Product Type', 'Can be Sold', 'Can be Purchased', 'Product Category',
    'Weight unit of measure label', 'Background', 'Routes', 'Purchase UoM',
    'Family', 'Subfamily', 'Production WW', 'Production OTHERS',
    'Name', 'Number of Irises', 'Finishing Effects', 'Shape', 
    'Depth (unpacked)', 'Width (unpacked)', 'Barcode', 'Width', 
    'Depth', 'Weight', 'HS Code'
]

# Streamlit app
def main():
    st.title("Product Generator for ERP")

    # Create input form for fixed parameters
    st.subheader("Fixed Product Parameters")
    for idx, param in enumerate(fixed_params.keys()):
        fixed_params[param] = st.text_input(f"{param}", fixed_params[param], key=f"fixed_{idx}")
    
    # Create input form for dynamic product declinations (without 'Family')
    st.subheader("Product Declinations (Use comma to separate multiple variations)")
    for idx, param in enumerate(dynamic_params.keys()):
        dynamic_params[param] = st.text_input(f"{param}", dynamic_params[param], key=f"dynamic_{idx}")

    # Create button to generate products
    if st.button("Generate Products"):
        df = generate_products(fixed_params, dynamic_params)
        
        # Display the generated DataFrame
        if not df.empty:
            st.write("Generated Products Data")
            st.dataframe(df)

            # Provide download button after displaying the DataFrame
            download_csv(df)
        else:
            st.warning("No data generated. Please check your inputs.")

# Function to generate product variations
def generate_products(fixed_params, dynamic_params):
    # Create a list of dynamic parameters with variations
    dynamic_variations = {}
    
    # Split each input by commas to get multiple values
    for param, value in dynamic_params.items():
        dynamic_variations[param] = [v.strip() for v in value.split(",") if v.strip()]

    # Generate all possible combinations of dynamic parameters using itertools.product
    if dynamic_variations:
        dynamic_combinations = list(itertools.product(*dynamic_variations.values()))
    else:
        dynamic_combinations = []

    product_data = []
    
    # Create a dictionary for each product combination with fixed and dynamic parameters
    for combination in dynamic_combinations:
        product = {**fixed_params}
        for idx, param in enumerate(dynamic_variations.keys()):
            product[param] = combination[idx]
        product_data.append(product)
    
    # Create DataFrame from product data
    df = pd.DataFrame(product_data)

    # Reorder the DataFrame columns to match the desired output order
    df = df[output_column_order]
    
    return df

# Function to handle CSV export
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
