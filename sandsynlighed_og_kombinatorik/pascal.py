from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *
from manim import config as global_config
config = global_config.copy()
config.background_color = WHITE

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

def _get_palette():
    hexes = ("#41436a", "#984063", "#f64668", "#fe9677")
    return [ManimColor.from_hex(h) for h in hexes]
config.background_color = WHITE


class PascalsTrekant(MovingCameraScene, Slide if slides else Scene):
    # _background_color = _get_palette()[0]
    config.background_color = WHITE
    # config["background_color"] = WHITE
    # CONFIG = {
    #     "camera_config": {"background_color": WHITE}
    # }
    def construct(self):
        palette = self.get_palette()
        self.setup_hexes()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def get_cmap(self):
        cmap = {
            "observation": BLUE
        }
        return cmap

    def get_palette(self):
        return _get_palette()

    def setup_hexes(self):
        palette = self.get_palette()
        # config.background_color = WHITE
        _font_size = 20
        _radius = 0.5
        base_hex = RegularPolygon(6, radius=_radius).rotate(PI/6).set(stroke_color=palette[1], stroke_width=1)
        nrows, ncols = 12, 17
        hex_grid = VGroup(*[
            VGroup(*[
                base_hex.copy().set_style(
                    stroke_color=palette[i%4], fill_color=palette[i%4]
                ) for _ in range(ncols + i%2)
            ]).arrange(RIGHT, buff=0.1*_radius) for i in range(nrows)
        ]).arrange(DOWN, buff=-_radius * np.sin(30*DEGREES) * 0.8)

        zeros = VGroup(*[
            VGroup(*[
                Integer(0, fill_opacity=0.5, stroke_opacity=0.5).move_to(cell) for cell in row
            ]) for row in hex_grid
        ])
        self.add(hex_grid)
        # self.add(zeros)
        # self.play(
        #     LaggedStart(
        #         *[
        #             LaggedStart(
        #                 *[DrawBorderThenFill(cell) for cell in row],
        #                 lag_ratio=0.05
        #             ) for row in hex_grid
        #         ],
        #         lag_ratio=0.05
        #     )
        # )
        #
        # self.play(
        #     LaggedStart(
        #         *[
        #             LaggedStart(
        #                 *[Write(z) for z in row],
        #                 lag_ratio=0.05
        #             ) for row in zeros
        #         ],
        #         lag_ratio=0.05
        #     )
        # )
        # self.slide_pause()

        row0, col0 = 2, ncols // 2
        new_vals = VGroup()
        # self.play(
        #     hex_grid[row0][col0].animate.set_style(fill_opacity=0.2),
        #     ReplacementTransform(zeros[row0][col0], new_vals[-1])
        # )
        # hex_grid[2][ncols // 2].set_style(fill_opacity=0.2)
        # self.remove(zeros[2][ncols // 2])
        # self.add(new_vals)
        self.slide_pause()

        self.camera.frame.save_state()
        new_hexes = VGroup()
        for i in range(10):
            n_cells = i + 1
            current_line = VGroup(Integer(1))
            if i == 0:
                current_line[0].move_to(hex_grid[row0][col0])
            else:
                current_line[0].move_to(hex_grid[row0 + i][col0 - i//2])

            if n_cells > 2:
                for j, offset in enumerate(np.arange(0, n_cells-2, 1)):
                    current_line.add(
                        Integer(new_vals[-1][j].get_value() + new_vals[-1][j+1].get_value())
                    )
                    current_line[-1].move_to(hex_grid[row0 + i][col0 + offset - (i-2)//2])
            if n_cells >= 2:
                current_line.add(Integer(1).move_to(hex_grid[row0 + i][col0 + (i+1)//2]))

            current_hexes = VGroup(
                *[
                    base_hex.copy().set_z_index(4).set_style(
                        fill_opacity=0.2, stroke_width=1.5, stroke_color=palette[(row0+i)%4], fill_color=palette[(row0+i)%4]
                    ).move_to(mob) for mob in current_line
                ]
            )
            current_line.set_z_index(5)
            new_vals.add(current_line)
            new_hexes.add(current_hexes)
            self.play(
                self.camera.frame.animate.set(
                    width=current_hexes.width + 2
                ).move_to(current_line)
            )
            self.play(
                FadeIn(new_vals[-1]),
                FadeIn(new_hexes[-1]),
                run_time=0.5
            )
            self.slide_pause()
        self.play(
            Restore(self.camera.frame)
        )
        # for row in hex_grid:
        #     row[col0].set_style(fill_opacity=1)

        # new_vals.add(VGroup(
        #     Integer(1).move_to(hex_grid[3][ncols // 2]),
        #     Integer(1).move_to(hex_grid[3][ncols // 2 + 1]),
        # ))
        # hex_grid[3][ncols // 2].set_style(fill_opacity=0.2)
        # hex_grid[3][ncols // 2 + 1].set_style(fill_opacity=0.2)
        # self.remove(zeros[3][ncols // 2], zeros[3][ncols // 2 + 1])
        # self.add(new_vals[-1])
        #
        # new_vals.add(VGroup(
        #     Integer(1).move_to(hex_grid[4][ncols // 2 - 1]),
        #     *[
        #         Integer(new_vals[-1][i].get_value() + new_vals[-1][i+1].get_value()).move_to(
        #             hex_grid[4][ncols // 2]
        #         ) for i in range(len(new_vals[-1]) - 1)
        #     ],
        #     Integer(1).move_to(hex_grid[4][ncols // 2 + 1]),
        # ))
        # hex_grid[4][ncols // 2 - 1].set_style(fill_opacity=0.2)
        # hex_grid[4][ncols // 2].set_style(fill_opacity=0.2)
        # hex_grid[4][ncols // 2 + 1].set_style(fill_opacity=0.2)
        # self.remove(zeros[4][ncols // 2], zeros[4][ncols // 2 + 1], zeros[4][ncols // 2 - 1])
        # self.add(new_vals[-1])
        #
        # new_vals.add(VGroup(
        #     Integer(1).move_to(hex_grid[5][ncols // 2 - 1]),
        #     *[
        #         Integer(new_vals[-1][i].get_value() + new_vals[-1][i+1].get_value()).move_to(
        #             hex_grid[5][ncols // 2 + i%2]
        #         ) for i in range(len(new_vals[-1]) - 1)
        #     ],
        #     Integer(1).move_to(hex_grid[5][ncols // 2 + 2]),
        # ))
        # hex_grid[5][ncols // 2 - 1].set_style(fill_opacity=0.2)
        # hex_grid[5][ncols // 2].set_style(fill_opacity=0.2)
        # hex_grid[5][ncols // 2 + 1].set_style(fill_opacity=0.2)
        # hex_grid[5][ncols // 2 + 2].set_style(fill_opacity=0.2)
        # self.remove(zeros[5][ncols // 2], zeros[5][ncols // 2 + 1], zeros[5][ncols // 2 - 1], zeros[5][ncols // 2 + 2])
        # self.add(new_vals[-1])


if __name__ == "__main__":
    classes = [
        PascalsTrekant
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        # if hasattr(cls, "_background_color"):
        #     command += rf" -c {cls._background_color}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name + "Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)
