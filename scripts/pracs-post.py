import os 
import shutil

render_dir = "_answers"

print(f"Tidying up {render_dir}")
for root, dirs, files in os.walk(render_dir):
    for filename in files:
        print(f"File: {filename}", end=" ")
        if not (filename.startswith("Practical-") and (filename.endswith(".pdf") or filename.endswith(".ipynb"))): 
            try:
                os.remove(os.path.join(root, filename))
                print("x removed")
            except FileNotFoundError:
                print(f"! unable to remove {dirname}")
        else:
            os.rename(os.path.join(root, filename), os.path.join(render_dir, filename))
            print("- retained")
    for dirname in dirs:
        print(f"Dir: {dirname}", end=" ")
        if not (dirname == 'practicals'):
            try:
                os.rmdir(os.path.join(root, dirname))
                print("x removed")
            except FileNotFoundError:
                print(f"! unable to remove {dirname}")
            except PermissionError:
                print(f"! permission error on {dirname}")
            except OSError:
                print(f"! os error on {dirname}")

        else:
            print("- retained")

print("Don't publish the answers. Just copy the answers to a shared folder.")
