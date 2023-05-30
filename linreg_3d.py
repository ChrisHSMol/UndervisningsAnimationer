from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class LinReg3D(ThreeDScene):
    def construct(self):
        # self.errorfield()
        self.test3d()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def errorfield(self):
        xmin, xmax, xstep = 10, 14, 1
        ymin, ymax, ystep = 8, 12, 1
        zmin, zmax, zstep = 0, 20, 2
        plane = ThreeDAxes(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            z_range=[zmin, zmax, zstep],
            x_length=4,
            y_length=4,
            z_length=4,
            # background_line_style={
            #     "stroke_color": TEAL,
            #     "stroke_width": 2,
            #     "stroke_opacity": 0.3
            # },
            # axis_config={"include_numbers": True}
        )

        a, b = 12, 10
        # data_points = []
        # for x, y in zip(
        #         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        #         [10, 22, 30, 48, 62, 68, 76, 95, 104, 120, 125]
        # ):
        #     data_points.append((x, y, 0))
        # data_points = np.array(data_points)

        errorfield = VGroup()
        for x in np.linspace(a-2, a+2, 10):
            for y in np.linspace(b-2, b+2, 10):
                errorfield.add(
                    Dot3D(
                        plane.c2p(x, y, (y - a*x - b)**2),
                        radius=0.01
                    )
                )

        self.add(plane, errorfield)
        self.begin_ambient_camera_rotation(about="theta")
        self.wait(5)
        self.stop_ambient_camera_rotation()

    def test3d(self):
        axes = ThreeDAxes(
            x_range=(0.9, 1.3, 0.1),
            y_range=(0.9, 1.3, 0.1),
            z_range=(-1, 15, 1)
        )

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        data_points = []
        for x, y in zip(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [1, 2.2, 3.0, 4.8, 6.2, 6.8, 7.6, 9.5, 10.4, 12.0, 12.5]
        ):
            data_points.append((x, y))
        data_points = np.array(data_points)

        # 3D variant of the Dot() object
        dot = Dot3D(axes.c2p(0, 0, 0))

        # zoom out so we see the axes
        self.set_camera_orientation(
            phi=0,
            zoom=0.5
        )

        self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # dots = VGroup(
        #     *[
        #         VGroup(
        #             *[
        #                 Dot3D(
        #                     # TODO: indfør punkter og beregn z-værdien som summen af kvadrerede afvigelser
        #                     # axes.c2p(x, y, (1 - 1.2*x - 1)**2),
        #                     # color=interpolate_color(BLUE, RED, 1/((1 - 1.2*x - 1)**2))
        #                     axes.c2p(a, b, np.sum([(p[1] - a*p[0] - b)**2 for p in data_points])),
        #                     color=interpolate_color(BLUE, RED, 1 / (np.sum([(p[1] - a*p[0] - b)**2 for p in data_points])+1)),
        #                     radius=0.02
        #                 ) for b in np.linspace(0.8, 1.2, 20)
        #             ]
        #         ) for a in np.linspace(1.0, 1.4, 20)
        #     ]
        # )
        # self.play(FadeIn(dots))
        # self.add(dots)
        def param_surface(u, v):
            x = u
            y = v
            # z = np.sin(x) * np.cos(y)
            z = min(15, np.sum([(p[1] - x*p[0] - y)**2 for p in data_points]))
            return z
        print(param_surface(1.15, 0.95))
        print(param_surface(1.25, 1.05))
        surface = Surface(
            lambda u, v: axes.c2p(u, v, param_surface(u, v)),
            # resolution=(resolution_fa, resolution_fa),
            v_range=[1.15, 1.25],
            u_range=[0.95, 1.05],
            )
        self.add(surface)

        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(
            phi=75 * DEGREES,
            theta=30 * DEGREES,
            zoom=1,
            run_time=1.5
        )

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(
            # about="gamma",
            rate=1.5
        )
        self.wait(2)
        self.stop_ambient_camera_rotation()
