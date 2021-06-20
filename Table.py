from Base import *
from Object import *

def cria_table(id_tex_livre, vertices_list, textures_coord_list):
    textures_names = []
    textures_names.append("Table/10233_Kitchen_Table_v1_Diffuse.jpg")
    filename = "Table/table.obj"

    table = Object(filename, textures_names, 1050, -125, 43, math.pi/2, -math.pi/2, 0, 0.028, id_tex_livre, vertices_list, textures_coord_list)

    return table