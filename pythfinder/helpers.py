import json

# Helper functions

# Remove duplicate dictionaries from a list of dictionaries, using 
# "uuid" as a primary key (assumes anything with the same uuid is 
# identical)
def remove_duplicates_by_id(l):
    # Get unique uuids
    item_uuids = list(set([i["uuid"] for i in l]))
    out = []
    for uuid in item_uuids:
        for item in l:
            if item["uuid"] == uuid:
                out.append(item)
                break
    return out

# Remove duplicate dictionaries from a list of dictionaries, using 
# "name" as a primary key (assumes anything with the same name is 
# identical)
def remove_duplicates_by_name(l):
    # Get unique names
    item_names = list(set([i["name"] for i in l]))
    out = []
    for name in item_names:
        for item in l:
            if item["name"] == name:
                out.append(item)
                break
    return out

# Perform a filtering operation on the provided list of dictionaries, 
# based on a single property, using a dictionary of numeric comparisons.
#
# Treats the set of all comparisons as an "and" operation
#
# If 'operations' is a single number, it assumes that the operator is 
# 'eq'
def numeric_filter(items,
                   key,
                   operations = {}):
    allowed_operators = ("lt", "gt", "le", "ge", "eq", "ne")
    for item in items:
        if key not in item.keys():
            raise KeyError("numeric_filter: key '" + key + "' not in keys of given item")
    if type(operations) is int or type(operations) is float:
        operations = {
            "eq": operations
        }
    for operator in operations.keys():
        if operator not in allowed_operators:
            raise ValueError("numeric_filter: operator '" + operator + "' not in list of allowed operators: " + str(allowed_operators))
        if operator == "lt":
            if type(items[0][key]) is list:
                subgroup = []
                for item in items:
                    for i in item[key]:
                        if i < operations["lt"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if item[key] < operations["lt"]]
        if operator == "gt":
            if type(items[0][key]) is list:
                subgroup = []
                for item in items:
                    for i in item[key]:
                        if i > operations["gt"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if item[key] > operations["gt"]]
        if operator == "le":
            if type(items[0][key]) is list:
                subgroup = []
                for item in items:
                    for i in item[key]:
                        if i <= operations["le"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if item[key] <= operations["le"]]
        if operator == "ge":
            if type(items[0][key]) is list:
                subgroup = []
                for item in items:
                    for i in item[key]:
                        if i >= operations["ge"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if item[key] >= operations["ge"]]
        if operator == "eq":
            if type(items[0][key]) is list:
                subgroup = []
                for item in items:
                    for i in item[key]:
                        if i == operations["eq"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if item[key] == operations["eq"]]
        if operator == "ne":
            if type(items[0][key]) is list:
                subgroup = []
                for item in items:
                    for i in item[key]:
                        if i != operations["ne"]:
                            subgroup.append(item)
                            break
                items = subgroup
            else:
                items = [item for item in items if item[key] != operations["ne"]]
    return items

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
def writeCharacter(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character.getDict(), f, indent=4)
