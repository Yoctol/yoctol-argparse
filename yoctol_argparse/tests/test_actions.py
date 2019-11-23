import pytest
from unittest.mock import patch

from ..actions import AppendIdValuePair, StoreIdKwargs
from ..parser import YoctolArgumentParser


class TestAppendIdValuePair:

    @pytest.fixture(scope='class')
    def yoctol_parser(self):
        parser = YoctolArgumentParser(prog='main.py')
        parser.add_argument(
            '--foo',
            action=AppendIdValuePair,
            id_choices=['a', 'b'],
            value_metavar='boo',
            value_type=int,
        )
        return parser

    def test_append(self, yoctol_parser):
        with patch('sys.argv', 'main.py --foo a 1 --foo b 2 --foo a 3'.split(' ')):
            args = yoctol_parser.parse_args()
        assert args.foo == [('a', 1), ('b', 2), ('a', 3)]

    @pytest.mark.parametrize('invalid_arg', [
        pytest.param('main.py --foo a', id='invalid_nargs'),
        pytest.param('main.py --foo a 1 b', id='invalid_nargs'),
        pytest.param('main.py --foo c 1', id='invalid_choice'),
        pytest.param('main.py --foo a b', id='invalid_value'),
    ])
    def test_raise_invalid_arg(self, yoctol_parser, invalid_arg):
        argv = invalid_arg.split()
        with patch('sys.argv', argv), pytest.raises(SystemExit) as exc_info:
            yoctol_parser.parse_args()
        assert exc_info.value.code == 2


class TestStoreIdKwargs:

    @pytest.fixture(scope='class')
    def yoctol_parser(self):
        parser = YoctolArgumentParser(prog='main.py')
        parser.add_argument(
            '--foo',
            action=StoreIdKwargs,
            id_choices=['a', 'b'],
            use_bool_abbreviation=True,
        )
        return parser

    @pytest.mark.parametrize('arg_string, expected_output', [
        ['main.py --foo a', ('a', {})],
        [
            'main.py --foo a I=1,F1=1.,F2=1e-4,F3=-1e-4',
            ('a', {'I': 1, 'F1': 1., 'F2': 1e-4, 'F3': -1e-4}),
        ],
        [
            'main.py --foo a B1=False,B2=True,B3',
            ('a', {'B1': False, 'B2': True, 'B3': True}),
        ],
        [
            'main.py --foo a NONE=None,FUNC=max,S=s',
            StoreIdKwargs.IdKwargsPair('a', {'NONE': None, 'FUNC': max, 'S': 's'}),
        ],
    ])
    def test_store(self, yoctol_parser, arg_string, expected_output):
        with patch('sys.argv', arg_string.split(' ')):
            args = yoctol_parser.parse_args()
        assert args.foo == expected_output

    @pytest.mark.parametrize('invalid_arg', [
        pytest.param('main.py --foo', id='nargs<1'),
        pytest.param('main.py --foo a 1 b', id='nargs>2'),
        pytest.param('main.py --foo c 1', id='invalid_choice'),
        pytest.param('main.py --foo a x=1=y', id='invalid_format_='),
        pytest.param('main.py --foo a x=1+y=y', id='invalid_format_split'),
        pytest.param('main.py --foo a x=1,x=2', id='duplicated_key'),
    ])
    def test_raise_invalid_arg(self, yoctol_parser, invalid_arg):
        argv = invalid_arg.split()
        with patch('sys.argv', argv), pytest.raises(SystemExit) as exc_info:
            yoctol_parser.parse_args()
        assert exc_info.value.code == 2
