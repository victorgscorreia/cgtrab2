from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Carro e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
    normals_list - lista de normais de vertices
@RETORNO
    object - o objeto Carro criado
'''
def cria_carro(id_tex_livre, vertices_list, textures_coord_list, normals_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Carro/10600_RC_Car_SG_v1_diffuse.jpg")
    filename = "Carro/carro.obj"
    mtl_filename = "Carro/carro.mtl"
    #criando o objeto
    carro = Object(filename, mtl_filename, textures_names, 0, 0, 0, math.pi/2, 3*math.pi/2, 0, 0.1, id_tex_livre, vertices_list, textures_coord_list, normals_list)

    return carro