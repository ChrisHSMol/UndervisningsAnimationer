from manim import *
import numpy as np


# class Skyder(VMobject):
#     def __init__(self, xmin=-5, xmax=5, xstep=1):
#         self.xmin = xmin
#         self.xmax = xmax
#         self.xstep = xstep
#
#     def
# wavelengths = np.linspace(400, 650, 26)
# colors = [
#     "#8300b5", "#7e00db", "#6a00ff", "#3800ff", "#000bff", "#004cff", "#007fff",  # 400nm - 460nm
#     "#00aeff", "#00daff", "#00fff5", "#00ff87", "#09ff00", "#3aff00", "#5aff00",  # 470nm - 530nm
#     "#81ff00", "#a3ff00", "#c3ff00", "#e1ff00", "#ffff00", "#ffdf00", "#ffbe00",  # 540nm - 600nm
#     "#ff9b00", "#ff7700", "#ff4b00", "#ff1b00", "#ff0000"  # 610nm - 650nm
# ]
VISIBLE_LIGHT = {
    int(w): ManimColor(c) for w, c in zip(
        np.linspace(380, 750, 38), [
            "#610061", "#79008d",  # 380nm - 390nm
            "#8300b5", "#7e00db", "#6a00ff", "#3800ff", "#000bff", "#004cff", "#007fff",  # 400nm - 460nm
            "#00aeff", "#00daff", "#00fff5", "#00ff87", "#09ff00", "#3aff00", "#5aff00",  # 470nm - 530nm
            "#81ff00", "#a3ff00", "#c3ff00", "#e1ff00", "#ffff00", "#ffdf00", "#ffbe00",  # 540nm - 600nm
            "#ff9b00", "#ff7700", "#ff4b00", "#ff1b00", "#ff0000", "#ff0000", "#ff0000",  # 610nm - 670nm
            "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000",  # 680nm - 740nm
        ]
    )
}


def interpolate_visible_light(delta, light_dict=VISIBLE_LIGHT):
    if delta <= 0:
        raise Exception(f"delta value needs to be strictly larger than 0")
    lowest_wavelength = min(light_dict.keys())
    interpolated_light_dict = {lowest_wavelength: light_dict[lowest_wavelength]}
    previous_wavelength = lowest_wavelength
    for w, c in light_dict.items():
        if w != lowest_wavelength:
            # interpolated_wavelengths = np.linspace(previous_wavelength, w, (w - previous_wavelength)/delta)
            interpolated_wavelengths = np.arange(previous_wavelength, w, delta)
            interpolated_colors = [
                interpolate_color(light_dict[w], light_dict[previous_wavelength], (w - int_w)/w) for int_w in interpolated_wavelengths
            ]
            for int_w, int_c in zip(interpolated_wavelengths, interpolated_colors):
                interpolated_light_dict[int_w] = int_c
            previous_wavelength = w
    return interpolated_light_dict


def _prep_title(title, close=False):
    if isinstance(title, str):
        title = Tex(title)
    title_ul = Underline(
        title,
        # stroke_opacity=[0, 1, 0],
        stroke_width=[0, 3, 3, 3, 0]
    )
    title_ul_box = Rectangle(
        width=title.width * 1.05,
        height=title.height * 1.6
    ).next_to(
        title_ul, DOWN, buff=0
    ).set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK)
    ul_group = VGroup(title_ul, title_ul_box)
    if close:
        ul_group.shift(UP * title_ul_box.height)
    return title_ul, title_ul_box, ul_group


def play_title(self, title, cols=None, edge=None, already_written=False):
    if isinstance(title, str):
        title = Tex(*[t + " " for t in title.split()])
    if cols is not None and isinstance(cols, dict):
        for k, v in cols.items():
            title[int(k)].set_color(v)
    title_ul, title_ul_box, ul_group = _prep_title(title)
    if already_written:
        self.add(title)
    else:
        self.play(Write(title), run_time=0.5)
    self.wait(2)
    if edge is not None:
        self.play(
            title.animate.to_edge(edge, buff=0.05).set_z_index(10).set_opacity(0.15),
        )
        self.play(
            FadeIn(title_ul_box.set_opacity(0.5).to_edge(edge, buff=0.05).set_z_index(9)),
            run_time=0.1
        )
        return title, title_ul_box
    else:
        self.play(GrowFromCenter(title_ul), run_time=1)
        self.add(ul_group)
        self.play(ul_group.animate.shift(UP * title_ul_box.height))
        self.play(ShrinkToCenter(title_ul))
        self.remove(ul_group, title)
    self.wait(2)


