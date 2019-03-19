from model import Model
from fields import StringField, IntField, DateField, FloatField


class User(Model):
    name = StringField(required=True)
    description = StringField()
    date_added = StringField()
    age = IntField()
    coins = FloatField()

    def __str__(self):
        return 'User {}'.format(self.name, self.age)

    def __repr__(self):
        return '<User {}>'.format(self.name, self.age)

    def update(self):
        pass

    class Meta:
        table_name = 'ormtable'

# class Man(User):
#     sex = StringField()
