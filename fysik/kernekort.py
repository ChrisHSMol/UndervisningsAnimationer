import sys

import numpy as np

sys.path.append("../")
from manim import *
from manim_chemistry import *
from helpers import *
import random
import subprocess

slides = False
# if slides:
#     from manim_slides import Slide


class KerneKort(MovingCameraScene if not slides else Slide):
    def construct(self):
        nuklider = self.prepare_nuclides()
        self.load_kerne_labels(nuklider=nuklider)

        # self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def prepare_nuclides(self):
        # nuklider = np.genfromtxt("nuclides.csv", delimiter=";", dtype=str)
        # # print(nuklider)
        # loc_dict = {}
        # for i, line in enumerate(nuklider):
        #     s = line[1]
        #     while True:
        #         try:
        #             _ = int(s[0])
        #             s = s[1:]
        #         except:
        #             break
        #         # s = s[1:]
        #     A, Z, N = int(line[2]), int(line[3]), int(line[4])
        #     loc_dict[f"{s}-{A}"] = [N, Z]
        # # for k, v in loc_dict.items():
        # #     print(k, v)
        # return loc_dict
        _nuks = np.genfromtxt("grundstof_Z.csv", delimiter=";", dtype=str)
        _nuk_dict = {}
        for nuk in _nuks:
            _nuk_dict[int(nuk[0])] = [nuk[2], nuk[1]]
        # print(_nuk_dict)
        nuklider = np.genfromtxt("complete_nuclides.csv", delimiter=";", dtype=str, skip_header=True)
        # print(nuklider)
        loc_dict = {}
        rad_colors = {}
        for i, line in enumerate(nuklider):
            # if i == 200:
            #     break
            A, Z, N = int(line[0]), int(line[1]), int(line[2])
            s = _nuk_dict[Z][0] if Z > 0 else "n"
            elem_name = _nuk_dict[Z][1] if Z > 0 else "neutron"
            rad_type = line[3]
            for i, _s in enumerate(rad_type):
                if _s not in "QWERTYUIOPASDFGHJKLZXCVBNM-+":
                    rad_type = rad_type[:i]
                    break
                else:
                    continue
            if not rad_type in rad_colors.keys():
                rad_colors[rad_type] = random_bright_color()
            loc_dict[f"{s}-{A}"] = [N, Z, elem_name, rad_type, rad_colors[rad_type]]
        # for k, v in loc_dict.items():
        #     print(k, v)
        return loc_dict

    def _nuklid_label(self, label, N, Z, fill_color, fill_opacity=1.0):
        _label = VGroup(
            Square(side_length=1, fill_color=fill_color, fill_opacity=fill_opacity),
            # MathTex(f"^{N+Z}_{Z}{label}")
            VGroup(
                VGroup(
                    # Integer(N+Z).set_stroke(BLACK), Integer(Z).set_stroke(BLACK)
                    MathTex(str(N+Z)).set_stroke(width=0.5, color=BLACK),
                    MathTex(str(Z)).set_stroke(width=0.5, color=BLACK)
                ).scale(0.5).arrange(DOWN, aligned_edge=RIGHT, buff=0.1),
                Tex(label).set_stroke(width=0.5, color=BLACK)
            ).arrange(RIGHT, buff=0.1)
        )
        return _label

    def load_kerne_labels(self, nuklider):
        # kernelabels = VGroup(*[
        #     MElementObject(
        #         atomic_number=nuklider[iso][1], atomic_mass=iso.split("-")[1], element_symbol=iso.split("-")[0],
        #         element_name=str(nuklider[iso][2]), fill_colors=(WHITE, nuklider[iso][4])
        #     ).set(height=1, width=1).move_to([nuklider[iso][0], nuklider[iso][1], 0]) for iso in list(nuklider.keys())[:100]
        # ])
        kernelabels = VGroup(*[
            self._nuklid_label(
                label=key.split("-")[0], N=val[0], Z=val[1], fill_color=val[4]
            ).move_to([val[0], val[1], 0]) for key, val in nuklider.items()
        ])
        self.add(kernelabels)
        self.camera.frame.set(
            width=kernelabels.width * 1.25, height=kernelabels.height * 1.25
        ).move_to(kernelabels)
        self.slide_pause()


if __name__ == "__main__":
    cls = KerneKort
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)