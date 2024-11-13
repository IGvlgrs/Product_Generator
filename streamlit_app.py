import streamlit as st
import itertools
import pandas as pd
from io import BytesIO
from data import fixed_params, TextInputs, Checkboxes, Selectors

class Family:
    def __init__(self, fixed_params):
        self.name = fixed_params['Family Name']
        self.fixed_params = fixed_params
        self.subfamilies = []
        self.short=fixed_params['Family Short Name']

    def __repr__(self):
        return f"Family({self.fixed_params}, {self.subfamilies})"

    def add_subfamily(self, subfamily):
        self.subfamilies.append(subfamily)


class Subfamily:
    def __init__(self, subfamily_name):
        self.name = subfamily_name
        self.short = ''.join([word[0] for word in subfamily_name.split()])
        self.subfamily_params = {
        'Shapes': '',
        'Mount Type': '',
        'Background': '',
        'Finishing Effects': '',
        'Effects': ''
        }
        self.inc = 0
        self.shapes = []
    def __repr__(self):
        return f"Subfamily({self.name}, {self.subfamily_params})"
    def add_shape(self, shape):
        self.shapes.append(shape)

class Shapes:
    def __init__(self, shape_name):
        self.name = shape_name
        self.short = ''.join([word[0] for word in shape_name.split()])
        self.shape_params = {
        'Number of Irises': '',
        'Is Round': False
        }
        self.number_of_irises = []
    def __repr__(self):
        return f"Shapes({self.name}, {self.shape_params})"

    def add_number_of_irises(self, number_of_irises):
        self.number_of_irises.append(number_of_irises)


class Number_of_Irises(Shapes):
    def __init__(self, number_of_irises):
        self.name = number_of_irises
        self.number_of_irises_params = {
        'Formats': ''
        }
    def __repr__(self):
        return f"Number_of_Irises({self.name}, {self.number_of_irises_params})"


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
    'Background': '',
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
}


# Text input fields for static parameters
TextInputs = {
        'Family Name': '',
        'Family Short Name': '',
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
    'Routes': ['Replenish on Order (MTO), Manufacture'],
    'Unit of Measure': ['Unit(s)', 'Box(es)', 'Pallet(s)', 'Kg(s)', 'm(s)']
}

def display_subfamilies(sublist, family):
    # Iterate through the subfamily list provided
    st.write("Below is a list of dynamic parameters for this subfamily, please enter all possibilities separated by a comma. If no information is required or one of the option is not to have any value, please put a dash -")
    st.write("For each shape provided, a new section will be displayed on the website to enter specific parameters for this shape.")
    for sub in sublist:
        sub = Subfamily(sub)  # Initialize the subfamily object
        family.add_subfamily(sub)
        st.subheader(sub.name)
        st.write(f"Short for {sub.name}: {sub.short}")
        sub.inc = st.number_input(f"{sub.name} - Increment for internal reference", value=0, key=f"subfamily_textinput_{sub.name}_internal_reference")
        # Iterate through the subfamily parameters
        for key in sub.subfamily_params:
            sub.subfamily_params[key] = st.text_input(f"{sub.name} - {key}", value=sub.subfamily_params.get(key, ""), key=f"subfamily_textinput_{sub.name}_{key}")
            # If shapes are provided, process them (without recreating the shape in every loop)
        if sub.subfamily_params['Shapes']:
            shape_list = sub.subfamily_params['Shapes'].split(',')  # Split shape input into a list
            display_shapes(shape_list,sub)  # Pass the list of shapes for further processing

def display_shapes(shape_list,sub):
    # Iterate through the shape list provided
    st.write("Below is a list of dynamic parameters for this shape, please enter all possibilities separated by a comma. If no information is required or one of the option is not to have any value, please put a dash -")
    st.write("For each number of irises provided, a new section will be displayed on the website to enter specific parameters for this number of irises.")
    for shape_name in shape_list:
        shape = Shapes(shape_name)  # Initialize the shape object
        sub.add_shape(shape)
        st.subheader(shape.name)
        st.write(f"Short for {shape.name}: {shape.short}")

        # Iterate through the shape parameters
        for key in shape.shape_params:
            if key == 'Is Round':
                shape.shape_params[key] = st.checkbox(f"{sub.name}-{shape.name} - {key}", value=shape.shape_params.get(key, ""), key=f"shape_checkbox_{shape.name}_{key}{sub.name}")
            else:
                shape.shape_params[key] = st.text_input(f"{sub.name}-{shape.name} - {key}", value=shape.shape_params.get(key, ""), key=f"shape_textinput_{shape.name}_{key}{sub.name}")
            # If number of irises are provided, process them
        if shape.shape_params['Number of Irises']:
            iris_list = shape.shape_params['Number of Irises'].split(',')
            display_number_of_irises(iris_list, shape, sub)

