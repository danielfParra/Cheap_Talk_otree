from otree.api import *
import math
import random
import json


class Constants(BaseConstants):
    name_in_url = 'N5_sender_receiver_game'
    players_per_group = 2
    num_rounds = 4
    BONUS_AMOUNT = Currency(4000)
    PIECE_RATE_DECODE = Currency(500)  # New constant for the piece rate per correct answer
    HONESTY_GUESS_BONUS = Currency(1000)  # Bonus for honesty guess
    CREDULITY_GUESS_BONUS = Currency(1000)  # Bonus for credulity guess
    SENDER_ROLE = 'Player A'
    RECEIVER_ROLE = 'Player B'
    TIME_PER_ROUND = 20
    FEEDBACK_TIME = 5
    ATTEMPT_DELAY = 5

    # Variables for matching with pools
    POOL_SIZE = 5  # Each pool has 5 players
    TOTAL_PLAYERS = 20

    TIME_PER_TASK = 20  # Time limit for each decoding task (in seconds)
    NUM_TASKS = 6  # Number of tasks in the decoding phase


    # Predefined lists of payoff-relevant rounds for senders and receivers
    # These vectors should be 12 rounds out of the total 24, for each role

    # Sender's payoff-relevant rounds
    PREDEFINED_SENDER_ROUNDS = [2, 5, 7, 9, 11, 13, 15, 16, 18, 19, 20, 23]

    # Receiver's payoff-relevant rounds
    PREDEFINED_RECEIVER_ROUNDS = [1, 3, 4, 6, 8, 10, 12, 14, 17, 21, 22, 24]

    # Load csv with encoded messages
    import pandas as pd
    file = '_static/data/encoded_messages.csv'
    df_encodings = pd.read_csv(file)

    # Load csv with decoding tasks (answer and encoding)
    import pandas as pd
    file = '_static/data/encoding_task.csv'
    df_decoding_tasks = pd.read_csv(file)

    # Control questions.
    Q_who_knows = '¿Quién conoce el número secreto?'
    O_who_knows = ['Jugador A', 'Jugador B', 'Ambos', 'Ninguno']
    A_who_knows = 'Ninguno'
    H_who_knows = 'Considere cómo se determina el número secreto. Si nadie ha recibido información sobre él, ¿cómo podría alguien conocerlo?'

    Q_task = '¿Cuál es tu tarea en este juego?'
    O_task = ['Adivinar el número secreto', 'Escribir un texto', 'Enviar un mensaje']
    A_task_PA = 'Enviar un mensaje'
    A_task_PB = 'Adivinar el número secreto'
    H_task = 'Piensa en qué acción se te requiere realizar durante el juego. Tu rol determina tu tarea principal.'

    Q_payoff_PB = '¿Cómo maximizan su pago los jugadores en tu rol (Jugador B)?'
    O_payoff_PB = ['Adivinando el número secreto lo más precisamente posible',
                   'Adivinando un número lo más cercano posible al mensaje', 'Siempre adivinando bajo',
                   'Siempre adivinando alto']
    A_payoff_PB = 'Adivinando el número secreto lo más precisamente posible'
    H_payoff_PB = 'Tu objetivo es acercarte lo más posible al número secreto real. Cuanto más precisa sea tu adivinanza, mejor será tu pago.'

    Q_payoff_PA = '¿Cómo maximizan su pago los jugadores en tu rol (Jugador A)?'
    O_payoff_PA = ['Haciendo que el Jugador B adivine el número secreto',
                   'Haciendo que el Jugador B adivine lo más alto posible',
                   'Haciendo que el Jugador B adivine cerca del número enviado']
    A_payoff_PA = 'Haciendo que el Jugador B adivine lo más alto posible'
    H_payoff_PA = 'Tu pago depende de influir en la adivinanza del Jugador B. Piensa exactamente por qué depende de la adivinanza.'

    Q_payoff_other_PA = '¿Cómo maximizan su pago los jugadores en el otro rol (Jugador B)?'
    O_payoff_other_PA = ['Adivinando el número secreto lo más precisamente posible',
                         'Adivinando un número lo más cercano posible al mensaje', 'Siempre adivinando bajo',
                         'Siempre adivinando alto']
    A_payoff_other_PA = 'Adivinando el número secreto lo más precisamente posible'
    H_payoff_other_PA = 'Considera el objetivo del otro jugador. Su mejor estrategia está alineada con identificar el número secreto real, no solo responder al mensaje en sí.'

    Q_payoff_other_PB = '¿Cómo maximizan su pago los jugadores en el otro rol (Jugador A)?'
    O_payoff_other_PB = ['Haciendo que adivines el número secreto', 'Haciendo que adivines lo más alto posible',
                         'Haciendo que adivines cerca del número enviado']
    A_payoff_other_PB = 'Haciendo que adivines lo más alto posible'
    H_payoff_other_PB = 'El pago del otro jugador depende de influir en tu adivinanza. Piensa exactamente por qué depende de la adivinanza.'

    Q_independence = 'Considera el siguiente escenario:'
    Q_independence_text = 'Estás en la ronda 3 del juego. En las rondas 1 y 2, el número secreto fue 5. ¿Cuál de las siguientes afirmaciones sobre el número secreto en la ronda 3 es verdadera?'
    O_independence = ['Es probable que sea mayor que 5, ya que el número secreto fue 5 en las rondas anteriores',
                      'Es probable que sea menor que 5, ya que el número secreto fue 5 en las rondas anteriores',
                      'Es probable que sea 5, ya que el número secreto fue 5 en las rondas anteriores',
                      'Cualquier número es igualmente probable, independientemente de las rondas anteriores']
    A_independence = 'Cualquier número es igualmente probable, independientemente de las rondas anteriores'
    H_independence = 'Piensa en cómo se eligen los números: ¿el proceso recuerda valores pasados?'

    Q_secret_number_generation = '¿Cómo se genera el número secreto?'
    O_secret_number_generation = ['Lo elige el Jugador A', 'Lo elige el Jugador B',
                                  'Lo genera aleatoriamente el computador']
    A_secret_number_generation = 'Lo genera aleatoriamente el computador'
    H_secret_number_generation = 'El número secreto se determina de una manera que ni el Jugador A ni el Jugador B tienen control directo sobre él. Piensa de dónde podría venir el número si ningún jugador es responsable de elegirlo.'

    Q_no_knowledge_guess = 'Adivinanza sin información:'
    Q_no_knowledge_guess_text = 'Supón que no tienes información sobre el número secreto. ¿Cuál es la mejor estrategia para estar más cerca al real?'
    O_no_knowledge_guess = ['Adivinar un número aleatorio', 'Adivinar 7 (el número más alto)',
                            'Adivinar 1 (el número más bajo)', 'Adivinar 4 (el promedio de todos los números posibles)']
    A_no_knowledge_guess = 'Adivinar 4 (el promedio de todos los números posibles)'
    H_no_knowledge_guess = 'Si no tienes información, tu mejor adivinanza debería minimizar el error potencial en todas las posibilidades. Considera qué elección equilibra el riesgo de adivinar demasiado alto o demasiado bajo.'

    wrong_answer_message = 'No respondiste correctamente a esta pregunta. La siguiente pista puede ayudarte cuando intentes responder de nuevo:'
    correct_answer_message = 'Respondiste correctamente a esta pregunta. No necesitas cambiarla.'

    # Templates
    ReceiverReminder = 'N5_sender_receiver_game/templates/ReceiverReminder.html'
    SenderReminder = 'N5_sender_receiver_game/templates/SenderReminder.html'

