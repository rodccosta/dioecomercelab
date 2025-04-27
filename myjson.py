import json

def load_json_file():    
    with open('products.json') as f:
        products = json.load(f)
    return products

def write_json_file(products):
    # the json file where the output must be stored
    out_file = open("products.json", "w")
    json.dump(products, out_file, indent = 6)
    out_file.close()
