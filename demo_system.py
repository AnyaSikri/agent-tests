#!/usr/bin/env python3
"""
Complete Vendor Filtering System Demo
This script demonstrates the full workflow:
1. Creating the vendor database
2. Defining use case requirements
3. Filtering and recommending vendors
"""

import sys
import os
from vendor_database import create_vendor_database, save_database
from user_input_example import use_case, additional_use_cases, print_use_case_summary
from vendor_filter import VendorFilter

def setup_database():
    """
    Set up the vendor database if it doesn't exist
    """
    if not os.path.exists('vendor_database.json'):
        print("📊 Creating vendor database...")
        database = save_database()
        print("✅ Database created successfully!")
    else:
        print("✅ Vendor database already exists")

def demo_insurance_claims():
    """
    Demo the insurance claims use case
    """
    print("\n" + "="*60)
    print("🏥 INSURANCE CLAIMS PRIORITY CLASSIFICATION DEMO")
    print("="*60)
    
    # Show the use case requirements
    print_use_case_summary(use_case)
    
    # Initialize filter and get recommendations
    filter_system = VendorFilter()
    recommendations = filter_system.get_vendor_recommendations(use_case)
    
    # Display results
    filter_system.print_recommendations(recommendations, use_case['name'])
    
    return recommendations

def demo_custom_requirements():
    """
    Demo with custom user-defined requirements
    """
    print("\n" + "="*60)
    print("🎯 CUSTOM REQUIREMENTS DEMO")
    print("="*60)
    
    # Example custom requirements
    custom_use_case = {
        "name": "Custom Document Analysis",
        "requirements": {
            "deployment": {"type": "Cloud", "reason": "Need scalability"},
            "latency": {"type": "Batch", "max_response_time": "1 hour", "reason": "Non-time-critical processing"},
            "modality": {
                "input": ["Text", "Image"],
                "output": ["Text"],
                "reason": "Process documents and images to extract text"
            }
        }
    }
    
    print("Custom Requirements:")
    print(f"  Deployment: {custom_use_case['requirements']['deployment']['type']}")
    print(f"  Latency: {custom_use_case['requirements']['latency']['type']}")
    print(f"  Input: {', '.join(custom_use_case['requirements']['modality']['input'])}")
    print(f"  Output: {', '.join(custom_use_case['requirements']['modality']['output'])}")
    
    # Get recommendations
    filter_system = VendorFilter()
    recommendations = filter_system.get_vendor_recommendations(custom_use_case)
    
    # Display results
    filter_system.print_recommendations(recommendations, custom_use_case['name'])
    
    return recommendations

def demo_filter_examples():
    """
    Demo various filtering options
    """
    print("\n" + "="*60)
    print("🔍 FILTERING EXAMPLES DEMO")
    print("="*60)
    
    filter_system = VendorFilter()
    
    # Example 1: Cloud deployment only
    print("\n1. Cloud Deployment Vendors:")
    cloud_vendors = filter_system.filter_by_deployment('Cloud')
    print(f"   Found {len(cloud_vendors)} vendors")
    for vendor in cloud_vendors[:3]:  # Show first 3
        print(f"   • {vendor['model_name']}")
    
    # Example 2: Real-time latency only
    print("\n2. Real-time Latency Vendors:")
    realtime_vendors = filter_system.filter_by_latency('real-time')
    print(f"   Found {len(realtime_vendors)} vendors")
    for vendor in realtime_vendors[:3]:  # Show first 3
        print(f"   • {vendor['model_name']}")
    
    # Example 3: Text input/output only
    print("\n3. Text Input/Output Vendors:")
    text_vendors = filter_system.filter_by_modality(['Text'], ['Text'])
    print(f"   Found {len(text_vendors)} vendors")
    for vendor in text_vendors[:3]:  # Show first 3
        print(f"   • {vendor['model_name']}")
    
    # Example 4: Combined filters
    print("\n4. Combined Filters (Cloud + Real-time + Text):")
    combined_vendors = filter_system.filter_vendors(
        deployment_type='Cloud',
        latency_requirement='real-time',
        input_modalities=['Text'],
        output_modalities=['Text']
    )
    print(f"   Found {len(combined_vendors)} vendors")
    for vendor in combined_vendors[:5]:  # Show first 5
        print(f"   • {vendor['model_name']}")

def interactive_demo():
    """
    Interactive demo where user can input their own requirements
    """
    print("\n" + "="*60)
    print("🎮 INTERACTIVE DEMO")
    print("="*60)
    
    print("Let's create your own use case!")
    
    # Get user input
    use_case_name = input("Enter use case name: ").strip()
    description = input("Enter description: ").strip()
    
    print("\nDeployment options: Cloud, On-premise, Any")
    deployment = input("Enter deployment type: ").strip()
    
    print("\nLatency options: Real-time, Batch, Any")
    latency = input("Enter latency requirement: ").strip()
    
    print("\nInput modality options: Text, Image, Video, Speech")
    input_mod = input("Enter input modalities (comma-separated): ").strip()
    input_modalities = [mod.strip() for mod in input_mod.split(',') if mod.strip()]
    
    print("\nOutput modality options: Text, Chat, Image, Video, Speech, Embedding")
    output_mod = input("Enter output modalities (comma-separated): ").strip()
    output_modalities = [mod.strip() for mod in output_mod.split(',') if mod.strip()]
    
    # Create custom use case
    custom_use_case = {
        "name": use_case_name,
        "description": description,
        "requirements": {
            "deployment": {"type": deployment, "reason": "User specified"},
            "latency": {"type": latency, "max_response_time": "User specified", "reason": "User specified"},
            "modality": {
                "input": input_modalities,
                "output": output_modalities,
                "reason": "User specified"
            }
        }
    }
    
    # Get recommendations
    filter_system = VendorFilter()
    recommendations = filter_system.get_vendor_recommendations(custom_use_case)
    
    # Display results
    filter_system.print_recommendations(recommendations, custom_use_case['name'])

def main():
    """
    Main demo function
    """
    print("🚀 VENDOR FILTERING SYSTEM DEMO")
    print("="*60)
    
    # Setup
    setup_database()
    
    # Run demos
    try:
        # Demo 1: Insurance claims
        demo_insurance_claims()
        
        # Demo 2: Custom requirements
        demo_custom_requirements()
        
        # Demo 3: Filter examples
        demo_filter_examples()
        
        # Demo 4: Interactive (optional)
        print("\n" + "="*60)
        interactive_choice = input("Would you like to try the interactive demo? (y/n): ").strip().lower()
        if interactive_choice in ['y', 'yes']:
            interactive_demo()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 