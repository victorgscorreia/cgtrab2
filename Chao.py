from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Chao e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto Chao criado
'''
def cria_chao(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Chao/grass.jpg")
    textures_names.append("Chao/street.jpg")
    filename = "Chao/chao.obj"
    mtl_filename = "Chao/chao.mtl"
    #criando o objeto
    chao = Object(filename, mtl_filename, textures_names, 0, 0, 0, 0, 0, 0, 50.0, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return chao