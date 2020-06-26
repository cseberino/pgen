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
                EXP_Y     = ("expression",
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
                                          ("VARIABLE", "y")))))))))))))))
                EXP_Z     = ("expression",
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
                                          ("VARIABLE", "z")))))))))))))))
                ST_PASS   = ("statement",
                             ("stat_semicol",
                              ("semicol_base", ("PASS", "pass")),
                              ("NEWLINE", "\n")))
                ST_BREAK  = ("statement",
                             ("stat_semicol",
                              ("semicol_base", ("BREAK", "break")),
                              ("NEWLINE", "\n")))

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
while x:
        pass
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("WHILE", "while"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_PASS, B_END))))
                self.assertEqual(output, answer)

                output    = p("""
if x:
        pass
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_PASS, B_END))))
                self.assertEqual(output, answer)

                output    = p("""
if x:
        pass
else:
        break
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_PASS, B_END),
                               ("ELSE", "else"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_BREAK, B_END))))
                self.assertEqual(output, answer)

                output    = p("""
if   x:
        pass
elif y:
        pass
elif z:
        break
else:
        break
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_PASS, B_END),
                               ("ELIF", "elif"),
                               EXP_Y,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_PASS, B_END),
                               ("ELIF", "elif"),
                               EXP_Z,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_BREAK, B_END),
                               ("ELSE", "else"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_BREAK, B_END))))
                self.assertEqual(output, answer)

unittest.main()
