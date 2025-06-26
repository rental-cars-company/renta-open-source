from decimal import Decimal
from typing import Tuple

from api.referral.models import ReferralInfo
from api.users.models import User
from common.constants import (
    BALANCE_FOR_NEW_REFERRAL,
    BALANCE_FOR_REGISTER_AS_REFERRAL,
)

from .decorators import no_referral_error_catch
from .exeptions import BadReferralCode


def register(user: User, referral_code: str | None):
    """Вызываем при регистрации нового пользователя
    При вызове передается код ПРИГЛАСИВШЕГО.
    """
    if referral_code is None:
        referral_info = ReferralInfo(user=user, balance=0)
    else:
        referral_info = ReferralInfo(
            user=user,
            used_referral_code=referral_code,
            balance=BALANCE_FOR_REGISTER_AS_REFERRAL,
        )
    referral_info.save()
    # --

    if referral_code is None:
        return

    ref = ReferralInfo.objects.filter(own_referral_code=referral_code).first()
    if ref is None:
        raise BadReferralCode

    ref.users_invited += 1
    ref.balance += BALANCE_FOR_NEW_REFERRAL
    ref.save()


@no_referral_error_catch
def referral_discounted_price(
    user: User, price: Decimal
) -> Tuple[Decimal, Decimal]:
    """Возвращает цену на аренду с учетом скидки с реферальной системы.
    Так же, вторым значением, возвращает остаток скидки.
    """
    ref_balance = user.referral.balance

    if price >= ref_balance:
        return price - ref_balance, Decimal(0)

    return Decimal(0), ref_balance - price


@no_referral_error_catch
def referral_set_balance(user: User, new_balance: Decimal):
    ref: ReferralInfo = user.referral
    ref.balance = new_balance
    ref.save()


@no_referral_error_catch
def get_user_ref_links(user: User) -> dict[str, str]:
    ref: ReferralInfo = user.referral
    return {"google-play": ref.own_referral_code}
