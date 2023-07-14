from django.shortcuts import render
from django.utils.safestring import mark_safe
import markdown

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    result_search = markdown.markdown(util.get_entry(request.GET.get("q")))
    result_search = mark_safe(result_search)
    return render(request, 'encyclopedia/search.html', {
        "entry": result_search 
    })

def create_newpage(request):
    if request.method == 'POST':
        title = request.POST.get('title',"")
        text = request.POST.get('text',"")
        return render(request, 'encyclopedia/create_newpage.html', {
            'create_newpage': util.save_entry(title,text)
        })
    return render(request,'encyclopedia/create_newpage.html',)