from manim import *
from helpers import *
import numpy as np

slides = True
if slides:
    from manim_slides import Slide


class UgrupperetData(Slide if slides else Scene):
    def construct(self):
        title = Tex("Ugrupperet", " data")
        title[0].set_color(YELLOW)
        play_title(self, title)
        self.slide_pause(0.5)
        self.kvartiler()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides)

    def data_to_DecNum(self, data):
        return VGroup(
            *[DecimalNumber(
                    val,
                    include_sign=False,
                    num_decimal_places=0,
                ).scale(0.5) for val in data]
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)

    def tegn_boksplot(self, kvartiler, kvartiltekst):
        q0, q1, q2, q3, q4 = kvartiler
        plane = NumberLine(
            x_range=(kvartiler[0]-2, kvartiler[-1]+2, 1),
            length=12,
            include_tip=True,
            include_numbers=True
        ).shift(2*DOWN)
        self.play(
            DrawBorderThenFill(plane)
        )
        self.slide_pause(0.5)
        full_plot = VGroup(plane)
        for q, t in zip([q0, q4], [kvartiltekst[1], kvartiltekst[9]]):
            line = Line(
                start=plane.n2p(q) + 0.5*UP,
                end=plane.n2p(q) + 1*UP
            )
            hnum = t.copy().scale(0.75).move_to(plane.n2p(q)+2*UP)
            self.play(
                DrawBorderThenFill(
                    line
                ),
                Circumscribe(t),
                DrawBorderThenFill(hnum),
                run_time=2
            )
            full_plot += line
            self.slide_pause(0.5)
        for q, t in zip([q2, q1, q3], [kvartiltekst[5], kvartiltekst[3], kvartiltekst[7]]):
            line = Line(
                start=plane.n2p(q),
                end=plane.n2p(q) + 1.5*UP
            )
            hnum = t.copy().scale(0.75).move_to(plane.n2p(q)+2*UP)
            self.play(
                DrawBorderThenFill(
                    line
                ),
                Circumscribe(t),
                DrawBorderThenFill(hnum),
                run_time=2
            )
            full_plot += line
            self.slide_pause(0.5)

        box = Rectangle(
            height=1.5,
            width=plane.n2p(q3)[0]-plane.n2p(q1)[0],
            fill_color=BLUE,
            fill_opacity=1,
            z_index=-1,
            stroke_width=0.1
        ).move_to(0.5*(plane.n2p(q3)+plane.n2p(q1))+0.75*UP)
        full_plot += box
        lines = VGroup(
            *[
                Line(
                    start=plane.n2p(ql) + 0.75 * UP,
                    end=plane.n2p(qh) + 0.75 * UP
                ) for ql, qh in zip([q0, q3], [q1, q4])
            ],
            Line(
                start=plane.n2p(q1) + 1.5 * UP,
                end=plane.n2p(q3) + 1.5 * UP
            )
        )
        full_plot += lines
        self.play(
            LaggedStart(
                DrawBorderThenFill(lines),
                lag_ratio=0.1
            ),
            FadeIn(box),
            run_time=2
        )
        self.slide_pause(0.5)
        self.add(full_plot)
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != full_plot]
        )
        return full_plot


    def kvartiler(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(d) for d in data],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause(0.5)

        steps = VGroup(
            Tex("Trin 1: Sortér data"),
            Tex("Trin 2: Find midterste tal"),
            Tex("Trin 3: Trin 2, men nederste halvdel"),
            Tex("Trin 4: Trin 2, men øverste halvdel")
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_edge(UR, buff=1.5)
        self.play(
            Write(steps[0]),
            run_time=2
        )
        self.slide_pause(0.5)

        data_ordered = self.data_to_DecNum(sorted(data_raw)).next_to(data, RIGHT, buff=2)
        self.play(
            TransformFromCopy(
                data,
                data_ordered
            )
        )
        self.slide_pause(0.5)

        self.play(
            Write(steps[1]),
            steps[0].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        topArrow = Arrow(
            start=0.5*LEFT,
            end=0.5*RIGHT,
            color=BLUE
        ).next_to(data_ordered[0], LEFT)
        botArrow = Arrow(
            start=0.5*RIGHT,
            end=0.5*LEFT,
            color=RED
        ).next_to(data_ordered[-1], RIGHT)
        self.play(
            Create(topArrow),
            Create(botArrow),
        )

        index_median = 0
        median = np.median(data_raw)
        for i in np.arange(len(data)-2)+1:
            self.play(
                topArrow.animate.next_to(data_ordered[i], LEFT),
                botArrow.animate.next_to(data_ordered[-1-i], RIGHT),
                run_time=2/(0.2*i+1)
            )
            if topArrow.get_center()[1] <= botArrow.get_center()[1]:
                self.play(
                    data_ordered[i].animate.set_color(YELLOW),
                    run_time=2
                )
                median = data_ordered[i].copy()
                self.play(
                    median.animate.next_to(steps[1], RIGHT, buff=1.5),
                    data_ordered[:i].animate.set_color(topArrow.get_color()),
                    data_ordered[-i:].animate.set_color(botArrow.get_color()),
                    # topArrow.animate.next_to(data_ordered[0], LEFT).set_opacity(0),
                    # botArrow.animate.next_to(data_ordered[i-1], RIGHT).set_opacity(0)
                    FadeOut(topArrow, botArrow)
                )
                # self.remove(topArrow, botArrow)
                index_median = i
                break

        # topArrow.set_opacity(1)
        # botArrow.set_opacity(1)
        topArrow.next_to(data_ordered[0], LEFT)
        botArrow.next_to(data_ordered[index_median-1], RIGHT).set_color(BLUE_C)

        self.slide_pause(0.5)
        self.play(
            Write(steps[2]),
            VGroup(steps[1], median).animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        self.play(
            FadeIn(topArrow),
            FadeIn(botArrow),
        )

        index_q1 = 0
        q1 = 0
        for i in np.arange(index_median) + 1:
            self.play(
                topArrow.animate.next_to(data_ordered[i], LEFT),
                botArrow.animate.next_to(data_ordered[index_median - i - 1], RIGHT),
                run_time=2/(0.2*i+1)
            )
            if topArrow.get_center()[1] == botArrow.get_center()[1]:
                print("HEJ")
            if topArrow.get_center()[1] < botArrow.get_center()[1]:
                self.play(
                    VGroup(data_ordered[i], data_ordered[i-1]).animate.set_color(YELLOW),
                    run_time=2
                )
                nums = [data_ordered[i-1].get_value(), data_ordered[i].get_value()]
                calculation_q1 = MathTex(
                    f"{{{data_ordered[i-1].get_value()}",
                    "+",
                    f"{data_ordered[i].get_value()}",
                    r"\over",
                    "2}",
                    "=",
                    # f"{np.mean(data_ordered[i-1].get_value(), data_ordered[i].get_value())}"
                    f"{np.mean(nums):.0f}"
                ).next_to(VGroup(data_ordered[i-1:i+1]), RIGHT).scale(0.5)
                calculation_q1[0].set_color(YELLOW)
                calculation_q1[2].set_color(YELLOW)
                calculation_q1[-1].set_color(YELLOW)
                q1_brace = Brace(
                    VGroup(data_ordered[i - 1:i + 1]),
                    RIGHT,
                    sharpness=0.1
                )
                self.play(
                    # Write(calculation),
                    TransformFromCopy(
                        VGroup(data_ordered[i - 1:i + 1]),
                        calculation_q1
                    ),
                    FadeOut(topArrow, botArrow),
                    Create(q1_brace),
                    run_time=1
                )
                self.slide_pause(0.5)
                index_q1 = i
                q1 = DecimalNumber(
                    np.mean(nums),
                    include_sign=False,
                    num_decimal_places=0,
                    color=YELLOW
                ).scale(0.5).next_to(calculation_q1, RIGHT, buff=-0.15)
                q1num = int(np.mean(nums))
                self.add(q1)
                self.play(
                    q1.animate.next_to(steps[2], RIGHT, buff=0.37),
                    data_ordered[:i-1].animate.set_color(topArrow.get_color()),
                    data_ordered[i+1:index_median].animate.set_color(botArrow.get_color()),
                )
                break

        self.slide_pause(0.5)
        self.play(
            Write(steps[3]),
            VGroup(steps[2], q1).animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        topArrow.next_to(data_ordered[index_median+1], LEFT).set_color(RED)
        botArrow.next_to(data_ordered[-1], RIGHT).set_color(RED_C)

        self.play(
            FadeIn(
                topArrow,
                botArrow
            )
        )
        self.slide_pause()

        index_q3 = 0
        q3 = 0
        for i in np.arange(index_median) + 1:
            it = index_median + i
            ib = len(data) - i
            self.play(
                topArrow.animate.next_to(data_ordered[it], LEFT),
                botArrow.animate.next_to(data_ordered[ib], RIGHT),
                run_time=2/(0.2*i+1)
            )
            if topArrow.get_center()[1] == botArrow.get_center()[1]:
                print("HEJ")
            if topArrow.get_center()[1] < botArrow.get_center()[1]:
                self.play(
                    VGroup(data_ordered[ib], data_ordered[it]).animate.set_color(YELLOW),
                    run_time=2
                )
                nums = [data_ordered[ib].get_value(), data_ordered[it].get_value()]
                calculation_q3 = MathTex(
                    f"{{{data_ordered[ib].get_value()}",
                    "+",
                    f"{data_ordered[it].get_value()}",
                    r"\over",
                    "2}",
                    "=",
                    # f"{np.mean(data_ordered[i-1].get_value(), data_ordered[i].get_value())}"
                    f"{np.mean(nums):.1f}"
                ).next_to(VGroup(data_ordered[ib:it+1]), RIGHT, buff=0).scale(0.5)
                calculation_q3[0].set_color(YELLOW)
                calculation_q3[2].set_color(YELLOW)
                calculation_q3[-1].set_color(YELLOW)
                q3_brace = Brace(
                    VGroup(data_ordered[ib:it+1]),
                    RIGHT,
                    sharpness=0.1
                )#.next_to(VGroup(data_ordered[ib:it]), RIGHT)
                self.play(
                    # Write(calculation),
                    TransformFromCopy(
                        VGroup(data_ordered[ib:it]),
                        calculation_q3
                    ),
                    FadeOut(topArrow, botArrow),
                    Create(q3_brace),
                    run_time=1
                )
                self.slide_pause(0.5)
                index_q3 = ib
                q3 = DecimalNumber(
                    np.mean(nums),
                    include_sign=False,
                    num_decimal_places=1,
                    color=YELLOW
                ).scale(0.5).next_to(calculation_q3, RIGHT, buff=-0.15)
                q3num = np.mean(nums)
                self.add(q3)
                self.play(
                    q3.animate.next_to(steps[3:], RIGHT, buff=0.25),
                    # data_ordered[index_median+1:index_q3].animate.set_color(topArrow.get_color()),
                    # data_ordered[index_q3+1:].animate.set_color(botArrow.get_color()),
                )
                break

        self.slide_pause(0.5)

        kvartiler = [min(data_raw), q1num, median.get_value(),
                     q3num, max(data_raw)]
        kvartil_tekst = Tex(
            "Kvartilsættet er derfor"
        )
        kvartilsaet = MathTex(
            "\{", q1num, "; ", median.get_value(), "; ", q3num, "\}"
        ).next_to(kvartil_tekst, DOWN)
        for i in [1, 3, 5]:
            kvartilsaet[i].set_color(YELLOW)
        self.play(
            *[m.animate.set_opacity(0.25) for m in self.mobjects],  # if m not in [median, q1, q3]],
            # *[m.animate.set_opacity(1) for m in [median, q1]],
            TransformFromCopy(VGroup(median, q1, q3), kvartilsaet),
            Write(kvartil_tekst),
            run_time=2
        )
        self.slide_pause(0.5)

        kvartilu_tekst = Tex(
            "Det udvidede kvartilsæt er"
        )
        kvartilsaetu = MathTex(
            "\{", min(data_raw), "; ", q1num, "; ",
            median.get_value(), "; ", q3num, "; ", max(data_raw), "\}"
        ).next_to(kvartil_tekst, DOWN)
        for i in [1, 3, 5, 7, 9]:
            kvartilsaetu[i].set_color(YELLOW)
        self.play(
            Transform(
                kvartil_tekst,
                kvartilu_tekst
            ),
            Transform(
                kvartilsaet,
                kvartilsaetu
            ),
            run_time=2
        )
        self.slide_pause(0.5)

        self.play(
            kvartilu_tekst.animate.to_edge(UL),
            kvartilsaetu.animate.to_edge(UP).shift(3*RIGHT),
            *[FadeOut(m) for m in self.mobjects if m not in [kvartilsaetu, kvartilu_tekst]],
            run_time=2
        )
        self.slide_pause(0.5)

        boksplot = self.tegn_boksplot(kvartiler, kvartilsaetu)


class SampleSize(Slide if slides else Scene):
    def construct(self):
        np.random.seed(42)
        self.slide_pause(0.1)
        pop_size = 3
        sam_size = ValueTracker(0.0)
        # responds = Dot(radius=0.04, color=YELLOW)
        num_res = 500

        scene_marker("Genererer locations")
        locs = [[0.1, 0, 0]]
        for i in range(num_res - 1):
            x, y = 10, 10
            while x**2 + y**2 >= pop_size**2:
                x, y = np.random.uniform(-pop_size, pop_size, 2)
            locs.append([x, y, 0])
        scene_marker(f"{len(locs)} locations genereret")

        population = Circle(radius=pop_size, color=GREEN)
        xt, yt = ValueTracker(0), ValueTracker(0)
        sample = always_redraw(lambda:
            Circle(radius=sam_size.get_value(), color=BLUE).move_to([xt.get_value(), yt.get_value(), 0])
        )
        # respondents = VGroup(*[
        #     responds.copy().move_to(loc) for loc in locs
        # ])
        respondents = always_redraw(lambda: VGroup(*[
            Dot(
                radius=0.04,
                # color=YELLOW if l[0]**2+l[1]**2 >= sam_size.get_value()**2 else BLUE
                color=YELLOW if (l[0]-xt.get_value())**2 + (l[1]-yt.get_value())** 2 >= sam_size.get_value()**2 else BLUE
            ).move_to(l) for l in locs
        ]))
        scene_marker("Respondenter genereret")

        # num_sam = always_redraw(lambda: DecimalNumber(
        #     len([l for l in locs if l[0] ** 2 + l[1] ** 2 < sam_size.get_value() ** 2])
        # ))
        disp_res = VGroup(Tex("Population: "), MathTex(f"{num_res}", color=GREEN)).arrange(RIGHT).to_edge(UL)
        disp_sam = always_redraw(lambda: VGroup(
            Tex("Respondenter: "),
            # MathTex(f"{len([l for l in locs if l[0] ** 2 + l[1] ** 2 < sam_size.get_value() ** 2])}", color=BLUE)
            # MathTex(f"{len([self.is_in_circle(l, sample) for l in locs])}", color=BLUE)
            MathTex(
                f"{len([l for l in locs if (l[0]-xt.get_value())**2 + (l[1]-yt.get_value())** 2 < sam_size.get_value()**2])}",
                color=BLUE
            )
        ).arrange(RIGHT).next_to(disp_res, DOWN, aligned_edge=LEFT))
        disp_pct = always_redraw(lambda: VGroup(
            Tex("Pct.:"),
            # MathTex(f"{len([l for l in locs if l[0] ** 2 + l[1] ** 2 < sam_size.get_value() ** 2])/num_res*100:.2f} \%", color=BLUE)
            # MathTex(f"{len([self.is_in_circle(l, sample) for l in locs])/num_res*100:.2f} \%", color=BLUE)
            MathTex(
                f"{len([l for l in locs if (l[0]-xt.get_value())**2 + (l[1]-yt.get_value())** 2 < sam_size.get_value() ** 2])/num_res*100:.2f} \%",
                color=BLUE
            )
        ).arrange(RIGHT).next_to(disp_sam, DOWN, aligned_edge=LEFT))

        self.play(
            Create(respondents),
            run_time=2
        )
        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(population),
            run_time=0.5
        )
        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(sample),
            run_time=0.5
        )
        self.play(
            Write(disp_res),
            Write(disp_sam),
            Write(disp_pct),
            run_time=0.5
        )
        self.slide_pause()

        for d in [4, 2, 1.1, 1]:
            self.play(
                sam_size.animate.set_value(pop_size/d),
                run_time=5
            )
            self.slide_pause()
            if d == 4:
                for x, y in np.append(np.random.uniform(low=-2, high=2, size=(4, 2)), [[0, 0]], axis=0):
                    self.play(
                        xt.animate.set_value(x),
                        yt.animate.set_value(y),
                        run_time=3
                    )
                self.slide_pause()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides)

    def is_in_circle(self, point, circle):
        print((point[0]-circle.get_center()[0])**2, circle.radius**2)
        if (point[0]-circle.get_center()[0])**2 + (point[1]-circle.get_center()[1])**2 < circle.get_radius()**2:
            return point


