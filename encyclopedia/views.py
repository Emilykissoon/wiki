import random
from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.http import HttpResponse
from django import forms
from django.urls import reverse


from . import util


class Edit(forms.Form):
    content = forms.CharField(label="content")


class Create(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request, title):
    entries = util.list_entries()
    if title not in entries:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    else:
        entry = util.get_entry(title)
        markdowner = Markdown()
        html = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": html, "title": title
        })


def search(request):
    entry = request.GET.get("q", "")
    if entry:
        entries = util.list_entries()
        for ent in entries:
            if str.lower(entry) == str.lower(ent):
                entry = entry.capitalize()
                return get_entry(request, entry)
        else:
            # substring_entries = [i for i in entries if entry in i]
            substring_entries = []
            for ent in entries:
                if str.lower(entry) in str.lower(ent):
                    if str.lower(ent) not in substring_entries:
                        substring_entries.append(ent)
            return render(request, "encyclopedia/search.html", {
                "entries": substring_entries,
                "entry": entry
            })
    else:
        return index(request)


def create(request):
    if request.method == "POST":
        info = Create(request.POST)
        if info.is_valid():
            title = info.cleaned_data["title"]
            content = info.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "Page with this title already exists"
                })
            else:
                util.save_entry(title, content)
                return get_entry(request, title)
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Not Valid"
            })
    else:
        return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        form = Edit(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return get_entry(request, title)
    else:
        print(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })


def random_entry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return get_entry(request, title)
