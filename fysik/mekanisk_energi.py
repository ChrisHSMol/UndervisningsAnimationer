from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = True
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
        play_title(self, title)
        self.slide_pause(0.5)
        self.basketbold()
        # self.slide_pause()
        self.dampening()
        self.slide_pause()

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
        pot_col = BLUE
        kin_col = GREEN
        mek_col = YELLOW
        test = False

        svg_path = r"..\SVGs\basketball.svg"
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
            return h0 - 0.5 * a * time**2 if time <= 1 else h0 - 0.5 * a * (2 - time)**2

        def vf(time, a=g):  # final velocity
            return a * time if time <= 1 else a * (2 - time)

        def epot(time, mass=m.get_value(), a=g):
            return d(time) * mass * a

        if not test:
            self.play(ball.animate.move_to(ball_ref.get_center() + d(t.get_value())*UP))

        ball.add_updater(lambda mob:
            mob.move_to(ball_ref.get_center() + d(t.get_value())*UP)
        )
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
                num_decimal_places=2,
                include_sign=False,
                color=pot_col
            ).next_to(h_brace, UL)
        )
        plane = Axes(
            x_range=(-0.05, 2.15, 0.1),
            y_range=(-5, 65, 10),
            x_length=7,
            # y_length=4.5
            y_length=7
        # ).to_edge(RIGHT)
        ).to_edge(DR, buff=0.55)
        if test:
            self.add(h_brace, h_text, plane)
        else:
            self.play(
                DrawBorderThenFill(h_brace),
                Write(h_text),
                Create(plane, lag_ratio=0.5),
                run_time=2
            )
            self.slide_pause()

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
        graph_mek = always_redraw(lambda: plane.plot(
            lambda x: epot(0),
            x_range=[0, t.get_value()],
            color=mek_col,
            z_index=plane.get_z_index()-2
        ))
        graph_pot = always_redraw(lambda: plane.plot(
            lambda x: max(epot(x), epot(2 - x)),
            x_range=[0, t.get_value()],
            color=pot_col,
            z_index=plane.get_z_index()-2
        ))
        graph_kin = always_redraw(lambda: plane.plot(
            lambda x: graph_mek.underlying_function(x) - graph_pot.underlying_function(x),
            x_range=[0, t.get_value()],
            color=kin_col,
            z_index=plane.get_z_index()-2
        ))
        mek_text = MathTex(
            r"E_{mek}", "=",
            r"E_{kin}", "+", r"E_{pot}"
        ).move_to(plane.c2p(1, epot(0)*1.125))
        mek_text[0].set_color(mek_col)
        mek_text[2].set_color(kin_col)
        mek_text[4].set_color(pot_col)
        self.play(Write(mek_text), run_time=0.75)
        self.add(graph_pot, graph_kin, graph_mek)  # , graph_rect)

        vel_arrow = always_redraw(lambda:
            Arrow(
                start=ball.get_center(),
                end=ball.get_center() + 0.5 * np.sqrt(vf(t.get_value())) * DOWN
                if t.get_value() <= 1 else ball.get_center() + 0.5 * np.sqrt(vf(t.get_value())) * UP,
                color=kin_col,
                buff=0
            )
        )
        self.add(vel_arrow)

        self.play(
            t.animate.set_value(1),
            run_time=5,
            rate_func=rate_functions.rush_into
        )
        self.play(
            t.animate.set_value(2),
            run_time=5,
            rate_func=rate_functions.rush_from
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [ball, plane, ground, h_text, h_brace]]
        )
        self.remove(ball, plane, ground, h_text, h_brace)

    def dampening(self):
        pot_col = BLUE
        kin_col = GREEN
        mek_col = YELLOW

        ground = VGroup(
            Line().scale(2).to_edge(DL, buff=1)
        )
        ground.add(*self.get_ground_lines(ground[0]))
        svg_path = r"..\SVGs\basketball.svg"
        ball = SVGMobject(svg_path).scale(0.5).next_to(ground, UP, buff=0).shift(5*UP)
        ball_ref = ball.copy().next_to(ground, UP, buff=0)

        t = ValueTracker(0)
        g = 9.82
        m = ValueTracker(1)
        h_max = 5
        bounce_factor = 0.75
        t_max = 8
        damp_fact = Tex(fr"Tab pr. hop: {(1-bounce_factor)*100:.1f}\%").to_edge(UL)

        # def d(time, a=g, h0=h_max, bounce_factor=0.5, t_max=t_max):  # Displacement
        #     di = [
        #         h0 - 0.5 * a * time ** 2,
        #         bounce_factor**1 * (h0 - 0.5 * a * (2 - time) ** 2),
        #         bounce_factor**2 * (h0 - 0.5 * a * (time - 2) ** 2),
        #         bounce_factor**3 * (h0 - 0.5 * a * (4 - time) ** 2),
        #         bounce_factor**4 * (h0 - 0.5 * a * (time - 4) ** 2),
        #         bounce_factor**5 * (h0 - 0.5 * a * (6 - time) ** 2),
        #         bounce_factor**6 * (h0 - 0.5 * a * (time - 6) ** 2),
        #     ]
        #     return di[int(np.floor(time))]

        def vf(time, a=g):  # final velocity
            return a * time if time <= 1 else a * (2 - time)

        def epot(height, mass=m.get_value(), a=g):
            return height * mass * a

        # ball.add_updater(lambda mob:
        #     mob.move_to(ball_ref.get_center() + d(t.get_value())*UP)
        # )
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
                ball.get_center()[1] - ball_ref.get_center()[1],
                num_decimal_places=2,
                include_sign=False,
                color=pot_col
            ).next_to(h_brace, UL)
        )
        plane = always_redraw(lambda: Axes(
            x_range=(-0.05, t_max + 0.15, 0.5),
            y_range=(-5, 65, 10),
            x_length=7,
            y_length=7
        ).to_edge(DR, buff=0.55))
        graph_mek = always_redraw(lambda: plane.plot(
            # lambda x: epot(0) * bounce_factor**int(np.floor(0.5 * (x+1))),
            lambda x: epot(h_max * bounce_factor**int(np.floor(0.5 * (x+1)))),
            x_range=[0, t.get_value()],
            color=mek_col,
            z_index=plane.get_z_index()-2,
            discontinuities=[2*i + 1 for i in range(t_max)]
        ))
        meklines = VGroup(*[
            Line(
                start=plane.c2p(2 * i + 0.98, epot(h_max * bounce_factor**i)),
                end=plane.c2p(2 * i + 1.02, epot(h_max * bounce_factor**(i + 1))),
                color=mek_col
            ) for i in range(t_max//2)
        ])
        graph_pot = always_redraw(lambda: plane.plot(
            lambda x: [
                epot(h_max) * (1 - x**2),
                epot(h_max) * bounce_factor * (4*x - 3 - x**2),
                epot(h_max) * bounce_factor**2 * (8*x - 15 - x**2),
                epot(h_max) * bounce_factor**3 * (12*x - 35 - x**2),
                epot(h_max) * bounce_factor**4 * (16*x - 63 - x**2),
                epot(h_max) * bounce_factor**4 * (20*x - 99 - 1),
            ][int(np.floor(0.5 * (x+1)))],
            x_range=[0, t.get_value()],
            color=pot_col,
            z_index=plane.get_z_index()-2
        ))
        graph_kin = always_redraw(lambda: plane.plot(
            lambda x: graph_mek.underlying_function(x) - graph_pot.underlying_function(x),
            x_range=[0, t.get_value()],
            color=kin_col,
            z_index=plane.get_z_index()-2
        ))
        mek_text = MathTex(
            r"E_{mek}", "=",
            r"E_{kin}", "+", r"E_{pot}"
        ).move_to(plane.c2p(t_max * 3/4, epot(h_max)*1.125))
        mek_text[0].set_color(mek_col)
        mek_text[2].set_color(kin_col)
        mek_text[4].set_color(pot_col)

        self.add(ball, plane, ground, h_text, h_brace, graph_pot, graph_kin, graph_mek)
        self.wait()
        self.play(Write(mek_text), Write(damp_fact))
        self.slide_pause()

        for i in range(t_max//2):
            # print(t.get_value())
            self.play(
                ball.animate.shift(bounce_factor**i * h_max * DOWN),
                t.animate.set_value(2*i + 1),
                run_time=2 * bounce_factor**i,
                rate_func=rate_functions.rush_into
            )
            # print(t.get_value())
            self.add(meklines[i])
            self.play(
                ball.animate.shift(bounce_factor**(i + 1) * h_max * UP),
                t.animate.set_value(2*i + 2),
                run_time=2 * bounce_factor**(i+1),
                rate_func=rate_functions.rush_from
            )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[Uncreate(m) for m in [ball, h_brace, ground, plane, graph_mek, graph_pot, graph_kin, *meklines]],
                *[Unwrite(m) for m in [mek_text, damp_fact, h_text]],
                lag_ratio=0.1
            ),
            run_time=2
        )

