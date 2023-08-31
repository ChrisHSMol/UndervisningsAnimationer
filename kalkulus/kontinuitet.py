from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class Kontinuitet(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        # self.kontinuitet()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def kontinuitet(self):
        x_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=5.5
        ).to_edge(LEFT)
        plane = NumberPlane(
            x_range=[-5.5, 5.5, 1],
            y_range=[-11, 11, 2],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).to_edge(RIGHT)
        graphs = VGroup(
            plane.plot(lambda x: 2 * x - 3, color=BLUE),
            plane.plot(lambda x: -1 * x**2 + 5, color=BLUE),
            plane.plot(lambda x: 0.2 * x ** 3 - 2 * x ** 2 + 3 * x + 5, color=BLUE),
            plane.plot(lambda x: np.abs(x), color=BLUE),
            plane.plot(lambda x: 3*x if x <= 1 else 2 - x, color=BLUE, discontinuities=[1]),
        )
        t_tracker = ValueTracker(-2)

        self.add(plane, x_line)

        for ig in range(len(graphs)):
            moving_x_point = always_redraw(lambda:
                Dot(
                    x_line.n2p(t_tracker.get_value()),
                    color=YELLOW
                )
            )
            moving_y_point = always_redraw(lambda:
                Dot(
                    plane.c2p(t_tracker.get_value(), graphs[ig].underlying_function(t_tracker.get_value())),
                    color=YELLOW
                )
            )

            dx_tracker = ValueTracker(0.5)
            input_circle = always_redraw(lambda:
                Circle(
                    radius=0.5*dx_tracker.get_value(),
                    color=YELLOW
                ).move_to(moving_x_point)
            )
            surrounding_x = always_redraw(lambda:
                Line(
                    start=x_line.n2p(t_tracker.get_value() - dx_tracker.get_value()),
                    end=x_line.n2p(t_tracker.get_value() + dx_tracker.get_value()),
                    color=RED
                )
            )
            surrounding_graph = always_redraw(lambda:
                plane.plot(
                    lambda x: graphs[ig].underlying_function(x),
                    x_range=[t_tracker.get_value() - dx_tracker.get_value(), t_tracker.get_value() + dx_tracker.get_value()],
                    color=RED,
                    discontinuities=[1]
                ).set_z_index(4)
            )
            output_circle = always_redraw(lambda:
                Circle(
                    # radius=max(
                    #     Line(
                    #         start=plane.c2p(t_tracker.get_value() - dx_tracker.get_value(),
                    #                         graphs[ig].underlying_function(t_tracker.get_value() - dx_tracker.get_value())),
                    #         end=plane.c2p(t_tracker.get_value(),
                    #                       graphs[ig].underlying_function(t_tracker.get_value())),
                    #     ).get_length(),
                    #     Line(
                    #         start=plane.c2p(t_tracker.get_value() + dx_tracker.get_value(),
                    #                         graphs[ig].underlying_function(t_tracker.get_value() + dx_tracker.get_value())),
                    #         end=plane.c2p(t_tracker.get_value(),
                    #                       graphs[ig].underlying_function(t_tracker.get_value())),
                    #     ).get_length()
                    # ),
                    radius=max([
                        Line(
                            start=plane.c2p(t_tracker.get_value() + i * dx_tracker.get_value(),
                                            graphs[ig].underlying_function(
                                                t_tracker.get_value() + i * dx_tracker.get_value())),
                            end=plane.c2p(t_tracker.get_value(),
                                          graphs[ig].underlying_function(t_tracker.get_value())),
                        ).get_length() for i in np.linspace(-1, 1, 100)
                    ]),
                    color=YELLOW
                ).move_to(moving_y_point)
            )

            self.add(
                moving_x_point, moving_y_point, output_circle, input_circle, surrounding_x, surrounding_graph, graphs[ig]
            )
            self.play(
                t_tracker.animate.set_value(2),
                run_time=6
            )
            self.play(t_tracker.animate.set_value(-2), run_time=1)
            self.remove(
                moving_x_point, moving_y_point, output_circle, input_circle, surrounding_x, surrounding_graph, graphs[ig]
            )
        # self.add(x_line, plane, input_circle, output_circle, surrounding_x, surrounding_graph)
        # self.add(graphs[ig], moving_y_point, moving_x_point)
        # self.play(
        #     t_tracker.animate.set_value(2),
        #     run_time=10
        # )
        # for g in graphs:
        #     self.play(
        #         Create(g),
        #         run_time=0.25
        #     )
        #     self.slide_pause()


