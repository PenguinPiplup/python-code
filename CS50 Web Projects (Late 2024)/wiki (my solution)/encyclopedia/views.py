from django.shortcuts import render
from django import forms
import re
from random import choice
from markdown2 import Markdown

from . import util

class NewWebForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

class NewEditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_find(request, TITLE):
    TITLE_md = util.get_entry(TITLE)
    if TITLE_md == None:
        return render(request, "encyclopedia/error.html")
    
    return render(request, "encyclopedia/definition.html", {
        "TITLE": TITLE,
        "TITLE_md": Markdown().convert(TITLE_md)
    })

def search(request):
    entries = util.list_entries()
    query = request.POST.get("q")
    compiled_query = re.compile(query, re.I)

    if query in entries:
        return render(request, "encyclopedia/definition.html", {
            "TITLE": query,
            "TITLE_md": Markdown().convert(util.get_entry(query))
        })

    matches = []

    for entry in entries:
        if re.search(compiled_query, entry):
            matches.append(entry)
    
    return render(request, "encyclopedia/matches.html", {
        "query": query,
        "matches": matches
    })

def newpage(request):
    if request.method == "POST":
        inputform = NewWebForm(request.POST)

        if inputform.is_valid():
            title = inputform.cleaned_data["title"]
            content = inputform.cleaned_data["content"]

            # Check if encyclopedia entry already exists
            entries = util.list_entries()
            for entry in entries:
                if title.casefold() == entry.casefold():
                    return render(request, "encyclopedia/error2.html", {
                        "error_message":entry + " page already exists"
                    })
                
            # Save new webpage
            util.save_entry(title, content)

            # Redirect user to new entry's page
            return wiki_find(request, title)

        else:
            return render(request, "encyclopedia/newpage.html", {
                "form":inputform
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": NewWebForm()
    })

def editpage(request, TITLE):
    if request.method == "POST":
        inputform = NewEditForm(request.POST)

        if inputform.is_valid():
            content = inputform.cleaned_data["content"]
                
            # Save new webpage
            util.save_entry(TITLE, content)

            # Redirect user to new entry's page
            return wiki_find(request, TITLE)
        else:
            return render(request, "encyclopedia/editapage.html", {
                "form": inputform,
                "TITLE": TITLE
            })

    existing_content = util.get_entry(TITLE)
    return render(request, "encyclopedia/editapage.html", {
        "form": NewEditForm(initial={"content":existing_content}),
        "TITLE": TITLE
    })

def random(request):
    entries = util.list_entries()
    TITLE = choice(entries)
    return render(request, "encyclopedia/definition.html", {
        "TITLE": TITLE,
        "TITLE_md": Markdown().convert(util.get_entry(TITLE))
    })