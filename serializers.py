from rest_framework import serializers
from courses_site.models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('is_admin', 'questionaire', 'user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ('preferences', 'rate', 'is_free', 'language', 'duration')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'category', 'source', 'provider', 'language', 'description')
