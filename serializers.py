from rest_framework import serializers
from financeapp.models import *

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class AccountSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        account = Account.objects.create(user=validated_data['user'], limit=validated_data['limit'])
        return account


    class Meta:
        model = Account
        fields = ('user', 'limit')


class OutcomesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        outcomes = Outcomes.objects.create(user=validated_data['user'], type=validated_data['type'],
                                           date=validated_data['date'], amount=validated_data['amount'])
        return outcomes

    class Meta:
        model = Outcomes
        fields = ('user', 'type', 'date', 'amount')


class OutcomesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeType
        fields = ('type', 'id')
