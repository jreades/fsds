import os 
import shutil

render_dir = "_answers"

print(f"Tidying up {render_dir}")
for root, dirs, files in os.walk(render_dir):
    for filename in files:
        print(f"File: {filename}", end=" ")
        if not (filename.startswith("Practical-") and filename.startswith(".pdf")): 
            print("x removed")
            os.remove(os.path.join(root, filename))
        else:
            print("- retained")
    for dirname in dirs:
        print(f"Dir: {dirname}", end=" ")
        if not (dirname == 'practicals'):
            os.remove(os.path.join(root, filename))
        else:
            print("- retained")
