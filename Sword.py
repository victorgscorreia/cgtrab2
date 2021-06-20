from Base import *
from Object import *

def cria_sword(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Sword/Sword_texture.png")
    filename = "Sword/sword.obj"

    espada = Object(filename, textures_names, -290, -50, -34, math.pi/2, math.pi/2, 0, 0.1, id_tex_livre, vertices_list, textures_coord_list)

    return espada