def play_title_reverse(self, title, edge=None):
    if isinstance(title, str):
        title = Tex(title)
    title_ul, title_ul_box, ul_group = _prep_title(title, close=True)
    if edge is None:
        self.add(title, ul_group)
        self.play(GrowFromCenter(title_ul), run_time=1)
        self.play(ul_group.animate.shift(DOWN * title_ul_box.height))
        self.remove(ul_group)
        self.play(ShrinkToCenter(title_ul))
    else:
        self.play(
            title.animate.move_to(edge).set_z_index(0).set_opacity(1.0)
        )
        # title_ul, title_ul_box, ul_group = _prep_title(title, close=True)
    self.wait(1)
    self.play(Unwrite(title), run_time=0.5)
    self.wait(1)


def play_title2(self, title, cols=None, direction=None, hidden_box_color=BLACK):
    if isinstance(title, str):
        title = Tex(*[t + " " for t in title.split()])
    if cols is not None and isinstance(cols, dict):
        for k, v in cols.items():
            title[int(k)].set_color(v)

    title_ul = Line(
        start=title.get_corner(DL) + 0.25*DL, end=title.get_corner(DR) + 0.25*DR, stroke_opacity=[0, 1, 0]
    ).scale(1.5).set_z_index(title.get_z_index()+2)
    title_ul_box = Rectangle(
        width=title.width * 1.25,
        height=title.height * 3.0
    ).next_to(
        title_ul, DOWN, buff=0
    ).set_style(fill_opacity=1, stroke_width=0, fill_color=hidden_box_color).set_z_index(title.get_z_index()+1)

    title.shift(DOWN)
    if direction is None:
        _dot = Dot(radius=title_ul.height * 0.5).move_to(title_ul)
        self.play(
            LaggedStart(
                GrowFromCenter(_dot),
                GrowFromCenter(title_ul),
                lag_ratio=1
            )
        )
        self.remove(_dot)
    else:
        self.play(
            # Create(title_ul)
            FadeIn(title_ul, shift=6*direction)
        )
    self.add(title, title_ul_box)
    self.wait(0.25)
    self.play(
        title.animate.shift(UP)
    )
    self.wait(1)
    self.play(
        title_ul.animate.shift(UP),
        title_ul_box.animate.shift(UP)
    )
    self.remove(title, title_ul_box)
    self.wait(0.25)
    if direction is None:
        _dot = Dot(radius=title_ul.height * 0.5).move_to(title_ul)
        self.play(
            LaggedStart(
                ShrinkToCenter(title_ul),
                ShrinkToCenter(_dot),
                lag_ratio=1
            )
        )
    else:
        self.play(
            # Uncreate(title_ul, reverse_rate_function=True)
            FadeOut(title_ul, shift=6*direction)
        )
    # if edge is not None:
    #     self.play(
    #         title.animate.to_edge(edge, buff=0.05).set_z_index(10).set_opacity(0.15),
    #     )
    #     self.play(
    #         FadeIn(title_ul_box.set_opacity(0.5).to_edge(edge, buff=0.05).set_z_index(9)),
    #         run_time=0.1
    #     )
    #     return title, title_ul_box
    # else:
    #     self.play(GrowFromCenter(title_ul), run_time=1)
    #     self.add(ul_group)
    #     self.play(ul_group.animate.shift(UP * title_ul_box.height))
    #     self.play(ShrinkToCenter(title_ul))
    #     self.remove(ul_group, title)
    # self.wait(2)


