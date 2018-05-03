"""Game."""
import sys

import numpy as np
import pygame
from pygame.locals import *
from scipy import constants


class CelestialBody(pygame.sprite.Sprite):
    def __init__(self, name, mass,
                 position=np.zeros(2, dtype=np.longdouble),
                 velocity=np.zeros(2, dtype=np.longdouble)):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = np.zeros(2, dtype=np.longdouble)

        self.FORCE_FACTOR = constants.G * self.mass
        self.VELOCITY_FACTOR = 100 / self.mass


class Universe:
    def __init__(self):
        self.i = 0
        self.bodies = list()

    def add_body(self, object):
        self.bodies.append(object)

    def object_movement(self, object):
        current_movement = object.movement

    def get_distance(self, object1, object2):
        distance = object1.position - object2.position
        return distance

    def get_gravity_force(self, object1, object2):
        mass1 = object1.mass
        mass2 = object2.mass
        distance = self.get_distance(object1, object2)
        # distance = np.linalg.norm(distance)
        force1 = (constants.G * mass1 * mass2) / np.square(distance[0])
        force2 = (constants.G * mass1 * mass2) / np.square(distance[1])
        if force1 == float('inf'):
            force1 = 0
        if force2 == float('inf'):
            force2 = 0
        force = np.array([force1, force2])
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

    def total_vectors(self, object1, object2):
        gravity = self.get_gravity_force(object1, object2)
        # print(gravity)
        # print(gravity)
        # print(velocity)
        return gravity

    # def update_forces(self, object1, object2):
    #     dist = object1.pos - object2.pos
    #     vector_distance = np.linalg.norm(dist)

    #     # Caculate common force of gravity
    #     g_com = (
    #         constants.G * object1.mass * object2.mass) / (vector_distance ** 2)

    #     object1.forces -= np.array([g_com * dist])

    def update(self, body):
        """Step up the simulation based on force calculations."""
        # Step up velocity and position
        body.velocity += np.dot(body.force, body.VELOCITY_FACTOR)
        body.position += np.dot(body.velocity, 100)

        # Reset force profile
        body.force = np.zeros(3, dtype=np.longdouble)

    def force_g(self, body, other_body):
        """Update the force the body has on this craft."""
        dist = body.position - other_body.position
        gravity_component = (body.FORCE_FACTOR * other_body.mass /
                             ((dist[0]**2 + dist[1]**2)**1.5))

        # Update forces array
        print(dist)
        print(gravity_component)
        body.force -= np.dot(dist, gravity_component)


def main_game():
    pygame.init()
    screen = pygame.display.set_mode((960, 960))
    pygame.display.set_caption('Spaaaaaaace')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    earth = CelestialBody('Earth', 53232, np.array([0, 0]))
    earth.position = np.array([120, 480], dtype='float64')
    moon = CelestialBody('Moon', 9333222233, np.array([0, 0]))
    moon.position = np.array([480, 480], dtype='float64')

    universe = Universe()
    universe.add_body(earth)
    universe.add_body(moon)
    allsprites = pygame.sprite.RenderPlain((moon, earth))
    clock = pygame.time.Clock()

    distance = universe.get_distance(earth, moon)

    vector1 = earth.velocity
    vector2 = moon.velocity

    earth_x, earth_y = earth.position
    earth.velocity = np.array([0, 200], dtype='float64')
    earth_x *= 960
    earth_y *= 960

    planets = [earth, moon]

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    while True:
        clock.tick(60)
        screen.fill((255, 255, 255))

        for i, planet in enumerate(planets):
            for j, other_planet in enumerate(planets):
                if planet != other_planet:
                    print(planet.position)
                    universe.force_g(planet, other_planet)

            universe.update(planet)
        # earth.position += universe.total_vectors(earth, moon)
        # earth.velocity = universe.total_vectors(earth, moon)

        # earth_x, earth_y = earth.position
        # moon_x, moon_y = moon.position

        # earth_xv, earth_yv = earth.velocity
        # print(earth.velocity)
        pygame.draw.circle(screen, RED, [int(earth_x), int(earth_y)], 5)
        # pygame.draw.circle(screen, RED, [int(moon_x), int(moon_y)], 10)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()


if __name__ == '__main__':
    main_game()
