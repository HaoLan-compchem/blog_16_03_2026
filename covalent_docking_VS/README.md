# Covalent Docking Virtual Screening

This directory contains workflows for performing covalent docking virtual screening studies.

## Directory Structure

- **IKZF2/**: Virtual screening workflow for IKZF2 target
- **binary/**: Binary classification workflow for covalent docking

## Environment Requirements

Both workflows require multiple conda environments due to incompatible dependencies. Each subdirectory contains:

- `environment_vina.yml` - Environment for AutoDock Vina operations
- `environment_openfe.yml` - Environment for OpenMM/OpenFE operations  
- `environment_autodock.yml` - Environment for AutoDock operations
- `README.md` - Detailed instructions for that specific workflow

## Quick Start

1. Navigate to the workflow directory of interest (IKZF2 or binary)
2. Follow the setup instructions in that directory's README.md
3. Create the required conda environments
4. Run the Jupyter notebook with appropriate kernel switching

## General Workflow Pattern

All workflows follow a similar pattern:

1. **Molecular Preparation** (vina environment)
   - Load and process molecular structures
   - Generate molecular variations
   
2. **Protein Preparation** (openfe_env environment)
   - Clean and prepare protein structures
   - Add missing atoms/residues
   
3. **Docking** (autodock/vina environments)
   - Perform molecular docking
   - Generate poses
   
4. **Analysis** (vina environment)
   - Filter results
   - Calculate RMSD
   - Extract valid poses

## Common Issues

### Environment Conflicts
The reason for multiple environments is that certain packages have conflicting dependencies:
- PyMOL and OpenMM have different Python version requirements
- AutoDock tools may conflict with RDKit versions
- OpenFF toolkit has specific OpenMM version requirements

### Kernel Switching
When using Jupyter notebooks:
- Install all environments as kernels (see individual READMEs)
- Switch kernels as indicated by cell comments
- Don't mix environments within a single kernel session

## Contributing

When adding new workflows to this directory:
1. Include all necessary environment.yml files
2. Add clear cell-level comments indicating required environments
3. Create a comprehensive README.md
4. Test the workflow with fresh conda environments

## Support

For issues specific to a workflow, refer to the README.md in that workflow's directory.
