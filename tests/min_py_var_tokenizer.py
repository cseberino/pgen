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

import re

WS = "\s+"

regexes = {"ADD_EQ"    : "\+=",
           "B_AND_EQ"  : "&=",
           "B_OR_EQ"   : "\|=",
           "B_XOR_EQ"  : "\^=",
           "BIT_AND"   : "&",
           "BIT_COMP"  : "~",
           "BIT_OR"    : "\|",
           "BIT_XOR"   : "\^",
           "BREAK"     : "break",
           "COLON"     : ":",
           "COMMA"     : ",",
           "CONTINUE"  : "continue",
           "DASH"      : "-",
           "DEF"       : "def",
           "DIV"       : "/",
           "DIVDIV"    : "//",
           "DIVDIV_EQ" : "//=",
           "DIV_EQ"    : "/=",
           "ELIF"      : "elif",
           "ELSE"      : "else",
           "EQEQ"      : "==",
           "EQUALS"    : "=",
           "EXP_EQ"    : "\*\*=",
           "FALSE"     : "False",
           "FOR"       : "for",
           "GR_TH_EQ"  : ">=",
           "GR_THAN"   : ">",
           "IF"        : "if",
           "IN"        : "in",
           "IS"        : "is",
           "L_BRACE"   : "\{",
           "L_BRACK"   : "\[",
           "LOG_AND"   : "and",
           "LOG_NOT"   : "not",
           "LOG_OR"    : "or",
           "L_PAREN"   : "\(",
           "L_SH_EQ"   : "<<=",
           "L_SHIFT"   : "<<",
           "LS_TH_EQ"  : "<=",
           "LS_THAN"   : "<",
           "MOD"       : "%",
           "MOD_EQ"    : "%=",
           "MULT_EQ"   : "\*=",
           "NATURAL"   : "\d+",
           "NEWLINE"   : "\n",
           "NONE"      : "None",
           "NOT_EQ"    : "!=",
           "PASS"      : "pass",
           "PLUS"      : "\+",
           "R_BRACE"   : "\}",
           "R_BRACK"   : "\]",
           "R_PAREN"   : "\)",
           "R_SH_EQ"   : ">>=",
           "R_SHIFT"   : ">>",
           "RETURN"    : "return",
           "SEMICOL"   : ";",
           "STAR"      : "\*",
           "STARSTAR"  : "\*\*",
           "STRING"    : '"(\\\\"|[^"])*(?<=[^\\\\])"',
           "SUB_EQ"    : "-=",
           "TRUE"      : "True",
           "VARIABLE"  : "[a-zA-Z_]\w*",
           "WHILE"     : "while"}
key     = lambda e : -len(e[1]) * (e[0] != "VARIABLE")
regexes = sorted(regexes.items(), key = key)

def tokenizer_(text):
        tokens = []
        index  = 0
        while index < len(text):
                match = re.match(WS, text[index:])
                if match:
                        index += len(match.group(0))
                        continue
                for e in regexes:
                        match = re.match(e[1], text[index:])
                        if match:
                                tokens.append((e[0], match.group(0)))
                                index += len(match.group(0))
                                break
        tokens.append(("NEWLINE", "\n"))

        return tokens

def tokenizer(text):
        tokens = []
        levels = [0]
        for e in text.split("\n"):
                if e:
                        level = re.search("\S", e).start()
                        if level > levels[-1]:
                                levels.append(level)
                                tokens.append(("BLOCK_BEG", ""))
                        else:
                                while level < levels[-1]:
                                        levels.pop()
                                        tokens.append(("BLOCK_END", ""))
                        tokens += tokenizer_(e)
        while levels != [0]:
                levels.pop()
                tokens.append(("BLOCK_END", ""))

        return tokens
