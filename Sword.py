from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Sword e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
@RETORNO
    object - o objeto Sword criado
'''
def cria_sword(id_tex_livre, vertices_list, textures_coord_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Sword/Sword_texture.png")
    filename = "Sword/sword.obj"
    #criando o objeto
    espada = Object(filename, textures_names, -290, -50, -34, math.pi/2, math.pi/2, 0, 0.1, id_tex_livre, vertices_list, textures_coord_list)

    return espada