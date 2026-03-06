from otree.api import *
import random

def make_field(label):
    return models.IntegerField(
        choices=[
            (1, "Muy favorable"),
            (2, "Algo favorable"),
            (3, "Algo desfavorable"),
            (4, "Muy desfavorable"),
            (5, "Sin opinión"),
            (6, "No sé"),
        ],
        label=label,
        widget=widgets.RadioSelect,
    )

class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Demographics
    age = models.IntegerField(label='Edad', min=13, max=100)

    gender = models.IntegerField(
        label='Género',
        choices=[[0, 'Masculino'], [1, 'Femenino'], [2, 'Prefiero no decir'], [3, 'Otro']]
    )
    gender_add = models.StringField(blank=True, label='')
    education = models.IntegerField(
        choices=[[0, 'Menos que secundaria'],
                 [1, 'Secundaria'],
                 [2, 'Algo de universidad'],
                 [3, 'Título de asociado'],
                 [4, 'Título universitario'],
                 [5, 'Título avanzado o profesional']
                 ],
        label='¿Cuál es tu nivel más alto de educación?'
    )
    student = models.IntegerField(
        label='¿Estás actualmente inscrito en la universidad?',
        choices=[[0, 'No'], [1, 'Sí']]
    )
    experiments = models.IntegerField(
        label='Por favor, da una estimación aproximada del número de experimentos en los que has participado antes',
        blank=True
    )

    reasoning = models.LongStringField(
        label='Por favor, da una explicación concisa de cómo tomaste tus decisiones en el experimento',
        blank=True
    )

    chosen_role = models.IntegerField(
        choices=[[1, 'Jugador A'],
                 [2, 'Jugador B'],
                 [0, 'Indiferente'],
                 ],
        label='Imagina que jugaras el mismo juego de nuevo y tuvieras una elección, ¿preferirías ser Jugador A o Jugador B?'
    )

    org_fundacion_ideas = make_field("Fundación Ideas para la Paz")
    org_fundacion_mujer = make_field("Fundación de la Mujer")
    org_fundacion_corona = make_field("Fundación Corona")
    org_fundacion_santo_domingo = make_field("Fundación Santo Domingo")
    org_fundacion_mujer_futuro = make_field("Fundación Mujer y Futuro")
    org_unicef_colombia = make_field("UNICEF Colombia")

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'student', 'experiments', 'reasoning', 'chosen_role',
                   "org_fundacion_ideas",
                   "org_fundacion_mujer",
                   "org_fundacion_corona",
                   "org_fundacion_santo_domingo",
                   "org_fundacion_mujer_futuro",
                   "org_unicef_colombia"
                   ]

class Redirect(Page):
    pass


page_sequence = [Demographics, Redirect]