import json, string
from bs4 import BeautifulSoup
from helium import *
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from SPARQLWrapper import SPARQLWrapper, JSON
from .forms import BuscarCantanteForm


class InicioView(TemplateView):
    template_name = 'base/inicio.html'

class BuscarCantantesView(FormView):
    template_name = 'base/buscar_cantantes.html'
    form_class = BuscarCantanteForm

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(request=self.request, form=form)
        cantante_insertado = string.capwords(form.cleaned_data.get('cantante'))
        consulta = SPARQLWrapper("http://dbpedia.org/sparql")
        consulta.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dbp: <http://dbpedia.org/property/>

            SELECT DISTINCT ?etiqueta
            WHERE {
                { ?cantante rdf:type dbo:MusicalArtist;
                   rdfs:label ?etiqueta .
                   FILTER(REGEX(str(?etiqueta), """+'"'+cantante_insertado+'"'+""") && LANGMATCHES(LANG(?etiqueta), "en")) . }
                UNION
                { ?cantante rdf:type dbo:Band;
                   rdfs:label ?etiqueta .
                   FILTER(REGEX(str(?etiqueta), """+'"'+cantante_insertado+'"'+""") && LANGMATCHES(LANG(?etiqueta), "en")) . }
            }
        """)
        consulta.setReturnFormat(JSON)
        resultado = consulta.query().convert()
        lista = []
        for r in resultado["results"]["bindings"]:
            if 'song)' not in r["etiqueta"]["value"]:
                lista.append(r["etiqueta"]["value"])
        context['resultado'] = json.dumps(lista)
        return self.render_to_response(context)

class PerfilCantanteView(TemplateView):
    template_name = 'base/perfil_cantante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cantante_nombre = kwargs['cantante_nombre']
        consulta = SPARQLWrapper("http://dbpedia.org/sparql")
        consulta.setQuery("""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbp: <http://dbpedia.org/property/>

            SELECT ?nombreGenero ?info ?nombreOcupacion ?pagWeb ?nombreNominacion ?infoNominacion ?nombreCancion
            WHERE {
                { <http://dbpedia.org/resource/"""+cantante_nombre+"""> dbo:abstract ?info .
                   FILTER (LANGMATCHES(LANG(?info ), "en")). }
            UNION
                { <http://dbpedia.org/resource/"""+cantante_nombre+"""> dbo:genre ?genero .
                   ?genero rdfs:label ?nombreGenero .
                   FILTER (LANGMATCHES(LANG(?nombreGenero ), "en")) .}
            UNION
                { <http://dbpedia.org/resource/"""+cantante_nombre+"""> dbp:occupation ?nombreOcupacion . }
            UNION
                { <http://dbpedia.org/resource/"""+cantante_nombre+"""> foaf:homepage ?pagWeb . }
            UNION
                { ?nominacion dbp:mostNominations <http://dbpedia.org/resource/"""+cantante_nombre+"""> ;
                   rdfs:label ?nombreNominacion ;
                   dbo:abstract ?infoNominacion .
                   FILTER (LANGMATCHES(LANG(?infoNominacion), "en") && LANGMATCHES(LANG(?nombreNominacion), "en")) .}
            UNION
                { ?canciones dbp:artist <http://dbpedia.org/resource/"""+cantante_nombre+"""> ;
                   rdf:type dbo:Song ;
                   rdfs:label ?nombreCancion .
                   FILTER (LANGMATCHES(LANG(?nombreCancion), "en")) . }
            }
        """)
        # { <http://dbpedia.org/resource/"""+cantante_nombre+"""> dbp:occupation ?ocupacion .
        #           ?ocupacion rdfs:label ?nombreOcupacion .
        #            FILTER (LANGMATCHES(LANG(?nombreOcupacion ), "en")) . }
        consulta.setReturnFormat(JSON)
        resultado = consulta.query().convert()
        datos = {}
        datos['nombreGenero'] = []
        datos['nombreOcupacion'] = []
        datos['nominaciones'] = {}
        datos['nominaciones']['nombre'] = []
        datos['nominaciones']['info'] = []
        datos['nombreCancion'] = []

        for r in resultado['results']['bindings']:
            for k, v in r.items():
                if k == 'nombreGenero':
                    datos['nombreGenero'].append(v['value'])
                if k == 'info':
                    datos['info'] = v['value']
                if k == 'nombreOcupacion':
                    datos['nombreOcupacion'].append(v['value'])
                if k == 'pagWeb':
                    datos['pagWeb'] = v['value']
                if k == 'nombreNominacion':
                    datos['nominaciones']['nombre'].append(v['value'])
                if k == 'infoNominacion':
                    datos['nominaciones']['info'].append(v['value'])
                if k == 'nombreCancion':
                    datos['nombreCancion'].append(v['value'])

        context['nombre'] = cantante_nombre
        context['resultado'] = json.dumps(datos)
        context['img_cantante'] = obtener_imagen(cantante_nombre)

        return context


def obtener_imagen(nombre):
    url = 'https://www.gettyimages.es/editorial-images'
    browser = start_chrome(url, headless=True)
    nombre = nombre.replace("_", " ")
    print(nombre)
    write(nombre, into="Busca las mejores fotos editoriales")
    press(ENTER)

    pagina_buscador = BeautifulSoup(browser.page_source, "lxml")
    url_resultado = pagina_buscador.find("div", class_="search-content__gallery-assets").find("div", class_="gallery-mosaic-asset").find("article", class_="gallery-mosaic-asset__container").a.get('href')

    go_to("https://www.gettyimages.es"+url_resultado)
    pagina_resultado = BeautifulSoup(browser.page_source, "lxml")
    img_url = pagina_resultado.find("img", class_="asset-card__image").get('src')
    print(img_url)

    return img_url