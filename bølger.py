from manim import *
from helpers import *
import numpy as np
import math

slides = True
if slides:
    from manim_slides import Slide


class Egenskaber(Slide if slides else Scene):
    def construct(self):
        self.wavelength()
        self.amplitude()
        self.frekvens()
        self.fart()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def wavelength(self):
        scene_marker("Bølgelængde")
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        self.play(DrawBorderThenFill(plane))
        subtitle = Tex("Bølgelængde", color=RED, font_size=48).set_z_index(plane.get_z_index()+2).to_edge(DL, buff=0.1)
        subrect = get_background_rect(subtitle)
        self.play(Write(subtitle), FadeIn(subrect))
        self.slide_pause()

        # sup_title = MarkupText("Bølgelængde, \lambda", color=RED).arrange(RIGHT).to_edge(UL)
        # sup_title = VGroup(
        #     Text(r"Bølgelængde, ", color=RED, font_size=36),
        #     MathTex(r"\lambda", color=RED)
        # ).arrange(RIGHT).set_z_index(8).scale(1).to_edge(UL)
        # self.play(
        #     Write(sup_title),
        #     Create(get_background_rect(sup_title)),
        #     run_time=0.5
        # )
        # self.slide_pause()

        l_tracker = ValueTracker(4)
        amp = 4
        wave = always_redraw(lambda: plane.plot(
            lambda x: amp*np.sin(2*x*PI/l_tracker.get_value()),
            color=BLUE
        ))
        self.play(
            Create(wave),
            run_time=4,
            # rate_func=rate_functions.double_smooth
        )
        self.slide_pause()

        x0_tracker = ValueTracker(0)
        v_dots = always_redraw(lambda: VGroup(
            Dot(
                plane.c2p(x0_tracker.get_value(), wave.underlying_function(x0_tracker.get_value())),
                color=RED
            ),
            Dot(
                plane.c2p(x0_tracker.get_value() + l_tracker.get_value(),
                          wave.underlying_function(x0_tracker.get_value() + l_tracker.get_value())),
                color=RED
            )
        ))
        self.play(Create(v_dots))

        v_lines = always_redraw(lambda: VGroup(
            *[
                Line(
                    start=plane.c2p(plane.p2c(d.get_center())[0], -1.1*amp),
                    end=plane.c2p(plane.p2c(d.get_center())[0], 1.1*amp),
                    color=RED
                ).set_opacity(0.75) for d in v_dots
            ]
        ))
        self.play(
            Create(v_lines)
        )
        self.slide_pause()

        for x in [1, 3, 4.5, 6, l_tracker.get_value()/4]:
            self.play(
                x0_tracker.animate.set_value(x),
                run_time=2
            )
            xs_pause(self)
        self.slide_pause()

        length_brace = always_redraw(lambda: BraceBetweenPoints(
            point_1=plane.c2p(x0_tracker.get_value(), 1.1*amp),
            point_2=plane.c2p(x0_tracker.get_value() + l_tracker.get_value(), 1.1*amp),
            color=RED,
            direction=UP
        ))
        # length_number = always_redraw(lambda: DecimalNumber(
        #     l_tracker.get_value(),
        #     num_decimal_places=2,
        #     include_sign=False,
        #     color=RED
        # ).next_to(length_brace, UP))
        length_number = always_redraw(lambda: MathTex(
            f"{l_tracker.get_value():.2f}",
            color=RED
        ).next_to(length_brace, UP))
        self.play(
            GrowFromCenter(length_brace)
        )
        self.slide_pause()
        self.play(
            Write(length_number)
        )
        self.slide_pause()

        for x in np.random.uniform(-5, 5, 5):
            self.play(
                x0_tracker.animate.set_value(x),
                run_time=3
            )
            xs_pause(self)
        self.play(
            x0_tracker.animate.set_value(-0.5*l_tracker.get_value()),
            run_time=3
        )
        self.slide_pause()

        length_text = always_redraw(lambda:
            MathTex(
                r"\lambda=",
                f"{l_tracker.get_value():.2f}",
                color=RED
            ).next_to(length_brace, UP)
        )
        self.play(
            TransformMatchingTex(length_number, length_text, transform_mismatches=True)
        )
        self.slide_pause()

        for l in [5, 3, 2, 6, 1, 0.4, 10, 6]:
            self.play(
                l_tracker.animate.set_value(l),
                x0_tracker.animate.set_value(-0.5*l),
                run_time=4
            )
            self.slide_pause(0.1)

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [plane, wave]]
        )
        self.remove(plane, wave)

    def amplitude(self):
        scene_marker("Amplitude")
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        length = 6
        amp_tracker = ValueTracker(4)
        offset = ValueTracker(0)
        wave = always_redraw(lambda: plane.plot(
            lambda x: amp_tracker.get_value()*np.sin(2*x*PI/length) + offset.get_value(),
            color=BLUE
        ))
        self.add(plane, wave)
        subtitle = Tex("Amplitude", color=GREEN, font_size=48).set_z_index(plane.get_z_index()+2).to_edge(DL, buff=0.1)
        subrect = get_background_rect(subtitle)
        self.play(Write(subtitle), FadeIn(subrect))
        self.slide_pause()

        # sup_title = VGroup(
        #     Text(r"Amplitude, ", color=GREEN, font_size=36),
        #     MathTex(r"A", color=GREEN)
        # ).arrange(RIGHT).set_z_index(8).scale(1).to_edge(UL)
        # self.play(
        #     Write(sup_title),
        #     Create(get_background_rect(sup_title)),
        #     run_time=0.5
        # )
        # self.slide_pause()

        amp_v_lines = always_redraw(lambda: VGroup(*[
            Line(
                start=plane.c2p(n*length/4, 0),
                end=plane.c2p(n*length/4, wave.underlying_function(n*length/4)),
                color=GREEN
            ).set_opacity(0.4) for n in [1, 3]
        ]))
        amp_h_lines = always_redraw(lambda: VGroup(*[
            Line(
                start=plane.c2p(n*length/4, wave.underlying_function(n*length/4)),
                end=plane.c2p(0, wave.underlying_function(n*length/4)),
                color=GREEN
            ).set_opacity(0.4) for n in [1, 3]
        ]))
        self.play(
            LaggedStart(
                Create(amp_v_lines),
                Create(amp_h_lines),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        for amp in [1, 2, 7, amp_tracker.get_value()]:
            self.play(
                amp_tracker.animate.set_value(amp),
                run_time=2
            )
            self.slide_pause(0.1)

        amp_full = always_redraw(lambda: Line(
            start=plane.c2p(0, wave.underlying_function(3*length/4)),
            end=plane.c2p(0, wave.underlying_function(length/4)),
            color=GREEN,
            stroke_width=4
        ))
        amp_brace = always_redraw(lambda: BraceBetweenPoints(
            # point_1=plane.c2p(0, )
            point_1=amp_full.get_center(),
            point_2=amp_full.get_top(),
            color=GREEN,
            direction=LEFT
        ))
        amp_text = always_redraw(lambda: MathTex(
            f"A={amp_tracker.get_value():.1f}",
            color=GREEN
        ).next_to(amp_brace, LEFT))
        # srec = VGroup(*[get_background_rect(m) for m in [amp_brace, amp_text]])
        self.play(
            Create(amp_full)
        )
        self.slide_pause()
        self.play(
            LaggedStart(
                GrowFromCenter(amp_brace),
                # FadeIn(srec),
                Write(amp_text),
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.slide_pause()

        for amp in [1, 2, 7, amp_tracker.get_value()]:
            self.play(
                amp_tracker.animate.set_value(amp),
                run_time=2
            )
            self.slide_pause(0.1)

        for off in [1, 2, -3, 4, offset.get_value()]:
            self.play(
                offset.animate.set_value(off),
                run_time=2
            )
            self.slide_pause(0.1)

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [plane, wave]]
        )
        self.remove(plane, wave)

    def frekvens(self):
        scene_marker("Frekvens")
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        length = 6
        amp_tracker = ValueTracker(4)
        phase_tracker = ValueTracker(0)
        wave = always_redraw(lambda: plane.plot(
            lambda x: amp_tracker.get_value()*np.sin(2*x*PI/length + phase_tracker.get_value()),
            color=BLUE
        ))
        self.add(plane, wave)
        subtitle = Tex("Frekvens", color=YELLOW, font_size=48).set_z_index(plane.get_z_index()+2).to_edge(DL, buff=0.1)
        subrect = get_background_rect(subtitle)
        self.play(Write(subtitle), FadeIn(subrect))
        self.slide_pause()

        # sup_title = VGroup(
        #     Text(r"Frekvens, ", color=YELLOW, font_size=36),
        #     MathTex(r"f", color=YELLOW)
        # ).arrange(RIGHT).set_z_index(8).scale(1).to_edge(UL)
        # self.play(
        #     Write(sup_title),
        #     Create(get_background_rect(sup_title)),
        #     run_time=0.5
        # )
        # self.slide_pause()

        top_dot = always_redraw(lambda: Dot(
            plane.c2p(length/4, wave.underlying_function(length/4)),
            color=YELLOW
        ))
        self.play(Create(top_dot))
        self.slide_pause()

        if slides:
            self.start_loop()
            self.play(amp_tracker.animate.set_value(-4),
                      rate_func=rate_functions.linear,
                      run_time=2)
            self.play(amp_tracker.animate.set_value(4),
                      rate_func=rate_functions.linear,
                      run_time=2)
            self.end_loop()
        else:
            for i in range(11):
                self.play(
                    amp_tracker.animate.set_value(4 * (-1)**i),
                    run_time=1.5 if i==0 else 1,
                    rate_func=rate_functions.rush_into if i==0 else rate_functions.linear
                )
        self.slide_pause()

        if slides:
            self.start_loop()
            self.play(phase_tracker.animate.set_value(32*PI),
                      rate_func=rate_functions.linear,
                      run_time=32)
            phase_tracker.set_value(0)
            self.end_loop()
        else:
            for i, phase in zip([1, 2, 1], [16*PI, -16*PI, 0]):
                self.play(
                    phase_tracker.animate.set_value(phase),
                    run_time=16*i,
                    rate_func=rate_functions.linear
                )
                self.slide_pause(0.1)

        # self.play(
        #     *[FadeOut(m) for m in self.mobjects if m not in [plane, wave]]
        # )
        # self.remove(plane, wave)
        self.play(
            *[FadeOut(m) for m in self.mobjects]
        )

    def _fart(self):
        scene_marker("Fart")
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        length = 6
        phase_tracker = ValueTracker(0)
        wave = always_redraw(lambda: plane.plot(
            lambda x: 4*np.sin(2*x*PI/length + phase_tracker.get_value()),
            color=BLUE
        ))
        self.add(plane, wave)
        self.slide_pause()

        top_dot = always_redraw(lambda: Dot(
            plane.c2p(length/4, wave.underlying_function(length/4)),
            color=YELLOW
        ))
        self.play(Create(top_dot))
        self.slide_pause()

        v_text = VGroup(
            Tex("Fart: "),
            DecimalNumber(0, num_decimal_places=1, include_sign=False, color=BLUE)
        ).arrange(RIGHT).to_edge(UL)
        self.play(FadeIn(v_text), run_time=0.5)
        self.slide_pause()

        tid = 10
        for v in [2, 4, 6, 0.5]:
            self.play(v_text[1].animate.set_value(v), run_time=0.5)
            self.play(
                phase_tracker.animate.set_value(tid*v),#*2*PI),
                rate_func=rate_functions.linear,
                run_time=tid
            )
            xs_pause(self)
            self.play(
                phase_tracker.animate.set_value(0),
                run_time=1
            )
            self.slide_pause()
        # self.slide_pause()

    def fart(self):
        wave_type = "dots"
        scene_marker("Fart")
        colors = [RED, BLUE, PURPLE, GREEN]
        plane = NumberPlane(
            x_range=[-6.5, 6.5, 1],
            y_range=[-3.25, 3.25, 1],
            x_length=6.5,
            y_length=3.25,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        )
        planes = VGroup(*[
            plane.copy().to_edge(edge) for edge in [UL, UR, DL, DR]
        ])
        srecs = VGroup(*[
            SurroundingRectangle(
                plane, buff=0, color=color, stroke_width=0.75
            ) for plane, color in zip(planes, colors)
        ])
        length = 3
        phase_trackers = [ValueTracker(0) for _ in planes]
        waves = always_redraw(lambda: VGroup(*[
            plane.plot(
                lambda x: 2*np.sin(2*x*PI/length + phase_tracker.get_value()),
                color=color, stroke_width=0.25 if wave_type == "dots" else 1
            ) for plane, phase_tracker, color in zip(planes, phase_trackers, colors)
        ]))
        self.play(
            LaggedStart(
                FadeIn(srecs),
                DrawBorderThenFill(planes),
                DrawBorderThenFill(waves),
                lag_ratio=0.33
            ),
            run_time=3
        )
        self.slide_pause()

        if wave_type == "dots":
            wave_dots = always_redraw(lambda: VGroup(*[
                VGroup(*[
                    Dot(
                        plane.c2p(x, 2*np.sin(x*2*PI/length + phase_tracker.get_value())),
                        color=color, radius=0.04
                    ) for x in np.linspace(-6.5, 6.5, 61)
                ]) for plane, phase_tracker, color in zip(planes, phase_trackers, colors)
            ]))
        dots = always_redraw(lambda: VGroup(*[
            Dot(
                # plane.c2p(length/4, wave.underlying_function(length/4)), color=YELLOW
                plane.c2p(
                    length/4,
                    2*np.sin(PI/2 + phase_tracker.get_value())
                ),
                color=YELLOW
            # ) for plane, wave in zip(planes, waves)
            ) for plane, phase_tracker in zip(planes, phase_trackers)
        ]))
        self.play(Create(wave_dots))
        self.play(DrawBorderThenFill(dots))
        self.add(dots)
        self.slide_pause()

        v_texts = VGroup(
            *[
                VGroup(
                    Tex("Fart: "),
                    DecimalNumber(0, color=srec.get_color())
                ).scale(0.75).arrange(RIGHT).next_to(
                    srec, direc, buff=-0.3
                ) for srec, direc in zip(srecs, [DOWN, DOWN, UP, UP])
            ]
        )
        self.play(
            Write(v_texts)
        )
        self.slide_pause()

        vs = [0.5, 2, 4, 10]
        self.play(
            *[v_text[1].animate.set_value(v) for v_text, v in zip(v_texts, vs)],
            run_time=1
        )
        self.slide_pause()
        if slides:
            self.start_loop()
            self.play(
                *[phase_tracker.animate.set_value(4*PI*v) for phase_tracker, v in zip(phase_trackers, vs)],
                rate_func=rate_functions.linear,
                run_time=4*PI
            )
            self.end_loop()
        else:
            tid = 30
            self.play(
                *[phase_tracker.animate.set_value(tid*v) for phase_tracker, v in zip(phase_trackers, vs)],
                rate_func=rate_functions.linear,
                run_time=tid
            )
            self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects]
        )

        # tid = 10
        # for v in [2, 4, 6, 0.5]:
        #     self.play(v_text[1].animate.set_value(v), run_time=0.5)
        #     self.play(
        #         phase_tracker.animate.set_value(tid*v),#*2*PI),
        #         rate_func=rate_functions.linear,
        #         run_time=tid
        #     )
        #     xs_pause(self)
        #     self.play(
        #         phase_tracker.animate.set_value(0),
        #         run_time=1
        #     )
        #     self.slide_pause()
        # # self.slide_pause()