def display_number_of_irises(nbiris_list,shape,sub):
    # Iterate through the list of irises provided
    st.write("Supported format types for products are for example 10x10, 20x120, 23 (diameter), 10x10x10 (cube), 10x10x20 (block), please provide 'height'x'width'x'depth' in priority")
    for nbiris_name in nbiris_list:
        nbiris = Number_of_Irises(nbiris_name)  # Initialize the iris object
        shape.add_number_of_irises(nbiris)
        st.subheader(nbiris.name)

        # Iterate through iris-specific parameters
        for key in nbiris.number_of_irises_params:
            nbiris.number_of_irises_params[key] = st.text_input(f"{sub.name} {shape.name}-{nbiris.name} - {key}", value=nbiris.number_of_irises_params.get(key, ""), key=f"nbiris_textinput_{nbiris.name}_{key}{shape.name}{sub.name}")

def generate_products(families):
    products = []

    # Iterate through each family
    for family in families:
        # Iterate through each subfamily in the family
        for subfamily in family.subfamilies:
            # Split subfamily_params that have comma-separated values into lists
            param_combinations = prepare_subfamily_combinations(subfamily)

            # Iterate through each shape in the subfamily
            for shape in subfamily.shapes:
                # If the shape has irises, we don't need to iterate over shapes separately again.
                if shape.shape_params['Number of Irises']:
                    for iris in shape.number_of_irises:
                        # Handle comma-separated formats for each iris
                        if iris.number_of_irises_params['Formats']:
                            formats = iris.number_of_irises_params['Formats'].split(',')
                            for format_value in formats:
                                for sub_param_combination in param_combinations:
                                    product = create_product_row(family, subfamily, shape, iris, format_value, sub_param_combination)
                                    products.append(product)
                        else:
                            # If no formats, create product for each iris
                            for sub_param_combination in param_combinations:
                                product = create_product_row(family, subfamily, shape, iris, None, sub_param_combination)
                                products.append(product)
                else:
                    # If no irises, we generate products based on the subfamily and shape params
                    for sub_param_combination in param_combinations:
                        product = create_product_row(family, subfamily, shape, None, None, sub_param_combination)
                        products.append(product)

    # Convert list of products to DataFrame
    df = pd.DataFrame(products)
    return df

def prepare_subfamily_combinations(subfamily):
    # Prepare lists for subfamily params, handling both unique values and comma-separated lists
    subfamily_param_lists = {}

    for key, value in subfamily.subfamily_params.items():
        # If the parameter contains commas, treat it as a list
        if ',' in value:
            subfamily_param_lists[key] = [item.strip() for item in value.split(',')]
        else:
            # If it's a unique value, treat it as a list with one entry
            subfamily_param_lists[key] = [value.strip()]

    # Generate all possible combinations of these parameters
    keys = list(subfamily_param_lists.keys())
    values = list(subfamily_param_lists.values())

    # Use itertools.product to generate combinations
    param_combinations = [dict(zip(keys, combination)) for combination in itertools.product(*values)]

    return param_combinations

def create_product_row(family, subfamily, shape, iris, format_value, sub_param_combination):
    # Initialize a product row using the Final_df template
    product = Final_df.copy()

    # Populate family-specific fields
    product['Family'] = family.fixed_params.get('Family Type', '').upper().strip()
    product['Product Type'] = family.fixed_params.get('Product Type', '').upper().strip()
    product['Can Be Sold'] = family.fixed_params.get('Can Be Sold', False)
    product['Can Be Purchased'] = family.fixed_params.get('Can Be Purchased', False)
    product['Production WW'] = family.fixed_params.get('Production WW', False)
    product['Production OTHERS'] = family.fixed_params.get('Production OTHERS', False)
    product['Production at IGP'] = family.fixed_params.get('Production at IGP', False)
    product['HS Code'] = family.fixed_params.get('HS Code', '').upper().strip()
    product['Product Category'] = family.fixed_params.get('Product Category', '').upper().strip()
    product['Routes'] = family.fixed_params.get('Routes', '').upper().strip()
    product['Unit of Measure'] = family.fixed_params.get('Unit of Measure', '').upper().strip()

    # Populate subfamily-specific fields
    product['Subfamily'] = subfamily.name.upper()
    product.update({k: v.upper().strip() if isinstance(v, str) else v for k, v in sub_param_combination.items()})

    # Populate shape-specific fields
    product['Shape'] = shape.name.upper()
    product.update({k: v.upper().strip() if isinstance(v, str) else v for k, v in shape.shape_params.items()})
    product['Is Round'] = shape.shape_params['Is Round']
    product['Format'] = format_value if format_value else ''
    product['Family'] = family.name.upper()

    # Populate number of irises-specific fields (if available)
    if iris:
        product['Number of Irises'] = iris.name.upper()
        product.update({k: v.upper().strip() if isinstance(v, str) else v for k, v in iris.number_of_irises_params.items()})

    # Remove 'Formats' from the product (drop it if exists)
    product.pop('Formats', None)
    product.pop('HS Code', None)
    product.pop('Effect', None)
    #Compute Height, Width, Depth, Weight
    product['Height (unpacked)'] = compute_height(product, format_value)
    product['Width (unpacked)'] = compute_width(product, format_value)
    product['Depth (unpacked)'] = compute_depth(product, format_value)

    # Optionally compute other fields, such as Barcode, Internal Reference, and Ratio
    product['Barcode'] = compute_barcode(product, format_value)
    inc=0
    product['Internal Reference'] = compute_internal_reference(family, subfamily, shape, iris, format_value,inc)
    product['Name'] = compute_ArtName(product, format_value)

    return product

