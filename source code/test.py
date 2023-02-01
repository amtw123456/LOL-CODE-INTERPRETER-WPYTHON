# GROUP MEMBERS
# LORIA, BRIAN ANGELO I.
# DOLOR, RONEL DYLAN JOSHUA A.
# ENRIQUEZ, CHAD ANDREI A.

from lexer import *
from lextypes import *
from syntax_analyzer import *

# this file is used to display the lexemes and its classification

lexemes = Lexemes("04_smoosh_assign.lol")
lexemes.create_lexers()
for i in lexemes.lexers:
    print("PRINTING TOKENS LIST: {TOKEN LEXEME:", i.lexeme, "} {TOKEN CLASSIFICATION:", i.lexClassification, "}")
