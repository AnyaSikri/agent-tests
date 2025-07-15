import urllib.request
import csv

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("BeautifulSoup (bs4) is required. Install it with 'pip install beautifulsoup4'.")


def fetch_bedrock_catalog() -> str:
    """
    Gets the AWS Bedrock models catalog HTML.
    Returns:
        str: HTML content of the catalog.
    """
    url = "https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html"
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    return html


def parse_bedrock_models(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    models = []
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        for row in table.find_all("tr")[1:]:  
            cells = row.find_all("td")
            if len(cells) != len(headers):
                continue
            model_info = {headers[i]: cells[i].get_text(strip=True) for i in range(len(headers))}
            models.append(model_info)
    return models


def check_hybrid_capability(model: dict) -> bool:
    """
    checks if the model supports hybrid deployment based on its information.
    args:
        model (dict): Model information dictionary.
    returns:
        bool: True if hybrid deployment is supported, False otherwise.
    """
    # Keywords that suggest hybrid deployment
    hybrid_keywords = [
        "VPC endpoint", "Private deployment", "Custom model hosting", "Outposts compatible",
        "Provisioned throughput", "Dedicated instance", "Amazon VPC integration",
        "AWS PrivateLink", "Bring your own VPC", "Network isolation"
    ]
    for value in model.values():
        for keyword in hybrid_keywords:
            if keyword.lower() in str(value).lower():
                return True
    return False


def get_deployment_type(model: dict) -> str:
    """
    infers deployment type (Cloud, On-premises, Hybrid, Unknown) for a model.
    args:
        model (dict): Model information dictionary.
    returns:
        str: Deployment type.
    """
    if check_hybrid_capability(model):
        return "Hybrid"
    regions = model.get("Regions supported", "")
    if regions:
        # If there are AWS regions listed, it's Cloud
        return "Cloud"
    # If no regions and no hybrid clues, assume On-premises
    return "On-premises"


def get_model_deployment_info(model_names: list[str], catalog_models: list[dict]) -> list[dict]:
    """
    gets deployment info for input models.
    args:
        model_names (list[str]): List of model names to check.
        catalog_models (list[dict]): List of all catalog model dictionaries.
    returns:
        list[dict]: List of dicts with model name and deployment type.
    """
    results = []
    for name in model_names:
        # Find the first model in the catalog with a matching name
        model = next((m for m in catalog_models if m.get("Model name", "") == name), None)
        if model:
            deployment_type = get_deployment_type(model)
        else:
            deployment_type = "Unknown"
        results.append({"Model name": name, "Deployment type": deployment_type})
    return results


def write_results_to_csv(results: list[dict], filename: str = "deployment.csv") -> None:
    """
    Writes the results to a CSV file.
    Args:
        results (list[dict]): List of model deployment info dicts.
        filename (str, optional): Output CSV filename. Defaults to 'deployment.csv'.
    Returns:
        None
    """
    if not results:
        return
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    html = fetch_bedrock_catalog()
    models = parse_bedrock_models(html)
    print(f"Total models found: {len(models)}")
    for m in models[:3]:
        name = m.get("Model name", "Unknown")
        print(f"Model: {name}")
        print(f"  Hybrid capable: {check_hybrid_capability(m)}")
        print(f"  Deployment type: {get_deployment_type(m)}")
    # Write all models' deployment info to CSV
    model_names = [m.get("Model name", "Unknown") for m in models]
    results = get_model_deployment_info(model_names, models)
    write_results_to_csv(results)
    print(f"Wrote deployment info for {len(results)} models to deployment.csv")
