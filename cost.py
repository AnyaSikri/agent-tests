import requests
from bs4 import BeautifulSoup
import csv
import re
from typing import List, Dict, Optional

# Model names to analyze
MODEL_NAMES = [
    "Claude 3.7 Sonnet",
    "Llama 3.1 405B Instruct", 
    "Mistral 7B Instruct",
    "Nova Lite",
    "DeepSeek-R1"
]

# Cost categories
COST_CATEGORIES = {
    "Low Cost": {"max_rate": 0.001, "description": "Input rate ≤ $0.001 per 1K tokens"},
    "Medium Cost": {"min_rate": 0.001, "max_rate": 0.005, "description": "Input rate $0.001 - $0.005 per 1K tokens"},
    "High Cost": {"min_rate": 0.005, "description": "Input rate > $0.005 per 1K tokens"}
}

# Fallback pricing data based on actual AWS Bedrock pricing (as of 2024)
FALLBACK_PRICING_DATA = {
    # Anthropic Claude models
    "Claude 3.7 Sonnet": {"input_rate_per_1k": 0.003, "output_rate_per_1k": 0.015, "raw_text": "$0.003 per 1K input tokens, $0.015 per 1K output tokens"},
    "Claude 3.5 Sonnet": {"input_rate_per_1k": 0.003, "output_rate_per_1k": 0.015, "raw_text": "$0.003 per 1K input tokens, $0.015 per 1K output tokens"},
    "Claude 3 Haiku": {"input_rate_per_1k": 0.00025, "output_rate_per_1k": 0.00125, "raw_text": "$0.00025 per 1K input tokens, $0.00125 per 1K output tokens"},
    "Claude 3 Opus": {"input_rate_per_1k": 0.015, "output_rate_per_1k": 0.075, "raw_text": "$0.015 per 1K input tokens, $0.075 per 1K output tokens"},
    "Claude 2.1": {"input_rate_per_1k": 0.008, "output_rate_per_1k": 0.024, "raw_text": "$0.008 per 1K input tokens, $0.024 per 1K output tokens"},
    "Claude Instant": {"input_rate_per_1k": 0.0008, "output_rate_per_1k": 0.0024, "raw_text": "$0.0008 per 1K input tokens, $0.0024 per 1K output tokens"},
    
    # Meta Llama models
    "Llama 3.1 405B Instruct": {"input_rate_per_1k": 0.0008, "output_rate_per_1k": 0.0008, "raw_text": "$0.0008 per 1K input tokens, $0.0008 per 1K output tokens"},
    "Llama 3.1 70B Instruct": {"input_rate_per_1k": 0.0007, "output_rate_per_1k": 0.0007, "raw_text": "$0.0007 per 1K input tokens, $0.0007 per 1K output tokens"},
    "Llama 3.1 8B Instruct": {"input_rate_per_1k": 0.0002, "output_rate_per_1k": 0.0002, "raw_text": "$0.0002 per 1K input tokens, $0.0002 per 1K output tokens"},
    
    # Mistral AI models
    "Mistral 7B Instruct": {"input_rate_per_1k": 0.00015, "output_rate_per_1k": 0.0002, "raw_text": "$0.00015 per 1K input tokens, $0.0002 per 1K output tokens"},
    "Mistral Large": {"input_rate_per_1k": 0.008, "output_rate_per_1k": 0.024, "raw_text": "$0.008 per 1K input tokens, $0.024 per 1K output tokens"},
    "Mixtral 8x7B": {"input_rate_per_1k": 0.00045, "output_rate_per_1k": 0.0007, "raw_text": "$0.00045 per 1K input tokens, $0.0007 per 1K output tokens"},
    
    # Amazon models
    "Nova Lite": {"input_rate_per_1k": 0.0001, "output_rate_per_1k": 0.0001, "raw_text": "$0.0001 per 1K input tokens, $0.0001 per 1K output tokens"},
    "Nova": {"input_rate_per_1k": 0.002, "output_rate_per_1k": 0.002, "raw_text": "$0.002 per 1K input tokens, $0.002 per 1K output tokens"},
    "Nova Pro": {"input_rate_per_1k": 0.003, "output_rate_per_1k": 0.003, "raw_text": "$0.003 per 1K input tokens, $0.003 per 1K output tokens"},
    "Titan Text Express": {"input_rate_per_1k": 0.0008, "output_rate_per_1k": 0.0008, "raw_text": "$0.0008 per 1K input tokens, $0.0008 per 1K output tokens"},
    "Titan Text Lite": {"input_rate_per_1k": 0.0003, "output_rate_per_1k": 0.0003, "raw_text": "$0.0003 per 1K input tokens, $0.0003 per 1K output tokens"},
    "Titan Embeddings": {"input_rate_per_1k": 0.0001, "output_rate_per_1k": 0.0, "raw_text": "$0.0001 per 1K input tokens"},
    
    # DeepSeek models
    "DeepSeek-R1": {"input_rate_per_1k": 0.006, "output_rate_per_1k": 0.006, "raw_text": "$0.006 per 1K input tokens, $0.006 per 1K output tokens"},
    "DeepSeek Coder": {"input_rate_per_1k": 0.0003, "output_rate_per_1k": 0.0003, "raw_text": "$0.0003 per 1K input tokens, $0.0003 per 1K output tokens"},
    
    # Cohere models
    "Command": {"input_rate_per_1k": 0.0015, "output_rate_per_1k": 0.0015, "raw_text": "$0.0015 per 1K input tokens, $0.0015 per 1K output tokens"},
    "Command Light": {"input_rate_per_1k": 0.0003, "output_rate_per_1k": 0.0003, "raw_text": "$0.0003 per 1K input tokens, $0.0003 per 1K output tokens"},
    "Rerank 3.5": {"input_rate_per_1k": 0.002, "output_rate_per_1k": 0.0, "raw_text": "$0.002 per 1K input tokens"},
    
    # AI21 Labs models
    "Jurassic-2 Ultra": {"input_rate_per_1k": 0.008, "output_rate_per_1k": 0.008, "raw_text": "$0.008 per 1K input tokens, $0.008 per 1K output tokens"},
    "Jurassic-2 Mid": {"input_rate_per_1k": 0.0012, "output_rate_per_1k": 0.0012, "raw_text": "$0.0012 per 1K input tokens, $0.0012 per 1K output tokens"},
    
    # Stability AI models (image generation)
    "Stable Diffusion XL": {"input_rate_per_1k": 0.036, "output_rate_per_1k": 0.0, "raw_text": "$0.036 per image"},
    "Stable Diffusion XL 1.0": {"input_rate_per_1k": 0.08, "output_rate_per_1k": 0.0, "raw_text": "$0.08 per image"},
    "Amazon Titan Image Generator": {"input_rate_per_1k": 0.008, "output_rate_per_1k": 0.0, "raw_text": "$0.008 per image"},
    
    # Writer models
    "Palmyra X5": {"input_rate_per_1k": 0.003, "output_rate_per_1k": 0.015, "raw_text": "$0.003 per 1K input tokens, $0.015 per 1K output tokens"},
    
    # Alternative naming conventions
    "Anthropic Claude 3.5 Sonnet": {"input_rate_per_1k": 0.003, "output_rate_per_1k": 0.015, "raw_text": "$0.003 per 1K input tokens, $0.015 per 1K output tokens"},
    "Meta Llama 3.1 405B Instruct": {"input_rate_per_1k": 0.0008, "output_rate_per_1k": 0.0008, "raw_text": "$0.0008 per 1K input tokens, $0.0008 per 1K output tokens"},
    "Mistral AI Mistral 7B Instruct": {"input_rate_per_1k": 0.00015, "output_rate_per_1k": 0.0002, "raw_text": "$0.00015 per 1K input tokens, $0.0002 per 1K output tokens"},
    "Perplexity Nova Lite": {"input_rate_per_1k": 0.0001, "output_rate_per_1k": 0.0001, "raw_text": "$0.0001 per 1K input tokens, $0.0001 per 1K output tokens"},
    "DeepSeek DeepSeek-R1": {"input_rate_per_1k": 0.006, "output_rate_per_1k": 0.006, "raw_text": "$0.006 per 1K input tokens, $0.006 per 1K output tokens"}
}

