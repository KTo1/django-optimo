import hashlib
import random

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile

from actionsapp.models import Action
from authapp.models import User
from mainapp.models import Products, ProductCategories
from django import forms

from ordersapp.models import Order


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


class UserAdminRegisterForm(UserCreationForm):
    '''form for admin register user'''

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите почту'
        self.fields['image'].widget.attrs['placeholder'] = 'Выберите фотографию'
        self.fields['age'].widget.attrs['placeholder'] = 'Укажите возраст'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    def save(self, commit=True):
        user = super(UserAdminRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.Random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']

        if not Valid.if_name_valid(username):
            raise ValidationError(Valid.description)

        return username


class UserAdminProfileForm(UserChangeForm):
    '''form for admin profile user'''

    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
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


class UserAdminOrderForm(forms.ModelForm):
    '''form for admin order detail'''

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserAdminOrderForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserAdminCategoryForm(forms.ModelForm):
    '''form for admin category'''

    class Meta:
        model = ProductCategories
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(UserAdminCategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProductForm(forms.ModelForm):
    '''form for admin product'''

    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Products
        fields = ('name', 'category', 'description', 'basic_price' ,'price', 'quantity', 'image')

    def __init__(self, *args, **kwargs):
        super(UserAdminProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['category'].widget.attrs['placeholder'] = 'Категория'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание'
        self.fields['basic_price'].widget.attrs['placeholder'] = 'Базовая цена'
        self.fields['price'].widget.attrs['placeholder'] = 'Цена'
        self.fields['price'].required = False
        self.fields['quantity'].widget.attrs['placeholder'] = 'Количество'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
        self.fields['category'].widget.attrs['class'] = 'form-control'


class UserAdminActionForm(forms.ModelForm):
    '''form for admin category'''

    class Meta:
        model = Action
        fields = ('name', 'category', 'percent')

    def __init__(self, *args, **kwargs):
        super(UserAdminActionForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Имя'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['category'].widget.attrs['class'] = 'form-control'