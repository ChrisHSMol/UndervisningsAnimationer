from manim import *
import random
import numpy as np


class Nuclid(VGroup):
    def __init__(
            self,
            nuclid_type="proton",
            nuclid_color=WHITE,
            sheen_factor=0.0,
            sheen_direction=UP,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.nuclid_type = nuclid_type
        self.nuclid_color = nuclid_color
        self.sheen_factor = sheen_factor
        self.sheen_direction = sheen_direction
        self.add(self.make_nuclid())

    def make_nuclid(self):
        nuclid = Dot(
            color=self.nuclid_color, sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction,
            stroke_width=1, stroke_color=BLACK
        ).scale(2)
        # super().__init__(nuclid)
        return nuclid

    def nuctype(self):
        return self[0]


class BohrAtom(VGroup):
    """
    Creates a Bohr like diagram
    """

    def __init__(
        self,
        e=14,  # Electrons
        p=14,  # Protons
        n=10,  # Neutrons
        level=None,  # Levels
        orbit_color=WHITE,
        electron_color=BLUE,
        proton_color=RED,
        neutron_color=WHITE,
        separate_nuclei=False,
        sheen_factor=-0.25,
        sheen_direction=DR,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.e = e
        self.p = p
        self.n = n
        self.level = level
        self.occupied_levels = self.calculate_levels()
        self.orbit_color = orbit_color
        self.electron_color = electron_color
        self.proton_color = proton_color
        self.neutron_color = neutron_color
        self.add(self.orbitals_group(), self.electrons_group(), self.nuclei_groups())
        # self.add(self.orbitals_group(), self.electrons_group(), self.protons_group(), self.neutrons_group())
        self.separate_nuclei = separate_nuclei
        self.sheen_factor = sheen_factor
        self.sheen_direction = sheen_direction
        self.TOTAL_ELECTRONS_PER_LEVEL = {
            # Electrons that fit in total: Level
            2: 1,
            10: 2,
            28: 3,
            60: 4,
            110: 5,
            182: 6,
        }

    def calculate_levels(self):
        TOTAL_ELECTRONS_PER_LEVEL = {
            # Electrons that fit in total: Level
            2: 1,
            10: 2,
            28: 3,
            60: 4,
            110: 5,
            182: 6,
        }
        if self.level:
            return self.level

        return TOTAL_ELECTRONS_PER_LEVEL[
            next(x for x in list(TOTAL_ELECTRONS_PER_LEVEL.keys()) if x >= self.e)
        ]

    def orbitals_group(self):
        return VGroup(
            *[
                Circle(radius=1 + i, color=self.orbit_color)
                for i in range(self.occupied_levels)
            ]
        )

    def protons_group(self) -> VGroup:
        # protons = VGroup(*[
        #     Dot(
        #         color=self.proton_color, sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction,
        #         stroke_width=1, stroke_color=BLACK
        #     ).scale(2).shift(np.random.uniform(-0.25, 0.25, 3)) for _ in range(self.p)
        # ])
        protons = VGroup(*[
            Nuclid(
                nuclid_type="proton", nuclid_color=self.proton_color,
                sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction
            ) for _ in range(self.p)
        ])
        if self.p > 1:
            [proton.shift(np.random.uniform(-0.25, 0.25, 3)) for proton in protons]
        # print(protons[0].nuclid_color, type(protons[0].nuclid_color), self.proton_color, type(self.proton_color))
        return protons

    def neutrons_group(self) -> VGroup:
        # neutrons = VGroup(*[
        #     Dot(
        #         color=self.neutron_color, sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction,
        #         stroke_width=1, stroke_color=BLACK
        #     ).scale(2).shift(np.random.uniform(-0.25, 0.25, 3)) for _ in range(self.n)
        # ])
        neutrons = VGroup(*[
            Nuclid(
                nuclid_type="neutron", nuclid_color=self.neutron_color,
                sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction
            ).shift(np.random.uniform(-0.25, 0.25, 3)) for _ in range(self.n)
        ])
        return neutrons

    def nuclei_groups(self) -> VGroup:#, protons: list, neutrons: list) -> VGroup:
        protons = self.protons_group()
        neutrons = self.neutrons_group()
        nuclei = VGroup(*protons, *neutrons)
        random.shuffle(nuclei)
        return VGroup(*nuclei)

    # def _nuclei_groups(self):
    #     protons = [
    #         Dot(color=self.proton_color)
    #         .scale(2)
    #         .shift(np.random.uniform(-0.25, 0.25, 3))
    #         for i in range(self.p)
    #     ]
    #     neutrons = [
    #         Dot(color=self.neutron_color)
    #         .scale(2)
    #         .shift(np.random.uniform(-0.25, 0.25, 3))
    #         for i in range(self.n)
    #     ]
    #     nuclei = protons + neutrons
    #     random.shuffle(nuclei)
    #
    #     return VGroup(*nuclei)

    def electrons_group(self):
        ELECTRONS_PER_LEVEL = {
            # Level: Electrons that fit in each level
            1: 2,
            2: 8,
            3: 18,
            4: 32,
            5: 50,
            6: 72,
        }
        level = self.calculate_levels()
        remaining_electrons = self.e
        electrons_group = VGroup()
        for level in ELECTRONS_PER_LEVEL:
            level_electrons = ELECTRONS_PER_LEVEL[level]
            if remaining_electrons > level_electrons:
                group = self.arrange_electrons(level_electrons, level)
            else:
                group = self.arrange_electrons(remaining_electrons, level)
                electrons_group.add(group)
                break

            remaining_electrons -= level_electrons
            electrons_group.add(group)

        return electrons_group

    def arrange_electrons(self, n_electrons, level):
        level_group = VGroup()
        for angle in np.arange(0, TAU, TAU / n_electrons):
            electron = Dot(
                color=self.electron_color, sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction,
                stroke_width=1, stroke_color=BLACK
            ).scale(2)
            electron.shift(level * RIGHT)
            electron.rotate(angle, about_point=[0, 0, 0])
            level_group.add(electron)

        return level_group

    def get_orbitals(self):
        return self[0]

    def get_electrons(self):
        return self[1]

    # def get_nuclei(self):
    #     return self[2]

    def get_protons(self):
        # return self[2]
        protons = VGroup(*[
            # nuc for nuc in self.get_nuclei() if rgb_to_hex(color_to_rgb(nuc.get_fill_color())) == self.proton_color
            nuc for nuc in self.get_nuclei() if nuc.nuclid_color == self.proton_color
            # nuc for nuc in self.get_nuclei() if nuc.nuctype() == "proton"
        ])
        return protons

    def get_neutrons(self):
        # return self[3]
        neutrons = VGroup(*[
            # nuc for nuc in self.get_nuclei() if rgb_to_hex(color_to_rgb(nuc.get_fill_color())) == self.neutron_color
            nuc for nuc in self.get_nuclei() if nuc.nuclid_color == self.neutron_color
            # nuc for nuc in self.get_nuclei() if nuc.nuctype() == "neutron"
        ])
        return neutrons

    def get_nuclei(self):
        # return self[2].add(self[3])
        return self[2]
