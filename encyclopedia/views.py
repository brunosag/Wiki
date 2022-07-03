from django.shortcuts import render

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
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })