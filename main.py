from math import cos, e, sin
from manim import *
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase

class S1(Scene):
    def construct(self):
        christmas = Text("Christmas is here...")
        christmasDesc = Text("Let's end the year with some Fourier decomposition.").scale(0.5)

        self.play(Write(christmas))
        self.play(Circumscribe(christmas, fade_out = True, buff = 0.5, color = GREEN_B))
        self.play(christmas.animate.set_color_by_gradient(RED_B, GREEN).shift(UP*3))
        self.wait()

        self.play(Create(christmasDesc))
        self.play(christmasDesc.animate.shift(DOWN*3).set_color_by_gradient(BLUE_B, LIGHT_BROWN))
        self.play(FadeOut(christmas))
        self.play(FadeOut(christmasDesc))
        self.wait()

class S2(VectorScene):
    def construct(self):
        complexPlane = NumberPlane(
            x_range=[-10,10,1],
            y_range=[-5,5,1],
        )

        t = ValueTracker(0)
        omega = ValueTracker(1)
        tEquals = MathTex("t = ", substrings_to_isolate="t").shift(UP*3).shift(LEFT*5).set_color_by_tex("t", GREEN_B)
        tDecimal = always_redraw(lambda: DecimalNumber(t.get_value()).next_to(tEquals, RIGHT))
        omegaEquals = Tex("$\omega = $").shift(UP*2).shift(LEFT*5).set_color_by_tex("mega", RED_B)
        omegaDecimal = always_redraw(lambda: DecimalNumber(omega.get_value()).next_to(omegaEquals, RIGHT))

        vector = always_redraw(lambda: Vector([np.cos(-2*PI*t.get_value()*omega.get_value()), np.sin(-2*PI*t.get_value()*omega.get_value())]).set_color(GREEN_B))
        
        unitCircle = Circle(color=RED_B)
        unitCircle.fill_opacity = 0
        eitheta = MathTex('e^{it} = \cos(t) + i\sin(t)').shift(DOWN*3).scale(0.9)
        eithetawfreq = MathTex('e^{-2\pi it\omega} = \cos(-2\pi t\omega) + i\sin(-2\pi t\omega)').shift(DOWN*3).scale(0.9)
        eithetawfreqafunc = MathTex('g(x)e^{-2\pi it\omega} = g(x)\cos(-2\pi t\omega) + ig(x)\sin(-2\pi t\omega)').shift(DOWN*3).scale(0.9)

        self.play(DrawBorderThenFill(complexPlane))
        self.play(Create(unitCircle))
        self.play(Write(eitheta))
        self.wait(2)
        self.play(ReplacementTransform(eitheta, eithetawfreq))
        self.play(Create(vector), Write(VGroup(tEquals, tDecimal)), Write(VGroup(omegaEquals, omegaDecimal)))
        self.play(t.animate.set_value(PI), run_time=5)
        cosSinVectorCoords = MobjectMatrix([[MathTex('\cos(-2\pi t\omega)')], [MathTex('\sin(-2\pi t\omega)')]]).move_to(vector.get_tip()).shift(DOWN*1, RIGHT*1.5).scale(0.7)
        self.play(GrowFromPoint(cosSinVectorCoords, vector.get_tip()))
        self.play(Circumscribe(cosSinVectorCoords, fade_out=True, color=YELLOW_B))
        self.wait(2)
        self.play(t.animate.set_value(2*PI), omega.animate.set_value(3), run_time=10)
        
        self.play(FadeOut(vector), FadeOut(cosSinVectorCoords), FadeOut(VGroup(tEquals, tDecimal)), FadeOut(VGroup(omegaEquals, omegaDecimal)))
        
        gofx = lambda x: cos(2*x*PI)+1
        functionAxes = Axes(
            x_range=[0,10,1],
            y_range=[0,5,1],
            x_length=10,
            y_length=5,
            tips=True,
            axis_config={"include_numbers":True}
        ).scale(0.5).to_corner(UL, buff=0.1).add_background_rectangle(BLACK, opacity=0.5)

        gofxShow = MathTex(r"g(x) = \cos(2x\pi)+1").to_corner(UR, buff=1)

        self.play(Create(functionAxes), Create(gofxShow))
        self.play(Create(functionAxes.plot(gofx, x_range=[0,10], use_smoothing=True, color=YELLOW_B)))
        self.play(ReplacementTransform(eithetawfreq, eithetawfreqafunc))
        t.set_value(0)
        vector2 = always_redraw(lambda: Vector([gofx(t.get_value())*np.cos(-2*PI*t.get_value()*omega.get_value()), gofx(t.get_value())*np.sin(-2*PI*t.get_value()*omega.get_value())]).set_color(GREEN_B))
        omega.set_value(1)
        windedFunc = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([
                (cos(2*x*PI)+1) * np.cos(-2*PI*x*omega.get_value()),
                (cos(2*x*PI)+1) * np.sin(-2*PI*x*omega.get_value()),
                0
            ]),
            t_range=np.array([0, t.get_value()]),
        ).set_color(YELLOW_B))
        self.play(GrowFromPoint(vector2, ORIGIN), Create(windedFunc))
        self.play(t.animate.set_value(10), run_time=10)
        self.wait(2)
        self.play(omega.animate.set_value(2), run_time=5)
        self.wait()
        self.play(omega.animate.set_value(4), run_time=5)
        self.wait()

