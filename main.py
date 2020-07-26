#!/usr/bin/env python3
"""

"""
import random as rd
import numpy as np
import itertools

from objet import *

# Partie 1 : Segments aléatoires
def construire_n_segments(n, width, height):
    return [segment_aleatoire(width, height) for _ in range(n)]

# def tracer_segments(segments, height, width):
#     for segment in segments:
#         segment.tracer_segment()

def tracer_segments(segments, height, width):
    svg = '<svg width="{}" height="{}">'.format(width, height)
    for segment in segments:
        svg += segment.tracer_segment()
    return svg + '</svg>'

# Partie 2 : symétrie
def symetrie(segment, width):
    point1 = Point(segment.point1.x + 2*abs( width - segment.point1.x), segment.point1.y)
    point2 = Point(segment.point2.x + 2*abs( width - segment.point2.x), segment.point2.y)
    return Segment(point1, point2)

def symetrie_segments(segments, width):
    return [symetrie(segment, width) for segment in segments]

# Partie 3 : rotation

def rotation_point(point, theta, origine):

    xd, yd = point.x, point.y
    xo, yo = origine[0], origine[1]
    xm, ym = xd - xo, yd - yo

    x = np.cos(theta) * xm + np.sin(theta) * ym + xo
    y = -np.sin(theta) * xm + np.cos(theta) * ym + yo
    return Point(x, y)

def rotation_segment(segment, theta, origine):
    return Segment(rotation_point(segment.point1, theta, origine), rotation_point(segment.point2, theta, origine))

def rotation_segments(segments, origine):
    nouveau_segments = []
    theta = 2*np.pi / 8
    for i in range(8):
        nouveau_segments += [rotation_segment(segment, theta*i, origine) for segment in segments]

    return nouveau_segments

