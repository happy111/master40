@prefix ex: <http://example.com/ontology/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ex:CommercialOntology
    a owl:Ontology ;
    rdfs:label "Commercial Domain Model" .

ex:Product
    a owl:Class ;
    rdfs:label "Product" .

ex:Customer
    a owl:Class ;
    rdfs:label "Customer" .

ex:Order
    a owl:Class ;
    rdfs:label "Order" .

ex:placesOrder
    a owl:ObjectProperty ;
    rdfs:domain ex:Customer ;
    rdfs:range ex:Order .

ex:containsProduct
    a owl:ObjectProperty ;
    rdfs:domain ex:Order ;
    rdfs:range ex:Product .
