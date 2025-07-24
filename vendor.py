import requests
from bs4 import BeautifulSoup
import csv
import re
from typing import List, Dict, Optional
import urllib.request

# Vendor formation years lookup table
VENDOR_FORMATION_DATA = {
    "Anthropic": {"formation_year": 2021, "company_name": "Anthropic PBC"},
    "Meta": {"formation_year": 2004, "company_name": "Meta Platforms Inc."},
    "Amazon": {"formation_year": 1994, "company_name": "Amazon.com Inc."},
    "Google": {"formation_year": 1998, "company_name": "Alphabet Inc. (Google)"},
    "Microsoft": {"formation_year": 1975, "company_name": "Microsoft Corporation"},
    "OpenAI": {"formation_year": 2015, "company_name": "OpenAI LP"},
    "Cohere": {"formation_year": 2019, "company_name": "Cohere Inc."},
    "AI21": {"formation_year": 2017, "company_name": "AI21 Labs"},
    "Stability": {"formation_year": 2020, "company_name": "Stability AI"},
    "Writer": {"formation_year": 2020, "company_name": "Writer Inc."},
    "Mistral": {"formation_year": 2023, "company_name": "Mistral AI"},
    "DeepSeek": {"formation_year": 2023, "company_name": "DeepSeek"},
    "Perplexity": {"formation_year": 2022, "company_name": "Perplexity AI"}
}

def fetch_html(url: str) -> str:
    """Fetch HTML content from URL"""
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    return html

def fetch_bedrock_catalog() -> str:
    """Fetch the AWS Bedrock catalog page"""
    url = "https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html"
    try:
        return fetch_html(url)
    except Exception as e:
        print(f"Error fetching Bedrock catalog: {e}")
        return ""

def parse_bedrock_models(html: str) -> List[str]:
    """Parse model names from AWS Bedrock catalog HTML"""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        print("No table found in the page!")
        return []

    rows = table.find_all("tr")
    if not rows:
        return []
    
    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    model_names = []
    
    for row in rows[1:]:
        cols = row.find_all("td")
        if cols:
            model_info = {headers[i]: cols[i].get_text(strip=True) for i in range(min(len(headers), len(cols)))}
            model_name = model_info.get("Model name", "")
            if model_name:
                model_names.append(model_name)
    
    return model_names

def extract_vendor_from_model_name(model_name: str) -> str:
    """Extract vendor name from model name"""
    model_name_lower = model_name.lower()
    
    # Direct vendor mappings
    vendor_mappings = {
        "claude": "Anthropic",
        "llama": "Meta",
        "mistral": "Mistral",
        "nova": "Perplexity",
        "deepseek": "DeepSeek",
        "command": "Cohere",
        "jurassic": "AI21",
        "stable diffusion": "Stability",
        "titan": "Amazon",
        "palmyra": "Writer",
        "gpt": "OpenAI",
        "gemini": "Google"
    }
    
    for keyword, vendor in vendor_mappings.items():
        if keyword in model_name_lower:
            return vendor
    
    return "Unknown"

def calculate_vendor_age(formation_year: int) -> int:
    """Calculate vendor age in years"""
    from datetime import datetime
    current_year = datetime.now().year
    return current_year - formation_year

def categorize_vendor(formation_year: int) -> str:
    """Categorize vendor based on formation year"""
    age = calculate_vendor_age(formation_year)
    
    if age < 2:
        return "Emerging Vendor"
    elif age >= 5:
        return "Known Vendor"
    else:
        return "Established Vendor"

def analyze_vendors_from_models(model_names: List[str]) -> List[Dict[str, str]]:
    """Analyze vendors from a list of model names"""
    results = []
    
    for model_name in model_names:
        vendor_name = extract_vendor_from_model_name(model_name)
        vendor_data = VENDOR_FORMATION_DATA.get(vendor_name, {})
        
        formation_year = vendor_data.get("formation_year")
        company_name = vendor_data.get("company_name", "Unknown")
        
        if formation_year:
            age_years = calculate_vendor_age(formation_year)
            category = categorize_vendor(formation_year)
            status = "Found in Database"
        else:
            formation_year = "Unknown"
            age_years = "Unknown"
            category = "Unknown"
            status = "Not Found in Database"
        
        result = {
            "Model Name": model_name,
            "Vendor Name": vendor_name,
            "Company Name": company_name,
            "Formation Year": formation_year,
            "Age (Years)": age_years,
            "Vendor Category": category,
            "Status": status
        }
        results.append(result)
    
    return results

def write_results_to_csv(results: List[Dict[str, str]], filename: str = "vendor_analysis_output.csv") -> None:
    """Write vendor analysis results to CSV file"""
    if not results:
        print("No results to write.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Vendor analysis results written to {filename}")

def display_vendor_summary(results: List[Dict[str, str]]) -> None:
    """Display a summary of vendor analysis results"""
    print("\n=== VENDOR ANALYSIS SUMMARY ===")
    
    # Count by category
    categories = {}
    vendors_found = set()
    vendors_not_found = set()
    
    for result in results:
        category = result["Vendor Category"]
        categories[category] = categories.get(category, 0) + 1
        
        if result["Status"] == "Found in Database":
            vendors_found.add(result["Vendor Name"])
        else:
            vendors_not_found.add(result["Vendor Name"])
    
    print(f"Total models analyzed: {len(results)}")
    print(f"Unique vendors found: {len(vendors_found)}")
    print(f"Vendors not in database: {len(vendors_not_found)}")
    
    print("\nVendor Categories:")
    for category, count in categories.items():
        print(f"  {category}: {count}")
    
    if vendors_not_found:
        print(f"\nVendors not in database: {', '.join(vendors_not_found)}")

def main():
    """Main function to run vendor analysis"""
    print("=== AWS BEDROCK VENDOR ANALYSIS ===")
    
    # Fetch and parse model names from AWS Bedrock catalog
    print("Fetching AWS Bedrock catalog...")
    html = fetch_bedrock_catalog()
    
    if not html:
        print("Failed to fetch catalog. Using sample model names.")
        model_names = [
            "Claude 3.7 Sonnet",
            "Llama 3.1 405B Instruct", 
            "Mistral 7B Instruct",
            "Nova Lite",
            "DeepSeek-R1"
        ]
    else:
        print("Parsing model names from catalog...")
        model_names = parse_bedrock_models(html)
        print(f"Found {len(model_names)} models in catalog")
    
    # Analyze vendors from model names
    print(f"\nAnalyzing {len(model_names)} models for vendor information...")
    results = analyze_vendors_from_models(model_names)
    
    # Display results
    print("\nVendor Analysis Results:")
    for result in results:
        print(f"Model: {result['Model Name']}")
        print(f"  Vendor: {result['Vendor Name']} ({result['Company Name']})")
        print(f"  Formation Year: {result['Formation Year']}")
        print(f"  Age: {result['Age (Years)']} years")
        print(f"  Category: {result['Vendor Category']}")
        print(f"  Status: {result['Status']}")
        print()
    
    # Display summary
    display_vendor_summary(results)
    
    # Write results to CSV
    write_results_to_csv(results)

if __name__ == "__main__":
    main()
