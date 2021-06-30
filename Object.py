from math import gamma
from Base import *

'''
Classe generica para um objeto no mundo
'''
class Object:
    '''
    contrutor da classe
    @PARAMETROS
        filename - nome do arquivo .obj do objeto
        textures_names - nomes dos arquivos de texturas.
        tx - parametro da matriz model - transladacao em x
        ty - parametro da matriz model - transladacao em y
        tz - parametro da matriz model - transladacao em z
        theta - parametro da matriz model - angulo de rotacao no eixo z.
        phi - parametro da matriz model - angulo de rotacao no eixo x.
        gamma - parametro da matriz model - angulo de rotacao no eixo y.
        s - parametro da matriz model - escala uniforme
        id_tex_livre - primeiro id de textura nao utilizado - passado como lista de tamanho 1
        vertices_list - lista de coordenadas de vertices
        textures_coord_list - lista de coordenadas de textura
    '''
    def __init__(self, filename, textures_names, tx, ty, tz, theta, phi, gamma, s, id_tex_livre, vertices_list, textures_coord_list):
        #atribuindo os valores passados no parametro para os atributos
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
        #chamando a funcao para carregar o modelo
        modelo = load_model_from_file(filename)
        materials_visited = []
        #iterando sobre cada face, adicionando os vertices e 
        #coordenadas de texturas nos arrays.
        for face in modelo['faces']:
            #se a primeira vez que aparece a textura, adiciona onde ela comeca.
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

        #carregando as texturas do objeto.
        for tex in textures_names:
            load_texture_from_file(id_tex_livre[0],tex)
            self.texture_ids.append( id_tex_livre[0] )
            id_tex_livre[0] += 1

    '''
    funcao de desenhar o objeto no mundo
    '''
    def draw(self, program):
        #montando a matriz model atraves dos parametros e enviando para GPU.
        mat_model = model(self.theta, self.phi,self.gamma, self.tx, self.ty, self.tz, self.s)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        #iterando sobre as textures
        for i in range(len(self.ini_textures)):
            #define id da textura do modelo
            glBindTexture(GL_TEXTURE_2D, self.texture_ids[i])
            # desenha o modelo
            glDrawArrays(GL_TRIANGLES, self.ini_textures[i], self.num_vertices_textures[i]) ## renderizando

    '''
    Esta funcao permite atualizar a transladacao do objeto no mundo
    @PARAMETROS
        tx - parametro da matriz model - transladacao em x
        tx=y - parametro da matriz model - transladacao em y
        tz - parametro da matriz model - transladacao em z
    '''
    def update_position(self, tx, ty, tz):
        self.tx = tx
        self.ty = ty
        self.tz = tz
    