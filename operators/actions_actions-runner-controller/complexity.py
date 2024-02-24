import yaml

# Load the YAML file from disk
yaml_file_path = 'fields.yaml'

with open(yaml_file_path, 'r') as file:
    yaml_data = yaml.safe_load(file)

entropy_values = {
    "bool": 1.0,
    "enum": 2.5,
    "string": 1.5,
    "unknown": 1.5,
}


def calculate_entropy(node_type):
    return entropy_values.get(node_type, entropy_values["unknown"])


def calculate_complexity_fixed(node):
    if isinstance(node, dict):
        if "type" in node:
            entropy = calculate_entropy(node["type"])
            if node["type"] == "object" and "properties" in node:
                return entropy + sum(calculate_complexity_fixed(prop) for prop in node["properties"].values())
            elif node["type"] == "array" and "items" in node:
                return entropy + calculate_complexity_fixed(node["items"])
            else:
                return entropy
        else:
            return sum(calculate_complexity_fixed(value) for key, value in node.items() if key != "description")
    elif isinstance(node, str):
        return calculate_entropy(node)
    else:
        return 0


yaml_complexity_dynamic = calculate_complexity_fixed(yaml_data)
print(yaml_complexity_dynamic)
