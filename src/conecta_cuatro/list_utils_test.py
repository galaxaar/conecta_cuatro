from conecta_cuatro.list_utils import find_streak, transpose, displace_list


VICTORY_STREAK = 3

def test_streak_at_beginning():
    assert find_streak(["x", "x", "x", "o"], "x", VICTORY_STREAK) 

def test_streak_breaks():
    assert find_streak(["o", "x", "x", "o"], "x", VICTORY_STREAK) == False

def test_streak_at_the_end():
    assert find_streak(["o", "x", "x", "x"], "x", VICTORY_STREAK) 

def test_streak_in_middle():
    assert find_streak(["o", "x", "x", "x", "o"], "x", VICTORY_STREAK)

def test_streak_with_non_existent_needle():
    assert find_streak(["x", "x", "x", "o"], "o", VICTORY_STREAK) == False

def test_streak_with_mixed_elements():
    assert find_streak([1, "x", "x", "o"], 1, VICTORY_STREAK) == False

def test_streak_with_more_than3():
    assert find_streak(["x", "x", "x", "x"], "x", VICTORY_STREAK) 

def test_streak_resets():
    assert find_streak(["x", "x", "o", "x", "x", "x"], "x", VICTORY_STREAK) 

def test_victory_invalid_streak():
    assert find_streak(["x", "x", "x"], "x", 0) == False
    
def test_victory_negative_streak():
    assert find_streak(["x", "x", "x"], "x", -1) == False

def test_find_else():
    assert find_streak(["o", "x", "o", "o"], "x", 2) == False

def test_transpose():
    original =  [[0, 7, 3], [4, 0, 1]]
    transposed = [[0, 4],[7, 0], [3, 1]]

    assert transpose(original) == transposed
    assert transpose(transpose(original)) == original


