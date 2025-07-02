import random
from Lunch_Decision_Algorithm import Meal, greedy, bandit, update_meal

# Test 1: Variety penalty should decrease over time
def test_variety_penalty_decreases():
    meal = Meal("Test Meal", cost=5, nutrition=8, craving_score=7)
    meal.last_eaten_day = 10

    penalty_day_11 = meal.variety_penalty(11)  # 1 day since eaten -> high penalty
    penalty_day_15 = meal.variety_penalty(15)  # 5 days since eaten -> no penalty

    assert penalty_day_15 < penalty_day_11, "Variety penalty did not decrease over time"
    print("test_variety_penalty_decreases passed")

# Test 2: Greedy should pick the best scoring meal
def test_greedy_selection():
    meals = [
        Meal("Low Crave", cost=5, nutrition=5, craving_score=2),
        Meal("High Crave", cost=5, nutrition=5, craving_score=9)
    ]
    weights = {'crave': 1.0, 'nutrition': 1.0, 'cost': 1.0, 'variety': 1.0}
    day = 1

    best = greedy(meals, day, weights)
    assert best.name == "High Crave", "Greedy did not pick the highest scoring meal"
    print("test_greedy_selection passed")

# Test 3: Bandit sometimes explores
def test_bandit_exploration():
    meals = [
        Meal("A", cost=5, nutrition=5, craving_score=1),
        Meal("B", cost=5, nutrition=5, craving_score=9)
    ]
    weights = {'crave': 1.0, 'nutrition': 1.0, 'cost': 1.0, 'variety': 1.0}
    day = 1

    explored = False
    for _ in range(100):  # Run enough times to hit exploration
        picked = bandit(meals, day, weights, epsilon=0.5)
        if picked.name == "A":
            explored = True
            break

    assert explored, "Bandit did not explore"
    print("test_bandit_exploration passed")

# Run all tests
if __name__ == "__main__":
    test_variety_penalty_decreases()
    test_greedy_selection()
    test_bandit_exploration()
