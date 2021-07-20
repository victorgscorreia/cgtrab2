from Base import *
from Object import *

'''
Esta funcao cria o objeto da luz externa, o farou do carro
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto luz externa criado
'''
def cria_luz_externa(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizadas em uma lista
    textures_names = []
    textures_names.append("Luz_Externa/luz_externa.png")
    filename = "Luz_Externa/luz_externa.obj"
    mtl_filename = "Luz_Externa/luz_externa.mtl"
    #criando o objeto
    luz = Object(filename, mtl_filename, textures_names, 0, 0, 0, 0, 0, 0, 0.1, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return luz