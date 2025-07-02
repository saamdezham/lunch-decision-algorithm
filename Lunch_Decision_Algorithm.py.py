# Lunch Decision Algorithm
import random
import copy

# Define a Meal class to store meal information and scoring behavior
class Meal:
    def __init__(self, name, cost, nutrition, craving_score):
        self.name = name  # Meal name
        self.cost = cost  # Cost of the meal
        self.nutrition = nutrition  # Nutrition score (higher is better)
        self.craving_score = craving_score  # How much the user craves it (1-10)
        self.last_eaten_day = -10  # Track last time this meal was eaten (initially far in the past)
        self.total_reward = 0  # Cumulative satisfaction score from feedback
        self.times_chosen = 0  # How many times the meal has been selected

    # Compute a penalty for eating the same meal too recently
    def variety_penalty(self, current_day):
        days_since = current_day - self.last_eaten_day
        return max(0, 5 - days_since)  # Penalize meals eaten in the past 5 days

    # Compute a weighted score for the meal based on craving, nutrition, cost, and variety
    #Linear utility function - combine multiple features that influence the decision
    def score(self, current_day, weights):
        penalty = self.variety_penalty(current_day)
        return (weights['crave'] * self.craving_score + #add craving and nutrition (positives)
                weights['nutrition'] * self.nutrition -
                weights['cost'] * self.cost - #sub cost and penalty (negatives)
                weights['variety'] * penalty)

# Greedy selection: choose the meal with the highest score today
# Short sighted: never tries a meal that scored poorly previously 
# Can get stuck picking the same meal since it slightly beats others

def greedy(meals, current_day, weights):
    best_score = float('-inf')
    selected = None
    for meal in meals:
        s = meal.score(current_day, weights)
        if s > best_score:
            best_score = s
            selected = meal
    return selected

# Epsilon-Greedy Bandit version: 
# Picks a random meal at a set probability. Otherwise, pick greedy best
# Helps try new meals that might turn out better long term 
# Models choosing between uncertain options

def bandit(meals, current_day, weights, epsilon):
    if random.random() < epsilon:
        return random.choice(meals)  # Explore: pick a random meal
    return greedy(meals, current_day, weights)  # Exploit: pick best based on score

# After choosing a meal, update its stats based on feedback
# meals evolve over time 
def update_meal(meal, feedback_score, current_day):
    meal.total_reward += feedback_score  # total satisfaction score the meal received: tracks how well liked
    #the meal is over time 
    meal.times_chosen += 1  # update how many times the meal has been eaten - selection frequency
    meal.last_eaten_day = current_day  # today is last eaten day
    # adapt craving score based on how much the user liked it - adaptive behavior 
    meal.craving_score = max(1, min(10, meal.craving_score + (feedback_score - 5) * 0.1))
    #if craving score is positive then it increases and vice versa

# Define example meal options
meals = [
    Meal("Turkey Sandwich", 7.5, 8, 7),
    Meal("Veggie Bowl", 6.0, 9, 5),
    Meal("Pizza Slice", 5.5, 4, 9),
    Meal("Tofu Stir Fry", 8.0, 10, 6),
    Meal("Burger", 9.0, 6, 8),
    Meal("PB&J Sandwich", 3, 4, 5),
    Meal("Steak Filet", 12, 10, 7)
    
]

# Define weight values to prioritize different aspects in the scoring function
# Ensure no single factor dominates unless the user wants it to 
weights = {
    'crave': 1.0,       # baseline craving importance
    'nutrition': 1.2,   # slightly more health aware
    'cost': 0.8,        # cost is less important (for this user) than craving and nutrition
    'variety': 1.5      # enourage a more diverse lunch routine
}

# Run Greedy Simulation
print("\n--- Greedy Simulation ---")
greedy_meals = copy.deepcopy(meals)  # ensure isolated state

#track total score and daily decisions
greedy_total_score = 0
greedy_daily_log = []

#Simulate 30 days of greedy lunch decisions
for day in range(1, 31):
    meal = greedy(greedy_meals, day, weights)  # Pick best meal today
    feedback = random.randint(3, 10)  # Simulate user satisfaction 3-10
    update_meal(meal, feedback, day)  # Update internal state of the meal
    greedy_total_score += feedback  # Track total satisfaction across the 30 days
    greedy_daily_log.append((day, meal.name, feedback))  # Log the decision

# Print Greedy simulation results
for day, name, feedback in greedy_daily_log:
    print(f"Day {day:2d}: {name:20} | Feedback: {feedback}")

# Run Bandit Simulation
print("\n--- Bandit Simulation ---")
bandit_meals = copy.deepcopy(meals) 

bandit_total_score = 0
bandit_daily_log = []

for day in range(1, 31):
    meal = bandit(bandit_meals, day, weights, epsilon=0.3)  # 30% explore chance - epsilon
    feedback = random.randint(4, 10)  
    update_meal(meal, feedback, day) 
    bandit_total_score += feedback  
    bandit_daily_log.append((day, meal.name, feedback))  

for day, name, feedback in bandit_daily_log:
    print(f"Day {day:2d}: {name:20} | Feedback: {feedback}")

print("\nSummary:")
print(f"Total Greedy Satisfaction Score: {greedy_total_score}")
print(f"Total Bandit Satisfaction Score: {bandit_total_score}")
