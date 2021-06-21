
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
from PIL import Image

from Carro import *
from Arvore import *
from Chessboard import *
from Casa import *
from Placa import *
from Table import *
from Sword import *
from Chao import *
from Ceu import *

polygonal_mode = False
altura = 1600
largura = 1200 
firstMouse = True
yaw = -90.0 
pitch = 0.0
lastX =  largura/2
lastY =  altura/2

#camera inicial dentro da casa
cameraPos   = glm.vec3(3.0,  4.0,  -25.0)
cameraFront = glm.vec3(0.0,  0.0, -1.0)
cameraUp    = glm.vec3(0.0,  1.0,  0.0)

fov = 85
near = 0.1
far = 65

stop = False

def check_colision_camera():
    MAX_X, MAX_Y, MAX_Z = 48, 48, 48
    MIN_X, MIN_Y, MIN_Z = -48, 2, -48
    global cameraPos
    if cameraPos.x >= MAX_X:
        cameraPos.x = MAX_X
    elif cameraPos.x <= MIN_X:
        cameraPos.x = MIN_X

    if cameraPos.y >= MAX_Y:
        cameraPos.y = MAX_Y
    elif cameraPos.y <= MIN_Y:
        cameraPos.y = MIN_Y

    if cameraPos.z >= MAX_Z:
        cameraPos.z = MAX_Z
    elif cameraPos.z <= MIN_Z:
        cameraPos.z = MIN_Z

def check_projection_camera():
    global fov, near, far
    MAX_FOV, MAX_NEAR, MAX_FAR = 180, 200, 200
    MIN_FOV, MIN_NEAR, MIN_FAR = 1, 0.1, 0.1

    if fov >= MAX_FOV:
        fov = MAX_FOV
    elif fov <= MIN_FOV:
        fov = MIN_FOV 

    if near >= MAX_NEAR:
        near = MAX_NEAR
    elif near <= MIN_NEAR:
        near = MIN_NEAR

    if far >= MAX_FAR:
        far = MAX_FAR
    elif far <= MIN_FAR:
        far = MIN_FAR
    

def key_event(window,key,scancode,action,mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode
    global fov, near, far
    global stop
    cameraSpeed = 0.2
    #movimentando camera
    if key == 87 and (action==1 or action==2): # tecla W
        cameraPos += cameraSpeed * cameraFront
    
    if key == 83 and (action==1 or action==2): # tecla S
        cameraPos -= cameraSpeed * cameraFront
    
    if key == 65 and (action==1 or action==2): # tecla A
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
        
    if key == 68 and (action==1 or action==2): # tecla D
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    
    #mudando polygonal mode
    if key == 80 and action==1 and polygonal_mode==True:
        polygonal_mode=False
    else:
        if key == 80 and action==1 and polygonal_mode==False:
            polygonal_mode=True
    
    #mexendo nos parametros da projection
    if key == 90 and (action==1 or action==2): #tecla Z
        near -= cameraSpeed

    if key == 88 and (action==1 or action==2): #tecla X
        near += cameraSpeed

    if key == 67 and (action==1 or action==2): #tecla C
        far -= cameraSpeed

    if key == 86 and (action==1 or action==2): #tecla V
        far += cameraSpeed

    if key == 70 and (action==1 or action==2): #tecla F
        fov -= cameraSpeed
    
    if key == 71 and (action==1 or action==2): #tecla G
        fov += cameraSpeed

    #fechando janela
    if key == 81 and action == 1:
        stop = True
    check_colision_camera()
    check_projection_camera()
        
def mouse_event(window, xpos, ypos):
    global firstMouse, cameraFront, yaw, pitch, lastX, lastY
    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False
    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    sensitivity = 0.3 
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    #89.9 pois se pitch = 90, cameraFront eh LD com cameraUp,
    #o que nao eh permitido e causa inconsistencias nos calculos
    if pitch >= 89.9: pitch = 89.9
    if pitch <= -89.9: pitch = -89.9

    front = glm.vec3()
    front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    front.y = math.sin(glm.radians(pitch))
    front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)

