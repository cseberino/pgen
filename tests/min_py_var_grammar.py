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

start = "program"

prods = \
"""
program       : statement+

statement     : stat_semicol | stat_if | stat_loop | stat_func

stat_semicol  : semicol_base (SEMICOL semicol_base)* NEWLINE

stat_if       : IF expression COLON NEWLINE block (ELIF expression COLON NEWLINE
                                              block)* [ELSE COLON NEWLINE block]

stat_loop     : WHILE expression             COLON NEWLINE block
              | FOR   VARIABLE IN expression COLON NEWLINE block

stat_func     : DEF VARIABLE L_PAREN [VARIABLE (COMMA VARIABLE)*] R_PAREN COLON
                                                                   NEWLINE block

expression    : exp_log_and (LOG_OR  exp_log_and)*

exp_log_and   : exp_log_not (LOG_AND exp_log_not)*

exp_log_not   : [LOG_NOT]   exp_comp

exp_comp      : exp_bit_or  (comp_op exp_bit_or)*

exp_bit_or    : exp_bit_xor (BIT_OR                      exp_bit_xor)*

exp_bit_xor   : exp_bit_and (BIT_XOR                     exp_bit_and)*

exp_bit_and   : exp_shift   (BIT_AND                     exp_shift)*

exp_shift     : exp_sum     ((L_SHIFT | R_SHIFT)         exp_sum)*

exp_sum       : exp_prod    ((PLUS | DASH)               exp_prod)*

exp_prod      : exp_prefix  ((STAR | DIV | MOD | DIVDIV) exp_prefix)*

exp_prefix    : [PLUS | DASH | BIT_COMP] exp_pow

exp_pow       : exp_inv_elems [STARSTAR exp_inv_elems]

exp_inv_elems : exp_base L_PAREN [expression (COMMA expression)*] R_PAREN
              | exp_base (L_BRACK elements R_BRACK)+
              | exp_base

exp_base      : NONE
              | TRUE
              | FALSE
              | NATURAL
              | STRING
              | VARIABLE
              | L_BRACK [expression (COMMA expression)*] R_BRACK
              | L_BRACK [expression comprehen_for]       R_BRACK
              | L_PAREN [expression (COMMA expression)*] R_PAREN
              | L_BRACE [key_val    (COMMA key_val)*]    R_BRACE

comprehen_for : FOR VARIABLE IN expression [comprehen_for | comprehen_if]

comprehen_if  : IF expression [comprehen_for | comprehen_if]

elements      : [expression] COLON [expression] [COLON [expression]]
              | expression

semicol_base  : PASS
              | BREAK
              | CONTINUE
              | expression [assign_op expression]
              | RETURN [expression]

block         : BLOCK_BEG statement+ BLOCK_END

key_val       : expression COLON expression

assign_op     : EQUALS | ADD_EQ | SUB_EQ | MULT_EQ | DIV_EQ | MOD_EQ | L_SH_EQ
                  | R_SH_EQ | B_AND_EQ | B_OR_EQ | B_XOR_EQ | EXP_EQ | DIVDIV_EQ

comp_op       : LS_THAN | LS_TH_EQ | GR_THAN | GR_TH_EQ | EQEQ | NOT_EQ | IN
                                                  | LOG_NOT IN | IS | IS LOG_NOT
"""
prods = [e.split(":") for e in prods.split("\n\n")]
prods = dict([(e[0].strip(), e[1].strip()) for e in prods])
