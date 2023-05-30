from manim import *
from helpers import *
import numpy as np

graph_col = YELLOW
a_col = PINK
lines_col = [RED, GREEN]
graph_params = {
    "xlims": (-2.5, 20.5, 1),
    "ylims": (-1.5, 11.5, 1),
    "width": 14
}

plane = NumberPlane(
    x_range=graph_params["xlims"],
    y_range=graph_params["ylims"],
    x_length=graph_params["width"],
    y_length=graph_params["width"] / 16 * 9,
    background_line_style={
        "stroke_color": TEAL,
        "stroke_width": 2,
        "stroke_opacity": 0.3
    },
    axis_config={"include_numbers": True}
)


class FordoblingsKonstant(MovingCameraScene):
    def construct(self):
        play_title(self, "Fordoblingskonstant")
        self.fordobling()
        srec = SurroundingRectangle(
            plane,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.90
        ).scale(3)
        self.play(FadeIn(srec), run_time=0.5)
        play_title(self, "Halveringskonstant")
        self.play(FadeOut(srec), run_time=0.5)
        self.halvering()
        play_title_reverse(self, "Fordoblings- og halveringskonstanter")

    def table_test(self):
        data_points = []
        for x, y in zip(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [10, 22, 30, 48, 62, 68, 76, 95, 104, 120, 125]
        ):
            data_points.append((x, y))
        data_points = np.array(data_points)
        table = create_table(data_points, orientation="vertical")
        self.add(table)

    def get_ylines(self, b, exp=1):
        return VGroup(*[Line(
            start=plane.c2p(0, 0),
            end=plane.c2p(0, (i + 1)**exp * b),
            color=col,
            stroke_width=5
        ) for i, col in enumerate(lines_col)])

    def get_pointlines(self, b, t, direction="h", exp=1):
        if direction == "h":
            return VGroup(*[DashedLine(
                start=plane.c2p(0, 2 ** ((i + 1)*exp) * b),
                end=plane.c2p((i + 1) * t, 2 ** ((i + 1)*exp) * b),
                color=col,
                stroke_width=3
            ) for i, col in enumerate(lines_col)])
        else:
            return VGroup(*[DashedLine(
                start=plane.c2p((i+1)*t, 2**((i + 1)*exp) * b),
                end=plane.c2p((i+1)*t, 0),
                color=col,
                stroke_width=3
            ) for i, col in enumerate(lines_col)])

    def get_ymarks(self, lines, exp=1):
        return VGroup(*[Line(
            start=plane.c2p(-0.25, 2**exp * plane.p2c(line.get_top())[1]),
            end=plane.c2p(0.25, 2**exp * plane.p2c(line.get_top())[1]),
            color=line.get_color(),
            stroke_width=3
        ) for line in lines])

    def get_xmarks(self, lines):
        return VGroup(*[Line(
            start=plane.c2p(plane.p2c(line.get_top())[0], -0.25),
            end=plane.c2p(plane.p2c(line.get_top())[0], 0.25),
            color=line.get_color(),
            stroke_width=3
        ) for line in lines])

    def fordobling(self):
        a, b = 1.08, 2.00
        t2 = np.log(2) / np.log(a)
        fordo_col = BLUE

        self.play(
            DrawBorderThenFill(
                plane
            ),
            run_time=1
        )
        m_pause(self)

        graph = plane.plot(
            lambda x: b * a**x,
            x_range=graph_params["xlims"],
            color=graph_col,
            stroke_width=2.5
        )
        graphText = VGroup(
            MathTex("y", "=", "b", "\\cdot", "a", "^x"),
            MathTex("y", "=", f"{b:.2f}", "\\cdot", f"{a:.2f}", "^x")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UR)
        graphText[0][4].set_color(a_col)
        graphText[1][4].set_color(a_col)
        self.play(
            LaggedStart(
                Create(
                    graph
                ),
                Write(
                    graphText
                ),
                lag_ratio=0.5
            ),
            run_time=1
        )
        m_pause(self)

        ylines = self.get_ylines(b)

        pointlinesh = self.get_pointlines(b, t2, "h")
        pointlinesv = self.get_pointlines(b, t2, "v")
        ymarks = self.get_ymarks(ylines)
        xmarks = self.get_xmarks(pointlinesv)
        for yline, xmark, ymark, lineh, linev in zip(ylines, xmarks, ymarks, pointlinesh, pointlinesv):
            ytext = Tex(
                str(int(b*yline.get_height())),
                color=yline.get_color(),
            ).next_to(yline, UL).shift(0.5*DOWN)
            self.play(
                Create(
                    yline
                ),
                Write(ytext, run_time=0.5),
                run_time=1
            )
            m_pause(self)
            self.play(
                yline.animate.shift(UP * yline.get_height()),
                ytext.animate.shift(UP * yline.get_height()),
                run_time=1
            )
            xs_pause(self)
            self.play(
                Transform(
                    VGroup(yline, ytext),
                    ymark
                ),
                run_time=1
            )
            s_pause(self)
            self.play(
                Create(
                    lineh
                ),
                run_time=2
            )
            m_pause(self)
            self.play(
                Create(
                    linev
                ),
                run_time=2
            )
            m_pause(self)
            self.play(
                TransformFromCopy(
                    linev,
                    xmark
                )
            )
            m_pause(self)

        braces = VGroup(
            *[
                BraceBetweenPoints(
                    point_1=plane.c2p(i * t2, 0),
                    point_2=plane.c2p((i + 1) * t2),
                    direction=UP,
                    color=xmark.get_color()
                ) for i, xmark in enumerate(xmarks)
            ]
        )
        braceTexts = VGroup(
            *[
                Tex(
                    str(int(t2)),
                    color=brace.get_color()
                ).next_to(brace, UP) for brace in braces
            ]
        )

        for brace, text in zip(braces, braceTexts):
            self.play(
                LaggedStart(
                    GrowFromCenter(
                        brace
                    ),
                    Write(
                        text
                    ),
                    lag_ratio=0.3
                ),
                run_time=1
            )
            m_pause(self)

        forklaring = VGroup(
            Text(f"Hver gang man går {t2:.0f}"),
            Text("hen ad x-aksen,"),
            Text("fordobles y-værdien på grafen.")
        ).arrange(DOWN, aligned_edge=LEFT)
        forklaring[0][-1].set_color(color_gradient(lines_col, 2))
        forklaring[2][:9].set_color(fordo_col)
        srec = SurroundingRectangle(
            forklaring,
            # color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.75,
            buff=MED_LARGE_BUFF
        )
        self.play(
            FadeIn(
                srec
            ),
            run_time=1
        )
        self.play(
            Write(
                forklaring
            ),
            run_time=1
        )
        l_pause(self)
        fordobling = VGroup(
            Tex("Dette kalder vi ", "fordobling", "skonstanten, ", "$T_2$"),
            Tex("og vi kan beregne den sådan:"),
            MathTex("T_2", " = ", "{\\log(2)", "\\over", "\\log(a)}")
        ).arrange(DOWN, aligned_edge=LEFT)
        fordobling[0][1].set_color(fordo_col)
        fordobling[0][-1][-1].set_color(fordo_col)
        fordobling[2][0][-1].set_color(fordo_col)
        fordobling[2][2][-2].set_color(fordo_col)
        fordobling[2][-1][-2].set_color(a_col)
        self.play(
            LaggedStart(
                Unwrite(forklaring, reverse=True),
                srec.animate.set_width(fordobling.get_width()*1.1),
                Write(fordobling),
                lag_ratio=0.5
            ),
            run_time=1
        )
        xl_pause(self)
        # self.play(
        #     FadeOut(
        #         *[
        #             m for m in self.mobjects if m != plane
        #         ]
        #     )
        # )
        fade_out_all(self)

    def halvering(self):
        a, b = 0.917, 10.00
        thalv = np.log(1/2) / np.log(a)
        halve_col = BLUE

        self.play(
            DrawBorderThenFill(
                plane
            ),
            run_time=1
        )
        m_pause(self)

        graph = plane.plot(
            lambda x: b * a**x,
            x_range=graph_params["xlims"],
            color=graph_col,
            stroke_width=2.5
        )
        graphText = VGroup(
            MathTex("y", "=", "b", "\\cdot", "a", "^x"),
            MathTex("y", "=", f"{b:.2f}", "\\cdot", f"{a:.3f}", "^x")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UR)
        graphText[0][4].set_color(a_col)
        graphText[1][4].set_color(a_col)
        self.play(
            LaggedStart(
                Create(
                    graph
                ),
                Write(
                    graphText
                ),
                lag_ratio=0.5
            ),
            run_time=1
        )
        m_pause(self)

        ylines = self.get_ylines(b, exp=-1)

        pointlinesh = self.get_pointlines(b, thalv, "h", exp=-1)
        pointlinesv = self.get_pointlines(b, thalv, "v", exp=-1)
        ymarks = self.get_ymarks(ylines, exp=-1)
        xmarks = self.get_xmarks(pointlinesv)
        for yline, xmark, ymark, lineh, linev in zip(ylines, xmarks, ymarks, pointlinesh, pointlinesv):
            ytext = always_redraw(lambda: DecimalNumber(
                plane.p2c(yline.get_end())[1],
                num_decimal_places=1,
                color=yline.get_color(),
            ).next_to(yline, UL).shift(0.5*DOWN))
            self.play(
                Create(
                    yline
                ),
                Write(ytext, run_time=0.5),
                run_time=1
            )
            m_pause(self)
            self.play(
                yline.animate.shift(DOWN * 0.25*yline.get_height()).scale(0.5),
                ytext.animate.shift(DOWN * 0.5*yline.get_height()),
                run_time=1
            )
            xs_pause(self)
            ytext.clear_updaters()
            self.play(
                Transform(
                    VGroup(yline, ytext),
                    ymark
                ),
                run_time=1
            )
            s_pause(self)
            self.play(
                Create(
                    lineh
                ),
                run_time=2
            )
            m_pause(self)
            self.play(
                Create(
                    linev
                ),
                run_time=2
            )
            m_pause(self)
            self.play(
                TransformFromCopy(
                    linev,
                    xmark
                )
            )
            m_pause(self)

        braces = VGroup(
            *[
                BraceBetweenPoints(
                    point_1=plane.c2p(i * thalv, 0),
                    point_2=plane.c2p((i + 1) * thalv),
                    direction=UP,
                    color=xmark.get_color()
                ) for i, xmark in enumerate(xmarks)
            ]
        )

        braceTexts = VGroup(
            *[
                Tex(
                    f"{thalv:.0f}",
                    color=brace.get_color()
                ).next_to(brace, UP) for brace in braces
            ]
        )

        for brace, text in zip(braces, braceTexts):
            self.play(
                LaggedStart(
                    GrowFromCenter(
                        brace
                    ),
                    Write(
                        text
                    ),
                    lag_ratio=0.3
                ),
                run_time=1
            )
            m_pause(self)

        forklaring = VGroup(
            Text(f"Hver gang man går {thalv:.0f}"),
            Text("hen ad x-aksen,"),
            Text("halveres y-værdien på grafen.")
        ).arrange(DOWN, aligned_edge=LEFT)
        forklaring[0][-1].set_color(color_gradient(lines_col, 2))
        forklaring[2][:8].set_color(halve_col)
        srec = SurroundingRectangle(
            forklaring,
            fill_color=BLACK,
            fill_opacity=0.75,
            buff=MED_LARGE_BUFF
        )
        self.play(
            FadeIn(
                srec
            ),
            run_time=1
        )
        self.play(
            Write(
                forklaring
            ),
            run_time=1
        )
        l_pause(self)
        halvering = VGroup(
            Tex("Dette kalder vi ", "halvering", "skonstanten, ", "$T_{1\\over2}$"),
            Tex("og vi kan beregne den sådan:"),
            MathTex("T_{1\\over2}", " = ", "{\\log({1\\over2})", "\\over", "\\log(a)}")
        ).arrange(DOWN, aligned_edge=LEFT)
        halvering[0][1].set_color(halve_col)
        halvering[0][-1][-3:].set_color(halve_col)
        halvering[2][0][-3:].set_color(halve_col)
        halvering[2][2][-4:-1].set_color(halve_col)
        halvering[2][-1][-2].set_color(a_col)
        self.play(
            LaggedStart(
                Unwrite(forklaring, reverse=True),
                srec.animate.set_width(halvering.get_width()*1.1),
                Write(halvering),
                lag_ratio=0.5
            ),
            run_time=1
        )
        xl_pause(self)
        fade_out_all(self)
        m_pause(self)

