from model import Model
from fields import StringField, IntField


class User(Model):
    name = StringField()
    description = StringField(required=False)
    date_added = StringField(required=False)
    age = IntField(required=False)

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
