from manim import *
import random
import numpy as np
import itertools as it
import sys
from collections.abc import Hashable, Iterable, Mapping, Sequence
from typing import TYPE_CHECKING, Callable, Literal

from PIL.Image import Image

# from manim import config
# from manim.constants import *
# from manim.mobject.mobject import Mobject
# from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
# from manim.mobject.opengl.opengl_mobject import OpenGLMobject
# from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
# from manim.mobject.three_d.three_d_utils import (
#     get_3d_vmob_gradient_start_and_end_points,
# )
# from manim.utils.bezier import (
#     bezier,
#     bezier_remap,
#     get_smooth_cubic_bezier_handle_points,
#     integer_interpolate,
#     interpolate,
#     partial_bezier_points,
#     proportions_along_bezier_curve_for_point,
# )
# from manim.utils.color import BLACK, WHITE, ManimColor, ParsableManimColor
# from manim.utils.iterables import (
#     make_even,
#     resize_array,
#     stretch_array_to_length,
#     tuplify,
# )
# from manim.utils.space_ops import rotate_vector, shoelace_direction

from typing import Any

import numpy.typing as npt
from manim.utils.color.X11 import VIOLET, CYAN1, BEIGE
from pandas.core.dtypes.inference import is_integer
from typing_extensions import Self

from manim.typing import (
    CubicBezierPath,
    CubicBezierPointsLike,
    CubicSpline,
    ManimFloat,
    MappingFunction,
    Point2DLike,
    Point3D,
    Point3D_Array,
    Point3DLike,
    Point3DLike_Array,
    RGBA_Array_Float,
    Vector3D,
    Zeros,
)


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
        # self.n_nucleons = self.p + self.n
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

    def calculate_arrangement_angles(self, n_electrons: int = 0):
        print(n_electrons)
        arrangement_angles = []
        if n_electrons <= 4:
            arrangement_angles.append([
                i * TAU / n_electrons for i in range(n_electrons)
            ])
        elif 4 < n_electrons <= 8:
            # arrangement_angles = [
            #     *[i * (TAU - 0) / 4 for i in range(4) if i >= n_electrons % 4],
            #     *[i * (TAU - 0) / 4 + 0.05 * PI for i in range(4) if i < n_electrons % 4],
            #     *[i * (TAU - 0) / 4 - 0.05 * PI for i in range(4) if i < n_electrons % 4],
            # ]
            arrangement_angles.append([0.05*PI, -0.05*PI])
            if n_electrons >= 6:
                arrangement_angles.append([1.05*PI, 0.95*PI])
            else:
                arrangement_angles.append([1.0*PI])
            if n_electrons >= 7:
                arrangement_angles.append([0.55*PI, 0.45*PI])
            else:
                arrangement_angles.append([0.5*PI])
            if n_electrons == 8:
                arrangement_angles.append([1.55*PI, 1.45*PI])
            else:
                arrangement_angles.append([1.5*PI])
        # elif n_electrons == 8:
        #     arrangement_angles = [
        #         *[i * (2*TAU - 0)/n_electrons + 0.05*PI for i in range(4)],
        #         *[i * (2*TAU - 0)/n_electrons - 0.05*PI for i in range(4)]
        #     ]
        # print(arrangement_angles)
        arrangement_angles = [x for xs in arrangement_angles for x in xs]  # Flatten list of lists to list
        # print(arrangement_angles)
        return arrangement_angles

    def orbitals_group(self):
        return VGroup(
            *[
                # Circle(radius=1 + i, color=self.orbit_color)
                Circle(radius=1 + i + self.n_nucleons()**0.1, color=self.orbit_color)
                # TODO: Find ud af, hvordan afstanden kan skrives til at være nogenlunde rigtig
                for i in range(self.occupied_levels)
            ]
        )

    def n_nucleons(self) -> int:
        return self.p + self.n

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
            # [proton.shift(np.random.uniform(-0.05, 0.05, 3) * self.n_nucleons()**0.5) for proton in protons]
            [proton.move_to(Circle(
                radius=np.random.uniform(0, 0.05)*self.n_nucleons()**0.5
            ).point_at_angle(np.random.uniform(0, 2*PI))) for proton in protons]
            [proton.set_z_index(2*z) for z, proton in enumerate(protons)]
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
            ) for _ in range(self.n)
        ])
        if self.n > 1:
            # [neutron.shift(np.random.uniform(-0.05, 0.05, 3) * self.n_nucleons()**0.5) for neutron in neutrons]
            [neutron.move_to(Circle(
                radius=np.random.uniform(0, 0.05)*self.n_nucleons()**0.5
            ).point_at_angle(np.random.uniform(0, 2*PI))) for neutron in neutrons]
            [neutron.set_z_index(2*z + 1) for z, neutron in enumerate(neutrons)]
        return neutrons

    def nuclei_groups(self) -> VGroup:#, protons: list, neutrons: list) -> VGroup:
        protons = self.protons_group()
        neutrons = self.neutrons_group()
        nuclei = VGroup(*protons, *neutrons)
        random.shuffle(nuclei)
        return VGroup(*nuclei)

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
                # group = self.arrange_electrons(level_electrons, level)
                group = self.arrange_electrons(
                    level_electrons, self.orbitals_group()[level-1].radius, use_orig_method=False
                )
            else:
                # group = self.arrange_electrons(remaining_electrons, level)
                group = self.arrange_electrons(
                    remaining_electrons, self.orbitals_group()[level-1].radius, use_orig_method=False
                )
                electrons_group.add(group)
                break

            remaining_electrons -= level_electrons
            electrons_group.add(group)

        return electrons_group

    def arrange_electrons(self, n_electrons, level, use_orig_method=True):
        level_group = VGroup()
        arrangement_angles = np.arange(0, TAU, TAU / n_electrons) if use_orig_method else self.calculate_arrangement_angles(n_electrons)
        # for angle in np.arange(0, TAU, TAU / n_electrons):
        for angle in self.calculate_arrangement_angles(n_electrons):
            print(f"Angle={angle}")
            electron = Dot(
                color=self.electron_color, sheen_factor=self.sheen_factor, sheen_direction=self.sheen_direction,
                stroke_width=1, stroke_color=BLACK
            ).scale(2)
            electron.shift(level * UP)
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


