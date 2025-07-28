# LLM Vendor Database System

A comprehensive system for collecting, processing, and analyzing information about Large Language Model (LLM) vendors and their offerings. The system systematically captures data across multiple dimensions including technical specifications, pricing, deployment options, and vendor characteristics.

## Overview

This system provides a structured approach to building a comprehensive database of LLM vendors by:

1. **Multi-dimensional Data Collection**: Systematic data capture across 8 attribute categories
2. **Automated Data Processing**: Scripts for collecting and processing vendor information  
3. **Comprehensive Database**: Unified database containing 80+ LLM models from 15+ vendors
4. **Schema Documentation**: Automated generation of database schema documentation
5. **Modular Architecture**: Separate modules for each data attribute

## File Structure

```
├── README.md                           # This file
├── DOCUMENTATION.md                    # Comprehensive documentation
├── working_items/                      # Database generation workspace
│   ├── main.py                        # Simple launcher script
│   ├── orchestrator_database.py       # Main orchestrator
│   ├── complete_llm_database.csv      # Final unified database
│   ├── llm_database_schema.csv        # Schema documentation
│   └── README.md                      # Working items documentation
└── attribute_functions/               # Data collection modules
    ├── vendor_database.py             # Base vendor information
    ├── cost.py                        # Pricing data collection
    ├── context_window.py              # Context window specifications
    ├── latency.py                     # Latency and performance data
    ├── modality.py                    # Input/output modality support
    ├── model_specificity.py           # Model classification data
    ├── source_type.py                 # Data source information
    ├── deployment_v2.py               # Deployment options
    └── [output CSV files]             # Generated data files
```

## Quick Start

### 1. Generate the Complete Database

```bash
cd working_items
python orchestrator_database.py
```

This will:
- Execute all 8 data collection modules
- Combine all data into a unified database
- Generate schema documentation
- Create the final `complete_llm_database.csv`


### 2. Run Individual Modules

```bash
cd attribute_functions
python vendor_database.py
python cost.py
python context_window.py
# ... etc for other modules
```

## Supported Vendors

The system tracks data for the following vendors:
- Anthropic (Claude models)
- Meta (Llama models)
- Mistral AI
- Cohere
- Stability AI
- Writer
- AI21 Labs
- Amazon (Nova/Titan models)
- DeepSeek
- Luma AI
- OpenAI
- Google
- Microsoft
- Nvidia
- Hugging Face

## Data Collection Modules

### 1. Vendor Database (`vendor_database.py`)
Establishes the base vendor database with fundamental vendor information including model names, vendor company information, formation year, and vendor maturity level.

### 2. Cost Analysis (`cost.py`)
Gathers pricing information for different model tiers and usage patterns including input/output token pricing and cost per 1K tokens.

### 3. Context Window (`context_window.py`)
Collects context window specifications and limitations including context window size in tokens and categories.

### 4. Latency Analysis (`latency.py`)
Gathers performance and latency-related information including latency support types and response time specifications.

### 5. Modality Support (`modality.py`)
Records input and output modality capabilities including support for Text, Image, Video, Speech, and Embedding.

### 6. Model Specificity (`model_specificity.py`)
Categorizes models by their specialization and use cases including General-Purpose, Domain-Specific, and Task-Specific classifications.

### 7. Source Type (`source_type.py`)
Records data sources and licensing information including open/closed source status and licensing details.

### 8. Deployment Options (`deployment_v2.py`)
Gathers deployment and infrastructure information including Cloud, On-premise, and Hybrid deployment types.

## Database Schema

The final database (`complete_llm_database.csv`) contains comprehensive information about each LLM model including:

- **Model Information**: Name, vendor, formation year, age, category, status
- **Technical Specifications**: Context window size, latency support, modality capabilities
- **Classification Data**: Model specificity, source type, deployment options
- **Metadata**: Source URLs, notes, and additional context

### Data Quality Metrics
- **Total Models**: 80+ LLM models
- **Total Vendors**: 15+ companies
- **Data Completeness**: Varies by attribute (60-95%)
- **Update Frequency**: Manual updates as needed

## Usage Examples

### Basic Data Analysis

```python
import pandas as pd

# Load the complete database
df = pd.read_csv('working_items/complete_llm_database.csv')

# Filter by vendor
anthropic_models = df[df['vendor_name'] == 'Anthropic']

# Filter by context window size
large_context_models = df[df['contextwindow_Context window tokens'] >= 100000]

# Filter by modality
multimodal_models = df[df['modality_Input modalities'].str.contains('Image', na=False)]
```

### Custom Data Collection

To add new data sources or modify existing ones:

1. Edit the relevant module in `attribute_functions/`
2. Update data sources in the module
3. Run the specific module to test changes
4. Re-run the orchestrator to regenerate the complete database

## Installation

### Prerequisites
- Python 3.7 or higher
- pandas library
- Internet connection for data collection

### Adding New Data Sources

1. Create a new module in `attribute_functions/`
2. Follow the module structure outlined in the documentation
3. Add the module to the `MODULES` list in `orchestrator_database.py`
4. Update the `OUTPUT_FILES` dictionary
5. Test the integration

### Extending the Database

Add new filtering methods or analysis capabilities by:
- Creating new analysis scripts
- Extending existing modules
- Adding new data attributes to the schema