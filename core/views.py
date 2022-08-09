import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from core.forms import ListForm, NewUserForm, ListEntryForm
from .models import List, ListEntry


@csrf_exempt
def index(request):
    lists = List.objects.all()

    visited_count = request.session.get('visited_count', 0)
    request.session['visited_count'] = visited_count + 1

    if request.method == 'POST':
        req = json.loads(request.body)
        print(f"request: {req}")
        obj = get_object_or_404(ListEntry, pk=req['id'])
        obj.completed = True if req['completed'] else False
        obj.save()
        response = {
            'id': obj.id,
            'completed:': obj.completed
        }
        print(f"response: {response}")
        return JsonResponse(response)

    context = {
        'lists': lists,
        'visited_count': visited_count,
    }
    return render(request, 'core/index.html', context)


def list_page(request, pk):
    alist = get_object_or_404(List, pk=pk)

    if request.method == 'POST':
        entry_form = ListEntryForm(request.POST)

        if entry_form.is_valid():
            list_entry = ListEntry()
            list_entry.entry_text = entry_form.cleaned_data['entry_text']
            list_entry.list = alist
            list_entry.save()
            messages.success(request, "Entry added successfully.")
            return redirect(reverse('core:list_page', args=(pk,)))
    else:
        entry_form = ListEntryForm()

    context = {
        'entry_form': entry_form,
        'alist': alist,
        'contributors': alist.contributors
    }
    return render(request, 'core/list.html', context)


@login_required
def add_list(request):
    page_title = "Add list"

    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            alist = List()
            alist.list_name = form.cleaned_data['list_name']
            alist.owner = request.user
            print(f"User: {alist.owner}")

            list_entry = ListEntry()
            list_entry.entry_text = form.cleaned_data['entry_text']
            list_entry.list = alist
            list_entry.completed = True

            alist.save()
            list_entry.save()
            # sometimes form was added twice, 'del form' was here to try to fix it
            messages.success(request, "List added successfully.")
            return redirect(reverse('core:list_page', args=(alist.pk,)))
    else:
        # first display of a form. fill it with initial data
        form = ListForm()

    return render(request, 'core/add_list.html', {'form': form, 'page_title': page_title})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('core:index')
        else:
            messages.error(request, "Information you have entered is invalid.")

    form = NewUserForm()
    return render(request, template_name="core/register.html", context={"register_form": form})
