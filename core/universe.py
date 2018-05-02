"""Game."""
import numpy as np
from scipy import constants


class Planet:
    def __init__(self, name, mass, coords, movement, velocity):
        self.name = name
        self.movement = movement
        self.coords = coords
        self.mass = mass
        self.velocity = velocity

    def new_vector_movement(self, other):
        # self.movement = 
        pass


class Universe:
    def __init__(self):
        self.objects = list()

    def add_object(self, object):
        self.objects.append(object)

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

    def total_vectors(self, vectors):
        output = 0
        for vector in vectors:
            output += vector
        return output


if __name__ == '__main__':
    earth = Planet('Earth', 5972, np.array([-5, 1]), np.array([5, -2]), 1)
    moon = Planet('Moon', 7348, np.array([1, 0]), np.array([15, 20]), 5)

    universe = Universe()
    universe.add_object(earth)
    universe.add_object(moon)

    distance = universe.get_distance(earth, moon)
    print(distance)
    norm = universe.vector_normalize(distance)
    print(norm)
    direction = universe.vector_direction(distance, norm)
    print(direction)
    velocity = universe.vector_gravity(direction, norm)
    # print(velocity)

    vector1 = earth.movement
    vector2 = moon.movement
    vectors = np.array([vector1, vector2])

    result = universe.total_vectors(vectors)
    print(result)
