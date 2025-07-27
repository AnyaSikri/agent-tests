import pandas as pd
import json

# Create the vendor database focused on maturity based on company age
def create_vendor_database():
    # Define vendor information directly
    vendor_info = {
        'Anthropic': {'formation_year': 2021, 'age_years': 3, 'category': 'AI Research', 'status': 'Active', 'maturity': 'emerging'},
        'Meta': {'formation_year': 2004, 'age_years': 20, 'category': 'Technology', 'status': 'Active', 'maturity': 'mature'},
        'Mistral': {'formation_year': 2023, 'age_years': 1, 'category': 'AI Research', 'status': 'Active', 'maturity': 'emerging'},
        'Cohere': {'formation_year': 2019, 'age_years': 5, 'category': 'AI Research', 'status': 'Active', 'maturity': 'established'},
        'Stability': {'formation_year': 2020, 'age_years': 4, 'category': 'AI Research', 'status': 'Active', 'maturity': 'emerging'},
        'Writer': {'formation_year': 2020, 'age_years': 4, 'category': 'AI Research', 'status': 'Active', 'maturity': 'emerging'},
        'AI21': {'formation_year': 2017, 'age_years': 7, 'category': 'AI Research', 'status': 'Active', 'maturity': 'established'},
        'Amazon': {'formation_year': 1994, 'age_years': 30, 'category': 'Technology', 'status': 'Active', 'maturity': 'mature'},
        'DeepSeek': {'formation_year': 2023, 'age_years': 1, 'category': 'AI Research', 'status': 'Active', 'maturity': 'emerging'},
        'Luma': {'formation_year': 2021, 'age_years': 3, 'category': 'AI Research', 'status': 'Active', 'maturity': 'emerging'},
        'Google': {'formation_year': 1998, 'age_years': 26, 'category': 'Technology', 'status': 'Active', 'maturity': 'mature'},
        'OpenAI': {'formation_year': 2015, 'age_years': 9, 'category': 'AI Research', 'status': 'Active', 'maturity': 'established'},
        'Microsoft': {'formation_year': 1975, 'age_years': 49, 'category': 'Technology', 'status': 'Active', 'maturity': 'mature'},
        'Nvidia': {'formation_year': 1993, 'age_years': 31, 'category': 'Technology', 'status': 'Active', 'maturity': 'mature'},
        'Hugging Face': {'formation_year': 2016, 'age_years': 8, 'category': 'AI Research', 'status': 'Active', 'maturity': 'established'}
    }
    
    # Define model names and their vendors
    model_vendor_mapping = {
        # Anthropic models
        'Claude 3.7 Sonnet': 'Anthropic',
        'Claude 3.5 Sonnet': 'Anthropic',
        'Claude 3.5 Sonnet v2': 'Anthropic',
        'Claude 3.5 Haiku': 'Anthropic',
        'Claude 3 Haiku': 'Anthropic',
        'Claude 3 Opus': 'Anthropic',
        'Claude 3 Sonnet': 'Anthropic',
        'Claude Opus 4': 'Anthropic',
        'Claude Sonnet 4': 'Anthropic',
        'Claude 2.1': 'Anthropic',
        'Claude 2': 'Anthropic',
        'Claude Instant': 'Anthropic',
        'Claude': 'Anthropic',
        
        # Meta models
        'Llama 3.1 405B Instruct': 'Meta',
        'Llama 3 8B Instruct': 'Meta',
        'Llama 3 70B Instruct': 'Meta',
        'Llama 3.1 8B Instruct': 'Meta',
        'Llama 3.1 70B Instruct': 'Meta',
        'Llama 3.2 1B Instruct': 'Meta',
        'Llama 3.2 3B Instruct': 'Meta',
        'Llama 3.2 11B Instruct': 'Meta',
        'Llama 3.2 90B Instruct': 'Meta',
        'Llama 3.3 70B Instruct': 'Meta',
        'Llama 4 Maverick 17B Instruct': 'Meta',
        'Llama 4 Scout 17B Instruct': 'Meta',
        
        # Mistral models
        'Mistral 7B Instruct': 'Mistral',
        'Mistral Large (24.02)': 'Mistral',
        'Mistral Large (24.07)': 'Mistral',
        'Mistral Small (24.02)': 'Mistral',
        'Mixtral 8x7B Instruct': 'Mistral',
        'Pixtral Large (25.02)': 'Mistral',
        
        # Cohere models
        'Command Light': 'Cohere',
        'Command R+': 'Cohere',
        'Command R': 'Cohere',
        'Command': 'Cohere',
        'Embed English': 'Cohere',
        'Embed Multilingual': 'Cohere',
        'Rerank 3.5': 'Cohere',
        
        # Stability models
        'Stable Diffusion 3.5 Large': 'Stability',
        'Stable Image Core 1.0': 'Stability',
        'Stable Image Ultra 1.0': 'Stability',
        'SD3 Large 1.0': 'Stability',
        'SDXL 1.0': 'Stability',
        
        # Writer models
        'Palmyra X4': 'Writer',
        'Palmyra X5': 'Writer',
        
        # AI21 models
        'Jamba 1.5 Large': 'AI21',
        'Jamba 1.5 Mini': 'AI21',
        'Jamba-Instruct': 'AI21',
        
        # Amazon models
        'Nova Canvas': 'Amazon',
        'Nova Lite': 'Amazon',
        'Nova Micro': 'Amazon',
        'Nova Premier': 'Amazon',
        'Nova Pro': 'Amazon',
        'Nova Reel': 'Amazon',
        'Nova Sonic': 'Amazon',
        'Rerank 1.0': 'Amazon',
        'Titan Embeddings G1 - Text': 'Amazon',
        'Titan Image Generator G1 v2': 'Amazon',
        'Titan Image Generator G1': 'Amazon',
        'Titan Multimodal Embeddings G1': 'Amazon',
        'Titan Text Embeddings V2': 'Amazon',
        'Titan Text G1 - Express': 'Amazon',
        'Titan Text G1 - Lite': 'Amazon',
        'Titan Text G1 - Premier': 'Amazon',
        
        # Other models
        'DeepSeek-R1': 'DeepSeek',
        'Ray v2': 'Luma',
        
        # OpenAI models
        'GPT-4': 'OpenAI',
        'GPT-4 Turbo': 'OpenAI',
        'GPT-3.5 Turbo': 'OpenAI',
        'GPT-3': 'OpenAI',
        
        # Google models
        'Gemini Pro': 'Google',
        'Gemini Flash': 'Google',
        'PaLM 2': 'Google',
        
        # Microsoft models
        'Phi-3': 'Microsoft',
        'Phi-2': 'Microsoft',
        
        # Nvidia models
        'Nemotron-4': 'Nvidia',
        
        # Hugging Face models
        'CodeLlama': 'Hugging Face',
        'StarCoder': 'Hugging Face'
    }
    
    # Create the vendor database
    vendor_database = []
    
    for model_name, vendor_name in model_vendor_mapping.items():
        vendor_info_dict = vendor_info.get(vendor_name, {
            'formation_year': 'Unknown',
            'age_years': 'Unknown', 
            'category': 'Unknown',
            'status': 'Unknown',
            'maturity': 'unknown'
        })
        
        vendor_entry = {
            'model_name': model_name,
            'vendor_name': vendor_name,
            'formation_year': vendor_info_dict['formation_year'],
            'age_years': vendor_info_dict['age_years'],
            'category': vendor_info_dict['category'],
            'status': vendor_info_dict['status'],
            'vendor_maturity': vendor_info_dict['maturity']
        }
        
        vendor_database.append(vendor_entry)
    
    return vendor_database

# Save the database to a CSV file
def save_database():
    database = create_vendor_database()
    
    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(database)
    df.to_csv('vendor_database_output.csv', index=False)
    
    print(f"Database created with {len(database)} models")
    print("Saved to vendor_database_output.csv")
    return database

if __name__ == "__main__":
    database = save_database()
    print("Vendor database created successfully!") 