def main():
    global altura, largura
    global cameraPos, cameraFront, cameraUp
    global fov, near, far
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(largura, altura, "Malhas e Texturas", None, None)
    glfw.make_context_current(window)

    vertex_code = """
            attribute vec3 position;
            attribute vec2 texture_coord;
            varying vec2 out_texture;
                    
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;        
            
            void main(){
                gl_Position = projection * view * model * vec4(position,1.0);
                out_texture = vec2(texture_coord);
            }
            """

    fragment_code = """
            uniform vec4 color;
            varying vec2 out_texture;
            uniform sampler2D samplerTexture;
            
            void main(){
                vec4 texture = texture2D(samplerTexture, out_texture);
                gl_FragColor = texture;
            }
            """

    # Request a program and shader slots from GPU
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Set shaders source
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # Compile shaders
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")

    # Attach shader objects to the program
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    # Build program
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    # Make program the default program
    glUseProgram(program)

    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    qtd_texturas = 10
    texturas = glGenTextures(qtd_texturas)

    vertices_list = []    
    textures_coord_list = []

    id_tex_livre = [0]

    #======================= CRIA OS OBJETOS ================================
    chao = cria_chao(id_tex_livre, vertices_list, textures_coord_list)
    carro = cria_carro(id_tex_livre, vertices_list, textures_coord_list)
    casa = cria_casa(id_tex_livre, vertices_list, textures_coord_list)
    placa = cria_placa(id_tex_livre, vertices_list, textures_coord_list)
    arvore = cria_arvore(id_tex_livre, vertices_list, textures_coord_list)
    mesa = cria_table(id_tex_livre, vertices_list, textures_coord_list)
    tabuleiro = cria_chessboard(id_tex_livre, vertices_list, textures_coord_list)
    espada = cria_sword(id_tex_livre, vertices_list, textures_coord_list)
    ceu = cria_ceu(id_tex_livre, vertices_list, textures_coord_list)
    #=========================================================================


    # Request a buffer slot from GPU
    buffer = glGenBuffers(2)

    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices['position'] = vertices_list


    # Upload data
    glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    loc_vertices = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc_vertices)
    glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)


    textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
    textures['position'] = textures_coord_list


    # Upload data
    glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
    glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
    stride = textures.strides[0]
    offset = ctypes.c_void_p(0)
    loc_texture_coord = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc_texture_coord)
    glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)   

        
    glfw.set_key_callback(window,key_event)
    glfw.set_cursor_pos_callback(window, mouse_event)


    glfw.show_window(window)
    glfw.set_cursor_pos(window, lastX, lastY)

    glEnable(GL_DEPTH_TEST) ### importante para 3D
    
    #variaveis para controle da movimentacao do carro
    min_pos_carro = -450
    max_pos_carro = 450
    speed_carro = 1
    pos_carro = 0

    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        if polygonal_mode==True:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        if polygonal_mode==False:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        
        
        #====================== MOVIMENTANDO CARRO =================================
        pos_carro += speed_carro
        if pos_carro >= max_pos_carro:
            pos_carro = max_pos_carro
            speed_carro *= -1
        elif pos_carro <= min_pos_carro:
            pos_carro = min_pos_carro
            speed_carro *= -1

        carro.update_position(0,pos_carro,0)
        #===========================================================================

        #======================= DESENHA OS OBJETOS ================================
        ceu.draw(program)
        chao.draw(program)
        carro.draw(program)
        casa.draw(program)
        placa.draw(program)
        arvore.draw(program)
        mesa.draw(program)
        tabuleiro.draw(program)
        espada.draw(program)
        #===========================================================================

        mat_view = view(cameraPos, cameraFront, cameraUp)
        loc_view = glGetUniformLocation(program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

        mat_projection = projection(altura, largura, fov, near, far)
        loc_projection = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)    
        
        
        glfw.swap_buffers(window)

        if stop:
            break

    glfw.terminate()

if __name__ == "__main__":
    main()