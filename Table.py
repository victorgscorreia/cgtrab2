from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Table e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto Table criado
'''
def cria_table(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Table/10233_Kitchen_Table_v1_Diffuse.jpg")
    filename = "Table/table.obj"
    mtl_filename = "Table/table.mtl"
    #criando o objeto
    table = Object(filename, mtl_filename, textures_names, 1050, -125, 43, math.pi/2, -math.pi/2, 0, 0.028, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return table