#!/usr/bin/env python3
"""
Run this to generate LLM vendor database generator
"""

import os
import sys
import subprocess

def run_database_generation():
    """Run the database generation"""
    print("Starting database generation...")
    
    result = subprocess.run([sys.executable, 'orchestrator_database.py'], 
                          capture_output=True, 
                          text=True)
    
    if result.returncode == 0:
        print("Database generation completed successfully!")
        return True
    else:
        print("Database generation failed")
        print(f"Error: {result.stderr}")
        return False

def show_status():
    """Show file status"""
    print("Checking generated files...")
    
    files = [
        'complete_llm_database.csv',
        'llm_database_schema.csv'
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"{file_path} ({size} bytes)")
        else:
            print(f"{file_path} (missing)")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        show_status()
    else:
        run_database_generation()

if __name__ == "__main__":
    main() 