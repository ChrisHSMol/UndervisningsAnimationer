import numpy as np
import random
import os
import shapely.geometry as geom
_preamble = [
    "\\documentclass[fleqn]{article}\n",
    "\\usepackage{opgaver}\n",
    "\\usepackage{multicol}\n",
    "\\usepackage{xcolor}\n",
    "\\usepackage{amsmath}\n",
    "\\pagestyle{empty}\n",
    "\n"
]
# _target = "C:\\Users\\KG-chri12mz\\OneDrive - IT Center Fyn\\Desktop\\Supermatematik\\genererede_opgaver"
_target = r"C:\Users\frhf-cm\PycharmProjects\UndervisningsAnimationer\misc_files\genererede_opgaver"


class Opgave():
    def skriv_opgaver_til_fil(self, filnavn, opgaver, opgavetekst=None, opgavetekst2=None, vspace=2, multicols=3, align=False):
        for _ in range(random.randint(5, 15)):
            random.shuffle(opgaver)
        with open(filnavn, "w") as outFile:
            if filnavn.endswith(".tex"):
                [outFile.write(l) for l in _preamble]
                outFile.write("\\begin{document}\n\n")
                outFile.write(f"\\begin{{multicols}}{multicols}\n\n")

            for opgave in opgaver:
                outFile.write("\\section{}\n")
                if opgavetekst is not None:
                    outFile.write(f"{opgavetekst}\n")
                if align:
                    outFile.write(r"\begin{align*}" + str(opgave[0]) + r"\end{align*}")
                else:
                    outFile.write(f"\\[{opgave[0]}\\]")
                if opgavetekst2 is not None:
                    outFile.write(f"{opgavetekst2}\n")
                outFile.write(f"\n% \\[{opgave[1]}\\]")
                outFile.write(f"\n\\vspace{{{vspace}cm}}\n\n")

            if filnavn.endswith(".tex"):
                outFile.write("\\end{multicols}\n\n")
                outFile.write("\\end{document}\n\n")
        return filnavn


