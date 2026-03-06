from otree.api import Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield instructions1
            yield instructions2
            yield TimeLimit
            yield Decode
            yield instructions3
            yield instructions4
            yield role_info

            for _ in range(5):
                yield ControlQuestions, {
                    'Q_task': random.choice(Constants.O_task),
                    'Q_payoff': random.choice(Constants.O_payoff_PA if self.player.id_in_group == 1 else Constants.O_payoff_PB),
                    'Q_payoff_other': random.choice(Constants.O_payoff_other_PA if self.player.id_in_group == 1 else Constants.O_payoff_other_PB),
                    'Q_independence': random.choice(Constants.O_independence),
                    'Q_secret_number_generation': random.choice(Constants.O_secret_number_generation),
                    'Q_no_knowledge_guess': random.choice(Constants.O_no_knowledge_guess),
                }

            yield TutorialIntro
            if self.player.id_in_group == 1:
                yield SenderTutorial, {'sender_choice': random.randint(1, 7)}
            else:
                if self.player.participant.treatment == "Decode":
                    yield ReceiverTutorial, {'receiver_guess': random.randint(1, 7), 'math_solution': random.randint(1, 100)}
                else:
                    yield ReceiverTutorial, {'receiver_guess': random.randint(1, 7)}

            yield start_page

        yield Submission(Round_number, check_html=False)

        if self.player.id_in_group == 1:
            yield SenderMessage, {'sender_choice': random.randint(1, 7)}


        else:
            if self.player.participant.treatment == "Decode":
                yield ReceiverGuess, {'receiver_guess': random.randint(1, 7), 'math_solution': random.randint(1, 100)}
            else:
                yield ReceiverGuess, {'receiver_guess': random.randint(1, 7)}

        yield Submission(Results, check_html=False)

        if self.player.round_number == Constants.num_rounds:
            yield HonestyGuess, {'honesty_guess': random.randint(1, 7)}
            yield FollowingGuess, {'credulity_guess': random.randint(1, 7)}


page_sequence = [
    instructions1, instructions2, TimeLimit, Decode, instructions3, instructions4,
    role_info,
    ControlQuestions, ControlQuestions, ControlQuestions, ControlQuestions, ControlQuestions,
    TutorialIntro, SenderTutorial, ReceiverTutorial, MyWaitPage, start_page,
    Round_number, SenderMessage, WaitForSender, ReceiverGuess, ResultsWaitPage, Results,
    MyWaitPage,
    HonestyGuess, FollowingGuess,
]

