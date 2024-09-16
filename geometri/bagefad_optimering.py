from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess
import random

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


class Bagefad(ThreeDScene, Slide if slides else Scene):
    btransparent = False

    def construct(self):
        self.slide_pause()
        self.bagefad_2d(banimations=True)
        # self.slide_pause()
        self.bagefad_3d()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def max_width(self):
        return 8

    def max_length(self):
        return 5

    def bagefad_2d(self, banimations=True):
        x_tracker = ValueTracker(0.0)
        base_vertices = VGroup(*[
            Dot(coord, radius=0) for coord in [
                [-0.5*self.max_width(), 0.5*self.max_length(), 0], [-0.5*self.max_width(), 0.5*self.max_length(), 0],
                [0.5*self.max_width(), -0.5*self.max_length(), 0], [0.5*self.max_width(), 0.5*self.max_length(), 0]
            ]
        ])
        sheet_vertices = always_redraw(lambda: VGroup(*[
            Dot(coord, radius=0) for coord in [
                [-0.5*self.max_width()+x_tracker.get_value(), 0.5*self.max_length(), 0],
                [-0.5*self.max_width()+x_tracker.get_value(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [-0.5*self.max_width(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [-0.5*self.max_width(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [-0.5*self.max_width()+x_tracker.get_value(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [-0.5*self.max_width()+x_tracker.get_value(), -0.5*self.max_length(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), -0.5*self.max_length(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [0.5*self.max_width(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [0.5*self.max_width(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), 0.5*self.max_length(), 0]
            ]
        ]))
        bkg_rect = Rectangle(
            width=self.max_width(), height=self.max_length(), fill_color=RED, fill_opacity=0.5, stroke_width=0.1
        ).set_z_index(1)
        big_polygon = always_redraw(lambda: Polygon(
            *[v.get_center() for v in sheet_vertices],
            fill_color=GRAY, fill_opacity=1, stroke_width=0.1
        ).set_z_index(2))
        self.add(big_polygon, bkg_rect, sheet_vertices, base_vertices)

        bracetexts = always_redraw(lambda: VGroup(
            MathTex("x", color=bkg_rect.get_color())
            .move_to((-0.5*self.max_width()-0.2, -0.5*self.max_length()+0.5*x_tracker.get_value(), 0)),
            MathTex("x", color=bkg_rect.get_color())
            .move_to((-0.5*self.max_width()+0.5*x_tracker.get_value(), -0.5*self.max_length()-0.2, 0)),
            MathTex("x", color=bkg_rect.get_color())
            .move_to((-0.5*self.max_width()+x_tracker.get_value()+0.2, -0.5*self.max_length()+0.5*x_tracker.get_value(), 0)),
            MathTex("x", color=bkg_rect.get_color())
            .move_to((-0.5*self.max_width()+0.5*x_tracker.get_value(), -0.5*self.max_length()+x_tracker.get_value()+0.2, 0)),
        ).set_z_index(3).set_opacity(min(2*x_tracker.get_value(), 1)))
        self.add(bracetexts)

        if banimations:
            self.play(
                x_tracker.animate.set_value(2),
                run_time=5
            )
            self.slide_pause()
            self.play(
                x_tracker.animate.set_value(1),
                run_time=5
            )
        else:
            self.play(
                x_tracker.animate.set_value(1),
                # run_time=2/_FRAMERATE[q]
                run_time=1
            )

        fold_lines = always_redraw(lambda: VGroup(
            DashedLine(start=sheet_vertices[1], end=sheet_vertices[4], stroke_color=YELLOW),
            DashedLine(start=sheet_vertices[4], end=sheet_vertices[7], stroke_color=YELLOW),
            DashedLine(start=sheet_vertices[7], end=sheet_vertices[10], stroke_color=YELLOW),
            DashedLine(start=sheet_vertices[10], end=sheet_vertices[1], stroke_color=YELLOW),
        ).set_z_index(3))

        if banimations:
            self.slide_pause()
            self.play(
                LaggedStart(
                    *[FadeOut(m) for m in [bkg_rect, *bracetexts]],
                    lag_ratio=0.1
                )
            )
            self.play(
                LaggedStart(
                    *[Create(m) for m in fold_lines],
                    lag_ratio=1
                )
            )
        else:
            self.add(fold_lines)
            self.remove(bracetexts, bkg_rect)
        # self.slide_pause()
        self.remove(big_polygon, fold_lines)

    def bagefad_3d(self):
        x_tracker = ValueTracker(1)
        sheet_vertices = always_redraw(lambda: VGroup(*[
            Dot(coord, radius=0) for coord in [
                [-0.5*self.max_width()+x_tracker.get_value(), 0.5*self.max_length(), 0],
                [-0.5*self.max_width()+x_tracker.get_value(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [-0.5*self.max_width(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [-0.5*self.max_width(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [-0.5*self.max_width()+x_tracker.get_value(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [-0.5*self.max_width()+x_tracker.get_value(), -0.5*self.max_length(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), -0.5*self.max_length(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [0.5*self.max_width(), -0.5*self.max_length()+x_tracker.get_value(), 0],
                [0.5*self.max_width(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), 0.5*self.max_length()-x_tracker.get_value(), 0],
                [0.5*self.max_width()-x_tracker.get_value(), 0.5*self.max_length(), 0]
            ]
        ]))
        big_polygon = always_redraw(lambda: Polygon(
            *[v.get_center() for v in sheet_vertices],
            fill_color=GRAY, fill_opacity=1, stroke_width=0.1
        ).set_z_index(2))
        fold_lines = always_redraw(lambda: VGroup(
            DashedLine(start=sheet_vertices[1], end=sheet_vertices[4], stroke_color=YELLOW),
            DashedLine(start=sheet_vertices[4], end=sheet_vertices[7], stroke_color=YELLOW),
            DashedLine(start=sheet_vertices[7], end=sheet_vertices[10], stroke_color=YELLOW),
            DashedLine(start=sheet_vertices[10], end=sheet_vertices[1], stroke_color=YELLOW),
        ).set_z_index(3))
        print(x_tracker.get_value())
        self.add(big_polygon, fold_lines)
        self.slide_pause()

        f1, f2, f3, f4 = [ValueTracker(0) for _ in range(4)]
        static_faces = always_redraw(lambda: VGroup(
            # Prism(
            #     dimensions=[10-2*x_tracker.get_value(), 5-2*x_tracker.get_value(), 0.01], fill_color=big_polygon.get_color(),
            #     fill_opacity=1, stroke_width=0.1
            # ),
            # *[Prism(
            #     dimensions=[x_tracker.get_value(), 5-2*x_tracker.get_value(), 0.01], fill_color=big_polygon.get_color(),
            #     fill_opacity=1, stroke_width=0.1
            # # ) for _ in range(2)],
            # ).shift((5-0.5*x_tracker.get_value()) * d) for d in [LEFT, RIGHT]],
            # *[Prism(
            #     dimensions=[10-2*x_tracker.get_value(), x_tracker.get_value(), 0.01], fill_color=big_polygon.get_color(),
            #     fill_opacity=1, stroke_width=0.1
            # # ) for _ in range(2)],
            # ).shift((2.5-0.5*x_tracker.get_value()) * d) for d in [UP, DOWN]],
            Prism(
                dimensions=(self.max_width()-2*x_tracker.get_value(), self.max_length()-2*x_tracker.get_value(), 0.01),
                fill_color=big_polygon.get_color(), fill_opacity=0.5, stroke_width=0.5, stroke_color=RED
            ),
            *[Prism(
                dimensions=(x_tracker.get_value(), self.max_length()-2*x_tracker.get_value(), 0.01),
                fill_color=big_polygon.get_color(), fill_opacity=0.5, stroke_width=0.5, stroke_color=RED
            ).shift((0.5*self.max_width()-0.5*x_tracker.get_value()) * d + f.get_value()*0.5*x_tracker.get_value()*(OUT - d)).rotate(
                -PI / 2 * f.get_value(), axis=fl.get_unit_vector()
            ) for d, f, fl in zip([LEFT, RIGHT], [f1, f3], [fold_lines[0], fold_lines[2]])],
            *[Prism(
                dimensions=(self.max_width()-2*x_tracker.get_value(), x_tracker.get_value(), 0.01),
                fill_color=big_polygon.get_color(), fill_opacity=0.5, stroke_width=0.5, stroke_color=RED
            ).shift((0.5*self.max_length()-0.5*x_tracker.get_value()) * d + f.get_value()*0.5*x_tracker.get_value()*(OUT - d)).rotate(
                -PI / 2 * f.get_value(), axis=fl.get_unit_vector()
            ) for d, f, fl in zip([UP, DOWN], [f4, f2], [fold_lines[3], fold_lines[1]])],
        ))
        # for i, d in enumerate([LEFT, RIGHT, UP, DOWN]):
        #     static_faces[i+1].next_to(static_faces[0], d, buff=0)
        self.remove(big_polygon)
        self.add(static_faces)

        self.move_camera(phi=PI / 2.5)
        self.begin_ambient_camera_rotation(rate=0.5, about="theta")
        self.play(
            LaggedStart(
                # static_faces[1].animate.rotate(
                #     -PI/2, axis=fold_lines[0].get_unit_vector()
                # ).shift(0.5*x_tracker.get_value()*(OUT + RIGHT)),
                # static_faces[4].animate.rotate(
                #     -PI/2, axis=fold_lines[1].get_unit_vector()
                # ).shift(0.5*x_tracker.get_value()*(OUT + UP)),
                # static_faces[2].animate.rotate(
                #     -PI/2, axis=fold_lines[2].get_unit_vector()
                # ).shift(0.5*x_tracker.get_value()*(OUT + LEFT)),
                # static_faces[3].animate.rotate(
                #     -PI/2, axis=fold_lines[3].get_unit_vector()
                # ).shift(0.5*x_tracker.get_value()*(OUT + DOWN)),
                *[f.animate.set_value(1) for f in [f1, f2, f3, f4]],
                lag_ratio=1
            )
        )
        self.slide_pause()
        self.play(
            FadeOut(fold_lines),
            run_time=0.5
        )
        self.remove(fold_lines)

        # dynamic_faces = always_redraw(lambda:
        #     VGroup(
        #         Prism(
        #             dimensions=(10 - 2 * x_tracker.get_value(), 5 - 2 * x_tracker.get_value(), 0.01),
        #             fill_color=big_polygon.get_color(),
        #             fill_opacity=1, stroke_width=0.1
        #         ),
        #     )
        # )
        # self.stop_ambient_camera_rotation()
        self.play(
            x_tracker.animate.set_value(0.5*min(self.max_length(), self.max_width())-0.5),
            run_time=5
        )
        self.play(
            x_tracker.animate.set_value(1),
            run_time=5
        )
        self.slide_pause()

        formula_text = always_redraw(lambda:
            VGroup(
                VGroup(
                    MathTex("x ="), DecimalNumber(x_tracker.get_value())
                ).arrange(RIGHT),
                VGroup(
                    Tex(f"Bredde ="), DecimalNumber(self.max_width() - 2*x_tracker.get_value())
                ).arrange(RIGHT),
                VGroup(
                    Tex("Længde ="), DecimalNumber(self.max_length() - 2*x_tracker.get_value())
                ).arrange(RIGHT),
                VGroup(
                    Tex("Volumen ="), DecimalNumber(
                        x_tracker.get_value() * (self.max_length()-2*x_tracker.get_value()) * (self.max_width()-2*x_tracker.get_value())
                    )
                ).arrange(RIGHT)
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(DL)
        )
        self.add_fixed_in_frame_mobjects(formula_text)
        self.slide_pause()

        self.play(
            x_tracker.animate.set_value(0.5*min(self.max_length(), self.max_width())-0.5),
            run_time=10
        )
        self.play(
            x_tracker.animate.set_value(0),
            run_time=10
        )
        self.slide_pause()

        plane = NumberPlane(
            x_range=[0, 0.5*min(self.max_length(), self.max_width()), 0.5],
            y_range=[0, 20, 5],
            x_length=2,
            y_length=4,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True}
        ).to_edge(UL)
        labels = plane.get_axis_labels(
            x_label=MathTex("x"),
            y_label=Tex("Volumen")
        )
        moving_dot = always_redraw(lambda: Dot(
            plane.c2p(
                x_tracker.get_value(),
                x_tracker.get_value() * (self.max_length()-2*x_tracker.get_value()) * (self.max_width()-2*x_tracker.get_value())
            )
        ))
        trace = TracedPath(moving_dot.get_center)
        self.add_fixed_in_frame_mobjects(plane, labels, moving_dot, trace)
        # self.play(
        #     x_tracker.animate.set_value(1),
        #     run_time=10
        # )
        # self.slide_pause()
        self.play(
            x_tracker.animate.set_value(0.5*min(self.max_length(), self.max_width())),
            run_time=20
        )
        self.slide_pause()


if __name__ == "__main__":
    cls = Bagefad
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
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

