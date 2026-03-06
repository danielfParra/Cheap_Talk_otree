from otree.api import *

author = 'Daniel Parra'
doc = """
Consent
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    players = subsession.get_players()
    num_players = len(players)

    for i, p in enumerate(subsession.session.get_participants(), start=1):
        p.label = f'P{i}'

    # ✅ If n=2, skip pools and let oTree handle matching
    if num_players == 2:
        players[0].participant.vars['role'] = 'Player A'
        players[1].participant.vars['role'] = 'Player B'
        players[0].participant.vars['receiver_type'] = 'none'
        if subsession.session.config['treatment'] == 'Decode':
            players[1].participant.vars['receiver_type'] = 'decode'
        else:
            players[1].participant.vars['receiver_type'] = 'direct'
        return  # No pool assignment needed

    # Define possible scenarios
    scenarios = {
        16: {'num_pools': 4, 'pool_size': 4},  # 4 pools of 4
        20: {'num_pools': 4, 'pool_size': 5},  # 4 pools of 5
        24: {'num_pools': 6, 'pool_size': 4},  # 6 pools of 4
        30: {'num_pools': 6, 'pool_size': 5},  # 6 pools of 5
    }

    # Select the closest matching scenario
    if num_players in scenarios:
        num_pools = scenarios[num_players]['num_pools']  # Total pools
        pool_size = scenarios[num_players]['pool_size']  # Players per pool
    else:
        raise ValueError(f"Unexpected number of participants: {num_players}")

    num_A_pools = num_pools // 2  # Half the pools for Player A
    num_B_pools = num_pools // 2  # Half the pools for Player B

    # Split players into Player A and Player B
    num_As = num_players // 2
    num_Bs = num_players - num_As  # Ensure balance

    players_A = players[:num_As]  # First half are A’s
    players_B = players[num_As:]  # Second half are B’s

    # Assign pools **ensuring pools 1 to num_A_pools are for A, and others for B**
    for i, player in enumerate(players_A):
        player.participant.vars['pool'] = (i % num_A_pools) + 1  # Pools 1, 2, ..., num_A_pools
        player.participant.vars['role'] = 'Player A'
        player.participant.vars['receiver_type'] = 'none'

    for i, player in enumerate(players_B):
        player.participant.vars['pool'] = (i % num_B_pools) + num_A_pools + 1  # Pools num_A_pools+1, ..., num_pools
        player.participant.vars['role'] = 'Player B'

    # Dictionary of PLayer B pools
    pool_dict = {}
    for player in players_B:
        pool = player.participant.vars['pool']
        if pool not in pool_dict:
            pool_dict[pool] = []
        pool_dict[pool].append(player)
    
    # Add two decoders to each pool
    for pool, players in pool_dict.items():
        for i, player in enumerate(players):
            if i < 2 and player.session.config['treatment'] == 'Decode':
                player.participant.vars['receiver_type'] = 'decode'
            else:
                player.participant.vars['receiver_type'] = 'direct'

    # ✅ Add this to verify assignments:
    print('\n--- Pool assignments in consent ---')
    for p in subsession.get_players():
        print(f"Participant {p.id_in_subsession}: pool = {p.participant.vars['pool']}, role = {p.participant.vars['role']}, receiver_type = {p.participant.vars['receiver_type']}")



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(
        label='''He leído la información sobre
    de datos y doy mi consentimiento para participar en el experimento y en el
    tratamiento de datos:''',
        choices=[[0, 'No'], [1, 'Sí']],
    )
    # consent2 = models.IntegerField(
    #     label='''Can you be in front of the screen for the
    # next 15 minutes?''',
    #     choices=[[0, 'No'], [1, 'Yes']],
    # )


# FUNCTIONS
# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']


def consent_error_message(player, value):
    if value != 1:
        return '''Si no está de acuerdo, no puede participar en el experimento de hoy.
        En este caso, puede cerrar la ventana y ponerse en contacto con los
        experimentadores.'''


# class Consent2(Page):
#     form_model = 'player'
#     form_fields = ['consent2']
#
#     @staticmethod
#     def consent2_error_message(player: Player, value):
#         if value != 1:
#             return '''If you do not have the time now, you cannot participate in today\'s
#             experiment. In this case, you can close the window and contact the
#             experimenters.'''


page_sequence = [Consent]
