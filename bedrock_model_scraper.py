import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv

# Sample list of model names
MODEL_NAMES = [
    "Claude 3.7 Sonnet",
    "Llama 3.1 405B Instruct",
    "Mistral 7B Instruct"
]


# Placeholder for scraping logic
def get_model_deployment_info(model_names):
    # TODO: Implement scraping logic for AWS Bedrock's catalog
    # Return a list of dicts: [{"Model Name": ..., "Closed/Open": ..., "Cloud/On-Premises": ...}, ...]
    return [{"Model Name": name, "Closed/Open": "?", "Cloud/On-Premises": "?"} for name in model_names]

def fetch_bedrock_catalog():
    url = "https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html"
    response = requests.get(url)
    print("HTTP status code:", response.status_code)
    print("First 500 characters of HTML:\n", response.text[:500])
    return response.text

def parse_bedrock_models(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        print("No table found in the page!")
        return []

    rows = table.find_all("tr")
    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    model_dicts = []
    for row in rows[1:]:
        cols = row.find_all("td")
        if cols:
            model_info = {headers[i]: cols[i].get_text(strip=True) for i in range(min(len(headers), len(cols)))}
            model_dicts.append(model_info)
    print("Table headers:", headers)
    for model in model_dicts[:5]:
        print("Sample model row:", model)
    return model_dicts

def match_input_models(input_models, catalog_models):
    print("\nMatching input models to catalog (exact match)...")
    catalog_dict = {model.get("Model name", ""): model for model in catalog_models}
    results = []
    for input_name in input_models:
        model = catalog_dict.get(input_name)
        if model:
            regions = model.get("Regions supported", "")
            if regions.strip():
                deployment_type = "Cloud"
            else:
                deployment_type = "?"
            results.append({
                "Model Name": input_name,
                "Deployment Type": deployment_type,
                "Regions Supported": regions
            })
        else:
            results.append({
                "Model Name": input_name,
                "Deployment Type": "?",
                "Regions Supported": "?"
            })
    return results

def write_results_to_csv(results, filename="deployment_types.csv"):
    if not results:
        print("No results to write.")
        return
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Results written to {filename}")

def main():
    print("Model names to look up:")
    for name in MODEL_NAMES:
        print("-", name)
    print("\nFetching AWS Bedrock catalog page...")
    html = fetch_bedrock_catalog()
    print("\nParsing model table...")
    catalog_models = parse_bedrock_models(html)
    results = match_input_models(MODEL_NAMES, catalog_models)
    print("\nDeployment Type Table:")
    print(tabulate(results, headers="keys", tablefmt="github"))
    write_results_to_csv(results)

if __name__ == "__main__":
    main() 