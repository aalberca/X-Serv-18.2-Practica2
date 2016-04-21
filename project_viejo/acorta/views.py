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
        lista = Urls.objects.all()
    	# solo voy al csv si el diccionario esta vacio y si el fichero existe!
    	# if len(lista) == 0:
    	# 	if os.access("urls.csv", 0):
		#       	with open("urls.csv", "r") as fd:
		#       		reader = csv.reader(fd)
		#       		vacio = True
		#       		for row in reader:
		#       			vacio = False
		#       		if not vacio: #si no esta vacio tengo que pasar el csv al diccionario
		#       			csvAdicc("urls.csv")
        # print "HOLAAAAAA"
        # httpCode = "200 OK"
        # htmlBody = "<html><body>" \
        #             + '<form method="POST" action="">' \
        #             + 'URL: <input type="text" name="Url"><br>' \
        #             + '<input type="submit" value="Enviar">' \
        #             + '</form>' \
        #             + "<body></html>"
        # fd = open('/home/ana/Escritorio/SARO/X-Serv-18.2-Practica2/project/templates/formulario_inicio.html')
        # template = Template(fd.read())
        # print "TEMPLATEEEEEE " + str(template)
        # fd.close()

        template = get_template('formulario_inicio.html')
        return HttpResponse(template.render(Context({})))

    elif request.method == "POST":
        url = request.POST['url']
        print "URL REAL ES    " + str(url)
        if len(url) == 0:
            httpCode = "405 Method Not Allowed"
            htmlBody = "Go Away!"
        elif len(url) != 0:
            if urllib.unquote(url[0:13]) == "http://":
                url_real = "http://" + url[13:]
            elif urllib.unquote(url[0:14]) == "https://":
                url_real = "https://" + url[14:]
            else:
                url_real = "http://" + url
            print "URL REAL ES    " + str(url_real)
            lista = Urls.objects.all()
            if url_real in lista: # quiere decir que ya ha sido acortada, busco su valor en la lista
                print url_real + "SI ESTA EN URLS_REALES!!!"
                url_acortada = Urls.objects.get(larga = url_real)
                url_acortada = urls_acortada.id
            else: # si no esta en la lista significa que es nueva, la tengo que acortar y meterla a la lista
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
