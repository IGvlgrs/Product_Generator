import streamlit as st
import pandas as pd
import itertools
from io import BytesIO

# Define fixed parameters
fixed_params = {
    'Material': '',
    'Short Material': '',
    'Can Be Sold': '',
    'Can Be Purchased': '',
    'Product Type': '',
    'Product Category': '',
    'Weight unit of measure label': '',
    'Is Round': '',
    'Routes': '',
    'Purchase UoM': '',
    'Family': '',
    'Subfamily': '',
    'Production WW': '',
    'Production OTHERS': '',
    'Customer Lead Time': '',
    'HS Code': '',
}

# Define dynamic parameters for product declinations (added 'Size')
dynamic_params = {
    'Number of Irises': '',
    'Finishing Effects': '',
    'Background': '',
    'Shape': '',  # This will be computed based on the size
    'Sizes': '',  # Size format: 10x10, 20x20, 30x30, 20x30
}

Cans = ['Can Be Sold', 'Can Be Purchased']
true_false = ['True', 'False']

Checkbox = ['Is Round']

# Compute the name of the product based on material and size
def compute_name(fixed_params, dynamic_params):
    return f"{fixed_params['Material']} {fixed_params['Short Material']} {dynamic_params.get('Sizes', '')}"

# Compute the barcode of the product based on various fields
def compute_barcode(row):
    return f"{row['Material']}{row['Short Material']}{row['Sizes']}{row['Finishing Effects']}{row['Number of Irises']}"

# Compute the internal reference
def compute_internal_reference(row):
    return f"{row['Material']}{row['Short Material']}{row['Sizes']}{row['Finishing Effects']}{row['Number of Irises']}"

# Function to compute shape automatically based on the size and whether it's round
def compute_shape(size, is_round):
    if is_round:
        return "Round"
    dimensions = [int(dim) for dim in size.split('x')]
    if len(dimensions) == 2:
        if dimensions[0] == dimensions[1]:
            return "Square"
        else:
            return "Rectangle"
    return "Unknown"

# Streamlit app
def main():
    st.title("Product Generator for ERP")
    
    # Create input form for fixed parameters
    st.subheader("Fixed Product Parameters")
    for idx, param in enumerate(fixed_params.keys()):
        if param in Cans:
            fixed_params[param] = st.selectbox(f"{param}", true_false, key=f"fixed_{idx}")
        elif param in Checkbox:
            fixed_params[param] = st.checkbox(f"{param}", key=f"fixed_{idx}")
        else:
            fixed_params[param] = st.text_input(f"{param}", fixed_params[param], key=f"fixed_{idx}")

    # Create input form for dynamic product declinations (including 'Size')
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

        # Compute the name using both fixed and dynamic parameters
        product['Name'] = compute_name(fixed_params, product)

        # Compute the barcode and internal reference
        product['Barcode'] = compute_barcode(product)
        product['Internal Reference'] = compute_internal_reference(product)

        # Compute the shape based on the size and whether it's round
        product['Shape'] = compute_shape(product['Sizes'], fixed_params['Is Round'])

        product_data.append(product)

    # Create DataFrame from product data
    df = pd.DataFrame(product_data)

    # Reorder the DataFrame columns to match the desired output order
    df = df[['Product Type', 'Can Be Sold', 'Can Be Purchased', 'Product Category',
             'Weight unit of measure label','Sizes', 'Background', 'Routes', 'Purchase UoM',
             'Family', 'Subfamily', 'Production WW', 'Production OTHERS',
             'Name', 'Number of Irises', 'Finishing Effects', 'Shape',
             'Barcode', 'HS Code']]

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

