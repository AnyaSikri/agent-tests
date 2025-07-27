import urllib.request
import csv
import difflib

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("BeautifulSoup (bs4) is required. Install it with 'pip install beautifulsoup4'.")

def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    return html

def parse_master_model_ids(html: str) -> list[dict]:
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
            # Add Model ID for matching
            if "Model ID" in model_info:
                model_info["model-id"] = model_info["Model ID"]
            elif "Model Id" in model_info:
                model_info["model-id"] = model_info["Model Id"]
            elif "Model" in model_info:
                model_info["model-id"] = model_info["Model"]
            else:
                model_info["model-id"] = cells[0].get_text(strip=True)
            models.append(model_info)
    return models

def parse_batch_enabled_models_table(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    models = []
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if not ("Provider" in headers and "Model" in headers):
            continue
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) != len(headers):
                continue
            model_info = {headers[i]: cells[i].get_text(strip=True) for i in range(len(headers))}
            models.append(model_info)
    return models

def match_batch_models_to_master(batch_models: list[dict], master_models: list[dict]) -> set[str]:
    batch_model_ids = set()
    for batch in batch_models:
        batch_provider = batch.get("Provider", "").lower()
        batch_model = batch.get("Model", "").lower()
        # Try to find the best match in master_models
        candidates = []
        for m in master_models:
            provider = m.get("Provider", m.get("Model provider", "")).lower()
            model_name = m.get("Model name", m.get("Model", "")).lower()
            model_id = m.get("model-id", "").lower()
            # Heuristic: match if provider and model name are both in the master model info
            if batch_provider in provider and batch_model in model_name:
                candidates.append(m["model-id"])
            elif batch_provider in provider and batch_model in model_id:
                candidates.append(m["model-id"])
        # If multiple candidates, use difflib to get the closest
        if candidates:
            best = difflib.get_close_matches(batch_model, candidates, n=1)
            if best:
                batch_model_ids.add(best[0])
            else:
                batch_model_ids.add(candidates[0])
    return batch_model_ids

def cross_reference_batch_support(master_models: list[dict], batch_model_ids: set[str]) -> list[dict]:
    labeled = []
    for m in master_models:
        model_id = m["model-id"]
        support_type = "batch-supported" if model_id in batch_model_ids else "real-time only"
        labeled.append({"model-id": model_id, "support_type": support_type})
    return labeled

def write_labeled_models_to_csv(labeled_list: list[dict], filename: str = "latency_label.csv") -> None:
    if not labeled_list:
        return
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=labeled_list[0].keys())
        writer.writeheader()
        writer.writerows(labeled_list)

if __name__ == "__main__":
    master_url = "https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html"
    batch_url = "https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference-supported.html"
    print("Fetching master model catalog...")
    master_html = fetch_html(master_url)
    master_models = parse_master_model_ids(master_html)
    print(f"Total models in master catalog: {len(master_models)}")
    print("Fetching batch-enabled model list...")
    batch_html = fetch_html(batch_url)
    batch_models = parse_batch_enabled_models_table(batch_html)
    print(f"Total batch-enabled models (table rows): {len(batch_models)}")
    batch_model_ids = match_batch_models_to_master(batch_models, master_models)
    print(f"Matched batch-enabled model IDs: {len(batch_model_ids)}")
    labeled_list = cross_reference_batch_support(master_models, batch_model_ids)
    print("Sample labeled models:")
    for m in labeled_list[:3]:
        print(f"  {m['model-id']}: {m['support_type']}")
    write_labeled_models_to_csv(labeled_list)
    print(f"Wrote batch support info for {len(labeled_list)} models to latency_label.csv")



