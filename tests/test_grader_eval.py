"""
Eval harness for grade_answer().

Mocks the Claude API so no API key is needed. Tests that grade_answer()
correctly parses Claude's response and handles edge cases in the output format.

Run with:  pytest tests/test_grader_eval.py -v
"""
import pytest
from unittest.mock import patch, MagicMock
from rag_utils import grade_answer


def _mock_claude_response(text: str):
    """Build a fake Anthropic API response returning the given text."""
    mock_content = MagicMock()
    mock_content.text = text

    mock_message = MagicMock()
    mock_message.content = [mock_content]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    return mock_client


# --- Parsing: does grade_answer correctly read Claude's YES/NO response? ---

def test_yes_response_returns_correct():
    client = _mock_claude_response("YES\nGreat job! That is exactly right!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, feedback = grade_answer("What color is grass?", "green", "green")
    assert is_correct is True

def test_no_response_returns_incorrect():
    client = _mock_claude_response("NO\nNot quite — the answer is green!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, feedback = grade_answer("What color is grass?", "green", "red")
    assert is_correct is False

def test_feedback_is_returned():
    client = _mock_claude_response("YES\nAmazing work, you got it!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        _, feedback = grade_answer("What color is grass?", "green", "green")
    assert feedback == "Amazing work, you got it!"

def test_yes_with_lowercase_still_correct():
    client = _mock_claude_response("yes\nWell done!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, _ = grade_answer("What color is grass?", "green", "green")
    assert is_correct is True

def test_yes_with_punctuation_still_correct():
    client = _mock_claude_response("YES!\nFantastic answer!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, _ = grade_answer("What color is grass?", "green", "green")
    assert is_correct is True


# --- Edge cases: what happens if Claude's response is malformed? ---

def test_missing_feedback_line_correct_answer():
    """Claude returns only YES with no second line."""
    client = _mock_claude_response("YES")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, feedback = grade_answer("What color is grass?", "green", "green")
    assert is_correct is True
    assert feedback  # should still return something, not crash

def test_missing_feedback_line_wrong_answer():
    """Claude returns only NO with no second line — fallback should include the correct answer."""
    client = _mock_claude_response("NO")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, feedback = grade_answer("What color is grass?", "green", "purple")
    assert is_correct is False
    assert "green" in feedback  # fallback message should mention the correct answer

def test_extra_whitespace_in_response():
    client = _mock_claude_response("  YES  \n  Good job!  ")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        is_correct, feedback = grade_answer("What color is grass?", "green", "green")
    assert is_correct is True


# --- Claude is called with the right inputs ---

def test_correct_answer_is_passed_to_claude():
    client = _mock_claude_response("YES\nGreat!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        grade_answer("What color is grass?", "green", "green")

    call_kwargs = client.messages.create.call_args
    prompt_text = call_kwargs.kwargs["messages"][0]["content"]
    assert "green" in prompt_text
    assert "What color is grass?" in prompt_text

def test_grade_answer_returns_tuple():
    client = _mock_claude_response("YES\nGreat!")
    with patch("rag_utils.anthropic.Anthropic", return_value=client):
        result = grade_answer("What color is grass?", "green", "green")
    assert isinstance(result, tuple) and len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)
