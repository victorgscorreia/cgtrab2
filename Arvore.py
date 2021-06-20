from Base import *
from Object import *


def cria_arvore(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Arvore/bark_0021.jpg")
    textures_names.append("Arvore/DB2X2_L01.png")
    filename = "Arvore/arvore.obj"

    arvore = Object(filename, textures_names, 8, 0, -8, 0, 0, 0, 3, id_tex_livre, vertices_list, textures_coord_list)

    return arvore