import os
import shutil
import importlib
import ast
import datetime

def create_backup(file_path, backup_dir):
    """Create a backup of the file in the specified directory."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
    shutil.copy2(file_path, backup_path)

def create_version_backup(root_dir):
    """Create a versioned backup of all Python files."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    version_dir = os.path.join(root_dir, "backups", f"version_{timestamp}")
    os.makedirs(version_dir)
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, root_dir)
                dst_path = os.path.join(version_dir, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

def validate_imports(file_path):
    """Validate imports in a Python file."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    
    valid_imports = []
    invalid_imports = []

    for imp in imports:
        if isinstance(imp, ast.Import):
            for alias in imp.names:
                try:
                    importlib.import_module(alias.name)
                    valid_imports.append(alias.name)
                except ImportError:
                    invalid_imports.append(alias.name)
        elif isinstance(imp, ast.ImportFrom):
            try:
                importlib.import_module(imp.module)
                valid_imports.append(imp.module)
            except ImportError:
                invalid_imports.append(imp.module)

    return valid_imports, invalid_imports

def validate_file_structure(root_dir):
    """Validate the file structure of the project."""
    expected_files = [
        'streamlit_app.py',
        'database.py',
        'utils/auth.py',
        'views/home.py',
        'views/blog_post.py',
        'views/category.py',
        'views/about.py',
        'views/contact.py',
        'views/search.py',
        'views/admin/dashboard.py',
        'views/admin/post_management.py',
        'views/admin/comment_management.py',
        'views/admin/user_management.py'
    ]

    missing_files = []
    for file_path in expected_files:
        full_path = os.path.join(root_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)

    return missing_files

def validate_and_correct(root_dir):
    """Validate and attempt to correct issues in the project."""
    create_version_backup(root_dir)

    missing_files = validate_file_structure(root_dir)
    if missing_files:
        print("Missing files:")
        for file in missing_files:
            print(f"  - {file}")
    else:
        print("All expected files are present.")

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"\nValidating {file_path}")
                
                valid_imports, invalid_imports = validate_imports(file_path)
                
                if invalid_imports:
                    print(f"  Invalid imports in {file}:")
                    for imp in invalid_imports:
                        print(f"    - {imp}")
                    
                    # Attempt to correct invalid imports
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    for imp in invalid_imports:
                        if imp.startswith('views.'):
                            corrected_imp = f"from {imp} import *"
                            content = content.replace(f"import {imp}", corrected_imp)
                    
                    create_backup(file_path, os.path.join(root_dir, "backups", "pre_correction"))
                    
                    with open(file_path, 'w') as f:
                        f.write(content)
                    
                    print(f"  Attempted to correct imports in {file}")
                else:
                    print(f"  All imports in {file} are valid.")

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    validate_and_correct(root_dir)