from logic_utils import check_guess, parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# Bug fix: check_guess hint messages were swapped — "Go HIGHER" shown when guess was too high (should be "Go LOWER")
def test_too_high_message_says_go_lower():
    # Guess is above the secret, so player should be told to go lower
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_message_says_go_higher():
    # Guess is below the secret, so player should be told to go higher
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# Bug fix: parse_guess was not checking if the number is within the valid range
def test_parse_guess_rejects_number_above_range():
    ok, value, err = parse_guess("101", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err

def test_parse_guess_rejects_number_below_range():
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err

def test_parse_guess_accepts_number_at_range_boundary():
    ok_low, value_low, _ = parse_guess("1", 1, 100)
    ok_high, value_high, _ = parse_guess("100", 1, 100)
    assert ok_low is True and value_low == 1
    assert ok_high is True and value_high == 100


# Bug fix: Hard difficulty had a smaller range (1-50) than Normal (1-100), making it easier
def test_hard_range_is_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high
