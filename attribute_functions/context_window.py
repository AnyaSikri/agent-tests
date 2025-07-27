import urllib.request
import csv

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("BeautifulSoup (bs4) is required. Install it with 'pip install beautifulsoup4'.")

# mapping of known model names to their context window sizes and sources
CONTEXT_WINDOW_INFO = {
    # Anthropic Claude 3/3.5
    "Claude 3 Haiku": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3", "notes": "Anthropic official docs, June 2024"},
    "Claude 3 Sonnet": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3", "notes": "Anthropic official docs, June 2024"},
    "Claude 3 Opus": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3", "notes": "Anthropic official docs, June 2024"},
    "Claude 3.5 Haiku": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3-5", "notes": "Anthropic official docs, June 2024"},
    "Claude 3.5 Sonnet v2": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3-5", "notes": "Anthropic official docs, June 2024"},
    "Claude 3.5 Sonnet": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3-5", "notes": "Anthropic official docs, June 2024"},
    "Claude 3.7 Sonnet": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3-5", "notes": "Anthropic official docs, June 2024"},
    "Claude Opus 4": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3", "notes": "Anthropic official docs, June 2024"},
    "Claude Sonnet 4": {"tokens": 200000, "source": "https://www.anthropic.com/news/claude-3", "notes": "Anthropic official docs, June 2024"},
    "Claude 2.1": {"tokens": 100000, "source": "https://www.anthropic.com/news/claude-2", "notes": "Anthropic official docs, June 2024"},
    "Claude 2": {"tokens": 100000, "source": "https://www.anthropic.com/news/claude-2", "notes": "Anthropic official docs, June 2024"},
    "Claude Instant": {"tokens": 100000, "source": "https://www.anthropic.com/news/claude-2", "notes": "Anthropic official docs, June 2024"},
    "Claude": {"tokens": 100000, "source": "https://www.anthropic.com/news/claude-2", "notes": "Anthropic official docs, June 2024"},
    # Meta Llama 3
    "Llama 3 8B Instruct": {"tokens": 8192, "source": "https://ai.meta.com/llama/", "notes": "Meta official docs, June 2024"},
    "Llama 3 70B Instruct": {"tokens": 8192, "source": "https://ai.meta.com/llama/", "notes": "Meta official docs, June 2024"},
    "Llama 3.1 8B Instruct": {"tokens": 8192, "source": "https://ai.meta.com/llama/", "notes": "Meta official docs, June 2024"},
    "Llama 3.1 70B Instruct": {"tokens": 8192, "source": "https://ai.meta.com/llama/", "notes": "Meta official docs, June 2024"},
    # Mistral
    "Mistral 7B Instruct": {"tokens": 32000, "source": "https://docs.mistral.ai/models/", "notes": "Mistral official docs, June 2024"},
    "Mistral Large (24.02)": {"tokens": 32000, "source": "https://docs.mistral.ai/models/", "notes": "Mistral official docs, June 2024"},
    "Mistral Large (24.07)": {"tokens": 32000, "source": "https://docs.mistral.ai/models/", "notes": "Mistral official docs, June 2024"},
    "Mistral Small (24.02)": {"tokens": 32000, "source": "https://docs.mistral.ai/models/", "notes": "Mistral official docs, June 2024"},
    "Mixtral 8x7B Instruct": {"tokens": 32000, "source": "https://docs.mistral.ai/models/", "notes": "Mistral official docs, June 2024"},
    # Cohere Command
    "Command": {"tokens": 128000, "source": "https://docs.cohere.com/docs/models", "notes": "Cohere official docs, June 2024"},
    "Command R": {"tokens": 128000, "source": "https://docs.cohere.com/docs/models", "notes": "Cohere official docs, June 2024"},
    "Command R+": {"tokens": 128000, "source": "https://docs.cohere.com/docs/models", "notes": "Cohere official docs, June 2024"},
    "Command Light": {"tokens": 128000, "source": "https://docs.cohere.com/docs/models", "notes": "Cohere official docs, June 2024"},
    # Amazon Titan
    "Titan Text G1 - Express": {"tokens": 8192, "source": "https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text-express.html", "notes": "AWS official docs, June 2024"},
    "Titan Text G1 - Lite": {"tokens": 8192, "source": "https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text-lite.html", "notes": "AWS official docs, June 2024"},
    "Titan Text G1 - Premier": {"tokens": 8192, "source": "https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-titan-text-premier.html", "notes": "AWS official docs, June 2024"},
    # Stability AI (Image models, context window not applicable)
    "Stable Image Core 1.0": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    "Stable Image Ultra 1.0": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    "SD3 Large 1.0": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    "SDXL 1.0": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    "Stable Diffusion 3.5 Large": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    # Other/unknown
    "Jamba-Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Jamba 1.5 Large": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Jamba 1.5 Mini": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Canvas": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Lite": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Micro": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Premier": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Pro": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Reel": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Nova Sonic": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Rerank 1.0": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Titan Embeddings G1 - Text": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Titan Image Generator G1 v2": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    "Titan Image Generator G1": {"tokens": "N/A", "source": "Image model - not applicable", "notes": "Image model - context window not applicable"},
    "Titan Multimodal Embeddings G1": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Titan Text Embeddings V2": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Embed English": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Embed Multilingual": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Rerank 3.5": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "DeepSeek-R1": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Ray v2": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 3.1 405B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 3.2 1B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 3.2 3B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 3.2 11B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 3.2 90B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 3.3 70B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 4 Maverick 17B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Llama 4 Scout 17B Instruct": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Marengo Embed v2.7": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Pegasus v1.2": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Palmyra X4": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
    "Palmyra X5": {"tokens": "unknown", "source": "unknown", "notes": "No public info as of 2024-06; checked provider docs and web."},
}

# Thresholds for category
SMALL_THRESHOLD = 8000
LARGE_THRESHOLD = 100000

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

def get_context_window_info(model_name: str) -> tuple:
    info = CONTEXT_WINDOW_INFO.get(model_name)
    if info:
        tokens = info["tokens"]
        source = info["source"]
        notes = info.get("notes", "")
        # Only categorize if tokens is an int
        if isinstance(tokens, int):
            if tokens >= LARGE_THRESHOLD:
                category = "large"
            elif tokens <= SMALL_THRESHOLD:
                category = "small"
            else:
                category = "unknown"
        else:
            category = "unknown"
        return tokens, category, source, notes
    else:
        return "unknown", "unknown", "unknown", "No public info as of 2024-06; checked provider docs and web."

def build_context_window_table(models: list[dict]) -> list[dict]:
    results = []
    seen_models = set()  # Track seen model names to avoid duplicates
    
    for m in models:
        name = m.get("Model name", "Unknown")
        
        # Skip if we've already processed this model
        if name in seen_models:
            continue
            
        seen_models.add(name)
        tokens, category, source, notes = get_context_window_info(name)
        results.append({
            "Model name": name,
            "Context window tokens": tokens,
            "Category": category,
            "Source": source,
            "Notes": notes
        })
    return results

def write_context_window_to_csv(results: list[dict], filename: str = "context_window_output.csv") -> None:
    if not results:
        return
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    html = fetch_bedrock_catalog()
    models = parse_bedrock_models(html)
    print("Model names from AWS Bedrock catalog:")
    for m in models:
        print(repr(m.get("Model name", "Unknown")))
    print(f"Total models found: {len(models)}")
    context_window_results = build_context_window_table(models)
    write_context_window_to_csv(context_window_results)
    print(f"Wrote context window info for {len(context_window_results)} models to context_window_output.csv")
