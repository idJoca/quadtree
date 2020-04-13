from quad_tree2d import QuadTree2D
from pygame import Surface, Rect, Vector2
from pygame.draw import rect as draw_rect


class DrawableQuadTree2D(QuadTree2D):

    def __init__(self, top_left: Vector2, bottom_right: Vector2, sub_type=None):
        super().__init__(top_left, bottom_right, DrawableQuadTree2D)

    def draw(self, canvas: Surface):
        draw_rect(canvas, (255, 255, 255), Rect(
            self.top_left.x, self.top_left.y, self.width, self.height), 1)

        if self.subdivided:
            self.top_left_quad.draw(canvas)
            self.bottom_left_quad.draw(canvas)
            self.top_right_quad.draw(canvas)
            self.bottom_right_quad.draw(canvas)
