from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=settings.DEFAULT_EMAIL_LENGTH,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
        )],
        required=True,
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=settings.DEFAULT_EMAIL_LENGTH,
        required=True,
    )
    username = serializers.CharField(
        max_length=settings.DEFAULT_USERNAME_LENGTH,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )],
        required=True,
    )

    def validate(self, attr):
        username = attr['username']
        if 'me' == username:
            raise serializers.ValidationError(
                f'Извините, имя пользователя "{username}" недоступно.'
            )
        return attr

    def validate_email(self, email):
        req_username = self.initial_data.get('username')
        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            if req_username != username:
                raise serializers.ValidationError(
                    f'Извините, email: {email} недоступно.')
        return email

    def validate_username(self, username):
        req_email = self.initial_data['email']
        if User.objects.filter(username=username).exists():
            email = User.objects.get(username=username).email
            if req_email != email:
                raise serializers.ValidationError(
                    f'Извините, имя пользователя {username} недоступно.')
        return username

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadOnlySerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title, author=request.user).exists():
                raise ValidationError('Можно оставить только один отзыв.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
