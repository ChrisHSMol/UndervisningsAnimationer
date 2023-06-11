from manim import *
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class HistSum(Slide, MovingCameraScene if slides else MovingCameraScene):
    def construct(self):
        self.histogram()
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

    def histogram(self):
        c1, c2, c3 = "#003f5c", "#bc5090", "#ffa600"
        np.random.seed(42)
        xmin, xmax = 0, 10
        size = 100
        data = np.random.random(size) * (xmax - xmin)
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
        self.play(
            DrawBorderThenFill(plane)
        )
        bkgrect = get_background_rect(plane, fill_opacity=1).next_to(plane, DOWN, buff=-0.5)
        self.add(bkgrect)

        for i, end in enumerate(np.arange(xmin, xmax, binsize) + binsize):
            idata = [d for d in data if end - binsize < d <= end]
            freq = len(idata) / size

            c = interpolate_color(
                interpolate_color(c1, c2, min(i, 2)/2),
                interpolate_color(c2, c3, (max(i, 2)-2)/2),
                i/4
            )
            hist_rect = Rectangle(
                width=plane.c2p(binsize, 0)[0] - plane.c2p(0, 0)[0],
                height=plane.c2p(0, freq)[1] - plane.c2p(0, 0)[1],
                stroke_width=0.1,
                stroke_color=c,
                fill_color=c,
                fill_opacity=1
            ).move_to(plane.c2p(end-0.5*binsize, -freq))
            self.add(hist_rect)
            self.play(
                hist_rect.animate.move_to(
                    plane.c2p(end-0.5*binsize, 0.5*freq)
                ),
                run_time=1.5
            )
