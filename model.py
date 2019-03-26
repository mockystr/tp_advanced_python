from typing import List

import psycopg2
from fields import Field
from exceptions import (MultipleObjectsReturned,
                        DoesNotExist,
                        DeleteError,
                        DuplicateKeyConstraint,
                        OrderByFieldError,
                        IntegrityError,
                        ParentClashError,
                        LookupError)
from constants import (user_db_constant,
                       password_db_constant,
                       host_db_constant,
                       port_db_constant,
                       database_db_constant)

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

        if hasattr(meta, 'table_name'):
            namespace['_table_name'] = meta.table_name
        else:
            namespace['_table_name'] = name

        # todo create table from shell

        if len(bases) > 1:
            raise ParentClashError("You can't inherit more than one table!")
        # todo use fields from base class

        if bases[0] != Model:
            fields = {k: v for k, v in [*namespace.items(), *bases[0].__dict__.items()]
                      if isinstance(v, Field)}
        else:
            fields = {k: v for k, v in namespace.items()
                      if isinstance(v, Field)}

        if hasattr(meta, 'order_by'):
            if isinstance(meta.order_by, (tuple, list)):
                stripped_order = [i.strip('-') for i in meta.order_by]
            else:
                raise ValueError("ordering can be only tuple or list object")

            if not set(stripped_order).issubset(fields.keys()):
                raise OrderByFieldError(
                    'ordering refers to the nonexistent field \'{}\''.format(stripped_order))

        namespace['_fields'] = fields
        namespace['_order_by'] = getattr(meta, 'order_by', None)
        return super().__new__(mcs, name, bases, namespace)


class Condition:
    def __init__(self, field_name, cond, value):
        self._conditions = ['exact', 'in', 'lt', 'gt', 'le', 'ge', 'contains', 'startswith', 'endswith']
        self.field_name = field_name
        self.cond = cond
        self.value = value

    def format_cond(self):
        print(self.field_name, self.cond, self.value)
        if self.cond in self._conditions:
            if self.cond == 'exact':
                return "{}={}".format(self.field_name, self.value)
            if self.cond == 'in':
                return "{} IN {}".format(self.field_name, tuple(self.value))
            if self.cond == 'lt':
                return "{} < {}".format(self.field_name, self.value)
            if self.cond == 'gt':
                return "{} > {}".format(self.field_name, self.value)
            if self.cond == 'le':
                return "{} <= {}".format(self.field_name, self.value)
            if self.cond == 'ge':
                return "{} >= {}".format(self.field_name, self.value)
            if self.cond == 'contains':
                return "{} LIKE '%{}%' ESCAPE '\\'".format(self.field_name, self.value)
            if self.cond == 'startswith':
                return "{} LIKE '{}%' ESCAPE '\\'".format(self.field_name, self.value)
            if self.cond == 'endswith':
                return "{} LIKE '%{}' ESCAPE '\\'".format(self.field_name, self.value)


# todo reverse method

