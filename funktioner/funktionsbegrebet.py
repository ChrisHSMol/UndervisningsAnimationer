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
        x_low, x_high = ValueTracker(-3), ValueTracker(8)
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

        # self.ikke_funktion()
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

    def definitionsmaengde(self, plane, f, f_opacity, x_low, x_high):
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
        self.slide_pause()

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
        smallest_rectangle = always_redraw(lambda:
            SurroundingRectangle(f, buff=0)
        )
        self.play(
            Create(smallest_rectangle)
        )
        self.slide_pause()

        n_rands = 4
        for xl, xh in zip(
                [(np.random.rand()-0.5) * 4 for _ in range(n_rands)],
                [(np.random.rand()-0.5) * 6 + 3 for _ in range(n_rands)],
        ):
            if xl > xh:
                xl, xh = xh, xl
            print(xl, xh)
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
        xmin, xmax, xstep = -4, 12, 1
        ymin, ymax, ystep = -4.5, 4.5, 1
        width = 14
        plane = self.get_plane(
            x=(xmin, xmax, xstep),
            y=(ymin, ymax, ystep),
            width=width
        ).shift(18*RIGHT)
        self.add(plane)

        # f = ParametricFunction(
        #     lambda u: (np.cos(u), np.sin(u), 0),
        #     stroke_color=RED,
        #     t_range=(0, TAU)
        # ).move_to(plane.c2p(0, 0))
        f = Circle(
            radius=(plane.c2p(1, 0) - plane.c2p(0, 0))[0],
            stroke_color=RED,
            fill_opacity=0
        ).move_to(plane.c2p(0, 0))

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
        self.play(
            Create(f)
        )
        self.slide_pause()

        scan_tracker = ValueTracker(-1)
        scanning_line = always_redraw(lambda:
            DashedLine(
                start=plane.c2p(scan_tracker.get_value(), -9),
                end=plane.c2p(scan_tracker.get_value(), 9),
                stroke_color=cmap["x"]
            )
        )
        scanning_points = always_redraw(lambda:
            VGroup(
                Dot(fill_color=cmap["f"], radius=0.1).move_to(
                    f.point_at_angle(PI * (1 - np.sin(PI * (scan_tracker.get_value() - 0))))
                )
            )
            # Intersection(f, scanning_line)
        )
        self.add(scanning_line, scanning_points)
        self.play(
            scan_tracker.animate.set_value(1),
            run_time=8,
            rate_func=rate_functions.linear
        )

        # scanning_point = always_redraw(lambda:
        #     Dot(
        #         plane.c2p(scan_tracker.get_value(), f.underlying_function(scan_tracker.get_value())),
        #         fill_color=cmap["f"],
        #         radius=0.1
        #     ),
        #     VGroup(
        #         *[
        #             Dot(fill_color=cmap["f"], radius=0.1).move_to(
        #
        #             )
        #         ]
        #     )
        # )




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
