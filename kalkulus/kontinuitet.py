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


