from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(entry)
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

def search(request):
    query = request.GET["q"]
    entries = util.list_entries()
    if query in entries:
        return redirect("wiki/" + query)
    results = [entry for entry in entries if query in entry]
    return render(request, "encyclopedia/search.html", {
        "results": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title in util.list_entries():
            messages.error(request, "An encyclopedia entry already exists with the provided title.")
            return render(request, "encyclopedia/new_page.html", {
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect("wiki/" + title)
    return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if not util.get_entry(title):
        return redirect(reverse("entry", args=[title]))
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect(reverse("entry", args=[title]))
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })