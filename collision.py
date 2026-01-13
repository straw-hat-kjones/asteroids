import pygame


def point_in_triangle(point, triangle):
    """Check if a point is inside a triangle using barycentric coordinates"""
    p = pygame.Vector2(point)
    a, b, c = [pygame.Vector2(v) for v in triangle]

    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def point_to_segment_distance(point, seg_start, seg_end):
    """Calculate minimum distance from point to line segment"""
    p = pygame.Vector2(point)
    a = pygame.Vector2(seg_start)
    b = pygame.Vector2(seg_end)

    ab = b - a
    ap = p - a

    # Project point onto line, clamping to segment
    ab_len_sq = ab.length_squared()
    if ab_len_sq == 0:
        return (p - a).length()

    t = max(0, min(1, ap.dot(ab) / ab_len_sq))

    # Closest point on segment
    closest = a + ab * t

    return (p - closest).length()


def circle_intersects_triangle(center, radius, triangle):
    """Check if a circle intersects with a triangle"""
    center = pygame.Vector2(center)

    # Check if center is inside triangle
    if point_in_triangle(center, triangle):
        return True

    # Check distance from center to each edge
    tri = [pygame.Vector2(v) for v in triangle]
    edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]

    for p1, p2 in edges:
        # Distance from center to line segment
        dist = point_to_segment_distance(center, p1, p2)
        if dist < radius:
            return True

    return False
