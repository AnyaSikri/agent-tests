"""
Example User Input File
This file demonstrates how users can specify their use case and requirements
for LLM vendor selection.
"""

# Example Use Case: Customer Insurance Claims Priority Classification
use_case = {
    "name": "Customer Insurance Claims Priority Classification",
    "description": "Automated system to classify incoming insurance claims based on priority level (High, Medium, Low) for efficient processing and resource allocation.",
    
    "requirements": {
        "deployment": {
            "type": "Cloud",
            "reason": "Need scalable infrastructure to handle varying claim volumes and ensure high availability"
        },
        
        "latency": {
            "type": "Real-time",
            "max_response_time": "5 seconds",
            "reason": "Claims need to be classified immediately upon submission to enable quick customer service responses"
        },
        
        "modality": {
            "input": ["Text"],
            "output": ["Text"],
            "reason": "Claims are submitted as text documents and need text-based priority labels as output"
        },
        
        "additional_requirements": {
            "accuracy": "High accuracy (>95%) for priority classification",
            "security": "HIPAA compliance for handling sensitive medical information",
            "volume": "Handle 1000+ claims per day",
            "availability": "99.9% uptime requirement",
            "cost": "Cost-effective for high-volume processing"
        }
    },
    
    "example_input": {
        "claim_text": "Patient experienced severe chest pain and shortness of breath on 2024-01-15. Emergency room visit required. Diagnosis: Acute myocardial infarction. Treatment: Cardiac catheterization and stent placement. Hospital stay: 5 days.",
        "expected_output": "Priority: HIGH - Life-threatening condition requiring immediate attention"
    }
}

# Additional Example Use Cases
additional_use_cases = {
    "customer_support_chatbot": {
        "name": "Customer Support Chatbot",
        "description": "AI-powered chatbot to handle customer inquiries and provide instant support",
        "requirements": {
            "deployment": {"type": "Cloud", "reason": "Global accessibility and scalability"},
            "latency": {"type": "Real-time", "max_response_time": "2 seconds", "reason": "Immediate customer service"},
            "modality": {
                "input": ["Text"],
                "output": ["Text", "Chat"],
                "reason": "Text-based conversations with chat interface"
            }
        }
    },
    
    "document_analysis": {
        "name": "Legal Document Analysis",
        "description": "Analyze legal documents to extract key information and identify relevant clauses",
        "requirements": {
            "deployment": {"type": "On-premise", "reason": "Data privacy and security requirements"},
            "latency": {"type": "Batch", "max_response_time": "30 minutes", "reason": "Non-time-critical processing"},
            "modality": {
                "input": ["Text", "Image"],
                "output": ["Text"],
                "reason": "Process both text documents and scanned images"
            }
        }
    },
    
    "content_generation": {
        "name": "Marketing Content Generation",
        "description": "Generate marketing copy and social media content based on product descriptions",
        "requirements": {
            "deployment": {"type": "Cloud", "reason": "Flexible scaling for campaign demands"},
            "latency": {"type": "Real-time", "max_response_time": "10 seconds", "reason": "Quick content creation for campaigns"},
            "modality": {
                "input": ["Text"],
                "output": ["Text"],
                "reason": "Text-based content generation"
            }
        }
    }
}

def get_use_case_requirements(use_case_name):
    """
    Retrieve requirements for a specific use case
    """
    if use_case_name == "insurance_claims":
        return use_case
    elif use_case_name in additional_use_cases:
        return additional_use_cases[use_case_name]
    else:
        return None

def print_use_case_summary(use_case_data):
    """
    Print a formatted summary of the use case and requirements
    """
    print(f"Use Case: {use_case_data['name']}")
    print(f"Description: {use_case_data['description']}")
    print("\nRequirements:")
    print(f"  Deployment: {use_case_data['requirements']['deployment']['type']} - {use_case_data['requirements']['deployment']['reason']}")
    print(f"  Latency: {use_case_data['requirements']['latency']['type']} ({use_case_data['requirements']['latency']['max_response_time']}) - {use_case_data['requirements']['latency']['reason']}")
    print(f"  Input Modalities: {', '.join(use_case_data['requirements']['modality']['input'])}")
    print(f"  Output Modalities: {', '.join(use_case_data['requirements']['modality']['output'])}")
    
    if 'additional_requirements' in use_case_data['requirements']:
        print("\nAdditional Requirements:")
        for req, value in use_case_data['requirements']['additional_requirements'].items():
            print(f"  {req.title()}: {value}")

if __name__ == "__main__":
    # Example usage
    print("=== INSURANCE CLAIMS USE CASE ===")
    print_use_case_summary(use_case)
    
    print("\n=== EXAMPLE INPUT/OUTPUT ===")
    print(f"Input: {use_case['example_input']['claim_text']}")
    print(f"Expected Output: {use_case['example_input']['expected_output']}") 