from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = True
if slides:
    from manim_slides import Slide


class AfledteFunktioner(MovingCameraScene, Slide if slides else Scene):
    name = "AfledteFunktioner"
    def construct(self):
        self.slide_pause()
        self.forklaring_af_sammenhaeng()
        self.slide_pause()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def forklaring_af_sammenhaeng(self):
        plane = NumberPlane(
            x_range=[-12, 12, 1],
            y_range=[-13.5, 13.5, 2],
            x_length=1.5*self.camera.frame.get_width(),
            y_length=1.5*self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        graphs = VGroup(
            plane.plot(lambda x: x**2, color=YELLOW),
            plane.plot(lambda x: 0.5*x**2 + 2*x, color=YELLOW),
            plane.plot(lambda x: 0.25*(x+3)*(x+1)*(x-2), color=YELLOW),
            plane.plot(lambda x: 0.05*(x+3)*(x+1.5)*(x-0.1)*(x-2)-1, color=YELLOW),
        )
        extra_graphs = VGroup(
            VGroup(
                plane.plot(lambda x: x**2, color=RED, x_range=[-12, 0]),
                plane.plot(lambda x: x**2, color=GREEN, x_range=[0, 12]),
            ),
            VGroup(
                plane.plot(lambda x: 0.5*x**2 + 2*x, color=RED, x_range=[-12, -2]),
                plane.plot(lambda x: 0.5*x**2 + 2*x, color=GREEN, x_range=[-2, 12]),
            ),
            VGroup(
                plane.plot(lambda x: 0.25*(x+3)*(x+1)*(x-2), color=GREEN, x_range=[-12, -2.12]),
                plane.plot(lambda x: 0.25*(x+3)*(x+1)*(x-2), color=RED, x_range=[-2.12, 0.79]),
                plane.plot(lambda x: 0.25*(x+3)*(x+1)*(x-2), color=GREEN, x_range=[0.79, 12]),
            ),
            VGroup(
                plane.plot(lambda x: 0.05*(x+3)*(x+1.5)*(x-0.1)*(x-2)-1, color=RED, x_range=[-12, -2.42]),
                plane.plot(lambda x: 0.05*(x+3)*(x+1.5)*(x-0.1)*(x-2)-1, color=GREEN, x_range=[-2.42, -0.68]),
                plane.plot(lambda x: 0.05*(x+3)*(x+1.5)*(x-0.1)*(x-2)-1, color=RED, x_range=[-0.68, 1.3]),
                plane.plot(lambda x: 0.05*(x+3)*(x+1.5)*(x-0.1)*(x-2)-1, color=GREEN, x_range=[1.3, 12]),
            )
        )
        subgraphs = VGroup(
            plane.plot(lambda x: 2*x, color=BLUE),
            plane.plot(lambda x: x + 2, color=BLUE),
            plane.plot(lambda x: 0.75*x**2 + x - 1.25, color=BLUE),
            plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3, color=BLUE),
        )
        extra_subgraphs = VGroup(
            VGroup(
                plane.plot(lambda x: 2*x, color=RED_A, x_range=[-12, 0]),
                plane.plot(lambda x: 2*x, color=GREEN_A, x_range=[0, 12]),
            ),
            VGroup(
                plane.plot(lambda x: x + 2, color=RED_A, x_range=[-12, -2]),
                plane.plot(lambda x: x + 2, color=GREEN_A, x_range=[-2, 12]),
            ),
            VGroup(
                plane.plot(lambda x: 0.75*x**2 + x - 1.25, color=GREEN_A, x_range=[-12, -2.12]),
                plane.plot(lambda x: 0.75*x**2 + x - 1.25, color=RED_A, x_range=[-2.12, 0.79]),
                plane.plot(lambda x: 0.75*x**2 + x - 1.25, color=GREEN_A, x_range=[0.79, 12]),
            ),
            VGroup(
                plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3, color=RED_A, x_range=[-12, -2.42]),
                plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3, color=GREEN_A, x_range=[-2.42, -0.68]),
                plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3, color=RED_A, x_range=[-0.68, 1.3]),
                plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3, color=GREEN_A, x_range=[1.3, 12]),
            )
        )
        self.play(
            DrawBorderThenFill(plane)
        )

        tekst = VGroup(
            VGroup(
                Tex("Når ", "f(x)", " er ", "aftagende").set_color_by_tex_to_color_map(
                    {"f(x)": color_gradient([YELLOW, GREEN, YELLOW, RED], 4), "aftagende": RED}
                ),
                Tex("er ", "f'(x)", " negativ").set_color_by_tex_to_color_map(
                    {"f'(x)": color_gradient([BLUE, GREEN_A, BLUE, RED_A], 4), "negativ": RED_A}
                )
            ).arrange(DOWN, aligned_edge=LEFT),
            VGroup(
                Tex("Når ", "f(x)", " er ", "tiltagende").set_color_by_tex_to_color_map(
                    {"f(x)": color_gradient([YELLOW, GREEN, YELLOW, RED], 4), "tiltagende": GREEN}
                ),
                Tex("er ", "f'(x)", " positiv").set_color_by_tex_to_color_map(
                    {"f'(x)": color_gradient([BLUE, GREEN_A, BLUE, RED_A], 4), "positiv": GREEN_A}
                )
            ).arrange(DOWN, aligned_edge=LEFT),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DR, buff=0.1).set_z_index(3)
        tekst_rec = get_background_rect(
            tekst,
            stroke_colour=color_gradient([YELLOW, GREEN, RED, BLUE, GREEN_A, RED_A], 8),
            buff=0.1
        )

        for graph, egraph, subgraph, esub in zip(graphs, extra_graphs, subgraphs, extra_subgraphs):
            self.play(
                LaggedStart(
                    *[Create(m, run_time=2) for m in [graph, subgraph]],
                    lag_ratio=0.5
                )
            )
            self.slide_pause()
            self.play(
                Create(egraph, lag_ratio=1),
                Create(esub, lag_ratio=1),
                run_time=3,
                rate_func=rate_functions.linear
            )
            if graph == graphs[0]:
                self.play(
                    Write(tekst),
                    FadeIn(tekst_rec),
                    run_time=1
                )
            self.slide_pause()
            if graph != graphs[-1]:
                self.play(
                    *[FadeOut(m) for m in [graph, subgraph, egraph, esub]]
                )

        scene_marker("Zoom in")

        ekstrema = VGroup(*[
            Dot(
                plane.c2p(x, graphs[-1].underlying_function(x)),
                stroke_color=color_gradient([GREEN, RED], 4),
                stroke_width=3
            ).scale(0.5) for x in [-2.42, -0.68, 1.3]
        ])
        slope_roots = VGroup(*[
            Dot(
                plane.c2p(x, subgraphs[-1].underlying_function(x)),
                stroke_color=color_gradient([GREEN_A, RED_A], 4),
                stroke_width=3
            ).scale(0.5) for x in [-2.42, -0.68, 1.3]
        ])
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(m) for m in [*ekstrema, *slope_roots]],
                lag_ratio=0.1
            )
        )
        self.camera.frame.save_state()
        for eks, slo in zip(ekstrema, slope_roots):
            self.play(
                self.camera.frame.animate.set(width=2).move_to(
                    between_mobjects(eks, slo)
                ),
                run_time=2
            )
            self.slide_pause()

        self.play(
            Restore(self.camera.frame)
        )

        afrunding = VGroup(
            Tex("f(x)", " har lige så mange ", "ekstrema").set_color_by_tex_to_color_map(
                {"f(x)": color_gradient([YELLOW, GREEN, YELLOW, RED], 4), "ekstrema": YELLOW}
            ),
            Tex("som ", "f'(x)", " har ", "rødder").set_color_by_tex_to_color_map(
                {"f'(x)": color_gradient([BLUE, GREEN_A, BLUE, RED_A], 4), "rødder": YELLOW}
            ),
            Tex("(og de findes endda ved samme ", "x-værdier", ")").set_color_by_tex_to_color_map(
                {"x-værdier": YELLOW}
            ),
        ).arrange(DOWN, aligned_edge=LEFT)
        afrect = get_background_rect(afrunding, stroke_colour=YELLOW)
        self.play(
            LaggedStart(
                *[FadeOut(d) for d in [*ekstrema, *slope_roots]],
                *[Uncreate(g) for g in [graphs[-1], subgraphs[-1], plane, *extra_graphs[-1], *extra_subgraphs[-1]]],
                AnimationGroup(
                    # tekst.animate.become(afrunding),
                    # tekst_rec.animate.become(afrect),
                    TransformMatchingTex(tekst, afrunding, transform_mismatches=True),
                    TransformMatchingShapes(tekst_rec, afrect)
                ),
                lag_ratio=0.05
            ),
            run_time=3
        )


if __name__ == "__main__":
    class_name = AfledteFunktioner.name
    scene_marker(rf"RUNNNING:    manim {sys.argv[0]} {class_name} -pqh")
    subprocess.run(rf"manim {sys.argv[0]} {class_name} -pqh")
    if slides:
        scene_marker(rf"RUNNING:    manim-slides convert {class_name} {class_name}.html")
        # subprocess.run(rf"manim-slides convert {class_name} {class_name}.html")
        subprocess.run(rf"manim-slides {class_name}")
