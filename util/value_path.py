"""

"""
# Original https://www.jusbrasil.com.br/jurisprudencia/busca?q=lei&idtopico=T10000003&idtopico=T10000008&o=data&dateFrom=2020-10-01&dateTo=2020-10-02T23%3A59%3A59

# BASE_URL_JUSBRASIL = "https://www.jusbrasil.com.br/jurisprudencia/busca?q=ementa" \
#                      "&idtopico=T10000003&idtopico=T10000008&o=data&" \
#                      "dateFrom=@dateFrom&dateTo=@dateToT23%3A59%3A59"

BASE_URL_JUSBRASIL = "https://www.jusbrasil.com.br/jurisprudencia/busca?q=ementa&p=@page&" \
                     "@id_topico&o=data&dateFrom=@dateFrom&dateTo=@dateToT23%3A59%3A59"

TOPICOS_COURTS = [
    10000001,  # STF
    #10000002,  # STJ
    #10000003,  # TSE
    #10000004,  # TST
    #10000010   # TJ's (Todos de uma vez

]

EMENTA_CLASS = "unprintable"

########################
# STF
########################
BASE_URL_STF = "https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&pesquisa_inteiro_teor=false" \
               "&sinonimo=true&plural=true&radicais=false&buscaExata=true&julgamento_data=@dateFrom-@dateTo" \
               "&page=@page&pageSize=@items_per_page&queryString=a%3F%20ou%20lei%3F%20ou%20ementa%3F%20ou%20relator%3F%20ou%20tribuna%3F" \
               "&sort=date&sortBy=desc"

XPATH_PROC = "//*[@id=\"result-index-@index\"]"
XPATH_INTEIRO_TEOR = "/html/body/app-root/app-home/main/search/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div/a[4]"
