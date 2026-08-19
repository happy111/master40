@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.com/ontology/> .

ex:ProductShape
    a sh:NodeShape ;
    sh:targetClass ex:Product ;
    sh:property [
        sh:path <http://www.w3.org/2000/01/rdf-schema#label> ;
        sh:minCount 1 ;
    ] .