class Prikformel(VGroup):
    def __init__(
            self,
            atom_label: str = "H",
            number_of_valence_electrons: int = 1,
            label_color: ParsableManimColor | None = WHITE,
            unpaired_location: Vector3D = RIGHT,
            rotation: float = 0.0,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.atom_label = atom_label
        self.number_of_valence_electrons = number_of_valence_electrons
        self.label_color = label_color
        self.unpaired_location = unpaired_location
        self.rotation = rotation
        self.label_group = self.make_label_group()
        self.locations = self.calculate_electron_positions()
        self.electron_group = self.populate_electrons()
        self.add(self.make_label_group(), self.populate_electrons())

    def make_label_group(self, **kwargs):
        return Text(self.atom_label, color=self.label_color, **kwargs)

    def calculate_electron_positions(self):
        locations = []
        for direction in [
            (UP, LEFT), (RIGHT, UP), (DOWN, RIGHT), (LEFT, DOWN), (UP, RIGHT), (RIGHT, DOWN), (DOWN, LEFT), (LEFT, UP)
        ]:
            loc = self.label_group.get_edge_center(direction[0])
            loc += 0.2 * direction[0] + 0.15 * direction[1]
            locations.append(loc)
        return locations

    def _electron(self):
        return Circle(
            fill_color=self.label_color, stroke_color=self.label_color, fill_opacity=1, radius=0.05
        )

    def populate_electrons(self):
        electron_group = VGroup()
        for i_electron, loc in zip(range(self.number_of_valence_electrons), self.calculate_electron_positions()):
            electron = self._electron()
            electron.move_to(loc)
            electron.rotate(self.rotation, about_point=ORIGIN)
            electron_group.add(electron)
        return electron_group

    def get_electron_group(self):
        return self.electron_group

    def get_atomic_label(self):
        return self.atom_label


class Molecule2D(VGroup):
    def __init__(
            self,
            atoms_dict: dict,  # dict: {"element": [x, y, z, charge]}
            bonds_dict: dict | None = None,  # not implemented yet
            bond_length: float = 0.5,
            add_element_label: bool = True,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.atoms_dict = atoms_dict
        self.bonds_dict = bonds_dict
        self.bond_length = bond_length
        self.add_element_label = add_element_label
        self.color_dict = {
            "H": WHITE, "C": BLACK, "N": BLUE, "O": RED, "F": GREEN, "Cl": GREEN, "Br": RED_A, "I": VIOLET,
            "He": CYAN1, "Ne": CYAN1, "Ar": CYAN1, "Kr": CYAN1, "Xe": CYAN1, "Rn": CYAN1,
            "P": ORANGE, "S": YELLOW, "B": BEIGE, "Li": VIOLET, "Na": VIOLET, "K": VIOLET, "Rb": VIOLET, "Cs": VIOLET,
            "Fr": VIOLET, "Be": GREEN_A, "Mg": GREEN_A, "Ca": GREEN_A, "Sr": GREEN_A, "Ba": GREEN_A, "Ra": GREEN_A,
            "Ti": GREY, "Fe": ORANGE
        }
        self.add(self.create_atoms())

    def _base_atom(self, element, charge=0):
        atom_label = ""
        for c in element:
            try:
                int(c)
            except:
                atom_label += c
        atom = VGroup(
            Circle(
                radius=0.25, fill_color=self.color_dict[atom_label], fill_opacity=1, stroke_width=0,
                stroke_color=self.color_dict[atom_label]
            )
        )
        if self.add_element_label:
            # if charge != 0:
            #     charge = str(charge) if charge < 0 else f"+{charge}"
            if charge > 0:
                charge = (str(charge) if charge > 1 else "") + "+"
            elif charge < 0:
                charge = (str(np.abs(charge)) if charge < -1 else "") + "-"
            else:
                charge = ""
            atom.add(
                Tex(
                    f"{atom_label}$^{{{charge}}}$", color=BLACK if atom_label != "C" else WHITE
                ).scale(0.5 if not charge else 0.4)
            )
        return atom

    def create_atoms(self):
        atoms = VGroup()
        for atom, loc in self.atoms_dict.items():
            loc, charge = loc[:3], loc[3]
            # atoms[atom] = self._base_atom(atom).move_to(loc)
            atoms.add(self._base_atom(atom, charge=charge).move_to(loc))
        return atoms

    # def bind_atoms(self):
    #     bonds = VGroup()
    #     for atom, loc in self.atoms_dict.items():
    #         for receiver in self.atoms_dict[atom]:
    #             bonds.add(
    #                 Line(start=loc, end=receiver)
    #             )

