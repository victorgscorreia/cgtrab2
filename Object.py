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
        normals_list - lista de normais de vertices
    '''
    def __init__(self, filename, mtl_filename, textures_names, tx, ty, tz, theta, phi, gamma, s, id_tex_livre, vertices_list, textures_coord_list , normals_list):
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
            if face[3] not in materials_visited:
                self.ini_textures.append( len(vertices_list) )
                materials_visited.append(face[3]) 
            for vertice_id in face[0]:
                vertices_list.append( modelo['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                textures_coord_list.append( modelo['texture'][texture_id-1] )
            for normal_id in face[2]:
                normals_list.append( modelo['normals'][normal_id-1] )
        
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
        
        #carregando os valores de iluminacao do arquivo mtl
        ilu = load_mtl_file(mtl_filename)
        #passando os valores de iluminacao para os atributos
        self.kas = ilu['kas']
        self.kds = ilu['kds']
        self.kss = ilu['kss']
        self.nss = ilu['nss']

    '''
    funcao de desenhar o objeto no mundo
    '''
    def draw(self, program):
        #montando a matriz model atraves dos parametros e enviando para GPU.
        mat_model = model(self.theta, self.phi,self.gamma, self.tx, self.ty, self.tz, self.s)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        #instanciando as variaves de loc de iluminacao
        loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
        loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
        loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
        loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU

        #iterando sobre as textures
        for i in range(len(self.ini_textures)):
            #setando os valores de iluminacao
            glUniform3f(loc_ka, self.kas[i][0], self.kas[i][1], self.kas[i][2]) ### envia ka pra gpu
            glUniform3f(loc_kd, self.kds[i][0], self.kds[i][1], self.kds[i][2]) ### envia kd pra gpu 
            glUniform3f(loc_ks, self.kss[i][0], self.kss[i][1], self.kss[i][2]) ### envia ks pra gpu  
            glUniform1f(loc_ns, self.nss[i]) ### envia ns pra gpu      

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
    def update_position(self, tx, ty, tz, is_light, program):
        if is_light:
            loc_light_pos = glGetUniformLocation(program, "lightPos") # recuperando localizacao da variavel lightPos na GPU
            glUniform3f(loc_light_pos, self.s*tx, self.s*ty, self.s*tz) ### posicao da fonte de luz
        self.tx = tx
        self.ty = ty
        self.tz = tz
    