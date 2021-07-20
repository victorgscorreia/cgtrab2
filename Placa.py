from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Placa e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto Placa criado
'''
def cria_placa(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Placa/Wooden sign texture.jpg")
    textures_names.append("Placa/Wooden sign texture.jpg")
    textures_names.append("Placa/Wooden sign texture.jpg")
    filename = "Placa/wooden_sign.obj"
    mtl_filename = "Placa/wooden_sign.mtl"
    #criando o objeto
    placa = Object(filename, mtl_filename, textures_names, -3, -22, 5, 0, math.pi/2, -math.pi/2, 0.5, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return placa