class LigningsLoesning(Opgave):
    # def sammenbland_opgaver_og_skriv_til_fil(self, filnavn, opgaver):
    #     for _ in range(5):
    #         random.shuffle(opgaver)
    #     self.skriv_ligninger_til_fil(filnavn, opgaver)
    #
    # def skriv_ligninger_til_fil(self, filnavn, ligninger):
    #     with open(filnavn, "w") as outFile:
    #         for ligning in ligninger:
    #             outFile.write("\\section{}\n")
    #             outFile.write("Løs ligningen:\n")
    #             outFile.write(f"\\[{ligning[0]}\\]")
    #             outFile.write(f"\n% \\[{ligning[1]}\\]")
    #             outFile.write("\n\\vspace{1.5cm}\n\n")

    def generer_ligninger_ud_fra_koefficienter(self, n_opgaver, x_min, x_max):
        # ax + b = cx + d <=> x = (d - b)/(a - c)
        resultater = []
        for iopg in range(n_opgaver):
            a, b, c, d = 0, 0, 0, 0
            while a == c and b == d:
                a, b, c, d = 0, 0, 0, 0
                while a == 0:
                    a = random.randint(x_min, x_max)
                while b == 0:
                    b = random.randint(x_min, x_max)
                while c == 0:
                    c = random.randint(x_min, x_max)
                while d == 0:
                    d = random.randint(x_min, x_max)
            try:
                while not ((d - b) / (a - c)).is_integer():
                    d += 1
            except:
                continue
            asign = ""
            bsign = "+" if b >= 0 else ""
            csign= ""
            dsign = "+" if d >= 0 else ""

            equation = f"{asign} {a} x {bsign} {b} = {csign} {c} x {dsign} {d}"
            solution = f"x = {int((d - b) / (a - c))}"
            resultater.append([equation, solution])
        return resultater

    def generer_ligninger_med_uniforme_loesninger(self, n_opgaver_pr_loesning, n_forskellige_loesninger, x_min, x_max,
                                                  b_shuffle):
        # ax + b = cx + d <=> x = (d - b)/(a - c)
        loesninger = []
        for iloes in range(n_forskellige_loesninger):
            l = random.randint(x_min, x_max)
            while l in loesninger or l in [-1, 0, 1]:
                l = random.randint(x_min, x_max)
            loesninger.append(l)
            print(l)
        resultater = []
        for loesning in loesninger:
            for iopg in range(n_opgaver_pr_loesning):
                a, b, c = 0, 0, 0
                while a == c:
                    a, b, c = 0, 0, 0
                    # while a in [0, 1]:
                    while a == 0:
                        a = random.randint(x_min, x_max)
                    while b == 0:
                        b = random.randint(x_min, x_max)
                    # while c in [0, 1]:
                    while c == 0:
                        c = random.randint(x_min, x_max)
                d = loesning * (a - c) + b
                asign = ""
                bsign = "+" if b >= 0 else ""
                csign = ""
                dsign = "+" if d >= 0 else ""

                # equation = f"{asign} {a} x {bsign} {b} = {csign} {c} x {dsign} {d}"
                equation = ""
                for _tal, _tegn, _led in zip([a, b, c, d], [asign, bsign, csign, dsign], ["x", " = ", "x", ""]):
                    if _tal == 0:
                        continue
                    elif np.abs(_tal) == 1 and _led == "x":
                        _tegn = "-" if _tal < 0 else ""
                        _tal = ""
                    equation += f" {_tegn} {_tal} {_led}"
                solution = f"x = {int((d - b) / (a - c))}"
                resultater.append([equation, solution])
        if b_shuffle:
            for _ in range(5):
                random.shuffle(resultater)
        return resultater

    def generer_ligninger_med_parenteser(self, n_opgaver_pr_loesning, n_forskellige_loesninger, x_min, x_max, b_shuffle):
        # a * (bx + c) = d <=> x = (d/a - c)/b
        loesninger = []
        for iloes in range(n_forskellige_loesninger):
            l = random.randint(x_min, x_max)
            while l in loesninger or l in [-1, 0, 1]:
                l = random.randint(x_min, x_max)
            loesninger.append(l)
            # print(l)
        resultater = []
        for loesning in loesninger:
            for iopg in range(n_opgaver_pr_loesning):
                a, b, c, d = 2, 1, 0, 1
                while not (d/a).is_integer():
                    a, d = 0, 0
                    while a  in [0, 1]:
                        a = random.randint(x_min, x_max)
                    while d == 0:
                        d = random.randint(x_min, x_max)
                while c == 0 or d/a == c or not ((d/a - c)/loesning).is_integer():
                    c = random.randint(x_min, x_max)
                    b = (d/a - c)/loesning
                b = int(b)
                # while b == 0 or not ((d/a - c)/b).is_integer():
                #     b = random.randint(x_min, x_max)
                # b = (d/a - c) / loesning
                # a, b, c = 0, 0, 0
                # while a == c:
                #     a, b, c = 0, 0, 0
                #     while a == 0:
                #         a = random.randint(x_min, x_max)
                #     while b == 0:
                #         b = random.randint(x_min, x_max)
                #     while c == 0:
                #         c = random.randint(x_min, x_max)
                # d = loesning * (a - c) + b
                asign = ""
                bsign = ""
                csign = "+" if c >= 0 else ""
                dsign = ""

                # equation = f"{asign} {a} \\cdot ({bsign} {b} x {csign} {c}) = {dsign} {d}"
                equation = ""
                for _tal, _tegn, _led in zip([a, b, c, d], [asign, bsign, csign, dsign], ["\\cdot (", "x", ") = ", ""]):
                    if _tal == 0:
                        continue
                    elif np.abs(_tal) == 1 and _led == "x":
                        _tegn = _tegn if _tal < 0 else ""
                        _tal = ""
                    equation += f" {_tegn} {_tal} {_led}"
                solution = f"x = {int((d/a - c)/b)}"
                resultater.append([equation, solution])
        if b_shuffle:
            for _ in range(5):
                random.shuffle(resultater)
        return resultater


