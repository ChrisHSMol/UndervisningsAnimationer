from manim import *
from helpers import *
import numpy as np
import subprocess
from custom_classes import BohrAtom
import sys

slides = False
if slides:
    import manim_slides

q = "ul"
_RESOLUTION = {
    "ul": "426,240",
    "l": "854,480",
    "h": "1920,1080"
}
_FRAMERATE = {
    "ul": 5,
    "l": 15,
    "h": 60
}


"""

class Keyword(Slide if slides else Scene):
    def construct(self):
        self.add(NumberPlane())
        keyword_overlay(self)
        slides_pause(self, 5)


class BezierSplineExample(Scene):
    def construct(self):
        p1 = np.array([0, 1, 0])
        p1b = p1 + [0, -0.5, 0]
        d1 = Dot(point=p1).set_color(BLUE)
        # l1 = Line(p1, p1b)
        p2 = np.array([-2, -1, 0])
        p2b = p2 + [0, 0.5, 0]
        d2 = Dot(point=p2).set_color(RED)
        # l2 = Line(p2b, p2)
        bezier = CubicBezier(p1, p1 + DOWN, p2 + UP, p2)
        self.play(
            LaggedStart(
                Create(d1),
                # Create(l1),
                Create(bezier),
                # Create(l2),
                Create(d2),
                lag_ratio=0.66
            ),
            run_time=2
        )
        xl_pause(self)
"""

class ShineTester(Scene):
    def construct(self):
        # line = Line(LEFT, UP, stroke_width=2, color=YELLOW)
        # line = VGroup(line, *add_shine(line, 10))
        # self.play(
        #     *[Create(shine) for shine in line],
        #     run_time=4
        # )
        #
        # circ = Circle(radius=2, color=BLUE, stroke_width=2).shift(DOWN).set_style(fill_opacity=0)
        # circ = VGroup(circ, *add_shine(circ, 10))
        # self.play(
        #     *[Create(shine) for shine in circ],
        #     run_time=4
        # )
        #
        # self.wait(1)
        # fade_out_all(self)

        plane = NumberPlane()
        graph = plane.plot(lambda x: x**2)
        self.add(plane)
        graph = VGroup(graph, *add_shine(graph, nlines=10))
        self.play(
            # Create(graph),
            DrawBorderThenFill(graph),
            run_time=2
        )
        self.wait(2)


class DrejeKnapTest(Scene):
    def construct(self):
        a_knap = DrejeKnap(range_min=-2, range_max=2, label="a", show_value=True, color=WHITE, accent_color=YELLOW)
        b_knap = DrejeKnap(range_min=-3, range_max=5, label="b", show_value=True, color=WHITE, accent_color=BLUE)
        a_tracker = a_knap.tracker
        b_tracker = b_knap.tracker
        a_knap.scale(1).to_edge(UL)
        b_knap.scale(1).next_to(a_knap, DOWN)
        self.add(a_knap, b_knap)

        slider = Slider(smin=-3, smax=5, label="b", color=BLUE).scale(1).to_edge(RIGHT)
        bb_tracker = slider.tracker
        self.add(slider)

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
        graph = always_redraw(lambda:
            plane.plot(lambda x: a_tracker.get_value() * x + b_tracker.get_value())
        )
        self.add(plane, graph)
        for i in range(10):
            self.play(
                a_tracker.animate.set_value(a_knap.get_max()),
                b_tracker.animate.set_value(b_knap.get_max()),
                bb_tracker.animate.set_value(b_knap.get_max()),
                run_time=5
            )
            self.play(
                a_tracker.animate.set_value(a_knap.get_min()),
                b_tracker.animate.set_value(b_knap.get_min()),
                bb_tracker.animate.set_value(b_knap.get_min())
            )


class BoxesTester(Scene):
    def construct(self):
        boxes = boxes_of_content(
            self,
            ["Titel", "Undertitel 1", "Ekstra"],
            [RED, BLUE, YELLOW]
        )
        for i, box in enumerate(boxes):
            if i == 0:
                self.play(Create(box))
            else:
                box.set_z_index(box.get_z_index() - 2)
                self.add(box)
                self.play(
                    box.animate.next_to(boxes[0], [LEFT, RIGHT][i%2])
                    # FadeIn(
                    #     box.next_to(boxes[0], [LEFT, RIGHT][i%2]), direction=[RIGHT, LEFT][i%2]
                    # )
                )
        self.wait(6)


class SheenDice(Scene):
    def construct(self):
        die = DieFace(5).set_sheen(-0.5, direction=DR)
        self.add(die)


