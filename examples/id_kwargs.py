from yoctol_argparse import (
    YoctolArgumentParser,
    StoreIdKwargs,
)

parser = YoctolArgumentParser()

parser.add_argument(
    '--exercise',
    action=StoreIdKwargs,
    id_choices=['squat', 'bench', 'deadlift'],
    split_token='&',
    use_bool_abbreviation=True,
    help='(exercise_type, kwargs_string)',
)

parser.parse_args('--exercise bench weight=70.0&reps=4&sets=4'.split())
# = Namespace(exercise=('bench', {'weight': 70.0, 'reps': 4, 'sets': 4}))
parser.parse_args('--exercise squat weight=90.0&reps=4&sets=4&use_belt'.split())
# = Namespace(exercise=('squat', {'weight': 90.0, 'reps': 4, 'sets': 4, 'use_belt': True}))
parser.parse_args('--exercise deadlift trainer="Daniel"&style="sumo"'.split())
# = Namespace(exercise=('deadlift', {'trainer': 'Daniel', 'style': 'sumo'}))

parser.parse_args('--exercise bench'.split())     # invalid nargs != 2
parser.parse_args('--exercise smith_machine weight=10'.split())  # invalid id isn't in choices
parser.parse_args('--exercise bench weight=max'.split())   # invalid value isn't int, float or bool
parser.parse_args('--exercise bench weight=10&weight=40'.split())  # duplicated key


parser.parse_args(['--help'])
# usage: id_value_pair.py [-h] [--exercise {squat, bench, deadlift} KWARGS_STRING]

# optional arguments:
#   -h, --help
#     show this help message and exit
#   --exercise {squat, bench, deadlift} KWARGS_STRING
