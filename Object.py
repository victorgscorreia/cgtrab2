from math import gamma
from Base import *

class Object:
    def __init__(self, filename, textures_names, tx, ty, tz, theta, phi, gamma, s, id_tex_livre, vertices_list, textures_coord_list):
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.theta = theta
        self.phi = phi
        self.gamma = gamma
        self.s = s

        self.texture_ids = []
        self.ini_textures = []
        self.num_vertices_textures = []

        modelo = load_model_from_file(filename)
        materials_visited = []

        for face in modelo['faces']:
            if face[2] not in materials_visited:
                self.ini_textures.append( len(vertices_list) )
                materials_visited.append(face[2]) 
            for vertice_id in face[0]:
                vertices_list.append( modelo['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                textures_coord_list.append( modelo['texture'][texture_id-1] )

        #contando o numero de vertices que iremos utilizar em cada textura
        for i in range( len(self.ini_textures) ):
            if i == len(self.ini_textures)-1:
                self.num_vertices_textures.append( len(vertices_list) - self.ini_textures[i] )
            else:
                self.num_vertices_textures.append(self.ini_textures[i+1] - self.ini_textures[i] )

        for tex in textures_names:
            load_texture_from_file(id_tex_livre[0],tex)
            self.texture_ids.append( id_tex_livre[0] )
            id_tex_livre[0] += 1

    def draw(self, program):
        mat_model = model(self.theta, self.phi,self.gamma, self.tx, self.ty, self.tz, self.s)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        #iterando sobre as textures
        for i in range(len(self.ini_textures)):
            #define id da textura do modelo
            glBindTexture(GL_TEXTURE_2D, self.texture_ids[i])
            # desenha o modelo
            glDrawArrays(GL_TRIANGLES, self.ini_textures[i], self.num_vertices_textures[i]) ## renderizando

    def update_position(self, tx, ty, tz):
        self.tx = tx
        self.ty = ty
        self.tz = tz
    