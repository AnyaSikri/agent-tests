import csv
from typing import List, Dict

# Simple cost categories
COST_CATEGORIES = {
    "Low Cost": {
        "max_rate": 0.001, 
        "description": "≤ $0.001 per 1K tokens"
    },
    "Medium Cost": {
        "min_rate": 0.001, 
        "max_rate": 0.005, 
        "description": "$0.001 - $0.005 per 1K tokens"
    },
    "High Cost": {
        "min_rate": 0.005, 
        "description": "> $0.005 per 1K tokens"
    }
}

# Core models with their pricing (simplified)
MODEL_PRICING = {
    "Claude 3.7 Sonnet": {
        "input": 0.003, 
        "output": 0.015
    },
    "Llama 3.1 405B Instruct": {
        "input": 0.0008, 
        "output": 0.0008
    },
    "Mistral 7B Instruct": {
        "input": 0.00015, 
        "output": 0.0002
    },
    "Nova Lite": {
        "input": 0.0001, 
        "output": 0.0001
    },
    "DeepSeek-R1": {
        "input": 0.006, 
        "output": 0.006
    }
}


def categorize_cost(input_rate: float) -> str:
    """Simple cost categorization based on input rate"""
    if input_rate <= COST_CATEGORIES["Low Cost"]["max_rate"]:
        return "Low Cost"
    elif input_rate <= COST_CATEGORIES["Medium Cost"]["max_rate"]:
        return "Medium Cost"
    else:
        return "High Cost"


def categorize_total_cost(total_rate: float) -> str:
    """Cost categorization based on total rate (input + output)"""
    if total_rate <= 0.002:  # $0.002 per 2K tokens
        return "Low Cost"
    elif total_rate <= 0.01:  # $0.01 per 2K tokens
        return "Medium Cost"
    else:
        return "High Cost"


def analyze_costs() -> List[Dict[str, str]]:
    """Analyze costs for all models"""
    results = []
    
    for model_name, pricing in MODEL_PRICING.items():
        input_rate = pricing["input"]
        output_rate = pricing["output"]
        total_cost = input_rate + output_rate
        input_category = categorize_cost(input_rate)
        total_category = categorize_total_cost(total_cost)
        
        results.append({
            "Model": model_name,
            "Input Cost": f"${input_rate:.6f}",
            "Output Cost": f"${output_rate:.6f}",
            "Total Cost": f"${total_cost:.6f}",
            "Input Category": input_category,
            "Total Category": total_category,
            "Description": COST_CATEGORIES[input_category]["description"]
        })
    
    return results


def save_to_csv(results: List[Dict[str, str]], filename: str = "cost_analysis.csv"):
    """Save results to CSV"""
    if not results:
        print("No results to save.")
        return
        
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def main():
    print("LLM Cost Analysis")
    print("=" * 40)
    
    # Analyze costs
    results = analyze_costs()
    
    # Display results
    for result in results:
        print(f"\n{result['Model']}")
        print(f"  Input: {result['Input Cost']} per 1K tokens")
        print(f"  Output: {result['Output Cost']} per 1K tokens")
        print(f"  Total: {result['Total Cost']} per 2K tokens")
        print(f"  Input Category: {result['Input Category']}")
        print(f"  Total Category: {result['Total Category']}")
    
    # Save to CSV
    save_to_csv(results)
    
    # Summary
    print(f"\nSummary (by Input Cost):")
    input_categories = [r["Input Category"] for r in results]
    for category in COST_CATEGORIES:
        count = input_categories.count(category)
        if count > 0:
            print(f"  {category}: {count} model(s)")
    
    print(f"\nSummary (by Total Cost):")
    total_categories = [r["Total Category"] for r in results]
    for category in COST_CATEGORIES:
        count = total_categories.count(category)
        if count > 0:
            print(f"  {category}: {count} model(s)")


if __name__ == "__main__":
    main() 
    