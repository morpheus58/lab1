from .models import expandedurl
from .forms import ExpandedUrlForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from lxml.html import fromstring
import requests

# Create your views here.
def urls_list(request):
    expandedurls = expandedurl.objects.all()
    return render(request, 'urlexpander/urls_list.html', {'expandedurls': expandedurls})

def urls_detail(request, pk):
    url = get_object_or_404(expandedurl, pk=pk)
    return render(request, 'urlexpander/urls_detail.html', {'expandedurl': url})
def url_new(request):
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST)
        if form.is_valid():
            eurl = form.save(commit=False)
            site = requests.get(eurl.short_url)
            eurl.http_status_code = site.status_code
            eurl.destination_url = site.url
            siteTree = fromstring(site.content)
            eurl.page_title = siteTree.findtext('.//title')
            eurl.save()
            return redirect('urlexpander.views.urls_detail', pk=eurl.pk)
    else:
        form = ExpandedUrlForm()
        return render(request, 'urlexpander/urls_edit.html', {'form': form})
def url_edit(request, pk):
    url = get_object_or_404(expandedurl, pk=pk)
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST, instance=url)
        if form.is_valid():
            url = form.save(commit=False)
            site = requests.get(url.short_url)
            url.http_status_code = site.status_code
            url.destination_url = site.url
            siteTree = fromstring(site.content)
            url.page_title = siteTree.findtext('.//title')
            url.save()
            return redirect('urlexpander.views.urls_detail', pk=url.pk)
    elif request.method == 'DELETE':
        expandedurl.objects.get(pk=pk).delete()
        return urls_list(request)
    else:
        form = ExpandedUrlForm(instance=url)
        return render(request, 'urlexpander/urls_edit.html', {'form': form})


#def delete_urls(request):
#   if request.method == 'GET':
