import os

def clear_file(file):
    with open(file, 'w') as f:
        f.truncate(0)

def create_file(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write('')

def write_append(text, path):
    with open(path, 'a') as f:
        f.write(text)

def write_array(array, path):
    for a in array:
        write_append(a, path)