Lunch Decision Algorithm

This project implements a decision support system to reduce daily lunch decision fatigue. It simulates how a person might choose meals over time using two algorithms: a Greedy strategy and an Epsilon-Greedy Bandit approach.

The algorithm takes into account:
- User cravings
- Nutrition value
- Cost
- Meal variety (to avoid repeats)

It updates meal preferences over time using user feedback and compares both strategies over a 30-day simulation.

---

##Files

- `lunch_picker.py` — Core algorithm and simulation logic
- `README.md` — This file

---

##How to Run

Make sure you have Python 3 installed. Then run:

```bash
python lunch_picker.py
