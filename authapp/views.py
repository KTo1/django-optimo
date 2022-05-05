from django.conf import settings
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth.views import LogoutView

# Create your views here.
from django.urls import reverse, reverse_lazy
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
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

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        form_profile = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.userprofile)
        if form.is_valid() and form_profile.is_valid():
            form.save()

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProfileTemplateView, self).get_context_data()
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)

        return context


class RegisterTemplateView(CreateView, BaseClassContextMixin):
    ''' view for user register'''

    model = User
    template_name = 'authapp/register.html'
    title = 'GeekShop - Регистрация'
    form_class = UserRegisterForm
    success_message = "Вы успешно зарегистрировались, вам на почту отправлено письмо с активацией."
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request, self.success_message)

        context = {'form' : form}
        return render(request, self.template_name, context)

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = 'Активация аккаунта GeekShop'
        message = f'Уважаемый {user.username}. \n Для подтверждения учетной записи перейдите по ссылке {settings.DOMAIN_NAME}{verify_link}'

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expires():
                user.activation_key = None
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(self, 'authapp/verification.html')

        except Exception as e:
            HttpResponseRedirect(reverse('index'))


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
            auth.login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return super(LoginTemplateView, self).form_valid(form)


class LogoutTemplateView(LogoutView):
    ''' view for user logout'''

    template_name = 'mainapp/index.html'
