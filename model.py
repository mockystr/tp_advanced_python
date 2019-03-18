import psycopg2
from fields import Field
from exceptions import (MultipleObjectsReturned, DoesNotExist, DeleteError)
from constants import (user_db_constant,
                       password_db_constant,
                       host_db_constant,
                       port_db_constant,
                       database_db_constant)


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)

        meta = namespace.get('Meta')
        if meta is None:
            raise ValueError('meta is none')
        if not hasattr(meta, 'table_name'):
            raise ValueError('table_name is empty')

        # todo create table from shell
        # todo mro
        # print(namespace.items())

        fields = {k: v for k, v in namespace.items()
                  if isinstance(v, Field)}

        # print(fields)
        namespace['_fields'] = fields
        namespace['_table_name'] = meta.table_name
        return super().__new__(mcs, name, bases, namespace)


class Manage:
    # todo order by
    # todo queryset slices

    def __init__(self):
        self.connection = psycopg2.connect(user=user_db_constant,
                                           password=password_db_constant,
                                           host=host_db_constant,
                                           port=port_db_constant,
                                           database=database_db_constant)
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
            SELECT * FROM {0} WHERE {1};
        """.format(self._table_name, ' AND '.join(['{}=\'{}\''.format(k, v) for k, v in kwargs.items()]))
        # print(select_get_query)

        self.cursor.execute(select_get_query)
        res = self.cursor.fetchall()

        # print(res)
        # print(self.cursor.description)

        if len(res) > 1:
            raise MultipleObjectsReturned('get() returned more than one {} -- it returned {}!'.
                                          format(self._table_name, len(res)))
        elif len(res) == 0:
            raise DoesNotExist('{} matching query does not exist.'.format(self._table_name))
        else:
            res_d = dict(zip([i.name for i in self.cursor.description], res[0]))
        # print(res_d)
        return self.model_cls(**res_d)

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner

        # print('owner', type(owner))
        setattr(self, '_table_name', owner._table_name)
        return self

    def create(self, *_, **kwargs):
        # print([type(i) for i in kwargs.values()])
        insert_query = """
            INSERT INTO {0} ({1}) VALUES ({2}) RETURNING *;
        """.format(self.model_cls._table_name,
                   ', '.join(kwargs.keys()),
                   ', '.join(map(lambda x: "\'{}\'".format(x), kwargs.values())))
        # print(insert_query)
        self.cursor.execute(insert_query)

        res = dict(zip([i.name for i in self.cursor.description], self.cursor.fetchone()))
        # print('res', res)
        # if 'commit' in kwargs.keys():
        self.connection.commit()
        return self.model_cls(**res)


class Model(metaclass=ModelMeta):
    def __init__(self, *_, **kwargs):
        self.connection = psycopg2.connect(user=user_db_constant,
                                           password=password_db_constant,
                                           host=host_db_constant,
                                           port=port_db_constant,
                                           database=database_db_constant)
        self.cursor = self.connection.cursor()

        setattr(self, 'id', kwargs.get('id'))
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)

    objects = Manage()

    def delete(self):
        if self.id is None:
            raise DeleteError('{} object can\'t be deleted because its id attribute is set to None.'.
                              format(self._table_name))
        try:
            delete_query = """
                DELETE FROM {}
                WHERE id={}
            """.format(self._table_name, self.id)

            self.cursor.execute(delete_query)
            self.connection.commit()
        except Exception:
            raise DeleteError('{} object can\'t be deleted because its id is incorrect.'.
                              format(self._table_name))

    def update(self):
        pass

    class Meta:
        table_name = ''
