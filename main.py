from BaseCanvas import BaseCanvas
from drawable_quad_tree2d import DrawableQuadTree2D
from pygame import Vector2, MOUSEBUTTONDOWN, MOUSEBUTTONUP, Rect
from pygame.event import Event
from pygame.draw import circle, rect as draw_rect
from pygame.mouse import get_pos as mouse_pos


class Main(BaseCanvas):

    def init_hook(self):
        self.quad = DrawableQuadTree2D(
            Vector2(0, 0), Vector2(self.width, self.height))

    def setup_hook(self):
        self.points = {}
        self.selected_points = []
        self.mouse_pressed = False
        self.point_buffer = 0
        self.rect_selection = None

    def loop_hook(self):
        if self.mouse_pressed:
            if self.point_buffer % 1 == 0:
                self.points[self.point_buffer] = Vector2(mouse_pos())
                self.quad.insert_point(self.point_buffer, self.points[self.point_buffer])
            self.point_buffer += 1

        if self.rect_selection is not None:
            self.select_points()
            rect_size = Vector2(mouse_pos()) - self.rect_selection
            draw_rect(self.canvas, (20, 250, 40), Rect(self.rect_selection.x, self.rect_selection.y,
                                                       rect_size.x, rect_size.y), 1)

        # self.canvas.lock()
        self.quad.draw(self.canvas)
        for point in self.points:
            if point in self.selected_points:
                color = (220, 255, 100)
            else:
                color = (120, 120, 120)
            circle(self.canvas, color, self.points[point], 3)
        # self.canvas.lock()

        print('pts: %i | sel. pts: %i | FPS: %.2f' % (len(self.points), len(self.selected_points), self.clock.get_fps()))

    def handle_events_hook(self, event: Event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # Left mouse button
                self.mouse_pressed = True
            if event.button == 3:
                # Right mouse button
                self.rect_selection = Vector2(event.pos)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                # Left mouse button
                self.mouse_pressed = False
            if event.button == 3:
                # Right mouse button
                self.rect_selection = None

    def select_points(self):
        self.selected_points = self.quad.get_point_inside_a_rect(
            self.rect_selection, Vector2(mouse_pos()), self.points)

    def resize_hook(self):
        self.quad.setup(bottom_right=self.screen_size)


if __name__ == "__main__":
    main = Main()
    main.loop()
