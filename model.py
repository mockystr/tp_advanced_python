import psycopg2
from fields import Field
from exceptions import (MultipleObjectsReturned,
                        DoesNotExist,
                        DeleteError,
                        DuplicateKeyConstraint)
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
    # todo filter

    def __init__(self):
        self.connection = psycopg2.connect(user=user_db_constant,
                                           password=password_db_constant,
                                           host=host_db_constant,
                                           port=port_db_constant,
                                           database=database_db_constant)
        self.cursor = self.connection.cursor()
        self.model_cls = None

    def all(self):
        """get all rows from table"""
        select_query = """SELECT * from {}""".format(self._table_name)
        self.cursor.execute(select_query)

        res = self.cursor.fetchall()
        res_d = [self.model_cls(**dict(zip([ii.name for ii in self.cursor.description], res[i]))) for i in
                 range(len(res))]
        return res_d

    def get(self, *_, **kwargs):
        """get only one object"""
        select_get_query = """
            SELECT * FROM {0} WHERE {1};
        """.format(self._table_name, ' AND '.join(['{}=\'{}\''.format(k, v) for k, v in kwargs.items()]))

        self.cursor.execute(select_get_query)
        res = self.cursor.fetchall()

        if len(res) > 1:
            raise MultipleObjectsReturned('get() returned more than one {} -- it returned {}!'.
                                          format(self._table_name, len(res)))
        elif len(res) == 0:
            raise DoesNotExist('{} matching query does not exist.'.format(self._table_name))
        elif len(res) == 1:
            res_d = dict(zip([i.name for i in self.cursor.description], res[0]))

        return self.model_cls(**res_d)

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner

        setattr(self, '_table_name', owner._table_name)
        return self

    def create(self, *_, **kwargs):
        """create object"""
        insert_query = """
            INSERT INTO {0} ({1}) VALUES ({2}) RETURNING *;
        """.format(self.model_cls._table_name,
                   ', '.join(kwargs.keys()),
                   ', '.join(map(lambda x: "\'{}\'".format(x), kwargs.values())))

        self.cursor.execute(insert_query)
        res = dict(zip([i.name for i in self.cursor.description], self.cursor.fetchone()))
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
        """delete object"""
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

    def save(self):
        """update if exists in db or create if not"""
        if self.__dict__.get('id') is not None:
            print('i need to update!')
            update_query = """
            
            """
        else:
            object_fields = ['id', *list(self._fields.keys())]
            # object_values = [self.__dict__.get('id', 'DEFAULT'), *list(self._fields.values())]
            # print('object_fields', object_fields)
            # print('object_values', object_values)
            values = []
            for i in object_fields:
                if getattr(self, i) is not None:
                    values.append(format("\'{}\'").format(i))
                else:
                    if i == 'id':
                        values.append('DEFAULT')
                    else:
                        values.append("null")

            insert_query = """
                        INSERT INTO {0} ({1}) VALUES ({2}) RETURNING id;
                    """.format(self._table_name,
                               ', '.join(object_fields),
                               ', '.join(values))
            # print(insert_query)
            self.cursor.execute(insert_query)
            self.connection.commit()

            self.id = self.cursor.fetchone()[0]

    class Meta:
        table_name = ''
