import json

# Helper functions

"""
Perform a filtering operation on the provided list of objects, based 
on a single property, using a dictionary of numeric comparisons.

Treats the set of all comparisons as an "and" operation

If 'operations' is a single number, it assumes that the operator is 'eq'
"""
def numeric_filter_objects(items,
                           attr,
                           operations = {}):
    allowed_operators = {"lt", "gt", "le", "ge", "eq", "ne"}
    for item in items:
        if attr not in item.__dict__.keys():
            raise AttributeError("numeric_filter: attr '" + attr + "' not in attributes of given object")
    if type(operations) is int or type(operations) is float:
        operations = {
            "eq": operations
        }
    for operator in operations.keys():
        if operator not in allowed_operators:
            raise ValueError("numeric_filter: operator '" + operator + "' not in list of allowed operators: " + str(allowed_operators))
        if operator == "lt":
            if type(getattr(items[0], attr)) is list:
                subgroup = []
                for item in items:
                    for i in getattr(item, attr):
                        if i < operations["lt"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if getattr(item, attr) < operations["lt"]]
        if operator == "gt":
            if type(getattr(items[0], attr)) is list:
                subgroup = []
                for item in items:
                    for i in getattr(item, attr):
                        if i > operations["gt"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if getattr(item, attr) > operations["gt"]]
        if operator == "le":
            if type(getattr(items[0], attr)) is list:
                subgroup = []
                for item in items:
                    for i in getattr(item, attr):
                        if i <= operations["le"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if getattr(item, attr) <= operations["le"]]
        if operator == "ge":
            if type(getattr(items[0], attr)) is list:
                subgroup = []
                for item in items:
                    for i in getattr(item, attr):
                        if i >= operations["ge"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if getattr(item, attr) >= operations["ge"]]
        if operator == "eq":
            if type(getattr(items[0], attr)) is list:
                subgroup = []
                for item in items:
                    for i in getattr(item, attr):
                        if i == operations["eq"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if getattr(item, attr) == operations["eq"]]
        if operator == "ne":
            if type(getattr(items[0], attr)) is list:
                subgroup = []
                for item in items:
                    for i in getattr(item, attr):
                        if i != operations["ne"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if getattr(item, attr) != operations["ne"]]
    return items

# Write the given character data to the file in path
def write_character(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character.getDict(), f, indent=4)
