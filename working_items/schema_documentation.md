# Schema Documentation

This describes the LLM vendor database schema.

## Output Files

The system generates these CSV files:

1. complete_vendor_database.csv - Vendor information
2. cost_analysis_output.csv - Cost data
3. context_window_output.csv - Context window data
4. latency_label.csv - Latency data
5. modality_output.csv - Modality data
6. llm_specificity_output.csv - Specificity data
7. source_type.csv - Source type data
8. deployment_types.csv - Deployment data
9. complete_llm_database.csv - Joined database
10. csv_schema_documentation.csv - Schema info

## Schema

### Vendor Database
- Vendor Name
- Company Name
- Formation Year
- Age (Years)
- Category
- Status

### Cost Analysis
- Model Name
- Input Rate per 1K tokens
- Cost Category
- Category Description
- Raw Pricing Text

### Context Window
- Model name
- Context window tokens
- Category
- Source
- Notes

### Latency Support
- model-id
- support_type
- notes

### Modality Support
- Model name
- Input modalities
- Output modalities
- Notes

### Model Specificity
- Model name
- Specificity Level
- Description
- Notes

### Source Type
- Model Name
- Source Type
- Description
- Notes

### Deployment Types
- Model Name
- Deployment Type
- Description
- Notes

## Joining

The system joins all files using Model Name as the primary key. AWS Bedrock model IDs are mapped to display names for the latency data.

Columns are prefixed to avoid conflicts:
- cost_*
- context_window_*
- latency_*
- modality_*
- llm_specificity_*
- source_type_*
- deployment_types_*

## Usage

```bash
cd working_items
python orchestrator_database.py
``` 