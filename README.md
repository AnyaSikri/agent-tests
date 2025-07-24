# Vendor Filtering System

A comprehensive system for filtering and recommending LLM vendors based on deployment type, latency requirements, and modality needs.

## 🎯 Overview

This system helps users find the most suitable LLM vendors by matching their specific requirements with vendor capabilities across three key dimensions:

1. **Deployment Type**: Cloud, On-premise, or Hybrid
2. **Latency Requirements**: Real-time, Batch, or Both
3. **Modality Support**: Input (Text, Image, Video, Speech) and Output (Text, Chat, Image, Video, Speech, Embedding)

## 📁 File Structure

```
├── vendor_database.py          # Creates the vendor database from CSV files
├── user_input_example.py       # Example use cases and requirements
├── vendor_filter.py            # Main filtering and recommendation engine
├── demo_system.py              # Complete demo of the system
├── README.md                   # This file
├── deployment_types.csv        # Vendor deployment information
├── latency_label.csv          # Vendor latency capabilities
├── modality_output.csv        # Vendor modality support
└── vendor_database.json       # Generated database (created by vendor_database.py)
```

## 🚀 Quick Start

### 1. Create the Database

First, create the vendor database by running:

```bash
python vendor_database.py
```

This will generate `vendor_database.json` containing all vendor information.

### 2. Run the Demo

To see the system in action:

```bash
python demo_system.py
```

This will demonstrate:
- Insurance claims use case
- Custom requirements filtering
- Various filter combinations
- Interactive mode for custom requirements

## 📋 Example Use Cases

### Insurance Claims Priority Classification

**Requirements:**
- **Deployment**: Cloud (for scalability and high availability)
- **Latency**: Real-time (5-second response time)
- **Modality**: Text input → Text output
- **Additional**: HIPAA compliance, 1000+ claims/day

**Example Input:**
```
"Patient experienced severe chest pain and shortness of breath on 2024-01-15. 
Emergency room visit required. Diagnosis: Acute myocardial infarction. 
Treatment: Cardiac catheterization and stent placement. Hospital stay: 5 days."
```

**Expected Output:**
```
"Priority: HIGH - Life-threatening condition requiring immediate attention"
```

### Other Example Use Cases

- **Customer Support Chatbot**: Real-time text conversations
- **Legal Document Analysis**: Batch processing of text and images
- **Marketing Content Generation**: Real-time text generation

## 🔧 How to Use

### 1. Define Your Requirements

Create a use case dictionary with your requirements:

```python
my_use_case = {
    "name": "My Use Case",
    "description": "Description of what you want to achieve",
    "requirements": {
        "deployment": {
            "type": "Cloud",  # or "On-premise"
            "reason": "Your reason"
        },
        "latency": {
            "type": "Real-time",  # or "Batch"
            "max_response_time": "5 seconds",
            "reason": "Your reason"
        },
        "modality": {
            "input": ["Text", "Image"],  # Supported input types
            "output": ["Text"],          # Required output types
            "reason": "Your reason"
        }
    }
}
```

### 2. Get Recommendations

```python
from vendor_filter import VendorFilter

# Initialize the filter
filter_system = VendorFilter()

# Get recommendations
recommendations = filter_system.get_vendor_recommendations(my_use_case)

# Print results
filter_system.print_recommendations(recommendations, my_use_case['name'])
```

### 3. Apply Specific Filters

```python
# Filter by deployment type
cloud_vendors = filter_system.filter_by_deployment('Cloud')

# Filter by latency
realtime_vendors = filter_system.filter_by_latency('real-time')

# Filter by modality
text_vendors = filter_system.filter_by_modality(['Text'], ['Text'])

# Combine filters
matching_vendors = filter_system.filter_vendors(
    deployment_type='Cloud',
    latency_requirement='real-time',
    input_modalities=['Text'],
    output_modalities=['Text']
)
```

## 📊 Database Structure

The vendor database contains entries with the following structure:

```json
{
  "model_name": "Claude 3.7 Sonnet",
  "model_id": "anthropic.claude-3-7-sonnet-20250219-v1:0",
  "deployment_type": "Cloud",
  "latency_support": "real-time only",
  "input_modalities": "Text, Image",
  "output_modalities": "Text, Chat"
}
```

## 🎯 Recommendation Scoring

The system categorizes recommendations into:

- **Perfect Matches** (Score ≥ 0.9): Meet all requirements exactly
- **Good Matches** (Score ≥ 0.7): Meet most requirements with minor considerations
- **Partial Matches** (Score < 0.7): Meet some requirements but may need additional configuration

## 🔍 Supported Filters

### Deployment Types
- Cloud
- On-premise
- Any (no filter)

### Latency Requirements
- Real-time
- Batch
- Both
- Any (no filter)

### Modalities
**Input:**
- Text
- Image
- Video
- Speech

**Output:**
- Text
- Chat
- Image
- Video
- Speech
- Embedding

## 🛠️ Customization

### Adding New Vendors

1. Update the CSV files (`deployment_types.csv`, `latency_label.csv`, `modality_output.csv`)
2. Run `vendor_database.py` to regenerate the database

### Extending the Filter

Add new filtering methods to the `VendorFilter` class in `vendor_filter.py`:

```python
def filter_by_new_criteria(self, criteria_value):
    # Your custom filtering logic
    pass
```

## 📝 Dependencies

- Python 3.7+
- pandas
- json (built-in)
- typing (built-in)

## 🤝 Contributing

To add new features or improve the system:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the demo system
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For questions or issues, please check the demo system first, then create an issue with:
- Your use case requirements
- Expected behavior
- Actual behavior
- Error messages (if any) 