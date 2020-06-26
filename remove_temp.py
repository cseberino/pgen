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

NOTHING = ("___NOTHING___", "___NOTHING___")

def remove_prods(ast, names):
        """
        Removes productions.
        """

        ast_ = []
        for e in ast:
                if isinstance(e, str):
                        ast_.append(e)
                else:
                        e = remove_prods(e, names)
                        if e[0] in names:
                                ast_ += e[1:]
                        else:
                                ast_.append(e)
        ast_ = tuple(ast_)

        return ast_

def remove_tuples(ast):
        """
        Removes tuples.
        """

        ast = list(ast)
        for i, e in enumerate(ast):
                if isinstance(e, tuple):
                        ast[i] = remove_tuples(e)
        if not isinstance(ast[0], str):
                inds = [i for i, e in enumerate(ast) if isinstance(e[0], tuple)]
                for i in reversed(inds):
                        ast = ast[:i] + list(ast[i]) + ast[i + 1:]
        ast = tuple(ast)

        return ast

def remove_nothings(ast):
        """
        Removes NOTHINGs.
        """

        ast = [e for e in ast if e != NOTHING]
        for i, e in enumerate(ast):
                if isinstance(e, tuple):
                        ast[i] = remove_nothings(e)
        ast = ast[0] if len(ast) == 1 else tuple(ast)

        return ast

def remove_temp(ast, names):
        """
        Removes the temporary elements added to the abstract syntax trees.
        """

        ast = remove_prods(ast, names)
        ast = remove_tuples(ast)
        ast = remove_nothings(ast)

        return ast