class ParablersTopOgNulpunkter(Opgave):
    def load_polynomium_koefficienter(self, filnavn):
        resultater = []
        with open(filnavn, "r") as inFile:
            for line in inFile:
                a, b, c = line.split(",")
                for p in (1, -1):
                    a, b, c = int(a) * p, int(b) * p, int(c) * p
                    asign = ""
                    bsign = "+" if b >= 0 else ""
                    csign = "+" if c >= 0 else ""
                    opgave = f"f(x) = {asign} {a} x^2 {bsign} {b} x {csign} {c}"
                    d = b**2 - 4 * a * c
                    toppunkt = [-b/(2*a), -d/(4*a)]
                    resultater.append([opgave, f"(x_T, y_T)={toppunkt}\td={d}"])
        return resultater

    def generer_opgaver_om_nulpunkter_uh(self, n_forskellige_svar, n_opgaver_pr_svar, x_min, x_max, b_shuffle):
        # f(x) = ax^2 + bx + c <=> x_0 = (-b +- sqrt(d))/(2a)
        diskriminanter = []
        for iloes in range(n_forskellige_svar - 2):
            d = random.randint(0, 10)**2
            while d in diskriminanter:
                d = random.randint(0, 10)**2
            diskriminanter.append(d)
        for iloes in range(2):
            d = -1 * random.randint(1, 10)
            while d in diskriminanter:
                d = -1 * random.randint(1, 10)
            diskriminanter.append(d)
        print(diskriminanter)

        resultater = []
        for d in diskriminanter:
            print(f"d = {d}")
            for iopg in range(n_opgaver_pr_svar):
                a, b, c = 0, 0, 0
                a_counter = 0
                x0 = [1000.0 for _ in range(2)]
                # while (a == 0 or b**2 - 4 * a * c != d) and a_counter < 1000:
                while (a == 0 or not sum(x0).is_integer() or not c.is_integer()) and a_counter < 1000:
                    a = 0
                    while a == 0:
                        a = random.randint(x_min, x_max)
                    b = random.randint(x_min, x_max)
                    # c = random.randint(x_min, x_max)
                    c = (b**2 - d)/(4*a)
                    if d >= 0:
                        [(-b + _sign * d ** 0.5) / (2 * a) for _sign in [1, -1]]
                    # x0 = [np.nan for _ in range(2)] if d < 0 else [(-b + _sign * d**0.5)/(2*a) for _sign in [1, -1]]
                    a_counter += 1
                if a_counter == 1000:
                    print(f"Opgave med d = {d} fejlede efter 1000 forsøg")
                    continue
                c = int(c)
                x0 = "N/A" if d < 0 else -b/(2*a) if d == 0 else [(-b + _sign * d**0.5)/(2*a) for _sign in [1, -1]]
                print(f"Opgave med d = {d} or x_0 = {x0} lavet i {a_counter} forsøg")
                asign = ""
                bsign = "+" if b >= 0 else ""
                csign = "+" if c >= 0 else ""

                # equation = f"f(x) = {asign} {a} x^2 {bsign} {b} x {csign} {c}"
                equation = "f(x) = "
                for _tal, _tegn, _led in zip([a, b, c], [asign, bsign, csign], ["x^2", "x", ""]):
                    if _tal == 0:
                        continue
                    elif np.abs(_tal) == 1 and _led != "":
                        if _led == "x^2":
                            _tegn = _tegn if _tal < 0 else ""
                        _tal = ""
                    equation += f" {_tegn} {_tal} {_led}"
                solution = f"x_0 = {x0} \t d = {d}"
                resultater.append([equation, solution])
            if a_counter == 1000:
                break
        if b_shuffle:
            for _ in range(5):
                random.shuffle(resultater)
        return resultater


