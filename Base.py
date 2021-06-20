import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
from PIL import Image

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

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
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


        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model

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
