from pygame import Vector2
from helper import Helper


class QuadTree2D():
    LIMIT_SIZE = 5

    def __init__(self, top_left: Vector2, bottom_right: Vector2, sub_type):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.point_ids = set([]) 
        self.subdivided = False
        self.sub_type = sub_type

        # Quadrants
        self.top_left_quad = None
        self.bottom_left_quad = None
        self.top_right_quad = None
        self.bottom_right_quad = None

        self.setup()

    def setup(self, top_left=None, bottom_right=None):
        """
        Defines some constans, that are quadrant dependent
        """
        if top_left is not None:
            self.top_left = top_left

        if bottom_right is not None:
            self.bottom_right = bottom_right

        # Relative sizes
        self.width = self.bottom_right.x - self.top_left.x
        self.height = self.bottom_right.y - self.top_left.y

        # Center Point
        self.middle_point = self.top_left + \
            Vector2(self.width / 2, self.height / 2)

        # Horizontally Centered Points
        self.middle_left_point = Vector2(
            self.middle_point.x - self.width / 2, self.middle_point.y)
        self.middle_right_point = Vector2(
            self.middle_point.x + self.width / 2, self.middle_point.y)

        # Vertically Centered Points
        self.middle_top_point = Vector2(
            self.middle_point.x, self.middle_point.y - self.height / 2)
        self.middle_bottom_point = Vector2(
            self.middle_point.x, self.middle_point.y + self.height / 2)

        if self.subdivided:
            self.subdivide()

    def subdivide(self):
        if self.top_left_quad is None:
            self.top_left_quad = self.sub_type(
                self.top_left, self.middle_point, self.sub_type)
        else:
            self.top_left_quad.setup(self.top_left, self.middle_point)

        if self.bottom_left_quad is None:
            self.bottom_left_quad = self.sub_type(
                self.middle_left_point, self.middle_bottom_point, self.sub_type)
        else:
            self.bottom_left_quad.setup(
                self.middle_left_point, self.middle_bottom_point)

        if self.top_right_quad is None:
            self.top_right_quad = self.sub_type(
                self.middle_top_point, self.middle_right_point, self.sub_type)
        else:
            self.top_right_quad.setup(
                self.middle_top_point, self.middle_right_point)

        if self.bottom_right_quad is None:
            self.bottom_right_quad = self.sub_type(
                self.middle_point, self.bottom_right, self.sub_type)
        else:
            self.bottom_right_quad.setup(self.middle_point, self.bottom_right)

        self.subdivided = True

    def insert_point(self, point_index: int, point_position: Vector2) -> bool:
        if Helper.is_point_outside_rect(self.top_left, self.bottom_right, point_position):
            return False

        if len(self.point_ids) >= QuadTree2D.LIMIT_SIZE and self.subdivided is False:
            self.subdivide()

        if self.subdivided:
            # This seems silly, but because, by definition, we'll always have four quadrants
            # There is no need to put this in a list and make it dynamic
            if self.top_left_quad.insert_point(point_index, point_position) is True:
                return True
            if self.bottom_left_quad.insert_point(point_index, point_position) is True:
                return True
            if self.top_right_quad.insert_point(point_index, point_position) is True:
                return True
            if self.bottom_right_quad.insert_point(point_index, point_position) is True:
                return True
        else:
            self.point_ids.add(point_index)

        return True

    def contains_point(self, point_index: int):
        if point_index in self.point_ids:
            return True

        if self.subdivided:
            return (self.top_left_quad.contains_point(point_index) or
                    self.bottom_left_quad.contains_point(point_index) or
                    self.top_right_quad.contains_point(point_index) or
                    self.bottom_right_quad.contains_point(point_index))

        return False

    def get_point_inside_a_rect(self, top_left: Vector2, bottom_right: Vector2, points_dict: dict):
        inside_points = {}

        for point in self.point_ids:
            if Helper.is_point_between_rect(top_left, bottom_right, points_dict[point]):
                inside_points[point] = points_dict[point]

        if self.subdivided:
            inside_points.update(self.top_left_quad.get_point_inside_a_rect(
                top_left, bottom_right, points_dict))
            inside_points.update(self.bottom_left_quad.get_point_inside_a_rect(
                top_left, bottom_right, points_dict))
            inside_points.update(self.top_right_quad.get_point_inside_a_rect(
                top_left, bottom_right, points_dict))
            inside_points.update(self.bottom_right_quad.get_point_inside_a_rect(
                top_left, bottom_right, points_dict))

        return inside_points
