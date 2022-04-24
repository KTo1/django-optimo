from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from authapp.models import User


class Valid:
    description = ''

    @staticmethod
    def if_name_valid(name):
        if len(name) < 15:
            return True
        else:
            Valid.description = 'Имя пользователя д.б. меньше 15 символов'
            return False

    @staticmethod
    def if_image_valid(image):
        if isinstance(image, ImageFieldFile):
            width, height = image.width, image.height
        else:
            width, height = image.image.size

        if width < 300 and height < 300:
            return True

        Valid.description = 'Аватар д.б. размером не более чем 300х300 пикселей'
        return False


class UserLoginForm(AuthenticationForm):
    '''form for login'''

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_username(self):
        username = self.cleaned_data['username']

        if not Valid.if_name_valid(username):
            raise ValidationError(Valid.description)

        return username


class UserRegisterForm(UserCreationForm):
    '''form for register'''

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите почту'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_username(self):
        username = self.cleaned_data['username']

        if not Valid.if_name_valid(username):
            raise ValidationError(Valid.description)

        return username


class UserProfileForm(UserChangeForm):
    '''form for profile'''

    image = forms.ImageField(widget=forms.FileInput(), required=False)
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    def clean_username(self):
        username = self.cleaned_data['username']

        if not Valid.if_name_valid(username):
            raise ValidationError(Valid.description)

        return username

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image and not Valid.if_image_valid(image):
            raise ValidationError(Valid.description)

        return image