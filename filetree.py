import os

def print_directory_contents(path, indent=0):
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        if os.path.isdir(child_path):
            print(' ' * indent + child + '/')
            print_directory_contents(child_path, indent + 4)
        else:
            print(' ' * indent + child)

print_directory_contents(r'C:/Users/Marcus/Repositories/ZyrenthSorter')