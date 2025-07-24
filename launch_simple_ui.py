#!/usr/bin/env python3
"""
Simple Launcher for Vendor Filtering System UI
This launcher works on any system with no external dependencies
"""

import os
import sys
import webbrowser
import threading
import time

def check_database():
    """Check if vendor database exists"""
    if not os.path.exists('vendor_database.json'):
        print("📊 Creating vendor database...")
        try:
            from vendor_database_simple import save_database
            save_database()
            print("✅ Database created successfully")
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    else:
        print("✅ Vendor database already exists")
    return True

def launch_simple_ui():
    """Launch the simple UI"""
    print("🚀 Launching LLM Vendor Filtering System (Simple UI)...")
    print("="*60)
    
    try:
        from simple_ui import main
        main()
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        print("Try running: python simple_ui.py directly")

def main():
    """Main launcher function"""
    print("🚀 LLM Vendor Filtering System - Simple UI Launcher")
    print("="*60)
    print("This UI uses Python's built-in HTTP server - no external dependencies!")
    print("="*60)
    
    # Check database
    if not check_database():
        print("❌ Cannot proceed without database")
        return
    
    # Launch UI
    launch_simple_ui()

if __name__ == "__main__":
    main() 