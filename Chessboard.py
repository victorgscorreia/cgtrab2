from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Chessboard e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto Chessboard criado
'''
def cria_chessboard(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Chessboard/10586_Chess Board_v1_diffuse.JPG")
    filename = "Chessboard/chessboard.obj"
    mtl_filename = "Chessboard/chessboard.mtl"
    #criando o objeto
    chessboard = Object(filename, mtl_filename, textures_names, 50, 968, 112, 0, -math.pi/2, 0, 0.03, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return chessboard