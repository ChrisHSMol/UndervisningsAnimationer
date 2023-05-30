from manim import *
from helpers import *

slides = False
if slides:
    from manim_slides import Slide

# xlims = (-0.05, 1.05, 0.1)
# ylims = (-5, 55, 10)
# limfac = 0.01
xlims = (-0.5, 15.5, 2)
ylims = (-5, 55, 10)
limfac = 0.1
width = 7
plane = Axes(
    x_range=xlims,
    y_range=ylims,
    x_length=width,
    y_length=width * (ylims[1]-ylims[0])/(xlims[1]-xlims[0]) * limfac,
)


class HoppendeBold(Slide if slides else MovingCameraScene):
    def construct(self):
        title = Tex("Mekanisk energi af en", "hoppende bold").arrange(DOWN, aligned_edge=LEFT)
        title[1].set_color(YELLOW)
        # play_title(self, title)
        self.slide_pause(0.5)
        self.basketboldTest()
        # self.basketbold()

    def slide_pause(self, t=0.5, slides_bool=slides):
        if slides_bool:
            indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
            self.play(FadeIn(indicator), run_time=0.25)
            xs_pause(self)
            self.pause()
            self.play(FadeOut(indicator), run_time=0.25)
        else:
            self.wait(t)

    def get_ground_lines(self, line, n=10, alpha=0.25):
        line_length = line.get_length()/n
        ground_lines = VGroup()
        for i in range(n):
            ground_lines.add(
                Line(
                    start=line.get_start() + line_length*(i+1)*RIGHT,
                    end=line.get_start() + line_length*(i*RIGHT + DOWN),
                    stroke_opacity=alpha
                )
            )
        return ground_lines

    def basketbold(self):
        h_col = BLUE
        kin_col = GREEN

        svg_path = r"SVGs\basketball.svg"
        ball = SVGMobject(svg_path)
        self.play(
            DrawBorderThenFill(ball),
            run_time=0.5
        )
        self.slide_pause()
        ground = VGroup(
            Line().scale(2).to_edge(DL, buff=1)
        )
        ground.add(*self.get_ground_lines(ground[0]))
        self.play(
            DrawBorderThenFill(ground)
        )
        self.slide_pause()
        self.play(
            ball.animate.scale(0.5).next_to(ground, UP, buff=0)
        )
        self.slide_pause()
        ball_ref = ball.copy()

        # t = ValueTracker(0)
        g = 9.82
        h = ValueTracker(0)
        # h = always_redraw(lambda: DecimalNumber(0.5 * t.get_value()**2 * g))
        h_top = 5
        m = ValueTracker(1)
        # ball.add_updater(lambda mob: mob.shift(h.get_value() * UP))
        ball.add_updater(lambda mob: mob.move_to(ball_ref.get_center() + h.get_value()*UP))
        # ball.add_updater(lambda mob: mob.move_to(ball_ref.get_center() + 0.10 * 0.5 * t.get_value()**2 * g * UP))
        # ball.add_updater(lambda mob: mob.move_to(ball_ref.get_center() + t.get_value() * UP))
        # self.play(
        #     h.animate.set_value(5),
        #     # t.animate.set_value(3),
        #     run_time=2
        # )
        self.slide_pause()
        h_brace = always_redraw(lambda:
            BraceBetweenPoints(
                point_1=ball_ref.get_center() + 0.5*ball_ref.get_height()*DL,
                point_2=ball.get_center() + 0.5*ball_ref.get_height()*DL,
                direction=LEFT,
                color=h_col
            )
        )
        h_text = always_redraw(lambda:
            DecimalNumber(
                h.get_value()*10,
                # 0.5 * t.get_value() ** 2 * g,
                num_decimal_places=1,
                include_sign=False,
                color=h_col
            # ).next_to(ball, LEFT)
            ).next_to(h_brace, UL)
        )
        self.play(
            Write(h_text),
            GrowFromCenter(h_brace)
        )
        self.slide_pause()

        plane.to_edge(RIGHT)
        self.play(
            DrawBorderThenFill(
                plane
            )
        )
        self.slide_pause(1)
        print(m.get_value(), g, h.get_value())
        graph_pot = always_redraw(lambda:
            plane.plot(
                # lambda x: m.get_value() * g * h.get_value(),
                lambda x: m.get_value() * g * x,
                x_range=[0, h.get_value()],
                color=h_col
            )
        )
        graph_kin = always_redraw(lambda:
            plane.plot(
                lambda x: m.get_value() * g * (h_top - x),
                x_range=[0, h.get_value()],
                color=kin_col
            )
        )
        self.play(
            Create(graph_pot, graph_kin)
        )

        for v, rfunc in zip([5, 0], [rate_functions.rush_into, rate_functions.rush_from]):
        # for v, rfunc in zip([0, 3], [rate_functions.rush_into, rate_functions.rush_from]):
            self.play(
                h.animate.set_value(v),
                # t.animate.set_value(v),
                rate_func=rfunc,
                run_time=2
            )
            # break
        self.slide_pause()

    def basketboldTest(self):
        pot_col = BLUE
        kin_col = GREEN
        mek_col = YELLOW
        test = True

        svg_path = r"SVGs\basketball.svg"
        ball = SVGMobject(svg_path)
        if test:
            self.add(ball)
        else:
            self.play(
                DrawBorderThenFill(ball),
                run_time=0.5
            )
            self.slide_pause()
        ground = VGroup(
            Line().scale(2).to_edge(DL, buff=1)
        )
        ground.add(*self.get_ground_lines(ground[0]))
        if test:
            self.add(ground, ball.scale(0.5).next_to(ground, UP, buff=0))
        else:
            self.play(
                DrawBorderThenFill(ground)
            )
            self.slide_pause()
            self.play(
                ball.animate.scale(0.5).next_to(ground, UP, buff=0)
            )
            self.slide_pause()
        ball_ref = ball.copy()

        t = ValueTracker(0)
        g = 9.82
        m = ValueTracker(1)
        h_max = 5

        def d(time, a=g, h0=h_max):  # Displacement
            return h0 - 0.5 * a * time**2

        def vf(time, a=g):  # final velocity
            return a * time

        def epot(time, mass=m.get_value(), a=g):
            return d(time) * mass * a

        ball.add_updater(lambda mob: mob.move_to(ball_ref.get_center() + d(t.get_value())*UP))
        h_brace = always_redraw(lambda:
            BraceBetweenPoints(
                point_1=ball_ref.get_center() + 0.5*ball_ref.get_height()*DL,
                point_2=ball.get_center() + 0.5*ball_ref.get_height()*DL,
                direction=LEFT,
                color=pot_col
            )
        )
        h_text = always_redraw(lambda:
            DecimalNumber(
                d(t.get_value()),
                num_decimal_places=1,
                include_sign=False,
                color=pot_col
            ).next_to(h_brace, UL)
        )
        plane = Axes(
            x_range=(-0.05, 1.15, 0.1),
            y_range=(-5, 65, 10),
            x_length=7,
            # y_length=4.5
            y_length=7
        # ).to_edge(RIGHT)
        ).to_edge(DR, buff=0.55)
        if test:
            self.add(h_brace, h_text, plane)

        # graph_pot = always_redraw(lambda:
        #     plane.plot(
        #         lambda x: epot(t.get_value()),
        #         # epot(t.get_value),
        #         color=pot_col,
        #         x_range=[0, t.get_value()]
        #     )
            # Dot(
            #     plane.c2p(t.get_value(), epot(t.get_value())),
            #     color=pot_col
            # )
        # )
        # graph_pot = TracedPath(
        #     Dot(epot(t.get_value())).get_center
        # )
        # graph_pot = plane.plot(
        #     always_redraw(lambda: epot(t.get_value))
        # )
        graph_pot = plane.plot(
            lambda x: epot(x),
            x_range=[0, 1],
            color=pot_col,
            z_index=plane.get_z_index()-2
        )
        graph_kin = plane.plot(
            lambda x: epot(0) - epot(x),
            x_range=[0, 1],
            color=kin_col,
            z_index=plane.get_z_index()-2
        )
        graph_mek = plane.plot(
            lambda x: epot(0),
            x_range=[0, 1],
            color=mek_col,
            z_index=plane.get_z_index()-2
        )
        graph_rect = always_redraw(lambda:
            SurroundingRectangle(
                graph_pot,
                buff=0,
                z_index=plane.get_z_index()-1,
                color=BLACK,
                fill_color=BLACK,
                fill_opacity=1,
            ).scale(1.05).shift(6*t.get_value()*RIGHT)
            # ).shift(plane.get_width()*t.get_value()*RIGHT)
        )
        mek_text = MathTex(
            r"E_{mek}", "=",
            r"E_{kin}", "+", r"E_{pot}"
        ).next_to(graph_mek, UP)
        mek_text[0].set_color(mek_col)
        mek_text[2].set_color(kin_col)
        mek_text[4].set_color(pot_col)
        self.play(Write(mek_text), run_time=0.75)
        self.add(graph_pot, graph_kin, graph_mek, graph_rect)

        vel_arrow = always_redraw(lambda:
            Arrow(
                start=ball.get_center(),
                end=ball.get_center() + np.sqrt(vf(t.get_value())) * DOWN,
                color=kin_col
            )
        )
        self.add(vel_arrow)

        self.play(
            t.animate.set_value(1),
            run_time=10,
            rate_func=rate_functions.rush_into
        )
        self.slide_pause(5)


