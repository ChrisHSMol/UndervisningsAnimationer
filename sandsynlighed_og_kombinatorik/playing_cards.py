import os

from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

slides = False
if slides:
    from manim_slides import Slide

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


class Kortspil(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.setup_playing_cards()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def setup_playing_cards(self):
        cards = VGroup()
        names = []
        base_dir = "../SVGs/playing_cards/"
        for card in os.listdir(base_dir):
            cards.add(
                SVGMobject(base_dir + card)
            )
            names.append(card.split(".")[0])
        # cards.arrange_in_grid(cols=13).scale(0.25)
        # self.add(cards)
        print(names)
        self.add(cards[0])
        self.slide_pause(0.5)
        for i, card in enumerate(cards[1:]):
            self.remove(cards[i])
            self.add(card)
            self.slide_pause(0.5)


if __name__ == "__main__":
    classes = [
        Kortspil
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)
