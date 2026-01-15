# IKZF2 Covalent Docking Virtual Screening Workflow

## Overview
This workflow performs covalent docking virtual screening for IKZF2. The notebook requires multiple conda environments due to dependencies that cannot coexist in a single environment.

## Prerequisites
- Conda or Mamba installed
- Basic understanding of Jupyter notebooks

## Environment Setup

This workflow requires three separate conda environments:

### 1. Vina Environment
Used for molecular docking with AutoDock Vina, RDKit molecular manipulations, and PyMOL visualization.

```bash
conda env create -f environment_vina.yml
conda activate vina
# Validate installation
python validate_environment.py vina
```

**Required for cells:** Cell 1, Cell 2, Cell 3, and Cell 17 (marked with `# conda vina env`)

### 2. OpenFE Environment  
Used for OpenMM molecular dynamics simulations and protein preparation with PDBFixer.

```bash
conda env create -f environment_openfe.yml
conda activate openfe_env
# Validate installation
python validate_environment.py openfe
```

**Required for cells:** Cell 9 (marked with `#conda openfe env`)

### 3. AutoDock Environment
Used for AutoDock-specific docking operations.

```bash
conda env create -f environment_autodock.yml
conda activate autodock
# Validate installation
python validate_environment.py autodock
```

**Required for cells:** Cell 13 (marked with `#conda autodock env`)

## Usage Instructions

### Running the Notebook

1. **Install all three environments** using the commands above

2. **Start Jupyter in the vina environment** (most cells use this):
   ```bash
   conda activate vina
   jupyter notebook workflow.ipynb
   ```

3. **Switch environments as needed:**
   - When you reach a cell with a different environment comment (e.g., `#conda openfe env`), you'll need to:
     - Stop the current kernel
     - Activate the required environment in your terminal
     - Restart Jupyter or change the kernel
   
   **OR** use Jupyter's kernel switching:
   - Install all environments as Jupyter kernels:
     ```bash
     conda activate vina
     python -m ipykernel install --user --name vina --display-name "Python (vina)"
     
     conda activate openfe_env
     python -m ipykernel install --user --name openfe_env --display-name "Python (openfe_env)"
     
     conda activate autodock
     python -m ipykernel install --user --name autodock --display-name "Python (autodock)"
     ```
   - Then switch kernels in Jupyter as needed for each cell

## Cell-by-Cell Environment Guide

- **Cells 1-3, 17:** Use `vina` environment
  - Molecular docking with Vina
  - RDKit molecular operations
  - PyMOL visualization
  
- **Cell 9:** Use `openfe_env` environment
  - OpenMM simulations
  - Protein preparation with PDBFixer
  
- **Cell 13:** Use `autodock` environment
  - AutoDock-specific operations

## Workflow Summary

The workflow performs the following steps:
1. Load and prepare molecular structures
2. Generate and process molecular variations
3. Perform covalent docking simulations
4. Filter and analyze docking results
5. Extract valid poses based on RMSD criteria

## Data Requirements

- Input SDF file: `covalent_cereblon_binders_final_clean_inc_sulf_long.sdf`
- PDB structures: `7LPS` and `7U8F` directories

## Output

- Docked poses for each ligand
- Valid poses filtered by RMSD threshold
- Final results in `final_docked_poses/` directory

## Troubleshooting

### ImportError for specific packages
Make sure you're using the correct conda environment for the cell you're executing. Check the environment comment at the top of each cell.

### Kernel crashes
This may happen due to memory issues or incompatible package versions. Try:
- Restarting the kernel
- Ensuring you're using the correct environment
- Checking package versions match the environment file

### Missing dependencies
If a package is missing:
```bash
conda activate <environment_name>
conda install <package_name>
```

## Notes

- The workflow processes 3,600 molecules through multiple docking trials
- Execution time can be substantial depending on computational resources
- Some cells produce large amounts of output and may take considerable time to complete

## Citation

If you use this workflow, please cite appropriately (add citation details here).
