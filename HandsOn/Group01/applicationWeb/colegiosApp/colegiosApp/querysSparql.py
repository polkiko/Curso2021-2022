# Querys Sparql
import rdflib
from rdflib.plugins.sparql import prepareQuery


class Colegios:
    def __init__(self):
        self.tipoCentro = {'Todos': 1, 'Otros': 2, 'Educación Infantil': 'INFANTIL', 'Educación Primaria': 'PRIMARIA',
                           'Educación Secundaria': 'SECUNDARIA'}
        self.titCentro = {'Todos': 1, 'Privado': 2, 'Privado Concertado': 3, 'Público': 4,
                          'Público-Titularidad Privada': 5}

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
                    ?centro cap:idSchool ?name.      
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

        SELECT ?name ?tipoVia ?nomCalle ?numCalle
            WHERE{{
            ?centro cap:hasAddress ?calle.
            ?calle cap:hasNameAddress ?nomCalle.
            ?calle cap:hasType ?tipoVia.
            ?calle cap:hasNumber ?numCalle.
            ?centro cap:nameSchool ?name
               FILTER regex(?name , "{nombre}").
        }} LIMIT 50
        """
        gres = g.query(q)
        resultado = []

        for row in gres:
            auxDic = {'colegio': row[0]}
            auxCalle = row[1] + " " + row[2] + ", " + row[3]
            auxDic['calle'] = auxCalle
            resultado.append(auxDic)
        return resultado

    def nombreColAvanzada(self, tipo, titularidad, municipio, codigoPostal):
        tipoAux = self.tipoCentro.get(tipo)
        titAux = self.titCentro.get(titularidad)
        print(tipoAux, titAux, municipio, codigoPostal)

    def colegiosCoord(self):
        g = rdflib.Graph()

        g.parse("../../rdf/output-with-links.nt")

        q = """
        PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX  cap: <http://www.colegiosapp.org/ontology#>
        PREFIX  dbo: <http://dbpedia.org/ontology#>
        PREFIX  owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?id ?name ?x ?y
            WHERE{
            ?centro cap:idSchool ?id.
            ?centro cap:nameSchool ?name.
            ?centro cap:xCoordinate ?x.
            ?centro cap:yCoordinate ?y.
        } GROUP BY ?id LIMIT 50
        """
        gres = g.query(q)
        resultado = []
        for row in gres:
            idSchool = row[0].toPython()
            nombre = row[1].toPython()
            xCoord = row[2].toPython()
            yCoord = row[3].toPython()
            auxDic = {'idSchool': idSchool, 'name': nombre, 'xCoord': xCoord, 'yCoord': yCoord}
            resultado.append(auxDic)
        return resultado


aux = Colegios()
# aux.nombreColAvanzada('Educación Primaria','Privado', 'Madrid', '28027')
aux.colegiosCoord()
