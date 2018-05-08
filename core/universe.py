"""Game."""
import math
import random
from collections import defaultdict

import numpy as np
import pygame

DENSITY = 0.001

WIDTH, HEIGHT = 900, 600
WIDTHD2, HEIGHTD2 = WIDTH / 2., HEIGHT / 2.
TEST = np.array([WIDTHD2, HEIGHTD2])


class CelestialBody:
    def __init__(self, name, radius):
        self.name = name
        self.radius = radius
        self.merged = False
        self.position = np.random.randint(2,)
        self.velocity = np.random.randint(-300, 300, 2) / 1000


class Derivative:
    def __init__(self, velocity, acceleration):
        self.velocity = velocity
        self.acceleration = acceleration


class Universe:
    def __init__(self):
        self.body_list = list()

    def add_body(self, body):
        self.set_mass_from_radius(body)
        self.body_list.append(body)

    def update_bodies(self, dt):
        for body in self.body_list:
            if body.merged or body.name == 'sun':
                continue
            handler = bodyHandler(body, self.body_list)
            handler.update(dt)

    def merge_range(self, body):
        if not body.merged:
            for other in self.body_list:
                if body is other or other.merged:
                    continue
                distance = self.get_distance(body, other)
                widths = body.radius + other.radius
                if distance <= widths:
                    return [body, other]
        return False

    def merge(self, bodies):
        body1 = bodies[0]
        body2 = bodies[1]
        if body1.mass < body2.mass:
            body1, body2 = body2, body1
        body2.merged = True
        new_velocity = (body1.velocity * body1.mass +
                        body2.velocity * body2.mass) / (
                            body1.mass + body2.mass)
        body1.mass += body2.mass
        self.set_radius_from_mass(body1)
        body1.velocity = new_velocity

    def set_mass_from_radius(self, body):
        body.mass = DENSITY * 4. * math.pi * (body.radius ** 3) / 3

    def set_radius_from_mass(self, body):
        body.radius = (3. * body.mass /
                       (DENSITY * 4. * math.pi)) ** (0.3333)


class bodyHandler(Universe):
    def __init__(self, body, body_list):
        self.body = body
        self.body_list = body_list

    def acceleration(self, self_position):
        body.state_acceleration = np.zeros([2])
        for other in self.body_list:
            if self.body is other or self.body.merged:
                continue
            position = other.position - self_position
            distance_squared = np.square(position)
            distance_sum = np.sum(distance_squared)
            distance = np.sqrt(distance_sum)
            force = (10 * self.body.mass *
                     other.mass) / distance_sum
            acceleration += (force * position) / distance
        return acceleration

    def initial_derivative(self):
        acceleration = self.acceleration(self.body.position)
        return Derivative(self.body.velocity, acceleration)

    def next_derivative(self, derivative, dt):
        position = self.body.position + derivative.velocity * dt
        velocity = self.body.velocity + derivative.acceleration * dt
        acceleration = self.acceleration(position)
        return Derivative(velocity, acceleration)

    def update(self, dt):
        k1 = self.initial_derivative()
        k2 = self.next_derivative(k1, dt * 0.5)
        k3 = self.next_derivative(k2, dt * 0.5)
        k4 = self.next_derivative(k3, dt)
        velocity = (1 / 6) * (k1.velocity + 2
                              * (k2.velocity + k3.velocity)
                              + k4.velocity)
        acceleration = (1 / 6) * (k1.acceleration + 2
                                  * (k2.acceleration + k3.acceleration)
                                  + k4.acceleration)
        self.body.position += velocity * dt
        self.body.velocity += acceleration * dt
        if self.body.position[0] > WIDTH:
            self.body.position[0] -= WIDTH
        if self.body.position[0] < 0:
            self.body.position[0] += WIDTH
        if self.body.position[1] > HEIGHT:
            self.body.position[1] -= HEIGHT
        if self.body.position[1] < 0:
            self.body.position[1] += HEIGHT


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
        radius = random.randint(4, 5)
        planets.append(CelestialBody("planet{}".format(i), radius))
        planets[i].position = np.array(
            [random.randint(1, WIDTH), random.randint(1, HEIGHT)], dtype='float64')
        universe.add_body(planets[i])
        planets[i].mass = 1
    # allsprites = pygame.sprite.RenderPlain((moon, earth))
    # sun = body("sun", 15)
    # sun.position = np.array([WIDTHD2, HEIGHTD2], dtype='float64')
    # sun.velocity = np.array([0, 0])
    # universe.add_body(sun)
    # sun.mass = 1000
    # universe.set_radius_from_mass(sun)
    # planets.append(sun)

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

        universe.update_bodies(dt)

        for planet in planets:
            bodies = universe.merge_range(planet)
            if bodies:
                universe.merge(bodies)
            if not planet.merged:
                position = planet.position.astype(int)
                radius = planet.radius
                pygame.draw.circle(
                    screen, (255, 255, 255),
                    (TEST + zoom * TEST * (position - TEST) /
                        TEST).astype(int).tolist(),
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


if __name__ == '__main__':
    main_game()
