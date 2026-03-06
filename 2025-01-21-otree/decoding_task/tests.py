from otree.api import Currency as c, currency_range, expect, Bot
from . import *

# Bot
class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1:
            yield DecodingInstructions
            yield DecodingStart

            # Load task data
            df_decoding_tasks = pd.read_csv('_static/data/encoding_task.csv')
            tasks = df_decoding_tasks.to_dict(orient='records')

            # Iterate through tasks, simulating correct answers
            for task in tasks[:Constants.NUM_TASKS]:  # Ensure only NUM_TASKS are attempted
                correct_answer = task['answer']  # Assuming 'answer' column exists in CSV
                yield Submission(DecodingTask, {'decoding_answer': correct_answer})


            # Final results page
            yield DecodingTaskResults

