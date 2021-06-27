import json, string
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
                ?cantante rdf:type dbo:MusicalArtist;
                rdfs:label ?etiqueta .
                FILTER(REGEX(str(?etiqueta), """+'"'+cantante_insertado+'"'+""") && LANGMATCHES(LANG(?etiqueta), "en")) .
            }
        """)
            # UNION
            #     { ?cantante rdf:type dbo:Band;
            #     rdfs:label ?etiqueta .
            #     FILTER(REGEX(str(?etiqueta), """+'"'+cantante_insertado+'"'+""") && LANGMATCHES(LANG(?etiqueta), "en")) . }
        consulta.setReturnFormat(JSON)
        resultado = consulta.query().convert()
        lista = []
        for r in resultado["results"]["bindings"]:
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
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX dbp: <http://dbpedia.org/property/>

            SELECT ?nombreGenero ?info ?ocupacion ?nombreCancion
            WHERE {
                { dbr:"""+cantante_nombre+""" dbo:abstract ?info .
                FILTER (LANGMATCHES(LANG(?info ), "en")). }
            UNION
                { dbr:"""+cantante_nombre+""" dbp:genre ?genero .
                  ?genero dbp:name ?nombreGenero . }
            UNION
                { dbr:"""+cantante_nombre+""" dbp:occupation ?ocupacion . }
            UNION
                { ?canciones dbp:artist dbr:"""+cantante_nombre+""" ;
                    rdf:type dbo:Song ;
                    dbp:name ?nombreCancion. }
            }
        """)
        consulta.setReturnFormat(JSON)
        resultado = consulta.query().convert()
        datos = {}
        datos['nombreGenero'] = []
        datos['ocupacion'] = []
        datos['nombreCancion'] = []

        for r in resultado['results']['bindings']:
            print(r)
            for k, v in r.items():
                if k == 'info':
                    datos['info'] = v['value']
                if k == 'nombreGenero':
                    datos['nombreGenero'].append(v['value'])
                if k == 'ocupacion':
                    datos['ocupacion'].append(v['value'])
                if k == 'nombreCancion':
                    datos['nombreCancion'].append(v['value'])

        context['nombre'] = cantante_nombre
        context['resultado'] = json.dumps(datos)

        return context
