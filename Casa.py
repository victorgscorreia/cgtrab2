from Base import *
from Object import *


def cria_casa(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Casa/Parede de Pedras.jpg")
    textures_names.append("Casa/Parede.jpg")
    textures_names.append("Casa/Telhado de palha.jpg")
    textures_names.append("Casa/Madeira para janela.jpg")
    textures_names.append("Casa/Porta de madeira.jpg")

    filename = "Casa/casa.obj"

    casa = Object(filename, textures_names, -0.8, 2.95, -12.3, 0, 0, 0, 1.7, id_tex_livre, vertices_list, textures_coord_list)

    return casa