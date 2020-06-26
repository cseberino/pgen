#!/usr/bin/env python3
#
# Copyright 2020 Christian Seberino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
sys.path.append("../..")

import pgen.make_parser
import pgen.add_prods
import unittest
import warnings
import string

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)

        def test_find_group(self):
                text   = "[abc(def)ghi]"
                output = pgen.add_prods.find_group(text)
                self.assertEqual(output, "(def)")

                text   = "[abc(defg(hijk)lmnop)]"
                output = pgen.add_prods.find_group(text)
                self.assertEqual(output, "(hijk)")

                text   = "[abcdefghij(((kl)))mno]"
                output = pgen.add_prods.find_group(text)
                self.assertEqual(output, "(kl)")

                text   = "[abce(fg)hijk(l)]"
                output = pgen.add_prods.find_group(text)
                self.assertEqual(output, "(fg)")

                text   = "[abcdefghij(((kl) ()))mno]"
                output = pgen.add_prods.find_group(text)
                self.assertEqual(output, "(kl)")

        def test_find_optional(self):
                text   = "(abc[def]ghi)"
                output = pgen.add_prods.find_optional(text)
                self.assertEqual(output, "[def]")

                text   = "(abc[defg[hijk]lmnop])"
                output = pgen.add_prods.find_optional(text)
                self.assertEqual(output, "[hijk]")

                text   = "(abcdefghij[[[kl]]]mno)"
                output = pgen.add_prods.find_optional(text)
                self.assertEqual(output, "[kl]")

                text   = "(abce[fg]hijk[l])"
                output = pgen.add_prods.find_optional(text)
                self.assertEqual(output, "[fg]")

                text   = "(abcdefghij[[[kl] []]]mno)"
                output = pgen.add_prods.find_optional(text)
                self.assertEqual(output, "[kl]")

        def test_arith_grammar(self):
                import arith_tokenizer
                import arith_grammar
                parser = pgen.make_parser.make_parser(arith_tokenizer,
                                                      arith_grammar)

                # ========================================================

                plus   = ("PLUS", "+")
                minus  = ("MINUS", "-")
                mult   = ("MULT", "*")
                div    = ("DIV", "/")
                lprns  = ("LPARENS", "(")
                rprns  = ("RPARENS", ")")

                # ========================================================

                nat_1  = ("NATURAL", "1")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1, plus, prod_1)
                answer = ("exp", sum_x)
                output = parser("1+1")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("exp", sum_x)
                output = parser("1234+328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1, minus, prod_1)
                answer = ("exp", sum_x)
                output = parser("1-1")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("exp", sum_x)
                output = parser("1234-328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "823")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("823")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(342)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y  = ("NATURAL", "87924")
                val_y  = ("value", nat_y)
                prod_y = ("product", val_y)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(342)*(87924)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_x = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_x)
                answer = ("exp", sum_x)
                output = parser("1234*328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_x = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_x)
                answer = ("exp", sum_x)
                output = parser("1234/328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, mult, val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("exp", sum_x)
                output = parser("11*22+3*5")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, div,  val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("exp", sum_x)
                output = parser("11/22+3*5")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, div,  val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("exp", sum_x)
                output = parser("11/22-3*5")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y  = ("NATURAL", "87924")
                val_y  = ("value", nat_y)
                prod_y = ("product", val_y)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(342)/(87924)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(23+25)/(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("exp", sum_x)
                output = parser("(23+25)+(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(23+25)*(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("exp", sum_x)
                output = parser("(23+25)-(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, minus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, div, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(23-25)/(8/723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_11 = ("NATURAL", "11")
                val_11 = ("value", nat_11)
                nat_22 = ("NATURAL", "22")
                val_22 = ("value", nat_22)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_8  = ("NATURAL", "8")
                val_8  = ("value", nat_8)
                nat_17 = ("NATURAL", "17")
                val_17 = ("value", nat_17)
                nat_4  = ("NATURAL", "4")
                val_4  = ("value", nat_4)

                p11d22 = ("product", val_11, div, val_22)
                p8d17  = ("product", val_8, div, val_17)
                p3     = ("product", val_3)
                p4     = ("product", val_4)

                sumone = ("sum", p11d22, plus, p3)
                sumtwo = ("sum", p8d17, minus, p4)

                expone = ("exp", sumone)
                exptwo = ("exp", sumtwo)

                valone = ("value", lprns, expone, rprns)
                valtwo = ("value", lprns, exptwo, rprns)

                pone   = ("product", valone, div, valtwo)
                sone   = ("sum", pone)
                answer = ("exp", sone)
                output = parser("(11/22+3)/(8/17-4)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, div,  val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, plus, prod_2)
                exp_x  = ("exp", sum_x)
                val_a  = ("value", lprns, exp_x, rprns)

                nat_5  = ("NATURAL", "8")
                val_5  = ("value", nat_5)
                nat_6  = ("NATURAL", "17")
                val_6  = ("value", nat_6)
                nat_7  = ("NATURAL", "4")
                val_7  = ("value", nat_7)
                nat_8  = ("NATURAL", "6")
                val_8  = ("value", nat_8)
                prod_3 = ("product", val_5, div,  val_6)
                prod_4 = ("product", val_7, mult, val_8)
                sum_y  = ("sum", prod_3, minus, prod_4)
                exp_y  = ("exp", sum_y)
                val_b  = ("value", lprns, exp_y, rprns)

                prod_z = ("product", val_a, div, val_b)
                sum_z  = ("sum", prod_z)
                answer = ("exp", sum_z)
                output = parser("(11/22+3*5)/(8/17-4*6)")
                self.assertEqual(output, answer)

                n      = 10 * [[]]
                v      = 10 * [[]]
                p      = 10 * [[]]
                for i in range(1, 10):
                        n[i] = ("NATURAL", str(i))
                        v[i] = ("value",   n[i])
                        p[i] = ("product", v[i])

                # ========================================================

                s      = ("sum", p[1], plus, p[2], plus, p[3])
                answer = ("exp", s)
                output = parser("1+2+3")
                self.assertEqual(output, answer)

                s      = ("sum", p[7], plus, p[8], plus, p[9], plus, p[3])
                answer = ("exp", s)
                output = parser("7+8+9+3")
                self.assertEqual(output, answer)

                s      = ("sum", p[7], plus, p[8], minus, p[9], plus, p[3])
                answer = ("exp", s)
                output = parser("7+8-9+3")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], mult, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("exp", s)
                output = parser("5*4*2*7")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], div, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("exp", s)
                output = parser("5*4/2*7")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], div, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("exp", s)
                output = parser("5*4/2*7")
                self.assertEqual(output, answer)

                p5t4   = ("product", v[5], mult, v[4])
                s5t4   = ("sum", p5t4)
                e5t4   = ("exp", s5t4)
                v5t4   = ("value", lprns, e5t4, rprns)
                pxd2t7 = ("product", v5t4, div, v[2], mult, v[7])
                p9t1d3 = ("product", v[9], mult, v[1], div, v[3])
                p8t3d5 = ("product", v[8], mult, v[3], div, v[5])
                p6     = ("product", v[6])
                p3     = ("product", v[3])
                sxm6   = ("sum", p8t3d5, minus, p6)
                exm6   = ("exp", sxm6)
                vxm6   = ("value", lprns, exm6, rprns)
                pxm6   = ("product", vxm6)
                s      = ("sum", pxd2t7, plus, p3, minus, p9t1d3, plus, pxm6)
                answer = ("exp", s)
                output = parser("(5*4)/2*7+3-9*1/3+(8*3/5-6)")
                self.assertEqual(output, answer)

        def test_adds_grammar(self):
                import adds_tokenizer
                import adds_grammar
                parser = pgen.make_parser.make_parser(adds_tokenizer,
                                                      adds_grammar)

                # ========================================================

                for let in string.ascii_lowercase:
                        setattr(sys.modules[__name__], let, (let.upper(), let))

                answer = ("start", ("one_or_more", b))
                output = parser("b")
                self.assertEqual(output, answer)

                answer = ("start", ("one_or_more", b, b, b, b, b))
                output = parser("bbbbb")
                self.assertEqual(output, answer)

                answer = ("start", ("zero_or_more", d))
                output = parser("d")
                self.assertEqual(output, answer)

                answer = ("start", ("zero_or_more", d, a))
                output = parser("da")
                self.assertEqual(output, answer)

                answer = ("start", ("zero_or_more", d, a, a, a, a, a))
                output = parser("daaaaa")
                self.assertEqual(output, answer)

                answer = ("start", ("optional", c, e))
                output = parser("ce")
                self.assertEqual(output, answer)

                answer = ("start", ("optional", e))
                output = parser("e")
                self.assertEqual(output, answer)

                answer = ("start", ("group", f, g))
                output = parser("fg")
                self.assertEqual(output, answer)

                answer = ("start", ("group", f, h))
                output = parser("fh")
                self.assertEqual(output, answer)

                answer = ("start", ("set", i, j, k))
                output = parser("ijk")
                self.assertEqual(output, answer)

        def test_min_c_var_tokenizer(self):
                import min_c_var_tokenizer

                for e in [("+=",       "ADD_EQ"),
                          ("&",        "AMPER"),
                          ("~",        "BIT_COMP"),
                          ("|",        "BIT_OR"),
                          ("^",        "BIT_XOR"),
                          ("break",    "BREAK"),
                          ("&=",       "B_AND_EQ"),
                          ("|=",       "B_OR_EQ"),
                          ("^=",       "B_XOR_EQ"),
                          ("char",     "CHAR"),
                          (",",        "COMMA"),
                          ("continue", "CONTINUE"),
                          ("-",        "DASH"),
                          ("/",        "DIV"),
                          ("/=",       "DIV_EQ"),
                          ("else",     "ELSE"),
                          ("=",        "EQUALS"),
                          ("==",       "EQEQ"),
                          ("for",      "FOR"),
                          (">",        "GR_THAN"),
                          (">=",       "GR_TH_EQ"),
                          ("if",       "IF"),
                          ("int",      "INT"),
                          ("&&",       "LOG_AND"),
                          ("||",       "LOG_OR"),
                          ("<",        "LS_THAN"),
                          ("<=",       "LS_TH_EQ"),
                          ("{",        "L_BRACE"),
                          ("[",        "L_BRACK"),
                          ("(",        "L_PAREN"),
                          ("<<",       "L_SHIFT"),
                          ("<<=",      "L_SH_EQ"),
                          ("%",        "MOD"),
                          ("%=",       "MOD_EQ"),
                          ("*=",       "MULT_EQ"),
                          ("!",        "LOG_NOT"),
                          ("!=",       "NOT_EQ"),
                          ("23434",    "NATURAL"),
                          ("+",        "PLUS"),
                          ("return",   "RETURN"),
                          ("}",        "R_BRACE"),
                          ("]",        "R_BRACK"),
                          (")",        "R_PAREN"),
                          (">>",       "R_SHIFT"),
                          (">>=",      "R_SH_EQ"),
                          (";",        "SEMICOL"),
                          ("sizeof",   "SIZEOF"),
                          ("*",        "STAR"),
                          ('"adf23"',  "STRING"),
                          ("-=",       "SUB_EQ"),
                          ("asdf3",    "VARIABLE"),
                          ("void",     "VOID"),
                          ("while",    "WHILE")]:
                          answer = [(e[1], e[0])]
                          output = min_c_var_tokenizer.tokenizer(e[0])
                          self.assertEqual(output, answer)

        def test_min_c_var_grammar(self):
                import min_c_var_tokenizer
                import min_c_var_grammar
                p = pgen.make_parser.make_parser(min_c_var_tokenizer,
                                                 min_c_var_grammar)

                SEMICOL    = ("SEMICOL",     ";")
                COMMA      = ("COMMA",       ",")
                STAR       = ("STAR",        "*")
                EQUALS     = ("EQUALS",      "=")
                TYPE_INT   = ("type",        ("INT",  "int"))
                TYPE_CHAR  = ("type",        ("CHAR", "char"))
                TYPE_VOID  = ("type",        ("VOID", "void"))
                L_PAREN    = ("L_PAREN",     "(")
                R_PAREN    = ("R_PAREN",     ")")
                L_BRACE    = ("L_BRACE",     "{")
                R_BRACE    = ("R_BRACE",     "}")
                VAR_I      = ("VARIABLE",    "i")
                VAR_X      = ("VARIABLE",    "x")
                VAR_Y      = ("VARIABLE",    "y")
                VAR_Z      = ("VARIABLE",    "z")
                VAR_F      = ("VARIABLE",    "f")
                VAR_G      = ("VARIABLE",    "g")
                DEC_INT_X  = ("declaration", TYPE_INT,   ("dec_base", VAR_X))
                DEC_INT_Y  = ("declaration", TYPE_INT,   ("dec_base", VAR_Y))
                DEC_CHAR_Z = ("declaration", TYPE_CHAR,  ("dec_base", VAR_Z))
                ST_INT_X   = ("statement",   ("stat_dec", DEC_INT_X,  SEMICOL))
                ST_INT_Y   = ("statement",   ("stat_dec", DEC_INT_Y,  SEMICOL))
                ST_CHAR_Z  = ("statement",   ("stat_dec", DEC_CHAR_Z, SEMICOL))
                EXP_0      = ("expression",
                              ("exp_log_and",
                               ("exp_log_not",
                                ("exp_comp",
                                 ("exp_bit_or",
                                  ("exp_bit_xor",
                                   ("exp_bit_and",
                                    ("exp_shift",
                                     ("exp_sum",
                                      ("exp_prod",
                                       ("exp_prefix",
                                        ("exp_inv_ind",
                                         ("exp_base",
                                          ("NATURAL", "0"))))))))))))))

                EXP_4      = ("expression",
                              ("exp_log_and",
                               ("exp_log_not",
                                ("exp_comp",
                                 ("exp_bit_or",
                                  ("exp_bit_xor",
                                   ("exp_bit_and",
                                    ("exp_shift",
                                     ("exp_sum",
                                      ("exp_prod",
                                       ("exp_prefix",
                                        ("exp_inv_ind",
                                         ("exp_base",
                                          ("NATURAL", "4"))))))))))))))

                output    = p("""
int f() {
        int  x;
        char z;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_func",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_F, L_PAREN, R_PAREN)),
                               ("stat_block",
                                L_BRACE, ST_INT_X, ST_CHAR_Z, R_BRACE))))
                self.assertEqual(output, answer)

                output    = p("""
char z;
int  y;

int f() {
        int  x;
        char z;
}

void g() {
        char z;
        int  x;
        int  ***y = 4;
}
""")
                s         = ("statement",
                             ("stat_dec",
                              ("declaration",
                               TYPE_INT, STAR, STAR, STAR, ("dec_base", VAR_Y),
                                                                 EQUALS, EXP_4),
                              SEMICOL))
                answer    = ("program",
                             ST_CHAR_Z,
                             ST_INT_Y,
                             ("statement",
                              ("stat_func",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_F, L_PAREN, R_PAREN)),
                               ("stat_block",
                                L_BRACE, ST_INT_X, ST_CHAR_Z, R_BRACE))),
                             ("statement",
                              ("stat_func",
                               ("declaration",
                                TYPE_VOID,
                                ("dec_base", VAR_G, L_PAREN, R_PAREN)),
                               ("stat_block",
                                L_BRACE, ST_CHAR_Z, ST_INT_X, s, R_BRACE))))
                self.assertEqual(output, answer)

                output    = p("""
int x[4];
""")
                answer    = ("program",
                             ("statement",
                              ("stat_dec",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_X, ("L_BRACK", "["), EXP_4,
                                                             ("R_BRACK", "]"))),
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
int x[4][4];
""")
                answer    = ("program",
                             ("statement",
                              ("stat_dec",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_X, ("L_BRACK", "["), EXP_4,
                                      ("R_BRACK", "]"), ("L_BRACK", "["), EXP_4,
                                                             ("R_BRACK", "]"))),
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
int f(int x, char z);
""")
                answer    = ("program",
                             ("statement",
                              ("stat_dec",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_F, ("L_PAREN", "("), DEC_INT_X,
                                          COMMA, DEC_CHAR_Z, ("R_PAREN", ")"))),
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
break;
continue;
return;
return 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_jump", ("BREAK",    "break"),    SEMICOL)),
                             ("statement",
                              ("stat_jump", ("CONTINUE", "continue"), SEMICOL)),
                             ("statement",
                              ("stat_jump", ("RETURN",   "return"),   SEMICOL)),
                             ("statement",
                              ("stat_jump",
                               ("RETURN", "return"), EXP_4, SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_exp", EXP_4, SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
if (4) {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               ("L_PAREN", "("),
                               EXP_4,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                output    = p("""
if (4) {
        break;
} else {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               ("L_PAREN", "("),
                               EXP_4,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")),
                               ("ELSE", "else"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                output    = p("""
while (4) {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("WHILE", "while"),
                               ("L_PAREN", "("),
                               EXP_4,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                output    = p("""
x = 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("exp_inv_ind", ("exp_base", VAR_X))),
                               ("assign_op", EQUALS),
                               EXP_4,
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
&x = 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("prefix_op", ("AMPER", "&")),
                                ("exp_inv_ind", ("exp_base", VAR_X))),
                               ("assign_op", EQUALS),
                               EXP_4,
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
&-~x = 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("prefix_op", ("AMPER",    "&")),
                                ("prefix_op", ("DASH",     "-")),
                                ("prefix_op", ("BIT_COMP", "~")),
                                ("exp_inv_ind", ("exp_base", VAR_X))),
                               ("assign_op", EQUALS),
                               EXP_4,
                               SEMICOL)))
                self.assertEqual(output, answer)

                sa        = ("stat_assign",
                             ("exp_prefix",
                              ("exp_inv_ind", ("exp_base", VAR_I))),
                             ("assign_op", EQUALS),
                             EXP_0,
                             SEMICOL)
                ebo_i     = ("exp_bit_or",
                             ("exp_bit_xor",
                              ("exp_bit_and",
                               ("exp_shift",
                                ("exp_sum",
                                 ("exp_prod",
                                  ("exp_prefix",
                                   ("exp_inv_ind",
                                    ("exp_base",
                                     VAR_I)))))))))
                ebo_4     = ("exp_bit_or",
                             ("exp_bit_xor",
                              ("exp_bit_and",
                               ("exp_shift",
                                ("exp_sum",
                                 ("exp_prod",
                                  ("exp_prefix",
                                   ("exp_inv_ind",
                                    ("exp_base",
                                     ("NATURAL", "4"))))))))))
                se        = ("stat_exp",
                             ("expression",
                              ("exp_log_and",
                               ("exp_log_not",
                                ("exp_comp",
                                 ebo_i,
                                 ("comp_op", ("LS_THAN", "<")),
                                 ebo_4)))),
                             SEMICOL)
                eip1      = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base", VAR_I)))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base",
                                         ("NATURAL", "1"))))))))))))))
                output    = p("""
for (i = 0; i < 4; i = i + 1) {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("FOR", "for"),
                               ("L_PAREN", "("),
                               sa,
                               se,
                               ("exp_prefix",
                                ("exp_inv_ind", ("exp_base", VAR_I))),
                               ("assign_op", EQUALS),
                               eip1,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                e         = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base", VAR_I)))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base", VAR_X)))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base",
                                         ("NATURAL", "1"))))))))))))))
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("exp_inv_ind",
                                 ("exp_base", VAR_I))),
                               ("assign_op", EQUALS),
                               e,
                               SEMICOL)))
                output    = p("""
i = i + x + 1;
""")
                self.assertEqual(output, answer)

        def test_min_py_var_tokenizer(self):
                import min_py_var_tokenizer

                for e in [("+=",       "ADD_EQ"),
                          ("&=",       "B_AND_EQ"),
                          ("|=",       "B_OR_EQ"),
                          ("^=",       "B_XOR_EQ"),
                          ("&",        "BIT_AND"),
                          ("~",        "BIT_COMP"),
                          ("|",        "BIT_OR"),
                          ("^",        "BIT_XOR"),
                          ("break",    "BREAK"),
                          (":",        "COLON"),
                          (",",        "COMMA"),
                          ("continue", "CONTINUE"),
                          ("-",        "DASH"),
                          ("def",      "DEF"),
                          ("/",        "DIV"),
                          ("//",       "DIVDIV"),
                          ("//=",      "DIVDIV_EQ"),
                          ("/=",       "DIV_EQ"),
                          ("elif",     "ELIF"),
                          ("else",     "ELSE"),
                          ("==",       "EQEQ"),
                          ("=",        "EQUALS"),
                          ("**=",      "EXP_EQ"),
                          ("False",    "FALSE"),
                          ("for",      "FOR"),
                          (">=",       "GR_TH_EQ"),
                          (">",        "GR_THAN"),
                          ("if",       "IF"),
                          ("in",       "IN"),
                          ("is",       "IS"),
                          ("{",        "L_BRACE"),
                          ("[",        "L_BRACK"),
                          ("and",      "LOG_AND"),
                          ("not",      "LOG_NOT"),
                          ("or",       "LOG_OR"),
                          ("(",        "L_PAREN"),
                          ("<<=",      "L_SH_EQ"),
                          ("<<",       "L_SHIFT"),
                          ("<=",       "LS_TH_EQ"),
                          ("<",        "LS_THAN"),
                          ("%",        "MOD"),
                          ("%=",       "MOD_EQ"),
                          ("*=",       "MULT_EQ"),
                          ("562",      "NATURAL"),
                          ("None",     "NONE"),
                          ("!=",       "NOT_EQ"),
                          ("pass",     "PASS"),
                          ("+",        "PLUS"),
                          ("}",        "R_BRACE"),
                          ("]",        "R_BRACK"),
                          (")",        "R_PAREN"),
                          (">>=",      "R_SH_EQ"),
                          (">>",       "R_SHIFT"),
                          ("return",   "RETURN"),
                          (";",        "SEMICOL"),
                          ("*",        "STAR"),
                          ("**",       "STARSTAR"),
                          ('"hello"',  "STRING"),
                          ("-=",       "SUB_EQ"),
                          ("True",     "TRUE"),
                          ("temp",     "VARIABLE"),
                          ("while",    "WHILE")]:
                          answer = [(e[1], e[0]), ("NEWLINE", "\n")]
                          output = min_py_var_tokenizer.tokenizer(e[0])
                          self.assertEqual(output, answer)
                output = min_py_var_tokenizer.tokenizer("""
if 3:
     pass
""")
                answer = [("IF",        "if"),
                          ("NATURAL",   "3"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("PASS",      "pass"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", "")]
                self.assertEqual(output, answer)

                output = min_py_var_tokenizer.tokenizer("""
def f(z):
    return z + 2

a = 3 + 4 ; f(x)

while x:
    for i in range(3):
         break
""")
                answer = [("DEF",       "def"),
                          ("VARIABLE",  "f"),
                          ("L_PAREN",   "("),
                          ("VARIABLE",  "z"),
                          ("R_PAREN",   ")"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("RETURN",    "return"),
                          ("VARIABLE",  "z"),
                          ("PLUS",      "+"),
                          ("NATURAL",   "2"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", ""),
                          ("VARIABLE",  "a"),
                          ("EQUALS",    "="),
                          ("NATURAL",   "3"),
                          ("PLUS",      "+"),
                          ("NATURAL",   "4"),
                          ("SEMICOL",   ";"),
                          ("VARIABLE",  "f"),
                          ("L_PAREN",   "("),
                          ("VARIABLE",  "x"),
                          ("R_PAREN",   ")"),
                          ("NEWLINE",   "\n"),
                          ("WHILE",     "while"),
                          ("VARIABLE",  "x"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("FOR",       "for"),
                          ("VARIABLE",  "i"),
                          ("IN",        "in"),
                          ("VARIABLE",  "range"),
                          ("L_PAREN",   "("),
                          ("NATURAL",   "3"),
                          ("R_PAREN",   ")"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("BREAK",     "break"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", ""),
                          ("BLOCK_END", "")]
                self.assertEqual(output, answer)

        def test_min_py_var_grammar(self):
                import min_py_var_tokenizer
                import min_py_var_grammar
                p         = pgen.make_parser.make_parser(min_py_var_tokenizer,
                                                         min_py_var_grammar)

                COLON     = ("COLON",   ":")
                SEMICOL   = ("SEMICOL", ";")
                L_PAREN   = ("L_PAREN", "(")
                R_PAREN   = ("R_PAREN", ")")
                L_BRACE   = ("L_BRACE", "{")
                R_BRACE   = ("R_BRACE", "}")
                VAR_X     = ("VARIABLE", "x")
                VAR_Y     = ("VARIABLE", "y")
                VAR_Z     = ("VARIABLE", "z")
                VAR_F     = ("VARIABLE", "f")
                VAR_G     = ("VARIABLE", "g")
                B_BEG     = ("BLOCK_BEG", "")
                B_END     = ("BLOCK_END", "")
                EXP_7     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_pow",
                                        ("exp_inv_elems",
                                         ("exp_base",
                                          ("NATURAL", "7")))))))))))))))
                EXP_X     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_pow",
                                        ("exp_inv_elems",
                                         ("exp_base",
                                          ("VARIABLE", "x")))))))))))))))
                STAT_PASS = ("statement",
                             ("stat_semicol",
                              ("semicol_base", ("PASS", "pass")),
                              ("NEWLINE", "\n")))

                output    = p("""
pass
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("PASS", "pass")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
pass
break
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("PASS", "pass")),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("BREAK", "break")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
pass ; break ; continue
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("PASS",     "pass")),
                               SEMICOL,
                               ("semicol_base", ("BREAK",    "break")),
                               SEMICOL,
                               ("semicol_base", ("CONTINUE", "continue")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
7
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
while 7:
        pass
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("WHILE", "while"),
                               EXP_7,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, STAT_PASS, B_END))))
                self.assertEqual(output, answer)

unittest.main()
