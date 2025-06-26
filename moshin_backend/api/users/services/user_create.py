from api.users.models import USER_ROLE_ADMIN, User


def with_credentials(
    username: str, password: str, role: str = USER_ROLE_ADMIN
) -> User:

    user = User(
        username=username,
        phone=None,
        role=role,
        is_staff=bool(role == USER_ROLE_ADMIN),
    )

    user.set_password(password)
    user.save()
    return user


def renter(phone: str, **data) -> User:
    user = User(phone=phone, username=None, **data)
    user.save()
    return user
