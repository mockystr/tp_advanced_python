import psycopg2
from fields import Field
from exceptions import (MultipleObjectsReturned,
                        DoesNotExist,
                        DeleteError,
                        DuplicateKeyConstraint,
                        OrderByFieldError,
                        IntegrityError,
                        ParentClashError)
from constants import (user_db_constant,
                       password_db_constant,
                       host_db_constant,
                       port_db_constant,
                       database_db_constant)

"""
КОСТЫЛИ:
name == 'None'

"""

connection = psycopg2.connect(user=user_db_constant,
                              password=password_db_constant,
                              host=host_db_constant,
                              port=port_db_constant,
                              database=database_db_constant)
cursor = connection.cursor()


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)

        meta = namespace.get('Meta')
        if meta is None:
            raise ValueError('meta is none')

        if not hasattr(meta, 'table_name'):
            raise ValueError('table_name does not exist')
        else:
            if not meta.table_name:
                raise ValueError('table_name is empty')

        # todo create table from shell
        # todo mro

        # print('bases[0] dict', bases[0].__dict__.items())
        # print('namespace', namespace)

        if len(bases) > 1:
            raise ParentClashError("You can't inherit more than one table!")

        if bases[0] != Model:
            fields = {k: v for k, v in [*namespace.items(), *bases[0].__dict__.items()]
                      if isinstance(v, Field)}
        else:
            fields = {k: v for k, v in namespace.items()
                      if isinstance(v, Field)}

        if hasattr(meta, 'order_by'):
            if isinstance(meta.order_by, (tuple, list)):
                stripped_order = [i.strip('-') for i in meta.order_by]
                # print(stripped_order)
            # elif isinstance(meta.order_by, str):
            #     stripped_order = meta.order_by.strip('-')
            #     # print(stripped_order)
            else:
                raise ValueError("ordering can be only tuple or list object")

            if not set(stripped_order).issubset(fields.keys()):
                raise OrderByFieldError(
                    'ordering refers to the nonexistent field \'{}\''.format(stripped_order))

        namespace['_fields'] = fields
        namespace['_table_name'] = meta.table_name
        namespace['_order_by'] = getattr(meta, 'order_by', None)
        return super().__new__(mcs, name, bases, namespace)


class Manage:
    # todo order by
    # set(['a', 'b']).issubset(['a', 'b', 'c'])
    # todo queryset slices
    # todo filter

    def __init__(self):
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
            self.formatted_order = []

            if isinstance(self.model_cls._order_by, (tuple, list)):
                for i in self.model_cls._order_by:
                    if i.startswith('-'):
                        self.formatted_order.append("{} DESC".format(i.strip('-')))
                    else:
                        self.formatted_order.append("{}".format(i.strip('-')))
            else:
                raise ValueError("ordering can be only tuple or list object")

        # setattr(self, '_table_name', owner._table_name)
        # setattr(self, '_order_by', owner._order_by)
        return self

    def all(self):
        """Get all rows from table"""
        select_query = """SELECT * FROM {}""".format(self.model_cls._table_name)

        if self.formatted_order:
            select_query += " ORDER BY {}".format(', '.join(self.formatted_order))

        # print(select_query)

        cursor.execute(select_query)
        res = cursor.fetchall()

        res_d = [self.model_cls(**dict(zip([ii.name for ii in cursor.description], res[i]))) for i in
                 range(len(res))]
        return res_d

    def filter(self, *_, **kwargs):
        """Get rows that are suitable for condition"""
        select_filter_query = """
            SELECT * FROM {0} WHERE {1}
        """.format(self.model_cls._table_name, ' AND '.join(['{}=\'{}\''.format(k, v) for k, v in kwargs.items()]))

        if self.formatted_order:
            select_filter_query += " ORDER BY {}".format(', '.join(self.formatted_order))

        print(select_filter_query)

        cursor.execute(select_filter_query)
        res = cursor.fetchall()
        res_d = [self.model_cls(**dict(zip([ii.name for ii in cursor.description], res[i]))) for i in
                 range(len(res))]
        return res_d

    def get(self, *_, **kwargs):
        """Get only one object"""
        select_get_query = """
            SELECT * FROM {0} WHERE {1};
        """.format(self.model_cls._table_name, ' AND '.join(['{}=\'{}\''.format(k, v) for k, v in kwargs.items()]))

        cursor.execute(select_get_query)
        res = cursor.fetchall()

        if len(res) > 1:
            raise MultipleObjectsReturned('get() returned more than one {} -- it returned {}!'.
                                          format(self.model_cls._table_name, len(res)))
        elif len(res) == 0:
            raise DoesNotExist('{} matching query does not exist.'.format(self.model_cls._table_name))
        else:
            res_d = dict(zip([i.name for i in cursor.description], res[0]))

        return self.model_cls(**res_d)

    def create(self, *_, **kwargs):
        """Create object"""
        insert_query = """
            INSERT INTO {0} ({1}) VALUES ({2}) RETURNING *;
        """.format(self.model_cls._table_name,
                   ', '.join(kwargs.keys()),
                   ', '.join(map(lambda x: "\'{}\'".format(x), kwargs.values())))

        cursor.execute(insert_query)
        res = dict(zip([i.name for i in cursor.description], cursor.fetchone()))
        connection.commit()

        return self.model_cls(**res)


