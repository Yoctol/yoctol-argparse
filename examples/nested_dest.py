from yoctol_argparse import YoctolArgumentParser

parser = YoctolArgumentParser()

parser.add_argument(
    '--exercise_type',
    dest='exercise.type',
    choices=['squat', 'bench', 'deadlift'],
)
parser.add_argument(
    '--exercise_sets',
    dest='exercise.volume.sets',
    type=int,
)
parser.add_argument(
    '--exercise_reps',
    dest='exercise.volume.reps',
    type=int,
)


parser.parse_args('--exercise_type bench --exercise_sets 5 --exercise_reps 10'.split())
# = NestedNamespace(exercise=NestedNamespace(type='bench', volume=NestedNamespace(reps=10, sets=5)))
