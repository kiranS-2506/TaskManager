#this function for check user in which group
def is_admin(user):

    return user.is_authenticated and user.groups.filter(name='Admin').exists()


def is_user(user):

    return user.is_authenticated and user.groups.filter(name='User').exists()

