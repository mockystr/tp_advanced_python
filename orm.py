from my_models import User
import datetime

if __name__ == '__main__':
    # user = User(name='name', )
    # user_obj = User.objects.get(id=1)
    # print(user_obj.name)
    print(
        User.objects.create(name='emir_name', age=150, date_added=datetime.datetime.now())
    )
    # print(user.__dict__)
    # print(User.objects.all())

    # User.objects.create(id=1, name='name')
    # User.objects.update(id=1)
    # User.objects.delete(id=1)
    #
    # User.objects.filter(id=2).filter(name='petya')
    #
    # user.name = '2'
    # user.save()
    # user.delete()
