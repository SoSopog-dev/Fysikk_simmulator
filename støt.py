import pygame
import numpy


def init():
    pygame.display.set_caption('Fysikk')
    pygame.display.init()
    (WIDTH, HEIGHT) = (1920, 1080)
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    return WIDTH, HEIGHT, WIN

def step(point, vector):

    x = point[0] + vector[0]
    y = point[1] + vector[1]

    return x, y

def product(k, vector):
    return [k*vector[0], k*vector[1]]

def add(vector_1, vector_2):
    return [vector_1[0] + vector_2[0], vector_1[1] + vector_2[1]]

class body():
    def __init__(self, x, y, mass, force, deformation_degree, width, heigth, shape = "square"):

        #Shape and size related variables
        self.x = x
        self.y = y
        self.width = width
        self.heigth = heigth
        self.shape = shape


        self.direction = [0,0]
        self.velocity = [0,0]
        self.acceleraiton = [0,0]


        self.mass = mass
        self.sum_force = force
        self.deformation_degree = deformation_degree
    
    def net_force(self, forces):
        #remote forces
        net_force = [0, 0]

        net_force = [sum(force[0] for force in forces), sum(force[1] for force in forces)]

        self.sum_force = net_force

        #print(self.sum_force)

    def update_movement(self):
        #Bruker Newtons andre lov

        self.acceleraiton = product( 1 / self.mass, self.sum_force) #Omformureling av F = m*a --> a = F/m #TODO SKALER MED TIDEN
        self.velocity = add(self.velocity, self.acceleraiton)
        self.direction = add(self.direction, self.velocity)

        self.x, self.y = step((self.x, self.y), self.direction)

        #print(f"\n Dette er akselerasjonsvektoren: {self.acceleraiton}, \n Dette er fartsvektoren: {self.velocity}, \n Dette er retningsvektoren: {self.direction}, \n Dette er den nye posisjonen: {self.x}, {self.y}")

    def draw(self, WIN):
        #Bør endres til case switch statments
        if self.shape == "circle":
            pygame.draw.circle(WIN, (255, 94, 5), (self.x, self.y), 50)
        
class string():
    def __init__(self, connections):
        self.connections = connections

    def draw(self, WIN):
        #Draw line between connection points (optional)
        pass
       

def draw_screen(WIN, objects, bg_color = (255,255,255)):

    WIN.fill(bg_color)

    for object in objects:
        object.draw(WIN)


    pygame.display.update()



def main():
    WIDTH, HEIGHT, WIN = init()
    g = [0, 9.818] # Grunnen til at det ikke er negativt er fordi (0,0) er øverst venstre ikke nederst venstre

    o = body(510, 50, 1, 0, 0, 5, 5, shape = "circle")

    objects = [o]

    clock = pygame.time.Clock()
    FPS = 1

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

        # Her trenger vi å beregne alle kreftene som virker på legemene
        
        for object in objects:
            forces = []
            forces.append(product(object.mass, g))


            #print(forces, type(forces))

            object.net_force(forces)

            object.update_movement()



        draw_screen(WIN, objects)
        clock.tick(FPS)

if __name__ == "__main__":
    main()