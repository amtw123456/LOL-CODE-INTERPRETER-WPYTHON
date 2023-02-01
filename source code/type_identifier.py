# GROUP MEMBERS
# LORIA, BRIAN ANGELO I.
# DOLOR, RONEL DYLAN JOSHUA A.
# ENRIQUEZ, CHAD ANDREI A.

from lexer import *

def get_type(lexeme):
    lexeme = str(lexeme)
    if lexeme == None:
        return "UNKNOWN"
    elif troof.match(lexeme):
        return BOOLEAN
    elif numbr.match(lexeme):
        return INTEGER
    elif numbar.match(lexeme):
        return FLOAT
    elif lexeme == "NOOB":
        return "NOOB"
    elif yarn.match(lexeme) or varident.match(lexeme):
        return STRING
    else:
        return "Empty"
