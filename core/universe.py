"""Game."""
import sys

import numpy as np
import pygame
from pygame.locals import *
from scipy import constants


class Particle(pygame.sprite.Sprite):
    def __init__(self, name, mass, position, velocity, acceleration):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.merged = False
        self.state = State(np.random.rand(2,), np.random.rand(2,))


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
        self.dt = 1

    def add_body(self, particle):
        self.particle_list.append(particle)

    def update_particles(self):
        for particle in self.particle_list:
            handler = HandleParticle(particle, self.particle_list)
            handler.update(self.dt)


class HandleParticle(Universe):
    def __init__(self, particle, particle_list):
        self.particle = particle
        self.particle_list = particle_list

    def acceleration(self, state):
        acceleration = np.zeros([2, 2])
        for other in self.particle_list:
            if self.particle is other or self.particle.merged:
                continue
            position = other.state._position - state._position
            distance_squared = np.square(position)
            distance_sum = np.sum(distance_squared)
            distance = np.sqrt(distance_sum)
            force = (self.particle.mass *
                     other.mass) / distance_squared
            acceleration += (force * position) / distance
        return acceleration

    def initial_derivative(self, state):
        acceleration = self.acceleration(state)
        return Derivative(state._velocity, acceleration)

    def next_derivative(self, initial_state, derivative, dt):
        state = State(np.array([0., 0.]), np.array([0., 0.]))
        state._position = initial_state._position + derivative._velocity * dt
        state._velocity = initial_state._velocity + derivative._acceleration * dt
        acceleration = self.acceleration(state)
        return Derivative(state._velocity, acceleration)

    def update(self, dt):
        k1 = self.initial_derivative(self.particle.state)
        k2 = self.next_derivative(self.particle.state, k1, dt * 0.5)
        k3 = self.next_derivative(self.particle.state, k2, dt * 0.5)
        k4 = self.next_derivative(self.particle.state, k3, dt)
        velocity = (1 / 6) * (k1._velocity + 2 *
                              (k2._velocity + k3._velocity) + k4._velocity)
        acceleration = (1 / 6) * (k1._acceleration + 2 *
                                  (k2._acceleration
                                   + k3._acceleration) + k4._acceleration)
        self.particle.state._position = velocity * dt
        self.particle.state._velocity = acceleration * dt


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



    earth = Particle('Earth', 53232, np.random.rand(2,), np.random.rand(2,), np.random.rand(2,))
    earth.position = np.array([120, 480], dtype='float64')
    moon = Particle('Moon', 9333222233, np.random.rand(2,), np.random.rand(2,), np.random.rand(2,))
    moon.position = np.array([480, 480], dtype='float64')

    universe = Universe()
    universe.add_body(earth)
    universe.add_body(moon)
    allsprites = pygame.sprite.RenderPlain((moon, earth))
    clock = pygame.time.Clock()

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

        # for i, planet in enumerate(planets):
        #     for j, other_planet in enumerate(planets):
        #         if planet != other_planet:
        #             print(planet.position)
        #             universe.force_g(planet, other_planet)

        #     universe.update(planet)
        universe.update_particles()
        print(earth.position)
        # earth.position += universe.total_vectors(earth, moon)
        # earth.velocity = universe.total_vectors(earth, moon)

        # earth_x, earth_y = earth.position
        # moon_x, moon_y = moon.position

        # earth_xv, earth_yv = earth.velocity
        # print(earth.velocity)
        position = earth.position.astype(int)
        print(position)
        pygame.draw.circle(screen, RED, position.tolist(), 5)
        position = moon.position.astype(int)
        pygame.draw.circle(screen, RED, position.tolist(), 10)

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
