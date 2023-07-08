from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np
from scipy.optimize import curve_fit

# try:
#     from manim_slides import Slide
#     slides = True
# except:
#     slides = False
slides = True
if slides:
    from manim_slides import Slide

cmap = {
    "lin": RED_C,
    "exp": GREEN_C,
    "pow": BLUE_C
}


def potensfunktion(x, a, b):
    return b*np.power(x, a)


def eksponentialfunktion(x, a, b):
    return b*np.power(a, x)


def linearfunktion(x, a, b):
    return a*x+b


class LinExpPow(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.analyse()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def analyse(self):
        self.slide_pause()
        np.random.seed(42)
        alin, blin = ValueTracker(0.75), ValueTracker(0.0)
        aexp, bexp = ValueTracker(1.40), ValueTracker(0.5)
        apow, bpow = ValueTracker(2.0), ValueTracker(0.1)

        xlim, ylim = [-0.5, 7.5], [-0.25, 5.75]
        plane_base = NumberPlane(
            x_range=xlim,
            y_range=ylim,
            x_length=4,
            y_length=3,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).set_z_index(2)
        planes = VGroup(*[
            plane_base.copy().to_edge(edge).shift(0.25*DOWN) for edge in [UL, UP, UR]
        ])
        plane_rects = VGroup(*[
            get_background_rect(
                plane, stroke_colour=cmap[c], buff=0.01, stroke_width=1.5
            ) for plane, c in zip(planes, ["lin", "exp", "pow"])
        ])
        self.play(
            LaggedStart(
                DrawBorderThenFill(planes),
                DrawBorderThenFill(plane_rects),
                lag_ratio=1
            ),
            run_time=2
        )
        plane_labels = VGroup(*[
            Tex(label, color=cmap[c]).set_z_index(2).next_to(plane, UP, buff=0.01) for label, c, plane in zip(
                ["Lineær", "Eksponentiel", "Potens"],
                ["lin", "exp", "pow"],
                planes
            )
        ])
        self.play(
            Write(plane_labels)
        )
        self.slide_pause()

        scene_marker("Generer 3 datasæt")
        xs = np.linspace(0.5, 6.5, 9)
        ys = np.array([
            alin.get_value()*xs+blin.get_value(),
            bexp.get_value()*aexp.get_value()**xs,
            bpow.get_value()*xs**apow.get_value()
        ])

        for yvals, label, ieq in zip(ys, ["lin", "exp", "pow"], range(len(planes))):
            dots = VGroup(*[
                VGroup(*[
                    Dot(
                        plane.c2p(x, y), radius=0.05
                    ).set_z_index(2) for x, y in zip(xs, yvals)
                ]) for plane in planes
            ])
            self.play(
                Create(
                    dots
                ),
                run_time=1
            )
            self.slide_pause()

            # regressions = np.array([
            #     np.polyfit(xs, yvals, 1),
            #     np.exp(np.polyfit(xs, np.log(yvals), 1)),
            #     np.polyfit(xs, yvals**(1/apow.get_value()), 1)
            # ])
            regressions = np.array([
                np.polyfit(xs, yvals, 1),
                np.exp(np.polyfit(xs, np.log(yvals), 1)),
                # curve_fit(f=potensfunktion, xdata=xs, ydata=yvals)[0]
                [apow.get_value(), bpow.get_value()]
            ])
            graphs = VGroup(
                planes[0].plot(
                    lambda x: regressions[0, 0] * x + regressions[0, 1],
                    x_range=xlim,
                    color=cmap["lin"]
                ).set_z_index(2),
                planes[1].plot(
                    lambda x: regressions[1, 1] * regressions[1, 0]**x,
                    x_range=xlim,
                    color=cmap["exp"]
                ).set_z_index(2),
                planes[2].plot(
                    # lambda x: regressions[2, 1] * x**regressions[2, 0],
                    lambda x: potensfunktion(x, *regressions[2]),
                    x_range=xlim,
                    color=cmap["pow"]
                ).set_z_index(2)
            )
            self.play(
                Create(graphs),
                run_time=2
            )
            self.slide_pause()
            self.play(
                Circumscribe(
                    VGroup(planes[ieq], plane_rects[ieq], plane_labels[ieq]),
                    fade_out=True
                ),
                run_time=2
            )
            self.slide_pause()

            self.play(
                FadeOut(dots),
                FadeOut(graphs)
            )
