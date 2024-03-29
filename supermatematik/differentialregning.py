from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

# slides = True
# if slides:
#     from manim_slides import Slide

q = "l"
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


class DifferentialRegning(Scene):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def construct(self):
        # _cols = {"e^": RED, "\\ln": RED, "n": RED}
        _cols = {}
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{amsmath}")
        # myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        regneregler = VGroup(
            Tex("Potensreglen: "),
            MathTex("f(x) = x^n", substrings_to_isolate="n").set_color_by_tex_to_color_map(_cols),
            MathTex(r"\rightarrow"),
            MathTex("f\'(x) = nx^{n-1}", substrings_to_isolate="n").set_color_by_tex_to_color_map(_cols),
            Tex("Eksponentreglen: "),
            MathTex("f(x) = \\mathrm{e}^x", tex_template=myTemplate, substrings_to_isolate="e^").set_color_by_tex_to_color_map(_cols),
            MathTex(r"\rightarrow"),
            MathTex("f\'(x) = \\mathrm{e}^x", tex_template=myTemplate, substrings_to_isolate="e^").set_color_by_tex_to_color_map(_cols),
            Tex("Logaritmereglen: "),
            MathTex("f(x) = \\ln(x)}", tex_template=myTemplate, substrings_to_isolate="\\ln").set_color_by_tex_to_color_map(_cols),
            MathTex(r"\rightarrow"),
            MathTex("f\'(x) = {1 \\over x}"),
            Tex("Nævnerreglen: "),
            MathTex("f(x) = {1 \\over x^n}", substrings_to_isolate="n").set_color_by_tex_to_color_map(_cols),
            MathTex(r"\rightarrow"),
            MathTex("f\'(x) = {-n \\over x^{n+1}}", substrings_to_isolate="n").set_color_by_tex_to_color_map(_cols),
        ).arrange_in_grid(4, 4, col_alignments="rlll", buff=0.5)
        self.add(regneregler[:4])
        self.wait(10)


if __name__ == "__main__":
    cls = DifferentialRegning
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
        # command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
