#!/usr/bin/env python3
"""
LLM Vendor Database Generator - Simple Orchestrator
"""

import os
import sys
import subprocess
import pandas as pd

# All modules to run
MODULES = [
    'vendor_database.py',
    'source_type.py',
    'cost.py',
    'context_window.py', 
    'latency.py',
    'modality.py',
    'model_specificity.py',
    'deployment_v2.py'
]

# Expected output files from each module
OUTPUT_FILES = {
    'vendor_database.py': 'vendor_database_output.csv',
    'cost.py': 'cost_analysis_output.csv',
    'context_window.py': 'context_window_output.csv',
    'latency.py': 'latency_label.csv',
    'modality.py': 'modality_output.csv',
    'model_specificity.py': 'llm_specificity_output.csv',
    'source_type.py': 'source_type.csv',
    'deployment_v2.py': 'deployment_types.csv'
}

def clean_files():
    """Remove existing output files"""
    files_to_remove = list(OUTPUT_FILES.values()) + [
        'complete_llm_database.csv',
        'schema_documentation.csv'
    ]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)

def run_module(module_name):
    """Run a single module"""
    print(f"Running {module_name}...")
    
    # Change to attribute_functions directory to run the module
    original_dir = os.getcwd()
    os.chdir('../attribute_functions')
    
    subprocess.run([sys.executable, module_name], check=True)
    
    # Change back to original directory
    os.chdir(original_dir)
    print(f"✓ {module_name} completed")

def join_all_data():
    """Join all CSV files into one comprehensive database"""
    print("Joining all data files...")
    
    # Start with vendor database as the base
    base_df = pd.read_csv(f"../attribute_functions/{OUTPUT_FILES['vendor_database.py']}")
    
    # Join each additional file
    for module, output_file in OUTPUT_FILES.items():
        if module == 'vendor_database.py':
            continue  # Skip base file
            
        file_path = f"../attribute_functions/{output_file}"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            
            # Standardize model name column to model_name
            model_col = None
            for col in df.columns:
                if 'model' in col.lower() or 'name' in col.lower():
                    model_col = col
                    break
            
            if model_col and model_col != 'model_name':
                df = df.rename(columns={model_col: 'model_name'})
            
            # Add prefix to other columns to avoid conflicts
            prefix = module.replace('.py', '').replace('_', '')
            for col in df.columns:
                if col != 'model_name':
                    df = df.rename(columns={col: f"{prefix}_{col}"})
            
            # Join with base database
            base_df = base_df.merge(df, on='model_name', how='left')
            print(f"✓ Joined {output_file}")
    
    # Save joined database
    base_df.to_csv('complete_llm_database.csv', index=False)
    print(f"✓ Complete database saved: {len(base_df)} rows, {len(base_df.columns)} columns")
    return base_df

def create_schema_documentation(df):
    """Create schema documentation for the final database"""
    print("Creating schema documentation...")
    
    schema_data = []
    for col in df.columns:
        schema_data.append({
            'Column_Name': col,
            'Data_Type': str(df[col].dtype),
            'Non_Null_Count': df[col].notna().sum(),
            'Null_Count': len(df) - df[col].notna().sum(),
            'Description': get_column_description(col)
        })
    
    schema_df = pd.DataFrame(schema_data)
    schema_df.to_csv('llm_database_schema.csv', index=False)
    print("✓ LLM database schema saved")

def get_column_description(col):
    """Get description for a column based on its name"""
    descriptions = {
        'model_name': 'Name of the LLM model',
        'vendor_name': 'Company that developed the model',
        'formation_year': 'Year the vendor company was founded',
        'age_years': 'Age of the vendor company in years',
        'category': 'Vendor company category',
        'status': 'Vendor company status',
        'vendor_maturity': 'Vendor maturity level (emerging/established/mature)',
        'cost_': 'Cost-related information',
        'context_window_': 'Context window information',
        'latency_': 'Latency-related data',
        'modality_': 'Input/output modality information',
        'model_specificity_': 'Model specificity details',
        'source_type_': 'Source type information',
        'deployment_': 'Deployment type information'
    }
    
    for prefix, desc in descriptions.items():
        if col.startswith(prefix):
            return desc
    return 'Additional model attribute'

def main():
    print("LLM Vendor Database Generator")
    print("=" * 40)
    
    # Clean existing files
    clean_files()
    
    # Run all modules
    for module in MODULES:
        run_module(module)
    
    # Join all data
    final_df = join_all_data()
    
    # Create schema documentation
    create_schema_documentation(final_df)
    
    print("\n✓ Database generation completed!")
    print("Files created:")
    print("  - complete_llm_database.csv")
    print("  - llm_database_schema.csv")

if __name__ == "__main__":
    main()
