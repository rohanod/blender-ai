import bpy
import os

def clean_docstring(doc):
    if not doc:
        return ""
    doc = doc.split("\n")
    cleaned_doc = [line.strip() for line in doc if line.strip() and not line.startswith("bpy")]
    return " ".join(cleaned_doc)

def save_operator_list():
    output_file_path = os.getenv('OUTPUT_FILE_PATH')

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write("For each request, you **must** generate a complete Python script that adheres to the following two-step process:\n\n")
        outfile.write("**Step 1: Scene Preparation**\n\n")
        outfile.write("* Begin by deleting all objects in the current Blender scene.\n")
        outfile.write('* **Crucially**, ensure that any object named "placeholder" is **not** deleted.\n\n')
        outfile.write("**Step 2: Scene Recreation**\n\n")
        outfile.write("* After the scene is cleared (excluding \"placeholder\"), fully recreate the requested scene or action from scratch using Blender 4.3 Python operators.\n")
        outfile.write("* Ensure that the script incorporates all previous requests and the new requests provided by the user.\n\n")
        outfile.write("**Output Requirements:**\n\n")
        outfile.write("* Under absolutely no circumstances should you output anything other than the raw Python code.\n")
        outfile.write("* Do not include any explanatory text, conversational elements, or any content that is not directly part of the Python script.\n")
        outfile.write("* If a request cannot be fulfilled with a valid Blender 4.3 Python operator, return an empty script.\n\n")
        outfile.write("**Reference Material:**\n\n")
        outfile.write("The following is a list of `bpy` operators for Blender 4.3. Use this to ensure the generated code is accurate and up-to-date:\n\n")
        
        op_categories = [attr for attr in dir(bpy.ops) if not attr.startswith("_")]
        for category in op_categories:
            cat_obj = getattr(bpy.ops, category)
            op_names = [op for op in dir(cat_obj) if not op.startswith("_")]
            for op_name in op_names:
                op_func = getattr(cat_obj, op_name)
                doc = op_func.__doc__
                cleaned_description = clean_docstring(doc)
                outfile.write(f"- `bpy.ops.{category}.{op_name}()`: {cleaned_description}\n\n")

    print(f"Operator list exported to: {output_file_path}")

save_operator_list()
