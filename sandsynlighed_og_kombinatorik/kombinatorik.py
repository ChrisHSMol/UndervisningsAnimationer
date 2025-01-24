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


class Fakultet(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.faktultet()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def make_object(self, color, radius=0.5):
        return Circle(radius=radius, stroke_color=color, fill_color=color, fill_opacity=1)

    def switch_places(self, mob1, mob2, angle=TAU/3, lr=0.0):
        targets = [mob1.get_center(), mob2.get_center()]
        self.play(
            LaggedStart(
                LaggedStart(
                    MoveAlongPath(
                        mob1, ArcBetweenPoints(targets[0], targets[1], angle=angle)
                    ),
                ),
                LaggedStart(
                    MoveAlongPath(
                        mob2, ArcBetweenPoints(targets[1], targets[0], angle=angle)
                    ),
                ),
                lag_ratio=lr
            )
        )
        return VGroup(mob2, mob1)

    def _switch_places(self, mob1, mob2, angle=TAU/3, lr_individual=0.75, lr_group=0.0):
        if len(mob1) == 1:
            mob1 = VGroup(mob1)
        if len(mob2) == 1:
            mob2 = VGroup(mob2)
        self.play(
            LaggedStart(
                LaggedStart(
                    *[
                        MoveAlongPath(
                            m1, ArcBetweenPoints(m1.get_center(), m2.get_center(), angle=angle)
                        ) for m1, m2 in zip(mob1, mob2)
                    ],
                    lag_ratio=lr_individual
                ),
                LaggedStart(
                    *[
                        MoveAlongPath(
                            m2, ArcBetweenPoints(m2.get_center(), m1.get_center(), angle=angle)
                        ) for m1, m2 in zip(mob1, mob2)
                    ],
                    lag_ratio=lr_individual
                ),
                lag_ratio=lr_group
            )
        )

    def _fact(self, n):
        f = 1
        for i in range(1, n+1):
            f *= i
        return f

    def faktultet(self):
        _c = [RED, BLUE, GREEN, YELLOW, PINK]
        two_objects = VGroup(
            *[
                VGroup(
                    *[self.make_object(c) for c in _c[:2]]
                ).arrange(RIGHT) for _ in range(self._fact(2))
            ]
        )
        self.add(two_objects)

        self.play(
            two_objects.animate.arrange(DOWN)
        )
        self.slide_pause()

        two_objects[1] = self.switch_places(*two_objects[1])
        self.slide_pause()

        three_objects = two_objects.copy()
        self.remove(two_objects)
        self.add(three_objects)

        [ob.add(self.make_object(_c[2]).next_to(ob, RIGHT)) for ob in three_objects]
        self.play(
            *[
                FadeIn(ob[-1], shift=RIGHT) for ob in three_objects
            ]
        )
        self.slide_pause()

        [three_objects.add(ob).arrange(DOWN, aligned_edge=LEFT) for ob in two_objects]
        self.play(
            *[
                FadeIn(ob, shift=DOWN) for ob in three_objects[-2:]
            ]
        )
        self.slide_pause()

        [ob.add(self.make_object(_c[2]).move_to(ob[-1])) for ob in three_objects[-2:]]
        self.play(
            *[
                FadeIn(ob[-1]) for ob in three_objects[-2:]
            ],
            *[
                ob[1].animate.shift((ob[1].get_center() - ob[0].get_center()) * RIGHT) for ob in three_objects[-2:]
            ]
        )
        self.slide_pause()

        # self.play(
        #     FadeOut(two_objects_copy),
        #     FadeOut(two_objects)
        # )
        #
        # three_objects = VGroup(
        #     *[
        #         Circle(radius=0.5, stroke_color=c, fill_color=c, fill_opacity=1) for c in _c[:3]
        #     ]
        # ).arrange(RIGHT)
        # three_objects_copy = VGroup(*[
        #     three_objects.copy() for _ in range(self._fact(len(three_objects)) - 1)
        # ])
        # self.play(
        #     FadeIn(three_objects_copy),
        #     FadeIn(three_objects)
        # )
        # self.slide_pause()
        #
        # self.play(
        #     VGroup(
        #         three_objects,
        #         *three_objects_copy
        #     ).animate.arrange(DOWN)
        # )
        # self.switch_places(
        #     [three_objects_copy[0][0], three_objects_copy[1][1], three_objects_copy[2][1], three_objects_copy[3][0], three_objects_copy[4][0]],
        #     [three_objects_copy[0][1], three_objects_copy[1][2], three_objects_copy[2][2], three_objects_copy[3][2], three_objects_copy[4][2]],
        # )
        # self.switch_places(
        #     [three_objects_copy[2][0], three_objects_copy[4][0]],
        #     [three_objects_copy[2][1], three_objects_copy[4][1]],
        # )
        # self.slide_pause()
        #
        # self.play(
        #     *[
        #         LaggedStart(
        #             *[
        #                 c.animate.set_style(fill_opacity=0.25) for c in row if c.get_color() == _c[2]
        #             ],
        #             lag_ratio=0
        #         ) for row in VGroup(three_objects, *three_objects_copy)
        #     ]
        # )


class KombinationerOgPermutationer(Fakultet):
    def construct(self):
        self.kombinationer()
        self.slide_pause(5)

    def kombinationer(self):
        pass


if __name__ == "__main__":
    classes = [
        Fakultet,
        # KombinationerOgPermutationer
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