def compute_height(product, format_value):
    if 'x' in format_value:
        return int(format_value.split('x')[0])
    else:
        return format_value

def compute_width(product, format_value):
    if 'x' in format_value:
        return int(format_value.split('x')[1])
    else:
        return format_value

def compute_depth(product, format_value):
    if 'x' in format_value:
        return int(format_value.split('x')[2])
    else:
        return 0.5

# Example utility functions for computing values
def compute_barcode(product, format_value):
    initals_mount_type = ''.join([word[0] for word in product['Mount Type'].split()])
    initals_finishing_effects = ''.join([word[0] for word in product['Finishing Effects'].split()])
    first2letters_effect = product['Effects'].strip()[:2]
    first2letters_background = product['Background'].strip()[:2]
    initals_shape = ''.join([word[0] for word in product['Shape'].split()])
    initials_subfamily = ''.join([word[0] for word in product['Subfamily'].split()])
    ret = f"{initials_subfamily}{product['Number of Irises']}-{format_value}-{initals_shape}-{first2letters_background}{initals_mount_type}-{first2letters_effect}"
    return ret

def compute_internal_reference(family, subfamily, shape, iris, format_value,inc):
    short_family = family.short
    subfamily.inc += 1
    return f"{short_family}{subfamily.short}-0000{subfamily.inc}"

def compute_ArtName(product, format_value):
    initials_subfamily = ''.join([word[0] for word in product['Subfamily'].split()])
    return f"{initials_subfamily} {product['Shape']} {product['Number of Irises']} {product['Format']} {product['Background']} WITH {product['Mount Type']} {product['Effects']}"

def main():
    st.title("Product Declinations")
    st.markdown("This tool is designed to create the product Excel sheet currently in use to launch new products. Some production information will be required on the first section of this tool.")
    st.markdown("---")

    # Section for fixed parameters
    st.subheader("Production Parameters")

    # Section for Family Type
    st.subheader("Define the Family Name")
    for key in TextInputs:
        fixed_params[key] = st.text_input(key, value=TextInputs.get(key, ""), key=f"family_textinput_{key}")

    # Section for checkboxes
    st.subheader("Production Checkboxes")
    for key in Checkboxes:
        fixed_params[key] = st.checkbox(key, value=Checkboxes.get(key, False), key=f"family_checkbox_{key}")

    # Section for dropdown selectors
    st.subheader("Define following selectors")
    for key, options in Selectors.items():
        fixed_params[key] = st.selectbox(key, options, key=f"family_selectbox_{key}")

    family = Family(fixed_params)
    # Section for dynaomic parameters (subfamilies and shapes)
    st.text("Please enter the list of subfamilies you want to generate separated by a coma")
    subfamilies = st.text_input("Subfamilies (comma-separated)")
    if subfamilies:
        subfamily_list = [subfamily.strip() for subfamily in subfamilies.split(',') if subfamily.strip()]  # Clean and split subfamilies input
        display_subfamilies(subfamily_list, family)
    else:
        st.warning("Please enter subfamilies separated by commas.")

    st.markdown("---")
    if st.button("Generate Products"):
        df = generate_products([family])
        if not df.empty:
            st.write("Generated Products Data")
            st.dataframe(df)
            download_csv(df)
        else:
            st.warning("No data generated. Please check your inputs.")

# Assuming Subfamily and Shapes classes are properly defined elsewhere in your code.
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
