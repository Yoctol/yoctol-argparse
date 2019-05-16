from yoctol_argparse import (
    YoctolArgumentParser,
    AppendIdValuePair,
    float_in_range,
)

parser = YoctolArgumentParser()

parser.add_argument(
    '--fruit',
    action=AppendIdValuePair,
    id_choices=['apple', 'banana', 'lemon'],
    value_metavar="PRICE",
    value_type=float_in_range(0., inclusive=False),
    help='(fruit_type, price) tuple',
)

parser.parse_args('--fruit apple 1 --fruit banana 2 --fruit apple 3'.split())
# = Namespace(fruit=[('apple', 1.), ('banana', 2.), ('apple', 3.)])

parser.parse_args('--fruit apple'.split())     # invalid nargs != 2
parser.parse_args('--fruit orange 1'.split())  # invalid id isn't in choices
parser.parse_args('--fruit apple z'.split())   # invalid value isn't float
parser.parse_args('--fruit apple 0'.split())   # invalid value isn't > 0.


parser.parse_args(['--help'])
# usage: id_value_pair.py [-h] [--fruit {apple, banana, lemon} Price]

# optional arguments:
#   -h, --help
#     show this help message and exit
#   --fruit {apple, banana, lemon} Price