class Subsession(BaseSubsession):
    def creating_session(self):
        # Assign payoff-relevant rounds
        for p in self.session.get_participants():
            if p.vars['role'] == Constants.SENDER_ROLE:
                p.vars['payoff_relevant_rounds'] = Constants.PREDEFINED_SENDER_ROUNDS
            elif p.vars['role'] == Constants.RECEIVER_ROLE:
                p.vars['payoff_relevant_rounds'] = Constants.PREDEFINED_RECEIVER_ROUNDS


class Group(BaseGroup):

    secret_number = models.IntegerField()
    sender_choice = models.IntegerField()
    sender_message = models.IntegerField()
    sender_message_encoded = models.StringField()
    receiver_guess = models.FloatField(min=0, max=7)
    tutorial_message = models.IntegerField()
    tutorial_message_encoded = models.StringField()
    math_solution = models.IntegerField(label=None)

    # to store win probabilities and win status
    sender_win_prob = models.FloatField()
    receiver_win_prob = models.FloatField()
    sender_wins = models.BooleanField()
    receiver_wins = models.BooleanField()

    # Incentivize guesses
    honesty_rate = models.FloatField()
    credulity_rate = models.FloatField()

    # Store the guess confirmation status
    # This field is used to check if the guess was confirmed by the user
    guess_confirmed = models.BooleanField(initial=False)


