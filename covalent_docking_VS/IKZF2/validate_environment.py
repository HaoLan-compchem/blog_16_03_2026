#!/usr/bin/env python3
"""
Validation script for checking conda environment setup.
Run this in each environment to verify all required packages are installed.
"""

import sys
import importlib

def check_imports(env_name, required_packages):
    """Check if all required packages can be imported."""
    print(f"\n{'='*60}")
    print(f"Validating {env_name} environment")
    print(f"{'='*60}\n")
    
    all_ok = True
    for package_info in required_packages:
        if isinstance(package_info, tuple):
            package, import_name = package_info
        else:
            package = import_name = package_info
            
        try:
            mod = importlib.import_module(import_name)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {package:30s} (version: {version})")
        except ImportError as e:
            print(f"✗ {package:30s} MISSING")
            all_ok = False
    
    print()
    if all_ok:
        print(f"✓ All packages successfully imported in {env_name}")
    else:
        print(f"✗ Some packages are missing in {env_name}")
        print(f"  Run: conda activate {env_name} && conda install <missing_packages>")
    
    return all_ok

def main():
    # Determine which environment we're in based on command line arg
    if len(sys.argv) < 2:
        print("Usage: python validate_environment.py [vina|openfe|autodock]")
        sys.exit(1)
    
    env_type = sys.argv[1].lower()
    
    if env_type == 'vina':
        packages = [
            'rdkit',
            ('openbabel', 'openbabel'),
            ('pymol', 'pymol'),
            'numpy',
            'scipy',
            'matplotlib',
        ]
        check_imports('vina', packages)
        
    elif env_type == 'openfe' or env_type == 'openfe_env':
        packages = [
            ('parmed', 'parmed'),
            ('openmm', 'openmm'),
            ('openmmforcefields', 'openmmforcefields'),
            ('openff-toolkit', 'openff.toolkit'),
            ('pdbfixer', 'pdbfixer'),
            ('biopython', 'Bio'),
            'numpy',
            'scipy',
        ]
        check_imports('openfe_env', packages)
        
    elif env_type == 'autodock':
        packages = [
            'rdkit',
            'numpy',
        ]
        result = check_imports('autodock', packages)
        if result:
            print("Note: autodock-vina is a command-line tool.")
            print("Verify installation with: vina --help")
        
    else:
        print(f"Unknown environment type: {env_type}")
        print("Valid options: vina, openfe, autodock")
        sys.exit(1)

if __name__ == '__main__':
    main()
