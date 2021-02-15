from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import youtube_dl
from .forms import DownloadForm

def sendurl(request):

    form = DownloadForm(request.POST or None)
    if form.is_valid():
        video_url = form.cleaned_data.get('url')
        if 'm.' in video_url:
            video_url = video_url.replace(u'm.', u'')
        elif 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
            video_url = 'https://www.youtube.com/watch?v=' + video_id
        if len(video_url.split("=")[-1]) != 11:
            return HttpResponse('Enter correct url.')
        
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(video_url, download=False) 
            formats = meta.get('formats', [meta])
        # for f in formats:
        #     print(f)
        print(type(formats[0]))
        return render(request, 'formatlist.html', {'formats': formats, 'form': form})

    

def home(request):
    form = DownloadForm(request.POST or None)
    return render(request, 'index.html', {'form': form})