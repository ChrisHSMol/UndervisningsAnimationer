import math
import random

from manim import *
import sys
import scipy

sys.path.append("../../")
sys.path.append("../../../")
import subprocess
from helpers import *
from custom_classes import *

slides = True
if slides:
    from manim_slides import Slide

q = "h"
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
_ONEFRAME = 1/_FRAMERATE[q]


class BjerrumDiagram(MovingCameraScene, Slide if slides else Scene):
    def _bkg_col(self):
        return DARKER_GRAY

    def construct(self):
        self.camera.background_color = self._bkg_col()
        title = Tex(r"Bjerrumdiagrammer").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        self.ligninger_og_udtryk()
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_cmap(self):
        cmap = {
            "V_base": PINK,
            "pH": GREEN,
            "xS": YELLOW,
            "korr_syre": RED,
            "korr_base": BLUE
        }
        # B31F11
        # 7D0A32
        # 8132B8
        return cmap

    def calc_pH(self, pKs, xS):
        return pKs + np.log10( (1-xS) / xS)

    def bjerrum_sigmoid(self, x, x0, k):
        return 1 - 1 / (1 + np.exp(-k * (x - x0)))

    def ligninger_og_udtryk(self):
        cmap = self.get_cmap()
        # pH = pKs + log([B]/[S])
        # x_S = [S] / ([S] + [B])
        # pH = pKs + log( (1-x_S) / x_S )
        c_form_syre = 1.00 # M
        V_syre = 0.025 # L

        c_form_base = 1.00 # M
        V_drop = 5.0e-5 # L -- middelvolumen af vanddråbe
        if not slides:
            V_drop = V_drop * 10

        n_eq = 1 # Antal ækvivalenspunkter - protonisering af syren

        # print(int(2*V_syre/V_drop))
        V_total = []
        c_akt_syre = []
        c_akt_base = []
        x_S_list = []
        for n_drops in range(int(n_eq*V_syre/V_drop)):
            totalV = V_syre + n_drops*V_drop
            cSyre = (c_form_syre*V_syre - n_drops*V_drop*c_form_base) / totalV
            cBase = c_form_base*n_drops*V_drop / totalV
            if cSyre*V_syre/totalV <= 0:
                break
            V_total.append(totalV)
            c_akt_syre.append(cSyre)
            c_akt_base.append(cBase)
            x_S_list.append(cSyre*V_syre/totalV)

        for i in range(5):
            print(V_total[i], c_akt_syre[i], c_akt_base[i], x_S_list[i])
        print(V_total[-1], c_akt_syre[-1], c_akt_base[-1], x_S_list[-1])

        reaktionsskema = Tex(
            r"CH$_3$COOH", " (aq)", " + ", r"H$_2$O", " (l)", r" $\rightarrow$ ",
            r"CH$_3$COO$^-$", " (aq)", " + ", r"H$_3$O$^+$", " (aq)"
        ).scale(0.8)
        reaktionsskema[0].set_color(cmap["korr_syre"])
        reaktionsskema[6].set_color(cmap["korr_base"])
        # self.add(reaktionsskema)
        self.play(
            Write(reaktionsskema),
            run_time=2
        )
        self.slide_pause()

        self.play(
            reaktionsskema.animate.to_edge(UP)
        )
        # self.slide_pause()

        pKs = 4.76
        # xS_list = [1-1e-3*i for i in range(1000)]
        # pH_list = [self.calc_pH(pKs, xS) for xS in xS_list]
        xS_list = x_S_list[1:]
        pH_list = [self.calc_pH(pKs, xs) for xs in xS_list]
        print(xS_list[:3], pH_list[:3])
        x_start, x_slut, dx, eps = 0, 14, 1, 1e-6
        y_start, y_slut, dy = 0, 1, 0.1
        plane = NumberPlane(
            x_range=(x_start, x_slut+eps, dx),
            y_range=(y_start, y_slut+eps, dy),
            x_length=10,
            y_length=6,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ).to_edge(LEFT, buff=1)
        axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
            for lab, c, coord in zip(
                [r"\text{pH}", r"x_S"], [cmap["pH"], cmap["xS"]], [(x_slut*1.05, 0), (0, y_slut*1.05)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, dy/10), end=plane.c2p(x, -dy/10), color=WHITE, stroke_width=1.5
            ) for x in np.arange(x_start, x_slut+eps, dx)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(dx/10, y), end=plane.c2p(-dx/10, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(y_start, y_slut+eps, dy)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0, color=cmap["pH"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(x_start, x_slut+eps, dx), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=cmap["xS"], font_size=24 if np.abs(y) > eps else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(y_start, y_slut+eps, dy), tickmarks["y"])]),
        }
        dots = VGroup(
            *[
                Dot(
                    # fill_color=three_way_interpolate(cmap["korr_base"], WHITE, cmap["korr_syre"], y, 1)
                    fill_color=three_way_interpolate(WHITE, cmap["korr_syre"], cmap["korr_syre"], y-0.5, 0.5) if y >= 0.5 else three_way_interpolate(cmap["korr_base"], cmap["korr_base"], WHITE, y, 0.5)
                ).scale(0.5).move_to(plane.c2p(x, y)) for x, y in zip(
                    pH_list, xS_list
                )
            ]
        )
        # self.add(plane, axis_labels, *ticks.values(), *tickmarks.values())
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                *[Create(t) for t in tickmarks.values()],
                *[Write(t) for t in ticks.values()],
                Write(axis_labels),
                lag_ratio=0.25
            )
        )
        self.slide_pause(5*_ONEFRAME)

        tekst_felt = Rectangle(
            width=8, height=3, fill_color=self._bkg_col(), fill_opacity=0.75, stroke_width=0
        ).set_z_index(10).next_to(reaktionsskema, DOWN, aligned_edge=RIGHT).shift(2*RIGHT)
        V_tilsat_tekst = VGroup(
            Tex("V tilsat NaOH: "),
            DecimalNumber((V_total[0]-V_syre)*1000, num_decimal_places=2, unit=r"~\text{mL}")
        ).set_z_index(11).arrange(RIGHT).next_to(tekst_felt, UP, aligned_edge=LEFT, buff=-0.5)
        pH_tekst = VGroup(
            Tex("pH: ", color=cmap["pH"]),
            DecimalNumber(pH_list[0], num_decimal_places=3, color=cmap["pH"])
        ).set_z_index(11).arrange(RIGHT).next_to(V_tilsat_tekst, DOWN, aligned_edge=LEFT, buff=0.5)
        xS_tekst = VGroup(
            Tex(r"Syrebrøken: $x_S = \frac{[S]}{[S]+[B]} = $", color=cmap["xS"]),
            DecimalNumber(xS_list[0], num_decimal_places=4, color=cmap["xS"])
        ).scale(0.9).set_z_index(11).arrange(RIGHT).next_to(pH_tekst, DOWN, aligned_edge=LEFT, buff=0.5)

        self.play(
            FadeIn(
                VGroup(tekst_felt, V_tilsat_tekst, pH_tekst, xS_tekst), shift=LEFT
            ),
            FadeIn(dots[0].scale(3))
        )
        self.slide_pause()

        # self.add(tekst_felt, V_tilsat_tekst, pH_tekst, xS_tekst)
        # self.add(dots)
        # self.add(dots[0].scale(3))

        for i in [1, 2, 3, 4, 5]:
            self.play(
                dots[i-1].animate.scale(1/3),
                ReplacementTransform(dots[i-1].copy(), dots[i].scale(3)),
                V_tilsat_tekst[1].animate.set_value((V_total[i]-V_syre)*1000).set_z_index(11),
                pH_tekst[1].animate.set_value(pH_list[i]).set_z_index(11),
                xS_tekst[1].animate.set_value(xS_list[i]).set_z_index(11)
            )
            self.slide_pause()

        for i in np.arange(6, len(pH_list), 1):
            i = int(i)
            self.play(
                dots[i-1].animate.scale(1/3),
                ReplacementTransform(dots[i-1].copy(), dots[i].scale(3)),
                V_tilsat_tekst[1].animate.set_value((V_total[i]-V_syre)*1000).set_z_index(11),
                pH_tekst[1].animate.set_value(pH_list[i]).set_z_index(11),
                xS_tekst[1].animate.set_value(xS_list[i]).set_z_index(11),
                run_time=5*_ONEFRAME
            )
            self.wait(_ONEFRAME)
        self.play(
            dots[i].animate.scale(1/3),
            run_time=0.25
        )
        self.slide_pause()

        _bjerrum_x = np.linspace(1, 13, 10)
        _bjerrum_y = [1/(1+10**(pH-pKs)) for pH in _bjerrum_x]
        popt, pcov = scipy.optimize.curve_fit(self.bjerrum_sigmoid, _bjerrum_x, _bjerrum_y)

        bjerrum_graph = plane.plot(
            lambda x: self.bjerrum_sigmoid(x, *popt),
            stroke_color=color_gradient((BLUE, RED), 2)
        )
        inv_bjerrum_graph = plane.plot(
            lambda x: 1
        )
        # self.add(bjerrum_graph)
        self.play(
            Create(bjerrum_graph),
            *[FadeOut(m) for m in (dots, tekst_felt, pH_tekst, xS_tekst, V_tilsat_tekst)]
        )
        self.slide_pause()

        korr_par = VGroup(
            Tex(
                r"CH$_3$COOH", color=cmap["korr_syre"]
            ).rotate(-80*DEGREES).move_to(plane.c2p(4, 0.5)).set_z_index(plane.get_z_index() + 3),
            Tex(
                r"CH$_3$COO$^-$", color=cmap["korr_base"]
            ).rotate(-80*DEGREES).move_to(plane.c2p(5.5, 0.5)).set_z_index(plane.get_z_index() + 3)
        )
        areas = VGroup(
            plane.get_riemann_rectangles(
                bjerrum_graph, x_range=(x_start, x_slut), dx=0.05, color=cmap["korr_syre"], fill_opacity=0.25, stroke_width=0
            ),
            plane.get_riemann_rectangles(
                inv_bjerrum_graph, bounded_graph=bjerrum_graph,
                x_range=(x_start, x_slut), dx=0.05, color=cmap["korr_base"], fill_opacity=0.25, stroke_width=0
            )
        )
        # self.add(korr_par)
        self.play(
            ReplacementTransform(reaktionsskema[0].copy(), korr_par[0]),
            ReplacementTransform(reaktionsskema[6].copy(), korr_par[1]),
            FadeIn(areas)
        )
        self.slide_pause()

        afl_lines = VGroup(
            DashedLine(
                start=plane.c2p(0, 0.5), end=plane.c2p(pKs, 0.5), stroke_color=cmap["xS"]
            ).set_z_index(plane.get_z_index() + 2),
            DashedLine(
                start=plane.c2p(pKs, 0.5), end=plane.c2p(pKs, 0), stroke_color=cmap["pH"]
            ).set_z_index(plane.get_z_index() + 2)
        )
        self.play(
            Create(afl_lines[0]),
            run_time=1.5
        )
        self.slide_pause()
        self.play(
            Create(afl_lines[1]),
            run_time=1.5
        )
        self.slide_pause()

        pKs_tekst = Tex(
            r"{{pH}}-værdien, når {{$x_S=0.5$}},\\aflæses som pKs-værdien"
        ).next_to(xS_tekst, DOWN, aligned_edge=RIGHT, buff=1).set_z_index(plane.get_z_index() + 3)
        pKs_tekst[0].set_color(cmap["pH"])
        pKs_tekst[2].set_color(cmap["xS"])
        pKs_bkg = get_background_rect(pKs_tekst, fill_color=self._bkg_col(), fill_opacity=0.75)
        pKs_marker = tickmarks["x"][0].copy().scale(3).move_to(plane.c2p(pKs, 0)).set_color(cmap["pH"])
        pKs_value = VGroup(
            Tex("pKs = ", color=cmap["pH"]),
            DecimalNumber(pKs, num_decimal_places=2, color=cmap["pH"])
        ).arrange(RIGHT).next_to(pKs_marker, DOWN, buff=0.25)
        # self.add(pKs_tekst, pKs_marker, pKs_value, pKs_bkg)
        self.play(
            LaggedStart(
                ReplacementTransform(afl_lines[1].copy(), pKs_marker),
                FadeIn(pKs_value),
                lag_ratio=0.25
            ),
            FadeIn(
                VGroup(pKs_bkg, pKs_tekst), shift=LEFT
            )
        )
        self.slide_pause()

        self.play(
            *[
                FadeOut(m) for m in (
                    plane, axis_labels, *ticks.values(), *tickmarks.values(), korr_par, bjerrum_graph, afl_lines,
                    pKs_marker, pKs_tekst, pKs_bkg, areas
                )
            ],
            reaktionsskema.animate.move_to(ORIGIN + 0.5*UP),
            pKs_value.animate.move_to(ORIGIN + 0.5*DOWN)
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in (reaktionsskema, pKs_value)]
        )


