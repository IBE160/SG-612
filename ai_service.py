import os
import google.generativeai as genai
import json

def get_ai_suggestions(title: str) -> dict:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        # Fallback if API key is not set, as Gemini API won't work
        # This is considered a fallback scenario
        print("GEMINI_API_KEY not found. Using rule-based fallback.")
        return _rule_based_fallback(title)


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
        
        return {"priority": priority, "label": label, "fallback": False} # Indicate not a fallback
    except Exception as e:
        print(f"Error calling Gemini API or parsing response: {e}. Using rule-based fallback.")
        return _rule_based_fallback(title)

def _rule_based_fallback(title: str) -> dict:
    """
    Implements rule-based fallback logic for AI suggestions.
    """
    title_lower = title.lower()
    
    fallback_suggestions = {}

    # Keyword matching for priority and label
    if "urgent" in title_lower or "now" in title_lower or "critical" in title_lower:
        fallback_suggestions["priority"] = "High"
        fallback_suggestions["label"] = "Urgent"
    elif "meeting" in title_lower or "report" in title_lower or "work" in title_lower:
        fallback_suggestions["priority"] = "Medium"
        fallback_suggestions["label"] = "Work"
    elif "groceries" in title_lower or "shop" in title_lower or "buy" in title_lower:
        fallback_suggestions["priority"] = "Low"
        fallback_suggestions["label"] = "Shopping"
    elif "study" in title_lower or "read" in title_lower or "learn" in title_lower:
        fallback_suggestions["priority"] = "Medium"
        fallback_suggestions["label"] = "Study"
    elif "home" in title_lower or "clean" in title_lower or "chores" in title_lower:
        fallback_suggestions["priority"] = "Low"
        fallback_suggestions["label"] = "Home"
    elif "health" in title_lower or "doctor" in title_lower or "exercise" in title_lower:
        fallback_suggestions["priority"] = "Medium"
        fallback_suggestions["label"] = "Health"
    elif "finance" in title_lower or "bill" in title_lower or "pay" in title_lower:
        fallback_suggestions["priority"] = "High" # Financial tasks often high priority
        fallback_suggestions["label"] = "Finance"
    else:
        # Default fallback if no keywords match
        fallback_suggestions["priority"] = "Low"
        fallback_suggestions["label"] = "Other"
    
    fallback_suggestions["fallback"] = True # Indicate that fallback was used
    return fallback_suggestions

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

    sample_title_4 = "Urgent call with client"
    suggestions_4 = get_ai_suggestions(sample_title_4)
    print(f"Suggestions for '{sample_title_4}': {suggestions_4}")

    sample_title_5 = "Default task title"
    suggestions_5 = get_ai_suggestions(sample_title_5)
    print(f"Suggestions for '{sample_title_5}': {suggestions_5}")