class S3(Scene):
    def construct(self):
        transformedPlane = NumberPlane(
            x_range=[-10,10,1],
            y_range=[-5,5,1],
            background_line_style={
                "stroke_color": GREEN_B
            },
        )

        functionAxes = Axes(
            x_range=[0,15,1],
            y_range=[0,5,1],
            x_length=15,
            y_length=5,
            tips=True,
            axis_config={"include_numbers":True}
        ).scale(0.5).to_corner(UL)
        gofx = lambda x: cos(2*PI*x)+cos(3*PI*x)/+2
        gofxShow = MathTex(r"\cos(2\pi t)+\cos(3\pi t)+2").to_corner(UR, buff=0.5).shift(DOWN*1)

        self.play(Create(functionAxes))
        surroundingRecFuncAxes = SurroundingRectangle(functionAxes, BLUE)
        self.play(Create(surroundingRecFuncAxes), Write(gofxShow))
        
        self.play(DrawBorderThenFill(transformedPlane))

        compositeFunc = functionAxes.plot(lambda x: cos(2*x*PI)+cos(3*x*PI)+2, x_range = [0,15], use_smoothing=True, color=RED_B)
        compositeFunc2 = functionAxes.plot(lambda x: cos(2*x*PI)+cos(3*x*PI)+2, x_range = [0,15], use_smoothing=True, color=RED_B)
        self.play(Create(compositeFunc), run_time = 3)
        self.play(Create(compositeFunc2), run_time = 0.1)
        self.wait(1)

        windSlider = ValueTracker(0)
        windedFunc = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([
                ((cos(2*x*PI)+cos(3*x*PI)+2)) * np.cos(-2*PI*x*windSlider.get_value()),
                ((cos(2*x*PI)+cos(3*x*PI)+2)) * np.sin(-2*PI*x*windSlider.get_value()),
                0
            ]),
            t_range=np.array([0, 15]),
        ).set_color(RED_B))

        self.play(ReplacementTransform(compositeFunc, windedFunc))

        self.play(FadeOut(VGroup(compositeFunc, compositeFunc2, functionAxes, gofxShow, surroundingRecFuncAxes)))

        #.move_to(transformedPlane.get_center())
        
        comPoint = always_redraw(lambda: Dot(windedFunc.get_center_of_mass(), color=YELLOW_B, radius=0.08))

        self.play(FadeIn(comPoint))

        fourierAxes = Axes(
            x_range=[0,2,1],
            y_range=[-1,1,0.5],
            x_length=10,
            y_length=5,
            tips=True,
            axis_config={"include_numbers":True}
        ).scale(0.7).to_corner(DR, buff=0.5).add_background_rectangle(color=BLACK, opacity=0.5)

        accuracyOfSum = 200
        def lambdaFourier(f):
            returnVal = 0
            for i in [float(j) / 100 for j in range(100, 1500, 1)]:
                returnVal += gofx(i)*cos(-2*PI*(i)*f)
            return returnVal

        self.play(Create(fourierAxes))
        self.play(Create(SurroundingRectangle(fourierAxes, color=YELLOW_B)))

        fourierFunction = always_redraw(lambda: fourierAxes.plot(
            lambda x: lambdaFourier(x)/800
        ).set_color(YELLOW_B))

        fourierTrackDot = always_redraw(lambda: Dot().move_to(fourierAxes.c2p(windSlider.get_value(), lambdaFourier(windSlider.get_value())/800)))

        self.play(FadeIn(fourierTrackDot))
        self.play(Create(TracedPath(fourierTrackDot.get_center, stroke_color=YELLOW_B, stroke_width=4)))
        self.wait(2)

        self.play(windSlider.animate.set_value(1), run_time=5)
        self.play(windSlider.animate.set_value(1.5), run_time=5)
        self.play(windSlider.animate.set_value(2), run_time=5)
        self.wait(2)

        finalFormula = MathTex(r'\hat{g}(\omega)=\int g(t)\cos(-2\pi\omega t) dt').shift(UP*3).set_color_by_gradient(RED_B, GREEN_B).add_background_rectangle(color=BLACK, opacity=0.5)
        self.play(Create(finalFormula))

        self.play(Circumscribe(finalFormula, color=BLUE_B, fade_out=True))

        self.wait()

class S4(Scene):
    def construct(self):
        textFinal = Text("We have finished with Fourier, Merry Christmas!").scale(0.7).shift(UP*3).set_color_by_gradient(RED_A, GREEN_B)
        textFinal2 = Text("We now have the formula:").scale(0.7).shift(UP*1.7).set_color_by_gradient(BLUE_B, LIGHT_BROWN)
        equation = MathTex('e^{it} = \cos(t) + i\sin(t)')
        equation2 = MathTex('e^{-2\pi it\omega} = \cos(-2\pi t\omega) + i\sin(-2\pi t\omega)')
        equation3 = MathTex('g(x)e^{-2\pi it\omega} = g(x)\cos(-2\pi t\omega) + ig(x)\sin(-2\pi t\omega)')
        equation4 = MathTex(r'\hat{g}(\omega)=\int g(t)\cos(-2\pi\omega t) dt')

        self.play(Write(textFinal))
        self.play(Write(textFinal2))
        self.wait()
        self.play(Write(equation))
        self.play(ReplacementTransform(equation, equation2))
        self.play(ReplacementTransform(equation2, equation3))
        self.play(ReplacementTransform(equation3, equation4))
        
        bounding = SurroundingRectangle(equation4).set_color_by_gradient(RED_B, GREEN_B)
        self.wait()
        self.play(Create(bounding))

        finalThing = MarkupText(f'Finally, I would like to thank <span foreground="{YELLOW_B}">Justin Tran</span> and...').scale(0.7).shift(DOWN*1.5)
        manimLogo = ManimBanner().scale(0.3).shift(DOWN*3)
        self.wait()
        self.play(Write(finalThing))
        self.play(manimLogo.create())
        self.wait()
        self.play(manimLogo.expand())
        self.wait()


#py -3.10-64 -m manim -pqm manim13.py S1
#py -3.10-64 -m manim -pqm manim13.py S2
