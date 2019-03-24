from my_models import User, Man
import datetime

if __name__ == '__main__':

    # from itertools import combinations
    #
    # x = 'abcde'
    # for i in [*range(10), *[''.join(l) for i in range(len(x)) for l in combinations(x, i + 1)]]:
    #     User(name=i).save()
    # print(user.__dict__)
    # user.save()
    # user.coins = '228.98'
    # user.save()
    # print(user.coins)

    # print([i for i in User.objects.all()])
    # users = User.objects.all()
    # print(users.__dict__)
    p = User.objects.filter(name='a')[:5]
    print(p.__dict__)
    print([i for i in User.objects.filter()[:5]])
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

    # todo filter
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
