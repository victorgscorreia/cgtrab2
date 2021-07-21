
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
from Luz_Interna import *
from Luz_Externa import *

#parametros da janela
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

#parametros da matriz projection
fov = 85
near = 0.1
far = 65

stop = False

luz_ambiente_externo_intencidade = 0.3
luz_interno_intencidade = 1.0


'''
Esta funcao faz a verificao se a intencidade da luz
interna e externa esta no intervalo [0,1]
nao permitindo que ultrapasse estes intervalos
.
'''
def check_limite_luz():
    global luz_ambiente_externo_intencidade
    global luz_interno_intencidade
    if luz_ambiente_externo_intencidade >= 1.0:
        luz_ambiente_externo_intencidade = 1.0
    
    if luz_ambiente_externo_intencidade <= 0.0:
        luz_ambiente_externo_intencidade = 0.0
    
    if luz_interno_intencidade >= 1.0:
        luz_interno_intencidade = 1.0
    
    if luz_interno_intencidade <= 0.0:
        luz_interno_intencidade = 0.0

'''
Esta funcao faz a verificao se a camera 
ainda se mantem dentro dos limites do mundo,
nao permitindo que a camera ultrapasse os limites.
'''
def check_colision_camera():
    #valores maximos e minimos da posicao da camera para cada coordenada
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

'''
Esta funcao verifica se os parametros da matriz de 
projecao estao dentro limites estipulados.
'''
def check_projection_camera():
    global fov, near, far
    #valores maximos e minimos dos parametros fov, near e far
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
    
