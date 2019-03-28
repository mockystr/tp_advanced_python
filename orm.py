from my_models import User, Man
import datetime
import random

# from itertools import combinations
# todo default values in insert

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

    man = Man(description='perfect gamer. registered in 2010',
              date_added=datetime.datetime.now(), age=18,
              coins=322, is_superuser=False,
              sex='male')
    man.name = 'mockystr'
    man.save()
    # man.date_added = None
    # man.save()
    print(man.__dict__)

    # print([i.age for i in User.objects.all()])

    # users = User.objects.all()
    # print(users.__dict__)

    # print([(i.id, i.name, i.age, i.coins) for i in User.objects.filter()[:10].order_by('-age')])
    # [print('\n', (i.name, i.age, i.coins)) for i in User.objects.filter(name='abe').order_by('-coins', 'age')]

    # p = User.objects.filter(name='abe')[:20].order_by('-coins')[1:3]
    # print([i.__dict__ for i in p])
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
    # qs = User.objects.filter(name__endswith='g').filter(id__le=2505)[:2]
    # print(qs.__dict__)
    # print([i for i in qs])
    # print(qs.__dict__)
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
