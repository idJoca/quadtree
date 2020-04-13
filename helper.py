from pygame import Vector2


class Helper():

    @staticmethod
    def is_point_between_rect(top_left: Vector2, bottom_right: Vector2, point: Vector2):
        temp = Vector2(top_left.x, top_left.y)
        temp_top_left = Vector2(top_left.x, top_left.y)
        temp_bottom_right = Vector2(bottom_right.x, bottom_right.y)

        if top_left.x > bottom_right.x:
            temp_top_left.x = temp_bottom_right.x
            temp_bottom_right.x = temp.x

        if top_left.y > bottom_right.y:
            temp_top_left.y = temp_bottom_right.y
            temp_bottom_right.y = temp.y

        return (point.x >= temp_top_left.x and point.x <= temp_bottom_right.x) and (point.y >= temp_top_left.y and point.y <= temp_bottom_right.y)

    @staticmethod
    def is_point_outside_rect(top_left: Vector2, bottom_right: Vector2, point: Vector2):
        return Helper.is_point_between_rect(top_left, bottom_right, point) is False
