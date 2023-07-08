from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np
import math

slides = True
if slides:
    from manim_slides import Slide


class BasicVectors(Slide if slides else Scene):
    def construct(self):
        bool_play_titles = True
        if bool_play_titles:
            self.slide_pause()
            title = Tex("Grundlæggende om ", "vektorer")
            title[1].set_color(YELLOW)
            _title, _title_ul_box = play_title(self, title, edge=DL)
        self.om_vektorer()
        self.slide_pause(0.5)

        if bool_play_titles:
            title2 = Tex("Vektorers ", "koordinater").set_z_index(_title.get_z_index())
            title2[1].set_color(BLUE)
            self.play(_title.animate.set_opacity(1.0).move_to([0, 0, 0]))
            self.play(Transform(_title, title2))
            self.play(_title.animate.set_opacity(0.15).to_edge(DL, buff=0.05))

        self.vektor_koordinater()
        self.play(*[FadeOut(m) for m in self.mobjects if m != _title])
        if bool_play_titles:
            play_title_reverse(self, _title, edge=ORIGIN)
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def om_vektorer(self):
        nline = NumberLine(include_numbers=True).set_z_index(6, family=True)
        srec1 = Rectangle(width=16, height=4, z_index=4)\
            .set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK).to_edge(DOWN, buff=0)
        srec2 = srec1.copy().to_edge(UP, buff=0)
        plane = NumberPlane(z_index=2)
        tekst_tal = Tex("Tal har en ", "størrelse").set_z_index(nline.get_z_index()+2)
        tekst_tal[1].set_color(GREEN)
        tekst_vek = Tex("Vektorer har en ", "størrelse", " og en ", "retning").set_z_index(nline.get_z_index()+2)
        tekst_vek[1].set_color(GREEN)
        tekst_vek[3].set_color(YELLOW)

        tekst_tal = VGroup(
            tekst_tal,
            SurroundingRectangle(tekst_tal, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=nline.get_z_index()+1)
        )
        tekst_vek = VGroup(
            tekst_vek,
            SurroundingRectangle(tekst_vek, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=nline.get_z_index()+1)
        )

        scene_marker("Tal vs. vektorer")
        self.play(
            Write(tekst_tal)
        )
        self.slide_pause()
        self.play(
            tekst_tal.animate.shift(1.5*UP),
            # Write(tekst_vek)
        )

        x_tracker = ValueTracker(0)
        size_tracker = ValueTracker(1)
        dot = always_redraw(lambda:
            Dot(
                [x_tracker.get_value(), 0, 0],
                color=GREEN,
                z_index=nline.get_z_index() + 1
                # .shift(0.1*UP)
            ).scale(size_tracker.get_value())
        )
        self.play(
            Create(dot)
        )
        self.slide_pause()
        for factor in [8, 0.1, 2]:
            self.play(
                # dot.animate.scale(factor)
                size_tracker.animate.set_value(factor)
            )
            xs_pause(self)

        dotline = always_redraw(lambda:
            Line(
                start=nline.n2p(0),
                end=nline.n2p(x_tracker.get_value()),
                stroke_width=8,
                color=dot.get_color(),
                z_index=dot.get_z_index()
            )
        )
        dot_text = always_redraw(lambda:
            DecimalNumber(
                dot.get_center()[0],
                include_sign=True,
                num_decimal_places=2,
                color=dot.get_color()
            ).next_to(dot, UP)
        )
        self.add(dotline)
        self.slide_pause()
        self.play(
            DrawBorderThenFill(nline),
            TransformFromCopy(tekst_tal[0][-1], dot_text)
        )
        self.slide_pause()
        for x in [2, -6, 0]:
            self.play(
                x_tracker.animate.set_value(x)
            )
            xs_pause(self)
        self.slide_pause(0.5)

        self.play(FadeOut(dot_text, dot))

        tekst_vek.move_to(tekst_tal)
        self.play(AnimationGroup(
            FadeOut(tekst_tal, shift=UP*0.5),
            FadeIn(tekst_vek, shift=UP*0.5)
        ))
        self.slide_pause(0.5)
        scene_marker("Vektorer")
        self.add(srec1, srec2, plane)
        self.play(
            srec1.animate.shift(5*DOWN),
            srec2.animate.shift(5*UP),
            tekst_vek.animate.to_edge(UP),
            FadeOut(nline)
        )
        self.remove(srec1, srec2, dotline)
        plane.set_z_index(0)

        x_tracker = ValueTracker(0)
        y_tracker = ValueTracker(0)
        size_tracker.set_value(0.25)
        vektor = always_redraw(lambda:
            Vector(
                # dot.get_center(),
                plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=GREEN
            ).set_z_index(plane.get_z_index() + 1)
        )
        vek_bue = always_redraw(lambda:
            Arc(
                # radius=0.25,
                radius=size_tracker.get_value(),
                start_angle=0,
                # angle=math.atan(y_tracker.get_value()/x_tracker.get_value()),
                angle=vektor.get_angle(),
                color=YELLOW
            )
        )

        self.slide_pause(0.5)
        self.add(vektor)
        self.slide_pause(0.5)
        # for x, y in zip([2, 1, -3, -2, 1], [1, 2, 3, -1, 0]):
        for x, y in zip([1, -1, 0, 0, 0, 0, 1], [0, 0, 0, 1, -1, 0, 0]):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
                run_time=1
            )
            xs_pause(self)
        self.slide_pause(0.5)
        self.add(vek_bue)
        for x, y in zip([2, -1, -3, 1], [1, 2, -2, 0]):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
                run_time=1
            )
            xs_pause(self)
        self.slide_pause(0.5)

        i = 0
        for x, y in zip([np.sqrt(3)/2, 0.5, 0, -0.5, -np.sqrt(3)/2, -1], [0.5, np.sqrt(3)/2, 1, np.sqrt(3)/2, 0.5, 0]):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
                run_time=0.25,
                rate_func=rate_functions.linear
            )
            if i == 0:
                self.play(
                    # vek_bue.animate.set_radius(1.0),
                    size_tracker.animate.set_value(1.0),
                    run_time=1.0
                )
                i += 1

        self.slide_pause(0.5)
        unit_circle = Circle(radius=1.0, color=vek_bue.get_color())
        self.play(Create(unit_circle), x_tracker.animate.set_value(0), run_time=1)
        self.remove(vek_bue)

        self.slide_pause(0.5)
        self.play(ApplyWave(unit_circle), run_time=2)
        self.slide_pause(0.5)
        self.play(
            FadeOut(VGroup(
                plane,
                unit_circle,
                tekst_vek
            ))
        )

    def vektor_koordinater(self):
        plane = NumberPlane().add_coordinates()
        self.play(
            FadeIn(plane),
            run_time=0.5
        )
        scene_marker("Punkters koordinater")
        tekst_punkt = Tex("Koordinater for ", "punkter").to_edge(UL).set_z_index(plane.get_z_index()+2)
        tekst_punkt[1].set_color(RED)
        tekst_punkt = VGroup(
            tekst_punkt,
            SurroundingRectangle(tekst_punkt, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=tekst_punkt.get_z_index() - 1)
        )
        self.play(
            FadeIn(tekst_punkt)
        )

        x_tracker = ValueTracker(0)
        y_tracker = ValueTracker(0)
        point = always_redraw(lambda:
            Dot(
                plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=RED,
                radius=0.125
            )
        )
        point_coord = always_redraw(lambda:
            Tex(
                "(", f"{x_tracker.get_value():3.1f}", "; ", f"{y_tracker.get_value():3.1f}", ")"
            ).next_to(point, DR).set_z_index(point.get_z_index())
        )
        point_coord = VGroup(
            point_coord,
            SurroundingRectangle(point_coord, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=point_coord.get_z_index() - 1)
        )
        vert_line = always_redraw(lambda:
            Line(
                start=plane.c2p(x_tracker.get_value(), 0, 0),
                end=plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=RED_C,
                stroke_width=3
            )
        )
        hori_line = always_redraw(lambda:
            Line(
                start=plane.c2p(0, y_tracker.get_value(), 0),
                end=plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=RED_C,
                stroke_width=3
            )
        )

        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(point),
            FadeIn(point_coord),
            run_time=0.5
        )
        self.add(vert_line, hori_line)
        self.slide_pause(0.5)

        i = 0
        for x, y in zip(
            [1, 3, -1, -4, 3, 0],
            [0, 1, 3, -2, -1, 0]
        ):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
            )
            xs_pause(self)
            if i == 1:
                ts = VGroup(
                    DecimalNumber(y_tracker.get_value(), num_decimal_places=0,
                                  color=vert_line.get_color()).scale(0.75).next_to(vert_line, LEFT),
                    DecimalNumber(x_tracker.get_value(), num_decimal_places=0,
                                  color=hori_line.get_color()).scale(0.75).next_to(hori_line, DOWN),
                )
                self.play(FadeIn(ts))
                self.slide_pause(0.5)
                self.play(FadeOut(ts))
            i += 1
        self.slide_pause(0.5)
        self.play(
            FadeOut(point),
            FadeOut(point_coord),
            run_time=0.5
        )
        # self.remove(vert_line, hori_line)
        self.slide_pause(0.5)

        scene_marker("Vektorers koordinater")
        tekst_vektor = Tex("Koordinater for ", "vektorer").to_edge(UL).set_z_index(plane.get_z_index()+2)
        tekst_vektor[1].set_color(YELLOW)
        tekst_vektor = VGroup(
            tekst_vektor,
            SurroundingRectangle(tekst_vektor, color=BLACK, fill_color=BLACK, buff=0.1, stroke_width=0.1,
                                 fill_opacity=0.5, z_index=tekst_vektor.get_z_index() - 1)
        )
        self.play(AnimationGroup(
            FadeOut(tekst_punkt[0][-1], shift=UP*0.5),
            FadeIn(tekst_vektor[0][-1], shift=UP*0.5)
        ))
        self.slide_pause(0.5)

        vector = always_redraw(lambda:
            Vector(
                direction=plane.c2p(x_tracker.get_value(), y_tracker.get_value(), 0),
                color=YELLOW
            )
        )
        self.add(vector)
        self.play(
            x_tracker.animate.set_value(1.0),
            y_tracker.animate.set_value(2.0)
        )
        self.slide_pause(0.5)

        vector_coord = always_redraw(lambda:
            Matrix(
                [[f"{x_tracker.get_value():3.2f}"],
                 [f"{y_tracker.get_value():3.2f}"]]
            ).next_to(vector, RIGHT)
        )
        self.play(
            DrawBorderThenFill(
                vector_coord
            )
        )

        for x, y in zip(
            [1, 3, -1, -4, 3, 2],
            [0, 1, 3, -2, -1, 1]
        ):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
            )
            xs_pause(self)
        self.slide_pause(0.5)
        self.play(FadeOut(vector_coord), run_time=0.5)

        scene_marker("Polære koordinater")
        vek_bue = always_redraw(lambda:
            Arc(
                radius=0.75,
                start_angle=0,
                angle=vector.get_angle(),
                color=YELLOW
            )
        )
        hori_line2 = always_redraw(lambda:
            Line(
                start=plane.c2p(0, 0, 0),
                end=plane.c2p(x_tracker.get_value(), 0, 0),
                color=RED_C,
                stroke_width=3
            )
        )
        self.play(
            # FadeOut(VGroup(vert_line, hori_line)),
            hori_line.animate.move_to(hori_line2),
            Create(
                vek_bue
            )
        )
        self.remove(hori_line)
        self.add(hori_line2)

        self.slide_pause(0.5)
        self.play(
            x_tracker.animate.set_value(5.0),
            y_tracker.animate.set_value(3.0),
        )
        vec_ang = always_redraw(lambda:
            # DecimalNumber(
            #     vector.get_angle() * 180/PI,
            #     num_decimal_places=1,
            #     include_sign=True,
            #     color=vek_bue.get_color()
            # ).scale(0.75).next_to(vek_bue, RIGHT)
            MathTex(f"{vector.get_angle() * 180/PI:.1f}^\circ",
                    color=vek_bue.get_color()).scale(0.75).next_to(vek_bue, RIGHT)
        )
        vec_len = always_redraw(lambda:
            DecimalNumber(
                vector.get_length(),
                num_decimal_places=1,
                color=vector.get_color()
            ).scale(0.75).next_to(vector, np.mean([UR, DL])).shift(0.5*UP)
        )
        self.play(
            Write(vec_ang),
            Write(vec_len)
        )
        self.slide_pause(0.5)

        for x, y in zip(
            [3, -1, -4, 3, 4],
            [1, 3, -2, -1, 3]
        ):
            self.play(
                x_tracker.animate.set_value(x),
                y_tracker.animate.set_value(y),
            )
            xs_pause(self)
        self.slide_pause(0.5)


