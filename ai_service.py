import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Last inn miljøvariabler (finner GEMINI_API_KEY i .env-filen)
load_dotenv()

def configure_genai():
    """Konfigurerer Google Gemini API med nøkkelen fra .env."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Advarsel: GEMINI_API_KEY ble ikke funnet. Fallback-logikk vil bli brukt.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Feil under konfigurering av Gemini API: {e}")
        return False

# Konfigurer API-en når modulen lastes
is_genai_configured = configure_genai()
model = genai.GenerativeModel('gemini-1.5-flash') if is_genai_configured else None

def get_ai_suggestions(task_title: str) -> dict:
    """
    Får AI-genererte forslag for en oppgavetittel.
    Returnerer en dictionary med 'label' og 'priority'.
    Bruker fallback-logikk ved feil.
    """
    if not is_genai_configured or not model:
        print("Bruker fallback-logikk fordi AI-tjenesten ikke er konfigurert.")
        return _fallback_logic(task_title)

    # System-prompt som instruerer AI-en til å returnere en JSON-struktur
    prompt = f"""
    Analyze the following task and return a clean JSON object with a suggested 'label' and 'priority'.
    Valid labels: School, Work, Home, Health, Finance, Shopping, Other.
    Valid priorities: Low, Medium, High.

    Do not add any commentary or markdown formatting like ```json. Only return the raw JSON object.

    Task: "{task_title}"
    """
    
    try:
        response = model.generate_content(prompt)
        # Renser svaret for å hente ut kun JSON-delen
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        suggestions = json.loads(cleaned_response)
        
        # Valider at vi fikk det vi forventet
        if 'label' in suggestions and 'priority' in suggestions:
            return suggestions
        else:
            print("AI-svar manglet forventede nøkler. Bruker fallback.")
            return _fallback_logic(task_title)

    except Exception as e:
        print(f"En feil oppstod under kall til Gemini API: {e}. Bruker fallback-logikk.")
        return _fallback_logic(task_title)

def _fallback_logic(task_title: str) -> dict:
    """
    Fallback-logikk som beskrevet i prosjektforslaget.
    Bruker enkel nøkkelord-matching.
    """
    task_lower = task_title.lower()
    if 'buy' in task_lower or 'shop' in task_lower or 'grocery' in task_lower:
        label = "Shopping"
    elif 'work' in task_lower or 'meeting' in task_lower or 'report' in task_lower:
        label = "Work"
    elif 'school' in task_lower or 'exam' in task_lower or 'homework' in task_lower or 'study' in task_lower:
        label = "School"
    else:
        label = "Other"
    
    priority = "Low"
    
    return {"label": label, "priority": priority}

# --- Testblokk ---
# Denne koden kjører kun når du kjører 'python ai_service.py' direkte.
# Den lar oss teste at alt fungerer som det skal.
if __name__ == "__main__":
    print("--- Starter test av ai_service.py ---")
    
    # Test 1: En typisk oppgave
    print("\nTest 1: 'Study for math exam tomorrow'")
    suggestions1 = get_ai_suggestions("Study for math exam tomorrow")
    print(f"Forslag: {suggestions1}")

    # Test 2: En annen oppgave som bør utløse fallback-nøkkelord
    print("\nTest 2: 'Buy milk and bread'")
    suggestions2 = get_ai_suggestions("Buy milk and bread")
    print(f"Forslag: {suggestions2}")

    # Test 3: En generell oppgave uten klare nøkkelord
    print("\nTest 3: 'Call mom'")
    suggestions3 = get_ai_suggestions("Call mom")
    print(f"Forslag: {suggestions3}")

    # For å teste feil-scenarioet, kan du midlertidig endre API-nøkkelen i .env til noe ugyldig.
    
    print("\n--- Testen er ferdig ---")