class Player(BasePlayer):
    pool = models.IntegerField()
    decoding_answer = models.IntegerField(blank=True)  # Stores the answer for each task
    task_number = models.IntegerField(initial=1)  # Tracks the current task (1 to 10)
    correct_answers = models.IntegerField(initial=0)  # Tracks how many correct answers the player has given
    receiver_type = models.StringField()  # Store 'decode' or 'direct'


    # Control question fields
    wrong_answer = models.IntegerField(initial = 1)
    wrong_answer_count = models.IntegerField(initial = 0)
    Q_task = models.StringField(label = Constants.Q_task, initial = 'na')
    Q_task_count = models.IntegerField(initial = 0)

    Q_payoff = models.StringField(initial = 'na')
    Q_payoff_count = models.IntegerField(initial = 0)
    Q_payoff_other = models.StringField(initial = 'na')
    Q_payoff_other_count = models.IntegerField(initial = 0)
    Q_independence = models.StringField(label = Constants.Q_independence, initial = 'na')
    Q_independence_count = models.IntegerField(initial = 0)
    Q_secret_number_generation = models.StringField(label = Constants.Q_secret_number_generation, initial = 'na')
    Q_secret_number_generation_count = models.IntegerField(initial = 0)
    Q_no_knowledge_guess = models.StringField(label = Constants.Q_no_knowledge_guess, initial = 'na')
    Q_no_knowledge_guess_count = models.IntegerField(initial = 0)


    is_sender_payoff_relevant = models.BooleanField(initial=False)
    is_receiver_payoff_relevant = models.BooleanField(initial=False)

    honesty_guess = models.IntegerField()
    credulity_guess = models.IntegerField()


# These functions assign choice options to questions and display them in a random order.
def Q_task_choices(player):
    L = Constants.O_task.copy()
    random.shuffle(L)
    return L

def Q_payoff_choices(player):
    if player.role == 'Player A':
        L = Constants.O_payoff_PA.copy()
    else:
        L = Constants.O_payoff_PB.copy()
    random.shuffle(L)
    return L

def Q_payoff_other_choices(player):
    if player.role == 'Player A':
        L = Constants.O_payoff_other_PA.copy()
    else:
        L = Constants.O_payoff_other_PB.copy()
    random.shuffle(L)
    return L

def Q_independence_choices(player):
    L = Constants.O_independence.copy()
    random.shuffle(L)
    return L

def Q_secret_number_generation_choices(player):
    L = Constants.O_secret_number_generation.copy()
    random.shuffle(L)
    return L

def Q_no_knowledge_guess_choices(player):
    L = Constants.O_no_knowledge_guess.copy()
    random.shuffle(L)
    return L

def check_cq_answers(answer, solution, count):
    if answer != solution:
        return 1, count + 1
    else:
        return 0, count


def set_payoffs(group: Group):
    # Get the sender and receiver players
    sender = group.get_player_by_id(1)
    receiver = group.get_player_by_id(2)

    # Apply the decoding bonus **only in the first round**
    if sender.round_number == 1:
        sender.payoff = sender.correct_answers * Constants.PIECE_RATE_DECODE
        receiver.payoff = receiver.correct_answers * Constants.PIECE_RATE_DECODE

    # --- Sender-Receiver Game Payoff Computation ---

    # Calculate the sender's probability based on the receiver's guess
    if group.receiver_guess == 0 and group.sender_message > 0:
        sender_prob = (group.sender_message - 1) / 6
    elif group.sender_message == 0:
        sender_prob = 0
    else:
        sender_prob = (group.receiver_guess - 1) / 6

    # Calculate the receiver's probability based on the given quadratic formula
    if group.receiver_guess == 0 and group.sender_message > 0:
        receiver_prob = 1 - (1 / 36) * (group.secret_number - group.sender_message) ** 2
    elif group.sender_message == 0:
        receiver_prob = 0
    else:
        receiver_prob = 1 - (1 / 36) * (group.secret_number - group.receiver_guess) ** 2

    # Determine if players win the bonus using a binomial draw
    sender_wins = random.random() < sender_prob  # Random trial for sender's win probability
    receiver_wins = random.random() < receiver_prob  # Random trial for receiver's win probability

    # Store win probabilities and win status in the Group model
    group.sender_win_prob = sender_prob
    group.receiver_win_prob = receiver_prob
    group.sender_wins = sender_wins
    group.receiver_wins = receiver_wins

    # Apply special conditions for sender and receiver payoffs
    if group.sender_message == 0:
        sender.payoff += Currency(0)
    elif group.receiver_guess == 0:
        receiver.payoff += Currency(0)
        sender.payoff += Constants.BONUS_AMOUNT if group.sender_message > 0 else Currency(0)
    else:
        # Set payoffs based on win probabilities without considering payoff relevance
        sender.payoff += Constants.BONUS_AMOUNT if sender_wins else Currency(0)
        receiver.payoff += Constants.BONUS_AMOUNT if receiver_wins else Currency(0)

    print(f"Round {sender.round_number}:")
    print(f"  - Secret number: {group.secret_number}")
    print(f"  - Sender's message: {group.sender_message}")
    print(f"  - Receiver's guess: {group.receiver_guess}")
    print(f"  - Sender probability: {sender_prob}, Receiver probability: {receiver_prob}")
    print(f"  - Sender wins: {sender_wins}, Receiver wins: {receiver_wins}")
    print(f"  - Sender payoff: {sender.payoff}, Receiver payoff: {receiver.payoff}")


