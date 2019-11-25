import argparse
import ast
from collections import namedtuple

from .formatters import format_choices


class AppendIdValuePair(argparse.Action):

    def __init__(self, id_choices, value_type, value_metavar, **kwargs):
        super().__init__(nargs=2, **kwargs)
        self.id_choices = id_choices
        self.value_type = value_type
        self.metavar = (format_choices(id_choices), value_metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        id_, value = values
        try:
            value = self.value_type(value)
        except (TypeError, ValueError):
            raise argparse.ArgumentError(
                self,
                f"invalid {self.value_type.__name__}: {value!r}",
            )

        if id_ not in self.id_choices:
            raise argparse.ArgumentError(
                self,
                f"invalid choice: '{id_}' "
                f"(choose from {', '.join(map(repr, self.id_choices))})",
            )
        if not getattr(namespace, self.dest, None):
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append((id_, value))


class StoreIdKwargs(argparse.Action):

    IdKwargsPair = namedtuple('IdKwargsPair', ['id', 'kwargs'])

    def __init__(
            self,
            id_choices,
            split_token=',',
            use_bool_abbreviation=True,
            default_as_string=True,
            **kwargs,
        ):
        super().__init__(nargs='+', **kwargs)
        self.id_choices = id_choices
        self.split_token = split_token
        self.default_as_string = default_as_string
        self.use_bool_abbreviation = use_bool_abbreviation
        self.metavar = (format_choices(id_choices), f'KEY1=VALUE1{split_token}KEY2=VALUE2')

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) == 2:
            id_, kwarg_string = values
            try:
                kwargs = self._process_kwargs_string(kwarg_string)
            except ValueError:
                raise argparse.ArgumentError(
                    self,
                    f"invalid kwargs: {kwarg_string!r}",
                )
            except NameError:
                raise argparse.ArgumentError(
                    self,
                    "value should be built-in types.",
                )
        elif len(values) == 1:
            id_, kwargs = values[0], {}
        else:
            raise argparse.ArgumentError(
                self,
                'expected at most 2 argument',
            )

        if id_ not in self.id_choices:
            raise argparse.ArgumentError(
                self,
                f"invalid choice: '{id_}' "
                f"(choose from {', '.join(map(repr, self.id_choices))})",
            )

        setattr(namespace, self.dest, self.IdKwargsPair(id_, kwargs))

    def _process_kwargs_string(self, kwarg_string):
        kwargs = {}
        kvs = kwarg_string.split(self.split_token)
        for kv in kvs:
            if '=' in kv:
                key, val = kv.split('=')
                try:
                    val = ast.literal_eval(val)
                except (SyntaxError, ValueError):
                    if not self.default_as_string:
                        raise
                    # default as string if can't eval
            elif self.use_bool_abbreviation:
                key, val = kv, True
            else:
                raise ValueError

            if key in kwargs:
                raise ValueError
            kwargs[key] = val

        return kwargs