# Partie 4 : clipage
def clipage(segments, height, width):

    width_limites = [width//3, 2*width//3]
    height_limites = [height//3, 2*height//3]
    for segment in segments:
        clipage_abscisse(segment, width_limites)
        clipage_ordonnee(segment, height_limites)

def clipage_abscisse(segment, width_limites):
    min_width, max_width = width_limites
    points = [segment.point1, segment.point2]
    for point in points:
        if point.x < min_width:
            point.x = min_width

        if point.x > max_width:
            point.x = max_width

def clipage_ordonnee(segment, height_limites):
    min_height, max_height = height_limites
    points = [segment.point1, segment.point2]
    for point in points:
        if point.y < min_height:
            point.y = min_height

        if point.y > max_height:
            point.y = max_height

# Partie 5: Segments élémentaires
def coef_directeur(segment):
    return (segment.point2.y - segment.point1.y)/(segment.point2.x - segment.point1.x)

def ordonnee_origine(segment, coef):
    return segment.point1.y - coef*segment.point1.x

def intersection_segments(couple_segment, height_limites, width_limites):
    segment1, segment2 = couple_segment

    # Verification des segments
    # Est ce qu'ils ont déjà en intersection avec d'autres segments ?
    if segment1.intersected and segment2.intersected:
        return

    # Est ce qu'il y a un segment qui est une droite verticale ?
    if segment1.point1.x == segment1.point2.x or segment2.point1.x == segment2.point2.x:
        return
    if segment1.point1.y == segment1.point2.y or segment2.point1.y == segment2.point2.y:
        return


    coef_dir_segment1 = coef_directeur(segment1)
    coef_dir_segment2 = coef_directeur(segment2)
    if coef_dir_segment1 == coef_dir_segment2:
        return
    ordonnee_origine_segment1 = ordonnee_origine(segment1, coef_dir_segment1)
    ordonnee_origine_segment2 = ordonnee_origine(segment2, coef_dir_segment2)

    intersection = (ordonnee_origine_segment2 - ordonnee_origine_segment1)/(coef_dir_segment1 - coef_dir_segment2)

    min_height, max_height = height_limites
    min_width, max_width = width_limites

    if min_width <= intersection <= max_width and min_height <= ordonnee_origine_segment1 + intersection*coef_dir_segment1 <= max_height:
        segment1.intersected = True
        segment2.intersected = True

        return

def segments_elementaires(segments, width, height):

    width_limites = [width//3, 2*width//3]
    height_limites = [height//3, 2*height//3]
    for couple_segment in itertools.combinations(segments, 2):
        intersection_segments(couple_segment, height_limites, width_limites)

    return [segment for segment in segments if segment.intersected]

# Partie 6: Translation x8
def translater_segment(segment, x_toTranslate, y_toTranslate):
    points = [segment.point1, segment.point2]

    point1, point2 = [Point(point.x + x_toTranslate, point.y + y_toTranslate) for point in points]

    return Segment(point1, point2)

def translation(segments, height, width):
    nouveaux_segments = []
    heights = [-height//3, 0, height//3]
    widths = [-width//3, 0, height//3]
    for x_toTranslate in widths:
        for y_toTranslate in heights:
            nouveaux_segments += [translater_segment(segment, x_toTranslate, y_toTranslate) for segment in segments]

    return nouveaux_segments

# Partie 7 : Suppressions degrés 1

def trouver_intersection(couple_segment):
    segment1, segment2 = couple_segment

    coef_dir_segment1 = coef_directeur(segment1)
    coef_dir_segment2 = coef_directeur(segment2)
    if coef_dir_segment2 == coef_dir_segment1:
        return
    ordonnee_origine_segment1 = ordonnee_origine(segment1, coef_dir_segment1)
    ordonnee_origine_segment2 = ordonnee_origine(segment2, coef_dir_segment2)

    intersection = (ordonnee_origine_segment2 - ordonnee_origine_segment1)/(coef_dir_segment1 - coef_dir_segment2)

    ord_origine = [ordonnee_origine_segment1, ordonnee_origine_segment2]
    coef_dir = [coef_dir_segment1, coef_dir_segment2]

    for index, segment in enumerate(couple_segment):
        x1, x2 = segment.point1.x, segment.point2.x
        y1, y2 = segment.point1.y, segment.point2.y
        x1_min, x1_max = min(x1, x2), max(x1, x2)
        y1_min, y1_max = min(y1, y2), max(y1, y2)

        if not (x1_min <= intersection <= x1_max and y1_min <= ord_origine[index] + coef_dir[index]*intersection <= y1_max):
            return []

    segment1.intersections.append(Point(intersection,ordonnee_origine_segment1 + coef_dir_segment1*intersection))
    segment2.intersections.append(Point(intersection, ordonnee_origine_segment2 + coef_dir_segment2*intersection))

def suppression_deg1_segment(segment):
    if len(segment.intersections) <= 1:
        return []

    if len(segment.intersections) == 2:
        return [Segment(*segment.intersections)]

    point1 = segment.intersections[0]
    return [Segment(point1, point2) for point2 in segment.intersections[1:]]

def suppression_deg1_segments(segments):
    nouveaux_segments = []
    for couple_segment in itertools.combinations(segments, 2):
        trouver_intersection(couple_segment)
    for segment in segments:
        nouveaux_segments += [element for element in suppression_deg1_segment(segment)]
    return nouveaux_segments


# main()
def motif(height = 800, width = 800, nombre_segments = 2):

    # Longueur Segment comprise entre 25% et 50% de la longueur total
    segment_width = (width//2 - width//4, width//2)
    # Hauteur Segment comprise entre 50% et 100% de la longueur total
    segment_height = (height//2, height)

    # Partie 1 : Segments aléatoires
    segments = construire_n_segments(nombre_segments, segment_width, segment_height)
    # tracer_segments(segments, height, width)

    # Partie 2 : symétrie
    segments_symetrie = symetrie_segments(segments, width//2)
    segments += segments_symetrie
    # tracer_segments(segments_symetrie)
    # tracer_segments(segments, height, width)

    # Partie 3 : rotation
    segments = rotation_segments(segments, (width//2, height//2))
    # tracer_segments(segments, height, width)

    # Partie 4 : clipage
    clipage(segments, height, width)
    # tracer_segments(segments, height, width)

    # Partie 5: Segments élémentaires
    segments = segments_elementaires(segments, height, width)
    # tracer_segments(segments, height, width)

    # Partie 6: Translation x8
    segments = translation(segments, height, width)
    # tracer_segments(segments, height, width)

    # Partie 7 : Suppressions degrés 1
    segments = suppression_deg1_segments(segments)
    return tracer_segments(segments, height, width)
