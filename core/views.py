import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt

from core.forms import ListForm, NewUserForm, ListEntryForm, AddContributorForm
from .models import List, ListEntry


# todo: apply sorting by creation date 
# to prevent same issues like with list entries
@csrf_exempt
def index(request):
    lists = List.objects.all()
    visited_count = request.session.get('visited_count', 0)
    request.session['visited_count'] = visited_count + 1

    if request.method == 'POST':  # todo add data to request in js - checkbox name
        req = json.loads(request.body)

        # handle updating checkbox state
        if req['action'] == 'update_checkbox':
            list_entry = get_object_or_404(ListEntry, pk=req['id'])
            list_entry.completed = True if req['completed'] else False
            list_entry.save()
            response = {
                'id': list_entry.id,
                'completed:': list_entry.completed
            }
            return JsonResponse(response)

    context = {
        'lists': lists,
        'visited_count': visited_count,
    }
    return render(request, 'core/index.html', context)


@csrf_exempt
def list_page(request, pk):
    alist = get_object_or_404(List, pk=pk)

    if request.method == 'POST':
        if 'add_entry' in request.POST:
            entry_form = ListEntryForm(request.POST)
            if entry_form.is_valid():
                list_entry = ListEntry()
                list_entry.entry_text = entry_form.cleaned_data['entry_text']
                list_entry.list = alist
                list_entry.date_created = datetime.now()
                list_entry.save()
                messages.success(request, "Entry added successfully.")
                return redirect(reverse('core:list_page', args=(pk,)))

        # handle adding contributors
        if 'add_contributor' in request.POST:
            add_contributor_form = AddContributorForm(request.POST)

            if add_contributor_form.is_valid():
                data = add_contributor_form.cleaned_data['contributor']
                alist.contributors.add(data)
                alist.save()
                messages.success(request,
                                 f"{data} successfully added as a contributor.")
                return redirect(reverse('core:list_page', args=(pk,)))

        req = json.loads(request.body)
        if req['action'] == 'edit_list_name':
            alist.list_name = req['list_name']
            alist.save()
            return JsonResponse({'list_name': alist.list_name})

        if req['action'] == 'edit_entry':
            entry = ListEntry.objects.get(pk=req['entry_id'])
            entry.entry_text = req['entry_text']
            entry.save()
            return JsonResponse({'entry_text': entry.entry_text})

        if req['action'] == 'delete_entry':
            entry = ListEntry.objects.get(pk=req['entry_id'])
            entry.delete()
            return JsonResponse({})

        if req['action'] == 'delete_contributor':
            print("here!")
            alist.contributors.remove(User.objects.get(pk=req['contributor_id']))
            return JsonResponse({})

    entry_form = ListEntryForm()
    add_contributor_form = AddContributorForm()
    excludes = [x.username for x in alist.contributors.all()]
    excludes.append(alist.owner.username)
    add_contributor_form.fields['contributor'].queryset = User.objects.all().exclude(username__in=excludes)

    context = {
        'entry_form': entry_form,
        'add_contributor_form': add_contributor_form,
        'alist': alist,
        'contributors': alist.contributors,
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

            list_entry = ListEntry()
            list_entry.entry_text = form.cleaned_data['entry_text']
            list_entry.list = alist
            list_entry.date_created = datetime.now()
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
    else:
        form = NewUserForm()

    return render(request, template_name="core/register.html", context={"register_form": form})
