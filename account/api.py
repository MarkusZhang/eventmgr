from models import UserProfile,UserCreditEarningHistory

def add_user_credit_earning(user,description,amount):
    # update credit
    profile=UserProfile.objects.get(user=user)
    profile.credit=profile.credit+amount
    profile.save()
    # add history
    UserCreditEarningHistory.objects.create(
        user = profile,
        description=description,
        amount=amount,
    )