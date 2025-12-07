import pytest
from unittest.mock import MagicMock, patch
import os
import json
from ai_service import get_ai_suggestions

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

    assert suggestions == {"priority": "High", "label": "Work"}
    mock_genai_model.return_value.generate_content.assert_called_once()

def test_get_ai_suggestions_api_error(mock_genai_model):
    # Simulate an API error
    mock_genai_model.return_value.generate_content.side_effect = Exception("API connection error")

    title = "Buy groceries"
    suggestions = get_ai_suggestions(title)

    # Expect fallback values in case of API error
    assert suggestions == {"priority": "Medium", "label": "Other"}
    mock_genai_model.return_value.generate_content.assert_called_once()

def test_get_ai_suggestions_malformed_response(mock_genai_model):
    # Simulate a malformed JSON response
    mock_response = MagicMock()
    mock_response.text = "this is not json"
    mock_genai_model.return_value.generate_content.return_value = mock_response

    title = "Check emails"
    suggestions = get_ai_suggestions(title)

    # Expect fallback values in case of malformed JSON
    assert suggestions == {"priority": "Medium", "label": "Other"}
    mock_genai_model.return_value.generate_content.assert_called_once()

def test_get_ai_suggestions_missing_api_key():
    # Temporarily remove GEMINI_API_KEY from environment for this test
    old_env = os.environ.copy()
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]

    with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
        get_ai_suggestions("Test task without API key")

    # Restore environment
    os.environ.clear()
    os.environ.update(old_env)

