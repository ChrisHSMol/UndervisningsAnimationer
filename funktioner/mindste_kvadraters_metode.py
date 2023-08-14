from manim import *
import sys
sys.path.append("../")
from helpers import *


def _prep_title(title, close=False):
    if isinstance(title, str):
        title = Tex(title)
    title_ul = Underline(title)
    title_ul_box = Rectangle(
        width=title.width,
        height=title.height * 1.6
    ).next_to(
        title_ul, DOWN, buff=0
    ).set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK)
    ul_group = VGroup(title_ul, title_ul_box)
    if close:
        ul_group.shift(UP * title_ul_box.height)
    return title_ul, title_ul_box, ul_group


def play_title(self, title):
    if isinstance(title, str):
        title = Tex(title)
    title_ul, title_ul_box, ul_group = _prep_title(title)
    self.play(Write(title), run_time=0.5)
    self.wait(2)
    self.play(GrowFromCenter(title_ul), run_time=1)
    self.add(ul_group)
    self.play(ul_group.animate.shift(UP * title_ul_box.height))
    self.play(ShrinkToCenter(title_ul))
    self.remove(ul_group, title)
    self.wait(2)


def play_title_reverse(self, title):
    if isinstance(title, str):
        title = Tex(title)
    title_ul, title_ul_box, ul_group = _prep_title(title, close=True)
    self.add(title, ul_group)
    self.play(GrowFromCenter(title_ul))
    self.play(ul_group.animate.shift(DOWN * title_ul_box.height))
    self.remove(ul_group)
    self.play(ShrinkToCenter(title_ul))
    self.wait(1)
    self.play(Unwrite(title), run_time=0.5)
    self.wait(1)


def p2p_anim(mob1, mob2, tex1, tex2=None, index=0):
    if tex2.isnone():
        tex2 = tex1
    return ReplacementTransform(
        mob1.get_parts_by_tex(tex1)[index],
        mob2.get_parts_by_tex(tex2)[index],
    )


def p2p_anim_copy(mob1, mob2, tex1, tex2=None, index=0):
    if tex2.isnone():
        tex2 = tex1
    return TransformFromCopy(
        mob1.get_parts_by_tex(tex1)[index],
        mob2.get_parts_by_tex(tex2)[index],
    )


def fade_out_all(self, rt=1):
    self.play(
        *[
            FadeOut(mob) for mob in self.mobjects
        ],
        run_time=rt
    )


def addsign(val, dec=1):
    if isinstance(val, MathTex):
        val = float(val.tex_string)
    if val >= 0:
        return f"+{val:.{dec}f}"
    else:
        return f"{val:.{dec}f}"


def sumtex(vals):
    sum = 0.0
    for val in vals:
        if isinstance(val, MathTex):
            vals += float(val.tex_string)
    return sum


def ftp(point1, point2, dim="y"): # Find Top Point
    d = {"x": 0, "y": 1, "z": 2}
    if isinstance(dim, str):
        dim = d[dim]
    return point1 if point1[dim]>point2[dim] else point2


slides = True
if slides:
    from manim_slides import Slide


