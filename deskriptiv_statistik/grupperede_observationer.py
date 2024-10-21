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


class GrupperingAfData(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        title = Tex("")
        play_title2(self, title)
        self.gruppering_af_data()
        # print(np.arange(0, 10, 2))

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def data_to_DecNum(self, data, numdec=0, bsign=False):
        return VGroup(
            *[DecimalNumber(
                    val,
                    include_sign=bsign,
                    num_decimal_places=numdec,
                ).scale(0.5) for val in data]
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)

    def one_to_one_sort(self, data, desc=True):
        _numbers = [d.get_value() for d in data]
        _numbers.sort(reverse=desc)
        sorted_data = self.data_to_DecNum(_numbers).next_to(data, RIGHT, buff=2)

        num_of_each_value = {}
        dict_sorting = {}
        for i, d in enumerate(data):
            strVal = str(d.get_value())

            if strVal not in num_of_each_value.keys():
                num_of_each_value[strVal] = 0

            dict_sorting[d] = [
                s for s in sorted_data if s.get_value() == d.get_value()
            ][num_of_each_value[strVal]]

            num_of_each_value[strVal] += 1
        return sorted_data, dict_sorting

    def inddel_i_grupper(
            self,
            data: list[float],
            start: float = 0.0,
            end: float = 10.0,
            size: float = 2.0
    ):
        grupperinger = {}
        interval_starts = np.arange(start, end, size)
        interval_ends = interval_starts + size
        # print(interval_starts)
        for st, en in zip(interval_starts, interval_ends):
            label = f"[{st}; {en}["
            hyps = len(
                [x for x in data if st <= x.get_value() < en]
            )
            grupperinger[label] = hyps
        # print(grupperinger)
        return grupperinger

    def prepare_table(
            self,
            data: list[float],
            cell_width: float = 1.5,
            cell_height: float = 0.65,
            include_header_row: bool = False,
            include_label_column: bool = False,
            include_coloured_inlay: bool = True,
            numdecs: list[int] = None,
    ):
        if numdecs is None:
            numdecs = [0, 0]
        row_offset = int(include_header_row)
        col_offset = int(include_label_column)
        different_numbers = np.unique(data)
        num_different_numbers = len(different_numbers)

        tabel_struktur = VGroup()
        for j in range(num_different_numbers + row_offset):
            row = VGroup()
            for i in range(5 + col_offset):
                row.add(
                    VGroup(
                        Rectangle(width=cell_width, height=cell_height, stroke_width=1),
                        Rectangle(
                            width=cell_width - 0.05, height=cell_height - 0.05, fill_opacity=0,
                            stroke_width=3 if include_coloured_inlay else 0,
                            stroke_color=[*[BLACK for _ in range(1+col_offset)], BLUE, BLUE, YELLOW, YELLOW][i],
                            stroke_opacity=[*[0 for _ in range(1+col_offset)], 0.5, 0.75, 0.5, 0.75][i]
                        )
                    )
                )
            row.arrange(RIGHT, buff=0)
            tabel_struktur.add(row)
        tabel_struktur.arrange(DOWN, buff=0)
        # TODO: coloured inlay to each rect

        _tabel_raw = []
        _tabel = []
        kumhyp = 0
        kumfre = 0
        for i, obs in enumerate(different_numbers):
            hyp = len([d for d in data if d == obs])
            kumhyp += hyp
            fre = hyp/len(data)
            kumfre += fre
            _tabel_raw.append([obs, hyp, kumhyp, fre, kumfre])
            _tabel.append([
                str(obs), str(hyp), str(kumhyp), f"{fre*100:.{numdecs[0]}f} \\%", f"{kumfre*100:.{numdecs[1]}f} \\%"
            ])

        tabel_data_raw = np.array(_tabel_raw)
        tabel_data = VGroup(*[
            VGroup(*[
                MathTex(d, font_size=22).move_to(tabel_struktur[j+row_offset][i+col_offset]) for i, d in enumerate(row)
            ]) for j, row in enumerate(_tabel)
        ])
        return tabel_struktur, tabel_data, tabel_data_raw

    def gruppering_af_data(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=0.5)
        sorted_data, sorting_dict = self.one_to_one_sort(data, desc=False)
        grupperinger = self.inddel_i_grupper(data, start=0, end=20, size=2)

        self.play(
            LaggedStart(
                *[DrawBorderThenFill(d) for d in data],
                lag_ratio=0.1
            ),
            run_time=1
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[TransformFromCopy(k, v) for k, v in sorting_dict.items()],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause()

        intervaller = VGroup(
            *[
                VGroup(
                    MathTex(l), Integer(v)
                ).arrange(RIGHT) for l, v in grupperinger.items()
            ]
        ).arrange(DOWN).to_edge(RIGHT)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(m) for m in intervaller]
            )
        )
        self.slide_pause()


if __name__ == "__main__":
    classes = [
        GrupperingAfData
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