def update_title(self, old_title, new_title, edge=None):
    self.play(
        old_title.animate.move_to(ORIGIN).set_opacity(1)
    )
    new_title.move_to(ORIGIN).set_opacity(1)
    xs_pause(self)
    self.play(
        TransformMatchingTex(
            old_title,
            new_title,
        )
    )
    s_pause(self)
    title_ul_box = Rectangle(
        width=new_title.width * 1.05,
        height=new_title.height * 1.6
    ).move_to(new_title).set_style(fill_opacity=0.5, stroke_width=0, fill_color=BLACK).set_z_index(9)
    new_title.set_z_index(10)
    if edge is not None:
        self.play(
            new_title.animate.to_edge(edge, buff=0.05).set_opacity(0.15),
            title_ul_box.animate.to_edge(edge, buff=0.05)
        )
        s_pause(self)
    return new_title, title_ul_box


def p2p_anim(mob1, mob2, tex1, tex2=None, index=0):
    if tex2 == None:
        tex2 = tex1
    return ReplacementTransform(
        mob1.get_parts_by_tex(tex1)[index],
        mob2.get_parts_by_tex(tex2)[index],
    )


def p2p_anim_copy(mob1, mob2, tex1, tex2=None, index=0):
    if tex2 == None:
        tex2 = tex1
    return TransformFromCopy(
        mob1.get_parts_by_tex(tex1)[index],
        mob2.get_parts_by_tex(tex2)[index],
    )


def fade_out_all(self, rt=1):
    self.play(
        *[
            FadeOut(mob) for mob in self.mobjects
        ],
        run_time=rt
    )


def ftp(point1, point2, dim="y"):  # Find Top Point
    d = {"x": 0, "y": 1, "z": 2}
    if isinstance(dim, str):
        dim = d[dim]
    return point1 if point1[dim] > point2[dim] else point2


def xs_pause(self, t=0.5):
    self.wait(t)


def s_pause(self, t=1):
    self.wait(t)


def m_pause(self, t=1.5):
    self.wait(t)


def l_pause(self, t=2.5):
    self.wait(t)


def xl_pause(self, t=5):
    self.wait(t)


def create_table(data, orientation="vertical", numcol1=BLUE, numcol2=None, dec=0, sign=False, scale=1.0):
    if numcol2 is None:
        numcol2 = numcol1
    if orientation == "horizontal":
        data = np.transpose(data)
    numbers = VGroup()
    for i in data:
        for j in i:
            numbers.add(
                DecimalNumber(
                    j,
                    color=numcol1,
                    num_decimal_places=dec,
                    include_sign=sign
                ).scale(scale)
            )
    numbers = numbers.arrange_in_grid(rows=len(data), col_alignments="rr")
    table = DecimalTable(
        data
    )
    return table


slides = False


def slides_pause(self, t=1.0, slides_bool=True):
    if t <= 0:
        pass
    if slides_bool:
        # indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
        # indicator = Arrow(
        #     start=LEFT, end=RIGHT, fill_opacity=0.5, fill_color=GREEN, stroke_width=50
        # ).scale(0.5).to_edge(DR, buff=0.1)
        indicator = MathTex(
            ">", font_size=50, color=GREEN, stroke_width=7, fill_opacity=0.5, stroke_opacity=0.5
        ).to_edge(DR, buff=0.1).set_z_index(100)
        # indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).move_to(
        #     0.45 * (ManimFrame().frame_width * RIGHT + ManimFrame().frame_height * DOWN)
        # )
        # indicator = Arrow(start=LEFT, end=RIGHT, fill_opacity=0.15, fill_color=GREEN, buff=20).to_edge(DR, buff=0.1)
        self.play(FadeIn(indicator), run_time=0.25)
        xs_pause(self)
        # self.pause()
        self.next_slide()
        self.play(FadeOut(indicator), run_time=0.25)
    else:
        self.wait(t)


def scene_marker(scene_name):
    print("-" * max(20, len(scene_name)))
    print(scene_name)
    print("-" * max(20, len(scene_name)))


def between_mobjects(left_mob, right_mob):
    return 0.5*(right_mob.get_edge_center(LEFT) + left_mob.get_edge_center(RIGHT))


def get_background_rect(mobject, buff=0.5, stroke_colour=None, stroke_width=1, fill_opacity=0.85, fill_color=BLACK):
    return Rectangle(
        width=mobject.width + buff,
        height=mobject.height + buff
    ).move_to(mobject).set_style(
        fill_opacity=fill_opacity,
        stroke_width=0 if stroke_colour is None else stroke_width,
        fill_color=fill_color,
        stroke_color=stroke_colour
    ).set_z_index(mobject.get_z_index()-1)


