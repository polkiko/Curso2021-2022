# Querys Sparql
import rdflib
from rdflib.plugins.sparql import prepareQuery


class Colegios:
    def __init__(self):
        self.tipoCentro = {'Todos': 1, 'Otros': 2, 'Educación Infantil': 'INFANTIL', 'Educación Primaria': 'PRIMARIA',
                           'Educación Secundaria': 'SECUNDARIA'}
        self.titCentro = {'Todos': 1, 'Privado': 'PRIVADO', 'Privado Concertado': 'PRIVADO CONCERTADO',
                          'Público': 'PÚBLICO', 'Público-Titularidad Privada': 'PÚBLICO-TITULARIDAD PRIVADA'}

    def nombreColegio(self, nombre, limite):
        g = rdflib.Graph()

        g.parse("../../rdf/output-with-links.nt")

        q = f"""
        PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX  cap: <http://www.colegiosapp.org/ontology#>
        PREFIX  dbo: <http://dbpedia.org/ontology#>
        PREFIX  owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?name ?tipoVia ?nomCalle ?numCalle ?x ?y
            WHERE{{
            ?centro cap:hasAddress ?calle.
            ?calle cap:hasNameAddress ?nomCalle.
            ?calle cap:hasType ?tipoVia.
            ?calle cap:hasNumber ?numCalle.
            ?centro cap:xCoordinate ?x.
            ?centro cap:yCoordinate ?y.
            ?centro cap:nameSchool ?name
               FILTER regex(?name , "{nombre}").
        }}  ORDER BY ?name LIMIT {limite}
        """
        gres = g.query(q)

        resultado = []
        for row in gres:
            auxDic = {'name': row[0],
                      'calle': row[1] + " " + row[2] + ", " + row[3],
                      'xCoord': float(row[4].toPython()),
                      'yCoord': float(row[5].toPython())
                      }
            resultado.append(auxDic)
        return resultado

    def nombreColAvanzada(self, tipo, titularidad, municipio, codigoPostal, limite):
        tipoAux = self.tipoCentro.get(tipo)
        titAux = self.titCentro.get(titularidad)
        print(tipoAux, titAux, municipio, codigoPostal)

        g = rdflib.Graph()
        g.parse("../../rdf/output-with-links.nt")
        qtit = ""
        qtipo = ""
        qmuni = ""
        qpost = ""
        if tipoAux != 1 and tipoAux != 2:
            qtipo = f"""?centro cap:hasTypeSchool ?tipo
                        FILTER regex(?tipo , "{tipoAux}").
                        """
        elif tipoAux == 2:
            qtipo = f"""?centro cap:hasTypeSchool ?tipo
                        FILTER (!regex(?tipo , "INFANTIL")).
                        ?centro cap:hasTypeSchool ?tipo
                        FILTER (!regex(?tipo , "PRIMARIA")).
                        ?centro cap:hasTypeSchool ?tipo
                        FILTER (!regex(?tipo , "SECUNDARIA")).
                        """
        if titAux != 1:
            qtit = f"""?centro cap:ownership ?tit
                        FILTER (?tit = "{titAux}").
                        """
        if municipio != "":
            qmuni = f"""?muni cap:hasNameMunicipality ?nomMuni
                       FILTER regex(?nomMuni , "{municipio}").
                        """
        if codigoPostal != "":
            qpost = f"""?calle cap:hasPostalCode ?postal
                        FILTER (?postal = "{codigoPostal}").
                        """
        qfinal = f"""
                PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX  cap: <http://www.colegiosapp.org/ontology#>
                PREFIX  dbo: <http://dbpedia.org/ontology#>
                PREFIX  owl: <http://www.w3.org/2002/07/owl#>

                SELECT ?name ?tipoVia ?nomCalle ?numCalle ?x ?y
                    WHERE{{
                    ?centro cap:idSchool ?id.
                    ?centro cap:hasAddress ?calle.
                    ?calle cap:hasNameAddress ?nomCalle.
                    ?calle cap:hasType ?tipoVia.
                    ?calle cap:hasNumber ?numCalle.
                    ?centro cap:xCoordinate ?x.
                    ?centro cap:yCoordinate ?y.
                    ?centro cap:nameSchool ?name.
                    ?centro cap:ownMunicipality ?muni.
                    """+ qmuni + qpost + qtipo + qtit + f"""}}
                GROUP BY ?id ORDER BY ?name LIMIT {limite}
                """
        gres = g.query(qfinal)
        resultado = []
        for row in gres:
            auxDic = {'name': row[0],
                      'calle': row[1] + " " + row[2] + ", " + row[3],
                      'xCoord': float(row[4].toPython()),
                      'yCoord': float(row[5].toPython())
                      }
            resultado.append(auxDic)
        return resultado

# aux = Colegios()
#aux.nombreColAvanzada('Educación Infantil', 'Privado', 'Madrid', '28027', 50)
# print(aux.nombreColAvanzada('Otros', 'Todos', 'Madrid', '', 50))