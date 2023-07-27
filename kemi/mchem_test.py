from manim import *
from manim_chemistry import *


class BohrDiagram(Scene):
    def construct(self):
        atom = BohrAtom(
            e=1, p=1, n=0,
            level=6
            # orbit_color=YELLOW
        ).scale(0.5)
        electrons = atom.get_electrons()
        nuclei = atom.get_nuclei()
        orbitals = atom.get_orbitals().set_style(stroke_width=1)
        moving_electron = electrons[0][0]
        # photon = Dot(color=YELLOW).scale(0.5).move_to([-12, 6, 0])
        photon = Dot(color=YELLOW).scale(0.5).to_edge(UL, buff=-1)

        trace = TracedPath(photon.get_start, stroke_color=YELLOW, dissipating_time=0.5)
        self.add(photon, trace)

        self.add_mobjects_from_animations
        self.play(
            FadeIn(atom),
            run_time=3
        )
        self.play(
            # MoveAlongPath(moving_electron, orbitals[0])
            Rotate(moving_electron, PI/2, about_point=atom.get_center())
        )
        # self.play(
        #     Rotate(electrons, -0.1),
        #     run_time=0.5
        # )
        # self.play(
        #     Rotate(electrons, 4*PI+0.1),
        #     run_time=7,
        #     rate_func=rate_functions.ease_in_out_sine
        # )
        #
        # self.wait(0.5)
        #
        # self.play(
        #     Indicate(nuclei)
        # )
        #
        # self.wait()
        #
        # self.play(
        #     Rotate(electrons, -0.1),
        #     run_time=0.5
        # )
        # self.play(
        #     Rotate(electrons, 8*PI+0.1),
        #     run_time=14,
        #     rate_func=rate_functions.ease_in_out_sine
        # )
        #
        # self.wait(2)

        # self.play(
        #     photon.animate.move_to(moving_electron.get_center())
        # )
        # self.play(
        #     Flash(moving_electron),
        #     Indicate(moving_electron),
        #     FadeOut(photon)
        # )
        # self.play(
        #     moving_electron.animate.shift((orbitals[1].radius-orbitals[0].radius) * UP)
        # )
        # self.remove(trace)
        self.absorption(moving_electron, to_orbital=orbitals[1])
        self.wait()

        self.excitation(moving_electron, to_orbital=orbitals[0])

        # photon.move_to(moving_electron.get_center())
        # self.play(
        #     Flash(moving_electron),
        #     Indicate(moving_electron),
        #     FadeIn(photon)
        # )
        #
        # new_trace = TracedPath(photon.get_start, stroke_color=YELLOW, dissipating_time=0.5)
        # self.add(new_trace)
        # self.play(
        #     # photon.animate.move_to([10, 6, 0]),
        #     photon.animate.to_edge(UR, buff=-1),
        #     moving_electron.animate.shift(DOWN)
        # )

        self.wait(5)

        self.absorption(moving_electron, orbitals[1], None)
        for morb, color in zip(orbitals[2:], ["#7e00db", "#3800ff", "#00fff5", "#ff0000"]):
            self.absorption(moving_electron, morb, color)
            self.excitation(moving_electron, orbitals[1], color)

    def absorption(self, electron, to_orbital, photon_color=YELLOW):
        target_dot = electron.copy().move_to(
            to_orbital.point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        photon = Dot(color=photon_color).scale(0.5).to_edge(UL, buff=-1)
        trace = TracedPath(photon.get_start, stroke_color=photon_color, dissipating_time=0.5)
        self.add(photon, trace)

        self.play(
            photon.animate.move_to(electron.get_center())
        )
        self.play(
            Flash(electron, color=photon_color),
            Indicate(electron, color=photon_color),
            FadeOut(photon)
        )
        self.play(
            electron.animate.become(target_dot)
        )
        self.remove(trace)
        # return electron

    def excitation(self, electron, to_orbital, photon_color=YELLOW):
        target_dot = electron.copy().move_to(
            to_orbital.point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        photon = Dot(color=photon_color).scale(0.5).move_to(electron.get_center())
        trace = TracedPath(photon.get_start, stroke_color=photon_color, dissipating_time=0.5)
        self.add(photon, trace)

        self.play(
            Flash(electron, color=photon_color),
            Indicate(electron, color=photon_color),
            FadeIn(photon)
        )
        self.play(
            photon.animate.to_edge(UR, buff=-1),
            electron.animate.become(target_dot)
        )
        self.remove(trace)


class AbsorptionsSpektrum(Scene):
    def construct(self):
        atom = BohrAtom(
            e=1, p=1, n=0,
            level=6
        )
        orbitals = atom.get_orbitals().set_style(stroke_width=1)
        electron = atom.get_electrons()[0][0]
        electron.rotate(PI/2, about_point=ORIGIN).shift(UP)
        # self.add(atom)
        atoms = VGroup(*[atom.copy().scale(0.25) for _ in range(4)]).arrange(RIGHT)
        electrons = VGroup(*[a.get_electrons()[0][0] for a in atoms])
        self.add(atoms)

        wavelengths = np.linspace(400, 650, 26)
        colors = [
            "#8300b5", "#7e00db", "#6a00ff", "#3800ff", "#000bff", "#004cff", "#007fff",  # 400nm - 460nm
            "#00aeff", "#00daff", "#00fff5", "#00ff87", "#09ff00", "#3aff00", "#5aff00",  # 470nm - 530nm
            "#81ff00", "#a3ff00", "#c3ff00", "#e1ff00", "#ffff00", "#ffdf00", "#ffbe00",  # 540nm - 600nm
            "#ff9b00", "#ff7700", "#ff4b00", "#ff1b00", "#ff0000"  # 610nm - 650nm
        ]

        rainbow = VGroup(
            *[
                Line(start=8*LEFT, end=8*RIGHT, stroke_width=2, color=color) for color in colors
            ]
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1).shift(16*LEFT)
        self.add(rainbow)

        self.play(
            rainbow.animate.shift(PI*RIGHT),
            rate_func=rate_functions.linear,
            run_time=PI
        )
        self.remove(rainbow)
        self.add(rainbow[1])
        rainbow_2 = VGroup(*[r.copy() for r in rainbow if not r == rainbow[1]])
        self.play(
            electrons[0].animate.shift(0.25*UP),
            rainbow_2.animate.shift((atoms[1].get_center() - atoms[0].get_center())[0]*RIGHT),
            rate_func=rate_functions.linear,
            run_time=(atoms[1].get_center() - atoms[0].get_center())[0]
        )
        self.remove(rainbow_2)
        self.add(rainbow_2[2])
        rainbow_3 = VGroup(*[r.copy() for r in rainbow_2 if not r == rainbow_2[2]])
        self.play(
            electrons[1].animate.shift(0.5*UP),
            rainbow_3.animate.shift((atoms[2].get_center() - atoms[1].get_center())[0]*RIGHT),
            rate_func=rate_functions.linear,
            run_time=(atoms[2].get_center() - atoms[1].get_center())[0]
        )
        self.remove(rainbow_3)
        self.add(rainbow_3[7])
        rainbow_4 = VGroup(*[r.copy() for r in rainbow_3 if not r == rainbow_3[7]])
        self.play(
            electrons[2].animate.shift(0.75*UP),
            rainbow_4.animate.shift((atoms[3].get_center() - atoms[2].get_center())[0]*RIGHT),
            rate_func=rate_functions.linear,
            run_time=(atoms[3].get_center() - atoms[2].get_center())[0]
        )
        self.remove(rainbow_4)
        self.add(rainbow_4[-1])
        rainbow_5 = VGroup(*[r.copy() for r in rainbow_4 if not r == rainbow_4[-1]])
        self.play(
            electrons[3].animate.shift(1.0*UP),
            rainbow_5.animate.shift(PI*RIGHT),
            rate_func=rate_functions.linear,
            run_time=PI
        )

