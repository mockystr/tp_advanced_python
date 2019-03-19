from model import Model
from fields import StringField, IntField, DateField, FloatField


class User(Model):
    name = StringField(required=True)
    description = StringField()
    date_added = DateField()
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
        order_by = '-name'

# class Man(User):
#     sex = StringField()
