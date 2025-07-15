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
    """
    Parses the AWS Bedrock catalog HTML to extract model information.
    Args:
        html (str): HTML content of the catalog.
    Returns:
        list[dict]: List of model info dictionaries.
    """
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


def get_modality_info(models: list[dict]) -> list[dict]:
    """
    For each model, extract only model name, input modalities, and output modalities.
    Args:
        models (list[dict]): List of model dictionaries from the catalog.
    Returns:
        list[dict]: List of dicts with model name, input modalities, and output modalities.
    """
    results = []
    for m in models:
        name = m.get("Model name", "Unknown")
        input_mod = m.get("Input modalities", "").strip()
        output_mod = m.get("Output modalities", "").strip()
        results.append({
            "Model name": name,
            "Input modalities": input_mod,
            "Output modalities": output_mod
        })
    return results


def write_modality_results_to_csv(results: list[dict], filename: str = "modality_output.csv") -> None:
    """
    Writes the modality results to a CSV file.
    Args:
        results (list[dict]): List of model modality info dicts.
        filename (str, optional): Output CSV filename. Defaults to 'modality_output.csv'.
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
    # Print a few sample modality results
    modality_results = get_modality_info(models)
    for m in modality_results[:3]:
        print(f"Model: {m['Model name']}")
        print(f"  Input modalities: {m['Input modalities']}")
        print(f"  Output modalities: {m['Output modalities']}")
    # Write all models' modality info to CSV
    write_modality_results_to_csv(modality_results)
    print(f"Wrote modality info for {len(modality_results)} models to modality_output.csv")
