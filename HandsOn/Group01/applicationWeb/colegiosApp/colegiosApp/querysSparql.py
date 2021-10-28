# Querys Sparql
import rdflib
from rdflib.plugins.sparql import prepareQuery


class Colegios:

    def numColegios(self):
        g = rdflib.Graph()

        g.parse("../../rdf/output-with-links.nt")

        q = """
                PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX  cap: <http://www.colegiosapp.org/ontology#>
                PREFIX  dbo: <http://dbpedia.org/ontology#>
                PREFIX  owl: <http://www.w3.org/2002/07/owl#>

                SELECT (count(?centro) as ?c)
                    WHERE{
                    ?centro cap:nameSchool ?name.      
                }
                """
        gres = g.query(q)
        for row in gres:
            return row[0]

    def nombreColegio(self, nombre):
        g = rdflib.Graph()

        g.parse("../../rdf/output-with-links.nt")

        q = f"""
        PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX  cap: <http://www.colegiosapp.org/ontology#>
        PREFIX  dbo: <http://dbpedia.org/ontology#>
        PREFIX  owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?centro
            WHERE{{
            ?centro cap:nameSchool ?name
               FILTER regex(?name , "{nombre}").
        }} LIMIT 50
        """
        gres = g.query(q)
        resultado = []
        for row in gres:
            print(row[0])
            resultado.append(row[0])
        return resultado