import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Konfigurasi Kubus 3D
vertices = ( (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1) )
edges = ( (0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7) )

def Draw_Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Draw_Square():
    glBegin(GL_QUADS)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glVertex2f(-1, 1)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Variabel Transformasi
    cube_trans = [ -3, 0, -10] # Posisi awal kiri
    cube_rot = 0
    cube_scale = 1.0
    
    sq_trans = [ 3, 0, -10] # Posisi awal kanan
    sq_rot = 0
    sq_scale = 1.0
    sq_shear = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Kontrol Keyboard
        keys = pygame.key.get_pressed()
       # KONTROL KUBUS 3D (Menggunakan Tombol Huruf)
        if keys[K_w]: cube_trans[1] += 0.1  # Translasi Atas
        if keys[K_s]: cube_trans[1] -= 0.1  # Translasi Bawah
        if keys[K_r]: cube_rot += 2         # Rotasi
        if keys[K_t]: cube_scale += 0.01    # Skala Besar

        # KONTROL PERSEGI 2D (Menggunakan Tombol Panah & Tombol Lain)
        if keys[K_UP]:    sq_trans[1] += 0.1   # Translasi Atas
        if keys[K_DOWN]:  sq_trans[1] -= 0.1   # Translasi Bawah
        if keys[K_RIGHT]: sq_rot += 2          # Rotasi
        if keys[K_l]:     sq_scale += 0.01     # Skala (Tombol L)
        if keys[K_h]:     sq_shear += 0.05     # Shearing (Tombol H)
        if keys[K_f]:     sq_scale_x *= -1     # Refleksi (Tombol F untuk Flip)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # RENDER KUBUS 3D (Sisi Kiri)
        glPushMatrix()
        glTranslatef(cube_trans[0], cube_trans[1], cube_trans[2])
        glRotatef(cube_rot, 1, 1, 1)
        glScalef(cube_scale, cube_scale, cube_scale)
        glColor3f(1, 1, 1) # Putih
        Draw_Cube()
        glPopMatrix()

        # RENDER PERSEGI 2D (Sisi Kanan)
        glPushMatrix()
        glTranslatef(sq_trans[0], sq_trans[1], sq_trans[2])
        glRotatef(sq_rot, 0, 0, 1)
        glScalef(sq_scale, sq_scale, 1)
        # Efek Shearing sederhana dengan matriks
        shear_matrix = [1, 0, 0, 0,  sq_shear, 1, 0, 0,  0, 0, 1, 0,  0, 0, 0, 1]
        glMultMatrixf(shear_matrix)
        glColor3f(0, 1, 0) # Hijau
        Draw_Square()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

main()