def draw_and_fade_in_mob(self, mob, **kwargs):
    self.play(
        LaggedStart(
            ShowPassingFlash(mob.copy(), time_width=2),
            FadeIn(mob),
            lag_ratio=0.5
        ),
        **kwargs
    )


class DieFace(VGroup):
    def __init__(self,
                 value,
                 side_length=1.0,
                 corner_radius=0.15,
                 stroke_color=WHITE,
                 stroke_width=2.0,
                 fill_color=BLUE_C,
                 dot_radius=0.08,
                 dot_color=GREY_E,
                 dot_coalesce_factor=0.5):
        dot = Dot(radius=dot_radius, fill_color=dot_color)
        square = Square(
            side_length=side_length,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=1.0,
        )
        square.round_corners(corner_radius)

        if not (1 <= value <= 6):
            raise Exception("DieFace only accepts integer inputs between 1 and 6")

        edge_group = [
            (ORIGIN,),
            (UL, DR),
            (UL, ORIGIN, DR),
            (UL, UR, DL, DR),
            (UL, UR, ORIGIN, DL, DR),
            (UL, UR, LEFT, RIGHT, DL, DR),
        ][value - 1]

        arrangement = VGroup(*(
            # dot.copy().move_to(square.get_bounding_box_point(vect))
            dot.copy().move_to(0.5*side_length * vect)
            for vect in edge_group
        ))
        arrangement.space_out_submobjects(dot_coalesce_factor)

        super().__init__(square, arrangement)
        self.value = value
        self.index = value


class CoinFace(VGroup):
    def __init__(self,
                 value,  # 0: Tails, 1: Heads
                 coin_radius=0.3,
                 stroke_color=WHITE,
                 stroke_width=1.0,
                 fill_color=[RED_C, BLUE_C],
                 coin_opacity=0.25,
                 use_heads_tails=False
                 ):
        if value not in (0, 1):
            raise Exception("CoinFace only accepts values of 0 (Plat, Tails) or 1 (Krone, Heads)")

        coin = Circle(
            radius=coin_radius, fill_color=fill_color[value], stroke_color=stroke_color, stroke_width=stroke_width,
            fill_opacity=coin_opacity
        )
        label_text = ["T", "H"][value] if use_heads_tails else ["P", "K"][value]
        label = Tex(
            label_text,
            # stroke_color=WHITE
        ).set(color=WHITE)
        # ).set_color_by_tex_to_color_map(
            # {"T": fill_color[0], "P": fill_color[0], "H": fill_color[1], "K": fill_color[1]}
            # {"T": stroke_color, "P": stroke_color, "H": stroke_color, "K": stroke_color}
        # )

        super().__init__(coin, label)
        self.value = value
        self.fill_color = fill_color[value]


def add_shine(mob, nlines=10, ends=False):
    # shines = VGroup(
    #     *[
    #         mob.copy().set_style(
    #             stroke_width=(2 * (i + 1)) ** 2,
    #             # fill_opacity=np.exp(-(i + 1) ** 2)
    #         ).set_opacity(np.exp(-(i + 1) ** 2)) for i in np.linspace(2, 0, nlines)
    #         # ) for i in np.linspace(2, 0, nlines)
    #     ]
    # )
    # shines.add(mob)
    shines = always_redraw(lambda: VGroup(*[
        mob.copy().set_style(
            # stroke_width=(mob.get_stroke_width() * (i + 1)) ** 2,
            stroke_width=(5 * (i + 1)) ** 2,
            fill_opacity=0
        ).set_opacity(np.exp(-(i + 1) ** 2)) for i in np.linspace(1, 0, nlines)
    ]))
    return shines


