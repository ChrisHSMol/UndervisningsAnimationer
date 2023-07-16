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

