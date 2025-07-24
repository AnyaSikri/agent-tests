#!/usr/bin/env python3
"""
Simple Web UI for Vendor Filtering System
A Flask-based web interface that doesn't require Gradio
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
from vendor_database_simple import create_vendor_database, save_database
from vendor_filter import VendorFilter
from user_input_example import use_case, additional_use_cases

app = Flask(__name__)

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

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Vendor Filtering System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .form-section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .form-section h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        
        select, input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        select:focus, input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .checkbox-item input[type="checkbox"] {
            width: auto;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .results {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        .results h3 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .vendor-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .vendor-name {
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        
        .vendor-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            font-size: 14px;
        }
        
        .vendor-detail {
            color: #666;
        }
        
        .vendor-detail strong {
            color: #333;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: 600;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #d63031;
        }
        
        @media (max-width: 768px) {
            .content {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 LLM Vendor Filtering System</h1>
            <p>Find the perfect LLM vendor for your specific requirements</p>
        </div>
        
        <div class="content">
            <div class="form-section">
                <h3>📋 Use Case Selection</h3>
                <div class="form-group">
                    <label for="use-case">Select Use Case:</label>
                    <select id="use-case" name="use_case">
                        <option value="Insurance Claims Classification">Insurance Claims Classification</option>
                        <option value="Customer Support Chatbot">Customer Support Chatbot</option>
                        <option value="Legal Document Analysis">Legal Document Analysis</option>
                        <option value="Marketing Content Generation">Marketing Content Generation</option>
                        <option value="Custom Use Case">Custom Use Case</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="custom-description">Custom Use Case Description (optional):</label>
                    <textarea id="custom-description" name="custom_description" rows="3" placeholder="Describe your use case requirements..."></textarea>
                </div>
            </div>
            
            <div class="form-section">
                <h3>⚙️ Requirements</h3>
                <div class="form-group">
                    <label for="deployment">Deployment Type:</label>
                    <select id="deployment" name="deployment">
                        <option value="Cloud">Cloud</option>
                        <option value="On-premise">On-premise</option>
                        <option value="Any">Any</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="latency">Latency Requirement:</label>
                    <select id="latency" name="latency">
                        <option value="Real-time">Real-time</option>
                        <option value="Batch">Batch</option>
                        <option value="Any">Any</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Input Modalities:</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="input-text" name="input_modalities" value="Text" checked>
                            <label for="input-text">Text</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="input-image" name="input_modalities" value="Image">
                            <label for="input-image">Image</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="input-video" name="input_modalities" value="Video">
                            <label for="input-video">Video</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="input-speech" name="input_modalities" value="Speech">
                            <label for="input-speech">Speech</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Output Modalities:</label>
                    <div class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" id="output-text" name="output_modalities" value="Text" checked>
                            <label for="output-text">Text</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="output-chat" name="output_modalities" value="Chat">
                            <label for="output-chat">Chat</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="output-image" name="output_modalities" value="Image">
                            <label for="output-image">Image</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="output-video" name="output_modalities" value="Video">
                            <label for="output-video">Video</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="output-speech" name="output_modalities" value="Speech">
                            <label for="output-speech">Speech</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" id="output-embedding" name="output_modalities" value="Embedding">
                            <label for="output-embedding">Embedding</label>
                        </div>
                    </div>
                </div>
                
                <button class="btn" onclick="findVendors()">🔍 Find Vendors</button>
            </div>
            
            <div id="results" class="results" style="display: none;">
                <h3>📊 Results</h3>
                <div id="results-content"></div>
            </div>
        </div>
    </div>
    
    <script>
        function findVendors() {
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('results-content');
            
            // Show loading
            resultsDiv.style.display = 'block';
            resultsContent.innerHTML = '<div class="loading">🔍 Finding vendors...</div>';
            
            // Get form data
            const formData = {
                use_case: document.getElementById('use-case').value,
                deployment: document.getElementById('deployment').value,
                latency: document.getElementById('latency').value,
                custom_description: document.getElementById('custom-description').value,
                input_modalities: Array.from(document.querySelectorAll('input[name="input_modalities"]:checked')).map(cb => cb.value),
                output_modalities: Array.from(document.querySelectorAll('input[name="output_modalities"]:checked')).map(cb => cb.value)
            };
            
            // Send request
            fetch('/api/find_vendors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsContent.innerHTML = `<div class="error">❌ ${data.error}</div>`;
                } else {
                    displayResults(data);
                }
            })
            .catch(error => {
                resultsContent.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            });
        }
        
        function displayResults(data) {
            const resultsContent = document.getElementById('results-content');
            
            let html = `
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">${data.summary.total_matches}</div>
                        <div class="stat-label">Total Matches</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.summary.perfect_matches}</div>
                        <div class="stat-label">Perfect Matches</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.summary.good_matches}</div>
                        <div class="stat-label">Good Matches</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.summary.partial_matches}</div>
                        <div class="stat-label">Partial Matches</div>
                    </div>
                </div>
            `;
            
            if (data.perfect_matches && data.perfect_matches.length > 0) {
                html += '<h4>🎯 Perfect Matches</h4>';
                data.perfect_matches.forEach(match => {
                    html += createVendorCard(match.vendor, match.score, 'Perfect Match');
                });
            }
            
            if (data.good_matches && data.good_matches.length > 0 && (!data.perfect_matches || data.perfect_matches.length === 0)) {
                html += '<h4>✅ Good Matches</h4>';
                data.good_matches.slice(0, 5).forEach(match => {
                    html += createVendorCard(match.vendor, match.score, 'Good Match');
                });
            }
            
            if (data.partial_matches && data.partial_matches.length > 0 && 
                (!data.perfect_matches || data.perfect_matches.length === 0) && 
                (!data.good_matches || data.good_matches.length === 0)) {
                html += '<h4>⚠️ Partial Matches</h4>';
                data.partial_matches.slice(0, 3).forEach(match => {
                    html += createVendorCard(match.vendor, match.score, 'Partial Match');
                });
            }
            
            if (!data.perfect_matches?.length && !data.good_matches?.length && !data.partial_matches?.length) {
                html += '<div class="error">❌ No vendors match your current requirements. Try relaxing some constraints.</div>';
            }
            
            resultsContent.innerHTML = html;
        }
        
        function createVendorCard(vendor, score, matchType) {
            return `
                <div class="vendor-card">
                    <div class="vendor-name">${vendor.model_name}</div>
                    <div class="vendor-details">
                        <div class="vendor-detail"><strong>Match Type:</strong> ${matchType}</div>
                        <div class="vendor-detail"><strong>Score:</strong> ${score.toFixed(2)}</div>
                        <div class="vendor-detail"><strong>Deployment:</strong> ${vendor.deployment_type}</div>
                        <div class="vendor-detail"><strong>Latency:</strong> ${vendor.latency_support}</div>
                        <div class="vendor-detail"><strong>Input:</strong> ${vendor.input_modalities}</div>
                        <div class="vendor-detail"><strong>Output:</strong> ${vendor.output_modalities}</div>
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/find_vendors', methods=['POST'])
def find_vendors():
    try:
        data = request.json
        
        # Create use case from user input
        if data['use_case'] == "Custom Use Case":
            use_case_data = {
                "name": "Custom Use Case",
                "description": data.get('custom_description', 'User-defined requirements'),
                "requirements": {
                    "deployment": {"type": data['deployment'], "reason": "User specified"},
                    "latency": {"type": data['latency'], "max_response_time": "User specified", "reason": "User specified"},
                    "modality": {
                        "input": data.get('input_modalities', []),
                        "output": data.get('output_modalities', []),
                        "reason": "User specified"
                    }
                }
            }
        else:
            # Use predefined use case
            if data['use_case'] == "Insurance Claims Classification":
                use_case_data = use_case
            else:
                use_case_data = additional_use_cases.get(data['use_case'].lower().replace(" ", "_"), use_case)
        
        # Get recommendations
        recommendations = filter_system.get_vendor_recommendations(use_case_data)
        
        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting LLM Vendor Filtering System Web UI...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000) 