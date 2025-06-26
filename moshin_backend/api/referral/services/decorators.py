from .exeptions import NoReferralError


def no_referral_error_catch(function):
    def wrapper(user, *args, **kwargs):
        try:
            return function(user, *args, **kwargs)
        except user.__class__.referral.RelatedObjectDoesNotExist:
            raise NoReferralError

    return wrapper
