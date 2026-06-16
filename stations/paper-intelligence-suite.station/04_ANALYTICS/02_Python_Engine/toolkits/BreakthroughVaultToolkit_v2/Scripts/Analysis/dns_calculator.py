# dns_calculator.py
"""
Calculate Disambiguation Necessity Score (DNS) for terms.
Higher score = more critical need for custom definition.
"""

def calculate_dns(num_meanings, conceptual_distance, usage_freq, overlap_percent):
    """
    Calculate Disambiguation Necessity Score.
    
    Args:
        num_meanings: Number of conflicting traditional definitions (e.g., 3 for physics/theology/philosophy)
        conceptual_distance: 0-10 scale of how different meanings are (10 = completely different)
        usage_freq: 0-1 normalized usage frequency in vault (occurrences / total terms)
        overlap_percent: Highest overlap with any traditional definition (0-100)
    
    Returns:
        DNS score (higher = more critical)
    """
    dns = num_meanings * conceptual_distance * usage_freq * (1 - overlap_percent/100)
    return round(dns, 2)


def interpret_dns(dns_score):
    """
    Interpret DNS score and provide recommendation.
    
    Args:
        dns_score: Calculated DNS value
    
    Returns:
        Dictionary with interpretation and action
    """
    if dns_score > 5.0:
        severity = "CRITICAL"
        action = "New definition ESSENTIAL - creates major confusion without it"
        priority = 1
    elif dns_score > 2.5:
        severity = "HIGH"
        action = "New definition STRONGLY RECOMMENDED - significant confusion likely"
        priority = 2
    elif dns_score > 1.0:
        severity = "MEDIUM"
        action = "Clarification needed - traditional definition may work with explanation"
        priority = 3
    else:
        severity = "LOW"
        action = "Traditional definition acceptable with brief note"
        priority = 4
    
    return {
        'dns_score': dns_score,
        'severity': severity,
        'action': action,
        'priority': priority
    }


if __name__ == "__main__":
    print("="*60)
    print("DISAMBIGUATION NECESSITY SCORE (DNS) ANALYSIS")
    print("="*60)
    print()
    
    # Test cases
    test_terms = [
        {
            'name': 'Coherence',
            'num_meanings': 3,        # Physics, Theology, Philosophy
            'conceptual_distance': 8, # Very different meanings
            'usage_freq': 0.85,       # Used extensively
            'overlap_percent': 30     # Only 30% overlap
        },
        {
            'name': 'Observer',
            'num_meanings': 3,        # Physics device, God, Consciousness
            'conceptual_distance': 9, # Extremely different
            'usage_freq': 0.75,       # Used frequently
            'overlap_percent': 20     # Very little overlap
        },
        {
            'name': 'Energy',
            'num_meanings': 2,        # Physics, Spiritual
            'conceptual_distance': 6, # Moderately different
            'usage_freq': 0.65,       # Used fairly often
            'overlap_percent': 45     # Moderate overlap
        },
        {
            'name': 'Time',
            'num_meanings': 2,        # Chronological, Kairos
            'conceptual_distance': 5, # Somewhat different
            'usage_freq': 0.50,       # Average usage
            'overlap_percent': 55     # High overlap
        }
    ]
    
    results = []
    for term in test_terms:
        dns = calculate_dns(
            term['num_meanings'],
            term['conceptual_distance'],
            term['usage_freq'],
            term['overlap_percent']
        )
        interpretation = interpret_dns(dns)
        
        results.append({
            'name': term['name'],
            **interpretation
        })
    
    # Sort by priority (1 = most critical)
    results.sort(key=lambda x: x['priority'])
    
    # Display results
    for result in results:
        print(f"TERM: {result['name']}")
        print(f"  DNS Score: {result['dns_score']}")
        print(f"  Severity: {result['severity']}")
        print(f"  Priority: {result['priority']}")
        print(f"  Action: {result['action']}")
        print()
        print("-"*60)
        print()
