#!/usr/bin/env python3
"""
Simple Test Script for Vendor Filtering System
This script demonstrates the core functionality without interactive input
"""

import json
from vendor_database_simple import create_vendor_database, save_database
from user_input_example import use_case
from vendor_filter import VendorFilter

def test_insurance_claims():
    """
    Test the insurance claims use case
    """
    print("🏥 TESTING INSURANCE CLAIMS USE CASE")
    print("="*50)
    
    # Create database if needed
    try:
        with open('vendor_database.json', 'r') as f:
            database = json.load(f)
        print(f"✅ Loaded database with {len(database)} vendors")
    except FileNotFoundError:
        print("📊 Creating vendor database...")
        database = save_database()
    
    # Initialize filter
    filter_system = VendorFilter()
    
    # Get recommendations
    recommendations = filter_system.get_vendor_recommendations(use_case)
    
    # Display results
    print(f"\n📊 RESULTS FOR: {use_case['name']}")
    print(f"Total matches: {recommendations['summary']['total_matches']}")
    print(f"Perfect matches: {recommendations['summary']['perfect_matches']}")
    print(f"Good matches: {recommendations['summary']['good_matches']}")
    print(f"Partial matches: {recommendations['summary']['partial_matches']}")
    
    if recommendations['perfect_matches']:
        print("\n🎯 PERFECT MATCHES:")
        for match in recommendations['perfect_matches'][:3]:  # Show top 3
            vendor = match['vendor']
            print(f"  • {vendor['model_name']}")
            print(f"    - Deployment: {vendor['deployment_type']}")
            print(f"    - Latency: {vendor['latency_support']}")
            print(f"    - Input: {vendor['input_modalities']}")
            print(f"    - Output: {vendor['output_modalities']}")
    
    return recommendations

def test_filtering():
    """
    Test various filtering options
    """
    print("\n🔍 TESTING FILTERING FUNCTIONALITY")
    print("="*50)
    
    filter_system = VendorFilter()
    
    # Test deployment filter
    cloud_vendors = filter_system.filter_by_deployment('Cloud')
    print(f"Cloud deployment vendors: {len(cloud_vendors)}")
    
    # Test latency filter
    realtime_vendors = filter_system.filter_by_latency('real-time')
    print(f"Real-time latency vendors: {len(realtime_vendors)}")
    
    # Test modality filter
    text_vendors = filter_system.filter_by_modality(['Text'], ['Text'])
    print(f"Text input/output vendors: {len(text_vendors)}")
    
    # Test combined filter
    combined_vendors = filter_system.filter_vendors(
        deployment_type='Cloud',
        latency_requirement='real-time',
        input_modalities=['Text'],
        output_modalities=['Text']
    )
    print(f"Combined filter (Cloud + Real-time + Text): {len(combined_vendors)}")
    
    if combined_vendors:
        print("\nTop 5 matching vendors:")
        for vendor in combined_vendors[:5]:
            print(f"  • {vendor['model_name']}")

def test_custom_use_case():
    """
    Test a custom use case
    """
    print("\n🎯 TESTING CUSTOM USE CASE")
    print("="*50)
    
    # Custom use case: Document analysis
    custom_use_case = {
        "name": "Document Analysis System",
        "requirements": {
            "deployment": {"type": "Cloud", "reason": "Scalability needed"},
            "latency": {"type": "Batch", "max_response_time": "30 minutes", "reason": "Non-time-critical"},
            "modality": {
                "input": ["Text", "Image"],
                "output": ["Text"],
                "reason": "Process documents and images"
            }
        }
    }
    
    filter_system = VendorFilter()
    recommendations = filter_system.get_vendor_recommendations(custom_use_case)
    
    print(f"Results for {custom_use_case['name']}:")
    print(f"Total matches: {recommendations['summary']['total_matches']}")
    print(f"Perfect matches: {recommendations['summary']['perfect_matches']}")
    print(f"Good matches: {recommendations['summary']['good_matches']}")
    
    if recommendations['perfect_matches']:
        print("\nPerfect matches:")
        for match in recommendations['perfect_matches'][:3]:
            vendor = match['vendor']
            print(f"  • {vendor['model_name']}")

def main():
    """
    Main test function
    """
    print("🚀 VENDOR FILTERING SYSTEM TEST")
    print("="*50)
    
    try:
        # Test 1: Insurance claims
        test_insurance_claims()
        
        # Test 2: Filtering functionality
        test_filtering()
        
        # Test 3: Custom use case
        test_custom_use_case()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 