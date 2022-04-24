from django.contrib import auth
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth.views import LogoutView

# Create your views here.
from django.urls import reverse, reverse_lazy
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User
from basketapp.models import Basket
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin, SuccessMessageMixin


class ProfileTemplateView(UpdateView, SuccessMessageMixin, BaseClassContextMixin, UserDispatchMixin):
    ''' view for user profile'''

    model = User
    template_name = 'authapp/profile.html'
    title = 'GeekShop - Профиль'
    form_class = UserProfileForm
    success_message = 'Данные успешно сохранены.'

    def get_success_url(self):
        return reverse_lazy('authapp:profile', kwargs={'pk': self.request.user.id})

    def get(self, request, *args, **kwargs):
        self.baskets = Basket.objects.filter(user=request.user)
        return super().get(request, *args, **kwargs)


class RegisterTemplateView(CreateView, SuccessMessageMixin, BaseClassContextMixin):
    ''' view for user register'''

    model = User
    template_name = 'authapp/register.html'
    title = 'GeekShop - Регистрация'
    form_class = UserRegisterForm
    success_message = "Вы успешно зарегистрировались, можете войти на сайт используя свой логин и пароль."
    success_url = reverse_lazy('authapp:login')


class LoginTemplateView(FormView, BaseClassContextMixin):
    ''' view for user login'''

    model = User
    template_name = 'authapp/login.html'
    title = 'GeekShop - Вход'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user.is_active:
            auth.login(self.request, user)

        return super(LoginTemplateView, self).form_valid(form)


class LogoutTemplateView(LogoutView):
    ''' view for user logout'''

    template_name = 'mainapp/index.html'



