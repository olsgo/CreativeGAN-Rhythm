#!/usr/bin/env python3
"""
Migration script to update CreativeGAN-Rhythm notebooks for M1 Max compatibility
"""

import json
import os
import re
import shutil
from pathlib import Path

def update_notebook_for_m1(notebook_path):
    """Update a single notebook for M1 Max compatibility"""
    print(f"Updating {notebook_path}...")
    
    # Create backup
    backup_path = str(notebook_path) + '.backup'
    shutil.copy2(notebook_path, backup_path)
    print(f"  Created backup: {backup_path}")
    
    # Read notebook
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    updated_cells = 0
    
    # Process each cell
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            original_source = cell['source'][:]
            updated_source = []
            cell_updated = False
            
            # Check if this is the first code cell with CUDA setup
            has_cuda = any('CUDA_VISIBLE_DEVICES' in line for line in cell['source'])
            if has_cuda:
                # Replace with M1 setup
                updated_source = [
                    "# M1 Max Optimized Setup\\n",
                    "import sys\\n",
                    "sys.path.append('./rhythm_can')\\n",
                    "\\n",
                    "# Import M1 optimization utilities\\n",
                    "from rhythm_can.m1_optimization import configure_tensorflow_for_m1, get_optimized_imports\\n",
                    "\\n",
                    "# Configure TensorFlow for M1 Max\\n",
                    "tf = configure_tensorflow_for_m1()\\n",
                    "\\n",
                    "# Get optimized imports\\n",
                    "imports = get_optimized_imports()\\n",
                    "globals().update(imports)\\n",
                    "\\n",
                    "print('✅ M1 Max optimization complete!')\\n"
                ]
                cell_updated = True
            else:
                # Process line by line for other updates
                for line in cell['source']:
                    # Update keras imports
                    if re.match(r'^from keras\\.', line):
                        updated_source.append(f"# {line}")
                        cell_updated = True
                    elif re.match(r'^import keras\\.', line):
                        updated_source.append(f"# {line}")
                        cell_updated = True
                    # Update optimizer learning rate parameter
                    elif 'lr=' in line and ('Adam(' in line or 'RMSprop(' in line):
                        updated_line = line.replace('lr=', 'learning_rate=')
                        updated_source.append(updated_line)
                        cell_updated = True
                    # Update tensorboard_logger imports
                    elif 'tensorboard_logger' in line:
                        updated_source.append(f"# {line}")
                        cell_updated = True
                    else:
                        updated_source.append(line)
            
            if cell_updated:
                cell['source'] = updated_source
                updated_cells += 1
    
    # Add title cell at the beginning
    title_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"# {os.path.basename(notebook_path)} - M1 Max Optimized\\n",
            "\\n",
            "This notebook has been optimized for M1 Max machines running macOS Sequoia:\\n",
            "- Updated to TensorFlow 2.x with Apple Silicon support\\n",
            "- Added Metal GPU acceleration\\n",
            "- Enabled mixed precision training\\n",
            "- Updated all Keras imports to use tf.keras\\n"
        ]
    }
    
    nb['cells'].insert(0, title_cell)
    updated_cells += 1
    
    # Save updated notebook
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    
    print(f"  Updated {updated_cells} cells")
    print(f"  ✅ Successfully updated {notebook_path}")
    
    return updated_cells

def main():
    """Main migration function"""
    print("🚀 Starting CreativeGAN-Rhythm M1 Max migration...")
    
    # Find all notebook files
    notebook_files = list(Path('.').glob('*.ipynb'))
    notebook_files = [nb for nb in notebook_files if 'M1_Max_Optimization_Guide' not in str(nb)]
    
    print(f"Found {len(notebook_files)} notebooks to update:")
    for nb in notebook_files:
        print(f"  - {nb}")
    
    total_updated_cells = 0
    
    # Update each notebook
    for notebook_path in notebook_files:
        try:
            updated_cells = update_notebook_for_m1(notebook_path)
            total_updated_cells += updated_cells
        except Exception as e:
            print(f"❌ Error updating {notebook_path}: {e}")
    
    print(f"\\n✅ Migration complete!")
    print(f"Updated {total_updated_cells} cells across {len(notebook_files)} notebooks")
    print(f"\\n📝 Next steps:")
    print(f"1. Install dependencies: pip install -r requirements.txt")
    print(f"2. Test the M1_Max_Optimization_Guide.ipynb notebook")
    print(f"3. Run your updated notebooks!")

if __name__ == "__main__":
    main()