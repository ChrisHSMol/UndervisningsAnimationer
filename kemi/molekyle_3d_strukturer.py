from manim import *
from manim_chemistry import *
import sys
sys.path.append("../")
from helpers import *

slides = False
if slides:
    from manim_slides import *


class MolekyleLoader(ThreeDScene):
    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def set_background_color(self, color):
        self.camera.background_color = color

    def read_mol_file(self, filename):
        structure = {}
        with open(filename, "r") as inFile:
            for line in inFile:
                line = line.split()
                if len(line[0]) <= 4:
                    structure[line[0]] = [float(l) for l in line[1:]]
        return structure

    def create_atom(self, atom_label, atom_coordinates):
        # scene_marker("Creating an atom")
        atom_colors = {
            "H": WHITE,
            "C": BLACK,
            "O": RED,
            "N": BLUE,
        }
        _atom_label = ""
        for c in atom_label:
            try:
                int(c)
            except:
                _atom_label += c

        atom = Dot3D(
            point=atom_coordinates,
            radius=0.16,
            color=atom_colors[_atom_label],
            # fill_opacity=0.95,
            sheen_factor=1
        )
        return atom

    def create_all_atoms(self, mol_structure):
        scene_marker("Creating all atoms")
        molecule = VGroup()
        for label, coord in mol_structure.items():
            molecule.add(self.create_atom(atom_label=label, atom_coordinates=coord))
        return molecule

    def create_bonds_between_atoms(self, atoms, distance_threshold):
        scene_marker("Creating the bonds")
        bonds = VGroup()
        for i, atom1 in enumerate(atoms):
            for j, atom2 in enumerate(atoms[:i]):
                interatomic_distance = np.linalg.norm(atom2.get_center() - atom1.get_center())
                if interatomic_distance <= distance_threshold:
                    bonds.add(
                        Line3D(
                            start=atom1.get_center(),
                            end=atom2.get_center(),
                            thickness=0.02,
                            color=WHITE
                        )
                    )
                else:
                    print(i, j, interatomic_distance)
        return bonds

    def create_molecule(self, mol_structure, distance_threshold=1.5):
        scene_marker("Creating the molecule")
        atoms = self.create_all_atoms(mol_structure)
        bonds = self.create_bonds_between_atoms(atoms, distance_threshold)
        return VGroup(atoms, bonds)


class Histidine(MolekyleLoader):
    def construct(self):
        self.set_background_color(LIGHT_GRAY)
        structure = self.read_mol_file(filename="mol_filer/histidine.txt")
        # molecule = self.create_all_atoms(structure)
        molecule = self.create_molecule(structure)
        self.add(molecule)
        self.begin_ambient_camera_rotation(about="phi", rate=1)
        self.wait(10)
        self.stop_ambient_camera_rotation()


# class Histidine(MolekyleLoader):
#     def construct(self):
#         struktur = self.read_mol_file("mol_filer/histidine.txt")
#         histidine = ThreeDMolecule(atoms_dict=struktur)
#         histidine = ThreeDMolecule.from_mol_file("mol_filer/histidine.txt", source_csv="../Elements_DK.csv")
#         self.add(histidine)
