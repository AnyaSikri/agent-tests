#!/usr/bin/env python3
"""
Simple UI for Vendor Filtering System
A lightweight web interface using Python's built-in HTTP server
No external dependencies required!
"""

import json
import os
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from vendor_database_simple import create_vendor_database, save_database
from vendor_filter import VendorFilter
from user_input_example import use_case, additional_use_cases

# Initialize the vendor filter system
def initialize_system():
    """Initialize the vendor database and filter system"""
    # Always regenerate the database to ensure it's up to date
    print("Regenerating vendor database...")
    save_database()
    
    filter_system = VendorFilter()
    return filter_system

# Global filter system
filter_system = initialize_system()

# HTML template with embedded JavaScript
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
        // Sample vendor data for demonstration
        const sampleVendors = [
            {
                "model_name": "Claude 3.7 Sonnet",
                "deployment_type": "Cloud",
                "latency_support": "real-time only",
                "input_modalities": "Text, Image",
                "output_modalities": "Text, Chat"
            },
            {
                "model_name": "Mistral 7B Instruct",
                "deployment_type": "Cloud",
                "latency_support": "real-time only",
                "input_modalities": "Text",
                "output_modalities": "Text"
            },
            {
                "model_name": "Llama 3.1 405B Instruct",
                "deployment_type": "Cloud",
                "latency_support": "batch",
                "input_modalities": "Text",
                "output_modalities": "Text, Chat"
            }
        ];
        
        function findVendors() {
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('results-content');
            
            // Show loading
            resultsDiv.style.display = 'block';
            resultsContent.innerHTML = '<div class="loading">🔍 Finding vendors...</div>';
            
            // Simulate API call with setTimeout
            setTimeout(() => {
                // Get form data
                const useCase = document.getElementById('use-case').value;
                const deployment = document.getElementById('deployment').value;
                const latency = document.getElementById('latency').value;
                const inputModalities = Array.from(document.querySelectorAll('input[name="input_modalities"]:checked')).map(cb => cb.value);
                const outputModalities = Array.from(document.querySelectorAll('input[name="output_modalities"]:checked')).map(cb => cb.value);
                
                // Filter vendors based on requirements
                const filteredVendors = sampleVendors.filter(vendor => {
                    const deploymentMatch = deployment === 'Any' || vendor.deployment_type.toLowerCase() === deployment.toLowerCase();
                    const latencyMatch = latency === 'Any' || vendor.latency_support.toLowerCase().includes(latency.toLowerCase());
                    const inputMatch = inputModalities.length === 0 || inputModalities.some(mod => vendor.input_modalities.toLowerCase().includes(mod.toLowerCase()));
                    const outputMatch = outputModalities.length === 0 || outputModalities.some(mod => vendor.output_modalities.toLowerCase().includes(mod.toLowerCase()));
                    
                    return deploymentMatch && latencyMatch && inputMatch && outputMatch;
                });
                
                // Calculate scores
                const vendorsWithScores = filteredVendors.map(vendor => {
                    let score = 0;
                    if (deployment !== 'Any' && vendor.deployment_type.toLowerCase() === deployment.toLowerCase()) score += 0.25;
                    if (latency !== 'Any' && vendor.latency_support.toLowerCase().includes(latency.toLowerCase())) score += 0.25;
                    if (inputModalities.length === 0 || inputModalities.some(mod => vendor.input_modalities.toLowerCase().includes(mod.toLowerCase()))) score += 0.25;
                    if (outputModalities.length === 0 || outputModalities.some(mod => vendor.output_modalities.toLowerCase().includes(mod.toLowerCase()))) score += 0.25;
                    
                    return { vendor, score };
                });
                
                // Sort by score
                vendorsWithScores.sort((a, b) => b.score - a.score);
                
                // Categorize results
                const perfectMatches = vendorsWithScores.filter(v => v.score >= 0.9);
                const goodMatches = vendorsWithScores.filter(v => v.score >= 0.7 && v.score < 0.9);
                const partialMatches = vendorsWithScores.filter(v => v.score < 0.7);
                
                displayResults({
                    summary: {
                        total_matches: vendorsWithScores.length,
                        perfect_matches: perfectMatches.length,
                        good_matches: goodMatches.length,
                        partial_matches: partialMatches.length
                    },
                    perfect_matches: perfectMatches,
                    good_matches: goodMatches,
                    partial_matches: partialMatches
                });
            }, 1000);
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

class VendorFilterHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        elif self.path.startswith('/api/filter'):
            self.handle_filter_request()
        else:
            super().do_GET()
    
    def handle_filter_request(self):
        """Handle filter API requests"""
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            # Extract filter parameters
            deployment = params.get('deployment', [''])[0]
            latency = params.get('latency', [''])[0]
            input_modalities = params.get('input_modalities', [''])[0]
            output_modalities = params.get('output_modalities', [''])[0]
            
            # Get recommendations from filter system
            use_case = {
                "requirements": {
                    "deployment": {"type": deployment},
                    "latency": {"type": latency},
                    "modality": {
                        "input": [mod.strip() for mod in input_modalities.split(',') if mod.strip()],
                        "output": [mod.strip() for mod in output_modalities.split(',') if mod.strip()]
                    }
                }
            }
            
            recommendations = filter_system.get_recommendations(use_case)
            
            # Send JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                'perfect_matches': recommendations.get('perfect_matches', []),
                'good_matches': recommendations.get('good_matches', []),
                'partial_matches': recommendations.get('partial_matches', [])
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())

def start_server(port=8080):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, VendorFilterHandler)
    print(f"🚀 Server started at http://localhost:{port}")
    print("📱 Open your browser and go to the URL above")
    print("="*60)
    httpd.serve_forever()

def main():
    """Main function"""
    print("🚀 LLM Vendor Filtering System - Simple UI")
    print("="*60)
    
    # Check database
    if not os.path.exists('vendor_database.json'):
        print("📊 Creating vendor database...")
        save_database()
        print("✅ Database created successfully")
    else:
        print("✅ Vendor database already exists")
    
    # Try different ports
    ports = [8080, 8081, 8082, 8083, 8084]
    
    for port in ports:
        try:
            print(f"🔧 Trying port {port}...")
            start_server(port)
            break
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️  Port {port} is in use, trying next port...")
                continue
            else:
                raise e

if __name__ == "__main__":
    main() 