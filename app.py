import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_bedrock_catalog():
    url = "https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_bedrock_models(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        return []
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    return [
        {headers[i]: td.get_text(strip=True) for i, td in enumerate(row.find_all("td"))}
        for row in table.find_all("tr")[1:]
        if row.find_all("td")
    ]

def get_deployment_type(model):
    return "Cloud" if model and model.get("Regions supported", "").strip() else "?"

def get_model_deployment_info(model_names, catalog_models):
    catalog_dict = {model.get("Model name", ""): model for model in catalog_models}
    return [
        {
            "Model Name": name,
            "Deployment Type": get_deployment_type(catalog_dict.get(name))
        }
        for name in model_names
    ]

st.title("AWS Bedrock Model Deployment Type Checker")

model_input = st.text_area("Enter model names (one per line):")
if st.button("Check Deployment Types"):
    model_names = [name.strip() for name in model_input.splitlines() if name.strip()]
    if model_names:
        html = fetch_bedrock_catalog()
        catalog_models = parse_bedrock_models(html)
        results = get_model_deployment_info(model_names, catalog_models)
        df = pd.DataFrame(results)
        st.table(df)
    else:
        st.warning("Please enter at least one model name.")