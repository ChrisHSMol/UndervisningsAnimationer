from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class LogRegler(MovingCameraScene, Slide if slides else None):
    def construct(self):
        defs = self.definitioner(banimationer=False)
        # self.regneregel_1(defs)
        # self.regneregel_2(defs)
        self.regneregel_3(defs)
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def definitioner(self, banimationer=True):
        cmap = {
            "x": BLUE_C,
            "n": YELLOW,
            "m": YELLOW_A,
        }
        log_defs = VGroup(
            MathTex(r"\log(10^x) = x", substrings_to_isolate="x").set_color_by_tex_to_color_map(cmap),
            MathTex(r"10^{\log(x)} = x", substrings_to_isolate="x").set_color_by_tex_to_color_map(cmap)
        ).scale(2).arrange(DOWN, aligned_edge=RIGHT).set_z_index(3)

        pow_rules = VGroup(
            MathTex(
                r"a^n \cdot a^m = a^{n + m}", substrings_to_isolate=["n", "m"]
            ).set_color_by_tex_to_color_map(cmap),
            VGroup(
                MathTex(
                    "a^n", r"\over", "a^m", substrings_to_isolate=["n", "m"]
                ).set_color_by_tex_to_color_map(cmap),
                MathTex(
                    "=", "a^{n - m}", substrings_to_isolate=["n", "m"]
                ).set_color_by_tex_to_color_map(cmap)
            ).arrange(RIGHT),
            MathTex(
                r"\left(a^n\right)^m = a^{n \cdot m}", substrings_to_isolate=["n", "m"]
            ).set_color_by_tex_to_color_map(cmap)
        ).scale(2).arrange(DOWN, aligned_edge=RIGHT).set_z_index(3)

        if banimationer:
            self.play(
                LaggedStart(
                    *[Write(d) for d in log_defs],
                    lag_ratio=1
                ),
                run_time=4
            )
            self.slide_pause()

            self.play(
                LaggedStart(
                    log_defs.animate.scale(0.5).to_edge(UL),
                    *[Write(p) for p in pow_rules],
                    lag_ratio=1
                ),
                run_time=6
            )
            self.slide_pause()

            self.play(
                pow_rules.animate.scale(0.5).to_edge(DL)
            )

            recs = VGroup(
                get_background_rect(log_defs, stroke_colour=cmap["x"]),
                get_background_rect(pow_rules, stroke_colour=color_gradient([cmap["n"], cmap["m"]], 3))
            )
            self.play(
                Create(recs, lag_ratio=0)
                # DrawBorderThenFill(recs)
            )

            def_titles = VGroup(
                Tex(r"Logaritmens\\definition", color=cmap["x"]).next_to(log_defs, DOWN, buff=0.0),
                Tex("Potensregneregler", color=cmap["n"]).next_to(pow_rules, UP, buff=0.0),
            ).scale(0.75)
            self.play(
                Write(def_titles)
            )
            self.slide_pause()

        else:
            log_defs.scale(0.5).to_edge(UL)
            pow_rules.scale(0.5).to_edge(DL)
            recs = VGroup(
                get_background_rect(log_defs, stroke_colour=cmap["x"]),
                get_background_rect(pow_rules, stroke_colour=color_gradient([cmap["n"], cmap["m"]], 3))
            )
            def_titles = VGroup(
                Tex(r"Logaritmens\\definition", color=cmap["x"]).next_to(log_defs, DOWN, buff=0.0),
                Tex("Potensregneregler", color=cmap["n"]).next_to(pow_rules, UP, buff=0.0),
            ).scale(0.75)
            self.add(log_defs, pow_rules, recs, def_titles)
        return log_defs, pow_rules, recs, def_titles, cmap

    def regneregel_1(self, defs):
        log_defs, pow_rules, recs, def_titles, cmap = defs
        cmap["a"] = RED
        cmap["b"] = RED_A
        regneregel = MathTex(
            r"\log(a\cdotb) = \log(a) + \log(b)", substrings_to_isolate=["a", "b"]
        ).set_color_by_tex_to_color_map(cmap).set_z_index(3)
        srec = get_background_rect(regneregel, stroke_colour=color_gradient([cmap["a"], cmap["b"]], 3))
        self.play(
            LaggedStart(
                Write(regneregel, run_time=4),
                Create(srec, run_time=1),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        self.play(
            VGroup(regneregel, srec).animate.to_edge(UR)
        )
        self.remove(regneregel, srec)
        self.add(regneregel, srec)

        og_term = MathTex(r"\log(a\cdotb)", substrings_to_isolate=["a", "b"]).set_color_by_tex_to_color_map(cmap)

        steps = VGroup(
            MathTex(
                r"=", r"\log\left( 10^{\log(a)}", r"\cdot", r"10^{\log(b)}", r"\right)", substrings_to_isolate=["a", "b"]
            ).set_color_by_tex_to_color_map(cmap),
            MathTex(
                r"=", r"\log\left( 10^{\log(a) + \log(b)}", r"\right)", substrings_to_isolate=["a", "b"]
            ).set_color_by_tex_to_color_map(cmap),
            MathTex(
                r"=", r"{\log(a) + \log(b)}", substrings_to_isolate=["a", "b"]
            ).set_color_by_tex_to_color_map(cmap),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        og_term.next_to(steps[0], LEFT)

        self.play(
            Write(og_term),
            run_time=1
        )
        self.slide_pause()

        self.play(
            Indicate(log_defs[1])
        )
        self.play(
            Write(steps[0]),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Indicate(pow_rules[0])
        )
        self.play(
            og_term.copy().animate.set_opacity(0.33),
            steps[0].animate.set_opacity(0.33),
            og_term.animate.next_to(steps[1], LEFT),
            TransformMatchingTex(
                steps[0].copy(), steps[1], transform_mismatches=True
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Indicate(log_defs[0])
        )
        self.play(
            og_term.copy().animate.set_opacity(0.33),
            steps[1].animate.set_opacity(0.33),
            og_term.animate.next_to(steps[2], LEFT),
            TransformMatchingTex(
                steps[1].copy(), steps[2], transform_mismatches=True
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [
                log_defs, pow_rules, recs, def_titles, regneregel, srec
            ]],
            VGroup(regneregel, srec).animate.move_to(ORIGIN),
            run_time=2
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                Uncreate(srec, lag_ratio=0, run_time=1),
                Unwrite(regneregel, run_time=1),
                lag_ratio=0.5
            ),
        )

    def regneregel_2(self, defs):
        log_defs, pow_rules, recs, def_titles, cmap = defs
        cmap["a"] = RED
        cmap["b"] = RED_A
        regneregel = MathTex(
            r"\log\left({a \over b}\right) = \log(a) - \log(b)", substrings_to_isolate=["a", "b"]
        ).set_color_by_tex_to_color_map(cmap).set_z_index(3)
        srec = get_background_rect(regneregel, stroke_colour=color_gradient([cmap["a"], cmap["b"]], 3))
        self.play(
            LaggedStart(
                Write(regneregel, run_time=4),
                Create(srec, run_time=1),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        self.play(
            VGroup(regneregel, srec).animate.to_edge(UR)
        )
        self.remove(regneregel, srec)
        self.add(regneregel, srec)

        og_term = MathTex(r"\log(a\cdotb)", substrings_to_isolate=["a", "b"]).set_color_by_tex_to_color_map(cmap)

        steps = VGroup(
            MathTex(
                r"=", r"\log\left(", r"{10^{\log(a)}", r"\over", r"10^{\log(b)}}", r"\right)",
                substrings_to_isolate=["a", "b"]
            ).set_color_by_tex_to_color_map(cmap),
            MathTex(
                r"=", r"\log\left( ", r"10^{\log(a) - \log(b)}", r"\right)", substrings_to_isolate=["a", "b"]
            ).set_color_by_tex_to_color_map(cmap),
            MathTex(
                r"=", r"{\log(a) - \log(b)}", substrings_to_isolate=["a", "b"]
            ).set_color_by_tex_to_color_map(cmap),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        og_term.next_to(steps[0], LEFT)

        self.play(
            Write(og_term),
            run_time=1
        )
        self.slide_pause()

        self.play(
            Indicate(log_defs[1])
        )
        self.play(
            Write(steps[0]),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Indicate(pow_rules[1])
        )
        self.play(
            og_term.copy().animate.set_opacity(0.33),
            steps[0].animate.set_opacity(0.33),
            og_term.animate.next_to(steps[1], LEFT),
            TransformMatchingTex(
                steps[0].copy(), steps[1], transform_mismatches=True
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Indicate(log_defs[0])
        )
        self.play(
            og_term.copy().animate.set_opacity(0.33),
            steps[1].animate.set_opacity(0.33),
            og_term.animate.next_to(steps[2], LEFT),
            TransformMatchingTex(
                steps[1].copy(), steps[2], transform_mismatches=True
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [
                log_defs, pow_rules, recs, def_titles, regneregel, srec
            ]],
            VGroup(regneregel, srec).animate.move_to(ORIGIN),
            run_time=2
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                Uncreate(srec, lag_ratio=0, run_time=1),
                Unwrite(regneregel, run_time=1),
                lag_ratio=0.5
            ),
        )

    def regneregel_3(self, defs):
        log_defs, pow_rules, recs, def_titles, cmap = defs
        cmap["a"] = RED
        cmap["b"] = RED_A
        regneregel = MathTex(
            r"\log( a^{b} ) = b \cdot \log(a)", substrings_to_isolate=["a", "b"]
        ).set_color_by_tex_to_color_map(cmap).set_z_index(3)
        srec = get_background_rect(regneregel, stroke_colour=color_gradient([cmap["a"], cmap["b"]], 3))
        self.play(
            LaggedStart(
                Write(regneregel, run_time=4),
                Create(srec, run_time=1),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        self.play(
            VGroup(regneregel, srec).animate.to_edge(UR)
        )
        self.remove(regneregel, srec)
        self.add(regneregel, srec)
        #
        # og_term = MathTex(r"\log(a^{b})", substrings_to_isolate=["a", "b"]).set_color_by_tex_to_color_map(cmap)
        #
        # steps = VGroup(
        #     MathTex(
        #         r"=", r"\log\left( \left( 10^{\log(a)} \right)^b", r"\right)", substrings_to_isolate=["a", "b"]
        #     ).set_color_by_tex_to_color_map(cmap),
        #     MathTex(
        #         r"=", r"\log\left( 10^{\log(a) \cdot b}", r"\right)", substrings_to_isolate=["a", "b"]
        #     ).set_color_by_tex_to_color_map(cmap),
        #     MathTex(
        #         r"=", r"b \cdot \log(a)", substrings_to_isolate=["a", "b"]
        #     ).set_color_by_tex_to_color_map(cmap),
        # ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        # og_term.next_to(steps[0], LEFT)
        #
        # self.play(
        #     Write(og_term),
        #     run_time=1
        # )
        # self.slide_pause()
        #
        # self.play(
        #     Indicate(log_defs[1])
        # )
        # self.play(
        #     Write(steps[0]),
        #     run_time=2
        # )
        # self.slide_pause()
        #
        # self.play(
        #     Indicate(pow_rules[2])
        # )
        # self.play(
        #     og_term.copy().animate.set_opacity(0.33),
        #     steps[0].animate.set_opacity(0.33),
        #     og_term.animate.next_to(steps[1], LEFT),
        #     TransformMatchingTex(
        #         steps[0].copy(), steps[1], transform_mismatches=True
        #     ),
        #     run_time=2
        # )
        # self.slide_pause()
        #
        # self.play(
        #     Indicate(log_defs[0])
        # )
        # self.play(
        #     og_term.copy().animate.set_opacity(0.33),
        #     steps[1].animate.set_opacity(0.33),
        #     og_term.animate.next_to(steps[2], LEFT),
        #     TransformMatchingTex(
        #         steps[1].copy(), steps[2], transform_mismatches=True
        #     ),
        #     run_time=2
        # )
        # self.slide_pause()
        #
        # self.play(
        #     *[FadeOut(m) for m in self.mobjects if m not in [
        #         log_defs, pow_rules, recs, def_titles, regneregel, srec
        #     ]],
        #     VGroup(regneregel, srec).animate.move_to(ORIGIN),
        #     run_time=2
        # )
        # self.slide_pause()
        #
        # self.play(
        #     LaggedStart(
        #         Uncreate(srec, lag_ratio=0, run_time=1),
        #         Unwrite(regneregel, run_time=1),
        #         lag_ratio=0.5
        #     ),
        # )

