# LLM Vendor Database Generator

This generates a complete LLM vendor database by running 8 different modules.

## Usage

```bash
cd working_items
python launch_database_generator.py
```

Or run directly:
```bash
cd working_items
python orchestrator_database.py
```

Check file status:
```bash
python launch_database_generator.py --status
```

## Files

### Scripts
- `orchestrator_database.py` - Main script
- `launch_database_generator.py` - Simple launcher

### Output Files
1. `complete_vendor_database.csv` - Vendor information
2. `cost_analysis_output.csv` - Cost data
3. `context_window_output.csv` - Context window data
4. `latency_label.csv` - Latency data
5. `modality_output.csv` - Modality data
6. `llm_specificity_output.csv` - Specificity data
7. `source_type.csv` - Source type data
8. `deployment_types.csv` - Deployment data
9. `complete_llm_database.csv` - Joined database
10. `csv_schema_documentation.csv` - Schema info

## How it works

The script runs these modules:
- cost.py
- context_window.py
- latency.py
- modality.py
- model_specificity.py
- source_type.py
- deployment_v2.py

Then joins all the CSV files into one database.