from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Arvore e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
@RETORNO
    object - o objeto Arvore criado
'''
def cria_arvore(id_tex_livre, vertices_list, textures_coord_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Arvore/bark_0021.jpg")
    textures_names.append("Arvore/DB2X2_L01.png")
    filename = "Arvore/arvore.obj"
    #criando o objeto
    arvore = Object(filename, textures_names, 8, 0, -8, 0, 0, 0, 3, id_tex_livre, vertices_list, textures_coord_list)

    return arvore