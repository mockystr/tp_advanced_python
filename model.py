import psycopg2
from fields import Field
from exceptions import MultipleObjectsReturned, DoesNotExist


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)

        meta = namespace.get('Meta')
        if meta is None:
            raise ValueError('meta is none')
        if not hasattr(meta, 'table_name'):
            raise ValueError('table_name is empty')

        # todo mro
        # print(namespace.items())

        fields = {k: v for k, v in namespace.items()
                  if isinstance(v, Field)}

        # print(fields)
        namespace['_fields'] = fields
        namespace['_table_name'] = meta.table_name
        return super().__new__(mcs, name, bases, namespace)


class Manage:
    def __init__(self):
        self.connection = psycopg2.connect(user="emirnavruzov",
                                           password="qwe123@#29",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="ormdb")
        self.cursor = self.connection.cursor()
        self.model_cls = None

    def all(self):
        select_query = """SELECT * from {}""".format(self._table_name)
        self.cursor.execute(select_query)

        res = self.cursor.fetchall()
        # columns_names = [ii.name for ii in self.cursor.description]
        res_d = [self.model_cls(**dict(zip([ii.name for ii in self.cursor.description], res[i]))) for i in
                 range(len(res))]
        return res_d

    def get(self, *_, **kwargs):
        select_get_query = """
            SELECT * FROM {0}
            WHERE {1}
        """.format(self._table_name, ' AND '.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))

        self.cursor.execute(select_get_query)
        res = self.cursor.fetchall()

        if len(res) > 1:
            raise MultipleObjectsReturned('get() returned more than one {}'.format(self._table_name))
        elif len(res) == 0:
            raise DoesNotExist('{} matching query does not exist.'.format(self._table_name))
        else:
            res_d = dict(zip([i.name for i in self.cursor.description], res[0]))

        return self.model_cls(**res_d)

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner

        # print('owner', type(owner))
        setattr(self, '_table_name', owner._table_name)
        return self

    def create(self, *_, **kwargs):
        print(self.model_cls)


class Model(metaclass=ModelMeta):
    def __init__(self, *_, **kwargs):
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)

        # setattr(self, '_table_name', self._table_name)

    objects = Manage()

    class Meta:
        table_name = ''
