#!/usr/bin/env python3
"""
Gradio UI for Vendor Filtering System
A beautiful, interactive web interface for filtering and recommending LLM vendors
"""

import gradio as gr
import json
import os
from vendor_database_simple import create_vendor_database, save_database
from vendor_filter import VendorFilter
from user_input_example import use_case, additional_use_cases

# Initialize the vendor filter system
def initialize_system():
    """Initialize the vendor database and filter system"""
    if not os.path.exists('vendor_database.json'):
        print("Creating vendor database...")
        save_database()
    
    filter_system = VendorFilter()
    return filter_system

# Global filter system
filter_system = initialize_system()

def get_vendor_recommendations(use_case_name, deployment_type, latency_type, 
                              input_modalities, output_modalities, custom_description=""):
    """
    Get vendor recommendations based on user input
    """
    try:
        # Create use case from user input
        if use_case_name == "Custom Use Case":
            use_case_data = {
                "name": "Custom Use Case",
                "description": custom_description or "User-defined requirements",
                "requirements": {
                    "deployment": {"type": deployment_type, "reason": "User specified"},
                    "latency": {"type": latency_type, "max_response_time": "User specified", "reason": "User specified"},
                    "modality": {
                        "input": input_modalities if input_modalities else [],
                        "output": output_modalities if output_modalities else [],
                        "reason": "User specified"
                    }
                }
            }
        else:
            # Use predefined use case
            if use_case_name == "Insurance Claims Classification":
                use_case_data = use_case
            else:
                use_case_data = additional_use_cases.get(use_case_name.lower().replace(" ", "_"), use_case)
        
        # Get recommendations
        recommendations = filter_system.get_vendor_recommendations(use_case_data)
        
        # Format results for display
        result_text = f"# 📊 Vendor Recommendations for: {use_case_data['name']}\n\n"
        result_text += f"**Total matches found:** {recommendations['summary']['total_matches']}\n"
        result_text += f"**Perfect matches:** {recommendations['summary']['perfect_matches']}\n"
        result_text += f"**Good matches:** {recommendations['summary']['good_matches']}\n"
        result_text += f"**Partial matches:** {recommendations['summary']['partial_matches']}\n\n"
        
        if recommendations['perfect_matches']:
            result_text += "## 🎯 Perfect Matches\n\n"
            for match in recommendations['perfect_matches']:
                vendor = match['vendor']
                result_text += f"### {vendor['model_name']}\n"
                result_text += f"- **Deployment:** {vendor['deployment_type']}\n"
                result_text += f"- **Latency:** {vendor['latency_support']}\n"
                result_text += f"- **Input:** {vendor['input_modalities']}\n"
                result_text += f"- **Output:** {vendor['output_modalities']}\n"
                result_text += f"- **Match Score:** {match['score']:.2f}\n\n"
        
        if recommendations['good_matches'] and not recommendations['perfect_matches']:
            result_text += "## ✅ Good Matches\n\n"
            for match in recommendations['good_matches'][:5]:  # Show top 5
                vendor = match['vendor']
                result_text += f"### {vendor['model_name']}\n"
                result_text += f"- **Match Score:** {match['score']:.2f}\n"
                result_text += f"- **Deployment:** {vendor['deployment_type']}\n"
                result_text += f"- **Latency:** {vendor['latency_support']}\n\n"
        
        if recommendations['partial_matches'] and not recommendations['perfect_matches'] and not recommendations['good_matches']:
            result_text += "## ⚠️ Partial Matches\n\n"
            for match in recommendations['partial_matches'][:3]:  # Show top 3
                vendor = match['vendor']
                result_text += f"### {vendor['model_name']}\n"
                result_text += f"- **Match Score:** {match['score']:.2f}\n"
                result_text += f"- **Deployment:** {vendor['deployment_type']}\n"
                result_text += f"- **Latency:** {vendor['latency_support']}\n\n"
        
        if not any([recommendations['perfect_matches'], recommendations['good_matches'], recommendations['partial_matches']]):
            result_text += "## ❌ No Matches Found\n\n"
            result_text += "No vendors match your current requirements. Try relaxing some constraints.\n\n"
        
        return result_text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_filter_stats():
    """Get statistics about the vendor database"""
    try:
        # Get various filter results
        cloud_vendors = filter_system.filter_by_deployment('Cloud')
        realtime_vendors = filter_system.filter_by_latency('real-time')
        batch_vendors = filter_system.filter_by_latency('batch')
        text_vendors = filter_system.filter_by_modality(['Text'], ['Text'])
        
        stats_text = "# 📈 Vendor Database Statistics\n\n"
        stats_text += f"**Total vendors in database:** {len(filter_system.vendor_database)}\n\n"
        stats_text += "## Filter Statistics\n\n"
        stats_text += f"**Cloud deployment:** {len(cloud_vendors)} vendors\n"
        stats_text += f"**Real-time latency:** {len(realtime_vendors)} vendors\n"
        stats_text += f"**Batch latency:** {len(batch_vendors)} vendors\n"
        stats_text += f"**Text input/output:** {len(text_vendors)} vendors\n\n"
        
        # Show some example vendors
        stats_text += "## Sample Vendors\n\n"
        for vendor in filter_system.vendor_database[:5]:
            stats_text += f"**{vendor['model_name']}**\n"
            stats_text += f"- Deployment: {vendor['deployment_type']}\n"
            stats_text += f"- Latency: {vendor['latency_support']}\n"
            stats_text += f"- Input: {vendor['input_modalities']}\n"
            stats_text += f"- Output: {vendor['output_modalities']}\n\n"
        
        return stats_text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_example_use_cases():
    """Display example use cases"""
    examples_text = "# 📋 Example Use Cases\n\n"
    
    # Insurance claims
    examples_text += "## 🏥 Insurance Claims Priority Classification\n\n"
    examples_text += "**Description:** Automated system to classify incoming insurance claims based on priority level.\n\n"
    examples_text += "**Requirements:**\n"
    examples_text += "- Deployment: Cloud (for scalability)\n"
    examples_text += "- Latency: Real-time (5-second response)\n"
    examples_text += "- Modality: Text input → Text output\n\n"
    examples_text += "**Example Input:**\n"
    examples_text += "> Patient experienced severe chest pain and shortness of breath. Emergency room visit required. Diagnosis: Acute myocardial infarction.\n\n"
    examples_text += "**Expected Output:**\n"
    examples_text += "> Priority: HIGH - Life-threatening condition requiring immediate attention\n\n"
    
    # Customer support
    examples_text += "## 💬 Customer Support Chatbot\n\n"
    examples_text += "**Description:** AI-powered chatbot to handle customer inquiries.\n\n"
    examples_text += "**Requirements:**\n"
    examples_text += "- Deployment: Cloud (global accessibility)\n"
    examples_text += "- Latency: Real-time (2-second response)\n"
    examples_text += "- Modality: Text input → Text/Chat output\n\n"
    
    # Document analysis
    examples_text += "## 📄 Legal Document Analysis\n\n"
    examples_text += "**Description:** Analyze legal documents to extract key information.\n\n"
    examples_text += "**Requirements:**\n"
    examples_text += "- Deployment: On-premise (data privacy)\n"
    examples_text += "- Latency: Batch (30-minute processing)\n"
    examples_text += "- Modality: Text/Image input → Text output\n\n"
    
    return examples_text

