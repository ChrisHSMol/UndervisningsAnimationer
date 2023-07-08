from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np

slides = True
if slides:
    from manim_slides import Slide


class GitterLigning(MovingCameraScene if not slides else MovingCameraScene, Slide):
    def construct(self):
        self.slide_pause()
        self.udstyr()
        self.gitter_ligning()
        self.hvidt_lys()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def udstyr(self):
        laser_gun = SVGMobject("SVGs/laser_gun.svg").to_edge(LEFT).shift(0.25*DOWN)
        laser_gun.set_color(invert_color(laser_gun.get_color()))
        laser_name = Tex("Laser").set_color(color_gradient([BLUE, GREEN, RED], 3)).next_to(laser_gun, UP)
        self.play(
            LaggedStart(
                DrawBorderThenFill(laser_gun),
                Write(laser_name),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        linjer = ValueTracker(10)
        dist_lg = ValueTracker(2)
        gitter_top = Line(
            1*DOWN, 1*UP, color=PINK
        ).next_to(laser_gun, RIGHT, buff=0).shift(0.25*UP + dist_lg.get_value()*RIGHT)
        gitter_ridser = always_redraw(lambda:
            VGroup(
                Square(5, color=gitter_top.get_color()),
                *[
                    Line(
                        start=[i, -2.5, 0],
                        end=[i, 2.5, 0],
                        stroke_width=0.5
                    # ) for i in np.linspace(-2.5, 2.5, int(linjer.get_value()/10))
                    ) for i in np.linspace(-2.5, 2.5, int(linjer.get_value()))
                ]
            ).next_to(gitter_top, RIGHT)
        )
        gitter_name = always_redraw(lambda:
            Tex(
                f"Gitter med {int(linjer.get_value())} ridser pr. mm",
                color=gitter_top.get_color()
            ).next_to(VGroup(gitter_ridser, gitter_top), UP)
        )
        gitter_name2 = always_redraw(lambda:
            # Tex(f"Gitter, d=1/{int(linjer.get_value())}", color=gitter_top.get_color()).next_to(
            #     gitter_top, UP)
            Tex(
                f"{int(linjer.get_value())} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UL)
        )
        self.play(
            LaggedStart(
                # Create(gitter_top),
                Create(gitter_ridser),
                Write(gitter_name),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()
        self.play(
            linjer.animate.set_value(200),
            run_time=5
        )
        self.slide_pause()

        self.play(
            Transform(gitter_ridser, gitter_top),
            Transform(gitter_name, gitter_name2)
        )
        self.remove(gitter_name, gitter_ridser)
        self.add(gitter_top, gitter_name2)

        dist_gw = ValueTracker(5)
        # wall = Line(5*DOWN, 5*UP).to_edge(RIGHT)
        wall = Line(5*DOWN, 5*UP).shift(dist_gw.get_value() * RIGHT)
        wall_tekst = Tex("Væg").next_to(wall, RIGHT).shift(3.5*UP)
        self.play(
            Create(wall),
            Create(wall_tekst),
        )
        self.slide_pause()
        self.remove(*[m for m in self.mobjects])

    def _gitter_ligning(self):
        linjer = ValueTracker(200)  # mm^-1
        wlength = ValueTracker(400)  # nm
        dist_lg = ValueTracker(2)  # m
        dist_gw = ValueTracker(5)  # m

        laser_gun = SVGMobject("SVGs/laser_gun.svg").to_edge(LEFT).shift(0.25*DOWN)
        laser_gun.set_color(invert_color(laser_gun.get_color()))
        laser_name = Tex("Laser").set_color(color_gradient([BLUE, GREEN, RED], 3)).next_to(laser_gun, UP)
        gitter_top = always_redraw(lambda:
            Line(
                DOWN, UP, color=PINK
            ).next_to(laser_gun, RIGHT, buff=0).shift(0.25*UP + dist_lg.get_value()*RIGHT)
        )
        gitter_name = always_redraw(lambda:
            Tex(
                f"{int(linjer.get_value())} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UP)
        )
        wall = Line(5*DOWN, 5*UP).shift(dist_gw.get_value() * RIGHT)
        wall_name = Tex("Væg").next_to(wall, RIGHT).shift(3.5 * UP)
        self.add(laser_gun, laser_name, wall, wall_name, gitter_top, gitter_name)

        colordots = VGroup()
        colorlines = VGroup()
        for wavelength, color in zip([400, 550, 700], [BLUE, GREEN, RED]):
            wlength.set_value(wavelength)
            laser_line = always_redraw(lambda:
                Line(
                    start=laser_gun.get_right() + 0.25*UP,
                    end=gitter_top.get_left(),
                    stroke_width=2,
                    color=color
                )
            )
            laser_lambda = always_redraw(lambda:
                Tex(
                    f"$\\lambda={wlength.get_value():.0f}$ nm", color=laser_line.get_color()
                ).scale(0.75).next_to(laser_line, DOWN)
            )
            diff_lines = always_redraw(lambda:
                VGroup(
                    *[
                        Line(
                            start=gitter_top.get_right(),
                            end=wall.get_left() + dist_gw.get_value() * np.tan(
                                np.arcsin(
                                    n * wlength.get_value()*10**(-9) * linjer.get_value()*10**3
                                )
                            ) * UP,
                            stroke_width=2*np.exp(-0.25*np.abs(n)),
                            color=laser_line.get_color()
                        ) for n in np.arange(-3, 3.1, 1)
                    ]
                )
            )
            self.play(
                Create(laser_line),
                Write(laser_lambda),
                rate_func=rate_functions.linear,
                run_time=dist_lg.get_value()
            )
            self.play(
                *[Create(dline) for dline in diff_lines],
                rate_func=rate_functions.linear,
                run_time=dist_gw.get_value()
            )
            self.slide_pause()
            dots = VGroup(
                *[
                    Dot(
                        dline.get_end(),
                        color=laser_line.get_color()
                    ) for dline in diff_lines
                ]
            )
            colordots.add(dots)
            colorlines.add(VGroup(laser_line, diff_lines))
            self.play(
                Create(dots)
            )
            self.slide_pause()
            self.play(
                FadeOut(laser_lambda, laser_line, diff_lines),
                dots.animate.set_opacity(0.25),
                run_time=0.5
            )

        for dots, lines in zip(colordots, colorlines):
            self.play(
                dots.animate.set_opacity(1),
                # lines.animate.set_opacity(1),
                run_time=0.5
            )
            self.slide_pause()
            self.play(
                dots.animate.set_opacity(0.25),
                # lines.animate.set_opacity(0.25),
                run_time=0.25
            )
        # self.play(
        #     # linjer.animate.set_value(600),
        #     wlength.animate.set_value(700),
        #     run_time=1
        # )

    def gitter_ligning(self):
        linjer = ValueTracker(200)  # mm^-1
        dist_lg = ValueTracker(2)  # m
        dist_gw = ValueTracker(5)  # m
        laser_thickness = 4

        laser_gun = SVGMobject("SVGs/laser_gun.svg").to_edge(LEFT).shift(0.25*DOWN)
        laser_gun.set_color(invert_color(laser_gun.get_color()))
        laser_name = Tex("Laser").set_color(color_gradient([BLUE, GREEN, RED], 3)).next_to(laser_gun, UP)
        gitter_top = always_redraw(lambda:
            Line(
                DOWN, UP, color=PINK
            ).next_to(laser_gun, RIGHT, buff=0).shift(0.25*UP + dist_lg.get_value()*RIGHT)
        )
        gitter_name = always_redraw(lambda:
            Tex(
                f"{int(linjer.get_value())} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UL)
        )
        wall = Line(5*DOWN, 5*UP).shift(dist_gw.get_value() * RIGHT)
        wall_name = Tex("Væg").next_to(wall, RIGHT).shift(3.5 * UP)
        self.add(laser_gun, laser_name, wall, wall_name, gitter_top, gitter_name)

        ligning = MathTex(
            r"\sin(\theta_n)", "=", r"{n \cdot \lambda \over d}"
        ).to_edge(UL)
        ligning[0][5].set_color(YELLOW)
        ligning[2][0].set_color(YELLOW)
        ligning[2][2].set_color(color_gradient([BLUE, GREEN, RED], 3))
        ligning[2][-1].set_color(LIGHT_PINK)
        konstant = MathTex("; ", "d", "=", r"{1\over", "ridser}").set_color_by_tex_to_color_map(
            {"d": LIGHT_PINK, "ridser": gitter_top.get_color()}
        ).next_to(ligning, RIGHT, buff=1)
        self.play(
            Write(ligning),
            Write(konstant),
            run_time=2
        )

        wavelengths = [400, 532, 680]
        colors = [BLUE, GREEN, RED]
        wc = {str(w): c for w, c in zip(wavelengths, colors)}
        lines = [200, 400, 600]
        for i, linjer in enumerate(lines):
            linjer = ValueTracker(linjer)
            gitter_name = Tex(
                f"{linjer.get_value():.0f} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UL)
            if i > 0:
                self.play(
                    Write(gitter_name),
                    run_time=0.5
                )

            laser_lines = VGroup(
                *[
                    Line(
                        start=laser_gun.get_right() + 0.25*UP,
                        end=gitter_top.get_left(),
                        stroke_width=laser_thickness,
                        color=color
                    ) for color in colors
                ]
            )
            laser_lambdas = VGroup(
                *[
                    Tex(
                        f"$\\lambda={wavelength:.0f}$ nm", color=line.get_color()
                    ).scale(0.6).next_to(line, DOWN) for wavelength, line in zip(wavelengths, laser_lines)
                ]
            )
            difflines = VGroup(
                *[
                    VGroup(
                        *[
                            Line(
                                start=gitter_top.get_right(),
                                end=wall.get_left() + dist_gw.get_value() * np.tan(
                                    np.arcsin(
                                        n * wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3
                                    )
                                ) * UP,
                                stroke_width=laser_thickness * np.exp(
                                    -3 * np.abs(np.arcsin(n * wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3))
                                ),
                                color=wc[str(wavelength)]
                            ) for n in np.arange(
                                -np.floor(1/(wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3)),
                                np.floor(1/(wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3)) + 0.1,
                                1
                            )
                        ]
                    ) for line, wavelength in zip(laser_lines, wavelengths)
                ]
            )

            for laser, diffs, text in zip(laser_lines, difflines, laser_lambdas):
                self.play(
                    *[Create(l) for l in laser],
                    Write(text, run_time=0.5),
                    rate_func=rate_functions.linear,
                    run_time=dist_lg.get_value()/(i+1)
                )
                self.play(
                    *[AnimationGroup(
                        *[
                            Create(
                                d,
                                rate_func=rate_functions.linear,
                                run_time=dist_gw.get_value()/(i+1)
                            ) for d in dline
                        ]
                    ) for dline in diffs],
                )
                self.slide_pause()
                self.play(
                    *[FadeOut(m) for m in [laser, diffs, text]],
                    run_time=0.25
                )

            # self.slide_pause()
            for laser, diffs in zip(laser_lines, difflines):
                self.play(
                    *[FadeIn(m) for m in [laser, diffs]],
                    run_time=0.5
                )
                self.play(
                    *[FadeOut(m) for m in [laser, diffs]],
                    run_time=0.5
                )

            if i < len(lines) - 1:
                self.play(FadeOut(gitter_name), run_time=0.25)
            self.remove(
                *[m for m in self.mobjects if m not in [
                    laser_gun, laser_name, gitter_top, wall, wall_name, ligning, konstant, gitter_name
                ]]
            )

        self.slide_pause()
        self.play(
            *[FadeOut(m, run_time=0.25) for m in self.mobjects if m not in [ligning]],
            ligning.animate.scale(3).move_to(ORIGIN).shift(2*UP),
            run_time=2
        )
        forklaring = VGroup(
            VGroup(
                MathTex(r"\lambda", font_size=48).set_color(color_gradient([BLUE, GREEN, RED], 3)),
                Tex(": Bølgelængde af laserens lys", font_size=30)
            ).arrange(RIGHT),
            VGroup(
                MathTex("d", font_size=48, color=LIGHT_PINK),
                Tex(": Gitterkonstanten. Afstanden mellem to ridser", font_size=30)
            ).arrange(RIGHT),
            VGroup(
                MathTex("n", color=YELLOW, font_size=48),
                Tex(": Den n.'te ordens prik", font_size=30)
            ).arrange(RIGHT),
            VGroup(
                MathTex(r"\theta", "_n", font_size=48).set_color_by_tex_to_color_map({"n": YELLOW}),
                Tex(": Vinklen mellem 0. ordens prik og n.'te ordens prik", font_size=30)
            ).arrange(RIGHT, aligned_edge=UP)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(ligning, DOWN, aligned_edge=LEFT)

        self.play(
            Write(forklaring)
        )
        self.slide_pause()
        fade_out_all(self)

    def hvidt_lys(self):
        linjer = ValueTracker(600)  # mm^-1
        dist_lg = ValueTracker(2)  # m
        dist_gw = ValueTracker(5)  # m
        laser_thickness = 4
        # colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        # wavelengths = [700, 605, 580, 532, 472, 400]
        wavelengths = np.linspace(400, 650, 26)
        colors = [
            "#8300b5", "#7e00db", "#6a00ff", "#3800ff", "#000bff", "#004cff", "#007fff",  # 400nm - 460nm
            "#00aeff", "#00daff", "#00fff5", "#00ff87", "#09ff00", "#3aff00", "#5aff00",  # 470nm - 530nm
            "#81ff00", "#a3ff00", "#c3ff00", "#e1ff00", "#ffff00", "#ffdf00", "#ffbe00",  # 540nm - 600nm
            "#ff9b00", "#ff7700", "#ff4b00", "#ff1b00", "#ff0000"  # 610nm - 650nm
        ]

        lamp = SVGMobject("SVGs/lamp.svg").to_edge(LEFT).shift(0.5*DOWN)
        lamp.set_color(invert_color(lamp.get_color()))
        lamp_name = Tex("Lampe").set_color(color_gradient(colors, 5)).next_to(lamp, UP)
        gitter_top = always_redraw(lambda:
            Line(
                DOWN, UP, color=PINK
            ).next_to(lamp, RIGHT, buff=0).shift(0.5*UP + dist_lg.get_value()*RIGHT).set_z_index(10)
        )
        normal = Line(start=gitter_top.get_center(), end=gitter_top.get_center() + 2*LEFT)
        n2 = Line(start=2*LEFT, end=2*RIGHT).shift(2*LEFT)
        gitter_name = always_redraw(lambda:
            Tex(
                f"{int(linjer.get_value())} ridser",
                color=gitter_top.get_color()
            ).next_to(gitter_top, UL)
        )
        wall = Line(5*DOWN, 5*UP).shift(dist_gw.get_value() * RIGHT).set_z_index(10)
        wall_name = Tex("Væg").next_to(wall, RIGHT).shift(3.5 * UP)
        self.play(
            *[FadeIn(m) for m in [lamp, lamp_name, wall, wall_name, gitter_top, gitter_name]],
            run_time=0.25
        )

        lights = VGroup(
            *[
                Line(
                    start=lamp.get_right() + 0.5*UP,
                    end=gitter_top.get_left(),
                    stroke_width=laser_thickness,
                    # color=c,
                    # stroke_opacity=1/len(colors),
                    stroke_opacity=0.25
                ) for c in colors
            ]
        )
        wc = {str(w): c for w, c in zip(wavelengths, colors)}
        difflines = VGroup(
            *[
                VGroup(
                    *[
                        Line(
                            start=gitter_top.get_right(),
                            end=wall.get_left() + dist_gw.get_value() * np.tan(
                                np.arcsin(
                                    n * wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3
                                )
                            ) * UP,
                            stroke_width=laser_thickness * np.exp(
                                # -3 * np.abs(np.arcsin(n * wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3))
                                -1 * np.abs(np.arcsin(n * wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3))
                            ),
                            # stroke_opacity=1/len(colors),
                            stroke_opacity=0.25,
                            color=wc[str(wavelength)]
                        ) for n in np.arange(
                            -np.floor(1/(wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3)),
                            np.floor(1/(wavelength * 10 ** (-9) * linjer.get_value() * 10 ** 3)) + 0.1,
                            1
                        )
                    ]
                ) for line, wavelength in zip(lights, wavelengths)
            ]
        )

        self.play(
            *[Create(light, rate_func=rate_functions.linear) for light in lights]
        )
        self.play(
            *[AnimationGroup(
                *[
                    Create(
                        d,
                        rate_func=rate_functions.linear,
                        run_time=dist_gw.get_value()
                    ) for d in dline
                ]
            ) for dline in difflines],
        )
        self.slide_pause()

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                height=0.75*gitter_top.height
            )
            .move_to(
                gitter_top
            ),
            run_time=2
        )
        self.play(
            self.camera.frame.animate.move_to(
                wall.get_left() + 1.75*UP + 0.25*LEFT
            ),
            run_time=5
        )
        self.play(
            Restore(self.camera.frame),
            run_time=5
        )
        fade_out_all(self)
