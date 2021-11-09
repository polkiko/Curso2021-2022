# Querys Sparql
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON

class Colegios:
    def __init__(self):
        self.tipoCentro = {'Todos': 1, 'Otros': 2, 'Educación Infantil': 'INFANTIL', 'Educación Primaria': 'PRIMARIA',
                           'Educación Secundaria': 'SECUNDARIA'}
        self.titCentro = {'Todos': 1, 'Privado': 'PRIVADO', 'Privado Concertado': 'PRIVADO CONCERTADO',
                          'Público': 'PÚBLICO', 'Público-Titularidad Privada': 'PÚBLICO-TITULARIDAD PRIVADA'}

    def nombreColegio(self, nombre):
        global auxDic
        g = rdflib.Graph()

        g.parse("../../rdf/output-with-links.nt")

        q = f"""
        PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX  cap: <http://www.colegiosapp.org/ontology#>
        PREFIX  dbo: <http://dbpedia.org/ontology#>
        PREFIX  owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?name ?tipoVia ?nomCalle ?numCalle ?x ?y ?wikidata ?nomMuni ?tipo ?tit ?cod ?url
            WHERE{{
            ?centro cap:hasAddress ?calle.
            ?calle cap:hasNameAddress ?nomCalle.
            ?calle cap:hasType ?tipoVia.
            ?calle cap:hasNumber ?numCalle.
            ?calle cap:hasPostalCode ?cod.
            ?centro cap:xCoordinate ?x.
            ?centro cap:yCoordinate ?y.
            ?centro cap:nameSchool ?name
                FILTER regex(?name , "{nombre}").
            ?centro cap:ownMunicipality ?muni.
            ?muni cap:hasNameMunicipality ?nomMuni.  
            ?muni owl:sameAs ?wikidata.
            ?centro cap:idSchool ?id.
            ?centro cap:hasTypeSchool ?tipo.
            ?centro cap:ownership ?tit.
            ?centro cap:urlSchool ?url.
        }}  GROUP BY ?id ORDER BY ?name
        """
        gres = g.query(q)

        resultado = []
        for row in gres:
            auxDic = self.completaRowAux(row)
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

                SELECT ?name ?tipoVia ?nomCalle ?numCalle ?x ?y ?wikidata ?nomMuni ?tipo ?tit ?postal ?url
                    WHERE{{
                    ?centro cap:idSchool ?id.
                    ?centro cap:hasAddress ?calle.
                    ?calle cap:hasNameAddress ?nomCalle.
                    ?calle cap:hasType ?tipoVia.
                    ?calle cap:hasNumber ?numCalle.
                    ?calle cap:hasPostalCode ?postal.
                    ?centro cap:xCoordinate ?x.
                    ?centro cap:yCoordinate ?y.
                    ?centro cap:nameSchool ?name.
                    ?centro cap:hasTypeSchool ?tipo.
                    ?centro cap:ownership ?tit.
                    ?centro cap:urlSchool ?url.
                    ?centro cap:ownMunicipality ?muni.
                    ?muni cap:hasNameMunicipality ?nomMuni.  
                    ?muni owl:sameAs ?wikidata.
                    """ + qmuni + qpost + qtipo + qtit + f"""}}
                GROUP BY ?id ORDER BY ?name LIMIT {limite}
                """
        gres = g.query(qfinal)
        resultado = []
        for row in gres:
            auxDic = self.completaRowAux(row)
            resultado.append(auxDic)
        return resultado

    def numeroPoblacion(self, municipio, sexo, edMin, edMax):
        numPobl = 0
        nomMuni = ''
        wikidata = ''
        area = 1
        resultado = []
        auxDic = {}
        result = self.buscarIntAux(edMin, edMax)
        arrMin = result[0]
        arrMax = result[1]
        qsexo = ""
        if sexo != "Ambos":
            qsexo = f"""?group cap:hasGender ?sexo
                        FILTER (?sexo = "{sexo}").
                        """
        var = 0
        for min, max in zip(arrMin, arrMax):
            g = rdflib.Graph()
            g.parse("../../rdf/output-with-links.nt")
            qfinal = f"""
                    PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX  cap: <http://www.colegiosapp.org/ontology#>
                    PREFIX  dbo: <http://dbpedia.org/ontology#>
                    PREFIX  owl: <http://www.w3.org/2002/07/owl#>
                    
                    SELECT ?pobl ?nameMuni ?wiki
                        WHERE{{
                            ?group cap:liveIn ?muni.
                            ?muni cap:hasNameMunicipality ?nameMuni
                                FILTER (?nameMuni = "{municipio}").
                            ?muni owl:sameAs ?wiki.
                            ?group cap:minAge ?min
                                FILTER (?min = "{min}"^^xsd:int).
                            ?group cap:maxAge ?max
                                FILTER (?max = "{max}"^^xsd:int).
                            ?group cap:numPeople ?pobl.
                            """ + qsexo + f"""}}
                    """
            gres = g.query(qfinal)

            for row in gres:
                nomMuni = row[1]
                numPobl = numPobl + int(row[0])
                wikidata = row[2]
                var = 1
        if var == 1:
            auxWiki = wikidata.replace("https://wikidata.org/entity/", "")
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

            sparql.setQuery(f"""
                        PREFIX wd: <http://www.wikidata.org/entity/>
                        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

                        SELECT ?coords ?area
                            WHERE {{
                                wd:{auxWiki} wdt:P625 ?coords.
                                wd:{auxWiki} wdt:P2046 ?area
                            }}
                        """)
            try:
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                coords = results['results']['bindings'][0]['coords']['value']
                coords = coords.replace('Point(', "")
                coords = coords.replace(')', "")
                x = ""
                for a in coords:
                    if a != " ":
                        x = x + a
                    else:
                        break
                coords = coords.replace(x + " ", "")
                y = coords
                auxDic['xCoord'] = x
                auxDic['yCoord'] = y
                area = results['results']['bindings'][0]['area']['value']
                auxDic['area'] = area
            except:
                print(Exception)

            auxDic['densidad'] = '{:.2f}'.format(numPobl / float(area))
            auxDic['numPobl'] = numPobl
            auxDic['nomMuni'] = nomMuni
            auxDic['sexo'] = sexo
            auxDic['edad'] = f"{edMin} a {edMax}"
            resultado.append(auxDic)
        return resultado

    def buscarIntAux(self, min, max):
        min = int(min)
        max = int(max)
        x = min
        y = max
        arrMin = []
        arrMax = []
        while x < max:
            arrMin.append(x)
            x = x + 5
        while y > min:
            arrMax.insert(0, y)
            y = y - 5
        return [arrMin, arrMax]

    def completaRowAux(self, row):

        # En caso de que la url no comience por http. Ej: www.losabetitos.com

        httpUrl = row[11].toPython()

        if not "https://" or not "http://" in httpUrl:
            httpUrl = ''.join(("https://", httpUrl))

        auxDic = {'name': row[0],
                  'calle': row[1] + " " + row[2] + ", " + row[3],
                  'xCoord': float(row[4].toPython()),
                  'yCoord': float(row[5].toPython()),
                  'municipio': row[7],
                  'tipo': row[8],
                  'titula': row[9],
                  'codPost': row[10],
                  'url': httpUrl
                  }
        aux = row[6].replace("https://wikidata.org/entity/", "")
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

        sparql.setQuery(f"""
                        PREFIX wd: <http://www.wikidata.org/entity/>
                        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

                        SELECT ?flag
                            WHERE {{
                                wd:{aux} wdt:P41 ?flag
                            }}
                        """)
        try:
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            svg = results['results']['bindings'][0]['flag']['value']
            auxDic['svg'] = svg
        except:
            print(Exception)
        return auxDic