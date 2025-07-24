import pandas as pd
import json

# Create the vendor database with deployment, latency, and modality attributes
def create_vendor_database():
    # Load existing data
    deployment_df = pd.read_csv('deployment_types.csv')
    latency_df = pd.read_csv('latency_label.csv')
    modality_df = pd.read_csv('modality_output.csv')
    
    # Clean and standardize model names
    deployment_df['Model Name'] = deployment_df['Model Name'].str.strip()
    latency_df['model-id'] = latency_df['model-id'].str.strip()
    modality_df['Model name'] = modality_df['Model name'].str.strip()
    
    # Create a mapping for model names to standardize across datasets
    model_mapping = {
        'Claude 3.7 Sonnet': 'anthropic.claude-3-7-sonnet-20250219-v1:0',
        'Llama 3.1 405B Instruct': 'meta.llama3-1-405b-instruct-v1:0',
        'Mistral 7B Instruct': 'mistral.mistral-7b-instruct-v0:2',
        'Claude 3.5 Sonnet': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
        'Claude 3.5 Sonnet v2': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
        'Claude 3.5 Haiku': 'anthropic.claude-3-5-haiku-20241022-v1:0',
        'Claude 3 Haiku': 'anthropic.claude-3-haiku-20240307-v1:0',
        'Claude 3 Opus': 'anthropic.claude-3-opus-20240229-v1:0',
        'Claude 3 Sonnet': 'anthropic.claude-3-sonnet-20240229-v1:0',
        'Claude Opus 4': 'anthropic.claude-opus-4-20250514-v1:0',
        'Claude Sonnet 4': 'anthropic.claude-sonnet-4-20250514-v1:0',
        'Llama 3 8B Instruct': 'meta.llama3-8b-instruct-v1:0',
        'Llama 3 70B Instruct': 'meta.llama3-70b-instruct-v1:0',
        'Llama 3.1 8B Instruct': 'meta.llama3-1-8b-instruct-v1:0',
        'Llama 3.1 70B Instruct': 'meta.llama3-1-70b-instruct-v1:0',
        'Llama 3.2 1B Instruct': 'meta.llama3-2-1b-instruct-v1:0',
        'Llama 3.2 3B Instruct': 'meta.llama3-2-3b-instruct-v1:0',
        'Llama 3.2 11B Instruct': 'meta.llama3-2-11b-instruct-v1:0',
        'Llama 3.2 90B Instruct': 'meta.llama3-2-90b-instruct-v1:0',
        'Llama 3.3 70B Instruct': 'meta.llama3-3-70b-instruct-v1:0',
        'Llama 4 Maverick 17B Instruct': 'meta.llama4-maverick-17b-instruct-v1:0',
        'Llama 4 Scout 17B Instruct': 'meta.llama4-scout-17b-instruct-v1:0',
        'Mistral Large (24.02)': 'mistral.mistral-large-2402-v1:0',
        'Mistral Large (24.07)': 'mistral.mistral-large-2407-v1:0',
        'Mistral Small (24.02)': 'mistral.mistral-small-2402-v1:0',
        'Mixtral 8x7B Instruct': 'mistral.mixtral-8x7b-instruct-v0:1',
        'Pixtral Large (25.02)': 'mistral.pixtral-large-2502-v1:0',
        'Command Light': 'cohere.command-light-text-v14',
        'Command R+': 'cohere.command-r-plus-v1:0',
        'Command R': 'cohere.command-r-v1:0',
        'Command': 'cohere.command-text-v14',
        'Embed English': 'cohere.embed-english-v3',
        'Embed Multilingual': 'cohere.embed-multilingual-v3',
        'Rerank 3.5': 'cohere.rerank-v3-5:0',
        'DeepSeek-R1': 'deepseek.r1-v1:0',
        'Ray v2': 'luma.ray-v2:0',
        'Stable Diffusion 3.5 Large': 'stability.sd3-5-large-v1:0',
        'Stable Image Core 1.0': 'stability.stable-image-core-v1:1',
        'Stable Image Ultra 1.0': 'stability.stable-image-ultra-v1:1',
        'Palmyra X4': 'writer.palmyra-x4-v1:0',
        'Palmyra X5': 'writer.palmyra-x5-v1:0',
        'Jamba 1.5 Large': 'ai21.jamba-1-5-large-v1:0',
        'Jamba 1.5 Mini': 'ai21.jamba-1-5-mini-v1:0',
        'Jamba-Instruct': 'ai21.jamba-instruct-v1:0',
        'Nova Canvas': 'amazon.nova-canvas-v1:0',
        'Nova Lite': 'amazon.nova-lite-v1:0',
        'Nova Micro': 'amazon.nova-micro-v1:0',
        'Nova Premier': 'amazon.nova-premier-v1:0',
        'Nova Pro': 'amazon.nova-pro-v1:0',
        'Nova Reel': 'amazon.nova-reel-v1:0',
        'Nova Sonic': 'amazon.nova-sonic-v1:0',
        'Rerank 1.0': 'amazon.rerank-v1:0',
        'Titan Embeddings G1 - Text': 'amazon.titan-embed-text-v1',
        'Titan Image Generator G1 v2': 'amazon.titan-image-generator-v2:0',
        'Titan Image Generator G1': 'amazon.titan-image-generator-v1',
        'Titan Multimodal Embeddings G1': 'amazon.titan-embed-image-v1',
        'Titan Text Embeddings V2': 'amazon.titan-embed-text-v2:0',
        'Titan Text G1 - Express': 'amazon.titan-text-express-v1',
        'Titan Text G1 - Lite': 'amazon.titan-text-lite-v1',
        'Titan Text G1 - Premier': 'amazon.titan-text-premier-v1:0',
        'Claude 2.1': 'anthropic.claude-v2:1',
        'Claude 2': 'anthropic.claude-v2',
        'Claude Instant': 'anthropic.claude-instant-v1',
        'Claude': 'anthropic.claude-v2:0',
        'SD3 Large 1.0': 'stability.sd3-large-v1:0',
        'SDXL 1.0': 'stability.stable-diffusion-xl-v1'
    }
    
    # Create the combined database
    vendor_database = []
    
    for model_name, model_id in model_mapping.items():
        # Get deployment type
        deployment_type = deployment_df[deployment_df['Model Name'] == model_name]['Deployment Type'].iloc[0] if len(deployment_df[deployment_df['Model Name'] == model_name]) > 0 else 'Unknown'
        
        # Get latency support
        latency_support = latency_df[latency_df['model-id'] == model_id]['support_type'].iloc[0] if len(latency_df[latency_df['model-id'] == model_id]) > 0 else 'Unknown'
        
        # Get modality information
        modality_row = modality_df[modality_df['Model name'] == model_name]
        if len(modality_row) > 0:
            input_modalities = modality_row['Input modalities'].iloc[0]
            output_modalities = modality_row['Output modalities'].iloc[0]
        else:
            input_modalities = 'Unknown'
            output_modalities = 'Unknown'
        
        vendor_entry = {
            'model_name': model_name,
            'model_id': model_id,
            'deployment_type': deployment_type,
            'latency_support': latency_support,
            'input_modalities': input_modalities,
            'output_modalities': output_modalities
        }
        
        vendor_database.append(vendor_entry)
    
    return vendor_database

# Save the database to a JSON file
def save_database():
    database = create_vendor_database()
    with open('vendor_database.json', 'w') as f:
        json.dump(database, f, indent=2)
    print(f"Database created with {len(database)} models")
    return database

if __name__ == "__main__":
    database = save_database()
    print("Vendor database created successfully!") 