class VektorOperationer(Slide if slides else Scene):
    def construct(self):
        bool_play_title = True
        if bool_play_title:
            self.slide_pause()
            titles = self.intro()
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [titles[0]]],
                titles[0].animate.move_to(ORIGIN)
            )

        if bool_play_title:
            edge = DL
            _title, _title_ul_box = play_title(self, titles[0], edge=edge, already_written=True)

        self.sum_af_vektorer()
        if bool_play_title:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title, _title_ul_box]]
            )
            _title, _title_ul_box = update_title(self, titles[0], titles[1], edge=edge)

        self.forskel_mellem_vektorer()
        if bool_play_title:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title, _title_ul_box]]
            )
            _title, _title_ul_box = update_title(self, titles[1], titles[2], edge=edge)

        self.skalering_af_vektorer()
        if bool_play_title:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title, _title_ul_box]]
            )
            _title, _title_ul_box = update_title(self, titles[2], titles[3], edge=edge)

        self.laengde_af_vektor()
        if bool_play_title:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title, _title_ul_box]]
            )
            _title, _title_ul_box = update_title(self, titles[3], titles[4], edge=edge)

        self.prikprodukt()
        if bool_play_title:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title]]
            )
            play_title_reverse(self, _title, edge=ORIGIN)
        self.slide_pause(5.0)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def intro(self):
        title1 = Tex("Sum ", "af ", "to ", "vektorer")
        title1[0].set_color(YELLOW)
        title2 = Tex("Forskel ", "mellem ", "to ", "vektorer")
        title2[0].set_color(YELLOW)
        title3 = Tex("Skalering ", "af ", "vektorer")
        title3[0].set_color(YELLOW)
        title4 = Tex("Længde ", "af ", "en ", "vektor")
        title4[0].set_color(YELLOW)
        title5 = Tex("Prikproduktet ", "af ", "to ", "vektorer")
        title5[0].set_color(YELLOW)
        sub_titles = VGroup(
            title1,
            title2,
            title3,
            title4,
            title5,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT)

        title = Tex("Vektorers ", "operationer")
        title[1].set_color(YELLOW)
        self.play(
            Write(title)
        )
        self.slide_pause()
        self.play(
            Unwrite(title, reverse=True)
        )
        self.play(
            Write(sub_titles)
        )
        self.slide_pause()
        return sub_titles

    def sum_af_vektorer(self):
        scene_marker("Sum af vektorer: start")
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

        xa, ya = ValueTracker(4), ValueTracker(1)
        xb, yb = ValueTracker(2), ValueTracker(3)

        vec_a = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()),
            color=RED
        ))
        vec_b = always_redraw(lambda: Vector(
            plane.c2p(xb.get_value(), yb.get_value()),
            color=BLUE
        ))

        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).next_to(vec_a, DR)
        )
        coord_b = always_redraw(lambda:
            Matrix(
                [[f"{xb.get_value():2.1f}"],
                 [f"{yb.get_value():2.1f}"]]
            ).set_column_colors(vec_b.get_color()).scale(0.75).next_to(vec_b, UL)
        )
        self.play(
            GrowArrow(vec_a),
            Write(coord_a)
        )
        self.slide_pause()

        for x, y in zip([1, -3, -2, 8, 4], [4, 1, -5, -1, 1]):
            self.play(
                xa.animate.set_value(x),
                ya.animate.set_value(y)
            )
            xs_pause(self)
        self.slide_pause()

        self.play(
            GrowArrow(vec_b),
            Write(coord_b)
        )
        self.slide_pause()

        vec_a_copy = always_redraw(lambda: Arrow(
            start=vec_b.get_end(),
            end=vec_b.get_end() + vec_a.get_end(),
            buff=0,
            color=RED,
        ).set_opacity(0.15))
        vec_b_copy = always_redraw(lambda: Arrow(
            start=vec_a.get_end(),
            end=vec_a.get_end() + vec_b.get_end(),
            buff=0,
            color=BLUE,
        ).set_opacity(0.15))
        self.play(LaggedStart(
            *[
                TransformFromCopy(vec_a, vec_a_copy),
                TransformFromCopy(vec_b, vec_b_copy)
            ],
            lag_ratio=0.75
        ), run_time=4)
        self.slide_pause()

        sum_opa = ValueTracker(1)
        vec_sum = always_redraw(lambda: Vector(
            plane.c2p(
                xa.get_value() + xb.get_value(),
                ya.get_value() + yb.get_value()
            ),
            color=PURPLE
        ).set_opacity(sum_opa.get_value()))
        coord_sum = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value() + xb.get_value():2.1f}"],
                 [f"{ya.get_value() + yb.get_value():2.1f}"]]
            ).set_column_colors(vec_sum.get_color()).scale(0.75).next_to(vec_sum, UR)
        )
        for i in range(2):
            if i:
                self.play(
                    GrowArrow(vec_sum),
                    Write(coord_sum)
                )
            for x, y in zip([1, -3, -2, 8, 4], [4, 1, -5, -1, 1]):
                self.play(
                    xa.animate.set_value(x),
                    ya.animate.set_value(y)
                )
                xs_pause(self)
            self.slide_pause()
        scene_marker("Sum af vektorer: sumvektor tegnet")

        coord_a_fixed = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).to_edge(UL)
        )
        coord_b_fixed = always_redraw(lambda:
            Matrix(
                [[f"{xb.get_value():2.1f}"],
                 [f"{yb.get_value():2.1f}"]]
            ).set_column_colors(vec_b.get_color()).scale(0.75).next_to(coord_a_fixed, RIGHT, buff=1)
        )
        coord_sum_fixed = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value() + xb.get_value():2.1f}"],
                 [f"{ya.get_value() + yb.get_value():2.1f}"]]
            ).set_column_colors(vec_sum.get_color()).scale(0.75).next_to(coord_b_fixed, RIGHT, buff=1)
        )
        vec_labels = always_redraw(lambda: VGroup(
            MathTex(r"\vec{a}", color=vec_a.get_color()).next_to(coord_a_fixed, DOWN),
            MathTex(r"\vec{b}", color=vec_b.get_color()).next_to(coord_b_fixed, DOWN),
            MathTex(r"\vec{a}+\vec{b}", color=vec_sum.get_color()).next_to(coord_sum_fixed, DOWN),
        ))
        self.play(
            TransformFromCopy(coord_a, coord_a_fixed),
            TransformFromCopy(coord_b, coord_b_fixed),
            TransformFromCopy(coord_sum, coord_sum_fixed),
            FadeOut(coord_a),
            FadeOut(coord_b),
            FadeOut(coord_sum),
            Write(vec_labels)
        )
        self.slide_pause()

        eq_sum_text = always_redraw(lambda: VGroup(
            MathTex("+").move_to(between_mobjects(coord_a_fixed, coord_b_fixed)),
            MathTex("=").move_to(between_mobjects(coord_b_fixed, coord_sum_fixed))
        ))
        self.play(
            Write(eq_sum_text)
        )
        self.slide_pause()

        for x, y in zip([1, -3, -2, 8, 4], [4, 1, -5, -1, 1]):
            self.play(
                xa.animate.set_value(x),
                ya.animate.set_value(y)
            )
            xs_pause(self)
        self.slide_pause()

        for x, y in zip([4, 3, -2, -7, 2], [1, -7, -5, 1, 3]):
            self.play(
                xb.animate.set_value(x),
                yb.animate.set_value(y)
            )
            xs_pause(self)
        self.slide_pause()
        scene_marker("Sum af vektorer: generel form")

        general = VGroup(
            Matrix(
                [[r"x_a"],
                 [r"y_a"]]
            ).set_column_colors(vec_a.get_color()),
            MathTex("+"),
            Matrix(
                [[r"x_b"],
                 [r"y_b"]]
            ).set_column_colors(vec_b.get_color()),
            MathTex("="),
            Matrix(
                [[r"x_a + x_b"],
                 [r"y_a + y_b"]]
            ).set_column_colors(vec_sum.get_color())
        ).arrange(RIGHT).set_z_index(10)
        general_box = Rectangle(
            width=general.width * 1.5,
            height=general.height * 1.5
        ).move_to(general).set_style(fill_opacity=0.85, stroke_width=0, fill_color=BLACK).set_z_index(9)
        self.play(
            FadeIn(general_box),
            Write(general)
        )
        self.slide_pause()

    def forskel_mellem_vektorer(self):
        scene_marker("Forskel mellem vektorer: start")
        np.random.seed(14)
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

        xa, ya = ValueTracker(4), ValueTracker(1)
        xb, yb = ValueTracker(2), ValueTracker(3)
        ab_opa = ValueTracker(1)

        vec_a = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()),
            color=GREEN
        ).set_opacity(ab_opa.get_value()))
        vec_b = always_redraw(lambda: Vector(
            plane.c2p(xb.get_value(), yb.get_value()),
            color=BLUE
        ).set_opacity(ab_opa.get_value()))

        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).to_edge(UL)
        )
        coord_b = always_redraw(lambda:
            Matrix(
                [[f"{xb.get_value():2.1f}"],
                 [f"{yb.get_value():2.1f}"]]
            ).set_column_colors(vec_b.get_color()).scale(0.75).next_to(coord_a, RIGHT, buff=1)
        )
        for v, c in zip([vec_a, vec_b], [coord_a, coord_b]):
            self.play(
                GrowArrow(v),
                FadeIn(c, shift=c.get_center()-ORIGIN),
                run_time=2
            )
            xs_pause(self)
        self.slide_pause()

        for ax, bx, ay, by in np.random.uniform(low=-5, high=5, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                xb.animate.set_value(bx),
                ya.animate.set_value(ay),
                yb.animate.set_value(by),
            )
            xs_pause(self)
        self.slide_pause()

        vec_b_copy = always_redraw(lambda: Arrow(
            start=plane.c2p(xa.get_value() - xb.get_value(), ya.get_value() - yb.get_value()),
            end=plane.c2p(xa.get_value(), ya.get_value()),
            buff=0,
            color=BLUE
        ).set_opacity(ab_opa.get_value()))
        self.play(
            TransformFromCopy(vec_b, vec_b_copy),
            FadeOut(vec_b)
        )
        diff_opa = ValueTracker(1)
        vec_diff = always_redraw(lambda: Vector(
            plane.c2p(
                xa.get_value() - xb.get_value(),
                ya.get_value() - yb.get_value()
            ),
            color=YELLOW
        ).set_opacity(diff_opa.get_value()))
        coord_diff = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value() - xb.get_value():2.1f}"],
                 [f"{ya.get_value() - yb.get_value():2.1f}"]]
            ).set_column_colors(vec_diff.get_color()).scale(0.75).next_to(coord_b, RIGHT, buff=1)
        )
        eq_diff_text = always_redraw(lambda: VGroup(
            MathTex("-").move_to(between_mobjects(coord_a, coord_b)),
            MathTex("=").move_to(between_mobjects(coord_b, coord_diff))
        ))
        vec_labels = always_redraw(lambda: VGroup(
            MathTex(r"\vec{a}", color=vec_a.get_color()).next_to(coord_a, DOWN),
            MathTex(r"\vec{b}", color=vec_b.get_color()).next_to(coord_b, DOWN),
            MathTex(r"\vec{a}-\vec{b}", color=vec_diff.get_color()).next_to(coord_diff, DOWN),
        ))

        self.play(
            GrowArrow(vec_diff),
            FadeIn(coord_diff),
            FadeIn(eq_diff_text),
            Write(vec_labels),
            ab_opa.animate.set_value(0.25),
            run_time=2
        )
        self.slide_pause()
        scene_marker("Forskel mellem vektorer: diff-vektor tegnet")

        for ax, bx, ay, by in np.random.uniform(low=-5, high=5, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                xb.animate.set_value(bx),
                ya.animate.set_value(ay),
                yb.animate.set_value(by),
            )
            xs_pause(self)
        self.slide_pause()
        scene_marker("Forskel mellem vektorer: generel form")

        general = VGroup(
            Matrix(
                [[r"x_a"],
                 [r"y_a"]]
            ).set_column_colors(vec_a.get_color()),
            MathTex("-"),
            Matrix(
                [[r"x_b"],
                 [r"y_b"]]
            ).set_column_colors(vec_b.get_color()),
            MathTex("="),
            Matrix(
                [[r"x_a - x_b"],
                 [r"y_a - y_b"]]
            ).set_column_colors(vec_diff.get_color())
        ).arrange(RIGHT).set_z_index(10)
        general_box = Rectangle(
            width=general.width * 1.5,
            height=general.height * 1.5
        ).move_to(general).set_style(fill_opacity=0.85, stroke_width=0, fill_color=BLACK).set_z_index(9)
        self.play(
            diff_opa.animate.set_value(0.25),
            ab_opa.animate.set_value(0.1),
            FadeIn(general_box),
            Write(general)
        )
        self.slide_pause()

    def skalering_af_vektorer(self):
        scene_marker("Skalering af vektorer: start")
        np.random.seed(14)
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

        xa, ya = ValueTracker(4), ValueTracker(1)
        t = ValueTracker(1)
        ab_opa = ValueTracker(1)

        vec_a = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()),
            color=YELLOW
        ).set_opacity(ab_opa.get_value()))
        skal_val = always_redraw(lambda: DecimalNumber(
            t.get_value(),
            include_sign=True,
            num_decimal_places=1,
            color=BLUE
        ).scale(0.75).to_edge(UL).shift(0.5*DOWN))
        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).next_to(skal_val, RIGHT, buff=0.75)
        )
        self.play(
            GrowArrow(vec_a),
            Write(coord_a)
        )
        self.slide_pause()

        # skal_val = always_redraw(lambda: DecimalNumber(
        #     t.get_value(),
        #     include_sign=True,
        #     num_decimal_places=1,
        #     color=BLUE
        # ).scale(0.75).next_to(coord_a, RIGHT, buff=0.75))
        skal_text = Tex("Skaleringsfaktor, $t$").next_to(skal_val, DOWN, aligned_edge=LEFT, buff=2).set_color(skal_val.get_color())
        vec_a_t = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()) * t.get_value(),
            color=GREEN
        ).set_opacity(1/(np.abs(t.get_value())**2)))
        coord_a_t = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value() * t.get_value():2.1f}"],
                 [f"{ya.get_value() * t.get_value():2.1f}"]]
            ).set_column_colors(vec_a_t.get_color()).scale(0.75).next_to(coord_a, RIGHT, buff=0.825)
        )
        vec_labels = always_redraw(lambda: VGroup(
            MathTex(r"\vec{a}", color=vec_a.get_color()).next_to(coord_a, DOWN),
            MathTex("t", color=skal_val.get_color()).next_to(skal_val, DOWN, buff=0.76),
            MathTex(r"t\vec{a}", color=vec_a_t.get_color()).next_to(coord_a_t, DOWN),
        ))
        self.play(
            GrowArrow(vec_a_t),
            Write(skal_val),
            Write(skal_text),
            Write(vec_labels),
            Write(coord_a_t)
        )
        self.slide_pause()
        scene_marker("Skalering af vektorer: skaleret vektor tegnet")

        eq_skal_text = always_redraw(lambda: VGroup(
            MathTex(r"\cdot").move_to(between_mobjects(skal_val, coord_a)),
            MathTex("=").move_to(between_mobjects(coord_a, coord_a_t)),
            MathTex(r"\left(").next_to(skal_val, LEFT, buff=0.05),
            MathTex(r"\right)").next_to(skal_val, RIGHT, buff=0.05)
        ))
        self.play(
            Write(eq_skal_text)
        )
        self.slide_pause()

        for tval in [2, 3, -2, 0, 0.5]:
            self.play(
                t.animate.set_value(tval)
            )
            xs_pause(self)
        self.slide_pause()

        for ax, ay in np.random.uniform(low=-5, high=5, size=(5, 2)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay)
            )
            xs_pause(self)
        self.slide_pause()

        for ax, ay, tval in np.random.uniform(low=-5, high=5, size=(5, 3)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
                t.animate.set_value(tval),
                run_time=2
            )
            xs_pause(self)
        self.slide_pause()
        scene_marker("Skalering af vektorer: generel form")

        general = VGroup(
            MathTex("t", color=skal_val.get_color()),
            MathTex(r"\cdot"),
            Matrix(
                [[r"x_a"],
                 [r"y_a"]]
            ).set_column_colors(vec_a.get_color()),
            MathTex("="),
            Matrix(
                [[r"t \cdot x_a"],
                 [r"t \cdot y_a"]]
            ).set_column_colors(vec_a_t.get_color())
        ).arrange(RIGHT).set_z_index(10)
        general_box = Rectangle(
            width=general.width * 1.5,
            height=general.height * 1.5
        ).move_to(general).set_style(fill_opacity=0.85, stroke_width=0, fill_color=BLACK).set_z_index(9)
        self.play(
            FadeIn(general_box),
            Write(general)
        )
        self.slide_pause()

    def laengde_af_vektor(self):
        scene_marker("Længde af vektor: start")
        np.random.seed(14)
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

        xa, ya = ValueTracker(4), ValueTracker(3)
        ab_opa = ValueTracker(1)

        vec_a = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()),
            color=GREEN
        ).set_opacity(ab_opa.get_value()))
        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).to_edge(UL)
        )
        self.play(
            GrowArrow(vec_a),
            Write(coord_a)
        )
        self.slide_pause()

        hline = always_redraw(lambda: DashedLine(
            start=plane.c2p(0, ya.get_value()),
            end=plane.c2p(xa.get_value(), ya.get_value()),
            # color=vec_a.get_color()
            color=BLUE,
            stroke_width=5
        ))
        vline = always_redraw(lambda: DashedLine(
            start=plane.c2p(xa.get_value(), 0),
            end=plane.c2p(xa.get_value(), ya.get_value()),
            # color=vec_a.get_color()
            color=YELLOW,
            stroke_width=5
        ))
        self.play(
            Create(hline),
            Create(vline)
        )
        self.slide_pause()

        for ax, ay in np.random.uniform(low=-5, high=5, size=(5, 2)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
            )
            xs_pause(self)
        self.play(
            xa.animate.set_value(4),
            ya.animate.set_value(3),
        )
        self.slide_pause()

        hline_new = always_redraw(lambda: DashedLine(
            start=plane.c2p(0, 0),
            end=plane.c2p(xa.get_value(), 0),
            color=hline.get_color(),
            stroke_width=6
        ))
        self.play(
            TransformFromCopy(hline, hline_new),
            FadeOut(hline)
        )
        self.slide_pause()

        hypo = always_redraw(lambda: Line(
            start=plane.c2p(0, 0),
            end=plane.c2p(xa.get_value(), ya.get_value()),
            color=vec_a.get_color()
        ))
        line_labels = always_redraw(lambda: VGroup(
            MathTex("a", color=hline.get_color()).next_to(hline_new, DOWN),
            MathTex("b", color=vline.get_color()).next_to(vline, RIGHT),
            MathTex("c", color=vec_a.get_color()).move_to(
                0.5*(hypo.get_start() + hypo.get_end())
            ).shift(0.15*UL),
        ))
        self.play(
            TransformFromCopy(vec_a, hypo),
            FadeOut(vec_a),
            FadeOut(coord_a)
        )
        self.slide_pause()

        self.play(
            Write(line_labels)
        )
        line_labels_copy = always_redraw(lambda: VGroup(
            MathTex("a^2", color=hline.get_color()),
            MathTex("+"),
            MathTex("b^2", color=vline.get_color()),
            MathTex("="),
            MathTex("c^2", color=vec_a.get_color()),
        ).arrange(RIGHT).to_edge(UL))
        self.play(
            TransformFromCopy(line_labels, line_labels_copy)
        )
        self.slide_pause()
        scene_marker("Længde af vektor: udregning")

        calc = always_redraw(lambda: VGroup(
            MathTex(f"({xa.get_value():.1f})^2", color=hline.get_color()),
            MathTex("+"),
            MathTex(f"({ya.get_value():.1f})^2", color=vline.get_color()),
            MathTex("="),
            MathTex(f"({(xa.get_value()**2 + ya.get_value()**2)**0.5:.1f})^2", color=hypo.get_color()),
        ).arrange(RIGHT).to_edge(UL).shift(DOWN))
        self.play(
            Write(calc)
        )
        self.slide_pause()

        for ax, ay in np.random.uniform(low=-5, high=5, size=(5, 2)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
            )
            xs_pause(self)
        self.play(
            xa.animate.set_value(4),
            ya.animate.set_value(3),
        )
        self.slide_pause()
        scene_marker("Længde af vektor: generel form")

        srec = Rectangle(
            width=16,
            height=9
        ).set_style(fill_opacity=0.875, stroke_width=0, fill_color=BLACK).set_z_index(7)
        equations = VGroup(
            MathTex("a^2", "+", "b^2", "=", "c^2"),
            MathTex("c^2", "=", "a^2", "+", "b^2"),
            MathTex("c", "=", r"\sqrt{", "a^2", "+", "b^2", "}"),
            MathTex(r"|\vec{a}|", "=", r"\sqrt{", "x_a^2", "+", "y_a^2", "}")
        ).arrange(DOWN, buff=0.5).set_z_index(8)
        for eq in equations:
            eq.set_color_by_tex_to_color_map({
                "a": hline.get_color(),
                "x": hline.get_color(),
                "b": vline.get_color(),
                "y": vline.get_color(),
                "c": hypo.get_color()
            })
        self.play(
            LaggedStart(*[
                FadeIn(srec),
                Write(equations[0])
            ], lag_ratio=0.5)
        )
        self.slide_pause()
        for i, eq in enumerate(equations[1:]):
            self.play(
                TransformMatchingTex(equations[i].copy(), eq, transform_mismathces=True, path_arc=PI/(2*(i+1))),
                run_time=2,
                # TransformFromCopy(equations[i], eq),
                # run_time=2
            )
            self.slide_pause()

    def prikprodukt(self):
        scene_marker("Prikprodukt af vektorer: start")
        np.random.seed(14)
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

        xa, ya = ValueTracker(4), ValueTracker(1)
        xb, yb = ValueTracker(2), ValueTracker(3)
        ab_opa = ValueTracker(1)
        br_opa = ValueTracker(1)

        vec_a = always_redraw(lambda: Vector(
            plane.c2p(xa.get_value(), ya.get_value()),
            color=RED
        ).set_opacity(ab_opa.get_value()))
        vec_b = always_redraw(lambda: Vector(
            plane.c2p(xb.get_value(), yb.get_value()),
            color=BLUE
        ).set_opacity(ab_opa.get_value()))

        coord_a = always_redraw(lambda:
            Matrix(
                [[f"{xa.get_value():2.1f}"],
                 [f"{ya.get_value():2.1f}"]]
            ).set_column_colors(vec_a.get_color()).scale(0.75).to_edge(UL)
        )
        coord_b = always_redraw(lambda:
            Matrix(
                [[f"{xb.get_value():2.1f}"],
                 [f"{yb.get_value():2.1f}"]]
            ).set_column_colors(vec_b.get_color()).scale(0.75).next_to(coord_a, RIGHT, buff=1)
        )
        braces = always_redraw(lambda: VGroup(
            BraceBetweenPoints(ORIGIN, plane.c2p(xa.get_value(), ya.get_value()), color=vec_a.get_color()),
            BraceBetweenPoints(plane.c2p(xb.get_value(), yb.get_value()), ORIGIN, color=vec_b.get_color()),
        ).set_opacity(br_opa.get_value()))
        for v, c, b in zip([vec_a, vec_b], [coord_a, coord_b], braces):
            self.play(
                GrowArrow(v),
                FadeIn(c),
                GrowFromPoint(b, ORIGIN),
                run_time=2
            )
            xs_pause(self)
        self.remove(braces)
        self.add(braces)
        self.slide_pause()

        braces_fixed = always_redraw(lambda: VGroup(
            Brace(coord_a, color=vec_a.get_color()),
            Brace(coord_b, color=vec_b.get_color())
        ))
        lengths = always_redraw(lambda: VGroup(
            DecimalNumber(
                (xa.get_value()**2 + ya.get_value()**2)**0.5, color=vec_a.get_color()
            ).next_to(braces_fixed[0], DOWN),
            DecimalNumber(
                (xb.get_value()**2 + yb.get_value()**2)**0.5, color=vec_b.get_color()
            ).next_to(braces_fixed[1], DOWN)
        ))
        for i in range(len(braces)):
            self.play(
                TransformFromCopy(braces[i], braces_fixed[i]),
                Write(lengths[i])
            )
        self.play(br_opa.animate.set_value(0.25))
        self.remove(braces_fixed, lengths)
        self.add(braces_fixed, lengths)
        self.slide_pause()

        for ax, bx, ay, by in np.random.uniform(low=-5, high=5, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                xb.animate.set_value(bx),
                ya.animate.set_value(ay),
                yb.animate.set_value(by),
            )
            xs_pause(self)
        self.play(
            xa.animate.set_value(6),
            xb.animate.set_value(2),
            ya.animate.set_value(0),
            yb.animate.set_value(3),
        )
        self.slide_pause()
        scene_marker("Prikprodukt af vektorer: projektion")

        sun = VGroup(
            Circle(radius=5, color=YELLOW).set_opacity(1),
            Circle(radius=6, color=BLACK, fill_opacity=0, stroke_width=0)
        ).shift(8*UP+RIGHT)
        sun += VGroup(*[Line(
            start=sun[0].point_at_angle((a + 270)*DEGREES),
            end=sun[1].point_at_angle((a + 270)*DEGREES),
            color=YELLOW,
            stroke_width=3
        ) for a in np.linspace(-45, 45, 15)])
        self.play(
            FadeIn(sun, shift=2*DOWN),
            run_time=2
        )
        self.slide_pause()
        # for a in [0.5, -1, 0.5]:
        #     self.play(
        #         Rotate(
        #             sun,
        #             angle=a * PI,
        #             about_point=ORIGIN
        #         ),
        #         run_time=5
        #     )

        hline = always_redraw(lambda: DashedLine(
            start=plane.c2p(xb.get_value(), yb.get_value()),
            end=plane.c2p(xb.get_value(), 0),
            color=vec_b.get_color()
        ))
        vec_b_proj = always_redraw(lambda: Vector(
            plane.c2p(xb.get_value(), 0),
            color=GREEN
        ).set_opacity(0.75))
        self.play(
            Create(hline)
        )
        self.slide_pause()
        self.play(
            TransformFromCopy(vec_b, vec_b_proj),
            FadeOut(sun, shift=2*UP)
        )

        for bx, by in np.random.uniform(low=-5, high=5, size=(5, 2)):
            self.play(
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
            )
            xs_pause(self)
        self.play(
            xb.animate.set_value(2),
            yb.animate.set_value(3),
        )
        self.slide_pause()

        res = VGroup(
            Brace(vec_b_proj, color=vec_b_proj.get_color()).next_to(coord_b, RIGHT, buff=1),
            braces_fixed[0].copy().next_to(coord_b, RIGHT, buff=2.5)
        )
        eq_text = always_redraw(lambda: VGroup(
            MathTex(r"\bullet").move_to(between_mobjects(coord_a, coord_b)),
            MathTex("=").move_to(between_mobjects(coord_b, res[0])),
            MathTex(r"\cdot").move_to(between_mobjects(res[0], res[1])),
        ))
        self.play(
            Write(res),
            Write(eq_text)
        )
        self.slide_pause()

        for bx, by in np.random.uniform(low=-5, high=5, size=(5, 2)):
            self.play(
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
            )
            xs_pause(self)
        self.play(
            xb.animate.set_value(4),
            yb.animate.set_value(3),
            br_opa.animate.set_value(0)
        )
        self.slide_pause()
        scene_marker("Prikprodukt af vektorer: forklaringer")

        forklaring1 = VGroup(
            Tex("Hvis den ", "blå", " og ", "røde", " vektor peger ", "samme", " retning:"),
            MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", ">", "0")
        ).arrange(DOWN, aligned_edge=RIGHT).set_z_index(12).to_edge(DR)
        forklaring1[0][1].set_color(vec_b.get_color())
        forklaring1[1][2].set_color(vec_b.get_color())
        forklaring1[0][3].set_color(vec_a.get_color())
        forklaring1[1][0].set_color(vec_a.get_color())
        forklaring1[0][5].set_color(YELLOW)
        forklaring1[1][-2:].set_color(YELLOW)
        srec = Rectangle(
            width=forklaring1.width * 1.05,
            height=forklaring1.height * 1.05
        ).move_to(forklaring1).set_style(fill_opacity=0.85, stroke_width=0, fill_color=BLACK).set_z_index(11)
        self.play(
            FadeIn(srec),
            Write(forklaring1)
        )
        self.slide_pause()

        self.play(
            xb.animate.set_value(-4),
            yb.animate.set_value(3),
        )
        self.slide_pause()

        forklaring2 = VGroup(
            Tex("Hvis den ", "blå", " og ", "røde", " vektor peger ", "modsat", " retning:"),
            MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", "<", "0")
        ).arrange(DOWN, aligned_edge=RIGHT).set_z_index(12).to_edge(DR)
        forklaring2[0][1].set_color(vec_b.get_color())
        forklaring2[1][2].set_color(vec_b.get_color())
        forklaring2[0][3].set_color(vec_a.get_color())
        forklaring2[1][0].set_color(vec_a.get_color())
        forklaring2[0][5].set_color(YELLOW)
        forklaring2[1][-2:].set_color(YELLOW)
        self.play(
            TransformMatchingTex(forklaring1, forklaring2)
        )
        self.slide_pause()

        self.play(
            xb.animate.set_value(0),
            yb.animate.set_value(3),
        )
        self.slide_pause()

        forklaring3 = VGroup(
            Tex("Hvis den ", "blå", " og ", "røde", " står ", "vinkelret", " på hinanden:"),
            MathTex(r"\vec{a}", r"\bullet", r"\vec{b}", "=", "0")
        ).arrange(DOWN, aligned_edge=RIGHT).set_z_index(12).to_edge(DR)
        forklaring3[0][1].set_color(vec_b.get_color())
        forklaring3[1][2].set_color(vec_b.get_color())
        forklaring3[0][3].set_color(vec_a.get_color())
        forklaring3[1][0].set_color(vec_a.get_color())
        forklaring3[0][5].set_color(YELLOW)
        forklaring3[1][-2:].set_color(YELLOW)
        self.play(
            TransformMatchingTex(forklaring2, forklaring3)
        )
        self.slide_pause()
        scene_marker("Prikprodukt af vektorer: generel form")

        srec2 = Rectangle(
            width=16,
            height=9
        ).set_style(fill_opacity=0.875, stroke_width=0, fill_color=BLACK).set_z_index(7)
        equations = VGroup(
            # MathTex(f"{Matrix([['x_a'], ['y_a']])}", r"\bullet", f"{Matrix([['x_b'], ['y_b']])}"),
            MathTex(r"\begin{bmatrix} x_a \\ y_a \end{bmatrix}", r"\bullet",
                    r"\begin{bmatrix} x_b \\ y_b \end{bmatrix}"),
            MathTex("=", "x_a", r"\cdot", "x_b", "+", "y_a", r"\cdot", "y_b"),
            # Matrix([["x_a"], ["y_a"]]),
            # MathTex(r"\bullet"),
            # Matrix([["x_b"], ["y_b"]]),
            # MathTex("="),
            # MathTex("x_a", r"\cdot", "x_b" + "y_a", r"\cdot", "y_b")
        ).set_z_index(8).arrange(RIGHT)
        for eq in equations:
            eq.set_color_by_tex_to_color_map({
                "x_a": vec_a.get_color(),
                "y_a": vec_a.get_color(),
                "x_b": vec_b.get_color(),
                "y_b": vec_b.get_color(),
            })
        self.play(
            srec.animate.set_z_index(5),
            forklaring3.animate.set_z_index(6),
            FadeIn(srec2),
            Write(equations[0])
        )
        self.slide_pause()
        for i, eq in enumerate(equations[1:]):
            self.play(
                TransformMatchingTex(equations[i].copy(), eq, transform_mismatches=True, path_arc=PI/(2*(i+1)))
            )
            self.slide_pause()


