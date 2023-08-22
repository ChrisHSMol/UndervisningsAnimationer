from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class HistSum(Slide, MovingCameraScene if slides else MovingCameraScene):
    def construct(self):
        self.histogram()
        self.sumkurve()
        self.slide_pause()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_distributed_numbers(self, size, distribution):
        if not isinstance(distribution, (list, tuple, np.ndarray)):
            raise Exception(f"distribution must be of type list")
        results = []
        for num in np.random.uniform(size=size):
            for i, lim in enumerate(distribution):
                if num < lim:
                    results.append(i + 1)
                    break
        return results

    def get_axhlines(self, plane):
        axhlines = VGroup()
        xmax = plane.axes[0].get_tick_range()[-1]
        for tick in plane.axes[1].get_tick_range():
            axhlines.add(
                DashedLine(
                    start=plane.c2p(0, tick),
                    end=plane.c2p(xmax, tick),
                    stroke_width=0.25
                )
            )
        return axhlines

    def histogram(self):
        c1, c2, c3 = "#003f5c", "#bc5090", "#ffa600"
        np.random.seed(42)
        xmin, xmax = 0, 10
        size = 1000
        # data = np.random.random(size) * (xmax - xmin)
        data = np.random.exponential(2, size)
        # data = [max(0.9*d - 0.9, 0) for d in data]

        nbins = 5
        binsize = (xmax - xmin) / nbins

        plane = Axes(
            x_range=[xmin, xmax, binsize],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=4.5,
            tips=False
        ).scale(1.25).add_coordinates().to_edge(DL).set_z_index(5)
        axhlines = self.get_axhlines(plane)
        self.play(
            DrawBorderThenFill(plane),
            Create(axhlines)
        )
        bkgrect = get_background_rect(plane, fill_opacity=1).next_to(plane, DOWN, buff=-0.5)
        self.add(bkgrect)

        rects = VGroup()
        texts = VGroup()
        freqs = []
        endpoints = np.arange(xmin, xmax, binsize) + binsize
        for i, end in enumerate(endpoints):
            freq = len([d for d in data if end - binsize < d <= end]) / size

            c = three_way_interpolate(c1, c2, c3, i, nbins-1)
            hist_rect = Rectangle(
                width=plane.c2p(binsize, 0)[0] - plane.c2p(0, 0)[0],
                height=plane.c2p(0, freq)[1] - plane.c2p(0, 0)[1],
                stroke_width=0.1,
                stroke_color=c,
                fill_color=c,
                fill_opacity=1
            ).move_to(plane.c2p(end-0.5*binsize, -freq))
            hist_text = MathTex(fr"{freq*100:.2f}\%", color=c).next_to(hist_rect, UP, buff=-0.5)
            rects.add(hist_rect)
            freqs.append(freq)
            texts.add(hist_text)

        self.add(rects)
        for hist_rect, hist_text, end, freq in zip(rects, texts, endpoints, freqs):
            self.play(
                LaggedStart(
                    hist_rect.animate.move_to(
                        plane.c2p(end - 0.5 * binsize, 0.5 * freq)
                    ),
                    hist_text.animate.move_to(
                        plane.c2p(end - 0.5 * binsize, freq + 0.075)
                    ),
                    lag_ratio=0.25,
                ),
                run_time=1.5
            )
        # self.play(
        #     *[LaggedStart(
        #         r.animate.move_to(
        #             plane.c2p(end - 0.5*binsize, 0.5*freq)
        #         ),
        #         t.animate.move_to(
        #             plane.c2p(end - 0.5*binsize, freq + 0.075)
        #         ),
        #         lag_ratio=0.25
        #     ) for r, t, end, freq in zip(rects, texts, endpoints, freqs)],
        #     run_time=2
        # )
        self.slide_pause()

        self.play(
            # *[FadeOut(m) for m in self.mobjects if m not in [plane, axhlines, *rects]]
            *[FadeOut(m) for m in [bkgrect, texts]]
        )
        self.remove(plane, axhlines, *rects)

    def sumkurve(self):
        c1, c2, c3 = "#003f5c", "#bc5090", "#ffa600"
        np.random.seed(42)
        xmin, xmax = 0, 10
        size = 1000
        # data = np.random.random(size) * (xmax - xmin)
        # data = [max((d + 2)/2 - 4, 0) for d in data]
        # data = np.exp(-np.random.random(size)) * (xmax - xmin)
        # print(data)
        data = np.random.exponential(2, size)

        nbins = 5
        binsize = (xmax - xmin) / nbins

        plane = Axes(
            x_range=[xmin, xmax, binsize],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=4.5,
            tips=False
        ).scale(1.25).add_coordinates().to_edge(DL).set_z_index(5)
        axhlines = self.get_axhlines(plane)
        # self.play(
        #     DrawBorderThenFill(plane),
        #     Create(axhlines)
        # )
        bkgrect = get_background_rect(plane, fill_opacity=0.85).next_to(plane, DOWN, buff=-0.5)
        self.add(plane, axhlines, bkgrect)

        rects = VGroup()
        lines = VGroup()
        freqs = []
        endpoints = np.arange(xmin, xmax, binsize) + binsize
        for i, end in enumerate(endpoints):
            hist_rect = VGroup()
            for j in range(i + 1):
                c = three_way_interpolate(c1, c2, c3, j, nbins - 1)
                freqj = len([d for d in data if endpoints[j] - binsize < d <= endpoints[j]]) / size
                hist_rect.add(
                    Rectangle(
                        width=plane.c2p(binsize, 0)[0] - plane.c2p(0, 0)[0],
                        height=plane.c2p(0, freqj)[1] - plane.c2p(0, 0)[1],
                        stroke_width=0.1,
                        stroke_color=c,
                        fill_color=c,
                        fill_opacity=1 if j == i else 0.25
                    )
                )
            freq = len([d for d in data if 0 < d <= end]) / size
            # hist_rect.arrange(UP, buff=0).move_to(plane.c2p(end-0.5*binsize, -freq))
            hist_rect.arrange(UP, buff=0).move_to(plane.c2p(end-0.5*binsize, -0.5*freq + freqj))
            rects.add(hist_rect)
            freqs.append(freq)

            lines.add(Line(
                start=lines[i - 1].get_end() if i > 0 else plane.c2p(0, 0),
                end=plane.c2p(end, freq),
                color=three_way_interpolate(c1, c2, c3, i, nbins - 1),
                stroke_width=5,
                z_index=6
            ))

        # self.add(rects)
        # for hist_rect, end, freq in zip(rects, endpoints, freqs):
        #     self.play(
        #         hist_rect.animate.move_to(
        #             plane.c2p(end-0.5*binsize, 0.5*freq)
        #         ),
        #         run_time=1.5
        #     )
        self.play(
            *[
                h.animate.move_to(
                    plane.c2p(end-0.5*binsize, 0.5*freq)
                ) for h, end, freq in zip(rects, endpoints, freqs)
            ]
        )
        self.remove(rects)
        self.slide_pause()

        # self.play(
        #     rects.animate.set_opacity(0.25)
        # )
        for line, rect in zip(lines, rects):
            self.play(
                ReplacementTransform(rect[-1].copy(), line),
                rect.animate.set_opacity(0.25),
                run_time=1
            )
            self.slide_pause()

        self.play(
            FadeOut(rects)
        )

