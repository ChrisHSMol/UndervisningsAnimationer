from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np
import math

slides = True
if slides:
    from manim_slides import Slide

c = {
    "tal": GREEN,
    "Tal": GREEN,
    "størrelse": GREEN,
    "punkt": RED,
    "Punkter": RED,
    "vektor": YELLOW,
    "Vektorer": YELLOW,
    "retning": YELLOW,
    "koordinat": BLUE
}


class VektorIntro(Slide if slides else Scene):
    def construct(self):
        bool_play_titles = True
        if bool_play_titles:
            titles = self.intro()
            self.slide_pause()
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [titles[0]]],
                titles[0].animate.move_to(ORIGIN)
            )
            edge = DL
            _title, _title_ul_box = play_title(self, titles[0], edge=edge, already_written=True)

        self.om_tal()
        self.om_punkter()

        if bool_play_titles:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title, _title_ul_box]]
            )
            _title, _title_ul_box = update_title(self, titles[0], titles[1], edge=edge)
        self.om_vektorer()

        if bool_play_titles:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [_title, _title_ul_box]]
            )
            _title, _title_ul_box = update_title(self, titles[1], titles[2], edge=edge)
        self.vektor_koordinater()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def intro(self):
        title1 = Tex("Genopfriskning ", "af ", "tal ", "og ", "punkter")
        title1[2].set_color(c["tal"])
        title1[-1].set_color(c["punkt"])
        title2 = Tex("Hvad ", "er ", "en ", "vektor", "?")
        title2[3].set_color(c["vektor"])
        title3 = Tex("Hvordan ", "beskriver ", "man ", "vektorer", "?")
        title3[1].set_color(c["koordinat"])
        title3[3].set_color(c["vektor"])
        sub_titles = VGroup(
            title1,
            title2,
            title3,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT)

        title = Tex("Introduktion ", "til ", "vektorer")
        title[-1].set_color(c["vektor"])
        self.play(
            Write(title),
            run_time=0.5
        )
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        self.play(
            Write(sub_titles),
            run_time=0.5
        )
        self.slide_pause()
        return sub_titles

    def om_tal(self):
        scene_marker("Tal og punkter: Tal")
        nline = NumberLine(include_numbers=True).set_z_index(6, family=True)
        tekst_tal = Tex("Tal ", "har en ", "størrelse")\
            .set_z_index(nline.get_z_index()+2)\
            .set_color_by_tex_to_color_map(c)
        self.play(
            Write(tekst_tal),
            run_time=0.75
        )
        self.slide_pause()

        x_tracker = ValueTracker(0)
        size_tracker = ValueTracker(1)
        opa_tracker = ValueTracker(1)
        dot = always_redraw(lambda:
            Dot(
                [x_tracker.get_value(), 0, 0],
                color=c["tal"],
                z_index=nline.get_z_index() + 1,
                fill_opacity=opa_tracker.get_value()
            ).scale(size_tracker.get_value())
        )
        self.play(
            tekst_tal.animate.shift(1.5*UP),
            TransformFromCopy(VGroup(tekst_tal[0], tekst_tal[-1]), dot)
        )
        self.slide_pause()

        self.play(
            size_tracker.animate.set_value(8)
        )
        self.slide_pause()

        radius_line = Line(
            start=dot.get_center(),
            end=dot.get_right(),
            color=dot.get_color()
        )
        self.play(
            opa_tracker.animate.set_value(0.25)
        )
        self.play(
            Create(radius_line)
        )
        self.play(
            Rotate(radius_line, angle=2*PI, about_point=dot.get_center()),
            run_time=2
        )
        self.slide_pause()
        self.play(
            FadeOut(radius_line)
        )
        self.play(
            ShowPassingFlash(
                Circle(radius=dot.get_radius()*size_tracker.get_value()).set_color(YELLOW),
                run_time=3,
                time_width=0.25
            )
        )
        self.play(
            opa_tracker.animate.set_value(1)
        )
        self.slide_pause()

        self.play(
            size_tracker.animate.set_value(2)
        )
        self.slide_pause()

        scene_marker("Tal og punkter: Tallinje")
        dotline = always_redraw(lambda:
            Arrow(
                start=nline.n2p(0),
                end=nline.n2p(x_tracker.get_value()),
                stroke_width=8,
                color=dot.get_color(),
                z_index=nline.get_z_index() + 1,
                buff=0
            )
        )
        dot_text = always_redraw(lambda:
            DecimalNumber(
                dot.get_center()[0],
                include_sign=True,
                num_decimal_places=2,
                color=dot.get_color()
            ).next_to(dot, UP).set_z_index(5)
        )
        self.add(dotline)
        self.play(
            DrawBorderThenFill(nline),
            TransformFromCopy(tekst_tal[-1], dot_text)
        )
        self.slide_pause()

        for x in [2, 5, 0.5, -6, 0]:
            self.play(
                x_tracker.animate.set_value(x)
            )
            self.slide_pause()

        dim_tekst_tal = Tex("Tal kan \"bevæge sig\" i ", "1 dimension").next_to(nline, DOWN).set_z_index(5)
        dim_tekst_tal[-1].set_color(c["tal"])
        self.play(
            Write(dim_tekst_tal)
        )
        self.slide_pause()

        srec1 = Rectangle(width=16, height=4, z_index=4)\
            .set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK).to_edge(DOWN, buff=0)
        srec2 = srec1.copy().to_edge(UP, buff=0)
        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            z_index=2
        ).add_coordinates()
        self.add(srec1, srec2, plane)
        self.play(
            srec1.animate.shift(5*DOWN),
            srec2.animate.shift(5*UP),
            FadeOut(tekst_tal, shift=UP),
            FadeOut(dim_tekst_tal, shift=DOWN),
            FadeOut(VGroup(nline, dot, dot_text)),
        )
        self.slide_pause()
        self.remove(plane)

    def om_punkter(self):
        scene_marker("Tal og punkter: punkter")
        np.random.seed(42)
        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            z_index=1
        ).add_coordinates()
        self.add(plane)

        tekst_origo = Tex(
            "Origo",
            color=c["punkt"]
        ).move_to(plane.c2p(-1, 2)).set_z_index(plane.get_z_index()+1)
        arrow_origo = Arrow(
            start=tekst_origo.get_center(),
            end=plane.c2p(0, 0)
        ).set_color(c["punkt"]).set_z_index(plane.get_z_index()+1)
        self.play(
            Write(tekst_origo),
            GrowArrow(arrow_origo),
            run_time=0.75
        )
        self.slide_pause()

        xp, yp = ValueTracker(0), ValueTracker(0)
        pkt = always_redraw(lambda: Dot(
            plane.c2p(xp.get_value(), yp.get_value()),
            color=c["punkt"],
            fill_opacity=1
        ).scale(1).set_z_index(plane.get_z_index()+1))
        self.play(
            TransformFromCopy(VGroup(tekst_origo, arrow_origo), pkt),
            FadeOut(tekst_origo, shift=-0.5 * tekst_origo.get_center()),
            FadeOut(arrow_origo, shift=-0.5 * arrow_origo.get_center())
        )
        self.slide_pause()

        hori_line = always_redraw(lambda: Line(
            start=plane.c2p(0, 0),
            end=plane.c2p(xp.get_value(), 0),
            color=RED_E,
            stroke_width=5,
            fill_opacity=0.5,
            z_index=plane.get_z_index()+1
        ))
        vert_line = always_redraw(lambda: Line(
            start=plane.c2p(xp.get_value(), 0),
            end=plane.c2p(xp.get_value(), yp.get_value()),
            color=RED_A,
            stroke_width=5,
            fill_opacity=0.5,
            z_index=plane.get_z_index()+1
        ))
        self.add(hori_line, vert_line)
        coord_pkt = always_redraw(lambda: VGroup(
            MathTex(r"\left("),
            MathTex(f"{xp.get_value():.1f}", color=hori_line.get_color()),
            MathTex(r";"),
            MathTex(f"{yp.get_value():.1f}", color=vert_line.get_color()),
            MathTex(r"\right)"),
        ).arrange(RIGHT, buff=0.1).next_to(pkt, UR))
        self.play(
            Write(coord_pkt),
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            xp.animate.set_value(3)
        )
        self.slide_pause()

        hori_text = always_redraw(lambda: DecimalNumber(
            xp.get_value(),
            include_sign=True if xp.get_value() < 0 else False,
            num_decimal_places=1,
            color=hori_line.get_color()
        ).next_to(hori_line, DOWN))
        self.play(
            Write(hori_text),
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            yp.animate.set_value(1)
        )
        self.slide_pause()

        vert_text = always_redraw(lambda: DecimalNumber(
            yp.get_value(),
            include_sign=True if yp.get_value() < 0 else False,
            num_decimal_places=1,
            color=vert_line.get_color()
        ).next_to(vert_line, LEFT))
        self.play(
            Write(vert_text),
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            yp.animate.set_value(2)
        )
        self.slide_pause()

        scene_marker("Tal og punkter: bevægende punkt")

        for x, y in np.random.uniform(low=-3, high=3, size=(4, 2)):
            self.play(
                xp.animate.set_value(x),
                yp.animate.set_value(y)
            )
            xs_pause(self)
        self.play(
            xp.animate.set_value(3),
            yp.animate.set_value(2)
        )
        self.slide_pause()

        dim_tekst_pkt = Tex(
            "Punkter ", "kan \"bevæge sig\" rundt i ", "2 dimensioner"
        ).move_to(plane.c2p(0, -2)).set_z_index(plane.get_z_index()+2)
        for i in [0, 2]:
            dim_tekst_pkt[i].set_color(c["punkt"])
        srec = get_background_rect(dim_tekst_pkt)
        self.play(
            FadeIn(srec),
            Write(dim_tekst_pkt),
            run_time=0.5
        )
        self.slide_pause()

        # remains = VGroup(plane, pkt, coord_pkt)
        # self.play(
        #     *[FadeOut(m) for m in self.mobjects if m not in remains],
        #     run_time=0.5
        # )
        # self.play(FadeOut(remains), run_time=0.5)

    def om_vektorer(self):
        scene_marker("Vektorer: kartesiske koordinater")
        np.random.seed(42)
        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            z_index=1
        ).add_coordinates()
        xp, yp = ValueTracker(3), ValueTracker(2)
        pkt = always_redraw(lambda: Dot(
            plane.c2p(xp.get_value(), yp.get_value()),
            color=c["punkt"],
            fill_opacity=1
        ).scale(1).set_z_index(plane.get_z_index()+1))
        coord_pkt = always_redraw(lambda: VGroup(
            MathTex(r"\left("),
            MathTex(f"{xp.get_value():.1f}", color=pkt.get_color()),
            MathTex(r";"),
            MathTex(f"{yp.get_value():.1f}", color=pkt.get_color()),
            MathTex(r"\right)"),
        ).arrange(RIGHT, buff=0.1).next_to(pkt, UR))
        self.play(FadeIn(VGroup(plane, pkt, coord_pkt)), run_time=0.5)
        # self.add(plane, pkt, coord_pkt)

        teksts = VGroup(
            Tex("Vektorer ", "kan ses som en forlængelse af ", "punkter"),
            Tex("Tal ", "har en ", "størrelse"),
            Tex("Vektorer ", "har en ", "størrelse ", "og en ", "retning")
        ).set_z_index(plane.get_z_index()+2)
        for tekst in teksts:
            tekst.set_color_by_tex_to_color_map(c).move_to(plane.c2p(0, -2))\
                .move_to(plane.c2p(-6 + 0.5*tekst.width, -2))
        srecs = VGroup(*[
            get_background_rect(t) for t in teksts
        ])
        self.play(
            FadeIn(srecs[0]),
            Write(teksts[0]),
            run_time=0.5
        )
        self.slide_pause()
        i = 0
        for t, s in zip(teksts[1:], srecs[1:]):
            self.play(
                Transform(srecs[i], s),
                # TransformMatchingTex(tekst_vek0, tekst_tal, transform_mismatch=True)
                LaggedStart(
                    Unwrite(teksts[i], reverse=False),
                    Write(t),
                    lag_ratio=0.5,
                    run_time=2*t.width/teksts.width
                )
            )
            i += 1
            self.slide_pause()
        self.play(
            FadeOut(VGroup(t, *srecs), run_time=0.25)
        )

        xbase, ybase = ValueTracker(0), ValueTracker(0)
        # translation = ValueTracker(ORIGIN)
        vek = always_redraw(lambda: Arrow(
            start=plane.c2p(xbase.get_value(), ybase.get_value()),
            end=plane.c2p(xp.get_value(), yp.get_value()),
            color=c["vektor"],
            z_index=2,
            buff=0
        # ).shift(translation.get_value()))
        ))
        self.play(
            GrowArrow(vek)
        )
        self.slide_pause()

        for x, y in np.append(np.random.uniform(low=-3, high=3, size=(5, 2)), [[3, 2]], axis=0):
            self.play(
                xp.animate.set_value(x),
                yp.animate.set_value(y),
                run_time=2
            )
            self.slide_pause(0.1)

        dim_tekst_vek = Tex(
            "Vektorer ", "kan også \"bevæge sig\" rundt i ", "2 dimensioner"
        ).move_to(plane.c2p(0, -2)).set_z_index(plane.get_z_index()+2)
        for i in [0, 2]:
            dim_tekst_vek[i].set_color(c["vektor"])
        srec = get_background_rect(dim_tekst_vek)
        self.play(
            FadeIn(srec),
            Write(dim_tekst_vek),
            run_time=0.5
        )
        self.slide_pause()


    def _om_vektorer(self):
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

