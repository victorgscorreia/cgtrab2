from Base import *
from Object import *

def cria_chao(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Chao/grass.jpg")
    textures_names.append("Chao/street.jpg")
    filename = "Chao/chao.obj"

    chao = Object(filename, textures_names, 0, 0, 0, 0, 0, 0, 50.0, id_tex_livre, vertices_list, textures_coord_list)

    return chao