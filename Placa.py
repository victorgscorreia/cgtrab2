from Base import *
from Object import *

def cria_placa(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Placa/Wooden sign texture.jpg")
    textures_names.append("Placa/Wooden sign texture.jpg")
    textures_names.append("Placa/Wooden sign texture.jpg")
    filename = "Placa/wooden_sign.obj"

    veemon = Object(filename, textures_names, -3, -22, 5, 0, math.pi/2, -math.pi/2, 0.5, id_tex_livre, vertices_list, textures_coord_list)

    return veemon