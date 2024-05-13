import sys

import numpy as np

sys.path.append("../")
from manim import *
# from manim_chemistry import *
from helpers import *
import random
import subprocess

slides = False
# if slides:
#     from manim_slides import Slide

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


class KerneKort(MovingCameraScene if not slides else Slide):
    def scale_factor(self):
        return 1/20

    def construct(self):
        nuklider = self.prepare_nuclides()
        kernekort = self.load_kerne_labels(nuklider=nuklider, N_range=(0, 160), Z_range=(0, 100))

        # self.play(
        #     self.camera.frame.animate.move_to(random.choice(kernekort)).set_width(10),
        #     run_time=1
        # )
        self.slide_pause()

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
        rad_colors = {"A": YELLOW, "B-": ORANGE, "B+": BLUE_B, "SF": GREEN, "IS": BLACK, "EC": TEAL, "n": RED, "p": PURE_BLUE}
        # rad_colors = {}
        for i, line in enumerate(nuklider):
            # if i == 200:
            #     break
            A, Z, N = int(line[0]), int(line[1]), int(line[2])
            s = _nuk_dict[Z][0] if Z > 0 else "n"
            elem_name = _nuk_dict[Z][1] if Z > 0 else "neutron"
            rad_type = line[3]
            _scounter = 0
            for i, _s in enumerate(rad_type):
                try:
                    _s = int(_s)
                    rad_type = rad_type[1:]
                    _scounter += 1
                    # print(rad_type)
                except:
                    if _s in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm-+":
                        continue
                    # elif not _sbreak:
                    #     rad_type = rad_type[1:]
                    else:
                        rad_type = rad_type[:i-_scounter]
                        break
            if rad_type not in rad_colors.keys():
                print(elem_name, A, rad_type)
                rad_colors[rad_type] = random_bright_color()
            loc_dict[f"{s}-{A}"] = [N, Z, elem_name, rad_type, rad_colors[rad_type]]
        # print(rad_colors.keys())
        # for k, v in loc_dict.items():
        #     print(k, v)
        return loc_dict

    def _nuklid_label(self, label, N, Z, fill_color, fill_opacity=1.0, N_range=None, Z_range=None, width=1):
        # print(f"{label}-{N+Z} \t {N} \t {Z}")
        if N_range is None:
            N_range = [0, 160]
        if Z_range is None:
            Z_range = [0, 100]

        _label = VGroup()
        if N < N_range[0] or N > N_range[1] or Z < Z_range[0] or Z > Z_range[1]:
            # print(N, Z)
            pass
        else:
            _label.add(
                Square(side_length=1, fill_color=fill_color, fill_opacity=fill_opacity, stroke_width=width),
                # MathTex(f"^{N+Z}_{Z}{label}")
                VGroup(
                    VGroup(
                        # Integer(N+Z).set_stroke(BLACK), Integer(Z).set_stroke(BLACK)
                        MathTex(str(N+Z)).set_stroke(width=0.5, color=BLACK),
                        MathTex(str(Z)).set_stroke(width=0.5, color=BLACK)
                    ).scale(0.5).arrange(DOWN, aligned_edge=RIGHT, buff=0.1),
                    Tex(label).set_stroke(width=0.5, color=BLACK)
                ).scale(0.9).arrange(RIGHT, buff=0.1).scale(2*width)
            )
        return _label

    def draw_axes(self):
        Nmin, Nmax = 0, 150
        Zmin, Zmax = 0, 120
        Nstep, Zstep = (Nmax - Nmin)//20, (Zmax - Zmin)//12
        scale_factor = self.scale_factor()
        # plane = NumberPlane(
        plane = Axes(
            x_range=(Nmin-1, Nmax, Nstep),
            y_range=(Zmin-1, Zmax, Zstep),
            x_length=(Nmax - Nmin)*scale_factor,
            y_length=(Zmax - Zmin)*scale_factor,
            tips=False,
            # background_line_style={
            #     "stroke_color": WHITE,
            #     "stroke_width": 3,
            #     "stroke_opacity": 1,
            #     # "stroke_opacity": 0.1
            # },
            axis_config={"include_numbers": True, "font_size": 288*scale_factor}
        ).set_z_index(4)
        # srec = get_background_rect(plane, stroke_colour=WHITE, stroke_width=3, buff=0)
        srec = Rectangle(width=Nmax-Nmin, height=Zmax-Zmin, stroke_width=3, stroke_color=WHITE).next_to(
            plane[0], UP, buff=0
        )
        # self.add(plane)
        return srec, plane

    def get_axlines(self, plane, x_range, y_range, xstep, ystep):
        axhlines = VGroup()
        axvlines = VGroup()
        xmax = x_range[1]
        ymax = y_range[1]
        for hline, vline in zip(np.arange(y_range[0], y_range[1], ystep), np.arange(x_range[0], x_range[1], xstep)):
            print(hline, vline)
            axhlines.add(DashedLine(
                start=plane.c2p(0, hline),
                end=plane.c2p(xmax, hline),
                stroke_width=2
            ).set_z_index(5))
            axvlines.add(DashedLine(
                start=plane.c2p(vline, 0),
                end=plane.c2p(vline, ymax),
                stroke_width=2
            ).set_z_index(5))
        return axhlines, axvlines

    def load_kerne_labels(self, nuklider, N_range=(0, 160), Z_range=(0, 100), overlap=20):
        scene_marker("Laver kort")
        plane_rect, plane = self.draw_axes()
        axhlines, axvlines = self.get_axlines(plane, N_range, Z_range, 10, 10)
        self.add(plane, plane_rect, axhlines, axvlines)
        self.slide_pause()
        # kernekort = VGroup()
        # for key, val in nuklider.items():
        #     # iZ = val[1] // (Z_range[1]/len(kernekort))
        #     # iN = val[0] // len(kernekort)
        #     if N_range[0] <= val[0] <= N_range[1] and Z_range[0] <= val[1] <= Z_range[1]:
        #         kernelabel = self._nuklid_label(
        #             label=key.split("-")[0], N=val[0], Z=val[1], fill_color=val[4], N_range=N_range, Z_range=Z_range
        #         ).move_to(plane.c2p(val[0], val[1], 0))

        kernekort = VGroup(*[VGroup() for _ in range(5)])
        _prevZ, _prevN, iK = 0, 0, 0
        for iZ, iN in zip(
                np.arange(0, Z_range[1] + 1, Z_range[1]//len(kernekort)),
                np.arange(0, N_range[1] + 1, N_range[1]//len(kernekort))
        ):
            print(iK)
            if iZ == 0:
                _prevZ = iZ
                _prevN = iN
                continue
            _Z = [_prevZ - overlap, iZ + overlap]
            _N = [_prevN - overlap, iN + overlap]
            print(_Z, _N)
            for key, val in nuklider.items():
                if not _N[0] <= val[0] <= _N[1] and not _Z[0] <= val[1] <= _Z[1]:
                    continue
                else:
                    kernelabel = self._nuklid_label(
                        label=key.split("-")[0], N=val[0], Z=val[1], fill_color=val[4], N_range=_N, Z_range=_Z,
                        width=self.scale_factor()
                    ).move_to(plane.c2p(val[0], val[1], 0))
                    kernekort[iK].add(kernelabel)
            iK += 1
            _prevZ = iZ
            _prevN = iN

        scene_marker("Add to scene")
        self.add(kernekort[0])
        # self.camera.frame.set(
        #     # width=kernekort.width * 1.25, height=kernekort.height * 1.25
        #     width=plane.width * 1.25, height=plane.height * 1.25
        # # ).move_to(kernekort)
        # ).move_to(plane)
        scene_marker("Vent")
        self.slide_pause(1/_FRAMERATE[q])
        for kk in kernekort[1:]:
            self.add(kk)
            self.slide_pause(1/_FRAMERATE[q])
        return kernekort


if __name__ == "__main__":
    cls = KerneKort
    class_name = cls.__name__
    # transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]} --disable_caching"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
