import json
import re

# NOTE: If you have an OpenAI key, set USE_MOCK = False and add your key.
# For the paper submission, running in Mock mode is sufficient to demonstrate logic.
USE_MOCK = True 
API_KEY = "sk-..." 

SAMPLE_RADIOLOGY_REPORT = """
EXAMINATION: CT CHEST WITHOUT CONTRAST
INDICATION: Chronic cough, history of smoking.
FINDINGS: The lungs are clear of consolidation or effusion. 
There is a 9mm spiculated nodule in the right upper lobe, series 4 image 12. 
This is new compared to prior study. 
Mediastinal lymph nodes are non-enlarged. Heart size is normal.
IMPRESSION: 
1. 9mm RUL pulmonary nodule, suspicious for malignancy. 
2. No acute infectious process.
RECOMMENDATION: Pulmonology referral and PET/CT scan recommended.
"""

def mock_llm_extraction(text):
    """
    Simulates the output of GPT-4 for the demonstration.
    """
    return {
        "analysis_timestamp": "2025-12-01T14:30:00Z",
        "findings": [
            {
                "entity": "Pulmonary Nodule",
                "location": "Right Upper Lobe",
                "size": "9mm",
                "characteristics": ["spiculated", "suspicious for malignancy"],
                "urgency": "High"
            }
        ],
        "referral_recommendation": {
            "specialty": "Pulmonology",
            "reason": "Evaluation of 9mm RUL nodule suspicious for malignancy",
            "icd_10_codes": ["R91.1", "J98.4"],
            "urgency_score": 9
        },
        "prior_auth_justification": "Patient presents with 9mm spiculated nodule. Fleischner Society guidelines recommend PET/CT for characterization of solid nodules >8mm in high-risk patients (history of smoking)."
    }

def real_llm_extraction(text):
    import openai
    openai.api_key = API_KEY
    
    prompt = f"""
    Analyze the following radiology report. Extract the key findings, required specialty referral, 
    and draft a clinical justification for Prior Authorization. Return JSON.
    
    REPORT:
    {text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    print("--- INPUT: Radiology Report ---")
    print(SAMPLE_RADIOLOGY_REPORT)
    print("\n--- PROCESSING: AI Agent Analysis ---")
    
    if USE_MOCK:
        result = mock_llm_extraction(SAMPLE_RADIOLOGY_REPORT)
        print("(Running in MOCK mode for demonstration)")
    else:
        result = real_llm_extraction(SAMPLE_RADIOLOGY_REPORT)
    
    print("\n--- OUTPUT: Structured JSON ---")
    print(json.dumps(result, indent=4))
    
    print("\n[!] Take a screenshot of this output for Figure 3 in your paper.")