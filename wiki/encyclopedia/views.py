from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.urls import reverse
import markdown
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request, title=""):
    title = title
    if not title:
        return redirect('index')
    
    entries = util.list_entries()

    search_title = title in entries
    
    if not search_title or search_title is None:
        return redirect(not_found)

    
    result_search = markdown.markdown(util.get_entry(title))
    result_search = mark_safe(result_search)
    
    return render(request, 'encyclopedia/search.html', {
                "entry": result_search,
                "title": title,
        })

def search_title(request, title):
    title =  request.GET.get('title',"")
    if not title:
        return redirect('index')
    return redirect('search', title = title)
    


def not_found(request):
     title = "Not Found!"
     text = "Sorry, not found !!!"
     return render(request, 'encyclopedia/not_found.html', {
                "entry": text,
                "title": title,
        })

def create_newpage(request):
    list_title = util.list_entries()
    title = request.POST.get('title',"")
    result = title in list_title
    if request.method == 'POST' and result == False and title != "":
        title = request.POST.get('title',"")
        text = request.POST.get('text',"")
        messages.success(request, 'New page successfully created!')
        return render(request, 'encyclopedia/create_newpage.html', {
            'create_newpage': util.save_entry(title,text)
        })
    else:
        if result == True:
            error = "Error, invalid title!"
            return render(request, 'encyclopedia/create_newpage.html', {'error_input': error})
    
    
    return render(request,'encyclopedia/create_newpage.html')


def search_random(request):
    title = random.choice(util.list_entries())
    return redirect('search', title = title)

def edit_page(request):
   if request.method == 'GET':
        title = request.POST.get('title',"")
        text = request.POST.get('text',"")
        messages.success(request, 'New page successfully created!')
        util.save_entry(title,text)
        return redirect('search', title=title)
   else:
        title = request.GET.get('title', '')
        result_search = util.get_entry(title)
        return render(request, 'encyclopedia/edit_page.html', {
                        "title_editvalue": title,
                        "text_editvalue": result_search,
                        })