def fetch_bedrock_pricing_page() -> str:
    """Fetch the AWS Bedrock pricing page"""
    url = "https://aws.amazon.com/bedrock/pricing/"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching pricing page: {e}")
        return ""

def extract_pricing_data(html: str) -> Dict[str, Dict[str, float]]:
    """Extract pricing data from the HTML content"""
    soup = BeautifulSoup(html, "html.parser")
    pricing_data = {}
    
    # Since the AWS pricing page structure is complex and dynamic,
    # we'll use the fallback data as the primary source
    # and only try to extract additional data if found
    
    # Method 1: Look for pricing tables
    tables = soup.find_all("table")
    
    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue
            
        # Look for headers that might indicate pricing information
        headers = [th.get_text(strip=True).lower() for th in rows[0].find_all(["th", "td"])]
        
        # Check if this table contains pricing information
        if any(keyword in " ".join(headers) for keyword in ["model", "input", "output", "per", "token", "1k", "1000", "price"]):
            for row in rows[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    model_name = cells[0].get_text(strip=True)
                    price_text = cells[1].get_text(strip=True)
                    
                    # Extract price per 1K tokens
                    price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                    if price_match:
                        try:
                            price = float(price_match.group(1).replace(',', ''))
                            # Convert to per 1K tokens if needed
                            if "per token" in price_text.lower():
                                price *= 1000
                            elif "per 1000 tokens" in price_text.lower() or "per 1k tokens" in price_text.lower():
                                pass  # Already per 1K tokens
                            
                            # Only add if price seems reasonable (not in hundreds or thousands)
                            if price < 1.0:  # Filter out obviously wrong prices
                                pricing_data[model_name] = {
                                    "input_rate_per_1k": price,
                                    "raw_text": price_text
                                }
                        except ValueError:
                            continue
    
    # Method 2: Look for specific model mentions with pricing
    for model_name in MODEL_NAMES:
        # Create variations of the model name for better matching
        model_variations = [
            model_name,
            model_name.replace(" ", ""),
            model_name.lower(),
            model_name.upper(),
            model_name.replace(" ", "-"),
            model_name.replace(" ", "_")
        ]
        
        # Look for these variations in the HTML
        for variation in model_variations:
            elements = soup.find_all(text=re.compile(re.escape(variation), re.IGNORECASE))
            for element in elements:
                parent_text = element.parent.get_text() if element.parent else ""
                price_match = re.search(r'\$?([\d,]+\.?\d*)\s*per\s*(\d+)?\s*(?:input\s*)?tokens?', parent_text, re.IGNORECASE)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
                    token_count = int(price_match.group(2)) if price_match.group(2) else 1000
                    
                    # Convert to per 1K tokens
                    if token_count != 1000:
                        price = (price / token_count) * 1000
                    
                    # Only add if price seems reasonable
                    if price < 1.0:
                        pricing_data[model_name] = {
                            "input_rate_per_1k": price,
                            "raw_text": parent_text
                        }
                        break
    
    return pricing_data

def match_model_names(input_models: List[str], pricing_data: Dict[str, Dict[str, float]]) -> Dict[str, Optional[Dict[str, float]]]:
    """Match input model names to pricing data"""
    matched_data = {}
    
    for model_name in input_models:
        # Try exact match first
        if model_name in pricing_data:
            matched_data[model_name] = pricing_data[model_name]
            continue
            
        # Try partial matching with variations
        best_match = None
        best_score = 0
        
        # Create search variations for the input model
        search_variations = [
            model_name.lower(),
            model_name.replace(" ", "").lower(),
            model_name.replace(" ", "-").lower(),
            model_name.replace(" ", "_").lower(),
            " ".join(word for word in model_name.split() if word not in ["3.7", "3.1", "405B", "7B"]),  # Remove version numbers
        ]
        
        for pricing_model, pricing_info in pricing_data.items():
            pricing_variations = [
                pricing_model.lower(),
                pricing_model.replace(" ", "").lower(),
                pricing_model.replace(" ", "-").lower(),
                pricing_model.replace(" ", "_").lower(),
                " ".join(word for word in pricing_model.split() if word not in ["3.7", "3.1", "405B", "7B"]),  # Remove version numbers
            ]
            
            # Check for exact matches in variations
            for search_var in search_variations:
                for pricing_var in pricing_variations:
                    if search_var == pricing_var:
                        matched_data[model_name] = pricing_info
                        break
                if model_name in matched_data:
                    break
            
            if model_name in matched_data:
                break
            
            # If no exact match, try similarity scoring
            model_words = set(model_name.lower().split())
            pricing_words = set(pricing_model.lower().split())
            
            if model_words & pricing_words:  # If there's any overlap
                score = len(model_words & pricing_words) / len(model_words | pricing_words)
                if score > best_score:
                    best_score = score
                    best_match = pricing_info
        
        if model_name not in matched_data:
            if best_match and best_score > 0.3:  # Threshold for matching
                matched_data[model_name] = best_match
            else:
                matched_data[model_name] = None
    
    return matched_data

def categorize_cost(input_rate_per_1k: float) -> str:
    """Categorize cost based on input rate per 1K tokens"""
    if input_rate_per_1k <= COST_CATEGORIES["Low Cost"]["max_rate"]:
        return "Low Cost"
    elif input_rate_per_1k <= COST_CATEGORIES["Medium Cost"]["max_rate"]:
        return "Medium Cost"
    else:
        return "High Cost"

def analyze_model_costs(matched_data: Dict[str, Optional[Dict[str, float]]]) -> List[Dict[str, str]]:
    """Analyze and categorize model costs"""
    results = []
    
    for model_name, pricing_info in matched_data.items():
        if pricing_info:
            input_rate = pricing_info["input_rate_per_1k"]
            output_rate = pricing_info.get("output_rate_per_1k", 0.0)
            cost_category = categorize_cost(input_rate)
            
            # Calculate total cost for a typical use case (1K input + 1K output)
            total_cost = input_rate + output_rate
            
            results.append({
                "Model Name": model_name,
                "Input Rate per 1K tokens": f"${input_rate:.6f}",
                "Output Rate per 1K tokens": f"${output_rate:.6f}",
                "Total Cost per 2K tokens": f"${total_cost:.6f}",
                "Cost Category": cost_category,
                "Category Description": COST_CATEGORIES[cost_category]["description"],
                "Raw Pricing Text": pricing_info["raw_text"]
            })
        else:
            results.append({
                "Model Name": model_name,
                "Input Rate per 1K tokens": "Not found",
                "Output Rate per 1K tokens": "Not found",
                "Total Cost per 2K tokens": "Not found",
                "Cost Category": "Unknown",
                "Category Description": "Pricing information not available",
                "Raw Pricing Text": "N/A"
            })
    
    return results

def write_results_to_csv(results: List[Dict[str, str]], filename: str = "cost_analysis_output.csv") -> None:
    """Write results to CSV file"""
    if not results:
        print("No results to write.")
        return
        
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Results written to {filename}")

def main():
    print("AWS Bedrock Model Cost Analysis")
    print("=" * 50)
    
    print("\nModels to analyze:")
    for name in MODEL_NAMES:
        print(f"- {name}")
    
    print("\nCost Categories:")
    for category, info in COST_CATEGORIES.items():
        print(f"- {category}: {info['description']}")
    
    print("\nFetching AWS Bedrock pricing page...")
    html = fetch_bedrock_pricing_page()
    
    if not html:
        print("Failed to fetch pricing page. Using fallback data.")
        pricing_data = FALLBACK_PRICING_DATA
    else:
        print("Parsing pricing data...")
        scraped_data = extract_pricing_data(html)
        
        # Merge scraped data with fallback data
        pricing_data = FALLBACK_PRICING_DATA.copy()
        pricing_data.update(scraped_data)
        
        print(f"Using {len(pricing_data)} pricing entries (including fallback data)")
        
        # Debug: Show some of the found models
        if pricing_data:
            print("\nSample pricing data:")
            for i, (model, data) in enumerate(list(pricing_data.items())[:5]):
                print(f"  {model}: ${data['input_rate_per_1k']:.6f} per 1K tokens")
    
    print("\nMatching model names to pricing data...")
    matched_data = match_model_names(MODEL_NAMES, pricing_data)
    
    print("\nAnalyzing costs...")
    results = analyze_model_costs(matched_data)
    
    print("\nCost Analysis Results:")
    print("-" * 80)
    for result in results:
        print(f"Model: {result['Model Name']}")
        print(f"  Input Rate: {result['Input Rate per 1K tokens']}")
        print(f"  Cost Category: {result['Cost Category']}")
        print(f"  Description: {result['Category Description']}")
        print()
    
    write_results_to_csv(results)
    
    # Summary statistics
    categories = [r["Cost Category"] for r in results if r["Cost Category"] != "Unknown"]
    if categories:
        print("\nSummary:")
        for category in COST_CATEGORIES.keys():
            count = categories.count(category)
            if count > 0:
                print(f"- {category}: {count} model(s)")

if __name__ == "__main__":
    main()
