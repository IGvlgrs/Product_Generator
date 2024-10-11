import pandas as pd

def compute_name(row, artname):
    return f"{row['Short Family Type']} {row['Format']} {artname} {row['Mount Type']} {row['Finishing Effects']} {row['Background']}"

def short_subfamily_type(subfam):
    subfam = subfam.split(' ')
    return ''.join([part[0].upper() for part in subfam])

def compute_ArtName(row):
    if row['Number of Irises'] == '1':
        return "SOLO"
    elif row['Number of Irises'] == '2':
        return "DUO"
    elif row['Number of Irises'] == '3':
        return "TRIO"
    elif row['Number of Irises'] == '4':
        return "QUATUOR"
    elif row['Number of Irises'] == '5':
        return "QUINTUOR"
    elif row['Number of Irises'] == '6':
        return "SEXTUOR"
    else:
        return "-"

def compute_depth(row):
    if row['Mount Type'] != '':
        return 2.5
    else:
        return 2.5

def compute_height(row):
    form = row['Format'].split('x')
    if row['Shape'] == "Round":
        return form[0]
    elif row['Shape'] == 'Square':
        return form[0]
    elif row['Shape'] == 'Rectangle':
        return min(form)
    elif row['Shape'] == 'Ligne':
        return max(form)
    else:
        return '-'

def compute_width(row):
    form = row['Format'].split('x')
    if row['Shape'] == 'Round':
        return form[0]
    elif row['Shape'] == 'Square':
        return form[0]
    elif row['Shape'] == 'Rectangle':
        return max(form)
    elif row['Shape'] == 'Ligne':
        return min(form)
    else:
        return '-'

def compute_barcode(row):
    return f"{row['Short Family Type']}{row['Number of Irises']}-{row['Format']}-MN"

def compute_internal_reference(row, inc):
    Shortsub = short_subfamily_type(row['Subfamily'])
    return f"{row['Short Family Type']}{Shortsub}-0000{inc}"

def compute_ratio(row):
    form = [int(x) for x in row['Format'].split('x')]
    return max(form) / min(form)

def compute_shape(size, nbiris, is_round):
    if "x" not in size:
        return "Round"
    dimensions = [int(x) for x in size.split('x')]
    ratio = max(dimensions[0],dimensions[1]) / min(dimensions[0],dimensions[1])
    if ratio == 1:
        return "Square"
    elif ratio == int(nbiris):
        return "Ligne"
    else:
        return "Rectangle"
#### Compute function to code : Name, Depth, Width, Height, Weight, Short, Volume, Barcode, Internal Reference, Shape