# pages.py

class MatchingWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        players = subsession.get_players()
        num_players = len(players)

     # ✅ If n=2, let oTree handle matching (skip pools)
        if num_players == 2:
            print("\n--- n=2: oTree will automatically match players ---")
            return

            # ✅ Otherwise, proceed with pool-based matching
            # ✅ Extract unique pools and divide into A-pools and B-pools

        all_pools = sorted(set(p.participant.vars['pool'] for p in players))
        num_A_pools = len(all_pools) // 2  # Half of the pools are for A, half for B
        A_pools = all_pools[:num_A_pools]  # First half are A pools
        B_pools = all_pools[num_A_pools:]  # Second half are B pools

        # ✅ Create dictionaries mapping pools to players
        pool_dict_A = {pool: [p for p in players if p.participant.vars['pool'] == pool] for pool in A_pools}
        pool_dict_B = {pool: [p for p in players if p.participant.vars['pool'] == pool] for pool in B_pools}

        # ✅ Keep fixed pool pairings
        pool_pairs = list(zip(A_pools, B_pools))  # [(1,3), (2,4), ...]

        # ✅ Shuffle players within each pool for new pairings every round
        for pool in pool_dict_A.values():
            random.shuffle(pool)  # Shuffle players in A-pools
        for pool in pool_dict_B.values():
            random.shuffle(pool)  # Shuffle players in B-pools

        # ✅ Create new group matrix by pairing shuffled players from fixed pools
        group_matrix = []
        for pool_A, pool_B in pool_pairs:
            while pool_dict_A[pool_A] and pool_dict_B[pool_B]:  # While both pools have players
                player_A = pool_dict_A[pool_A].pop()
                player_B = pool_dict_B[pool_B].pop()
                group_matrix.append([player_A.id_in_subsession, player_B.id_in_subsession])

        # ✅ Assign groups
        subsession.set_group_matrix(group_matrix)

        # ✅ Create a dictionary mapping player ID to player object
        players_by_id = {p.id_in_subsession: p for p in players}

        print(f'\n--- Round {subsession.round_number} Group Matching ---')
        for group in group_matrix:
            p1 = players_by_id[group[0]]
            p2 = players_by_id[group[1]]
            print(
                f"Group: {group} -> "
                f"Player {p1.id_in_subsession} (Pool {p1.participant.vars['pool']}) "
                f"paired with "
                f"Player {p2.id_in_subsession} (Pool {p2.participant.vars['pool']})"
            )

