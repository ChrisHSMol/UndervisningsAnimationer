import sys
sys.path.append("../")
from manim import *
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class SpejledeFunktioner(ThreeDScene, Slide if slides else Scene):
    def construct(self):
        self.slide_pause()
        self.invers_funktion()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def invers_funktion(self):
        # plane = NumberPlane(
        #     x_range=[-5.5, 5.5, 1],
        #     y_range=[-5.5, 5.5, 1],
        #     x_length=5.5,
        #     y_length=5.5,
        #     background_line_style={
        #         "stroke_color": TEAL,
        #         "stroke_width": 0.5,
        #         "stroke_opacity": 0.5,
        #     },
        # ).set_z_index(3)
        plane = ThreeDAxes(
            x_range=[-5.5, 5.5, 1],
            y_range=[-5.5, 5.5, 1],
            z_range=[-0.01, 0.01, 0.01],
            x_length=10,
            y_length=10,
            z_length=0.01,
            z_axis_config={"include_tip": False}
        )
        # plane_rect = get_background_rect(plane, buff=0, stroke_colour=RED, fill_opacity=0)
        # _screen_rect = VGroup(*[
        #     get_background_rect(
        #         plane, buff=10, fill_opacity=1
        #     ).set_z_index(4).next_to(plane, d, buff=0) for d in [UP, DOWN, LEFT, RIGHT]
        # ])
        # self.add(_screen_rect, plane_rect)
        pcol = YELLOW
        picol = interpolate_color(pcol, invert_color(pcol), 0.5)
        sw = 2.0

        functions = VGroup(
            plane.plot(lambda x: x + 2, color=pcol, stroke_width=sw, x_range=[-11, 11]),
            plane.plot(lambda x: x * 2, color=pcol, stroke_width=sw, x_range=[-11, 11]),
            plane.plot(lambda x: x ** 2, color=pcol, stroke_width=sw, x_range=[-11, 11]),
            plane.plot(lambda x: 2 ** x, color=pcol, stroke_width=sw, x_range=[-11, 11]),
        )
        functions_inverse = VGroup(
            plane.plot(lambda x: x - 2, color=picol, stroke_width=sw, x_range=[-11, 11]),
            plane.plot(lambda x: x / 2, color=picol, stroke_width=sw, x_range=[-11, 11]),
            VGroup(
                plane.plot(lambda x: np.sqrt(x), color=picol, stroke_width=sw, x_range=[0, 11]),
                plane.plot(lambda x: -np.sqrt(x), color=picol, stroke_width=sw, x_range=[0, 11])
            ),
            plane.plot(lambda x: np.log2(x), color=picol, stroke_width=sw, x_range=[1E-2, 11]),
        )
        function_names = VGroup(
            VGroup(
                MathTex("f(x)=x + 2", color=pcol).move_to(plane.c2p(-4, 4)),
                MathTex("g(x)=x - 2", color=picol).move_to(plane.c2p(4, -4))
            ),
            VGroup(
                MathTex(r"f(x)=2 \cdot x", color=pcol).move_to(plane.c2p(-4, 4)),
                MathTex(r"g(x)={1\over2} \cdot x", color=picol).move_to(plane.c2p(4, -4))
            ),
            VGroup(
                MathTex("f(x)=x^2", color=pcol).move_to(plane.c2p(-4, 4)),
                MathTex(r"g(x)=\sqrt{x}", color=picol).move_to(plane.c2p(4, -4))
            ),
            VGroup(
                MathTex("f(x)=2^x", color=pcol).move_to(plane.c2p(-4, 4)),
                MathTex(r"g(x)=\log_2(x)", color=picol).move_to(plane.c2p(4, -4))
            ),
        )
        mirror_line = plane.plot(lambda x: x, color=WHITE)

        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                Create(mirror_line),
                lag_ratio=0.5
            )
        )
        self.move_camera(phi=60*DEGREES)
        self.move_camera(theta=-3*PI/4)
        self.slide_pause()

        for f, fi, fname in zip(functions, functions_inverse, function_names):
            # break
            # self.begin_ambient_camera_rotation(rate=0.04)
            # self.begin_ambient_camera_rotation(rate=0.05, about="phi")
            self.play(
                Create(f),
                Create(fi) if len(fi) == 1 else Create(fi[::-1]),
                Write(fname, lag_ratio=0),
                run_time=0.5
            )
            self.wait()

            self.play(
                Rotate(
                    VGroup(plane.copy(), f.copy()).set_z_index_by_z_coordinate(),
                    angle=PI, axis=UR, about_point=plane.c2p(0, 0)
                ),
                run_time=6
            )
            self.slide_pause()

            # self.play(*[FadeOut(m) for m in self.mobjects if m not in [plane, plane_rect, _screen_rect]])
            self.play(*[FadeOut(m) for m in self.mobjects if m not in [plane, mirror_line]])
            # self.stop_ambient_camera_rotation()
            # self.move_camera(phi=60*DEGREES)
            # break

        self.play(
            Uncreate(plane, lag_ratio=0.33),
            Uncreate(mirror_line),
        )
