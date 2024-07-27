import os

def list_directory_contents(path, indent=''):
    try:
        entries = os.listdir(path)
    except PermissionError:
        print(f"{indent}\033[31m[Permission Denied]\033[0m")  # Red color for permission denied
        return

    directories = []
    files = []

    for entry in entries:
        if entry.startswith('.'):
            continue  # Skip hidden directories and files

        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            directories.append(entry)
        else:
            files.append(entry)

    if len(files) > 10 or True:
        print(f"{indent}\033[33m[{len(files)} files]\033[0m")  # Yellow color for file count
    else:
        for file in files:
            print(f"{indent}\033[34m{file}\033[0m")  # Blue color for files

    for directory in directories:
        print(f"{indent}{directory}/")
        list_directory_contents(os.path.join(path, directory), indent + '  ')

# Specify the directory path here
directory_path = 'C:/Users/ondra/Documents/Fun/Maths/MonteCarlo/project/'
print(f"Directory tree for: {directory_path}")
list_directory_contents(directory_path)
