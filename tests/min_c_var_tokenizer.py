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

regexes = {"ADD_EQ"   : "\+=",
           "AMPER"    : "&",
           "B_AND_EQ" : "&=",
           "B_OR_EQ"  : "\|=",
           "B_XOR_EQ" : "\^=",
           "BIT_COMP" : "~",
           "BIT_OR"   : "\|",
           "BIT_XOR"  : "\^",
           "BREAK"    : "break",
           "CHAR"     : "char",
           "COMMA"    : ",",
           "CONTINUE" : "continue",
           "DASH"     : "-",
           "DIV"      : "/",
           "DIV_EQ"   : "/=",
           "ELSE"     : "else",
           "EQEQ"     : "==",
           "EQUALS"   : "=",
           "FOR"      : "for",
           "GR_TH_EQ" : ">=",
           "GR_THAN"  : ">",
           "IF"       : "if",
           "INT"      : "int",
           "L_BRACE"  : "\{",
           "L_BRACK"  : "\[",
           "L_PAREN"  : "\(",
           "L_SH_EQ"  : "<<=",
           "L_SHIFT"  : "<<",
           "LOG_AND"  : "&&",
           "LOG_NOT"  : "!",
           "LOG_OR"   : "\|\|",
           "LS_TH_EQ" : "<=",
           "LS_THAN"  : "<",
           "MOD"      : "%",
           "MOD_EQ"   : "%=",
           "MULT_EQ"  : "\*=",
           "NATURAL"  : "\d+",
           "NOT_EQ"   : "!=",
           "PLUS"     : "\+",
           "R_BRACE"  : "\}",
           "R_BRACK"  : "\]",
           "R_PAREN"  : "\)",
           "R_SH_EQ"  : ">>=",
           "R_SHIFT"  : ">>",
           "RETURN"   : "return",
           "SEMICOL"  : ";",
           "SIZEOF"   : "sizeof",
           "STAR"     : "\*",
           "STRING"   : '"(\\\\"|[^"])*(?<=[^\\\\])"',
           "SUB_EQ"   : "-=",
           "VARIABLE" : "[a-zA-Z_]\w*",
           "VOID"     : "void",
           "WHILE"    : "while"}
key     = lambda e : -len(e[1]) * (e[0] != "VARIABLE")
regexes = sorted(regexes.items(), key = key)

def tokenizer(text):
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

        return tokens
