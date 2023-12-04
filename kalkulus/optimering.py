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
_QUALITY = {
    "ul": (6, 6),
    "l": (12, 12),
    "h": (48, 48)
}


class CylindersAreal(ThreeDScene, Slide if slides else Scene):
    def construct(self):
        cmap = {
            "r": RED,
            "h": BLUE,
            "OA": YELLOW
        }
        self.set_camera_orientation(phi=PI/8, zoom=0.125)
        V = 330
        r = ValueTracker(16.0)
        cylinder = always_redraw(lambda:
            Cylinder(
                radius=r.get_value(),
                height=V/(PI*r.get_value()*r.get_value()),
                direction=OUT,
                # stroke_color=RED,
                fill_color=cmap["r"],
                # resolution=(24, 24) if q == "h" else (8, 8)
                resolution=_QUALITY[q]
            ).move_to([0, 0, -5])
        )
        radius_and_height_text = always_redraw(lambda:
            VGroup(
                VGroup(
                    Tex("Radius ="), DecimalNumber(r.get_value())
                ).arrange(RIGHT).set(color=cmap["r"]),
                # VGroup(
                #     Tex("Højde ="), DecimalNumber(V / (PI * r.get_value() * r.get_value()))
                # ).arrange(RIGHT).set(color=cmap["h"]),
                VGroup(
                    Tex(f"Højde = {V / (PI * r.get_value() * r.get_value()):.2f}")
                ).arrange(RIGHT).set(color=cmap["h"]),
                VGroup(
                    Tex("Volumen ="), DecimalNumber(V)
                ).arrange(RIGHT),
                VGroup(
                    Tex("Overfladeareal ="), DecimalNumber(PI*r.get_value()*r.get_value() + V/(PI*r.get_value()))
                ).arrange(RIGHT).set(color=cmap["OA"])
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(DL)
        )
        self.add_fixed_in_frame_mobjects(radius_and_height_text)
        self.add(cylinder)
        self.move_camera(phi=PI/8, zoom=0.125)
        self.begin_ambient_camera_rotation(rate=0.5, about="theta")

        plane = NumberPlane(
            x_range=[0, 5, 0.5],
            y_range=[0, 120, 10],
            x_length=5,
            y_length=6,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).to_edge(DR)
        labels = plane.get_axis_labels(
            x_label=Tex("Radius", color=cmap["r"]),
            y_label=Tex("Overfladeareal", color=cmap["OA"])
        )
        plane[2].set_color(cmap["r"])
        plane[3].set_color(cmap["OA"])
        moving_dot = always_redraw(lambda:
            Dot(
                plane.c2p(r.get_value(), PI*r.get_value()*r.get_value() + V/(PI*r.get_value())),
                color=cmap["OA"]
            )
        )
        trace = TracedPath(moving_dot.get_center, color=cmap["OA"])
        self.add_fixed_in_frame_mobjects(plane, labels, moving_dot, trace)

        # self.wait(5)
        self.slide_pause(5)
        self.move_camera(phi=PI/4, zoom=0.125)
        # self.wait()
        self.slide_pause()
        self.play(
            r.animate.set_value(4.0),
            run_time=4
        )
        # self.wait(5)
        self.slide_pause(5)

        self.play(
            r.animate.set_value(1.5),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)
        self.play(
            r.animate.set_value(1.2825),
            run_time=2
        )
        # self.wait()
        self.slide_pause()
        self.play(
            r.animate.set_value(2.56),
            run_time=2
        )
        # self.wait(5)
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)


if __name__ == "__main__":
    class_name = CylindersAreal.__name__
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
