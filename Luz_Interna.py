from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Luz Interna e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto Luz Interna criado
'''
def cria_luz_interna(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Lantern/texture_high.png")
    textures_names.append("Lantern/texture_high.png")
    filename = "Lantern/lantern.obj"
    mtl_filename = "Lantern/lantern.mtl"
    #criando o objeto
    luz = Object(filename, mtl_filename, textures_names, 0, 0, 0, 0, 0, 0, 1, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return luz