from my_models import User, Man
import datetime
import random

# from itertools import combinations

if __name__ == '__main__':
    print()
    # x = 'abcdefg'
    # for i,k in zip(range(50), [''.join(l) for i in range(len(x)) for l in combinations(x, i + 1)]):
    #     User(name=k, age=random.randint(-i, i), coins=random.randint(0, i*100)).save()

    # user = User.objects.get(id=2528)
    # print(user.__dict__)
    # user.name = 'new_name'
    # print(user.__dict__)
    # user.save()

    # man = User.objects.create(name='asd', description='perfect gamer. registered in 2010',
    #                           date_added=[2010, 12, 12], age=18,
    #                           coins=322, is_superuser=False)
    # print(man.__dict__)
    # man.save()
    # man.date_added = {'year': 2012, 'month': 10, 'day': 5}
    # man.save()

    # man = Man(description='perfect gamer. registered in 2010',
    #           date_added=datetime.datetime.now(), age=18,
    #           coins=322, is_superuser=False,
    #           sex='male')
    # man.name = 'mockystr'
    # man.save()
    # man.date_added = None
    # man.save()
    # print(man.__dict__)

    # print([i.age for i in User.objects.all()])

    # users = User.objects.all()
    # print(users.__dict__)

    # print([(i.id, i.name, i.age, i.coins) for i in User.objects.filter()[:10].order_by('-age')])
    # [print('\n', (i.name, i.age, i.coins)) for i in User.objects.filter(name='abe').order_by('-coins', 'age')]

    # p = User.objects.filter(name__startswith='e')[:20].order_by('-name')
    # print([i for i in p])
    # print(p.count())

    # print([i for i in User.objects.all().filter(name__startswith='e').order_by('-name').
    #       order_by('description').order_by('coins')])

    # print(User.objects.all()[:25].filter(age__ge=-15)[20:].filter()[:10].count())

    # print([i for i in User.objects.all()[5]])

    # user_obj = User.objects.get(id=2538)
    # print(user_obj.__dict__)
    # user_obj.name = 'new_edit_after_get'
    # user_obj.save()

    # user_obj = User.objects.get(name__startswith='e')

    # print([i for i in User.objects.filter(name__in='ef')])
    # print([i for i in User.objects.filter(id__le=2500)])
    # qs = User.objects.filter(name__endswith='g').filter(id__le=2505)[:20]
    # print(qs.__dict__)
    # print([i for i in qs])
    # print(qs.count())

    # user_obj = User.objects.create(name='emir_name', age=150, date_added=datetime.datetime.now(),
    #                                description='im',
    #                                coins=123.3)
    # user_obj.delete()
    #
    # print(user_obj.coins)

    # print(User.objects.get(id=106).coins)
    # user = User(name='i', date_added={'year': 2010, 'day': 10, 'month': 10})
    # user.save()
    # user.date_added = [2010, 12, 12]
    # user.save()
    # print(user.__dict__)

    # print([i for i in User.objects.filter(name__startswith='e').order_by('-name')])
    # print(User.objects.filter(name__startswith='e').order_by('-name')[2])

    # update_int = User.objects.filter(name__startswith='3', age__ge=0).order_by('-name')[:5].update(description='new_52')
    # print(update_int)

    # delete_int = User.objects.filter(name__startswith='b').order_by('-name')[:7].delete()
    # print(delete_int)
    # print([i for i in User.objects.filter(name__startswith='b').order_by('-name')[:7]])

    """sql injections check"""
    # print([i for i in User.objects.filter(name='\' or 1=1')])
    # SELECT * FROM ormtable WHERE name=''' or 1=1' ORDER BY name NULLS FIRST

    # print([i for i in User.objects.filter(age__lt='5 or 1=1')])
    # psycopg2.DataError: invalid input syntax for integer: "5 or 1=1"
    # LINE 1: SELECT * FROM ormtable WHERE age < '5 or 1=1' ORDER BY name ...

    # print([i for i in User.objects.filter(name__in=['a', ') SELECT * from ormtable;'])])
    # SELECT * FROM ormtable WHERE name IN ('a', ') SELECT * from ormtable;') ORDER BY name NULLS FIRST
    # print([i for i in User.objects.filter(name__contains='a %\' or 1=1')])
    # SELECT * FROM ormtable WHERE name LIKE '%a %'' or 1=1%' ESCAPE '\' ORDER BY name NULLS FIRST

    from model import connection, cursor
    # query = 'SELECT * from ormtable where name=%s order by name DESC'
    # cursor.execute(query, ('\' or 1=1', ))
    # print(cursor.fetchall())
    # print(cursor.query)
    # cursor.execute()

    from psycopg2 import sql

    #
    # q = 'SELECT * from %s where name=%s order by name DESC'
    #
    # cursor.execute(q, ("ormtable", 1))
    # print(cursor.fetchall())

    # r = cursor.execute('INSERT INTO %s (name,date_added) VALUES (%s, %s);',
    #                    ('ormtable', 'O rehly', datetime.date(2005, 11, 18)))
    # print(cursor.query)
    # print(sql.SQL('SELECT * from ormtable where name={}').format(sql.Identifier('\'')).as_string(connection))
    #
    # select_get_query = sql.SQL("SELECT * FROM {0} WHERE {1};").format(sql.Identifier('ormtable'),
    #                                                                   sql.SQL(' AND ').join(
    #                                                                       map(sql.Identifier, ['name=\''])))
    # cursor.execute(select_get_query)
    # res = cursor.fetchall()
    # print(res)

    # sql_query = 'SELECT * FROM %s'
    # cursor.execute(sql_query, (str(input()),))
