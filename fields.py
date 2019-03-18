import datetime


class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def validate(self, value):
        if value is None and not self.required:
            return None
        # todo exceptions
        return self.f_type(value)


class IntField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(int, required, default)


class StringField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(str, required, default)


class DateField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(datetime.datetime, required, default)


class FloatField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(float, required, default)
