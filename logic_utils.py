def get_num_questions() -> int:
    """Return the number of questions per trivia session."""
    return 5


def update_score(current_score: int, is_correct: bool) -> int:
    """Update score: +10 for correct, no change for incorrect."""
    if is_correct:
        return current_score + 10
    return current_score
