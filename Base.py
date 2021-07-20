import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
from PIL import Image

'''
Esta funcao cria a matriz model de um objeto, atra ves dos parametros de 
transformacao passados.
@PARAMETROS
    theta - parametro da matriz model - angulo de rotacao no eixo z.
    phi - parametro da matriz model - angulo de rotacao no eixo x.
    gamma - parametro da matriz model - angulo de rotacao no eixo y.
    t_x - parametro da matriz model - transladacao em x
    t_y - parametro da matriz model - transladacao em y
    t_z - parametro da matriz model - transladacao em z
    s - parametro da matriz model - escala uniforme
@RETORNO
    numpy array - matriz model.
'''
def model(theta, phi, gamma ,t_x, t_y, t_z, s):
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
    
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, phi, glm.vec3(1, 0, 0))
    matrix_transform = glm.rotate(matrix_transform, gamma, glm.vec3(0, 1, 0))
    matrix_transform = glm.rotate(matrix_transform, theta, glm.vec3(0, 0, 1))
    
    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s, s, s))

    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))  
    
    matrix_transform = np.array(matrix_transform).T # pegando a transposta da matriz (glm trabalha com ela invertida)
    
    return matrix_transform

'''
Esta funcao cria a matriz view da camera, atraves dos parametros passados
@PARAMETROS
    cameraPos - posicao da camera
    cameraFront - direcao que a camera esta olhando
    cameraUp - Direcao que aponta para cima da camera
'''
def view(cameraPos, cameraFront, cameraUp):
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
    mat_view = np.array(mat_view)
    
    return mat_view

'''
Esta funcao cria a matriz projection da camera, atraves dos parametros passados
@PARAMETROS
    altura - altura da janela
    largura - largura da janela
    fov - fov da camera
    near - a partir de qual distancia a camera comeca a "ver".
    far - ate qual distancia a camera consegue "ver".
'''
def projection(altura, largura, fov, near, far):
    fov_ = glm.radians(fov)
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(fov_, largura/altura, near, far)
    mat_projection = np.array(mat_projection)    
    return mat_projection

'''
Esta funcao le um objeto de um .obj.
@PARAMETROS
    filename - nome do arquivo .obj
'''
def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    normals = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando normais
        if values[0] == 'vn':
            normals.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, face_normals, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    model['normals'] = normals

    return model

'''
Esta funcao le os parametros de iluminacao
das texturas de um objeto, atraves do arquivo .mtl,
esses parametros sendo ka, kd, ks e ns
'''
def load_mtl_file(filename):

    #inicialianzo as lista que armazenaram os valores
    kas = []
    kds = []
    kss = []
    nss = []

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .mtl
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue

        #se a linha comecar com ka, le o vetor de tamanho 3 que o representa
        if values[0] == "Ka":
            ka = []
            for v in values[1:]:
                ka.append(float(v))
            kas.append(ka)
        
        #se a linha comecar com kd, le o vetor de tamanho 3 que o representa
        if values[0] == "Kd":
            kd = []
            for v in values[1:]:
                kd.append(float(v))
            kds.append(kd)

        #se a linha comecar com ks, le o vetor de tamanho 3 que o representa
        if values[0] == "Ks":
            ks = []
            for v in values[1:]:
                ks.append(float(v))
            kss.append(ks)
        
        #se a linha comecar com Ns, le o valor real que o representa
        elif values[0] == "Ns":
            for v in values[1:]:
                nss.append(float(v))

    #inicilizando o dicionario de retorno
    ilu = {}
    #atribuindo ao dicionario as listas
    ilu['kas'] = kas
    ilu['kds'] = kds
    ilu['kss'] = kss
    ilu['nss'] = nss
    #retornando
    return ilu

'''
Esta funcao le uma textura de um arquivo de textura.
@PARAMETROS
    texture_id - a qual id de textura a textura lida sera atribuida.
    img_textura - nome do arquivo de textura
'''
def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width = img.size[0]
    img_height = img.size[1]

    image_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    #image_data = np.array(list(img.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
