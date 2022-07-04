from django.shortcuts import render, redirect

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