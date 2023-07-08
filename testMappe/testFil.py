from manim import *
import sys
sys.path.append("../")
from helpers import *
from manim_slides import Slide


class Test(Slide):
    def construct(self):
        self.play(
            Create(Circle())
        )
        slides_pause(self, 1, True)
        self.play(
            Create(Square())
        )
        slides_pause(self, 1, True)
