from rest_framework import serializers

from models import UserCreditEarningHistory

class UserCreditEarningHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCreditEarningHistory
        fields = ('id','description','amount','datetime',)
