from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = True
if slides:
    from manim_slides import Slide
q = "h"
_RESOLUTION = {
    "ul": "426,240",
    "l": "854,480",
    "h": "1920,1080"
}
_FRAMERATE = {
    "ul": 5,
    "l": 15,
    "h": 60
}
_slowdown_factor = 1


class CoinRotationParadox(MovingCameraScene, Slide if slides else Scene):
    def _construct(self):
        r1, r2 = 1, 1
        circle1 = Circle(radius=r1)
        circle2 = Circle(radius=r2).next_to(circle1, UP, buff=0)
        dot = always_redraw(lambda: Dot(color=YELLOW).move_to(circle2.get_start()))
        trace = TracedPath(dot.get_center)
        circle2.add_updater(lambda m: m.rotate(1/(circle1.radius + circle2.radius + 1)))
        # circle2.add_updater(lambda m, dt: m.rotate(r2/r1 + 1))
        self.add(circle1, circle2, dot, trace)
        self.play(
            MoveAlongPath(circle2, Circle(radius=r1 + r2).rotate(PI)),
            run_time=r1 + r2,
            rate_func=rate_functions.linear
        )

    def construct(self):
        r1, r2 = 4, 1
        circle1 = Circle(radius=r1)
        circle2 = VGroup(Circle(radius=r2).next_to(circle1, LEFT, buff=0))
        # for i, v in enumerate(np.linspace(0, 2*PI, 9)):
        #     _col = BLUE if i == 0 else interpolate_color(YELLOW, WHITE, 0.5)
        #     circle2.add(
        #         Dot().set(color=_col).move_to(circle2[0].point_at_angle(v))
        #     )
        # circle2.add(Line(start=circle2[0].get_center(), end=circle2[0].get_start(), stroke_color=BLUE))
        circle2.add(
            *[
                Dot(
                    color=interpolate_color(YELLOW, WHITE, 0.5) if v != 0.0 else BLUE
                ).move_to(
                    circle2[0].point_at_angle(v)
                ) for v in np.linspace(0, 2*PI, 9)
            ],
            Line(start=circle2[0].get_center(), end=circle2[0].get_start())
        )
        trace = TracedPath(circle2[1].get_center, stroke_color=BLUE, stroke_opacity=[0.5, 1])

        self.play(
            self.camera.frame.animate.set(
                height=2 * (r1 + r2 + 2)
            ),
            # ).move_to(circle2),
            run_time=0.1
        )
        # self.camera.frame.set(height=2*(r1 + r2) + 1)

        def _untilwaiter():
            return (circle2[-1].get_end() - circle2[-1].get_start() == RIGHT).all()

        _omega1 = 1 / _FRAMERATE[q] * _slowdown_factor
        _omega2 = (r1/r2) / _FRAMERATE[q] * _slowdown_factor
        circle2.add_updater(lambda m: m.rotate(_omega2))
        circle2.add_updater(lambda m: m.rotate(_omega1, about_point=ORIGIN))
        # self.camera.frame.add_

        self.add(circle1, circle2, trace)
        self.wait(60)
        # self.wait(2*PI)
        # self.pause()
        # circle1.set(radius=3)
        # self.wait(60-2*PI)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)


if __name__ == "__main__":
    class_name = CoinRotationParadox.__name__
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