class Model(metaclass=ModelMeta):
    def __init__(self, *_, **kwargs):
        setattr(self, 'id', kwargs.get('id'))
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)

    objects = Manage()

    def delete(self):
        """Delete object"""
        if self.id is None:
            raise DeleteError('{} object can\'t be deleted because its id attribute is set to None.'.
                              format(self._table_name))
        try:
            delete_query = """
                DELETE FROM {}
                WHERE id={}
            """.format(self._table_name, self.id)

            cursor.execute(delete_query)
            connection.commit()
        except Exception:
            raise DeleteError('{} object can\'t be deleted because its id is incorrect.'.
                              format(self._table_name))

    def check_fields(self):
        """Return exception if required field is none"""
        # print('fields', self._fields)
        for field_name, field in self._fields.items():
            # print(getattr(self, field_name) == "None")
            # print(field.required)

            if (getattr(self, field_name) is None or getattr(self, field_name) == "None") and field.required:
                raise IntegrityError(
                    'NOT NULL constraint failed: {} in {} column'.format(getattr(self, field_name), field_name))

    def save(self):
        """Update if exists in db or create if not"""
        object_fields = ['id', *list(self._fields.keys())]
        self.check_fields()

        if self.__dict__.get('id') is not None:

            set_arr = []
            for i in object_fields:
                attr_value = getattr(self, i)

                if attr_value is None:
                    set_arr.append("{}=null".format(i))
                else:
                    set_arr.append("{}=\'{}\'".format(i, attr_value))

            update_query = """
                UPDATE {}
                SET {}
                WHERE id={}
            """.format(self._table_name,
                       ', '.join(set_arr),
                       self.id)
            # print(update_query)
            cursor.execute(update_query)
            connection.commit()
        else:
            # object_values = [self.__dict__.get('id', 'DEFAULT'), *list(self._fields.values())]
            # print('object_fields', object_fields)
            # print('object_values', object_values)
            # print([(i, getattr(self, i)) for i in object_fields])
            values = []
            for i in object_fields:
                if getattr(self, i) is not None:
                    values.append(format("\'{}\'").format(getattr(self, i)))
                else:
                    if i == 'id':
                        values.append('DEFAULT')
                    else:
                        values.append("null")
            # print(values)
            insert_query = """
                        INSERT INTO {0} ({1}) VALUES ({2}) RETURNING id;
                    """.format(self._table_name,
                               ', '.join(object_fields),
                               ', '.join(values))
            cursor.execute(insert_query)
            connection.commit()

            self.id = cursor.fetchone()[0]

    class Meta:
        table_name = ''
