"""Game."""
import math
import random
import sys
from collections import defaultdict

import numpy as np
import pygame
from pygame.locals import *
from scipy import constants

DENSITY = 0.001

WIDTH, HEIGHT = 900, 600
WIDTHD2, HEIGHTD2 = WIDTH / 2., HEIGHT / 2.
TEST = np.array([WIDTHD2, HEIGHTD2])


class Particle:
    def __init__(self, name, radius):
        self.name = name
        self.radius = radius
        self.merged = False
        self.state = State(np.random.rand(
            2,), np.random.randint(0, 300, 2) / 20)


class State:
    def __init__(self, position, velocity):
        self._position = position
        self._velocity = velocity


class Derivative:
    def __init__(self, velocity, acceleration):
        self._velocity = velocity
        self._acceleration = acceleration


class Universe:
    def __init__(self):
        self.particle_list = list()

    def add_body(self, particle):
        self.set_mass_from_radius(particle)
        self.particle_list.append(particle)

    def update_particles(self, dt):
        for particle in self.particle_list:
            if particle.merged or particle.name == 'sun':
                continue
            handler = HandleParticle(
                particle, self.particle_list)
            handler.update(dt)

    def get_distance(self, particle1, particle2):
        position1 = particle1.state._position
        position2 = particle2.state._position
        distance = np.linalg.norm(position2 - position1)
        return distance

    def merge_range(self, particle):
        if not particle.merged:
            for other in self.particle_list:
                if particle is other or other.merged:
                    continue
                distance = self.get_distance(particle, other)
                widths = particle.radius + other.radius
                if distance <= widths:
                    return [particle, other]
        return False

    def merge(self, particles):
        particle1 = particles[0]
        particle2 = particles[1]
        if particle1.mass < particle2.mass:
            particle1, particle2 = particle2, particle1
        particle2.merged = True
        new_velocity = (particle1.state._velocity * particle1.mass +
                        particle2.state._velocity * particle2.mass) / (
                            particle1.mass + particle2.mass)
        particle1.mass += particle2.mass
        self.set_radius_from_mass(particle1)
        particle1.state._velocity = new_velocity

    def set_mass_from_radius(self, particle):
        particle.mass = DENSITY * 4. * math.pi * (particle.radius ** 3) / 3

    def set_radius_from_mass(self, particle):
        particle.radius = (3. * particle.mass /
                           (DENSITY * 4. * math.pi)) ** (0.3333)


class HandleParticle(Universe):
    def __init__(self, particle, particle_list):
        self.particle = particle
        self.particle_list = particle_list

    def acceleration(self, state):
        acceleration = np.zeros([2])
        for other in self.particle_list:
            if self.particle is other or self.particle.merged:
                continue
            position = other.state._position - state._position
            distance_squared = np.square(position)
            distance_sum = np.sum(distance_squared)
            distance = np.sqrt(distance_sum)
            force = (1000 * self.particle.mass *
                     other.mass) / distance_sum
            acceleration += (force * position) / distance
        return acceleration

    def initial_derivative(self):
        acceleration = self.acceleration(self.particle.state)
        return Derivative(self.particle.state._velocity, acceleration)

    def next_derivative(self, derivative, dt):
        state = State(np.array([0., 0.]), np.array([0., 0.]))
        state._position = self.particle.state._position + derivative._velocity * dt
        state._velocity = self.particle.state._velocity + derivative._acceleration * dt
        acceleration = self.acceleration(state)
        return Derivative(state._velocity, acceleration)

    def update(self, dt):
        k1 = self.initial_derivative()
        k2 = self.next_derivative(k1, dt * 0.5)
        k3 = self.next_derivative(k2, dt * 0.5)
        k4 = self.next_derivative(k3, dt)
        velocity = (1 / 6) * (k1._velocity + 2
                              * (k2._velocity + k3._velocity)
                              + k4._velocity)
        acceleration = (1 / 6) * (k1._acceleration + 2
                                  * (k2._acceleration + k3._acceleration)
                                  + k4._acceleration)
        self.particle.state._position += velocity * dt
        self.particle.state._velocity += acceleration * dt


def main_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Spaaaaaaace')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 30, 30))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    universe = Universe()
    planets = list()
    for i in range(20):
        radius = random.randint(2, 3)
        planets.append(Particle("planet{}".format(i), radius))
        planets[i].state._position = np.array(
            [random.randint(1, WIDTH), random.randint(1, HEIGHT)], dtype='float64')
        universe.add_body(planets[i])
        print(planets[i].state._position)
    # allsprites = pygame.sprite.RenderPlain((moon, earth))
    sun = Particle("sun", 15)
    sun.state._position = np.array([WIDTHD2, HEIGHTD2], dtype='float64')
    sun.state._velocity = np.array([0, 0])
    universe.add_body(sun)
    sun.mass = 1000
    universe.set_radius_from_mass(sun)
    planets.append(sun)

    zoom = 1.0
    dt = 1

    keysPressed = defaultdict(bool)

    def ScanKeyboard():
        while True:
            # Update the keysPressed state:
            evt = pygame.event.poll()
            if evt.type == pygame.NOEVENT:
                break
            elif evt.type in [pygame.KEYDOWN, pygame.KEYUP]:
                keysPressed[evt.key] = evt.type == pygame.KEYDOWN
    bClearScreen = True
    while True:
        if bClearScreen:
            screen.fill((0, 0, 0))

        universe.update_particles(dt)

        for planet in planets:
            particles = universe.merge_range(planet)
            if particles:
                universe.merge(particles)
            if not planet.merged:
                position = planet.state._position.astype(int)
                radius = planet.radius
                # print(earth.state._position)
                # print(radius)
                pygame.draw.circle(
                    screen, (255, 255, 255),
                    (TEST + zoom * TEST * (position - TEST) / TEST).astype(int).tolist(),
                    int(radius * zoom))

        ScanKeyboard()

        pygame.display.flip()
        # for event in pygame.event.get():
        if keysPressed[pygame.K_KP_PLUS]:
            zoom /= 0.99
        if keysPressed[pygame.K_KP_MINUS]:
            zoom /= 1.01
        if keysPressed[pygame.K_ESCAPE]:
            break
        if keysPressed[pygame.K_SPACE]:
            while keysPressed[pygame.K_SPACE]:
                ScanKeyboard()
            bClearScreen = not bClearScreen
        # while True:
        #     event = pygame.event.poll()
        #     if event.type == NOEVENT:
        #         break
        #     if event.type == QUIT:
        #         sys.exit()
        #     elif event.type in [KEYDOWN, KEYUP]:
        #         if event.key == K_KP_PLUS:
        #             zoom /= 0.99
        #         if event.key == K_KP_MINUS:
        #             zoom /= 1.01


if __name__ == '__main__':
    main_game()
