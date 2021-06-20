from Base import *
from Object import *

def cria_carro(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Carro/10600_RC_Car_SG_v1_diffuse.jpg")
    filename = "Carro/carro.obj"

    carro = Object(filename, textures_names, 0, 0, 0, math.pi/2, 3*math.pi/2, 0, 0.1, id_tex_livre, vertices_list, textures_coord_list)

    return carro