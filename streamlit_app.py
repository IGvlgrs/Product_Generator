import streamlit as st
import pandas as pd

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

# Define dynamic parameters for product declinations
dynamic_params = {
    'Name': '',
    'Family': '',
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

# Streamlit app
def main():
    st.title("Product Generator for ERP")

    # Create input form for fixed parameters
    st.subheader("Fixed Product Parameters")
    for param in fixed_params.keys():
        fixed_params[param] = st.text_input(f"{param}", fixed_params[param])
    
    # Create input form for dynamic product declinations
    st.subheader("Product Declinations")
    for param in dynamic_params.keys():
        dynamic_params[param] = st.text_input(f"{param}", dynamic_params[param])

    # Create button to generate products
    if st.button("Generate Products"):
        df = generate_products(fixed_params, dynamic_params)
        st.write("Generated Products Data")
        st.dataframe(df)
        
        # Option to download as Excel file
        st.download_button("Download as Excel", df.to_excel(index=False), "products.xlsx", "application/vnd.ms-excel")

# Function to generate product variations
def generate_products(fixed_params, dynamic_params):
    # Create a list of dictionaries with the generated product variations
    product_data = []

    # Example: Simulating multiple combinations (add logic here to create more variations as needed)
    for i in range(5):  # You can change this logic to generate variations as per user input
        product = {**fixed_params, **dynamic_params}
        product['Name'] += f" Variation {i+1}"  # Example: Add variation to name
        product_data.append(product)
    
    # Create DataFrame from product data
    df = pd.DataFrame(product_data)
    return df

if __name__ == "__main__":
    main()