class _Interferens(Slide if slides else Scene):
    def construct(self):
        self.konstr_destr()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def konstr_destr(self):
        plane = NumberPlane(
            x_range=[-16, 16, 1],
            y_range=[-9, 9, 1],
            x_length=16,
            y_length=9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        self.play(DrawBorderThenFill(plane))
        self.slide_pause()

        ampA, ampB = ValueTracker(4), ValueTracker(4)
        phaA, phaB = ValueTracker(0), ValueTracker(0)
        lowA, higA = ValueTracker(-20), ValueTracker(0)
        lowB, higB = ValueTracker(0), ValueTracker(20)
        length = 4
        waveA = always_redraw(lambda:
            plane.plot(
                lambda x: ampA.get_value() * np.sin(2*x*PI/length + phaA.get_value()),
                x_range=[lowA.get_value(), higA.get_value()],
                color=RED
            )
        )
        waveB = always_redraw(lambda:
            plane.plot(
                lambda x: ampB.get_value() * np.sin(2*x*PI/length + phaB.get_value()),
                x_range=[lowB.get_value(), higB.get_value()],
                color=BLUE
            )
        )
        self.play(
            Create(waveA),
            Create(waveB),
            run_time=1
        )
        self.slide_pause()

        # self.play(
        #     ampA.animate.set_value(4),
        #     ampB.animate.set_value(2),
        #     run_time=2
        # )
        # self.slide_pause()


class Interferens(Slide if slides else Scene):
    def construct(self):
        self.konstr_destr()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def konstr_destr(self):
        planes = VGroup(*[
            NumberPlane(
                x_range=[-12, 12, 1],
                y_range=[-2.5, 2.5, 1],
                x_length=12,
                y_length=2.5,
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            ).scale(0.75) for _ in range(3)
        ]).arrange(DOWN).to_edge(RIGHT)

        phase_trackers = [ValueTracker(0.0) for _ in range(3)]
        amp_trackers = [ValueTracker(1.0) for _ in range(3)]
        # opa_trackers = {wave: [ValueTracker(1.0) for _ in range(3)] for wave in ["A", "B", "C"]}
        opA_trackers = [ValueTracker(1.0) for _ in range(3)]
        opB_trackers = [ValueTracker(1.0) for _ in range(3)]
        opC_trackers = [ValueTracker(1.0) for _ in range(3)]
        colors = [BLUE, YELLOW, GREEN]
        brects = VGroup(
            *[
                get_background_rect(
                    plane, stroke_colour=color, buff=0, stroke_width=4
                ) for plane, color in zip(planes, colors)
            ]
        )

        waves_A = always_redraw(lambda: VGroup(*[
            plane.plot(
                lambda x: amp_trackers[0].get_value() * np.cos(x + phase_trackers[0].get_value()),
                color=colors[0],
                stroke_opacity=opa_tracker.get_value()
            # ) for plane, opa_tracker in zip(planes, opa_trackers["A"])
            ) for plane, opa_tracker in zip(planes, opA_trackers)
        ]))
        waves_B = always_redraw(lambda: VGroup(*[
            plane.plot(
                lambda x: amp_trackers[1].get_value() * np.cos(x + phase_trackers[1].get_value()),
                color=colors[1],
                stroke_opacity=opa_tracker.get_value()
            # ) for plane, opa_tracker in zip(planes, opa_trackers["B"])
            ) for plane, opa_tracker in zip(planes, opB_trackers)
        ]))
        waves_C = always_redraw(lambda: VGroup(*[
            plane.plot(
                lambda x: amp_trackers[2].get_value() * np.cos(x + phase_trackers[2].get_value()),
                color=colors[2],
                stroke_opacity=opa_tracker.get_value()
            # ) for plane, opa_tracker in zip(planes, opa_trackers["C"])
            ) for plane, opa_tracker in zip(planes, opC_trackers)
        ]))

        # self.add(planes, waves_A, waves_C, waves_B, brects)
        self.play(
            *[
                LaggedStart(
                    DrawBorderThenFill(plane),
                    Create(brect),
                    lag_ratio=0.5
                ) for plane, brect in zip(planes, brects)
            ]
            # LaggedStart(*[
            #     LaggedStart(
            #         DrawBorderThenFill(plane),
            #         FadeIn(brect),
            #         lag_ratio=0.1
            #     ) for plane, brect in zip(planes, brects)],
            #     lag_ratio=0.3
            # )
        )
        self.slide_pause()
        self.play(
            *[Create(wave) for wave in waves_A]
        )
        self.play(
            phase_trackers[0].animate.set_value(-PI/2)
        )
        print(*[tracker.get_value() for tracker in opA_trackers])
        self.play(
            *[tracker.animate.set_value(0.25) for tracker in opA_trackers[:]]
        )
        print(*[tracker.get_value() for tracker in opA_trackers])
        self.slide_pause()
        #
        # waveA = always_redraw(lambda:
        #     plane.plot(
        #         lambda x: np.cos(x),
        #         color=BLUE,
        #         stroke_opacity=oA_tracker.get_value()
        #     )
        # )
        # waveB = always_redraw(lambda:
        #     plane.plot(
        #         lambda x: amp_tracker.get_value() * np.cos(x + phase_tracker.get_value()),
        #         color=YELLOW,
        #         stroke_opacity=oB_tracker.get_value()
        #     )
        # )
        # eqA = always_redraw(lambda: MathTex(r"f(x)").set_color(waveA.get_color()).move_to(plane.c2p(-8, 4)))
        # eqB = always_redraw(lambda: MathTex(r"g(x)").set_color(waveB.get_color()).move_to(plane.c2p(8, 4)))
        # self.play(
        #     LaggedStart(
        #         LaggedStart(
        #             Create(waveA, run_time=2),
        #             Write(eqA),
        #             lag_ratio=0.5
        #         ),
        #         LaggedStart(
        #             Create(waveB, run_time=2),
        #             Write(eqB),
        #             lag_ratio=0.5
        #         ),
        #         lag_ratio=1
        #     )
        # )
        # self.play(
        #     phase_tracker.animate.set_value(-1.0)
        # )
        # self.slide_pause()
        #
        # waveAB = always_redraw(lambda:
        #     plane.plot(
        #         lambda x: np.cos(x) + amp_tracker.get_value() * np.cos(x + phase_tracker.get_value()),
        #         color=GREEN,
        #         stroke_opacity=oAB_tracker.get_value()
        #     )
        # )
        # self.play(
        #     oA_tracker.animate.set_value(0.25),
        #     oB_tracker.animate.set_value(0.25),
        #     Create(waveAB, run_time=2)
        # )
        # self.slide_pause()
        #
        # for amp in [2, 4, 1]:
        #     for phi in [-20, 20, -1]:
        #         self.play(
        #             phase_tracker.animate.set_value(phi),
        #             run_time=20
        #         )
        #     self.play(
        #         amp_tracker.animate.set_value(amp)
        #     )
# TODO: et grafvindue pr bølge og en for den samlede? Evt. med fadede udgaver af hinanden i deres koordinatsystem




class Doppler(Slide if slides else MovingCameraScene):
    def construct(self):
        self.lydkilde()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def lydkilde(self):
        ambulance = SVGMobject("SVGs/ambulance.svg")
        self.play(
            DrawBorderThenFill(ambulance),
            run_time=2
        )
        self.slide_pause()

        time = ValueTracker(0)
        sound_radius1 = ValueTracker(0.0)
        sound_radius2 = ValueTracker(0.0)
        sound_radius3 = ValueTracker(0.0)
        sound_radius4 = ValueTracker(0.0)
        sound_radius5 = ValueTracker(0.0)
        sradii = [ValueTracker(0.0) for _ in range(5)]
        swave = always_redraw(lambda:
            # Circle(
            #     radius=sound_radius.get_value(),
            #     color=BLUE_C,
            #     stroke_width=10/(0.1*sound_radius.get_value() + 1)**2 if sound_radius.get_value() < 5 else 0
            # ).move_to(ambulance.get_center())
            VGroup(*[
                Circle(
                    radius=sr.get_value(),
                    color=BLUE_C,
                    # stroke_width=10/(0.1*sr.get_value() + 1)**2 if sr.get_value() < 5 else 0
                    stroke_width=5
                ).move_to(
                    ambulance.get_center() if sr.get_value() < 0.1 else [0.4*i, 0, 0]
                ) for i, sr in enumerate(sradii)
            ])
        )
        # for i in range(5):
        #     self.add(swave)
        #     self.play(
        #         sound_radius.animate.set_value(5.0),
        #         rate_func=rate_functions.linear,
        #         run_time=4
        #     )
        #     sound_radius.set_value(0.0)
        #     self.remove(swave)
        self.add(swave)
        self.play(
            LaggedStart(
                *[sr.animate.set_value(5.0) for sr in sradii],
                lag_ratio=0.2
            ),
            rate_func=rate_functions.linear,
            run_time=5
        )
        self.remove(swave)

        self.slide_pause()

        [sr.set_value(0.0) for sr in sradii]
        self.add(swave)
        self.play(
            AnimationGroup(
                LaggedStart(
                    *[sr.animate.set_value(5.0) for sr in sradii],
                    lag_ratio=0.2
                ),
                ambulance.animate.shift(2*RIGHT)
            ),
            rate_func=rate_functions.linear,
            run_time=5
        )
        self.remove(swave)

