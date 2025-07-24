#!/usr/bin/env python3
"""
Launcher script for the Flask Web UI
Handles installation and launches the vendor filtering web interface
"""

import subprocess
import sys
import os

def install_flask():
    """Install Flask if not already installed"""
    try:
        import flask
        print("✅ Flask is already installed")
        return True
    except ImportError:
        print("📦 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Flask")
            return False

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

def launch_web_ui():
    """Launch the Flask web UI"""
    print("🚀 Launching LLM Vendor Filtering System Web UI...")
    print("="*60)
    print("The web interface will open in your browser at: http://localhost:5000")
    print("="*60)
    
    try:
        from simple_web_ui import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error launching web UI: {e}")
        print("Try running: python simple_web_ui.py directly")

def main():
    """Main launcher function"""
    print("🚀 LLM Vendor Filtering System - Web UI Launcher")
    print("="*60)
    
    # Check and install Flask
    if not install_flask():
        print("❌ Cannot proceed without Flask")
        return
    
    # Check database
    if not check_database():
        print("❌ Cannot proceed without database")
        return
    
    # Launch web UI
    launch_web_ui()

if __name__ == "__main__":
    main() 