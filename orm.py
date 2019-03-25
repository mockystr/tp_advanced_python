from my_models import User, Man
import datetime
import random

if __name__ == '__main__':
    # from itertools import combinations
    #
    # x = 'abcdefg'
    # for i,k in zip(range(50), [''.join(l) for i in range(len(x)) for l in combinations(x, i + 1)]):
    #     User(name=k, age=random.randint(-i, i), coins=random.randint(0, i*100)).save()

    # print(user.__dict__)
    # user.save()
    # user.coins = '228.98'
    # user.save()
    # print(user.coins)

    print([i.age for i in User.objects.all()])
    # users = User.objects.all()
    # print(users.__dict__)
    # print(User.objects.filter()[:10].__dict__)
    # print([(i.id, i.name, i.age, i.coins) for i in User.objects.filter()[:10].order_by('-age')])
    print([i.name for i in User.objects.filter(name='abe').filter(age=2)])
    # print([(i.age, i.coins) for i in User.objects.filter()[:10].order_by('coins')])

    # print([i for i in User.objects.filter()[:5]])
    # user_obj = User.objects.get(id=300)
    # print(user_obj)

    # user_obj = User.objects.create(name='emir_name', age=150, date_added=datetime.datetime.now(),
    #                                description='im',
    #                                coins=123.3)
    # user_obj.delete()
    #
    # print(user_obj.coins)

    # print(User.objects.get(id=106).coins)
    # print(User.objects.create())

    #
    # User.objects.create(id=1, name='name')
    #

    # user.name = '2'
    # user.save()
    # user.delete()

    # User.objects.filter(id=2).filter(name='petya')

    # m = Man(name='emir', sex='female', age=15)
    #
    # print(m.__dict__)
    #
    # m.name = 'emir'
    # m.sex = 'male'
    # m.age = 15
    # m.save()
    #
    # m = Man.objects.create(name='emir', sex='female', age=18)
    #
    # print(m.__dict__)
    #
    # print(Man.objects.filter(name='1'))
