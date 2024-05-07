import sys
sys.path.append("../")
from manim import *
# from manim_chemistry import *
from custom_classes import BohrAtom
from helpers import *
import random
import subprocess

slides = True
if slides:
    from manim_slides import Slide

q = "l"
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


class BueSekund(MovingCameraScene, Scene if not slides else Slide):
    def construct(self):
        self.slide_pause()
        self.buesekund()
        fade_out_all(self)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def buesekund(self):
        self.camera.frame.set(
            height=2.5
        )
        plane = NumberPlane(
            x_range=[-1.1, 1.1, 0.1],
            y_range=[-1.1, 1.1, 0.1],
            background_line_style={"stroke_width": 0.1},
            stroke_width=0.25
        )
        circle = Circle(radius=1, stroke_color=WHITE, stroke_width=0.5).set_z_index(2)
        angle_tracker = ValueTracker(0)
        tracked_angle = always_redraw(lambda:
            Arc(
                radius=circle.radius,
                start_angle=0,
                angle=angle_tracker.get_value(),
                color=RED,
                stroke_width=1
            ).set_z_index(circle.get_z_index() + 1)
        )
        self.play(
            DrawBorderThenFill(plane),
            Create(circle)
        )
        self.slide_pause()
        self.add(tracked_angle)

        vinkel = always_redraw(lambda:
            VGroup(
                DecimalNumber(angle_tracker.get_value() * 180/PI, num_decimal_places=2, color=tracked_angle.get_color()),
                MathTex(r"^\circ", color=tracked_angle.get_color())
            ).scale(0.5).arrange(RIGHT, aligned_edge=UP, buff=0).next_to(circle, RIGHT).shift(0.25*UP)
        )
        self.play(
            FadeIn(vinkel)
        )
        self.slide_pause()

        self.play(
            angle_tracker.animate.set_value(6),
            run_time=3
        )
        self.wait()
        self.play(
            angle_tracker.animate.set_value(1*DEGREES),
            run_time=2
        )
        self.slide_pause()

        self.play(
            self.camera.frame.animate.set(height=0.1).move_to(tracked_angle),
            FadeOut(plane),
            run_time=2
        )
        self.slide_pause()

        buetime = Tex(r"Buetime = $1^\circ$", font_size=1).next_to(tracked_angle, UR, buff=0).set_z_index(6)
        self.play(
            FadeIn(buetime),
            run_time=1
        )
        self.wait()
        self.play(
            FadeOut(buetime),
            run_time=1
        )
        self.slide_pause()

        bueminut_tracker = ValueTracker(0)
        bueminut = always_redraw(lambda:
            Arc(
                radius=circle.radius,
                start_angle=0,
                angle=bueminut_tracker.get_value() * DEGREES / 60,
                color=YELLOW,
                stroke_width=0.25
            ).set_z_index(tracked_angle.get_z_index() + 1)
        )
        self.add(bueminut)
        self.play(
            bueminut_tracker.animate.set_value(60),
            run_time=2
        )
        self.wait()
        self.play(
            bueminut_tracker.animate.set_value(1)
        )

        self.play(
            self.camera.frame.animate.set(height=0.005).move_to(bueminut),
            run_time=2
        )
        self.slide_pause()

        bueminut_tekst = Tex(r"Bueminut = $\frac{1}{60}^\circ$", font_size=0.05).next_to(bueminut, UR, buff=0).set_z_index(10)
        self.play(
            FadeIn(bueminut_tekst),
            run_time=1
        )
        self.wait()
        self.play(
            FadeOut(bueminut_tekst),
            run_time=1
        )
        self.slide_pause()

        buesekund_tracker = ValueTracker(0)
        buesekund = always_redraw(lambda:
            Arc(
                radius=circle.radius,
                start_angle=0,
                angle=buesekund_tracker.get_value() * DEGREES / 3600,
                color=BLUE,
                stroke_width=0.01
            ).set_z_index(tracked_angle.get_z_index() + 1)
        )
        self.add(buesekund)
        self.play(
            buesekund_tracker.animate.set_value(60),
            run_time=2
        )
        self.wait()
        self.play(
            buesekund_tracker.animate.set_value(1)
        )

        self.play(
            self.camera.frame.animate.set(height=0.0005).move_to(buesekund),
            run_time=2
        )
        self.slide_pause()

        buesekund_tekst = Tex(
            r"Buesekund = $\frac{1}{3600}^\circ$", color=BLACK, font_size=0.005
        ).next_to(buesekund, UR, buff=0).set_z_index(6)
        self.play(
            FadeIn(buesekund_tekst),
            run_time=1
        )
        self.wait()
        self.play(
            FadeOut(buesekund_tekst),
            run_time=1
        )
        self.slide_pause()


if __name__ == "__main__":
    cls = BueSekund
    class_name = cls.__name__
    # transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
