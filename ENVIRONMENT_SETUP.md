# Environment Setup Guide

## Conda Environment for Covalent Docking Workflows

This repository contains Jupyter notebooks for covalent docking and virtual screening workflows. These notebooks require specific molecular modeling and docking tools.

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed

### Setting up the environment

1. Create the conda environment from the environment file:

```bash
conda env create -f environment_vina.yml
```

2. Activate the environment:

```bash
conda activate vina
```

3. Launch Jupyter Notebook:

```bash
jupyter notebook
```

### Environment Contents

The `vina` environment includes:

- **Python 3.9**: Base Python interpreter
- **RDKit**: Open-source cheminformatics toolkit for molecular modeling
- **OpenBabel**: Chemical toolbox for molecular format conversion
- **PyMOL**: Molecular visualization system
- **AutoDock Vina**: Molecular docking program
- **NumPy & SciPy**: Scientific computing libraries
- **Jupyter**: Interactive notebook environment

### Workflows requiring this environment

The following notebooks require the `vina` conda environment:

- `covalent_docking_VS/IKZF2/workflow.ipynb`
- `covalent_docking_VS/binary/workflow.ipynb`

### Troubleshooting

If you encounter issues with the environment setup:

1. Make sure conda is up to date:
   ```bash
   conda update conda
   ```

2. Try creating the environment with specific channel priorities:
   ```bash
   conda env create -f environment_vina.yml --channel conda-forge
   ```

3. If a package is not available, try installing it separately with pip after activating the environment:
   ```bash
   conda activate vina
   pip install <package-name>
   ```

### Updating the environment

To update the environment with new dependencies:

1. Edit `environment_vina.yml`
2. Update the existing environment:
   ```bash
   conda env update -f environment_vina.yml --prune
   ```

### Removing the environment

To remove the environment when no longer needed:

```bash
conda deactivate
conda env remove -n vina
```
