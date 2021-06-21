from Base import *
from Object import *

def cria_ceu(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Ceu/toy_story.jpg")
    filename = "Ceu/ceu.obj"

    chao = Object(filename, textures_names, 0, 0, 0, 0, 0, 0, 50.0, id_tex_livre, vertices_list, textures_coord_list)

    return chao