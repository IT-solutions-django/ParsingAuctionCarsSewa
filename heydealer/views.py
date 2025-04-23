from django.shortcuts import render
from django.http import HttpResponse
from heydealer.utils.parsing import main


def start_parsing(request):
    main()
    return HttpResponse('Парсинг начался')