class DifferentialRegning(Opgave):
    def generer_opgaver_om_polynomier(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            opgave = "f(x) = "
            if random.random() <= 0.5:
                maks_orden = 2
            else:
                maks_orden = random.randint(3, 6)
            for i in range(maks_orden + 1):
                orden = maks_orden - i
                koeff = random.randint(-2, 2)
                if i == 0:
                    while koeff == 0:
                        koeff = random.randint(-10, 10)
                if koeff == 0:
                    continue
                # else:
                _koeff = str(koeff)

                # _sign = "" if i == 0 else "+"
                _sign = ""
                if i > 0 and koeff > 0:
                    _sign = "+"

                # _orden = str(orden) if orden > 1 else ""
                _orden = str(orden)
                if orden <= 1:
                    _orden = ""

                # _led = "x^" if orden > 1 else "x" if orden > 0 else ""
                _led = ""
                if orden > 0:
                    _led += "x"
                if orden > 1:
                    _led += "^"

                if np.abs(koeff) == 1 and orden != 0:
                    _koeff = ""
                    _sign = "+" if i != 0 else ""
                opgave += f"{_sign}{_koeff}{_led}{_orden}  "
            opgaver.append([opgave, ""])
        return opgaver

    def generer_opgaver_om_blandede_funktioner(self, n_opgaver):
        opgaver = []
        funktionstyper = [r"\ln(x)", r"\frac{1}{x}", r"\frac{1}{x^2}", r"\frac{1}{x^3}", r"\mathrm{e}^x"]
        for iopg in range(n_opgaver):
            opgave = "f(x) = "
            if random.random() <= 0.75:
                n_led = 3
            else:
                n_led = random.randint(4, 6)
            for i in range(n_led):
                if random.random() <= 0.25:
                    opgave += "" if i == 0 else "+"
                    led = random.choice(funktionstyper)
                    while led in opgave:
                        led = random.choice(funktionstyper)
                    opgave += led
                    continue
                orden = random.randint(0, 5)
                koeff = random.randint(-2, 2)
                if i == 0:
                    while koeff == 0:
                        koeff = random.randint(-10, 10)
                if koeff == 0:
                    continue
                # else:
                _koeff = str(koeff)

                # _sign = "" if i == 0 else "+"
                _sign = ""
                if i > 0 and koeff > 0:
                    _sign = "+"

                # _orden = str(orden) if orden > 1 else ""
                _orden = str(orden)
                if orden <= 1:
                    _orden = ""

                # _led = "x^" if orden > 1 else "x" if orden > 0 else ""
                _led = ""
                if orden > 0:
                    _led += "x"
                if orden > 1:
                    _led += "^"

                if np.abs(koeff) == 1 and orden != 0:
                    _koeff = ""
                    _sign = "+" if i != 0 else ""
                opgave += f"{_sign}{_koeff}{_led}{_orden}  "
            opgaver.append([opgave, ""])
        return opgaver


class VektorRegning(Opgave):
    def generer_opgaver_om_prikprodukt(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            koefs = []
            opgave = ""
            for ivek, vname in enumerate([r"\vec{a}", r"\vec{b}"]):
                vx, vy = [random.randint(-10, 10) for _ in range(2)]
                koefs.append([vx, vy])
                opgave += rf"{vname} = \begin{{pmatrix}} {vx} \\ {vy} \end{{pmatrix}}"
                opgave += r"\text{ og }" if ivek == 0 else ""
            sol = koefs[0][0]*koefs[1][1] - koefs[0][1]*koefs[1][0]
            opgaver.append([opgave, sol])
        return opgaver

    def generer_opgaver_om_retningsvektorer(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            koefs = []
            opgave = ""
            for pname, ender in zip(["A", "B", "C"], [", ", " og ", ". "]):
                px, py = [random.randint(-5, 10) for _ in range(2)]
                koefs.append([px, py])
                opgave += rf"{pname}({px}, {py})\text{{{ender}}}"
            sol = [np.array(koefs[1]) - np.array(koefs[0]), np.array(koefs[2]) - np.array(koefs[0])]
            opgaver.append([opgave, sol])
        return opgaver

    def generer_opgaver_om_linjens_ligning(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            px, py = [random.randint(-5, 10) for _ in range(2)]
            nx, ny = [random.randint(-5, 5) for _ in range(2)]
            while 0 in [px, py]:
                px, py = [random.randint(-5, 10) for _ in range(2)]
            while 0 in [nx, ny]:
                nx, ny = [random.randint(-5, 5) for _ in range(2)]
            opgave = rf"P({px}, {py}) \quad \vec{{n}}=\begin{{pmatrix}} {nx}\\{ny} \end{{pmatrix}}."
            sol = f"{nx}x + {ny}y + {nx*(-px) + ny*(-py)} = 0"
            opgaver.append([opgave, sol])
        return opgaver


class Geometri(Opgave):
    def generer_cirkelligning_fra_centrum_og_radius(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            opgave = ""
            cx, cy, r = 0, 0, 0
            while (cx == 0 and cy == 0) or r == 0:
                cx = random.randint(-10, 10)
                cy = random.randint(-10, 10)
                r = random.randint(1, 10)
            opgave += f"C({cx},{cy}) \\quad r={r}"
            svar = "(x"
            svar += "-" if cx >= 0 else "+"
            svar += f"{np.abs(cx)})^2 + (y"
            svar += "-" if cy >= 0 else "+"
            svar += f"{np.abs(cy)})^2 = "
            svar += "(" if r < 0 else ""
            svar += f"{r}"
            svar += ")" if r < 0 else ""
            svar += "^2"
            opgaver.append([opgave, svar])
        return opgaver

    def generer_kryds_af_linjer(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            a1, b1, c1 = 0, 0, 0
            a2, b2, c2 = 0, 0, 0
            # while a1 == a2 or b1 == b2:
            while a2*b1 - a1*b2 == 0 or b1*b2 == 0 or a1*a2 == 0 or not ((c1*b2-c2*b1)/(a2*b1-a1*b2)).is_integer():
                a1, a2, b1, b2, c1, c2 = [random.randint(-10, 10) for _ in range(6)]
            l = r"l: \quad &"
            l += f"{a1}x" if a1 < 0 else f"{a1}x" if a1 > 0 else ""
            l += f"{b1}y" if b1 < 0 else f"+{b1}y" if b1 > 0 else ""
            l += f"{c1}" if c1 < 0 else f"+{c1}" if c1 > 0 else ""
            l += "=0"
            m = r"m: \quad &"
            m += f"{a2}x" if a2 < 0 else f"{a2}x" if a2 > 0 else ""
            m += f"{b2}y" if b2 < 0 else f"+{b2}y" if b2 > 0 else ""
            m += f"{c2}" if c2 < 0 else f"+{c2}" if c2 > 0 else ""
            m += "=0"
            opgaver.append([
                f"{l} \\\\ {m}",
                f"({(c1*b2-c2*b1)/(a2*b1-a1*b2)}, {(-a1*(c1*b2-c2*b1)/(a2*b1-a1*b2)-c1)/b1})"
            ])
        return opgaver

    def generer_kryds_af_linje_og_cirkel(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            # a, b, c, x0, y0, r = 0, 0, 0, 0, 0, 0
            # while r == 0 or a*b*c == 0:
                # a, b, c, x0, y0 = [random.randint(-10, 10) for _ in range(5)]
                # x0, y0 = [random.randint(-10, 10) for _ in range(2)]
                # r = random.randint(1, 10)
                # TODO: Find ud af, hvordan man kan lave skæringen mellem linjen og cirklen afhænge af c
                # TODO: så man kan skrue på c indtil man har en tilfredsstillende løsning

            x0, y0 = [random.randint(-10, 10) for _ in range(2)]
            r = random.randint(1, 10)
            circ = geom.Point(x0, y0).buffer(r, 40).boundary

            p1, p2 = [random.choice(circ.__geo_interface__["coordinates"]) for _ in range(2)]
            line = geom.LineString([p1, p2])
            inter = circ.intersection(line)
            i = 0
            # for _k in np.linspace(-2, 2, 401):
            #     if np.abs(np.abs(_k-np.round(_k, 0))-0.5) <= 1E-3:
            #         print(_k, np.abs(_k-np.round(_k, 0))-0.5)
            # while (
            #         not (np.abs(p1[0]-int(p1[0])) <= 1E-2 or np.abs(p1[0]-np.round(p1[0], 0))+0.5 <= 1E-3) or
            #         not (np.abs(p1[1]-int(p1[1])) <= 1E-2 or np.abs(p1[1]-np.round(p1[1], 0))+0.5 <= 1E-3) or
            #         not (np.abs(p2[0]-int(p2[0])) <= 1E-2 or np.abs(p2[0]-np.round(p2[0], 0))+0.5 <= 1E-3) or
            #         not (np.abs(p2[1]-int(p2[1])) <= 1E-2 or np.abs(p2[1]-np.round(p2[1], 0))+0.5 <= 1E-3) or
            #         np.abs(p1[0]-p2[0]) <= 1E-2 or type(inter) != geom.MultiPoint
            # ) and i < 1E5:
            while i < 1E6:
                # print(inter)
                # p1 = random.choice(circ.__geo_interface__["coordinates"])
                # p2 = random.choice(circ.__geo_interface__["coordinates"])
                p1, p2 = [random.choice(circ.__geo_interface__["coordinates"]) for _ in range(2)]
                line = geom.LineString([p1, p2])
                inter = circ.intersection(line)
                i += 1
                if (
                        (np.abs(p1[0]-int(p1[0])) <= 1E-2 or np.abs(np.abs(p1[0]-np.round(p1[0], 0))-0.5) <= 1E-2) and
                        (np.abs(p1[1]-int(p1[1])) <= 1E-2 or np.abs(np.abs(p1[1]-np.round(p1[1], 0))-0.5) <= 1E-2) and
                        (np.abs(p2[0]-int(p2[0])) <= 1E-2 or np.abs(np.abs(p2[0]-np.round(p2[0], 0))-0.5) <= 1E-2) and
                        (np.abs(p2[1]-int(p2[1])) <= 1E-2 or np.abs(np.abs(p2[1]-np.round(p2[1], 0))-0.5) <= 1E-2) and
                        # np.abs(2*p1[0] - np.round(2*p1[0], 0)) <= 1E-2 and
                        # np.abs(2*p1[1] - np.round(2*p1[1], 0)) <= 1E-2 and
                        # np.abs(2*p2[0] - np.round(2*p2[0], 0)) <= 1E-2 and
                        # np.abs(2*p2[1] - np.round(2*p2[1], 0)) <= 1E-2 and
                        np.abs(p1[0]-p2[0]) > 1E-2 and type(inter) == geom.MultiPoint
                ):
                    # print(np.abs(np.abs(p1[0]-np.round(p1[0], 0))-0.5))
                    # print(p1)
                    break
            print(i, inter)
            a = int((p2[1] - p1[1])/(p2[0] - p1[0]))
            b = -1
            c = int(p2[1] - a*p2[0])
            # geom.MultiPoint
            l = r"l:& \quad"
            l += f"{a}x" if a < 0 else f"{a}x" if a > 0 else ""
            l += f"{b}y" if b < 0 else f"+{b}y" if b > 0 else ""
            l += f"{c}" if c < 0 else f"+{c}" if c > 0 else ""
            l += "=0"
            C = r"C:& \quad(x"
            C += "-" if x0 >= 0 else "+"
            C += f"{np.abs(x0)})^2 + (y"
            C += "-" if y0 >= 0 else "+"
            C += f"{np.abs(y0)})^2 = "
            C += "(" if r < 0 else ""
            C += f"{r}"
            C += ")" if r < 0 else ""
            C += "^2"
            # opgave = f"l: {a}x{b}y+{c}=0 \\\\ C({x0}, {y0}), r={r}"
            opgave = f"{l} \\\\ {C}"
            svar = f"{inter.geoms[0].__geo_interface__['coordinates']}, {inter.geoms[1].__geo_interface__['coordinates']}"
            opgaver.append([opgave, svar])
        return opgaver


class ToPunkt(Opgave):
    def generer_to_punkt_formel_linear(self, n_opgaver):
        opgaver = []
        for iopg in range(n_opgaver):
            opgave = ""
            a, b = 0, 0
            while a == 0 or b == 0:
                a = random.randint(-5, 5)
                b = random.randint(-10, 10)

            x1, x2 = 0, 0
            while x2 <= x1:
                x1, x2 = [random.randint(-5, 10) for _ in range(2)]
            y1, y2 = [a * x + b for x in [x1, x2]]
            opgave += f"A({x1}, {y1}) \\quad B({x2}, {y2})"
            svar = f"y = {a} * x "
            svar += "+" if b >= 0 else ""
            svar += f" {b}"
            opgaver.append([opgave, svar])
        return opgaver


# r = LigningsLoesning()
# ul = r.generer_ligninger_med_uniforme_loesninger(
#     n_forskellige_loesninger=18,
#     n_opgaver_pr_loesning=5,
#     x_min=-10,
#     x_max=10,
#     b_shuffle=True
# )
# pl = r.generer_ligninger_med_parenteser(
#     n_forskellige_loesninger=18,
#     n_opgaver_pr_loesning=5,
#     x_min=-10,
#     x_max=10,
#     b_shuffle=True
# )
# resultater = ul + pl
# for res in resultater:
#     print("\\section{}\n", "Løs ligningen:\n", f"\\[{res[0]}\\]", f"\n% \\[{res[1]}\\]", "\n\\vspace{2cm}\n")
# filnavn = r.skriv_opgaver_til_fil(
#     "ligningsløsning.tex", resultater, opgavetekst="Løs ligningen:", vspace=3
# )

# parabel = ParablersTopOgNulpunkter()
# resultater = parabel.load_polynomium_koefficienter("parabel_toppunkt_koefficienter.txt")
# filnavn = parabel.skriv_opgaver_til_fil(
#     "parablens_toppunkt.tex", resultater, opgavetekst="Find koordinatsættet til toppunktet for parablen:",
#     vspace=2.5
# )
# resultater = parabel.generer_opgaver_om_nulpunkter_uh(
#     n_forskellige_svar=12,
#     n_opgaver_pr_svar=5,
#     x_min=-10,
#     x_max=10,
#     b_shuffle=True
# )
# filnavn = parabel.skriv_opgaver_til_fil(
#     "parablens_nulpunkter.tex", resultater, opgavetekst="Bestem nulpunkterne for $f$:",
#     vspace=3
# )
# for res in resultater:
#     print(
#         "\\section{}\n", "Bestem nulpunkterne for f:\n",
#         f"\\[{res[0]}\\]", f"\n% \\[{res[1]}\\]", "\n\\vspace{1.5cm}\n"
#     )
#
# dif_opg = DifferentialRegning()
# opgaver = []
# opgaver += dif_opg.generer_opgaver_om_polynomier(n_opgaver=100)
# opgaver += dif_opg.generer_opgaver_om_blandede_funktioner(n_opgaver=100)
# filnavn = dif_opg.skriv_opgaver_til_fil(
#     "differentialregning.tex", opgaver, opgavetekst="En funktion $f$ er givet ved:", opgavetekst2="Bestem $f'$.",
#     vspace=3
# )

# vek_opg = VektorRegning()
# opgaver = []
# opgaver += vek_opg.generer_opgaver_om_prikprodukt(n_opgaver=48)
# filnavn = vek_opg.skriv_opgaver_til_fil(
#     "prikprodukt.tex", opgaver,
#     opgavetekst="I et koordinatsystem er vektorerne $\\vec{a}$ og $\\vec{b}$ givet ved:",
#     opgavetekst2="Bestem skalarproduktet $\\vec{a}\\cdot\\vec{b}$.",
#     vspace=4
# )
# vek_opg = VektorRegning()
# opgaver = []
# opgaver += vek_opg.generer_opgaver_om_retningsvektorer(n_opgaver=48)
# filnavn = vek_opg.skriv_opgaver_til_fil(
#     "retningsvektorer.tex", opgaver,
#     opgavetekst="I et koordinatsystem er der givet punkterne:",
#     opgavetekst2="Bestem koordinatsættet til hver af vektorerne $\\overrightarrow{AB}$ og $\\overrightarrow{AC}$.",
#     vspace=4
# )
# vek_opg = VektorRegning()
# opgaver = []
# opgaver += vek_opg.generer_opgaver_om_linjens_ligning(n_opgaver=48)
# filnavn = vek_opg.skriv_opgaver_til_fil(
#     "linjens_ligning.tex", opgaver,
#     opgavetekst="En linje $l$ går gennem punktet $P$ og har normalvektoren $\\vec{n}$:",
#     opgavetekst2="Opskriv en ligning for $l$.",
#     vspace=4
# )

# geom_opg = Geometri()
# opgaver = []
# opgaver += geom_opg.generer_cirkelligning_fra_centrum_og_radius(n_opgaver=60)
# filnavn = geom_opg.skriv_opgaver_til_fil(
#     "cirklens_ligning.tex", opgaver,
#     opgavetekst="En cirkel har centrum $C$ og radius $r$ som følger:",
#     opgavetekst2="Bestem en ligning for cirklen.",
#     vspace=2.5
# )
# geom_opg = Geometri()
# opgaver = []
# opgaver += geom_opg.generer_kryds_af_linjer(n_opgaver=60)
# filnavn = geom_opg.skriv_opgaver_til_fil(
#     "skæring_mellem_linjer.tex", opgaver,
#     opgavetekst="To linjer $l$ og $m$ er givet ved:",
#     opgavetekst2="Bestem koordinatsættet til skæringspunktet mellem $l$ og $m$.",
#     vspace=4,
#     align=True
# )
# geom_opg = Geometri()
# opgaver = []
# opgaver += geom_opg.generer_kryds_af_linje_og_cirkel(n_opgaver=24)
# filnavn = geom_opg.skriv_opgaver_til_fil(
#     "skæring_mellem_linje_og_cirkel.tex", opgaver,
#     opgavetekst="En linje $l$ og en cirkel $C$ er givet ved:",
#     opgavetekst2="Bestem koordinatsættet til skæringspunkterne mellem $l$ og $C$.",
#     vspace=4,
#     align=True
# )

to_punkt_opg = ToPunkt()
opgaver = []
opgaver += to_punkt_opg.generer_to_punkt_formel_linear(n_opgaver=48)
filnavn = to_punkt_opg.skriv_opgaver_til_fil(
    "to_punkt_formel_lin.tex", opgaver,
    opgavetekst="Bestem ligningen til grafen, som går gennem punkterne:",
    vspace=2.5
)

# for res in opgaver:
#     print(
#         "\\section{}\n",
#         "En linje $l$ og en cirkel $C$ er givet ved::\n",
#         f"\\[{res[0]}\\]", f"\n% \\[{res[1]}\\]",
#         "\nBestem koordinatsættet til skæringspunkterne mellem $l$ og $C$.",
#         "\n\\vspace{1.5cm}\n"
#     )

os.system(f"pdflatex {filnavn}")
filnavn = f"{filnavn[:-4]}.pdf"
os.replace(filnavn, f"{_target}\\{filnavn}")
[os.remove(filnavn[:-3] + ext) for ext in ["aux", "log", "out"]]
os.system(f"explorer.exe {_target}\\{filnavn}")
