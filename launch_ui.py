#!/usr/bin/env python3
"""
Launcher script for the Gradio UI
Handles installation and launches the vendor filtering interface
"""

import subprocess
import sys
import os

def install_gradio():
    """Install Gradio if not already installed"""
    try:
        import gradio
        print("✅ Gradio is already installed")
        return True
    except ImportError:
        print("📦 Installing Gradio...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio>=4.0.0"])
            print("✅ Gradio installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Gradio")
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

def launch_ui():
    """Launch the Gradio UI"""
    print("🚀 Launching LLM Vendor Filtering System UI...")
    print("="*60)
    print("The UI will open in your browser at: http://localhost:7860")
    print("You can also access it via the public link that will be provided.")
    print("="*60)
    
    try:
        from gradio_ui import create_interface
        demo = create_interface()
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            show_error=True,
            title="LLM Vendor Filtering System"
        )
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        print("Try running: python gradio_ui.py directly")

def main():
    """Main launcher function"""
    print("🚀 LLM Vendor Filtering System - UI Launcher")
    print("="*60)
    
    # Check and install Gradio
    if not install_gradio():
        print("❌ Cannot proceed without Gradio")
        return
    
    # Check database
    if not check_database():
        print("❌ Cannot proceed without database")
        return
    
    # Launch UI
    launch_ui()

if __name__ == "__main__":
    main() 