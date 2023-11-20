__author__ = 'desultory'
__version__ = '1.0.0'


def replace_file_line(file_path, old_line, new_line):
    """
    Replaces a line in a file
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if old_line not in lines:
        raise ValueError("Old line not found: %s" % old_line)

    lines[lines.index(old_line)] = new_line

    with open(file_path, 'w') as f:
        f.writelines(lines)
