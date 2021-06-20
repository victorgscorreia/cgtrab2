from Base import *
from Object import *


def cria_chessboard(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Chessboard/10586_Chess Board_v1_diffuse.JPG")
    filename = "Chessboard/chessboard.obj"

    chessboard = Object(filename, textures_names, 50, 968, 112, 0, -math.pi/2, 0, 0.03, id_tex_livre, vertices_list, textures_coord_list)

    return chessboard