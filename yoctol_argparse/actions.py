import argparse

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

    def __init__(
            self,
            id_choices,
            split_token='&',
            use_boolean_abbreviation=True,
            **kwargs,
        ):
        super().__init__(nargs=2, **kwargs)
        self.id_choices = id_choices
        self.split_token = split_token
        self.use_boolean_abbreviation = use_boolean_abbreviation
        self.metavar = (format_choices(id_choices), 'KWARGS STRING')

    def __call__(self, parser, namespace, values, option_string=None):
        id_, kwarg_string = values
        if id_ not in self.id_choices:
            raise argparse.ArgumentError(
                self,
                f"invalid choice: '{id_}' "
                f"(choose from {', '.join(map(repr, self.id_choices))})",
            )
        try:
            kwargs = self._process_kwargs_string(kwarg_string)
        except (TypeError, ValueError):
            raise argparse.ArgumentError(
                self,
                f"invalid kwargs: {kwarg_string!r}",
            )

        setattr(namespace, self.dest, (id_, kwargs))

    def _process_kwargs_string(self, kwarg_string):
        kwargs = {}
        kvs = kwarg_string.split(self.split_token)
        for kv in kvs:
            if '=' in kv:
                key, val = kv.split('=')
                val = eval(val)
            elif self.use_boolean_abbreviation:
                key, val = kv, True
            else:
                raise ValueError

            if key in kwargs:
                raise ValueError
            kwargs[key] = val

        return kwargs