def keyword_overlay(self):
    srec = ScreenRectangle(height=10, stroke_width=0, fill_color=BLACK, fill_opacity=0.5)
    self.play(FadeIn(srec), run_time=0.5)
    droplets = VGroup(
        Dot(UP, color=WHITE, radius=0.08),
        Dot(UP, color=WHITE, radius=0.04),
    )
    # self.play(FadeIn(droplets, shift=DOWN))
    # self.remove(droplet)
    plane = NumberPlane()
    paths = VGroup(
        plane.plot(lambda x: -0.03 * x**2 + np.cos(x), x_range=[-8, 0]),
        plane.plot(lambda x: -0.03 * x**2 + np.cos(x), x_range=[0, 8]),
    )
    circ = Circle(radius=1).shift(2*UP).rotate(-PI/2)
    # self.add(paths, circ)
    self.play(
        # AnimationGroup(
        #     MoveAlongPath(droplets[0], paths[0]),
        #     MoveAlongPath(droplets[1], paths[1])
        # ),
        MoveAlongPath(droplets[0], paths[0]),
        rate_func=rate_functions.rush_into,
        run_time=2
    )
    self.play(
        MoveAlongPath(droplets[0], circ),
        rate_func=rate_functions.linear,
        run_time=1
    )
    self.play(
        MoveAlongPath(droplets[0], paths[1]),
        rate_func=rate_functions.rush_from,
        run_time=2
    )


class DrejeKnap(VGroup):
    def __init__(self,
                 color=None,
                 accent_color=None,
                 range_min=0,
                 range_max=5,
                 range_step=1,
                 start_value=0,
                 radius=1,
                 label=None,
                 show_value=False
                 ):

        if color is None:
            color = WHITE
        if accent_color is None:
            accent_color = WHITE
        circ = VGroup(
            Circle(radius=radius, color=color),
            # Circle(radius=radius, color=WHITE),
            Circle(radius=1.2 * radius, color=BLACK, stroke_width=0.01),
            Circle(radius=0.45 * radius, color=BLACK, stroke_width=0.01)
        )
        # circ += VGroup(
        #     *[
        #         Dot(
        #             circ[1].point_at_angle(-270/360 * i + 200 * DEGREES),
        #             color=color,
        #             radius=0.02 * (i + 1)
        #         ) for i in np.arange(0, range_max-range_min+range_step, range_step)
        #     ]
        # )
        n_points = int((range_max - range_min) / range_step + 1)
        angle_range = 270
        angle_step = angle_range / (n_points - 1)
        angle_offset = 225
        marks = VGroup(
            *[
                Line(
                    start=circ[0].point_at_angle((angle_offset - angle_step * i) * DEGREES),
                    end=circ[1].point_at_angle((angle_offset - angle_step * i) * DEGREES),
                    color=color,
                    # color=WHITE
                ) for i in range(n_points)
            ]
        )
        circ += marks
        # angle_tracker = ValueTracker(range_min)
        angle_tracker = ValueTracker(start_value)
        circ += always_redraw(lambda:
            Line(
                start=circ[2].point_at_angle(
                    # (angle_offset - angle_step * (angle_tracker.get_value()-range_min)) * DEGREES
                    (angle_offset - angle_step * (angle_tracker.get_value() - range_min + range_max) / (range_max - range_min)) * DEGREES
                    # (angle_offset - angle_step * (angle_tracker.get_value() - range_min + range_max) / (range_max - range_min))
                ),
                end=circ[0].point_at_angle(
                    # (angle_offset - angle_step * (angle_tracker.get_value()-range_min)) * DEGREES
                    (angle_offset - angle_step * (angle_tracker.get_value() - range_min + range_max) / (range_max - range_min)) * DEGREES
                    # (angle_offset - angle_step * (angle_tracker.get_value() - range_min + range_max) / (range_max - range_min))
                ),
                color=accent_color,
                stroke_width=6
            )
        )
        circ += VGroup(
            *[
                MathTex(i, color=accent_color).next_to(line, d, buff=0.05) for i, line, d in zip(
                    [range_min, range_max],
                    [marks[0], marks[-1]],
                    [DL, DR]
                )
            ]
        )
        if label is not None:
            circ += MathTex(label, color=accent_color).set_color(accent_color).scale(2).move_to(circ[0])

        if show_value:
            circ += always_redraw(lambda:
                DecimalNumber(angle_tracker.get_value(), color=accent_color).next_to(circ[0], DOWN, buff=0.1)
            )

        super().__init__(circ)
        self.tracker = angle_tracker
        self.color = color
        self.accent_color = accent_color
        self.range_min = range_min
        self.range_max = range_max
        self.range_step = range_step
        self.radius = radius
        self.label = label

    def get_min(self):
        return self.range_min

    def get_max(self):
        return self.range_max

    def get_step(self):
        return self.range_step

    def get_value(self):
        value = always_redraw(lambda:
            DecimalNumber(self.tracker.get_value(), color=self.accent_color).next_to(self[0], DOWN, buff=0.1)
        )
        return value


