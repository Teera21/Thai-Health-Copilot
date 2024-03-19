import os

def is_name_in_folder(name, path='./data/data_user'):
    # List all entries in the given path
    all_entries = os.listdir(path)
    
    # Filter out directories from all entries
    directories = [d for d in all_entries if os.path.isdir(os.path.join(path, d))]
    
    # Check if the name is part of any folder names
    for folder in directories:
        if name in folder:
            file_path = path+'/{}/Information.txt'.format(name)

# Using the 'with' statement to automatically handle file closing
            with open(file_path, 'r') as file:
                file_content = file.read()
            return True, file_content  # Name found in folder name
    return False,""  # Name not found in any folder name