class Titrerkurve(BjerrumDiagram):
    def construct(self):
        self.camera.background_color = self._bkg_col()
        # title = Tex(r"Bjerrumdiagrammer").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.titrering()
        self.wait(5)

    def calc_tit_pH(self, pKs, cS, cB):
        return pKs + np.log10(cB/cS)

    def titrering(self):
        cmap = self.get_cmap()
        # pH = pKs + log([B]/[S])
        # x_S = [S] / ([S] + [B])
        # pH = pKs + log( (1-x_S) / x_S )
        c_form_syre = 1.00 # M
        V_syre = 0.025 # L
        pKs = 4.76

        c_form_base = 1.00 # M
        V_drop = 5.0e-5 # L -- middelvolumen af vanddråbe
        if not slides:
            V_drop = V_drop * 10

        n_eq = 2 # Antal ækvivalenspunkter - protonisering af syren

        # print(int(2*V_syre/V_drop))
        V_added = []
        V_total = []
        c_akt_syre = []
        c_akt_base = []
        pH_list = []
        for n_drops in range(int(n_eq * (V_syre * c_form_syre) / (V_drop * c_form_base))):
            addedV = n_drops*V_drop
            totalV = V_syre
            cSyre = (c_form_syre*V_syre - n_drops*V_drop*c_form_base) / totalV
            cBase = c_form_base*n_drops*V_drop / totalV

            # print(addedV * c_form_base, V_syre * c_form_syre)
            if addedV*c_form_base < V_syre*c_form_syre:
                print(f"a: {addedV * c_form_base:.5f}    {V_syre * c_form_syre:.3f}")
                pH_list.append(self.calc_tit_pH(pKs, cSyre, cBase))
            elif np.abs(addedV*c_form_base - V_syre*c_form_syre) <= 1e-5:
                print(f"b: {addedV * c_form_base:.5f}    {V_syre * c_form_syre:.3f}")
                pH_list.append(
                    -np.log10( 1.0e-14 / ( (1+np.sqrt(1-4*(1/5.71e-10)*(-c_form_syre*V_syre/totalV)))/(2*(1/5.71e-10)) ) )
                )
            else:
                print(f"c: {addedV * c_form_base:.5f}    {V_syre * c_form_syre:.3f}")
                pH_list.append(
                    -np.log10( 1.0e-14 / ((addedV*c_form_base - V_syre*c_form_syre)/totalV) )
                )

            # if cSyre*V_syre/totalV <= 0:
            #     print(addedV*c_form_base, V_syre*c_form_syre)
            #     if np.abs(addedV*c_form_base - V_syre*c_form_syre) <= 1e-6:
            #         pH_list.append(7.0)
            #     else:
            #         pH_list.append(-np.log10( 1.0e-14 * totalV / (addedV*c_form_base - V_syre*c_form_syre) ))
            # else:
            #     pH_list.append(self.calc_tit_pH(pKs, cSyre, cBase))
            V_added.append(addedV)
            V_total.append(totalV)
            c_akt_syre.append(cSyre)
            c_akt_base.append(cBase)

        for i in range(5):
            print(V_total[i], c_akt_syre[i], c_akt_base[i], pH_list[i], V_added[i])
        print(V_total[-1], c_akt_syre[-1], c_akt_base[-1], pH_list[-1], V_added[-1])

        reaktionsskema = Tex(
            r"CH$_3$COOH", " (aq)", " + ", r"OH$^-$", " (aq)", r" $\rightarrow$ ",
            r"CH$_3$COO$^-$", " (aq)", " + ", r"H$_2$O", " (l)"
        ).scale(0.8)
        reaktionsskema[0].set_color(cmap["korr_syre"])
        reaktionsskema[6].set_color(cmap["korr_base"])
        # self.add(reaktionsskema)
        # self.play(
        #     Write(reaktionsskema),
        #     run_time=2
        # )
        # self.slide_pause()
        #
        # self.play(
        #     reaktionsskema.animate.to_edge(UP)
        # )
        # self.slide_pause()

        # xS_list = [1-1e-3*i for i in range(1000)]
        # pH_list = [self.calc_pH(pKs, xS) for xS in xS_list]
        x_list = V_added
        y_list = pH_list
        print(x_list[:3], y_list[:3])
        x_start, x_slut, dx, eps = 0, 50, 5, 1e-6
        y_start, y_slut, dy = 0, 14, 1
        plane = NumberPlane(
            x_range=(x_start, x_slut+eps, dx),
            y_range=(y_start, y_slut+eps, dy),
            x_length=10,
            y_length=6,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ).to_edge(LEFT, buff=1)
        axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
            for lab, c, coord in zip(
                [r"V(NaOH)~\text{mL}", r"\text{pH}"], [cmap["V_base"], cmap["pH"]], [(x_slut*1.15, 0), (0, y_slut*1.05)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, dy/10), end=plane.c2p(x, -dy/10), color=WHITE, stroke_width=1.5
            ) for x in np.arange(x_start, x_slut+eps, dx)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(dx/10, y), end=plane.c2p(-dx/10, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(y_start, y_slut+eps, dy)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0, color=cmap["V_base"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(x_start, x_slut+eps, dx), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=0, include_sign=y < 0, color=cmap["pH"], font_size=24 if np.abs(y) > eps else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(y_start, y_slut+eps, dy), tickmarks["y"])]),
        }
        dots = VGroup(
            *[
                Dot().scale(0.5).move_to(plane.c2p(x*1000, y)) for x, y in zip(
                    x_list, y_list
                )
            ]
        )
        self.add(plane, axis_labels, *ticks.values(), *tickmarks.values())
        self.add(dots)
        # self.play(
        #     LaggedStart(
        #         DrawBorderThenFill(plane),
        #         *[Create(t) for t in tickmarks.values()],
        #         *[Write(t) for t in ticks.values()],
        #         Write(axis_labels),
        #         lag_ratio=0.25
        #     )
        # )
        # self.slide_pause(5*_ONEFRAME)



if __name__ == "__main__":
    classes = [
        BjerrumDiagram,
        # Titrerkurve
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html --one-file --offline"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name + "Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)