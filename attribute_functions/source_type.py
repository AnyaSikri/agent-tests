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


def get_provider_source_type(provider: str, provider_license_map: dict) -> str:
    """
    Maps a provider to its source type (open/closed) using a dictionary.
    Args:
        provider (str): Provider name from the catalog.
        provider_license_map (dict): Mapping of provider names to 'open' or 'closed'.
    Returns:
        str: 'open', 'closed', or 'unknown'.
    """
    if not provider:
        return "unknown"
    return provider_license_map.get(provider.strip(), "unknown")


def get_llm_source_type_info(llm_names: list[str], catalog_models: list[dict], provider_license_map: dict) -> list[dict]:
    """
    Gets source type info for input LLMs using the Provider column and a mapping dict.
    Args:
        llm_names (list[str]): List of LLM names to check.
        catalog_models (list[dict]): List of all catalog model dictionaries.
        provider_license_map (dict): Mapping of provider names to 'open' or 'closed'.
    Returns:
        list[dict]: List of dicts with LLM name and source type.
    """
    results = []
    for name in llm_names:
        model = next((m for m in catalog_models if m.get("Model name", "") == name), None)
        if model:
            provider = model.get("Provider", "")
            source_type = get_provider_source_type(provider, provider_license_map)
        else:
            source_type = "unknown"
        results.append({"LLM name": name, "Source type": source_type})
    return results


def write_llm_source_type_to_csv(results: list[dict], filename: str = "source_type.csv") -> None:
    """
    Writes the LLM source type results to a CSV file.
    Args:
        results (list[dict]): List of LLM source type info dicts.
        filename (str, optional): Output CSV filename. Defaults to 'source_type.csv'.
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
    
    # Example provider_license_map (expand as needed)
    provider_license_map = {
        "Meta": "open",
        "Mistral": "open",
        "Cohere": "closed",
        "Anthropic": "closed",
        "AI21 Labs": "closed",
        "Amazon": "closed",
        "Stability AI": "open",
        "StabilityAI": "open",
        "Stability": "open",
        "Google": "closed",
        "Jurassic": "closed",
        # Add more mappings as needed
    }
    
    # Get all model names and analyze source types (deduplicated)
    seen_models = set()
    llm_names = []
    for m in models:
        name = m.get("Model name", "Unknown")
        if name not in seen_models:
            seen_models.add(name)
            llm_names.append(name)
    llm_source_type_results = get_llm_source_type_info(llm_names, models, provider_license_map)
    write_llm_source_type_to_csv(llm_source_type_results)
    print(f"Wrote LLM source type info for {len(llm_source_type_results)} models to source_type.csv")
    
    # Print sample results
    print("\nSample source type analysis:")
    for result in llm_source_type_results[:5]:
        print(f"  {result['LLM name']}: {result['Source type']}")