# Create the Gradio interface
def create_interface():
    """Create the main Gradio interface"""
    
    with gr.Blocks(
        title="LLM Vendor Filtering System",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .main-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        """
    ) as demo:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🚀 LLM Vendor Filtering System</h1>
            <p>Find the perfect LLM vendor for your specific requirements</p>
        </div>
        """)
        
        with gr.Tabs():
            
            # Main filtering tab
            with gr.TabItem("🔍 Vendor Filtering", id=0):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📋 Use Case Selection")
                        
                        use_case_dropdown = gr.Dropdown(
                            choices=[
                                "Insurance Claims Classification",
                                "Customer Support Chatbot", 
                                "Legal Document Analysis",
                                "Marketing Content Generation",
                                "Custom Use Case"
                            ],
                            value="Insurance Claims Classification",
                            label="Select Use Case or Create Custom"
                        )
                        
                        custom_description = gr.Textbox(
                            label="Custom Use Case Description (optional)",
                            placeholder="Describe your use case requirements...",
                            lines=3
                        )
                        
                        gr.Markdown("### ⚙️ Requirements")
                        
                        deployment_dropdown = gr.Dropdown(
                            choices=["Cloud", "On-premise", "Any"],
                            value="Cloud",
                            label="Deployment Type"
                        )
                        
                        latency_dropdown = gr.Dropdown(
                            choices=["Real-time", "Batch", "Any"],
                            value="Real-time",
                            label="Latency Requirement"
                        )
                        
                        input_modalities = gr.CheckboxGroup(
                            choices=["Text", "Image", "Video", "Speech"],
                            value=["Text"],
                            label="Input Modalities"
                        )
                        
                        output_modalities = gr.CheckboxGroup(
                            choices=["Text", "Chat", "Image", "Video", "Speech", "Embedding"],
                            value=["Text"],
                            label="Output Modalities"
                        )
                        
                        filter_button = gr.Button("🔍 Find Vendors", variant="primary", size="lg")
                    
                    with gr.Column(scale=2):
                        gr.Markdown("### 📊 Results")
                        results_output = gr.Markdown(
                            value="# Welcome to the LLM Vendor Filtering System!\n\nSelect your requirements and click 'Find Vendors' to get started.",
                            label="Recommendations"
                        )
                
                # Connect the button
                filter_button.click(
                    fn=get_vendor_recommendations,
                    inputs=[
                        use_case_dropdown,
                        deployment_dropdown,
                        latency_dropdown,
                        input_modalities,
                        output_modalities,
                        custom_description
                    ],
                    outputs=results_output
                )
            
            # Statistics tab
            with gr.TabItem("📈 Database Statistics", id=1):
                stats_button = gr.Button("📊 Load Statistics", variant="secondary")
                stats_output = gr.Markdown(label="Database Statistics")
                
                stats_button.click(
                    fn=get_filter_stats,
                    outputs=stats_output
                )
            
            # Examples tab
            with gr.TabItem("📋 Examples", id=2):
                examples_output = gr.Markdown(
                    value=show_example_use_cases(),
                    label="Example Use Cases"
                )
            
            # About tab
            with gr.TabItem("ℹ️ About", id=3):
                gr.Markdown("""
                # About the LLM Vendor Filtering System
                
                This system helps you find the most suitable LLM vendors based on three key criteria:
                
                ## 🎯 Filtering Criteria
                
                1. **Deployment Type**: Cloud, On-premise, or Hybrid
                2. **Latency Requirements**: Real-time, Batch, or Both
                3. **Modality Support**: Input (Text, Image, Video, Speech) and Output (Text, Chat, Image, Video, Speech, Embedding)
                
                ## 🏆 Recommendation Scoring
                
                - **Perfect Matches** (Score ≥ 0.9): Meet all requirements exactly
                - **Good Matches** (Score ≥ 0.7): Meet most requirements with minor considerations
                - **Partial Matches** (Score < 0.7): Meet some requirements but may need additional configuration
                
                ## 📊 Database
                
                The system contains information about **66 LLM vendors** from major providers including:
                - Anthropic (Claude models)
                - Meta (Llama models)
                - Mistral AI
                - Cohere
                - Amazon (Titan, Nova)
                - And many more...
                
                ## 🚀 How to Use
                
                1. Select a predefined use case or create a custom one
                2. Specify your deployment, latency, and modality requirements
                3. Click "Find Vendors" to get personalized recommendations
                4. Review the results and choose the best vendor for your needs
                
                ## 🔧 Technical Details
                
                - Built with Python and Gradio
                - No external dependencies (pure Python implementation)
                - Real-time filtering and scoring
                - Comprehensive vendor database
                
                ---
                
                **Created for efficient LLM vendor selection and comparison.**
                """)
    
    return demo

# Launch the interface
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
        title="LLM Vendor Filtering System"
    ) 