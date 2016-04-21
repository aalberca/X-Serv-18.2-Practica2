from django.shortcuts import render
from django.http import HttpResponse
from models import Urls
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
# Create your views here.

import csv
import urllib
import os

@csrf_exempt
def acorta(request):

    if request.method == "GET":
        template = get_template('formulario_inicio.html')
        return HttpResponse(template.render(Context({})))

    elif request.method == "POST":
        url = request.POST['url']
        print "URL REAL ES    " + str(url)
        if len(url) == 0:
            httpCode = "405 Method Not Allowed"
            htmlBody = "Go Away!"
        elif len(url) != 0:
            if url[0:7] == "http://":
                url_real = url
            elif url[0:8] == "https://":
                url_real = url
            else:
                url_real = "http://" + url
            print "URL REAL ES    " + str(url_real)
            lista = Urls.objects.all()
            ya_acortada = False
            for elemento in lista:
                if elemento.larga == url_real: # quiere decir que ya ha sido acortada, busco su valor en la lista
                    print url_real + "SI ESTA EN URLS_REALES!!!"
                    url_acortada = Urls.objects.get(larga = url_real)
                    url_acortada = url_acortada.id
                    ya_acortada = True
            if ya_acortada == False: # si no esta en la lista significa que es nueva, la tengo que acortar y meterla a la lista
                nueva_url = Urls(larga = url_real)
                nueva_url.save()
                url_acortada = nueva_url.id


            template = get_template('plantilla_enlaces.html')
            return HttpResponse(template.render(Context({'url_acortada':url_acortada, 'url_real': url_real})))
    else:
        httpCode = "405 Method Not Allowed"
        htmlBody = "Go Away!"

    return HttpResponse(htmlBody)

def redireccion(request, numeroUrl):
    lista = Urls.objects.all()
    if numeroUrl in lista:
        url_real = Urls.objects.get(id = int(numeroUrl))

        #tengo que redirigir
        httpCode = "302 Found"
        htmlBody = "<html><head>" + '<meta http-equiv="refresh" content="0;url=' + url_real + '" />' + "</head></html>"
    else:
        httpCode = "404 Not Found"
        htmlBody = "Recurso no disponible"
    return HttpResponse(httpCode, htmlBody)
