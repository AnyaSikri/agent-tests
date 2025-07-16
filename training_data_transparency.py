import csv
import requests
from bs4 import BeautifulSoup

AWS_BEDROCK_MODELS_URL = 'https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html'

def fetch_bedrock_catalog() -> str:
    response = requests.get(AWS_BEDROCK_MODELS_URL, timeout=10)
    response.raise_for_status()
    return response.text

def parse_bedrock_models(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    models = []
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if 'provider' in headers and 'model name' in headers:
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                if len(cells) != len(headers):
                    continue
                model_info = {headers[i]: cells[i].get_text(strip=True) for i in range(len(headers))}
                # Try to extract documentation link from the appropriate cell
                doc_link = None
                # Prefer a documentation or link column if present
                for i, h in enumerate(headers):
                    if 'documentation' in h or 'link' in h:
                        a_tag = cells[i].find('a', href=True)
                        if a_tag:
                            doc_link = a_tag['href']
                            if not doc_link.startswith('http'):
                                doc_link = 'https://docs.aws.amazon.com/bedrock/latest/userguide/' + doc_link.lstrip('./')
                        break
                # Otherwise, try to get link from model name cell
                if not doc_link:
                    name_idx = headers.index('model name')
                    a_tag = cells[name_idx].find('a', href=True)
                    if a_tag:
                        doc_link = a_tag['href']
                        if not doc_link.startswith('http'):
                            doc_link = 'https://docs.aws.amazon.com/bedrock/latest/userguide/' + doc_link.lstrip('./')
                model_info['doc_link'] = doc_link or AWS_BEDROCK_MODELS_URL
                # Normalize keys for downstream use
                model_info['name'] = model_info.get('model name', '')
                model_info['provider'] = model_info.get('provider', '')
                models.append(model_info)
    return models

def fetch_model_doc(doc_link):
    """Fetch and extract main text from the documentation page for the model."""
    try:
        response = requests.get(doc_link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'li'])
        text = '\n'.join(p.get_text(separator=' ', strip=True) for p in paragraphs)
        return text
    except Exception as e:
        print(f"Failed to fetch {doc_link}: {e}")
        return ""

def analyze_transparency(text, model_info=None):
    text_lower = text.lower()
    # Expanded keyword lists
    full_keywords = [
        'trained on', 'dataset', 'corpus', 'pile', 'c4', 'wikipedia', 'openwebtext', 'books', 'common crawl', 'laion', 'refinedweb', 'specific datasets',
        'open dataset', 'public dataset', 'huggingface', 'data sources:'
    ]
    moderate_keywords = [
        'web data', 'internet data', 'public data', 'proprietary data', 'mix of sources', 'large-scale data', 'variety of sources', 'publicly available', 'licensed data',
        'third-party data', 'private data', 'not disclosed', 'not publicly available', 'undisclosed', 'confidential', 'internal data', 'copyrighted data'
    ]
    # Provider-based heuristics
    if model_info:
        provider = model_info.get('provider', '').lower()
        name = model_info.get('name', '').lower()
        if 'stability' in provider or 'stable diffusion' in name:
            return 'Full transparency'
        if 'anthropic' in provider or 'amazon' in provider or 'ai21' in provider or 'writer' in provider:
            # These providers are known to be black box unless proven otherwise
            if any(kw in text_lower for kw in full_keywords):
                return 'Full transparency'
            elif any(kw in text_lower for kw in moderate_keywords):
                return 'Moderate transparency'
            else:
                return 'Black Box (no info)'
    # General logic
    if any(kw in text_lower for kw in full_keywords):
        return 'Full transparency'
    elif any(kw in text_lower for kw in moderate_keywords):
        return 'Moderate transparency'
    else:
        return 'Black Box (no info)'

def write_results_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'provider', 'transparency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def main():
    print("Fetching AWS Bedrock Supported Models catalog...")
    html = fetch_bedrock_catalog()
    models = parse_bedrock_models(html)
    print(f"Found {len(models)} models.")
    results = []
    for model in models:
        print(f"Processing {model['name']} ({model['provider']})...")
        doc_text = fetch_model_doc(model['doc_link'])
        transparency = analyze_transparency(doc_text, model)
        results.append({
            'name': model['name'],
            'provider': model['provider'],
            'transparency': transparency
        })
    write_results_to_csv(results, 'training_data_transparency_output.csv')
    print("Done! Results written to training_data_transparency_output.csv")

if __name__ == "__main__":
    main()