class Differentiabilitet(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.slide_pause()
        self.rolling_slope()
        self.slope_graph()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def rolling_slope(self):
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-9, 12, 1],
            x_length=1.25*self.camera.frame.get_width(),
            y_length=7/6*self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        graphs = VGroup(
            plane.plot(lambda x: x**2, color=YELLOW)
        )
        self.add(plane, graphs)

        x0 = ValueTracker(-3)
        moving_tangent = always_redraw(lambda:
            plane.get_secant_slope_group(
                x=x0.get_value(),
                graph=graphs[0],
                dx=1E-4,
                include_dy_line=False,
                include_dx_line=False,
                secant_line_color=BLUE,
                secant_line_length=3
            )
        )
        moving_value = always_redraw(lambda:
            DecimalNumber(
                2*x0.get_value(),
                num_decimal_places=2,
                include_sign=True,
                color=BLUE
            ).move_to(plane.c2p(1.25*x0.get_value(), 1*(graphs[0].underlying_function(x0.get_value()) - 1)))
        )
        self.add(moving_tangent, moving_value)
        j_list = [1, 0.5, 0.125]
        for j in j_list:
            # for i in np.arange(x0.get_value() + j, -x0.get_value() + 1E-4, j):
            #     self.play(
            #         AnimationGroup(
            #             FadeOut(get_background_rect(moving_value, fill_color=GRAY, buff=0.05), run_time=0.1),
            #             FadeIn(moving_value.copy().set_color(BLUE_B), run_time=0.05),
            #             FadeIn(moving_tangent.copy().set_style(stroke_color=BLUE_B, stroke_opacity=0.5), run_time=0.05),
            #         ),
            #         x0.animate.set_value(i),
            #         run_time=2 * np.abs(x0.get_value() - i),
            #         rate_func=rate_functions.linear
            #     )
            # self.play(
            #     AnimationGroup(
            #         FadeOut(get_background_rect(moving_value, fill_color=GRAY, buff=0.05), run_time=0.1),
            #         FadeIn(moving_value.copy().set_color(BLUE_B), run_time=0.05),
            #         FadeIn(moving_tangent.copy().set_style(stroke_color=BLUE_B, stroke_opacity=0.5), run_time=0.05),
            #     )
            # )
            text_copies = always_redraw(lambda: VGroup(*[
                DecimalNumber(
                    2*i,
                    include_sign=True,
                    num_decimal_places=2,
                    color=moving_value.get_color(),
                    stroke_opacity=0 if i > x0.get_value() else 0.75,
                    fill_opacity=0 if i > x0.get_value() else 0.75
                ).move_to(
                    plane.c2p(1.25 * i, 1 * (graphs[0].underlying_function(i) - 1))
                ) for i in np.arange(-3, 3 + 1E-4, j)
            ]))
            slope_copies = always_redraw(lambda: VGroup(*[
                plane.get_secant_slope_group(
                    x=i,
                    graph=graphs[0],
                    dx=1E-4,
                    include_dy_line=False,
                    include_dx_line=False,
                    secant_line_color=BLUE,
                    secant_line_length=3,
                ).set_style(stroke_opacity=0 if i > x0.get_value() else 0.5) for i in np.arange(-3, 3 + 1E-4, j)
            ]))
            print(text_copies, slope_copies)
            self.add(text_copies, slope_copies)
            self.play(
                x0.animate.set_value(3),
                run_time=6
            )
            self.slide_pause()
            if j == j_list[-1]:
                tekst = VGroup(
                    Tex("Det bliver svært at overskue."),
                    Tex("I stedet for at skrive hældningerne,"),
                    Tex("så lad os plotte deres værdi som punkter:")
                ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
                trec = get_background_rect(tekst, stroke_colour=RED, buff=0.5, fill_opacity=0.9)
                self.play(
                    LaggedStart(
                        FadeIn(trec),
                        Write(tekst),
                        lag_ratio=0.1
                    )
                )
                self.slide_pause()

            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [plane, graphs, moving_value, moving_tangent]],
                x0.animate.set_value(-3),
                run_time=1
            )
            self.remove(text_copies, slope_copies)
            self.slide_pause()
        self.remove(moving_value, moving_tangent, plane, graphs)

    def _slope_graph(self):
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-9, 12, 1],
            x_length=1.25*self.camera.frame.get_width(),
            y_length=7/6*self.camera.frame.get_height(),
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
            plane.plot(lambda x: 2*x+2 if x <= 1 else -2*x+6, color=YELLOW)
        )
        subgraphs = VGroup(
            plane.plot(lambda x: 2*x),
            plane.plot(lambda x: x + 2),
            plane.plot(lambda x: 0.75*x**2 + x - 1.25),
            plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3),
            plane.plot(lambda x: 2 if x <= 1 else -2)
        )

        for graph, subgraph in zip(graphs, subgraphs):
            x0 = ValueTracker(-3)
            moving_tangent = always_redraw(lambda:
                plane.get_secant_slope_group(
                    x=x0.get_value(),
                    graph=graph,
                    dx=1E-4,
                    include_dy_line=False,
                    include_dx_line=False,
                    secant_line_color=BLUE,
                    secant_line_length=3
                )
            )
            moving_value = always_redraw(lambda:
                DecimalNumber(
                    subgraph.underlying_function(x0.get_value()),
                    num_decimal_places=2,
                    include_sign=True,
                    color=BLUE
                ).move_to(plane.c2p(1.25*x0.get_value(), 1*(graph.underlying_function(x0.get_value()) - 1)))
            )
            if graph == graphs[0]:
                self.add(plane, graph, moving_tangent, moving_value)
            else:
                self.play(
                    # LaggedStart(
                    #     Create(graph),
                    #     Create(moving_tangent),
                    #     Write(moving_value),
                    #     lag_ratio=0.2
                    # ),
                    # run_time=0.5
                    *[Transform(mold, mnew) for mold, mnew in zip(prevs, VGroup(graph, moving_tangent, moving_value))],
                    run_time=2
                )

            for j in [0.125]:
                self.add(Dot(plane.c2p(-3, subgraph.underlying_function(-3)), color=BLUE))
                for i in np.arange(x0.get_value() + j, -x0.get_value() + 1E-4, j):
                    self.play(
                        x0.animate.set_value(i),
                        run_time=2 * np.abs(x0.get_value() - i),
                        rate_func=rate_functions.linear
                    )
                    self.add(Dot(plane.c2p(i, subgraph.underlying_function(i)), color=BLUE))
                self.slide_pause()
                self.play(
                    *[FadeOut(m) for m in self.mobjects if m not in [plane, graph, moving_value, moving_tangent]],
                    x0.animate.set_value(-3),
                    run_time=1
                )

            if graph != graphs[-1]:
                prevs = VGroup(graph, moving_tangent, moving_value)
            else:
                self.play(
                    LaggedStart(
                        Uncreate(graph),
                        Uncreate(moving_tangent),
                        Unwrite(moving_value),
                        lag_ratio=0.2
                    ),
                    run_time=0.5
                )

    def slope_graph(self):
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-9, 12, 1],
            x_length=1.25*self.camera.frame.get_width(),
            y_length=7/6*self.camera.frame.get_height(),
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
            plane.plot(lambda x: 2*x+2 if x <= 1 else -2*x+6, color=YELLOW)
        )
        graph_texts = VGroup(*[
            Tex("f(x) er kontinuert").set_color_by_tex_to_color_map(
                {"f(x)": YELLOW}
            ).to_edge(DR).shift(UP) for _ in graphs
        ])
        subgraphs = VGroup(
            plane.plot(lambda x: 2*x, color=BLUE),
            plane.plot(lambda x: x + 2, color=BLUE),
            plane.plot(lambda x: 0.75*x**2 + x - 1.25, color=BLUE),
            plane.plot(lambda x: -0.4275 - 2*0.2375*x + 0.36*x**2 + 0.2*x**3, color=BLUE),
            plane.plot(lambda x: 2 if x <= 1 else -2, color=BLUE, discontinuities=[1])
        )
        subgraph_texts = VGroup(
            *[Tex("f'(x) er kontinuert").set_color_by_tex_to_color_map(
                {"f'(x)": BLUE}
            ).next_to(graph_text, DOWN, aligned_edge=RIGHT) for graph_text in graph_texts[:-1]],
            Tex("f'(x) er ikke kontinuert").set_color_by_tex_to_color_map(
                {"f'(x)": BLUE}
            ).next_to(graph_texts[-1], DOWN, aligned_edge=RIGHT)
        )
        xmin, xmax = -4, 4
        asdf = 0

        for graph, subgraph, graph_text, subgraph_text in zip(graphs, subgraphs, graph_texts, subgraph_texts):
            asdf += 1
            print(f"Ved graf {asdf}")
            x0 = ValueTracker(xmin)
            moving_tangent = always_redraw(lambda:
                plane.get_secant_slope_group(
                    x=x0.get_value(),
                    graph=graph,
                    dx=1E-4,
                    include_dy_line=False,
                    include_dx_line=False,
                    secant_line_color=BLUE,
                    secant_line_length=3
                )
            )
            moving_value = always_redraw(lambda:
                DecimalNumber(
                    subgraph.underlying_function(x0.get_value()),
                    num_decimal_places=2,
                    include_sign=True,
                    color=BLUE
                ).move_to(plane.c2p(1.25*x0.get_value(), 1*(graph.underlying_function(x0.get_value()) - 1)))
            )

            if graph == graphs[0]:
                self.add(plane, graph, moving_tangent, moving_value)
            else:
                self.play(
                    *[ReplacementTransform(mold, mnew) for mold, mnew in zip(
                        prevs, VGroup(graph, moving_tangent, moving_value)
                    )],
                    run_time=2
                )
            prevs = VGroup(graph, moving_tangent, moving_value)

            for j in [0.125]:
                dots = always_redraw(lambda: VGroup(*[
                    Dot(
                        plane.c2p(i, subgraph.underlying_function(i)), color=BLUE,
                        fill_opacity=0 if x0.get_value() <= i else 1
                    ) for i in np.arange(xmin, xmax + 1E-4, j)
                ]))
                self.add(dots)
                self.play(
                    x0.animate.set_value(xmax),
                    run_time=1*(xmax - xmin),
                    rate_func=rate_functions.linear
                )
                self.slide_pause()

                self.play(
                    Create(subgraph),
                    Write(VGroup(graph_text, subgraph_text), lag_ratio=0.25),
                    run_time=2
                )
                self.slide_pause()

                self.play(
                    x0.animate.set_value(xmin),
                    Uncreate(subgraph),
                    Unwrite(VGroup(graph_text, subgraph_text), lag_ratio=0.25, reverse=True),
                    run_time=1
                )
                self.remove(dots)

        self.play(
            LaggedStart(
                Uncreate(graph),
                Uncreate(moving_tangent),
                Unwrite(moving_value),
                lag_ratio=0.2
            ),
            run_time=0.5
        )