class GridBackAndMobDrawer(Scene):
    def construct(self):
        t = Tex("HEJ").scale(5).set_z_index(5)
        brect = get_background_rect(t, stroke_colour=RED, stroke_width=2, fill_color=BLUE)
        self.add(t, brect)
        # draw_and_fade_in_mob(self, brect, run_time=1)
        # self.wait()
        # draw_and_fade_in_mob(self, t, run_time=1)
        trace_dot = Dot(brect.get_corner(UR), radius=0.0001)
        trace = TracedPath(trace_dot.get_center, stroke_color=brect.get_stroke_color(), dissipating_time=10)
        self.add(trace)
        self.play(
            DrawBorderThenFill(brect),
            run_time=0.5
        )


class TestTransparentBackground(Scene):
    def construct(self):
        self.wait()
        self.play(
            Write(
                MathTex(r"c = \pm\sqrt{a^2 + b^2}", color=BLACK)
            ),
            run_time=2
        )
        self.wait()


class TestBohrAtom(Scene):
    def construct(self):
        ECOL = GOLD_A
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY
        balmer_colors = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]

        atom = BohrAtom(
            e=7, p=10, n=12,
            # level=6,
            orbit_color=OCOL,
            electron_color=ECOL,
            proton_color=PCOL,
            neutron_color=NCOL,
            sheen_factor=-0.25,
            separate_nuclei=True
        ).scale(1)
        protons = atom.get_protons()
        print(protons)
        # protons.shift(2*RIGHT)
        neutrons = atom.get_neutrons()
        print(neutrons)
        # neutrons.shift(2*LEFT)
        electron = atom.get_electrons()
        orbitals = atom.get_orbitals().set_style(stroke_width=1.5)
        print([orb.radius for orb in orbitals])
        # electron.move_to(
        #     orbitals[1].point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        # )
        backup_electron = electron.copy()
        # self.play(
        #     FadeIn(atom)
        # )
        self.add(atom, protons, neutrons)
        self.wait()
        self.play(
            protons.animate.shift(2*RIGHT),
            neutrons.animate.shift(2*LEFT)
        )
        self.wait(5)


class TestBohrAtomOvergange(Scene):
    def construct(self):
        ECOL = GOLD_A
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY
        balmer_colors = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]

        atoms = VGroup(*[
            BohrAtom(
                e=e, p=p, n=n,
                # level=6,
                orbit_color=OCOL,
                electron_color=ECOL,
                proton_color=PCOL,
                neutron_color=NCOL,
                sheen_factor=-0.25,
                separate_nuclei=True
            ).scale(1) for e, p, n in zip(np.arange(1, 11, 1), np.arange(1, 11, 1), np.arange(1, 11, 1))
        ])
        self.play(
            Create(atoms[0])
        )
        self.wait(2/_FRAMERATE[q])
        for i, atom in enumerate(atoms[1:]):
            self.play(
                # TransformMatchingShapes(atoms[i], atom, transform_mismatches=False)
                FadeOut(atoms[i]),
                FadeIn(atom)
            )
            self.wait(2/_FRAMERATE[q])
        self.wait(5)


class TestTitelSkrivning(Scene):
    def construct(self):
        title = Tex("Dette er en test")
        play_title2(self, title)
        self.wait()


class TestVariabelZoomTykkelse(MovingCameraScene):
    def construct(self):
        lines = VGroup(*[
            Line(start=2*LEFT, end=2*RIGHT, stroke_width=0.5).shift(1/x*DOWN) for x in [1, 2, 3, 4, 5, 6]
        ])
        brace = always_redraw(lambda: VGroup(*[
                BraceBetweenPoints(
                    lines[i].get_end(), lines[1+i].get_end(), stroke_width=0.01*self.camera.frame.get_height(),
                    sharpness=1/(i+1), buff=0
                ) for i in range(len(lines) - 1)
            ])
        )
        brace_text = always_redraw(lambda: VGroup(*[
                DecimalNumber(
                    lines[i].get_end()[1] - lines[i+1].get_end()[1], num_decimal_places=4,
                    font_size=min(4.2*self.camera.frame.get_height(), 32)
                ).next_to(brace[i], RIGHT, buff=0.15) for i in range(len(lines) - 1)
            ])
        )
        self.add(lines, brace, brace_text)
        for b, t in zip(brace, brace_text):
            self.play(
                self.camera.frame.animate.set(height=1.5).move_to(VGroup(b, t)),
                run_time=4
            )
        # self.play(
        #     self.camera.frame.animate.set(height=2.5).move_to(brace[0]),
        #     run_time=4
        # )
        # self.play(
        #     self.camera.frame.animate.set(height=1.5).move_to(brace[0]),
        #     run_time=4
        # )











if __name__ == "__main__":
    cls = TestTitelSkrivning
    class_name = cls.__name__
    # transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