'''
Funcao de evento do teclado
'''
def key_event(window,key,scancode,action,mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode
    global fov, near, far
    global stop
    global luz_interno_intencidade
    global luz_ambiente_externo_intencidade
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

    intencidade_speed = 0.02
    if key == 85 and (action==1 or action==2): #letra U
        luz_ambiente_externo_intencidade -= intencidade_speed
    
    if key == 73 and (action==1 or action==2):
        luz_ambiente_externo_intencidade += intencidade_speed

    if key == 75 and (action==1 or action==2):
        luz_interno_intencidade -= intencidade_speed
    
    if key == 76 and (action==1 or action==2):
        luz_interno_intencidade += intencidade_speed

    #fechando janela
    if key == 81 and action == 1:
        stop = True

    check_limite_luz()
    check_colision_camera()
    check_projection_camera()

'''
Funcao de evento do mouse
'''
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

'''
fluxo principal do programa
'''
def main():
    #linkando os valores globais
    global altura, largura
    global cameraPos, cameraFront, cameraUp
    global fov, near, far
    global luz_ambiente_externo_intencidade
    global luz_interno_intencidade

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(largura, altura, "Malhas e Texturas", None, None)
    glfw.make_context_current(window)

    vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;
        
       
        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(  model * vec4(position, 1.0));
            out_normal = vec3( model *vec4(normals, 1.0));            
        }
        """

    fragment_code = """

        // parametro com a cor da(s) fonte(s) de iluminacao
        uniform vec3 lightPos; // define coordenadas de posicao da luz
        uniform vec3 lightAmbiente;
        uniform vec3 lightIncidente;
        
        // parametros da iluminacao ambiente e difusa
        uniform vec3 ka; // coeficiente de reflexao ambiente
        uniform vec3 kd; // coeficiente de reflexao difusa
        
        // parametros da iluminacao especular
        uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
        uniform vec3 ks; // coeficiente de reflexao especular
        uniform float ns; // expoente de reflexao especular
        
        // parametros recebidos do vertex shader
        varying vec2 out_texture; // recebido do vertex shader
        varying vec3 out_normal; // recebido do vertex shader
        varying vec3 out_fragPos; // recebido do vertex shader
        uniform sampler2D samplerTexture;
        
        void main(){
        
            // calculando reflexao ambiente
            vec3 ambient = ka * lightAmbiente;             
        
            // calculando reflexao difusa
            vec3 norm = normalize(out_normal); // normaliza vetores perpendiculares
            vec3 lightDir = normalize(lightPos - out_fragPos); // direcao da luz
            float diff = max(dot(norm, lightDir), 0.0); // verifica limite angular (entre 0 e 90)
            vec3 diffuse = kd * diff * lightIncidente; // iluminacao difusa
            
            // calculando reflexao especular
            vec3 viewDir = normalize(viewPos - out_fragPos); // direcao do observador/camera
            vec3 reflectDir = normalize(reflect(-lightDir, norm)); // direcao da reflexao
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular = ks * spec * lightIncidente;             
            
            // aplicando o modelo de iluminacao
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + diffuse + specular),1.0)*texture; // aplica iluminacao
            gl_FragColor = result;

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
    normals_list = [] 

    id_tex_livre = [0]

    #======================= CRIA OS OBJETOS ================================
    chao = cria_chao(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    carro = cria_carro(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    casa = cria_casa(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    placa = cria_placa(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    arvore = cria_arvore(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    mesa = cria_table(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    tabuleiro = cria_chessboard(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    espada = cria_sword(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    ceu = cria_ceu(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    luz_interna = cria_luz_interna(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    luz_externa = cria_luz_externa(id_tex_livre, vertices_list, textures_coord_list, normals_list)
    #=========================================================================


    # Request a buffer slot from GPU
    buffer = glGenBuffers(3)

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

    normals = np.zeros(len(normals_list), [("position", np.float32, 3)]) # três coordenadas
    normals['position'] = normals_list


    # Upload coordenadas normals de cada vertice
    glBindBuffer(GL_ARRAY_BUFFER, buffer[2])
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    stride = normals.strides[0]
    offset = ctypes.c_void_p(0)
    loc_normals_coord = glGetAttribLocation(program, "normals")
    glEnableVertexAttribArray(loc_normals_coord)
    glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)

        
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

    #definindo valores luz externa
    lightAmbExt = np.zeros((3,))
    lightAmbExt[0] = 1.0
    lightAmbExt[1] = 1.0
    lightAmbExt[2] = 1.0

    lightIncExt = np.zeros((3,))
    lightIncExt[0] = 1.0
    lightIncExt[1] = 1.0
    lightIncExt[2] = 1.0


    #definindo valores luz interna
    lightAmbInt = np.zeros((3,))
    lightAmbInt[0] = 1.0
    lightAmbInt[1] = 1.0
    lightAmbInt[2] = 1.0

    lightIncInt = np.zeros((3,))
    lightIncInt[0] = 1.0
    lightIncInt[1] = 1.0
    lightIncInt[2] = 1.0

    while not glfw.window_should_close(window):

        glfw.poll_events() 
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        if polygonal_mode==True:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        if polygonal_mode==False:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        
        loc_view_pos = glGetUniformLocation(program, "viewPos") # recuperando localizacao da variavel viewPos na GPU
        glUniform3f(loc_view_pos, cameraPos[0], cameraPos[1], cameraPos[2]) ### posicao da camera/observador (x,y,z)
        #====================== MOVIMENTANDO CARRO =================================
        pos_carro += speed_carro
        if pos_carro >= max_pos_carro:
            pos_carro = max_pos_carro
            speed_carro *= -1
        elif pos_carro <= min_pos_carro:
            pos_carro = min_pos_carro
            speed_carro *= -1

        carro.update_position(0,pos_carro,0, False, program)
        #===========================================================================
        

        #====================== CARREGA LUZ EXTERNA ================================
        loc_light_amb = glGetUniformLocation(program, "lightAmbiente")
        loc_light_inc = glGetUniformLocation(program, "lightIncidente")

        le = luz_ambiente_externo_intencidade
        #setando os valores desta luz nos parametros da gpu
        glUniform3f(loc_light_amb, le*lightAmbExt[0], le*lightAmbExt[1], le*lightAmbExt[2])
        glUniform3f(loc_light_inc, lightIncExt[0], lightIncExt[1], lightIncExt[2])

        luz_externa.update_position(16.5 - pos_carro,6,0, True, program)
        luz_externa.draw(program)
        #===========================================================================

        #======================= DESENHA OS OBJETOS INTERNOS =======================
        ceu.draw(program)
        chao.draw(program)
        carro.draw(program)
        casa.draw(program)
        placa.draw(program)
        arvore.draw(program)
        
        #===========================================================================

        #====================== CARREGA LUZ INTERNA ================================
        loc_light_amb = glGetUniformLocation(program, "lightAmbiente")
        loc_light_inc = glGetUniformLocation(program, "lightIncidente")

        li = luz_interno_intencidade
        #setando os valores desta luz nos parametros da gpu
        glUniform3f(loc_light_amb, li*lightAmbInt[0], li*lightAmbInt[1], li*lightAmbInt[2])
        glUniform3f(loc_light_inc, li*lightIncInt[0], li*lightIncInt[1], li*lightIncInt[2])

        luz_interna.update_position(3.3,3.3,-30, True, program)
        luz_interna.draw(program)
        #===========================================================================

        #======================= DESENHA OS OBJETOS INTERNOS =======================
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