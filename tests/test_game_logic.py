import pytest
from logic_utils import get_num_questions, update_score
from rag_utils import get_collection, retrieve_questions


# --- logic_utils tests ---

def test_get_num_questions_returns_positive_int():
    n = get_num_questions()
    assert isinstance(n, int) and n > 0

def test_update_score_correct_adds_ten():
    assert update_score(0, True) == 10
    assert update_score(20, True) == 30

def test_update_score_incorrect_unchanged():
    assert update_score(0, False) == 0
    assert update_score(30, False) == 30

def test_update_score_never_goes_negative():
    assert update_score(0, False) >= 0


# --- retrieve_questions tests ---

@pytest.fixture(scope="module")
def collection():
    return get_collection()

@pytest.mark.parametrize("category", ["Animals", "Colors", "Shapes", "Numbers"])
def test_retrieve_returns_correct_category(collection, category):
    questions = retrieve_questions(collection, category, n=3)
    assert all(q["category"] == category for q in questions)

def test_retrieve_returns_requested_count(collection):
    questions = retrieve_questions(collection, "Animals", n=3)
    assert len(questions) == 3

def test_retrieve_question_has_required_keys(collection):
    questions = retrieve_questions(collection, "Colors", n=1)
    assert len(questions) == 1
    q = questions[0]
    assert {"id", "question", "answer", "category"} <= q.keys()

def test_retrieve_no_empty_fields(collection):
    questions = retrieve_questions(collection, "Shapes", n=4)
    for q in questions:
        assert q["question"].strip()
        assert q["answer"].strip()

def test_retrieve_respects_max_available(collection):
    # There are 8 docs per category; asking for more should not crash
    questions = retrieve_questions(collection, "Numbers", n=100)
    assert len(questions) <= 8
