import random as rd

class Point():
    """docstring fo Point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

def point_aleatoire(width, height):
    return Point(rd.randint(width[0], width[1]), rd.randint(height[0], height[1]))


class Segment():
    """docstring for Segment."""
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.intersected = False
        self.intersections = []

    def tracer_segment(self):
        return '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="red"/>'.format(self.point1.x, self.point1.y, self.point2.x, self.point2.y)

def segment_aleatoire(width, height):
    p1 = point_aleatoire(width, height)
    p2 = point_aleatoire(width, height)
    return Segment(p1, p2)
