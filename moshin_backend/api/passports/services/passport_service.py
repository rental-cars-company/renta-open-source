from api.passports.models import Passport
from api.users.models import User


def get(user_owner: User) -> Passport | None:
    return Passport.objects.filter(user=user_owner).first()


def create_no_scan(
    user_owner: User, is_id_card: bool, image_file, image_file_back
) -> Passport:

    obj = Passport(
        user=user_owner,
        is_id_card=is_id_card,
        image_file=image_file,
        image_file_back=image_file_back,
    )

    obj.save()
    return obj
