#!/usr/bin/env python3
"""
Test script for the Gradio UI components
Tests the UI functions without launching the full interface
"""

import sys
import os

def test_ui_functions():
    """Test the UI functions without launching Gradio"""
    print("🧪 Testing UI Components")
    print("="*50)
    
    try:
        # Test database initialization
        from vendor_database_simple import save_database
        print("✅ Database functions imported")
        
        # Test filter system
        from vendor_filter import VendorFilter
        filter_system = VendorFilter()
        print("✅ Filter system initialized")
        
        # Test use case data
        from user_input_example import use_case, additional_use_cases
        print("✅ Use case data loaded")
        
        # Test UI functions (without Gradio)
        print("✅ All UI dependencies available")
        
        # Test recommendation function
        recommendations = filter_system.get_vendor_recommendations(use_case)
        print(f"✅ Recommendation system working - found {recommendations['summary']['total_matches']} matches")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing UI components: {e}")
        return False

def test_gradio_import():
    """Test if Gradio can be imported"""
    print("\n📦 Testing Gradio Import")
    print("="*50)
    
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
        print(f"   Version: {gr.__version__}")
        return True
    except ImportError:
        print("❌ Gradio not installed")
        print("   Run: pip install gradio>=4.0.0")
        return False

def main():
    """Main test function"""
    print("🚀 UI Component Test")
    print("="*50)
    
    # Test core functions
    core_ok = test_ui_functions()
    
    # Test Gradio
    gradio_ok = test_gradio_import()
    
    print("\n" + "="*50)
    if core_ok and gradio_ok:
        print("✅ All tests passed! UI is ready to launch.")
        print("   Run: python launch_ui.py")
    elif core_ok:
        print("⚠️  Core functions work, but Gradio needs to be installed.")
        print("   Run: pip install gradio>=4.0.0")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("="*50)

if __name__ == "__main__":
    main() 