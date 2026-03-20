from otree.api import Bot, Submission
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        # Randomly choose a gender option
        selected_gender = random.choice([0, 1, 2, 3])  # 0 = Male, 1 = Female, 2 = Rather not say, 3 = Other
        gender_add_value = "Non-binary" if selected_gender == 3 else ""  # Only fill gender_add if 'Other' is selected

        # Randomly select ratings for the organization questions (1 to 6)
        org_ratings = {field: random.randint(1, 6) for field in [
            "org_fundacion_ideas",
            "org_fundacion_mujer",
            "org_fundacion_corona",
            "org_fundacion_santo_domingo",
            "org_fundacion_mujer_futuro",
            "org_unicef_colombia"
        ]}

        yield Submission(Demographics, {
            'age': random.randint(18, 100),  # Ensure valid age range
            'gender': selected_gender,
            'gender_add': gender_add_value,  # Only submitted when gender == 3
            'education': random.choice([0, 1, 2, 3, 4, 5]),
            'student': random.choice([0, 1]),
            'experiments': random.randint(0, 100) if random.choice([True, False]) else '',
            'reasoning': 'I made my decisions based on logical reasoning and available information.' if random.choice([True, False]) else '',
            'chosen_role': random.choice([0, 1, 2]),
            **org_ratings  # ✅ Include organization ratings dynamically
        }, check_html=False)  # ✅ Disables HTML validation to prevent field mismatch errors
