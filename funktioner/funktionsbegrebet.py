from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

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


class FunktionsBegrebet(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        cmap = self.get_cmap()
        title = Tex("Funktionsbegrebet, {{Dm}}({{f}}) og {{Vm}}({{f}})").set_color_by_tex_to_color_map(cmap)
        play_title2(self, title)
        self.funktionsbegrebet()
        fade_out_all(self)
        # self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def get_cmap(self):
        cmap = {
            "x": BLUE,
            "y": YELLOW
        }
        cmap["x_axis"] = interpolate_color(cmap["x"], WHITE, 0.625)
        cmap["y_axis"] = interpolate_color(cmap["y"], WHITE, 0.625)
        cmap["f"] = interpolate_color(cmap["x"], cmap["y"], 0.5)
        cmap["Dm"] = cmap["x"]
        cmap["Vm"] = cmap["y"]
        return cmap

    def get_plane(self, x, y, width):
        cmap = self.get_cmap()
        xmin, xmax, xstep = x
        ymin, ymax, ystep = y
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=9/16 * width,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.15
            },
            axis_config={
                "include_numbers": True,
                "include_ticks": True,
                "font_size": 24,
                "line_to_number_buff": 0.15
            },
            x_axis_config={
                "label_direction": DOWN,
                "color": cmap["x_axis"],
                "decimal_number_config": {
                    # "color": cmap["x"],
                    "num_decimal_places": 0
                },
            },
            y_axis_config={
                "label_direction": LEFT,
                "color": cmap["y_axis"],
                "decimal_number_config": {
                    # "color": cmap["y"],
                    "num_decimal_places": 0
                }
            }
        )
        return plane

    def funktionsbegrebet(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = -4, 12, 1
        ymin, ymax, ystep = -9, 9, 1
        width = 14
        plane = self.get_plane(
            x=(xmin, xmax, xstep),
            y=(ymin, ymax, ystep),
            width=width
        )
        self.play(
            DrawBorderThenFill(plane)
        )
        self.slide_pause()

        _par = (
            0.17619047619, -1.47142857143, 2.32380952381, 3.97142857143 # (-1, 0) (1, 5) (4, 1) (6, 3)
        )
        # x_low, x_high = ValueTracker(-3), ValueTracker(8)
        x_low, x_high = ValueTracker(xmin), ValueTracker(xmax)
        f_opacity = ValueTracker(1)
        f = always_redraw(lambda:
            plane.plot(
                # lambda x: _par[0]*x**3 + _par[1]*x**2 + _par[2]*x + _par[3],
                lambda x: sum([_par[i] * x**(3-i) for i in range(4)]),
                stroke_color=cmap["f"],
                x_range=(x_low.get_value(), x_high.get_value()),
                stroke_opacity=f_opacity.get_value()
            )
        )
        self.play(
            Create(f)
        )
        self.slide_pause()

        self.begreber(plane, f, f_opacity, x_low, x_high, (xmin, xmax, ymin, ymax))

        scan_tracker = ValueTracker(-4)
        scanning_line = always_redraw(lambda:
            DashedLine(
                start=plane.c2p(scan_tracker.get_value(), -9),
                end=plane.c2p(scan_tracker.get_value(), 9),
                stroke_color=cmap["x"]
            )
        )
        scanning_point = always_redraw(lambda:
            Dot(
                plane.c2p(scan_tracker.get_value(), f.underlying_function(scan_tracker.get_value())),
                fill_color=cmap["f"],
                radius=0.1
            )
        )
        funktions_tekst = VGroup(
            Tex("En {{funktion}} kræver at alle").set_color_by_tex_to_color_map(cmap),
            Tex("{{x}} i {{definitionsmængden}} har").set_color_by_tex_to_color_map(cmap),
            Tex("præcist én tilhørende {{y}}").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        funktions_tekst[1][2].set_color(cmap["Dm"])
        funktions_tekst_box = get_background_rect(funktions_tekst)
        VGroup(funktions_tekst_box, funktions_tekst).to_edge(DR, buff=0)
        self.play(
            Write(funktions_tekst),
            FadeIn(funktions_tekst_box),
            Create(scanning_line, run_time=0.25),
            Create(scanning_point, run_time=0.25)
        )
        self.slide_pause()

        self.play(
            scan_tracker.animate.set_value(8),
            run_time=10,
            rate_func=rate_functions.linear
        )
        self.slide_pause()

        self.ikke_funktion()

        self.play(
            x_low.animate.set_value(-1),
            x_high.animate.set_value(6),
            *[FadeOut(m, run_time=0.5) for m in [scanning_line, scanning_point, funktions_tekst, funktions_tekst_box]],
            run_time=3
        )
        self.slide_pause()

        self.definitionsmaengde(plane, f, f_opacity, x_low, x_high)
        self.vaerdimaengde(plane, f, f_opacity, x_low, x_high)
        self.opsamlet(f, x_low, x_high)

    def begreber(self, plane, f, f_opacity, x_low, x_high, lims):
        scene_marker("Begreber")
        cmap = self.get_cmap()
        xmin, xmax, ymin, ymax = lims
        dm_tekst = VGroup(
            Tex("{{Definitionsmængden, Dm,}} er alle de").set_color_by_tex_to_color_map(cmap),
            Tex("{{$x$}}-værdier, som har en {{$y$}}-værdi").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        dm_tekst_box = get_background_rect(dm_tekst)
        VGroup(dm_tekst_box, dm_tekst).to_edge(DR, buff=0)
        self.play(
            *[FadeIn(m) for m in [dm_tekst, dm_tekst_box]]
        )

        dots = VGroup(
            *[
                Dot(plane.c2p(x, 0), fill_color=cmap["x"], radius=0.08) for x in np.arange(
                    x_low.get_value(), x_high.get_value()+0.01, 0.25
                )
            ]
        )
        _dots = VGroup(
            *[
                Dot(plane.c2p(x, f.underlying_function(x)), fill_color=cmap["x"], radius=0.08) for x in np.arange(
                    x_low.get_value(), x_high.get_value()+0.01, 0.25
                )
            ]
        )
        dotlines = always_redraw(lambda:
            VGroup(*[
                DashedLine(
                    start=(dot.get_x(), plane.c2p(0, 0)[1], 0),
                    end=dot.get_center(),
                    stroke_color=color_gradient((cmap["x"], cmap["f"]), 3),
                    stroke_width=2,
                    dashed_ratio=0.5
                ) for dot in dots
            ])
        )
        self.add(dotlines)
        self.play(
            Create(dots)
        )
        self.play(
            LaggedStart(
                *[
                    dot.animate.move_to(_dot).set_style(fill_color=cmap["f"]) for dot, _dot in zip(dots, _dots)
                ],
                lag_ratio=0.1
            ),
            run_time=10
        )
        self.slide_pause()

        dm_tekst_fuld = VGroup(
            Tex("Selvom grafen her kun er vist i intervallet [-4; 12],"),
            Tex(r"er {{Dm}} her alle tal, dvs. intervallet {{$]-\infty; \infty[$}}."),
            Tex(r"Dette kan også skrives {{$\mathbb{R}$}}.")
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        dm_tekst_fuld[1][1].set_color(cmap["Dm"])
        dm_tekst_fuld[1][3].set_color(cmap["Dm"])
        dm_tekst_fuld[2][1].set_color(cmap["Dm"])
        dm_tekst_fuld_box = get_background_rect(dm_tekst_fuld)
        VGroup(dm_tekst_fuld_box, dm_tekst_fuld).to_edge(DR, buff=0)
        self.play(
            *[FadeIn(m) for m in [dm_tekst_fuld, dm_tekst_fuld_box]],
            *[FadeOut(m) for m in [dm_tekst, dm_tekst_box]],
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m) for m in [*dots, *dotlines]],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause()

        dm_hul = VGroup(
            Tex("Hvis der er et hul i grafen, fjerner man"),
            Tex("{{$x$}}-værdier fra {{Dm}}")
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        dm_hul[1][0].set_color(cmap["x"])
        dm_hul[1][2].set_color(cmap["Dm"])
        dm_hul_box = get_background_rect(dm_hul)
        VGroup(dm_hul_box, dm_hul).to_edge(DR, buff=0)
        f_hul = plane.plot(
            lambda x: f.underlying_function(x),
            stroke_color=cmap["f"],
            x_range=(x_low.get_value(), x_high.get_value()),
            discontinuities=[4.5],
            dt=0.5
        )
        self.play(
            *[FadeIn(m) for m in [dm_hul, dm_hul_box]],
            *[FadeOut(m) for m in [dm_tekst_fuld, dm_tekst_fuld_box]],
            f_opacity.animate.set_value(0),
            FadeIn(f_hul),
            run_time=0.5
        )
        self.slide_pause()

        dm_tekst_hul = VGroup(
            Tex(r"{{Dm}} er alle tal undtagen intervallet {{$[4; 5]$}}."),
            Tex(r"Det skrives enten som {{$]-\infty; 4[ \quad\wedge\quad ]5; \infty[$}}"),
            Tex(r"eller som {{$\mathbb{R} \setminus [4; 5]$}}.")
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        dm_tekst_hul[0][0].set_color(cmap["Dm"])
        dm_tekst_hul[0][2].set_color(cmap["Dm"])
        dm_tekst_hul[1][1].set_color(cmap["Dm"])
        dm_tekst_hul[2][1].set_color(cmap["Dm"])
        dm_tekst_hul_box = get_background_rect(dm_tekst_hul)
        VGroup(dm_tekst_hul_box, dm_tekst_hul).to_edge(DR, buff=0)
        self.play(
            *[FadeOut(m) for m in [dm_hul, dm_hul_box]],
            *[FadeIn(m) for m in [dm_tekst_hul, dm_tekst_hul_box]],
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            *[
                FadeOut(m) for m in [dm_tekst_hul, dm_tekst_hul_box, f_hul]
            ],
            f_opacity.animate.set_value(1),
            run_time=0.5
        )

        vm_tekst = VGroup(
            Tex("{{Værdimængden, Vm,}} er alle de").set_color_by_tex_to_color_map(cmap),
            Tex("{{$y$}}-værdier, som {{$f$}} kan producere").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        vm_tekst_box = get_background_rect(vm_tekst)
        VGroup(vm_tekst_box, vm_tekst).to_edge(DR, buff=0)
        self.play(
            *[FadeIn(m) for m in [vm_tekst, vm_tekst_box]]
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in [vm_tekst, vm_tekst_box]]
        )

        # _xs = []
        # _ys = []
        # for x in np.arange(xmin, xmax + 0.01, 0.25):
        #     if f.underlying_function(x) not in _ys:
        #         _xs.append(x)
        #         _ys.append(f.underlying_function(x))
        # dots = VGroup(
        #     *[
        #         Dot(plane.c2p(0, y), fill_color=cmap["y"], radius=0.08) for y in _ys
        #     ]
        # )
        # _dots = VGroup(
        #     *[
        #         Dot(plane.c2p(x, y)) for x, y in zip(_xs, _ys)
        #     ]
        # )
        # dotlines = always_redraw(lambda:
        #     VGroup(*[
        #         DashedLine(
        #             start=(plane.c2p(0, 0)[0], dot.get_y(), 0),
        #             end=dot.get_center(),
        #             stroke_color=color_gradient((cmap["y"], cmap["f"]), 3),
        #             stroke_width=2,
        #             dashed_ratio=0.5
        #         ) for dot in dots
        #     ])
        # )
        # self.add(dotlines)
        # self.play(
        #     Create(dots)
        # )
        # self.play(
        #     LaggedStart(
        #         *[
        #             dot.animate.move_to(_dot).set_style(fill_color=cmap["f"]) for dot, _dot in zip(dots, _dots)
        #         ],
        #         lag_ratio=0.1
        #     ),
        #     run_time=10
        # )
        # self.slide_pause()

    def definitionsmaengde(self, plane, f, f_opacity, x_low, x_high):
        scene_marker("Definitionsmængde")
        cmap = self.get_cmap()
        begr_dm_tekst = Tex(r"Når {{definitionsmængden}} er begrænset\\tegner man prikker for enden").set_z_index(5)
        begr_dm_tekst[1].set_color(cmap["Dm"])
        begr_dm_tekst_box = get_background_rect(begr_dm_tekst)
        VGroup(begr_dm_tekst_box, begr_dm_tekst).to_edge(DR, buff=0)
        end_opacities = (ValueTracker(1), ValueTracker(1))
        endpoints = always_redraw(lambda:
            VGroup(*[
                Dot(
                    radius=0.1, fill_color=interpolate_color(BLACK, cmap["f"], end_opacities[i].get_value()),
                    stroke_color=GREEN, fill_opacity=1, stroke_width=2 * (1-end_opacities[i].get_value())
                ).move_to(
                    plane.c2p(x.get_value(), f.underlying_function(x.get_value()))
                ) for i, x in enumerate([x_low, x_high])
            ])
        )
        self.play(
            FadeIn(begr_dm_tekst),
            FadeIn(begr_dm_tekst_box),
            DrawBorderThenFill(endpoints),
            run_time=0.5
        )
        self.slide_pause()

        dm_collapse = always_redraw(lambda:
            Line(
                start=plane.c2p(x_low.get_value(), 0), end=plane.c2p(x_high.get_value(), 0),
                stroke_color=cmap["Dm"], stroke_width=7
            )
        )
        axlines = always_redraw(lambda:
            VGroup(
                DashedLine(
                    start=dm_collapse.get_start(),
                    end=endpoints[0].get_center(),
                    stroke_color=cmap["x"]
                ),
                DashedLine(
                    start=dm_collapse.get_end(),
                    end=endpoints[1].get_center(),
                    stroke_color=cmap["x"]
                )
            )
        )
        self.play(
            ReplacementTransform(f.copy(), dm_collapse)
        )
        self.play(
            f_opacity.animate.set_value(0.25),
            Create(axlines)
        )
        self.slide_pause()

        dm_brace = always_redraw(lambda:
            Brace(dm_collapse, DOWN, color=dm_collapse.get_color(), buff=1)
        )
        dm_brace_tekst = always_redraw(lambda:
            VGroup(
                MathTex(r"{{Dm}}({{f}}) = ").set_color_by_tex_to_color_map(cmap),
                MathTex("[" if end_opacities[0].get_value() else "]"),
                    # f"{x_low.get_value():.2f}",
                DecimalNumber(x_low.get_value(), color=cmap["x"]),
                MathTex("; "),
                    # f"{x_high.get_value():.2f}",
                DecimalNumber(x_high.get_value(), color=cmap["x"]),
                MathTex("]" if end_opacities[1].get_value() else "[")
                # ).set_color_by_tex_to_color_map(cmap).next_to(dm_brace, DOWN)
            ).arrange(RIGHT).next_to(dm_brace, DOWN).set_z_index(5)
        )
        dm_brace_tekst_box = always_redraw(lambda: get_background_rect(dm_brace_tekst))
        self.play(
            DrawBorderThenFill(dm_brace),
            Write(dm_brace_tekst),
            FadeIn(dm_brace_tekst_box)
        )
        self.slide_pause()

        self.play(
            x_high.animate.set_value(7),
            run_time=5
        )
        self.play(
            x_high.animate.set_value(2),
            run_time=5
        )
        self.play(
            x_high.animate.set_value(6),
            x_low.animate.set_value(-2),
            run_time=5
        )
        self.play(
            x_low.animate.set_value(-1),
            run_time=2
        )
        self.slide_pause()

        endpoint_forklaring = VGroup(
            VGroup(
                Tex("En {{fyldt}} cirkel betyder, at tallet er {{inkluderet}}"),
                endpoints[0].copy()
            ).arrange(RIGHT),
            VGroup(
                Tex("En {{tom}} cirkel betyder, at tallet er {{ekskluderet}}"),
                endpoints[0].copy().set_style(fill_color=BLACK, stroke_width=1)
            ).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=RIGHT).set_z_index(5)
        endpoint_forklaring[0][0][1].set_style(stroke_color=cmap["f"], fill_color=cmap["f"])
        endpoint_forklaring[0][0][3].set_style(stroke_color=cmap["f"], fill_color=cmap["f"])
        endpoint_forklaring[1][0][1].set_style(stroke_color=cmap["f"], stroke_width=0.5, fill_color=BLACK)
        endpoint_forklaring[1][0][3].set_style(stroke_color=cmap["f"], stroke_width=0.5, fill_color=BLACK)
        endpoint_forklaring_box = get_background_rect(endpoint_forklaring)
        VGroup(endpoint_forklaring_box, endpoint_forklaring).to_edge(DR, buff=0)
        self.play(
            LaggedStart(
                LaggedStart(
                    *[FadeOut(m, shift=RIGHT) for m in (begr_dm_tekst, begr_dm_tekst_box)], lag_ratio=0.1
                ),
                LaggedStart(
                    *[FadeIn(m, shift=RIGHT) for m in (endpoint_forklaring, endpoint_forklaring_box)], lag_ratio=0.1
                ),
                lag_ratio=0.5
            )
        )

        self.play(
            end_opacities[1].animate.set_value(0),
            run_time=0.1
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m) for m in [
                    endpoints, dm_brace, dm_collapse, dm_brace_tekst, dm_brace_tekst_box, endpoint_forklaring,
                    endpoint_forklaring_box,
                    axlines
                ]],
                f_opacity.animate.set_value(1),
                lag_ratio=0.1
            )
        )

    def vaerdimaengde(self, plane, f, f_opacity, x_low, x_high):
        scene_marker("Værdimængde")
        cmap = self.get_cmap()
        end_opacities = (ValueTracker(1), ValueTracker(1))
        endpoints = always_redraw(lambda:
            VGroup(*[
                Dot(
                    radius=0.1, fill_color=interpolate_color(BLACK, cmap["f"], end_opacities[i].get_value()),
                    stroke_color=GREEN, fill_opacity=1, stroke_width=2 * (1-end_opacities[i].get_value())
                ).move_to(
                    plane.c2p(x.get_value(), f.underlying_function(x.get_value()))
                ) for i, x in enumerate([x_low, x_high])
            ])
        )
        vm_collapse = always_redraw(lambda:
            Line(
                start=plane.c2p(0, min(
                    [f.underlying_function(x) for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01)]
                )),
                end=plane.c2p(0, max(
                    [f.underlying_function(x) for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01)]
                )),
                stroke_color=cmap["Vm"], stroke_width=7
            )
        )
        self.play(
            self.camera.frame.animate.shift(4 * LEFT)
        )
        self.play(
            ReplacementTransform(f.copy(), vm_collapse)
        )
        axlines = always_redraw(lambda:
            VGroup(
                DashedLine(
                    start=vm_collapse.get_start(),
                    # end=endpoints[0].get_center(),
                    end=plane.c2p(
                        *[x for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01) if f.underlying_function(x) == min(
                            [f.underlying_function(x) for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01)]
                        )],
                        min([f.underlying_function(x) for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01)])
                    ),
                    stroke_color=cmap["y"]
                ),
                DashedLine(
                    start=vm_collapse.get_end(),
                    # end=endpoints[1].get_center(),
                    end=plane.c2p(
                        *[x for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01) if f.underlying_function(x) == max(
                            [f.underlying_function(x) for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01)]
                        )],
                        max([f.underlying_function(x) for x in np.arange(x_low.get_value(), x_high.get_value(), 0.01)])
                    ),
                    stroke_color=cmap["y"]
                )
            )
        )
        self.play(
            f_opacity.animate.set_value(0.25),
            FadeIn(endpoints),
            Create(axlines)
        )
        self.slide_pause()

        vm_brace = always_redraw(lambda:
            Brace(vm_collapse, LEFT, color=vm_collapse.get_color(), buff=1)
        )
        vm_brace_tekst = always_redraw(lambda:
            VGroup(
                MathTex(r"{{Vm}}({{f}}) = ").set_color_by_tex_to_color_map(cmap),
                MathTex("[" if end_opacities[0].get_value() else "]"),
                    # f"{x_low.get_value():.2f}",
                DecimalNumber(
                    plane.p2c(vm_collapse.get_start())[1],
                    color=cmap["y"]
                ),
                MathTex("; "),
                    # f"{x_high.get_value():.2f}",
                DecimalNumber(
                    plane.p2c(vm_collapse.get_end())[1],
                    color=cmap["y"]
                ),
                MathTex("]" if end_opacities[1].get_value() else "[")
                # ).set_color_by_tex_to_color_map(cmap).next_to(dm_brace, DOWN)
            ).arrange(RIGHT).next_to(vm_brace, LEFT).set_z_index(5)
        )
        vm_brace_tekst_box = always_redraw(lambda: get_background_rect(vm_brace_tekst))
        self.play(
            DrawBorderThenFill(vm_brace),
            Write(vm_brace_tekst),
            FadeIn(vm_brace_tekst_box)
        )
        self.slide_pause()

        self.play(
            x_high.animate.set_value(7),
            run_time=5
        )
        self.play(
            x_high.animate.set_value(0),
            run_time=5
        )
        self.play(
            x_high.animate.set_value(6),
            x_low.animate.set_value(-2),
            run_time=5
        )
        self.play(
            x_low.animate.set_value(-1),
            run_time=2
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m) for m in [
                    vm_brace, vm_collapse, vm_brace_tekst, vm_brace_tekst_box, endpoints, axlines
                ]],
                f_opacity.animate.set_value(1),
                lag_ratio=0.1
            ),
            self.camera.frame.animate.shift(4 * RIGHT)
        )

    def opsamlet(self, f, x_low, x_high):
        scene_marker("Opsamling")
        smallest_rectangle = always_redraw(lambda:
            SurroundingRectangle(f, buff=0)
        )
        self.play(
            Create(smallest_rectangle)
        )
        self.slide_pause()

        for xl, xh in zip([0, 2, -2, -1], [2, 4, 7, 6]):
            if xl > xh:
                xl, xh = xh, xl
            # print(xl, xh)
            self.play(
                x_low.animate.set_value(xl),
                x_high.animate.set_value(xh),
                run_time=5
            )
            self.slide_pause()
        self.play(
            x_low.animate.set_value(-1),
            x_high.animate.set_value(6),
            run_time=5
        )
        self.slide_pause()

        self.play(
            FadeOut(smallest_rectangle)
        )

    def ikke_funktion(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = -8, 8, 1
        ymin, ymax, ystep = -4.5, 4.5, 1
        width = 14
        plane = self.get_plane(
            x=(xmin, xmax, xstep),
            y=(ymin, ymax, ystep),
            width=width
        ).shift(18*RIGHT)
        self.add(plane)

        f = ImplicitFunction(
            lambda x, y: x * y**2 - x**2 * y - 2,
            # lambda x, y: x**2 + y**2 - 10,
            stroke_color=RED,
            x_range=(xmin, xmax),
            y_range=(ymin, ymax)
        ).move_to(plane.c2p(0, 0)).scale(
            (plane.c2p(1, 0) - plane.c2p(0, 0))[0]
        )

        self.camera.frame.save_state()
        cam_width = self.camera.frame.get_width()
        self.play(
            self.camera.frame.animate.set(width=cam_width * 1.25),
            run_time=0.5
        )
        self.play(
            self.camera.frame.animate.move_to(plane),
            run_time=1
        )
        self.play(
            self.camera.frame.animate.set(width=cam_width),
            run_time=0.5
        )

        scan_tracker = ValueTracker(xmin)
        scanning_line = always_redraw(lambda:
            DashedLine(
                start=plane.c2p(scan_tracker.get_value(), -9),
                end=plane.c2p(scan_tracker.get_value(), 9),
                stroke_color=cmap["x"]
            )
        )
        scanning_points = always_redraw(lambda:
            # VGroup(
            #     Dot(fill_color=cmap["f"], radius=0.1).move_to(
            #         f.point_at_angle(PI * (1 - np.sin(PI * (scan_tracker.get_value() - 0))))
            #     )
            # )
            # Intersection(f, scanning_line)
            VGroup(
                *[
                    Dot(
                        radius=0.1, fill_color=BLUE
                    ).move_to(plane.c2p(scan_tracker.get_value(), y)) for y in np.arange(
                        ymin, ymax, 0.0001
                    ) if np.abs(f.function(scan_tracker.get_value(), y)) <= 1E-2
                ]
            )
        )
        # self.add(scanning_line, scanning_points)
        self.play(
            Create(f),
            Create(scanning_line),
            DrawBorderThenFill(scanning_points)
        )
        self.slide_pause()

        self.play(
            scan_tracker.animate.set_value(xmax),
            run_time=10,
            rate_func=rate_functions.linear
        )
        self.slide_pause()
        self.play(
            *[FadeOut(m) for m in (scanning_points, scanning_line)],
            run_time=0.5
        )

        self.play(
            self.camera.frame.animate.set(width=cam_width * 1.25),
            run_time=0.5
        )
        self.play(
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=1
        )
        self.play(
            self.camera.frame.animate.set(width=cam_width),
            run_time=0.5
        )
        self.remove(plane, f)




if __name__ == "__main__":
    classes = [
        FunktionsBegrebet
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)
