import os
import google.generativeai as genai
import json

def get_ai_suggestions(title: str) -> dict:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    genai.configure(api_key=GEMINI_API_KEY)

    # For text-only input, use the gemini-pro model
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze the following task title and suggest a 'priority' (Low, Medium, High) and a 'label' (e.g., Work, Personal, Shopping, Study, Home, Health, Finance, Other).
    Return the response as a JSON object with keys "priority" and "label".
    Only return the JSON object, do not include any other text or formatting.

    Task Title: "{title}"
    """

    try:
        response = model.generate_content(prompt)
        # Assuming the model returns a JSON string in its text response
        json_response = json.loads(response.text)
        
        priority = json_response.get("priority", "Medium")
        label = json_response.get("label", "Other")
        
        return {"priority": priority, "label": label}
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Fallback in case of API error or malformed response
        return {"priority": "Medium", "label": "Other"}

if __name__ == '__main__':
    # Example usage (requires GEMINI_API_KEY to be set in environment)
    # You can set it like: $env:GEMINI_API_KEY="YOUR_API_KEY"
    print("Testing ai_service.py...")
    
    # Test with a sample task title
    sample_title_1 = "Prepare presentation for Monday meeting"
    suggestions_1 = get_ai_suggestions(sample_title_1)
    print(f"Suggestions for '{sample_title_1}': {suggestions_1}")

    sample_title_2 = "Buy groceries: milk, eggs, bread"
    suggestions_2 = get_ai_suggestions(sample_title_2)
    print(f"Suggestions for '{sample_title_2}': {suggestions_2}")

    sample_title_3 = "Fix bug in login module"
    suggestions_3 = get_ai_suggestions(sample_title_3)
    print(f"Suggestions for '{sample_title_3}': {suggestions_3}")
