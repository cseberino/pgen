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

import pgen.add_prods
import pgen.remove_temp

NOTHING = ("___NOTHING___", "___NOTHING___")

def cache(func):
        cache_ = globals()[func.__name__ + "_cache"] = {}

        def func_(left, right, objects, prods):
                if isinstance(right, list):
                        right_ = tuple(tuple(right))
                else:
                        right_ = right
                key = (left, right_, tuple(objects))
                if key not in cache_:
                        cache_[key] = func(left, right, objects, prods)

                return cache_[key]

        return func_

@cache
def prodizer_one(left, right, tokens, prodizer):
        """
        helper function
        """

        if   (len(tokens) == 0) and (right == NOTHING[0]):
                ast = (left, NOTHING)
        elif right in prodizer:
                ast = prodizer[right](tokens, prodizer)
                if ast:
                        ast = (left, ast)
        elif (len(tokens) == 1) and (right == tokens[0][0]):
                ast = (left, tokens[0])
        else:
                ast = None

        return ast

@cache
def prodizer_list(left, right, tokens, prodizer):
        """
        helper function
        """

        ast = None
        for e in right:
                if isinstance(e, tuple):
                        ast = prodizer_tuple(left, e, tokens, prodizer)
                else:
                        ast = prodizer_one(left, e, tokens, prodizer)
                if ast:
                        break

        return ast

@cache
def prodizer_tuple(left, right, tokens, prodizer):
        """
        helper function
        """

        asts = []
        for e in right:
                if tokens:
                        for i in range(len(tokens), -1, -1):
                                ast = prodizer_one(e, e, tokens[:i], prodizer)
                                if ast:
                                        tokens = tokens[i:]
                                        break
                else:
                        ast = prodizer_one(e, e, [], prodizer)
                if ast:
                        asts.append(ast[1])
                else:
                        asts = None
                        break
        ast = (left,) + tuple(asts) if asts and not tokens else None

        return ast

def make_prodizer(left, right):
        """
        Makes productionizers.
        """

        right_ = right
        if   "|" in right_:
                right_ = [e.strip() for e in right_.split("|")]
                for i, e in enumerate(right_):
                        if " " in e:
                                right_[i] = tuple(e.split())
        elif " " in right_:
                right_ = tuple(right_.split())

        def prodizer(tokens, prodizer):
                if   isinstance(right_, list):
                        ast = prodizer_list( left, right_, tokens, prodizer)
                elif isinstance(right_, tuple):
                        ast = prodizer_tuple(left, right_, tokens, prodizer)
                else:
                        ast = prodizer_one(  left, right_, tokens, prodizer)

                return ast

        return prodizer

def make_parser(tokenizer, grammar):
        """
        Makes parsers.
        """

        names    = pgen.add_prods.add_prods(grammar)
        prodizer = dict([(e, make_prodizer(e, grammar.prods[e]))
                         for e in grammar.prods])

        def parser(text):
                tokens = tokenizer.tokenizer(text)
                ast    = prodizer[grammar.start](tokens, prodizer)
                ast    = pgen.remove_temp.remove_temp(ast, names)

                return ast

        return parser
