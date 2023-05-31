from manim import *
import numpy as np


# class Skyder(VMobject):
#     def __init__(self, xmin=-5, xmax=5, xstep=1):
#         self.xmin = xmin
#         self.xmax = xmax
#         self.xstep = xstep
#
#     def


def _prep_title(title, close=False):
    if isinstance(title, str):
        title = Tex(title)
    title_ul = Underline(title)
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


def slides_pause(self, t=1.0, slides_bool=slides):
    if slides_bool:
        indicator = Dot(fill_opacity=0.5, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
        # indicator = Arrow(start=LEFT, end=RIGHT, fill_opacity=0.15, fill_color=GREEN, buff=20).to_edge(DR, buff=0.1)
        self.play(FadeIn(indicator), run_time=0.25)
        xs_pause(self)
        self.pause()
        self.play(FadeOut(indicator), run_time=0.25)
    else:
        self.wait(t)


def scene_marker(scene_name):
    print("-" * 20)
    print(scene_name)
    print("-" * 20)


def between_mobjects(left_mob, right_mob):
    return 0.5*(right_mob.get_edge_center(LEFT) + left_mob.get_edge_center(RIGHT))


def get_background_rect(mobject, buff=0.5, stroke_colour=None, stroke_width=1, fill_opacity=0.85):
    return Rectangle(
        width=mobject.width + buff,
        height=mobject.height + buff
    ).move_to(mobject).set_style(
        fill_opacity=fill_opacity,
        stroke_width=0 if stroke_colour is None else stroke_width,
        fill_color=BLACK,
        stroke_color=stroke_colour
    ).set_z_index(mobject.get_z_index()-1)


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


def add_shine(mob, nlines=10, ends=False):
    # shines = VGroup(
    #     *[
    #         Line(
    #             # start=line.get_left(),
    #             # end=line.get_right(),
    #             start=line.get_start(),
    #             end=line.get_end(),
    #             stroke_width=(2 * (i + 1)) ** 2,
    #             color=line.get_color()
    #         ).set_opacity(np.exp(-(i + 1) ** 2)) for i in np.linspace(2, 0, nlines)
    #     ]
    # )
    shines = VGroup(
        *[
            mob.copy().set_style(
                stroke_width=(2 * (i + 1)) ** 2,
                # fill_opacity=np.exp(-(i + 1) ** 2)
            ).set_opacity(np.exp(-(i + 1) ** 2)) for i in np.linspace(2, 0, nlines)
            # ) for i in np.linspace(2, 0, nlines)
        ]
    )
    # if ends:
    #     for ex in [line.get_start(), line.get_end()]:
    #         shines.add(
    #             *[
    #                 Dot(
    #                     ex,
    #                     color=line.get_color(),
    #                     radius=(0.145*(i + 1)) ** 2
    #                 ).set_opacity(np.exp(-(i + 1) ** 2)) for i in np.linspace(2, 0, nlines)
    #             ]
    #         )
    shines.add(mob)
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
        angle_tracker = ValueTracker(0)
        circ += always_redraw(lambda:
            Line(
                start=circ[2].point_at_angle(
                    (angle_offset - angle_step * (angle_tracker.get_value()-range_min)) * DEGREES
                ),
                end=circ[0].point_at_angle(
                    (angle_offset - angle_step * (angle_tracker.get_value()-range_min)) * DEGREES
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

