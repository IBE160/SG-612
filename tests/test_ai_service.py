import pytest
from unittest.mock import MagicMock, patch
import os
import json
from ai_service import get_ai_suggestions, _rule_based_fallback # Import _rule_based_fallback for direct testing

# Mock the os.getenv for GEMINI_API_KEY
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key"}):
        yield

# Mock the google.generativeai client
@pytest.fixture
def mock_genai_model():
    with patch("google.generativeai.GenerativeModel") as mock_model:
        yield mock_model

def test_get_ai_suggestions_success(mock_genai_model):
    # Simulate a successful response from Gemini API
    mock_response = MagicMock()
    mock_response.text = json.dumps({"priority": "High", "label": "Work"})
    mock_genai_model.return_value.generate_content.return_value = mock_response

    title = "Prepare presentation for team meeting"
    suggestions = get_ai_suggestions(title)

    assert suggestions == {"priority": "High", "label": "Work", "fallback": False}
    mock_genai_model.return_value.generate_content.assert_called_once()

def test_get_ai_suggestions_api_error_triggers_fallback(mock_genai_model):
    # Simulate an API error, which should trigger the rule-based fallback
    mock_genai_model.return_value.generate_content.side_effect = Exception("API connection error")

    title = "Buy groceries"
    suggestions = get_ai_suggestions(title)

    # Expect rule-based fallback values in case of API error
    assert suggestions == {"priority": "Low", "label": "Shopping", "fallback": True}
    mock_genai_model.return_value.generate_content.assert_called_once()

def test_get_ai_suggestions_malformed_response_triggers_fallback(mock_genai_model):
    # Simulate a malformed JSON response, which should trigger the rule-based fallback
    mock_response = MagicMock()
    mock_response.text = "this is not json"
    mock_genai_model.return_value.generate_content.return_value = mock_response

    title = "Check emails for work"
    suggestions = get_ai_suggestions(title)

    # Expect rule-based fallback values in case of malformed JSON
    assert suggestions == {"priority": "Medium", "label": "Work", "fallback": True}
    mock_genai_model.return_value.generate_content.assert_called_once()

@patch.dict(os.environ, {"GEMINI_API_KEY": ""}) # Temporarily unset API key for this test
def test_get_ai_suggestions_missing_api_key_triggers_fallback():
    # When API key is missing, _rule_based_fallback should be called directly
    title = "Urgent task"
    suggestions = get_ai_suggestions(title)
    
    # Expect rule-based fallback for "Urgent" keyword
    assert suggestions == {"priority": "High", "label": "Urgent", "fallback": True}

# New tests for _rule_based_fallback function directly
def test_rule_based_fallback_urgent():
    title = "Urgent meeting with client"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "High", "label": "Urgent", "fallback": True}

def test_rule_based_fallback_work():
    title = "Write report for project"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "Medium", "label": "Work", "fallback": True}

def test_rule_based_fallback_shopping():
    title = "Buy some new shoes"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "Low", "label": "Shopping", "fallback": True}

def test_rule_based_fallback_study():
    title = "Study for the exam"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "Medium", "label": "Study", "fallback": True}

def test_rule_based_fallback_home():
    title = "Clean the house"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "Low", "label": "Home", "fallback": True}

def test_rule_based_fallback_health():
    title = "Go to the gym"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "Medium", "label": "Health", "fallback": True}

def test_rule_based_fallback_finance():
    title = "Pay bills online"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "High", "label": "Finance", "fallback": True}

def test_rule_based_fallback_default():
    title = "Random task without keywords"
    suggestions = _rule_based_fallback(title)
    assert suggestions == {"priority": "Low", "label": "Other", "fallback": True}