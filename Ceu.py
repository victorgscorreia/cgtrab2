from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Ceu e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
@RETORNO
    object - o objeto Ceu criado
'''
def cria_ceu(id_tex_livre, vertices_list, textures_coord_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Ceu/toy_story.jpg")
    filename = "Ceu/ceu.obj"
    #criando o objeto
    chao = Object(filename, textures_names, 0, 0, 0, 0, 0, 0, 50.0, id_tex_livre, vertices_list, textures_coord_list)

    return chao