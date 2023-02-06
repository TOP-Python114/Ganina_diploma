from django.shortcuts import render
from .forms import UserForm
from . import module


def index(request):
    return render(request, 'main/index.html')


def vacancy(request):
    text = ''
    submit_but = request.POST.get('submit')
    form = UserForm(request.POST or None)
    if form.is_valid():
        text = form.cleaned_data.get('text')
        rez = module.run(text)
        text = rez
    context = {'form': form, 'text': text, 'submit_but': submit_but}
    return render(request, 'main/vacancy.html', context)
