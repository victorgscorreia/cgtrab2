from Base import *
from Object import *

'''
Esta funcao cria um objeto do tipo Casa e o retorna
@PARAMETROS
    id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
    vertices_list - lista de coordenadas de vertices
    textures_coord_list - lista de coordenadas de textura
@RETORNO
    object - o objeto Casa criado
'''
def cria_casa(id_tex_livre, vertices_list, textures_coord_list):
    #adicionando os nomes das texturas utilizdas em uma lista
    textures_names = []
    textures_names.append("Casa/Parede de Pedras.jpg")
    textures_names.append("Casa/Parede.jpg")
    textures_names.append("Casa/Telhado de palha.jpg")
    textures_names.append("Casa/Madeira para janela.jpg")
    textures_names.append("Casa/Porta de madeira.jpg")

    filename = "Casa/casa.obj"
    #criando o objeto
    casa = Object(filename, textures_names, -0.8, 2.95, -12.3, 0, 0, 0, 1.7, id_tex_livre, vertices_list, textures_coord_list)

    return casa