class RegnereglerVektorer(Slide if slides else Scene):
    def construct(self):
        self.kommutativ_regel()
        self.associativ_regel()
        self.slide_pause(5.0)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def kommutativ_regel(self):
        np.random.seed(42)
        beskrivelse = VGroup(
            Tex("Den ", "kommutative", " regneregel", " siger,"),
            Tex("at det er ligegyldigt i hvilken rækkefølge"),
            Tex("man lægger ", "to vektorer", " sammen.")
        ).arrange(DOWN, aligned_edge=LEFT)
        beskrivelse[0][1].set_color(YELLOW)
        beskrivelse[2][1].set_color((RED, BLUE))
        sub_bes = beskrivelse[0][:3].copy().to_edge(DL, buff=0.05).set_opacity(0.15).set_z_index(10)
        srec = Rectangle(
            width=sub_bes.width * 1.05,
            height=sub_bes.height * 1.05,
            z_index=9
        ).move_to(sub_bes).set_style(fill_opacity=0.5, stroke_width=0, fill_color=BLACK)
        self.play(
            Write(beskrivelse)
        )
        self.slide_pause()
        regel = MathTex(r"\vec{a}", "+", r"\vec{b}", "=", r"\vec{b}", "+", r"\vec{a}")
        regel[0].set_color(RED)
        regel[6].set_color(RED)
        regel[2].set_color(BLUE)
        regel[4].set_color(BLUE)
        self.play(
            beskrivelse.animate.shift(2*UP),
            FadeIn(regel, shift=2*UP)
        )
        self.slide_pause()
        self.play(
            TransformFromCopy(beskrivelse[0][:3], sub_bes),
            FadeOut(VGroup(beskrivelse, regel))
        )
        self.add(srec)

        plane_left = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).to_edge(LEFT).add_coordinates()
        plane_right = plane_left.copy().to_edge(RIGHT)
        self.play(
            DrawBorderThenFill(
                VGroup(plane_left, plane_right)
            )
        )
        self.slide_pause()

        xa, ya = ValueTracker(5), ValueTracker(2)
        xb, yb = ValueTracker(-1), ValueTracker(3)
        ab_opa = ValueTracker(1)
        vec_a_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xa.get_value(), ya.get_value()), color=RED, buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_b_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xb.get_value(), yb.get_value()), color=BLUE, buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_a_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xa.get_value(), ya.get_value()), color=RED, buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_b_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xb.get_value(), yb.get_value()), color=BLUE, buff=0
        ).set_opacity(ab_opa.get_value()))

        vec_a_text = VGroup(
            MathTex(r"\vec{a}").set_color(vec_a_left.get_color()).next_to(plane_left, UP).shift(0.5*LEFT),
            MathTex(r"\vec{a}").set_color(vec_a_right.get_color()).next_to(plane_right, UP).shift(0.5*RIGHT)
        )
        vec_b_text = VGroup(
            MathTex(r"\vec{b}").set_color(vec_b_left.get_color()).next_to(plane_left, UP).shift(0.5*RIGHT),
            MathTex(r"\vec{b}").set_color(vec_b_right.get_color()).next_to(plane_right, UP).shift(0.5*LEFT)
        )

        self.play(
            *[GrowArrow(v) for v in [vec_a_left, vec_a_right, vec_b_right, vec_b_left]],
            Write(VGroup(vec_a_text, vec_b_text))
        )
        self.slide_pause()

        # for x, y in zip([-2, 1, 5], [1, 3, 2]):
        for ax, bx, ay, by in np.random.uniform(low=-5, high=5, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
            )
            xs_pause(self)

        vec_b_left_copy = always_redraw(lambda: Arrow(
            start=plane_left.c2p(xa.get_value(), ya.get_value()),
            end=plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            color=vec_b_left.get_color(),
            buff=0
        ).set_opacity(ab_opa.get_value()))
        vec_a_right_copy = always_redraw(lambda: Arrow(
            start=plane_right.c2p(xb.get_value(), yb.get_value()),
            end=plane_right.c2p(xb.get_value() + xa.get_value(), yb.get_value() + ya.get_value()),
            color=vec_a_right.get_color(),
            buff=0
        ).set_opacity(ab_opa.get_value()))
        self.play(
            TransformFromCopy(vec_b_left, vec_b_left_copy),
            TransformFromCopy(vec_a_right, vec_a_right_copy),
            FadeOut(VGroup(vec_a_right, vec_b_left))
        )
        self.slide_pause()

        vec_sum_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0),
            plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            color=PURPLE, buff=0
        ))
        vec_sum_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0),
            plane_right.c2p(xb.get_value() + xa.get_value(), yb.get_value() + ya.get_value()),
            color=PURPLE, buff=0
        ))
        eq_symbols = VGroup(
            MathTex("+").move_to(between_mobjects(vec_a_text[0], vec_b_text[0])),
            MathTex("+").move_to(between_mobjects(vec_b_text[1], vec_a_text[1])),
        )
        self.play(
            *[GrowArrow(v) for v in [vec_sum_right, vec_sum_left]],
            ab_opa.animate.set_value(0.25),
            FadeIn(eq_symbols[:2])
        )
        self.slide_pause()

        # for ax, bx, ay, by in zip(
        #     [3, 5, 5, 5, -2],
        #     [-1, -1, -4, -1, -2],
        #     [-1, 2, 2, 2, -1],
        #     [3, 3, -1, 3, 5]
        # ):
        for ax, bx, ay, by in np.random.uniform(low=-3, high=3, size=(5, 4)):
            self.play(
                xa.animate.set_value(ax),
                xb.animate.set_value(bx),
                ya.animate.set_value(ay),
                yb.animate.set_value(by)
            )
            xs_pause(self)
        self.play(
            xa.animate.set_value(-2),
            xb.animate.set_value(-2),
            ya.animate.set_value(-1),
            yb.animate.set_value(5)
        )

        regel.to_edge(UP, buff=0)
        self.play(
            plane_left.animate.move_to(ORIGIN),
            plane_right.animate.move_to(ORIGIN),
            Transform(VGroup(vec_a_text, vec_b_text, eq_symbols), regel),
            run_time=3
        )
        self.slide_pause()
        fade_out_all(self)

    def associativ_regel(self):
        np.random.seed(69)
        beskrivelse = VGroup(
            Tex("Den ", "associative", " regneregel", " siger,"),
            Tex("at hvis man lægger ", "flere vektorer", " sammen,"),
            Tex("så er det ligegyldigt, hvor man starter.")
        ).arrange(DOWN, aligned_edge=LEFT)
        beskrivelse[0][1].set_color(YELLOW)
        beskrivelse[1][1].set_color(color_gradient((BLUE, RED, GREEN), 14))
        sub_bes = beskrivelse[0][:3].copy().to_edge(DL, buff=0.05).set_opacity(0.15).set_z_index(10)
        srec = Rectangle(
            width=sub_bes.width * 1.05,
            height=sub_bes.height * 1.05,
            z_index=9
        ).move_to(sub_bes).set_style(fill_opacity=0.5, stroke_width=0, fill_color=BLACK)
        self.play(
            Write(beskrivelse)
        )
        self.slide_pause()
        regel = MathTex(r"\left(", r"\vec{a}", "+", r"\vec{b}", r"\right)", "+", r"\vec{c}", "=",
                        r"\vec{a}", "+", r"\left(", r"\vec{b}", "+", r"\vec{c}", r"\right)")
        regel[1].set_color(RED)
        regel[8].set_color(RED)
        regel[3].set_color(BLUE)
        regel[11].set_color(BLUE)
        regel[6].set_color(GREEN)
        regel[13].set_color(GREEN)
        self.play(
            beskrivelse.animate.shift(2*UP),
            FadeIn(regel, shift=2*UP)
        )
        self.slide_pause()
        self.play(
            TransformFromCopy(beskrivelse[0][:3], sub_bes),
            FadeOut(VGroup(beskrivelse, regel))
        )
        self.add(srec)

        plane_left = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).to_edge(LEFT).add_coordinates()
        plane_right = plane_left.copy().to_edge(RIGHT)
        self.play(
            DrawBorderThenFill(
                VGroup(plane_left, plane_right)
            )
        )
        self.slide_pause()

        xa, ya = ValueTracker(5), ValueTracker(2)
        xb, yb = ValueTracker(1), ValueTracker(3)
        xc, yc = ValueTracker(-1), ValueTracker(1)
        r1_opa = ValueTracker(1)
        r2_opa = ValueTracker(1)
        r3_opa = ValueTracker(1)

        vec_a_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xa.get_value(), ya.get_value()), buff=0, color=RED
        ).set_opacity(r1_opa.get_value()))
        vec_b_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xb.get_value(), yb.get_value()), buff=0, color=BLUE
        ).set_opacity(r1_opa.get_value()))
        vec_c_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0), plane_left.c2p(xc.get_value(), yc.get_value()), buff=0, color=GREEN
        ).set_opacity(r2_opa.get_value()))

        vec_a_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xa.get_value(), ya.get_value()), buff=0, color=RED
        ).set_opacity(r2_opa.get_value()))
        vec_b_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xb.get_value(), yb.get_value()), buff=0, color=BLUE
        ).set_opacity(r1_opa.get_value()))
        vec_c_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0), plane_right.c2p(xc.get_value(), yc.get_value()), buff=0, color=GREEN
        ).set_opacity(r1_opa.get_value()))

        vec_left_text = VGroup(
            MathTex(r"\vec{a}", color=vec_a_left.get_color()).next_to(plane_left, UP).shift(1.0*LEFT),
            MathTex(r"\vec{b}", color=vec_b_left.get_color()).next_to(plane_left, UP).shift(0.0*LEFT),
            MathTex(r"\vec{c}", color=vec_c_left.get_color()).next_to(plane_left, UP).shift(1.0*RIGHT),
        )
        vec_right_text = VGroup(
            MathTex(r"\vec{a}", color=vec_a_right.get_color()).next_to(plane_right, UP).shift(1.0*LEFT),
            MathTex(r"\vec{b}", color=vec_b_right.get_color()).next_to(plane_right, UP).shift(0.0*LEFT),
            MathTex(r"\vec{c}", color=vec_c_right.get_color()).next_to(plane_right, UP).shift(1.0*RIGHT),
        )

        self.play(
            *[GrowArrow(v) for v in [vec_a_left, vec_a_right, vec_b_left, vec_b_right, vec_c_left, vec_c_right]],
            Write(VGroup(vec_left_text, vec_right_text))
        )
        self.slide_pause()

        for ax, bx, ay, by, cx, cy in np.random.uniform(low=-5, high=5, size=(5, 6)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
                xc.animate.set_value(cx),
                yc.animate.set_value(cy),
            )
            xs_pause(self)
        self.slide_pause()
        self.play(
            xa.animate.set_value(5),
            ya.animate.set_value(2),
            xb.animate.set_value(1),
            yb.animate.set_value(3),
            xc.animate.set_value(-1),
            yc.animate.set_value(1),
        )
        self.slide_pause()

        vec_b_left_copy = always_redraw(lambda: Arrow(
            start=plane_left.c2p(xa.get_value(), ya.get_value()),
            end=plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            color=vec_b_left.get_color(),
            buff=0
        ).set_opacity(r1_opa.get_value()))
        vec_b_right_copy = always_redraw(lambda: Arrow(
            start=plane_right.c2p(xc.get_value(), yc.get_value()),
            end=plane_right.c2p(xc.get_value() + xb.get_value(), yc.get_value() + yb.get_value()),
            color=vec_b_right.get_color(),
            buff=0
        ).set_opacity(r1_opa.get_value()))
        self.play(
            TransformFromCopy(vec_b_left, vec_b_left_copy),
            TransformFromCopy(vec_b_right, vec_b_right_copy),
            FadeOut(VGroup(vec_b_right, vec_b_left))
        )

        vec_sum_ab_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0),
            plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            color=PURPLE, buff=0
        ))
        vec_sum_bc_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0),
            plane_right.c2p(xb.get_value() + xc.get_value(), yb.get_value() + yc.get_value()),
            color=TEAL, buff=0
        ))
        eq_symbols_1 = VGroup(
            MathTex(r"\left(").next_to(vec_left_text[0], LEFT, buff=0),
            MathTex("+").move_to(between_mobjects(vec_left_text[0], vec_left_text[1])),
            MathTex(r"\right)").next_to(vec_left_text[1], RIGHT, buff=0),
            MathTex(r"\left(").next_to(vec_right_text[1], LEFT, buff=0),
            MathTex("+").move_to(between_mobjects(vec_right_text[1], vec_right_text[2])),
            MathTex(r"\right)").next_to(vec_right_text[2], RIGHT, buff=0),
        )
        self.play(
            *[GrowArrow(v) for v in [vec_sum_ab_left, vec_sum_bc_right]],
            Write(eq_symbols_1),
            r1_opa.animate.set_value(0.25)
        )
        self.slide_pause()

        for ax, bx, ay, by, cx, cy in np.random.uniform(low=-3, high=3, size=(5, 6)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
                xc.animate.set_value(cx),
                yc.animate.set_value(cy),
            )
            xs_pause(self)
        self.slide_pause()
        self.play(
            xa.animate.set_value(3),
            ya.animate.set_value(1.5),
            xb.animate.set_value(1),
            yb.animate.set_value(3),
            xc.animate.set_value(-1),
            yc.animate.set_value(1),
        )
        self.slide_pause()

        vec_sum_ab_left_copy = always_redraw(lambda: Arrow(
            start=plane_left.c2p(xc.get_value(), yc.get_value()),
            end=plane_left.c2p(xa.get_value() + xb.get_value() + xc.get_value(),
                               ya.get_value() + yb.get_value() + yc.get_value()),
            color=vec_sum_ab_left.get_color(),
            buff=0
        ).set_opacity(r3_opa.get_value()))
        vec_sum_bc_right_copy = always_redraw(lambda: Arrow(
            start=plane_right.c2p(xa.get_value(), ya.get_value()),
            end=plane_right.c2p(xc.get_value() + xb.get_value() + xa.get_value(),
                                yc.get_value() + yb.get_value() + ya.get_value()),
            color=vec_sum_bc_right.get_color(),
            buff=0
        ).set_opacity(r3_opa.get_value()))

        vec_c_left_copy = always_redraw(lambda: Arrow(
            start=plane_left.c2p(xa.get_value() + xb.get_value(), ya.get_value() + yb.get_value()),
            end=plane_left.c2p(xa.get_value() + xb.get_value() + xc.get_value(),
                               ya.get_value() + yb.get_value() + yc.get_value()),
            color=vec_c_left.get_color(),
            buff=0
        ).set_opacity(r2_opa.get_value()))
        vec_a_right_copy = always_redraw(lambda: Arrow(
            start=plane_right.c2p(xb.get_value() + xc.get_value(), yb.get_value() + yc.get_value()),
            end=plane_right.c2p(xc.get_value() + xb.get_value() + xa.get_value(),
                                yc.get_value() + yb.get_value() + ya.get_value()),
            color=vec_a_right.get_color(),
            buff=0
        ).set_opacity(r2_opa.get_value()))
        self.play(
            TransformFromCopy(vec_sum_ab_left, vec_sum_ab_left_copy),
            TransformFromCopy(vec_sum_bc_right, vec_sum_bc_right_copy),
            TransformFromCopy(vec_c_left, vec_c_left_copy),
            TransformFromCopy(vec_a_right, vec_a_right_copy),
            FadeOut(VGroup(vec_sum_bc_right, vec_sum_ab_left)),
            run_time=4
        )

        vec_sum_left = always_redraw(lambda: Arrow(
            plane_left.c2p(0, 0),
            plane_left.c2p(xa.get_value() + xb.get_value() + xc.get_value(),
                           ya.get_value() + yb.get_value() + yc.get_value()),
            color=YELLOW, buff=0
        ))
        vec_sum_right = always_redraw(lambda: Arrow(
            plane_right.c2p(0, 0),
            plane_right.c2p(xc.get_value() + xb.get_value() + xa.get_value(),
                           yc.get_value() + yb.get_value() + ya.get_value()),
            color=YELLOW, buff=0
        ))
        eq_symbols_2 = VGroup(
            MathTex("+").move_to(between_mobjects(eq_symbols_1[2], vec_left_text[2])),
            MathTex("+").move_to(between_mobjects(vec_right_text[0], eq_symbols_1[3])),
        )
        self.play(
            *[GrowArrow(v) for v in [vec_sum_left, vec_sum_right]],
            Write(eq_symbols_2),
            r3_opa.animate.set_value(0.25),
            r2_opa.animate.set_value(0.25),
            r1_opa.animate.set_value(0.1)
        )
        self.slide_pause()

        for ax, bx, ay, by, cx, cy in np.random.uniform(low=-3, high=3, size=(5, 6)):
            self.play(
                xa.animate.set_value(ax),
                ya.animate.set_value(ay),
                xb.animate.set_value(bx),
                yb.animate.set_value(by),
                xc.animate.set_value(cx),
                yc.animate.set_value(cy),
            )
            xs_pause(self)
        self.slide_pause()
        self.play(
            xa.animate.set_value(3),
            ya.animate.set_value(1.5),
            xb.animate.set_value(1),
            yb.animate.set_value(3),
            xc.animate.set_value(-1),
            yc.animate.set_value(1),
        )
        self.slide_pause()

        regel.to_edge(UP, buff=0)
        self.play(
            plane_left.animate.move_to(ORIGIN),
            plane_right.animate.move_to(ORIGIN),
            r3_opa.animate.set_value(0.0),
            Transform(VGroup(vec_left_text, vec_right_text, eq_symbols_1, eq_symbols_2), regel),
            run_time=3
        )
        self.remove(vec_sum_ab_left_copy, vec_sum_bc_right_copy)
        self.slide_pause()
        fade_out_all(self)
