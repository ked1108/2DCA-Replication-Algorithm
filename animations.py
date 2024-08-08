from manim import *

class DrawCircles(Scene):
    
    def construct(self):
        # circles =VGroup(*[Circle(radius=0.5) for _ in range(12)])
        # circles.arrange_in_grid(rows=3, cols=4, buff=1)
        circles = Circle(radius=0.5)
        # self.add(circles)
        self.play(Create(circles))