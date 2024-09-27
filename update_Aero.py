import re
import subprocess

def get_commit_count():
    try:
        # Check if inside a git repository
        subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'])
        
        # Get the current commit count
        commit_count = int(subprocess.check_output(['git', 'rev-list', '--count', 'HEAD']).strip())
        return commit_count
    except subprocess.CalledProcessError:
        return None

commit_count = get_commit_count()

if commit_count is not None:
    # Divide the commit count by 100 to get a version number with two decimal places
    version = commit_count / 100

    # Specify the path to the Python file
    file_path = 'C:\\Coding\\SAE_Aero\\Aero.py'

    # Read the current content of the Python file
    with open(file_path, 'r') as file:
        content = file.read()

    # Update the version in the Python file
    content = re.sub(r'__version__ = .*', f'__version__ = "{version:.2f}"', content)

    # Write the updated content back to the Python file
    with open(file_path, 'w') as file:
        file.write(content)
else:
    print("Error: Not a git repository or no commits found.")