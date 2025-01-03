import bpy
import os
import csv

def clean_docstring(doc):
    if not doc:
        return ""
    doc = doc.split("\n")
    cleaned_doc = [line.strip() for line in doc if line.strip() and not line.startswith("bpy")]
    return " ".join(cleaned_doc)

def save_operator_list():
    output_file_path = "YOUR/FILE/PATH/operator_list.csv" # Put your filepath here

    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Operator', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        op_categories = [attr for attr in dir(bpy.ops) if not attr.startswith("_")]
        for category in op_categories:
            cat_obj = getattr(bpy.ops, category)
            op_names = [op for op in dir(cat_obj) if not op.startswith("_")]
            for op_name in op_names:
                op_func = getattr(cat_obj, op_name)
                doc = op_func.__doc__
                cleaned_description = clean_docstring(doc)
                writer.writerow({'Operator': f"bpy.ops.{category}.{op_name}()", 'Description': cleaned_description})

    print(f"Operator list exported to: {output_file_path}")

save_operator_list()
