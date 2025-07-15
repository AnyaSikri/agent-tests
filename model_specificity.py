import urllib.request
import csv

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("BeautifulSoup (bs4) is required. Install it with 'pip install beautifulsoup4'.")

# Define task-specific keywords for classification
# Decision tree keyword lists
TASK_KEYWORDS = [
    "embed", "embedding", "rerank", "image", "video", "canvas", "reel", "diffusion"
]
GENERAL_INDICATORS = [
    "chat", "instruct", "conversation", "assistant", "gpt", "llama", "claude", "sonnet", "haiku"
]
CREATION_KEYWORDS = [
    "generate", "create", "canvas", "reel", "stable", "diffusion"
]

DOMAIN_KEYWORDS = [
    "medical", "health", "biomedical", "legal", "finance", "financial", "biology", "chemistry", "science", "robotics", "education", "tutor", "customer support"
]

def fetch_bedrock_catalog() -> str:
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


def classify_model_specificity(model: dict) -> tuple[str, str]:
    """
    - If model_name contains task_keywords: return "Task-Specific"
    - Elif input_modalities == ["Text"] AND output_modalities == ["Text"]:
        - If model_name contains general_indicators: return "General-Purpose"
        - Else: return "Domain-Specific"
    - Elif multiple_modalities:
        - If model_name contains creation_keywords: return "Task-Specific"
        - Else: return "Domain-Specific"
    Returns (classification, matched_keywords)
    """
    name = model.get("Model name", "").lower()
    input_mod = model.get("Input modalities", "").lower()
    output_mod = model.get("Output modalities", "").lower()
    input_modalities = [m.strip() for m in input_mod.split(",") if m.strip()]
    output_modalities = [m.strip() for m in output_mod.split(",") if m.strip()]
    # 1. Task-specific by name
    matched_task = [kw for kw in TASK_KEYWORDS if kw in name]
    if matched_task:
        return "Task-Specific", ", ".join(matched_task)
    # 2. Text-to-text
    if input_modalities == ["text"] and output_modalities == ["text"]:
        matched_general = [kw for kw in GENERAL_INDICATORS if kw in name]
        if matched_general:
            return "General-Purpose", ", ".join(matched_general)
        else:
            return "Domain-Specific", ""
    # 3. Multiple modalities
    if len(input_modalities) > 1 or len(output_modalities) > 1 or (input_modalities and output_modalities and input_modalities != output_modalities):
        matched_creation = [kw for kw in CREATION_KEYWORDS if kw in name]
        if matched_creation:
            return "Task-Specific", ", ".join(matched_creation)
        else:
            return "Domain-Specific", ""
    # Fallback
    return "Domain-Specific", ""


def get_llm_info(models: list[dict]) -> list[dict]:
    results = []
    for m in models:
        name = m.get("Model name", "Unknown")
        llm = m.get("Provider", m.get("Model provider", "Unknown"))
        classification, matched_keywords = classify_model_specificity(m)
        results.append({
            "Model name": name,
            "LLM": llm,
            "Classification": classification,
            "Matched Keywords": matched_keywords
        })
    return results


def write_llm_results_to_csv(results: list[dict], filename: str = "llm_specificity_output.csv") -> None:
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
    llm_results = get_llm_info(models)
    for m in llm_results[:3]:
        print(f"Model: {m['Model name']}")
        print(f"  LLM: {m['LLM']}")
        print(f"  Classification: {m['Classification']}")
        print(f"  Matched Keywords: {m['Matched Keywords']}")
    write_llm_results_to_csv(llm_results)
    print(f"Wrote LLM specificity info for {len(llm_results)} models to llm_specificity_output.csv")
