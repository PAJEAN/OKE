# OKE - Open Knowledge Extraction.

Author:
 + Pierre-Antoine Jean
 
Co-authors:
 + Sebastien Harispe
 + Sylvie Ranwez
 + Patrice Bellot
 + Jacky Montmain

OKE (Open Knowledge Extraction) allows to infer new relations from extracted relations. It is based on a syntactic and taxonomic implications and a set of rules to make a partial order on relations. This last one allows to compute criterias on relations (belief and specificity) to evaluate relevant relations through selection models.

#### Dependences ####
OKE requires:
 + Python 2.7
 + CGI librairies (BaseHTTPServer et CGIHTTPServer)
 + pywsd: https://github.com/alvations/pywsd

#### Folders ####
  + Data
    
    +Relations -- predicate(suj, obj) --
      
      + Predicats: You need to disinguish your relations with predicates. Each predicate has its own file. Format --> #ID\tSuj_wsd\tObj_wsd\tSuj\tObj with suj_wsd disambiguised suject of the relation (resp. obj_wsd) and suj the subject of the relation (resp. obj).
    
    + Phrases: This folder has two main files. id_phrases.txt indexes your sentences --> #ID\tsentence1\r and sources.reverb indexes sources of your sentences --> #ID\tSource1|Source2\r. Finally, you have to use sources.py to count the support of each relation.
  
  + CSS (Boostraps)

#### Run ####
 + python run_server.py
 + localhost:8888/index.py

#### Reference ####
 + Jean, P. A., Harispe, S., Ranwez, S., Bellot, P., & Montmain, J. (2017). Étude d'un modèle d'inférence de connaissances à partir de textes. In CORIA (pp. 201-217).

