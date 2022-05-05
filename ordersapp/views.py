from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView


class OrderList(ListView):
    pass


class OrderCreate(CreateView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderRead(DetailView):
    pass


class OrderDelete(DeleteView):
    pass


def order_forming_complited(requets, pk):
    pass