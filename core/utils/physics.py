import numpy
from scipy import constants


class Physics:
    def __init__(self):
        pass

    def get_distance(self, body1, body2):
        position1 = body1.position
        position2 = body2.position
        distance = numpy.linalg.norm(position2 - position1)
        return distance

    def acceleration(self, body, other):
        position = other.position - body.state_position
        distance_squared = numpy.square(position)
        distance_sum = numpy.sum(distance_squared)
        distance = numpy.sqrt(distance_sum)
        force = (constants.G * self.body.mass *
                 other.mass) / distance_sum
        body.state_acceleration += (force * position) / distance
        return body.state_acceleration
