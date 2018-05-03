"""Game."""
import sys

import numpy as np
import pygame
from pygame.locals import *
from scipy import constants


class AstronomicalBody(pygame.sprite.Sprite):
    def __init__(self, name, mass, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.coords = None
        self.mass = mass
        self.velocity = velocity
        
    def new_vector_movement(self, other):
        # self.movement = 
        pass


class Universe:
    def __init__(self):
        self.i = 0
        self.bodies = list()

    def add_body(self, object):
        self.bodies.append(object)

    def object_movement(self, object):
        current_movement = object.movement

    def get_distance(self, object1, object2):
        distance = np.array(object1.coords - object2.coords)
        return distance

    def get_gravity_force(self, object1, object2):
        mass1 = object1.mass
        mass2 = object2.mass
        distance = self.get_distance(object1, object2)
        force = (constants.G * mass1 * mass2) / np.square(distance)
        return force

    def vector_normalize(self, distance):
        norm = np.sqrt(distance[0] ** 2 + distance[1] ** 2)
        return norm

    def vector_direction(self, distance, norm):
        direction = np.array([distance[0] / norm, distance[1] / norm])
        return direction

    def vector_gravity(self, direction, norm):
        gravtity = np.array([direction[0] * norm, direction[1] * norm])
        return gravtity

    def total_vectors(self, object):
        vector = object.coords + np.array([self.i, 1])
        return vector


def main_game():
    pygame.init()
    screen = pygame.display.set_mode((1280, 1280))
    pygame.display.set_caption('Spaaaaaaace')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    earth = AstronomicalBody('Earth', 5972, np.array([5, -2]))
    earth.coords = np.random.rand(2)
    moon = AstronomicalBody('Moon', 7348, np.array([15, 20]))
    moon.coords = np.random.rand(2)

    universe = Universe()
    universe.add_body(earth)
    universe.add_body(moon)
    allsprites = pygame.sprite.RenderPlain((moon, earth))
    clock = pygame.time.Clock()


    distance = universe.get_distance(earth, moon)

    vector1 = earth.velocity
    vector2 = moon.velocity
    vectors = np.array([vector1, vector2])

    earth_x, earth_y = earth.coords
    earth_x *= 1280
    earth_y *= 1280


    BLACK = ( 0, 0, 0)
    WHITE = ( 255, 255, 255)
    GREEN = ( 0, 255, 0)
    RED = ( 255, 0, 0)

    while True:
        clock.tick(60)
        screen.fill((255, 255, 255))

        result = universe.total_vectors(earth)
        earth.coords = result

        earth_x, earth_y = earth.coords
        universe.i = 1

        pygame.draw.circle(screen, RED, [int(earth_x), int(earth_y)], 5)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()


if __name__ == '__main__':
    main_game()
