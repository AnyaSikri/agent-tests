import json
from typing import List, Dict, Any, Optional

class VendorFilter:
    """
    A filtering system to match user requirements with vendor capabilities
    based on deployment type, latency needs, and modality requirements.
    """
    
    def __init__(self, database_path: str = 'vendor_database.json'):
        """
        Initialize the vendor filter with the vendor database
        """
        try:
            with open(database_path, 'r') as f:
                self.vendor_database = json.load(f)
        except FileNotFoundError:
            print(f"Database file {database_path} not found. Please run vendor_database.py first.")
            self.vendor_database = []
    
    def filter_by_deployment(self, deployment_type: str) -> List[Dict[str, Any]]:
        """
        Filter vendors by deployment type (Cloud, On-premise, etc.)
        """
        if deployment_type.lower() == 'any':
            return self.vendor_database
        
        filtered_vendors = []
        for vendor in self.vendor_database:
            if vendor['deployment_type'].lower() == deployment_type.lower():
                filtered_vendors.append(vendor)
        
        return filtered_vendors
    
    def filter_by_latency(self, latency_requirement: str) -> List[Dict[str, Any]]:
        """
        Filter vendors by latency support (real-time, batch, etc.)
        """
        if latency_requirement.lower() == 'any':
            return self.vendor_database
        
        filtered_vendors = []
        for vendor in self.vendor_database:
            vendor_latency = vendor['latency_support'].lower()
            req_latency = latency_requirement.lower()
            
            # Handle different latency requirements
            if req_latency == 'real-time':
                if 'real-time' in vendor_latency:
                    filtered_vendors.append(vendor)
            elif req_latency == 'batch':
                if 'batch' in vendor_latency:
                    filtered_vendors.append(vendor)
            elif req_latency == 'both':
                filtered_vendors.append(vendor)
        
        return filtered_vendors
    
    def filter_by_modality(self, input_modalities: List[str], output_modalities: List[str]) -> List[Dict[str, Any]]:
        """
        Filter vendors by input and output modality requirements
        """
        if not input_modalities and not output_modalities:
            return self.vendor_database
        
        filtered_vendors = []
        for vendor in self.vendor_database:
            vendor_input = vendor['input_modalities'].lower()
            vendor_output = vendor['output_modalities'].lower()
            
            # Check input modality requirements
            input_match = True
            if input_modalities:
                input_match = any(modality.lower() in vendor_input for modality in input_modalities)
            
            # Check output modality requirements
            output_match = True
            if output_modalities:
                output_match = any(modality.lower() in vendor_output for modality in output_modalities)
            
            if input_match and output_match:
                filtered_vendors.append(vendor)
        
        return filtered_vendors
    
    def filter_vendors(self, 
                      deployment_type: str = 'any',
                      latency_requirement: str = 'any',
                      input_modalities: List[str] = None,
                      output_modalities: List[str] = None) -> List[Dict[str, Any]]:
        """
        Apply all filters to find matching vendors
        """
        if input_modalities is None:
            input_modalities = []
        if output_modalities is None:
            output_modalities = []
        
        # Apply filters sequentially
        filtered = self.vendor_database
        
        if deployment_type != 'any':
            filtered = self.filter_by_deployment(deployment_type)
        
        if latency_requirement != 'any':
            filtered = self.filter_by_latency(latency_requirement)
        
        if input_modalities or output_modalities:
            filtered = self.filter_by_modality(input_modalities, output_modalities)
        
        return filtered
    
    def get_recommendations(self, use_case_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get vendor recommendations based on use case requirements
        """
        requirements = use_case_requirements['requirements']
        
        # Extract requirements
        deployment_req = requirements['deployment']['type']
        latency_req = requirements['latency']['type']
        input_modalities = requirements['modality']['input']
        output_modalities = requirements['modality']['output']
        
        # Get matching vendors
        matching_vendors = self.filter_vendors(
            deployment_type=deployment_req,
            latency_requirement=latency_req,
            input_modalities=input_modalities,
            output_modalities=output_modalities
        )
        
        # Categorize recommendations
        recommendations = {
            'perfect_matches': [],
            'good_matches': [],
            'partial_matches': [],
            'summary': {
                'total_matches': len(matching_vendors),
                'perfect_matches': 0,
                'good_matches': 0,
                'partial_matches': 0
            }
        }
        
        for vendor in matching_vendors:
            score = self._calculate_match_score(vendor, requirements)
            
            if score >= 0.9:
                recommendations['perfect_matches'].append({
                    'vendor': vendor,
                    'score': score,
                    'reason': 'Perfect match for all requirements'
                })
                recommendations['summary']['perfect_matches'] += 1
            elif score >= 0.7:
                recommendations['good_matches'].append({
                    'vendor': vendor,
                    'score': score,
                    'reason': 'Good match with minor considerations'
                })
                recommendations['summary']['good_matches'] += 1
            else:
                recommendations['partial_matches'].append({
                    'vendor': vendor,
                    'score': score,
                    'reason': 'Partial match - may need additional configuration'
                })
                recommendations['summary']['partial_matches'] += 1
        
        return recommendations
    
    def _calculate_match_score(self, vendor: Dict[str, Any], requirements: Dict[str, Any]) -> float:
        """
        Calculate a match score between vendor capabilities and requirements
        """
        score = 0.0
        total_criteria = 0
        
        # Deployment match
        if vendor['deployment_type'].lower() == requirements['deployment']['type'].lower():
            score += 1.0
        total_criteria += 1
        
        # Latency match
        vendor_latency = vendor['latency_support'].lower()
        req_latency = requirements['latency']['type'].lower()
        if req_latency == 'real-time' and 'real-time' in vendor_latency:
            score += 1.0
        elif req_latency == 'batch' and 'batch' in vendor_latency:
            score += 1.0
        elif req_latency == 'both':
            score += 1.0
        total_criteria += 1
        
        # Modality match
        input_match = any(modality.lower() in vendor['input_modalities'].lower() 
                         for modality in requirements['modality']['input'])
        output_match = any(modality.lower() in vendor['output_modalities'].lower() 
                          for modality in requirements['modality']['output'])
        
        if input_match:
            score += 1.0
        if output_match:
            score += 1.0
        total_criteria += 2
        
        return score / total_criteria if total_criteria > 0 else 0.0
    
    def print_recommendations(self, recommendations: Dict[str, Any], use_case_name: str):
        """
        Print formatted vendor recommendations
        """
        print(f"\n=== VENDOR RECOMMENDATIONS FOR: {use_case_name} ===")
        print(f"Total matches found: {recommendations['summary']['total_matches']}")
        print(f"Perfect matches: {recommendations['summary']['perfect_matches']}")
        print(f"Good matches: {recommendations['summary']['good_matches']}")
        print(f"Partial matches: {recommendations['summary']['partial_matches']}")
        
        if recommendations['perfect_matches']:
            print("\n🎯 PERFECT MATCHES:")
            for match in recommendations['perfect_matches']:
                vendor = match['vendor']
                print(f"  • {vendor['model_name']} (Score: {match['score']:.2f})")
                print(f"    - Deployment: {vendor['deployment_type']}")
                print(f"    - Latency: {vendor['latency_support']}")
                print(f"    - Input: {vendor['input_modalities']}")
                print(f"    - Output: {vendor['output_modalities']}")
                print(f"    - Reason: {match['reason']}\n")
        
        if recommendations['good_matches']:
            print("\n✅ GOOD MATCHES:")
            for match in recommendations['good_matches'][:3]:  # Show top 3
                vendor = match['vendor']
                print(f"  • {vendor['model_name']} (Score: {match['score']:.2f})")
                print(f"    - {match['reason']}\n")
        
        if recommendations['partial_matches'] and not recommendations['perfect_matches'] and not recommendations['good_matches']:
            print("\n⚠️  PARTIAL MATCHES:")
            for match in recommendations['partial_matches'][:3]:  # Show top 3
                vendor = match['vendor']
                print(f"  • {vendor['model_name']} (Score: {match['score']:.2f})")
                print(f"    - {match['reason']}\n")

def main():
    """
    Example usage of the vendor filter
    """
    # Initialize the filter
    filter_system = VendorFilter()
    
    # Example: Insurance claims use case
    from user_input_example import use_case
    
    print("🔍 ANALYZING VENDOR DATABASE...")
    print(f"Total vendors in database: {len(filter_system.vendor_database)}")
    
    # Get recommendations
    recommendations = filter_system.get_vendor_recommendations(use_case)
    
    # Print results
    filter_system.print_recommendations(recommendations, use_case['name'])
    
    # Example: Test different filters
    print("\n=== FILTER EXAMPLES ===")
    
    # Cloud deployment only
    cloud_vendors = filter_system.filter_by_deployment('Cloud')
    print(f"Cloud deployment vendors: {len(cloud_vendors)}")
    
    # Real-time latency only
    realtime_vendors = filter_system.filter_by_latency('real-time')
    print(f"Real-time latency vendors: {len(realtime_vendors)}")
    
    # Text input/output only
    text_vendors = filter_system.filter_by_modality(['Text'], ['Text'])
    print(f"Text input/output vendors: {len(text_vendors)}")

if __name__ == "__main__":
    main() 