class instructions1(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.pool = player.participant.vars.get('pool', None)  # ✅ Store pool in Player table
        if player.participant.vars['role'] == Constants.RECEIVER_ROLE:
            player.receiver_type = player.participant.vars.get('receiver_type', 'unknown')

class instructions2(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

class TimeLimit(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}


class instructions3(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

class instructions4(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}
    
class Decode(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.treatment == "Decode"

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}


class Round_number(Page):
    timeout_seconds = 3
    timer_text = 'La siguiente ronda comienza en:'


class role_info(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}

class ControlQuestions(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.wrong_answer > 0
    
    form_model = 'player'
    form_fields = ['Q_task', 'Q_payoff', 'Q_payoff_other', 'Q_independence', 'Q_no_knowledge_guess', 'Q_secret_number_generation']

    @staticmethod
    def before_next_page(player,timeout_happened):
        player.wrong_answer = 0
        if player.participant.role == 'Player A':
            a, player.Q_task_count = check_cq_answers(player.Q_task, Constants.A_task_PA, player.Q_task_count)
            b, player.Q_payoff_count = check_cq_answers(player.Q_payoff, Constants.A_payoff_PA, player.Q_payoff_count)
            c, player.Q_payoff_other_count = check_cq_answers(player.Q_payoff_other, Constants.A_payoff_other_PA, player.Q_payoff_other_count)
        else:
            a, player.Q_task_count = check_cq_answers(player.Q_task, Constants.A_task_PB, player.Q_task_count)
            b, player.Q_payoff_count = check_cq_answers(player.Q_payoff, Constants.A_payoff_PB, player.Q_payoff_count)
            c, player.Q_payoff_other_count = check_cq_answers(player.Q_payoff_other, Constants.A_payoff_other_PB, player.Q_payoff_other_count)
        d, player.Q_independence_count = check_cq_answers(player.Q_independence, Constants.A_independence, player.Q_independence_count)
        e, player.Q_no_knowledge_guess_count = check_cq_answers(player.Q_no_knowledge_guess, Constants.A_no_knowledge_guess, player.Q_no_knowledge_guess_count)
        f, player.Q_secret_number_generation_count = check_cq_answers(player.Q_secret_number_generation, Constants.A_secret_number_generation, player.Q_secret_number_generation_count)


        player.wrong_answer = max(a,b,c,d,e,f)
        player.wrong_answer_count += player.wrong_answer


class start_page(Page):
    # Only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    
    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}
    
class SenderTutorial(Page):
    form_model = 'group'
    form_fields = ['sender_choice']

    @staticmethod
    def is_displayed(player: Player):
        # Nur für Player A in der ersten Runde
        return player.id_in_group == 1 and player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        current_round = player.round_number
        is_receiver_payoff_relevant = current_round in Constants.PREDEFINED_RECEIVER_ROUNDS
        return dict(
            is_receiver_payoff_relevant=is_receiver_payoff_relevant
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Dummy-Wert setzen, um keine Auswirkungen auf spätere Berechnungen zu haben
        player.group.sender_message = None


class SenderMessage(Page):
    form_model = 'group'
    form_fields = ['sender_choice']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    timeout_seconds = Constants.TIME_PER_ROUND
    timer_text = '⏳ Tiempo restante:'

    @staticmethod
    def vars_for_template(player: Player):
        current_round = player.round_number
        is_receiver_payoff_relevant = current_round in Constants.PREDEFINED_RECEIVER_ROUNDS
        return dict(
            is_receiver_payoff_relevant=is_receiver_payoff_relevant
        )


    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.group.sender_message = 0

        # Generate a new secret number for each round (whether timeout happens or not)
        player.group.secret_number = random.randint(1, 7)

        group = player.group
        current_round = player.round_number

        # Handle timeout: set sender_message to 0 if timeout happens
        if timeout_happened:
            group.sender_message = 0

        # Generate a new secret number for each round
        group.secret_number = random.randint(1, 7)

        # Set message 
        if group.sender_choice == 8:
            group.sender_message = group.secret_number
        else:
            group.sender_message = group.sender_choice

        # Encode message 
        print('here')
        print(group.sender_message)
        if group.sender_message == 0:
            group.sender_message_encoded = 'El Jugador A no envió un número'
        else:
            # Get player B in the group
            playerB = group.get_player_by_role(Constants.RECEIVER_ROLE)
            if playerB.participant.receiver_type == "decode":
            #if player.participant.receiver_type == "decode":
                df_temp = Constants.df_encodings[Constants.df_encodings['number'] == group.sender_message].sample(1)
                player.group.sender_message_encoded = df_temp['encoding'].values[0]
            else:
                player.group.sender_message_encoded = str(group.sender_message)

        # Determine if the current round is payoff-relevant for sender and receiver
        player.is_sender_payoff_relevant = current_round in Constants.PREDEFINED_SENDER_ROUNDS
        player.is_receiver_payoff_relevant = current_round in Constants.PREDEFINED_RECEIVER_ROUNDS

class WaitForSender(WaitPage):
    template_name = 'N5_sender_receiver_game/ReceiverWaitPage.html'

    def is_displayed(player: Player):
        return player.role == Constants.RECEIVER_ROLE

class TutorialIntro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        return {"round_number": player.round_number}
    
    @staticmethod
    def before_next_page(player: Group, timeout_happened):
        tutorial_message = random.randint(1, 7)
        player.group.tutorial_message = tutorial_message
        if player.participant.receiver_type == "decode":
            df_temp = Constants.df_encodings[Constants.df_encodings['number'] == tutorial_message].sample(1)
            player.group.tutorial_message_encoded = df_temp['encoding'].values[0]
        else:
            player.group.tutorial_message_encoded = str(tutorial_message)

class ReceiverTutorial(Page):
    form_model = 'group'
    @staticmethod
    def get_form_fields(player: Player):
        if player.participant.receiver_type == "decode":
            return ['receiver_guess', 'math_solution']
        else:
            return ['receiver_guess']
    
    @staticmethod
    def is_displayed(player: Player):
        # Nur für Player B in der ersten Runde
        return player.id_in_group == 2 and player.round_number == 1
    

    @staticmethod
    def vars_for_template(player: Player):
        current_round = player.round_number
        is_sender_payoff_relevant = current_round in Constants.PREDEFINED_SENDER_ROUNDS
        return dict(
            is_sender_payoff_relevant=is_sender_payoff_relevant
        )

    @staticmethod
    def js_vars(player: Player):
        sender_message = player.group.tutorial_message
        return dict(
            encoded_message=player.group.tutorial_message_encoded,
            sender_message=sender_message,
            treatment=player.participant.treatment,
            receiver_type=player.participant.receiver_type,
            max_guess=7,  # Maximum allowed guess
            min_guess=1  # Minimum allowed guess
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Dummy-Wert setzen, um keine Auswirkungen auf spätere Berechnungen zu haben
        player.group.receiver_guess = None
        if player.participant.receiver_type == "decode":
            player.group.math_solution = None


class ReceiverGuess(Page):
    form_model = 'group'
    @staticmethod
    def get_form_fields(player: Player):
        if player.participant.receiver_type == "decode":
            return ['receiver_guess', 'math_solution', 'guess_confirmed']
        else:
            return ['receiver_guess', 'guess_confirmed']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    timeout_seconds = Constants.TIME_PER_ROUND
    timer_text = '⏳ Tiempo restante:'

    @staticmethod
    def vars_for_template(player: Player):
        # Obtener el mensaje del sender
        sender_message = player.group.sender_message

        # Verificar si la ronda es payoff-relevant para el Sender (Participante A)
        current_round = player.round_number
        is_sender_payoff_relevant = current_round in Constants.PREDEFINED_SENDER_ROUNDS

        return dict(
            sender_message=sender_message,  # Pasar el mensaje del sender
            is_sender_payoff_relevant=is_sender_payoff_relevant  # Pasar si la ronda es payoff-relevant para el Sender
        )
    @staticmethod
    def js_vars(player: Player):
        return dict(
            sender_message = player.group.sender_message,
            encoded_message=player.group.sender_message_encoded,
            treatment=player.participant.treatment,
            receiver_type=player.participant.receiver_type,
            max_guess=7,  # Maximum allowed guess
            min_guess=1  # Minimum allowed guess
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        # Only set receiver_guess to 0 if timeout happens
        if timeout_happened and not player.group.guess_confirmed:
            player.group.receiver_guess = 0

        current_round = player.round_number

        # Determine if the current round is payoff-relevant for sender and receiver
        player.is_sender_payoff_relevant = current_round in Constants.PREDEFINED_SENDER_ROUNDS
        player.is_receiver_payoff_relevant = current_round in Constants.PREDEFINED_RECEIVER_ROUNDS


class ResultsWaitPage(WaitPage):
    template_name = 'N5_sender_receiver_game/SenderWaitPage.html'
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(self):
        # Get the sender and receiver players
        sender = self.group.get_player_by_id(1)
        receiver = self.group.get_player_by_id(2)

        return {
            'secret_number': self.group.secret_number,
            'sender_message': self.group.sender_message,
            'receiver_guess': self.group.receiver_guess,
            'player_payoff': self.payoff,  # Player's total earnings this round
            'correct_answers': self.correct_answers,  # Player's correct answers
            'extra_earnings': self.correct_answers * Constants.PIECE_RATE_DECODE,  # Extra earnings from decoding
            'piece_rate_decode': Constants.PIECE_RATE_DECODE,  # Rate per correct answer
        }

    timeout_seconds = Constants.FEEDBACK_TIME
    timer_text = '⏳ Tiempo restante:'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        current_round = player.round_number
        sender = player.group.get_player_by_id(1)
        receiver = player.group.get_player_by_id(2)

        # Check if this round is payoff-relevant for the sender and receiver
        is_sender_payoff_relevant = current_round in Constants.PREDEFINED_SENDER_ROUNDS
        is_receiver_payoff_relevant = current_round in Constants.PREDEFINED_RECEIVER_ROUNDS

        # If the round is NOT payoff-relevant, we subtract that round's payout from the cumulative total.
        if not is_sender_payoff_relevant:
            sender.payoff = 0 # Subtract payment if not relevant
        if not is_receiver_payoff_relevant:
            receiver.payoff = 0 # Subtract payment if not relevant

    # Instead of setting to 0, we SUBTRACT only the sender-receiver game earnings
        if not is_sender_payoff_relevant:
            sender.payoff -= Constants.BONUS_AMOUNT if sender.group.sender_wins else Currency(0)
        if not is_receiver_payoff_relevant:
            receiver.payoff -= Constants.BONUS_AMOUNT if receiver.group.receiver_wins else Currency(0)

        # Ensure that payoff never goes below the decoding bonus
        sender.payoff = max(sender.payoff, sender.correct_answers * Constants.PIECE_RATE_DECODE)
        receiver.payoff = max(receiver.payoff, receiver.correct_answers * Constants.PIECE_RATE_DECODE)

        player.pool = player.participant.vars.get('pool', None)  # ✅ Store pool in Player table
        if player.participant.vars['role'] == Constants.RECEIVER_ROLE:
            player.receiver_type = player.participant.vars.get('receiver_type', 'unknown')

        print(f"Round {current_round}: Sender Payoff = {sender.payoff}, Receiver Payoff = {receiver.payoff}")
        print(f"Total Sender Payoff (Cumulative): {sender.participant.payoff}")
        print(f"Total Receiver Payoff (Cumulative): {receiver.participant.payoff}")

class HonestyGuess(Page):
    form_model = 'player'
    form_fields = ['honesty_guess']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment != "Babbling"

class FollowingGuess(Page):
    form_model = 'player'
    form_fields = ['credulity_guess']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def before_next_page(player, timeout_happened):

        # Calculate the honesty and credulity rates. 
        msg = 0 
        hnum = 0
        cnum = 0
        hmsg = 0
        for p in player.subsession.get_players():
            hrate_p = 0
            if p.role == Constants.SENDER_ROLE:
                for r in range(1, Constants.num_rounds + 1):
                    msg += 1
                    if p.in_round(r).group.sender_choice == 8:
                        hnum += 1
            else:
                for r in range(1, Constants.num_rounds + 1):
                    sender_message = p.in_round(r).group.sender_message
                    if sender_message == 7:
                        hmsg += 1
                        if p.in_round(r).group.receiver_guess >= 6.8:
                            cnum += 1

        player.group.honesty_rate = hnum / msg if msg > 0 else 0
        player.group.credulity_rate = cnum / hmsg if hmsg > 0 else 0

        if player.participant.treatment != "Babbling":
            honesty_guess_prob = 1 - (player.group.honesty_rate - player.honesty_guess/100) ** 2
            wins = random.random() < honesty_guess_prob
            player.payoff += Constants.HONESTY_GUESS_BONUS if wins else Currency(0)

        credulity_guess_prob = 1 - (player.group.credulity_rate - player.credulity_guess/100) ** 2
        wins = random.random() < credulity_guess_prob
        player.payoff += Constants.CREDULITY_GUESS_BONUS if wins else Currency(0)

class MyWaitPage(WaitPage):
    wait_for_all_groups = True

page_sequence = [
    MatchingWaitPage,instructions1, instructions2, TimeLimit, Decode, instructions3, instructions4,
    role_info,
    ControlQuestions, ControlQuestions, ControlQuestions, ControlQuestions, ControlQuestions,
    TutorialIntro, SenderTutorial, ReceiverTutorial, MyWaitPage, start_page,
    Round_number, SenderMessage, WaitForSender, ReceiverGuess, ResultsWaitPage, Results,
    MyWaitPage,
    HonestyGuess, FollowingGuess,
]


