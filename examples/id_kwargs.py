from yoctol_argparse import (
    YoctolArgumentParser,
    IdKwargs,
)

parser = YoctolArgumentParser()

parser.add_argument(
    '--exercise',
    action=IdKwargs,
    id_choices=['squat', 'bench', 'deadlift'],
    split_token=',',
    use_bool_abbreviation=True,
    default=IdKwargs.IdKwargsPair('squat', weight=50, reps=10, sets=5, use_belt=True),
    metavar='exercise_type',
    help='(exercise_type, kwargs_string)',
)

parser.parse_args('--exercise bench'.split())
# = Namespace(exercise=('bench', {}))
parser.parse_args('--exercise bench weight=70.0,reps=4,sets=4'.split())
# = Namespace(exercise=('bench', {'weight': 70.0, 'reps': 4, 'sets': 4}))
parser.parse_args('--exercise squat weight=90.0,reps=4,sets=4,use_belt'.split())
# = Namespace(exercise=('squat', {'weight': 90.0, 'reps': 4, 'sets': 4, 'use_belt': True}))
parser.parse_args('--exercise deadlift trainer=Daniel,style=sumo'.split())
# = Namespace(exercise=('deadlift', {'trainer': 'Daniel', 'style': 'sumo'}))

parser.parse_args('--exercise'.split())     # invalid nargs = 0
parser.parse_args('--exercise bench squat deadlift'.split())     # invalid nargs > 2
parser.parse_args('--exercise smith_machine weight=10'.split())  # invalid id isn't in choices
parser.parse_args('--exercise bench weight=10,weight=40'.split())  # duplicated key


parser.parse_args(['--help'])
# usage: id_value_pair.py [-h] [--exercise {squat, bench, deadlift} KEY1=VAL1,KEY2=VAL2 ...]

# optional arguments:
#   -h, --help
#     show this help message and exit
#   --exercise {squat, bench, deadlift} KEY1=VAL1,KEY2=VAL2 ...