class Slider(VGroup):
    def __init__(self,
                 smin=-5,
                 smax=5,
                 step_size=1,
                 color=WHITE,
                 accent_color=YELLOW,
                 label=None,
                 direction="vertical"
                 ):
        endpoint = UP
        pticks = [LEFT, RIGHT]
        scale = 2
        if direction.lower() == "horizontal":
            endpoint = RIGHT
            pticks = [DOWN, UP]
            scale = 3
        # if direction.lower() == "vertical":
        #     endpoint = UP
        n_points = int((smax - smin)/step_size + 1)
        tracker = ValueTracker(0)
        slider = VGroup(
            Line(
                start=ORIGIN,
                # end=2 * UP,
                end=scale * endpoint,
                color=color,
                stroke_width=2
            )
        )
        _slider_ticks = [
            Line(
                # start=0.05 * LEFT + i * UP,
                # end=0.05 * RIGHT + i * UP,
                start=0.05 * pticks[0] + i * endpoint,
                end=0.05 * pticks[1] + i * endpoint,
                color=color,
                stroke_width=2
            # ) for i in np.linspace(0, 2, n_points)
            ) for i in np.linspace(0, scale, n_points)
        ]
        slider.add(*_slider_ticks)
        slider.add(*[
            DecimalNumber(
                n,
                num_decimal_places=0,
                include_sign=n != 0
            ).scale(0.35).next_to(
                # hline, LEFT, buff=0.075
                hline, pticks[0], buff=0.075
            ) for n, hline in zip(np.arange(smin, smax + 0.01, 1), slider[1:])
        ])
        if label is not None:
            slider.add(
                # MathTex(label).set_color(color=accent_color).next_to(slider[0], UP)
                # MathTex(label, color=accent_color).next_to(slider[0], UP)
                MathTex(label, color=accent_color).next_to(slider[0], endpoint)
            )

        slider.add(always_redraw(lambda:
            Arrow(
               # 0.5 * RIGHT, 0.5 * LEFT, color=accent_color
               0.5 * pticks[1], 0.5 * pticks[0], color=accent_color
            ).next_to(
                # _slider_ticks[0], RIGHT, buff=0.1
                _slider_ticks[0], pticks[1], buff=0.1
            ).shift(
                # 2*(tracker.get_value() - smin) / (smax - smin) * UP
                scale*(tracker.get_value() - smin) / (smax - smin) * endpoint
            )
        ))
        super().__init__(slider)
        self.tracker = tracker
        self.smin = smin
        self.smax = smax
        self.step = step_size
        self.color = color
        self.accent_color = accent_color
        self.label = label
        self.direction = direction


def three_way_interpolate(c1, c2, c3, alpha, alpha_max):
    c = interpolate_color(
        interpolate_color(c1, c2, min(alpha, 0.5*alpha_max) / (0.5*alpha_max)),
        interpolate_color(c2, c3, (max(alpha, 0.5*alpha_max) - 0.5*alpha_max) / (0.5*alpha_max)),
        alpha / alpha_max
    )
    return c


def boxes_of_content(self, list_of_contents, list_of_colors):
    boxes = VGroup()
    for text, color in zip(list_of_contents, list_of_colors):
        if not isinstance(text, Tex):
            text = Tex(text)
        boxes.add(
            VGroup(
                text,
                get_background_rect(text, stroke_colour=color)
            )
        )
    return boxes


def sunset_color_scheme(n):
    uneven = ["#003f5c", "#374c80", "#7a5195", "#bc5090", "#ef5675", "#ff764a", "#ffa600"]
    even = ["#003f5c", "#2f4b7c", "#665191", "#a05195", "#d45087", "#f95d6a", "#ff7c43", "#ffa600"]
    list = even if n % 2 == 0 else uneven
    returnlist = []
    for i in np.arange(0, len(list), n):
        returnlist.append(list[i])
    # return color_gradient(["#003f5c", "#ffa600"], n)
    return returnlist

