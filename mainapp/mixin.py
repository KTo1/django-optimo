from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, FormView
from django.views.generic.base import View, ContextMixin


class SuccessMessageMixin(FormView):
    success_message = ""

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class CustomDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CustomDispatchMixin, self).dispatch(request, *args, **kwargs)


class UserDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDispatchMixin, self).dispatch(request, *args, **kwargs)


class BaseClassContextMixin(ContextMixin):
    title = ''
    categories = []
    def get_context_data(self, **kwargs):
        contex = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        contex['title'] = self.title
        contex['categories'] = self.categories

        return contex


class BaseClassDeleteMixin(DeleteView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())