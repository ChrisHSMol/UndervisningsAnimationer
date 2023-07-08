from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = True
if slides:
    from manim_slides import Slide
base_col = GREEN
rent_col = GREEN_A
annu_col = BLUE
term_col = RED
graph_params = {
    "xlims": (0, 13.5, 1),
    "ylims": (0, 7500, 1000),
    "width": 12
}
plane = Axes(
    x_range=graph_params["xlims"],
    y_range=graph_params["ylims"],
    x_length=graph_params["width"],
    y_length=graph_params["width"] / 16 * 9,
    axis_config={"include_numbers": True}
)
b = 500
r1, r2 = 0.25, 0.02


class Annuitetsopsparing(Slide, MovingCameraScene if slides else MovingCameraScene):
    def construct(self):
        title = "Annuitetsopsparing"
        # play_title(title)
        self.slide_pause(0.5)
        yaxis_lines = self.add_axis_lines(plane, "y")
        self.play(
            DrawBorderThenFill(plane),
            Create(yaxis_lines)
        )
        self.slide_pause(0.5)
        self.one_time_payment()
        # self.annuitet()

    def slide_pause(self, t=1.0, slides_bool=slides):
        if slides_bool:
            indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
            self.play(FadeIn(indicator), run_time=0.25)
            xs_pause(self)
            self.pause()
            self.play(FadeOut(indicator), run_time=0.25)
        else:
            self.wait(t)

    def add_axis_lines(self, axes, axis, stroke_width=0.5, alpha=0.5):
        lines = VGroup()
        if axis == "y":
            for i in range(*axes.get_y_range()):
                lines += DashedLine(
                    start=axes.c2p(0, i),
                    end=axes.c2p(axes.get_x_range()[1], i),
                    color=axes.get_color(),
                    stroke_width=stroke_width,
                    stroke_opacity=alpha
                )
        return lines

    def get_rectangle(self, xpoint, height, buff=0.45, c=base_col):
        return Rectangle(
            width=(plane.c2p(xpoint+buff, 0) - plane.c2p(xpoint-buff, 0))[0],
            height=(plane.c2p(xpoint+buff, height) - plane.c2p(xpoint+buff, 0))[1],
            stroke_width=0.5,
            fill_color=c,
            fill_opacity=1,
            z_index=0
        ).move_to(plane.c2p(xpoint, height/2))

    def get_rect_height(self, rect):
        h = b/0.45 * rect.height
        return DecimalNumber(
            h,
            num_decimal_places=2,
            z_index=rect.z_index + 1,
            color=base_col
            ).scale(0.45).next_to(rect, UP, buff=0.1)
        # ).scale(0.45).next_to(rect, DOWN).shift(0.625*UP)
        #     color=DARKER_GRAY,
        #     stroke_color=DARKER_GRAY
        # ).scale(0.45).next_to(rect, UP).shift(0.45 * DOWN)

    def one_time_payment(self):
        speed_up_index = 4

        b_rects = VGroup()
        rect_texts = VGroup()
        self.camera.frame.save_state()

        b_rect = self.get_rectangle(
            xpoint=1,
            height=b
        )
        rect_text = self.get_rect_height(b_rect)
        b_rects += b_rect
        rect_texts += rect_text
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(b_rect.get_top()),
            run_time=2
        )
        srec = SurroundingRectangle(
            b_rect,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=1,
            z_index=-1
        ).shift(0.58*DOWN)
        self.add(srec)
        self.play(
            # Create(b_rect),
            # GrowFromEdge(b_rect.set_z_index(-2), DOWN),
            b_rect.set_z_index(-2).shift(0.6*DOWN).animate.shift(0.6*UP).set_z_index(0),
            rate_func=rate_functions.ease_out_back,
            run_time=1
        )
        self.remove(srec)
        self.slide_pause(0.5)
        self.play(
            Write(rect_text),
            run_time=0.5
        )
        self.slide_pause(0.5)

        r1_text =MathTex(
            f"+{100*r1:.0f}\%",
            color=rent_col,
            z_index=-1
        ).scale(0.45)

        for i in range(2, 13):
            h = b * (1+r1)**(i-1)
            b_rect = self.get_rectangle(
                xpoint=i,
                height=h
            )
            rect_text = self.get_rect_height(b_rect)

            self.play(
                self.camera.frame.animate.set(
                    width=4
                ).move_to(b_rect.get_top()),
                run_time=2 if i < speed_up_index else 1
            )
            prev_rect = b_rects[-1].copy()#.set_z_index(-1)
            b_rect.set_z_index(1)
            rente = self.get_rectangle(
                i,
                b * ((1+r1)**(i-1) - (1+r1)**(i-2)),
                c=rent_col
            )
            self.play(
                prev_rect.animate.move_to(
                    plane.c2p(i, h/(2*(1+r1)))
                ),
                run_time=1 if i < speed_up_index else 0.5
            )
            # prev_rect.set_z_index(0)
            b_rect.set_z_index(0)
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            self.play(
                TransformFromCopy(
                    prev_rect,
                    rente.next_to(prev_rect, UP, buff=0)
                ),
                Write(
                    r1_text.next_to(b_rect, UP, buff=0.1)
                ),
                run_time=1 if i < speed_up_index else 0.5
            )
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            self.play(
                Transform(
                    VGroup(prev_rect, rente),
                    b_rect
                ),
                # FadeOut(r1_text)
                r1_text.animate.shift(0.5*DOWN),
                run_time=1 if i < speed_up_index else 0.5
            )
            self.remove(r1_text)
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            self.play(
                Write(
                    rect_text
                ),
                run_time=0.5 if i < speed_up_index else 0.25
            )
            b_rects += b_rect
            rect_texts += rect_text
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            # break

        self.play(
            Restore(
                self.camera.frame
            ),
            run_time=2
        )
        self.slide_pause(3)

        forklaring1 = VGroup(
            Tex("Begyndelsesværdi, ", "b", ": ", f"{b:.2f}"),
            Tex("Rente, ", "r", ": ", f"{r1*100:.0f}\%", " = ", f"{r1:.2f}"),
            MathTex("y = ", f"{b:.2f}", "\\cdot", "(1+", f"{r1:.2f}", ")^n")
        ).arrange(DOWN, aligned_edge=LEFT).move_to(plane.c2p(4, 6500))
        forklaring1[0][1].set_color(base_col)
        forklaring1[0][-1].set_color(base_col)
        forklaring1[1][1].set_color(rent_col)
        forklaring1[1][3].set_color(rent_col)
        forklaring1[1][-1].set_color(rent_col)
        forklaring1[2][1].set_color(base_col)
        forklaring1[2][4].set_color(rent_col)
        forklaring1[2][-1][-1].set_color(term_col)
        self.play(
            Write(
                forklaring1
            ),
            run_time=1
        )
        self.slide_pause(3)
        # self.play(FadeOut(
        #     *[
        #         m for m in self.mobjects if m not in (plane, yaxis_lines)
        #     ]
        # ))
        # self.slide_pause(0.5)

    def annuitet(self):
        speed_up_index = 20
        a_rects = VGroup()
        rect_texts = VGroup()
        self.camera.frame.save_state()

        a_rect = self.get_rectangle(
            xpoint=1,
            height=b
        )
        rect_text = self.get_rect_height(a_rect)
        a_rects += a_rect
        rect_texts += rect_text
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(a_rect.get_top()),
            run_time=2
        )
        srec = SurroundingRectangle(
            a_rect,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=1,
            z_index=-1
        ).shift(0.58 * DOWN)
        self.add(srec)
        self.play(
            a_rect.set_z_index(-2).shift(0.6 * DOWN).animate.shift(0.6 * UP).set_z_index(0),
            rate_func=rate_functions.ease_out_back,
            run_time=1
        )
        self.remove(srec)
        self.slide_pause(0.5)
        self.play(
            Write(rect_text),
            run_time=0.5
        )
        self.slide_pause(0.5)

        r2_text = MathTex(
            f"+{100 * r2:.0f}\%",
            color=rent_col,
            z_index=-1
        ).scale(0.45)

        for i in range(2, 13):
            # h = b * (1+r1)**(i-1)
            # a_rect = self.get_rectangle(
            #     xpoint=i,
            #     height=h
            # )
            # rect_text = self.get_rect_height(a_rect)
            h = b * ((1+r2)**(i-1) - 1) / r2
            sub_rect = self.get_rectangle(
                xpoint=i-1,
                height=h,
                c=annu_col
            )

            self.play(
                self.camera.frame.animate.set(
                    width=4
                ).move_to(sub_rect.get_top()),
                a_rect.animate.set_color(annu_col),
                rect_text.animate.set_color(annu_col),
                run_time=2 if i < speed_up_index else 1
            )
            prev_rect = a_rect.copy().move_to(plane.c2p(i, h/(2*(1+r2))))#.set_z_index(-1)
            sub_rect.set_z_index(1)
            rente = self.get_rectangle(
                xpoint=i,
                height=b * (((1+r2)**(i-1) - 1) / r2 - ((1+r2)**(i-2) - 1) / r2),
                c=rent_col
            )
            self.play(
                # prev_rect.animate.move_to(
                sub_rect.animate.move_to(
                    plane.c2p(i, h/(2*(1+r2)))
                ),
                run_time=1 if i < speed_up_index else 0.5
            )
            # prev_rect.set_z_index(0)
            sub_rect.set_z_index(0)
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            self.play(
                prev_rect.set_z_index(-2).animate.shift(0.6 * UP).set_z_index(0),
                rate_func=rate_functions.ease_out_back,
                run_time=1
            )
            self.play(
                TransformFromCopy(
                    sub_rect,
                    rente.next_to(prev_rect, UP, buff=0)
                ),
                Write(
                    r2_text.next_to(a_rect, UP, buff=0.1)
                ),
                run_time=1 if i < speed_up_index else 0.5
            )
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            self.play(
                Transform(
                    VGroup(prev_rect, rente),
                    a_rect
                ),
                # FadeOut(r1_text)
                r2_text.animate.shift(0.5*DOWN),
                run_time=1 if i < speed_up_index else 0.5
            )
            self.remove(r2_text)
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            self.play(
                Write(
                    rect_text
                ),
                run_time=0.5 if i < speed_up_index else 0.25
            )
            a_rects += a_rect
            rect_texts += rect_text
            self.slide_pause(0.5 if i < speed_up_index else 0.25)
            break

        self.play(
            Restore(
                self.camera.frame
            ),
            run_time=2
        )
        self.slide_pause(3)