class QuerySet:
    def __init__(self, model_cls, where=None, limit=None, order_by=None, res=None):
        self.model_cls = model_cls
        self.fields = self.model_cls._fields
        self.where: dict = where
        self.res = res
        self.limit = limit
        self.__cache = {'count': -1, 'order_by': 0}

        if order_by is not None and isinstance(order_by, (list, tuple)):
            self._order_by: list = order_by
        elif hasattr(self.model_cls, '_order_by'):
            if isinstance(self.model_cls._order_by, (list, tuple)):
                self._order_by: list = self.model_cls._order_by
        elif order_by is not None:
            raise ValueError("ordering can be only tuple or list object")
        else:
            self._order_by = None

    def format_where(self):
        if self.where:
            where_list = []

            for i in self.where.items():
                ispl = i[0].split('__')
                if len(ispl) == 2:
                    where_list.append(Condition(ispl[0], ispl[1], i[1]).format_cond())
                if len(ispl) == 1:
                    where_list.append(Condition(i[0], 'exact', i[1]).format_cond())
            return where_list
        return None

    def format_limit(self):
        if self.limit is not None:
            limit_list = []

            if isinstance(self.limit, slice):
                if self.limit.start:
                    limit_list.extend(['OFFSET', str(self.limit.start)])
                if self.limit.stop:
                    limit_list.extend(['LIMIT', str(self.limit.stop - (self.limit.start or 0))])
                return limit_list
            elif isinstance(self.limit, int):
                limit_list.extend(['OFFSET', str(self.limit), 'LIMIT', '1'])
                return limit_list
            else:
                raise TypeError('unsupported type of limit index')
        return None

    def format_order_list(self):
        if self._order_by:
            formatted_order = []

            for i in self._order_by:
                if i.startswith('-'):
                    formatted_order.append("{} DESC NULLS LAST".format(i.strip('-')))
                else:
                    formatted_order.append("{} NULLS FIRST".format(i.strip('-')))
            return formatted_order
        return None

    def filter(self, *_, **kwargs):
        """Get rows that are suitable for condition"""
        if self.where is not None:
            self.where = {**self.where, **kwargs}
        else:
            self.where = kwargs
        return self

    def __getitem__(self, key):
        if isinstance(key, int):
            self.limit = key
            return self
        elif isinstance(key, slice):
            if self.limit is not None:
                if key.stop:
                    if self.limit.stop:
                        max_start = max(self.limit.start or 0, key.start or 0)
                        min_stop = min(self.limit.stop, key.stop)
                        if max_start < min_stop:
                            self.limit = slice(max_start,
                                               min_stop,
                                               None)
                        else:
                            self.limit = slice((self.limit.start or 0) + (key.start or 0),
                                               min(self.limit.stop,
                                                   (self.limit.start or 0) + key.stop),
                                               None)
                    else:
                        self.limit = slice(max(self.limit.start or 0, key.start or 0), key.stop, None)
                else:
                    self.limit = slice(max(self.limit.start or 0, key.start or 0), getattr(self.limit, 'stop'), None)
            else:
                self.limit = key
            return self
        else:
            raise TypeError('wrong index')

    def order_by(self, *args):
        if isinstance(args, (tuple, list)):
            stripped_order = [i.strip('-') for i in args]
            if not set(stripped_order).issubset(self.model_cls._fields.keys()):
                raise OrderByFieldError('ordering refers to the nonexistent field \'{}\''.
                                        format(stripped_order))
        else:
            raise ValueError("ordering can be only tuple or list object")

        if self._order_by is not None:
            if self.__cache['order_by'] == 0:
                self._order_by = args
                self.__cache['order_by'] = 1
            else:
                self._order_by = [*self._order_by, *args]
        else:
            self._order_by = args
        return self

    def reverse(self):
        if self.res is not None:
            if isinstance(self.res, list):
                self.res.reverse()
        return self

    def count(self):
        if 'count' in self.__cache.keys() and self.__cache['count'] != -1:
            return self.__cache['count']
        return self._count_perform()

    def _count_perform(self):
        if self.res is not None:
            res_len = len(self.res)
            self.__cache['count'] = res_len
            return res_len

        query = ['SELECT count(*) FROM (SELECT * FROM {}'.format(self.model_cls._table_name)]

        if self.where:
            query.extend(['WHERE', ' AND '.join(self.format_where())])
        if self.limit:
            query.extend(self.format_limit())

        query.append(') as tmp_table')
        print(' '.join(query))
        cursor.execute(' '.join(query))
        res_len = cursor.fetchone()[0]
        self.__cache['count'] = res_len
        return res_len

    def _build(self):
        query = ["SELECT *"]
        query.extend(['FROM', self.model_cls._table_name])

        if self.where:
            query.extend(['WHERE', ' AND '.join(self.format_where())])

        if self._order_by is not None:
            query.extend(["ORDER BY", ", ".join(self.format_order_list())])

        if self.limit is not None:
            query.extend(self.format_limit())

        # print('BUILD QUERY', query)
        print(' '.join(query))

        cursor.execute(' '.join(query))
        res = cursor.fetchall()
        self.res = [self.model_cls(**dict(zip([ii.name for ii in cursor.description], res[i]))) for i in
                    range(len(res))]

    def __str__(self):
        return '<QuerySet of {}>'.format(self.model_cls._table_name)

    # def __repr__(self):
    #     self._build()
    #     return '<model.QuerySet ({})>'.format(self.res)

    def __iter__(self):
        if self.res is None:
            self._build()

        return iter(self.res)


class Manage:
    def __init__(self):
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
        return self

    def all(self):
        """Get all rows from table"""
        return QuerySet(self.model_cls)

    def filter(self, *_, **kwargs):
        """Get rows that are suitable for condition"""
        return QuerySet(self.model_cls, kwargs)

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

    def check_fields(self):
        """Return exception if required field is none"""
        for field_name, field in self._fields.items():
            if (getattr(self, field_name) is None or getattr(self, field_name) == "None") and field.required:
                raise IntegrityError(
                    'NOT NULL constraint failed: {} in {} column'.format(getattr(self, field_name),
                                                                         field_name))

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

            update_query = "UPDATE {} SET {} WHERE id={}".format(self._table_name,
                                                                 ', '.join(set_arr),
                                                                 self.id)
            cursor.execute(update_query)
            connection.commit()
        else:
            values = []
            for i in object_fields:
                if getattr(self, i) is not None:
                    values.append(format("\'{}\'").format(getattr(self, i)))
                else:
                    if i == 'id':
                        values.append('DEFAULT')
                    else:
                        values.append("null")

            insert_query = """INSERT INTO {0} ({1}) 
                              VALUES ({2})
                              RETURNING id;""".format(self._table_name,
                                                      ', '.join(object_fields),
                                                      ', '.join(values))
            cursor.execute(insert_query)
            connection.commit()

            self.id = cursor.fetchone()[0]

    class Meta:
        table_name = ''
