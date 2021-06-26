import json
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
        cantante_insertado = form.cleaned_data.get('cantante').capitalize()
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT DISTINCT *
            WHERE {
            ?x rdf:type dbo:MusicalArtist;
            rdfs:label ?label.
            FILTER(REGEX(str(?label), """+'"'+cantante_insertado+'"'+""") && LANGMATCHES(LANG(?label), "es")).
            }
        """)
        sparql.setReturnFormat(JSON)
        resultado = sparql.query().convert()
        lista = []
        for r in resultado["results"]["bindings"]:
            lista.append(r["label"]["value"])
        context['resultado'] = json.dumps(lista)
        return self.render_to_response(context)

class PerfilCantanteView(TemplateView):
    template_name = 'base/perfil_cantante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cantante_nombre = kwargs['cantante_nombre']
        context['nombre'] = cantante_nombre
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            PREFIX dbr: <http://dbpedia.org/resource/>

            SELECT ?property ?hasValue ?isValueOf
            WHERE {
            { dbr:"""+cantante_nombre+""" ?property ?hasValue }
            UNION
            { ?isValueOf ?property dbr:"""+cantante_nombre+""" }
            }
        """)
        sparql.setReturnFormat(JSON)
        resultado = sparql.query().convert()
        lista = []
        for r in resultado["results"]["bindings"]:
            if "abstract" in r["property"]["value"]:
                if r["hasValue"]["xml:lang"] == 'es':
                    lista.append(r["hasValue"]["value"])
            if "property/genre" in r["property"]["value"]:
                lista.append(r["hasValue"]["value"])
        context['resultado'] = json.dumps(lista)
        return context