class _LeastSquares(MovingCameraScene if not slides else Slide, MovingCameraScene):
    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def construct(self):
        title = "Mindste kvadraters metode"
        play_title(self, title)

        # xvals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # yvals = [10, 22, 30, 48, 62, 68, 76, 95, 104, 120, 125]
        data_points = []
        for x, y in zip(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [10, 22, 30, 48, 62, 68, 76, 95, 104, 120, 125]
        ):
            data_points.append((x, y, 0))
        data_points = np.array(data_points)

        point_col = BLUE
        graph_col = YELLOW
        squar_col = RED

        # table = IntegerTable(
        #     data_points[:, :2],
        #     color=point_col,
        #     col_labels=[Text("Måneder"), Text("Længde")],
        #     include_outer_lines=True,
        #     element_to_mobject={"color": point_col}
        # ).to_edge(RIGHT).scale(0.55).shift(1.5*RIGHT)
        # self.play(DrawBorderThenFill(table))
        # self.wait(1)

        xmin, xmax, xstep = -1, 11.5, 1
        ymin, ymax, ystep = -10, 150, 20
        width = 10
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=width / 16 * 9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True}
        ).move_to(DL).shift(LEFT)
        self.slide_pause()
        self.play(
            DrawBorderThenFill(
                plane
            ),
            run_time=2
        )
        self.wait(1)
        # self.slide_pause()

        points = always_redraw(lambda: VGroup(*[
            Dot(plane.c2p(*point), color=point_col) for point in data_points
        ]))
        self.play(
            LaggedStart(*[
                DrawBorderThenFill(point) for point in points
            ],
                lag_ratio=0.5
                ),
            run_time=1
        )
        # self.wait(1)
        self.slide_pause()

        # =====================================================================
        # =====================================================================
        # =====================================================================

        # a = ValueTracker(5)
        # b = ValueTracker(40)
        a_knap = DrejeKnap(range_min=0, range_max=20, range_step=2, label="a", start_value=5)
        b_knap = DrejeKnap(range_min=0, range_max=100, range_step=10, label="b", start_value=40)
        knapper = VGroup(a_knap, b_knap).arrange(DOWN).scale(0.5).next_to(plane, RIGHT, aligned_edge=DOWN)
        a = a_knap.tracker
        b = b_knap.tracker
        graph = always_redraw(lambda:
            plane.plot(
                lambda x: a.get_value() * x + b.get_value(),
                x_range=[xmin, xmax], color=graph_col, stroke_width=2.5
            )
        )
        graph_text = always_redraw(lambda:
            MathTex(
                "y", "=", f"{a.get_value():.2f}", r"\cdot", "x", "+",
                f"{b.get_value():.2f}",
                color=graph_col
            ).next_to(plane, UP, aligned_edge=LEFT)
        )
        # graph_points = np.array([(x, graph.underlying_function(x), 0) for x in data_points[:, 0]])
        # print(graph_points)
        # _points = always_redraw(lambda:
        #     VGroup(*[
        #         Dot(
        #             plane.c2p(*gpoint),
        #             color=None
        #         ).scale(0.01) for gpoint in graph_points
        #     ])
        # )
        _points = always_redraw(lambda: VGroup(*[
            Dot(plane.c2p(
                point[0],
                a.get_value() * point[0] + b.get_value()
            ), color=None).scale(0.01) for point in data_points
            # )) for point in data_points
        ]))
        # graph_points = VGroup(
        #     *[
        #         always_redraw(lambda:
        #             gpoint.get_center()
        #         ) for gpoint in _points
        #     ]
        # )
        # print(graph_points)
        self.add(_points)
        self.play(
            LaggedStart(
                DrawBorderThenFill(graph),
                Write(graph_text),
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.play(
            DrawBorderThenFill(knapper),
            run_time=1
        )
        # self.wait(1)
        self.slide_pause()

        srec = SurroundingRectangle(
            graph_text[:6],
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.75
        )
        self.play(FadeIn(srec), run_time=0.5)
        for i in [0, 80, 40]:
            self.play(
                b.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.play(FadeOut(srec), run_time=0.5)
        # self.wait(1)
        self.slide_pause()

        srec = VGroup(
            SurroundingRectangle(graph_text[:2], color=BLACK, fill_color=BLACK,
                                 fill_opacity=0.75),
            SurroundingRectangle(graph_text[3:], color=BLACK, fill_color=BLACK,
                                 fill_opacity=0.75).shift(0.25 * RIGHT)
        )
        self.play(FadeIn(srec), run_time=0.5)
        for i in [2, 20, 5]:
            self.play(
                a.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.play(FadeOut(srec), run_time=0.5)
        # self.wait(1)
        self.slide_pause()

        # =====================================================================
        # =====================================================================
        # =====================================================================

        question = VGroup(
            Tex("Hvordan finder vi ud af,"),
            Tex("hvordan linjen skal placeres?")
        ).arrange(DOWN, aligned_edge=LEFT)
        srec = SurroundingRectangle(
            plane,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.90
        ).scale(3)
        self.play(FadeIn(srec), run_time=1)
        self.wait(1)
        self.play(Write(question), run_time=2)
        self.wait(1)
        self.play(Unwrite(question, reverse=False), run_time=1)
        self.play(FadeOut(srec))
        # self.wait(1)
        self.slide_pause()

        dotlines = always_redraw(
            lambda: VGroup(
                *[
                    Line(
                        start=point.get_center(),
                        end=gpoint.get_center(),
                        color=squar_col,
                        stroke_width=2.5
                    ) for point, gpoint in zip(points, _points)
                ]
            )
        )
        self.play(
            LaggedStart(*[
                DrawBorderThenFill(line) for line in dotlines
            ],
                lag_ratio=0.5,
                rate_func=rate_functions.smooth
            ),
            run_time=1.5
        )
        # self.wait(1)
        self.add(dotlines)
        self.slide_pause()

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(points[0]).shift(0.5 * UP),
            run_time=2
        )
        # self.wait(1)
        self.slide_pause()
        self.play(
            ShowPassingFlash(
                Line(
                    start=plane.c2p(data_points[0][0],
                                    graph.underlying_function(data_points[0][0])),
                    end=plane.c2p(*data_points[0]),
                    stroke_width=3,
                    color=YELLOW
                ),
                time_width=1.5
            ),
            run_time=2
        )

        dotlines_text = always_redraw(lambda:
            VGroup(*[
                DecimalNumber(
                    point[1] - (a.get_value() * point[0] + b.get_value()),
                    num_decimal_places=1,
                    include_sign=True,
                    color=squar_col
                ).scale(0.5).next_to(dotline, LEFT).shift(
                    0.2 * RIGHT
                ) for point, dotline in zip(data_points, dotlines)
            ])
        )
        self.play(
            Write(
                dotlines_text[0]
            ),
            run_time=0.5
        )
        # self.wait(1)
        self.slide_pause()
        self.play(
            LaggedStart(
                Restore(self.camera.frame),
                *[
                    Write(
                        dotline_text
                    ) for dotline_text in dotlines_text[1:]
                ],
                lag_ratio=0.1
            ),
            run_time=4
        )
        # self.wait(1)
        self.add(dotlines_text)
        self.slide_pause()
        dotlines_text_copy = always_redraw(lambda:
            VGroup(
                *[
                    text.copy().scale(1.5).next_to(
                        graph_text, UP, aligned_edge=LEFT
                    ).shift(
                        0.9 * UP + 1.00 * i * RIGHT
                    ) for i, text in enumerate(dotlines_text)
                ])
        )
        self.play(
            ReplacementTransform(
                dotlines_text.copy(),
                dotlines_text_copy
            ),
            run_time=2
        )
        # self.wait(1)
        self.slide_pause()

        brace = Brace(
            VGroup(
                dotlines_text_copy
            ),
            DOWN
        )
        brace_text = Tex(
            "Sum af afvigelser fra grafen = "
        ).next_to(brace, DOWN).shift(0.2 * UP)
        dev_sum = always_redraw(lambda:
            DecimalNumber(
                sum([
                    point[1] - (a.get_value() * point[0] + b.get_value()) for point in data_points
                ]),
                num_decimal_places=1,
                include_sign=True,
                color=squar_col
            ).next_to(brace_text, RIGHT)
        )
        self.play(
            GrowFromCenter(brace),
            run_time=1
        )
        self.wait(1)
        self.play(
            Write(VGroup(
                brace_text,
                dev_sum
            )),
            run_time=1
        )
        # self.wait(1)
        self.slide_pause()

        self.play(
            b.animate.set_value(60),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            b.animate.set_value(0),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            b.animate.set_value(20),
            run_time=1.5
        )
        # self.wait(1)
        self.slide_pause()

        # =====================================================================
        # =====================================================================
        # =====================================================================

        question = VGroup(
            Tex("Det fungerer ikke helt."),
            Tex("Kan vi gøre det bedre?")
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(FadeIn(srec), run_time=1)
        self.wait(1)
        self.play(Write(question), run_time=2)
        self.wait(1)
        self.play(Unwrite(question, reverse=False), run_time=1)
        self.play(
            FadeOut(
                VGroup(
                    srec,
                    dotlines,
                    dotlines_text,
                    dotlines_text_copy,
                    brace,
                    brace_text,
                    dev_sum
                )
            ),
            run_time=1
        )
        # self.wait(1)
        self.slide_pause()

        dotsquares = always_redraw(lambda:
            VGroup(
                *[
                    Square(
                        side_length=np.abs(point.get_y() - gpoint.get_y()),
                        color=squar_col,
                        stroke_width=2.5
                    ).next_to(
                        ftp(point.get_center(), gpoint.get_center()),
                        DL,
                        buff=0
                    ) for point, gpoint in zip(points, _points)
                ]
            )
        )

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(points[0]).shift(0.5*UP),
            run_time=2
        )
        # self.wait(1)
        self.slide_pause()
        self.play(
            ShowPassingFlash(
                Square(
                    side_length=dotlines[0].get_height(),
                    stroke_width=2.5,
                    color=YELLOW
                ).next_to(dotlines[0].get_top(), DL, buff=0),
                time_width=1.5
            ),
            run_time=3
        )
        self.play(
            LaggedStart(*[
                DrawBorderThenFill(sq) for sq in dotsquares
            ],
                lag_ratio=0.5,
                rate_func=rate_functions.smooth
            ),
            run_time=1.5
        )
        # self.wait(1)
        self.add(dotsquares)
        self.slide_pause()

        dotsquares_text = always_redraw(lambda:
            VGroup(*[
                DecimalNumber(
                    (point[1]-(a.get_value()*point[0]+b.get_value()))**2,
                    num_decimal_places=1,
                    include_sign=True,
                    color=squar_col
                ).scale(0.45).move_to(sq) for sq, point in zip(dotsquares, data_points)
            ]
            )
        )
        self.play(
            Write(
                dotsquares_text[0]
            ),
            run_time=0.5
        )
        # self.wait(1)
        self.slide_pause()
        self.play(
            LaggedStart(
                Restore(self.camera.frame),
                *[
                    Write(
                        dotsquare_text
                    ) for dotsquare_text in dotsquares_text[1:]
                ],
                lag_ratio=0.1
            ),
            run_time=4
        )
        # self.wait(1)
        self.add(dotsquares_text)
        self.slide_pause()

        dotsquares_text_copy = always_redraw(lambda:
            VGroup(
                *[
                    text.copy().scale(1.1).next_to(
                        graph_text, UP, aligned_edge=LEFT
                    ).shift(
                        0.9*UP + 1.00*i*RIGHT
                    ) for i, text in enumerate(dotsquares_text)
                ]
            )
        )
        self.play(
            ReplacementTransform(
                dotsquares_text.copy(),
                dotsquares_text_copy
            ),
            run_time=2
        )
        # self.wait(1)
        self.slide_pause()

        brace = Brace(
            VGroup(
                dotsquares_text_copy
            ),
            DOWN
        )
        brace_text = Tex(
            "Sum af firkanternes areal = "
        ).next_to(brace, DOWN).shift(0.2*UP)
        sq_sum = always_redraw(lambda:
            DecimalNumber(
                sum([
                    (point[1]-(a.get_value()*point[0]+b.get_value()))**2 for point in data_points
                ]),
                num_decimal_places=1,
                include_sign=True,
                color=squar_col
            ).next_to(brace_text, RIGHT)
        )
        self.play(
            GrowFromCenter(brace),
            run_time=1
        )
        self.wait(1)
        self.play(
            Write(VGroup(
                brace_text,
                sq_sum
            )),
            run_time=1
        )
        # self.wait(1)
        self.slide_pause()

        for i in [60, 0, 20]:
            self.play(
                b.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        # self.wait(1)
        self.slide_pause()

        for i in [15, 10, 12]:
            self.play(
                a.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.wait(1)
        self.play(
            b.animate.set_value(10),
            run_time=2
        )
        # self.play(FadeOut(dotsquares_text), run_time=0.5)
        # self.wait(1)
        self.slide_pause()

        fade_out_all(self)
        play_title_reverse(self, title=title)


class LeastSquares(MovingCameraScene if not slides else Slide, MovingCameraScene):
    def construct(self):
        title = "Mindste kvadraters metode"
        play_title(self, title)

        plane, points = self.plot_points_on_plane(animation=True)
        self.try_simple_deviation(plane, points)

        play_title_reverse(title)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def distribute_colors(self):
        point_col = BLUE_C
        graph_col = BLUE_A
        dev_cols = [GREEN, RED]
        acol = YELLOW
        bcol = PURPLE
        return [point_col, graph_col, dev_cols, acol, bcol]

    def plot_points_on_plane(self, animation=True):
        data_points = []
        for x, y in zip(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [10, 22, 30, 48, 62, 68, 76, 95, 104, 120, 125]
        ):
            data_points.append((x, y, 0))
        data_points = np.array(data_points)

        point_col, graph_col, dev_cols, acol, bcol = self.distribute_colors()

        xmin, xmax, xstep = -1, 11.5, 1
        ymin, ymax, ystep = -10, 150, 20
        width = 10
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=width / 16 * 9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True}
        ).move_to(DL).shift(LEFT)
        if animation:
            self.slide_pause()
            self.play(
                DrawBorderThenFill(
                    plane
                ),
                run_time=2
            )
            self.wait(1)

        points = VGroup(*[
            Dot(plane.c2p(*point), color=point_col) for point in data_points
        ])
        if animation:
            self.play(
                LaggedStart(*[
                    DrawBorderThenFill(point) for point in points
                ],
                    lag_ratio=0.5
                    ),
                run_time=1
            )
            self.slide_pause()
            self.remove(plane, points)
        return plane, points

    def try_simple_deviation(self, plane, points):
        # self.add(plane, points)
        xmin, xmax, xstep = -1, 11.5, 1
        point_col, graph_col, dev_cols, acol, bcol = self.distribute_colors()

        # a_knap = DrejeKnap(range_min=0, range_max=20, range_step=2, label="a", start_value=5, accent_color=acol)
        # b_knap = DrejeKnap(range_min=0, range_max=100, range_step=10, label="b", start_value=40, accent_color=bcol)
        # knapper = VGroup(a_knap, b_knap).arrange(DOWN).scale(0.5).next_to(plane, RIGHT, aligned_edge=DOWN)
        # a = a_knap.tracker
        # b = b_knap.tracker
        a = ValueTracker(5.0)
        b = ValueTracker(40.0)
        graph = always_redraw(lambda:
            plane.plot(
                lambda x: a.get_value() * x + b.get_value(),
                x_range=[xmin, xmax], color=graph_col, stroke_width=2.5
            )
        )
        opa1, opa2 = ValueTracker(1), ValueTracker(1)
        graph_text = always_redraw(lambda:
            # MathTex(
            #     "y", "=", f"{a.get_value():.2f}", r"\cdot", "x", "+",
            #     f"{b.get_value():.2f}",
            #     color=graph_col
            # ).next_to(plane, UP, aligned_edge=LEFT)
            VGroup(
                MathTex("y = ").set_opacity(min(opa1.get_value(), opa2.get_value())),
                DecimalNumber(a.get_value(), num_decimal_places=2, color=acol).set_opacity(opa1.get_value()),
                MathTex(r"\cdot x + ").set_opacity(min(opa1.get_value(), opa2.get_value())),
                DecimalNumber(b.get_value(), num_decimal_places=2, color=bcol).set_opacity(opa2.get_value()),
            ).arrange(RIGHT).next_to(plane, UP, aligned_edge=LEFT)
        )
        _points = always_redraw(lambda: VGroup(*[
            Dot(
                plane.c2p(
                    plane.p2c(point.get_center())[0],
                    graph.underlying_function(plane.p2c(point.get_center())[0]),
                    0
                ),
                color=None
            ).scale(0.01) for point in points
            # ), color=None).scale(0.01) for point in points
        ]))
        self.add(_points)
        self.play(
            LaggedStart(
                DrawBorderThenFill(graph),
                Write(graph_text),
                lag_ratio=0.1
            ),
            run_time=2
        )
        # self.play(
        #     DrawBorderThenFill(knapper),
        #     run_time=1
        # )
        self.slide_pause()

        # srec = SurroundingRectangle(
        #     graph_text[:6],
        #     color=BLACK,
        #     fill_color=BLACK,
        #     fill_opacity=0.75
        # )
        # self.play(FadeIn(srec), run_time=0.5)
        self.play(opa1.animate.set_value(0.25), run_time=1.5)
        for i in [0, 80, 40]:
            self.play(
                b.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.play(opa1.animate.set_value(1), run_time=0.5)
        # self.play(FadeOut(srec), run_time=0.5)
        # self.wait(1)
        self.slide_pause()

        # srec = VGroup(
        #     SurroundingRectangle(graph_text[:2], color=BLACK, fill_color=BLACK,
        #                          fill_opacity=0.75),
        #     SurroundingRectangle(graph_text[3:], color=BLACK, fill_color=BLACK,
        #                          fill_opacity=0.75).shift(0.25 * RIGHT)
        # )
        # self.play(FadeIn(srec), run_time=0.5)
        self.play(opa2.animate.set_value(0.25), run_time=1.5)
        for i in [2, 20, 5]:
            self.play(
                a.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.play(opa2.animate.set_value(1), run_time=0.5)
        # self.play(FadeOut(srec), run_time=0.5)
        # self.wait(1)
        self.slide_pause()

        question = VGroup(
            Tex("Hvordan finder vi ud af,"),
            Tex("hvordan linjen skal placeres?")
        ).arrange(DOWN, aligned_edge=LEFT)
        srec = get_background_rect(question)
        self.play(
            LaggedStart(
                FadeIn(srec, run_time=0.25),
                Write(question, run_time=1),
                lag_ratio=1
            )
        )
        self.slide_pause()
        self.play(FadeOut(VGroup(question, srec), run_time=0.25))

        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------

        dotlines = always_redraw(
            lambda: VGroup(
                *[
                    Line(
                        start=point.get_center(),
                        end=gpoint.get_center(),
                        color=dev_cols[0] if gpoint.get_y() - point.get_y() < 0 else dev_cols[1],
                        stroke_width=2.5
                    ) for point, gpoint in zip(points, _points)
                ]
            )
        )
        self.play(
            LaggedStart(*[
                DrawBorderThenFill(line) for line in dotlines
            ],
                        lag_ratio=0.5,
                        rate_func=rate_functions.smooth
                        ),
            run_time=1.5
        )
        # self.wait(1)
        self.add(dotlines)
        self.slide_pause()

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(points[0]).shift(0.5 * UP),
            run_time=2
        )
        self.slide_pause()
        self.play(
            ShowPassingFlash(
                Line(
                    start=plane.c2p(plane.p2c(points[0].get_center())[0],
                                    graph.underlying_function(plane.p2c(points[0].get_center())[0])),
                    end=plane.c2p(*plane.p2c(points[0].get_center())),
                    stroke_width=3,
                    color=YELLOW
                ),
                time_width=1.5
            ),
            run_time=2
        )

        dotlines_text = always_redraw(lambda:
            VGroup(*[
                DecimalNumber(
                    plane.p2c(gpoint.get_center())[1] - plane.p2c(point.get_center())[1],
                    num_decimal_places=1,
                    include_sign=True,
                    color=dev_cols[0] if plane.p2c(gpoint.get_center())[1] - plane.p2c(point.get_center())[1] < 0 else dev_cols[1]
                ).scale(0.5).next_to(dotline, LEFT).shift(
                    0.2 * RIGHT
                ) for point, gpoint, dotline in zip(points, _points, dotlines)
            ])
        )
        self.play(
            Write(
                dotlines_text[0]
            ),
            run_time=0.5
        )
        self.slide_pause()
        self.play(
            LaggedStart(
                Restore(self.camera.frame),
                *[
                    Write(
                        dotline_text
                    ) for dotline_text in dotlines_text[1:]
                ],
                lag_ratio=0.1
            ),
            run_time=4
        )
        self.add(dotlines_text)
        self.slide_pause()

        dotlines_text_copy = always_redraw(lambda:
            VGroup(*[
                text.copy().scale(1.5).next_to(
                    graph_text, UP, aligned_edge=LEFT
                ).shift(
                    0.9 * UP + 1.10 * i * RIGHT
                ) for i, text in enumerate(dotlines_text)
            ])
        )
        self.play(
            ReplacementTransform(
                dotlines_text.copy(),
                dotlines_text_copy
            ),
            run_time=2
        )
        self.slide_pause()

        brace = Brace(
            VGroup(
                dotlines_text_copy
            ),
            DOWN
        )
        brace_text = Tex(
            "Sum af afvigelser fra grafen = "
        ).next_to(brace, DOWN).shift(0.2 * UP)
        dev_sum = always_redraw(lambda:
            DecimalNumber(
                sum([
                    plane.p2c(gpoint.get_center())[1] - plane.p2c(point.get_center())[1] for point, gpoint in zip(points, _points)
                ]),
                num_decimal_places=1,
                include_sign=True,
                color=dev_cols[
                    sum([
                        plane.p2c(gpoint.get_center())[1] - plane.p2c(point.get_center())[1] for point, gpoint in
                        zip(points, _points)
                    ]) >= 0
                ]
            ).next_to(brace_text, RIGHT)
        )
        self.play(
            GrowFromCenter(brace),
            run_time=1
        )
        self.wait(1)
        self.play(
            Write(VGroup(
                brace_text,
                dev_sum
            )),
            run_time=1
        )
        self.slide_pause()

        self.play(
            b.animate.set_value(60),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            b.animate.set_value(0),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            b.animate.set_value(20),
            run_time=1.5
        )
        self.slide_pause()

        question = VGroup(
            Tex("Hvordan finder vi ud af,"),
            Tex("hvordan linjen skal placeres?")
        ).arrange(DOWN, aligned_edge=LEFT)
        srec = get_background_rect(question)
        self.play(
            LaggedStart(
                FadeIn(srec, run_time=0.25),
                Write(question, run_time=1),
                lag_ratio=1
            )
        )
        self.slide_pause()

        self.play(
            FadeOut(
                VGroup(
                    question,
                    srec,
                    dotlines,
                    dotlines_text,
                    dotlines_text_copy,
                    brace,
                    brace_text,
                    dev_sum
                )
            ),
            run_time=1
        )
        # self.slide_pause()

        dotsquares = always_redraw(lambda:
            VGroup(*[
                Square(
                    side_length=np.abs(point.get_y() - gpoint.get_y()),
                    color=dev_cols[0],
                    stroke_width=2.5
                ).next_to(
                    ftp(point.get_center(), gpoint.get_center()),
                    DL,
                    buff=0
                ) for point, gpoint in zip(points, _points)
            ])
        )

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(points[0]).shift(0.5 * UP),
            run_time=2
        )
        self.slide_pause()

        self.play(
            ShowPassingFlash(
                Square(
                    side_length=dotlines[0].get_height(),
                    stroke_width=2.5,
                    color=YELLOW
                ).next_to(dotlines[0].get_top(), DL, buff=0),
                time_width=1.5
            ),
            run_time=3
        )
        self.play(
            LaggedStart(*[
                DrawBorderThenFill(sq) for sq in dotsquares
            ],
                        lag_ratio=0.5,
                        rate_func=rate_functions.smooth
                        ),
            run_time=1.5
        )
        self.add(dotsquares)
        self.slide_pause()

        dotsquares_text = always_redraw(lambda:
            VGroup(*[
                DecimalNumber(
                    (plane.p2c(gpoint.get_center())[1] - plane.p2c(point.get_center())[1]) ** 2,
                    num_decimal_places=1,
                    include_sign=True,
                    color=dev_cols[0]
                ).scale(0.45).move_to(sq) for sq, point, gpoint in zip(dotsquares, points, _points)
            ])
        )
        self.play(
            Write(
                dotsquares_text[0]
            ),
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                Restore(self.camera.frame),
                *[
                    Write(
                        dotsquare_text
                    ) for dotsquare_text in dotsquares_text[1:]
                ],
                lag_ratio=0.1
            ),
            run_time=4
        )
        self.add(dotsquares_text)
        self.slide_pause()

        dotsquares_text_copy = always_redraw(lambda:
            VGroup(*[
                text.copy().scale(1.1).next_to(
                graph_text, UP, aligned_edge=LEFT
                ).shift(
                    0.9 * UP + 1.10 * i * RIGHT
                ) for i, text in enumerate(dotsquares_text)
            ])
        )
        self.play(
            ReplacementTransform(
                dotsquares_text.copy(),
                dotsquares_text_copy
            ),
            run_time=2
        )
        self.slide_pause()

        brace = Brace(
            VGroup(
                dotsquares_text_copy
            ),
            DOWN
        )
        brace_text = Tex(
            "Sum af firkanternes areal = "
        ).next_to(brace, DOWN).shift(0.2 * UP)
        sq_sum = always_redraw(lambda:
            DecimalNumber(
                sum([
                    (
                            plane.p2c(gpoint.get_center())[1] - plane.p2c(point.get_center())[1]
                    ) ** 2 for point, gpoint in zip(points, _points)
                ]),
                num_decimal_places=1,
                include_sign=True,
                color=dev_cols[0]
            ).next_to(brace_text, RIGHT)
        )
        self.play(
            GrowFromCenter(brace),
            run_time=1
        )
        self.wait(1)
        self.play(
            Write(VGroup(
                brace_text,
                sq_sum
            )),
            run_time=1
        )
        self.slide_pause()

        for i in [60, 0, 20]:
            self.play(
                b.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.slide_pause()

        for i in [15, 10, 12]:
            self.play(
                a.animate.set_value(i),
                run_time=2
            )
            self.wait(0.5)
        self.wait(1)
        self.play(
            b.animate.set_value(10),
            run_time=2
        )
        self.slide_pause()

    def blabla(self):
        # =====================================================================
        # =====================================================================
        # =====================================================================

        question = VGroup(
            Tex("Hvordan finder vi ud af,"),
            Tex("hvordan linjen skal placeres?")
        ).arrange(DOWN, aligned_edge=LEFT)
        srec = SurroundingRectangle(
            plane,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.90
        ).scale(3)
        self.play(FadeIn(srec), run_time=1)
        self.wait(1)
        self.play(Write(question), run_time=2)
        self.wait(1)
        self.play(Unwrite(question, reverse=False), run_time=1)
        self.play(FadeOut(srec))
        # self.wait(1)
        self.slide_pause()



        # =====================================================================
        # =====================================================================
        # =====================================================================

        question = VGroup(
            Tex("Det fungerer ikke helt."),
            Tex("Kan vi gøre det bedre?")
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(FadeIn(srec), run_time=1)
        self.wait(1)
        self.play(Write(question), run_time=2)
        self.wait(1)
        self.play(Unwrite(question, reverse=False), run_time=1)



        fade_out_all(self)
        play_title_reverse(self, title=title)

