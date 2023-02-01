# GROUP MEMBERS
# LORIA, BRIAN ANGELO I.
# DOLOR, RONEL DYLAN JOSHUA A.
# ENRIQUEZ, CHAD ANDREI A.

import re
from lextypes import *

# IDENTIFIERS
varident = re.compile("^[A-Za-z][A-Za-z0-9_]*$")

#LITERALs
numbr = re.compile("^-?[0-9]+$")
numbar = re.compile("^-?[0-9]*\.[0-9]+$")
yarn = re.compile("^\".*?\"$")
troof = re.compile("^(WIN|FAIL)$")
type_literal = re.compile("^(NOOB|NUMBR|NUMBAR|YARN|TROOF)$")

# KEYWORDS PART
HAI = re.compile("^HAI$")
KTHXBYE = re.compile("^KTHXBYE$")
# COMMENTS PARTS
BTW = re.compile("^BTW")
OBTW = re.compile("^OBTW")
TLDR = re.compile("^TLDR$")
MULTICOMMENT_STRING = re.compile('^OBTW(.*)TLDR$')

# VARIABLE IDENTIFCATION PART
I_HAS_A = re.compile("^I HAS A$")
ITZ = re.compile("^ITZ$")
R = re.compile("^R$")
# MATH PART
AN = re.compile("^AN$")
SUM_OF = re.compile("^SUM OF$")
DIFF_OF = re.compile("^DIFF OF$")
PRODUKT_OF = re.compile("^PRODUKT OF$")
QUOSHUNT_OF = re.compile("^QUOSHUNT OF$")
MOD_OF = re.compile("^MOD OF$")
BIGGR_OF = re.compile("^BIGGR OF$")
SMALLR_OF = re.compile("^SMALLR OF$")
# LOGICAL OPERATORS PART
BOTH_OF = re.compile("^BOTH OF$")
EITHER_OF = re.compile("^EITHER OF$")
WON_OF = re.compile("^WON OF$")
NOT = re.compile("^NOT$")
ANY_OF = re.compile("^ANY OF$")
ALL_OF = re.compile("^ALL OF$")
# OPERATORS
BOTH_SAEM = re.compile("^BOTH SAEM$")
DIFFRINT = re.compile("^DIFFRINT$")

SMOOSH = re.compile("^SMOOSH$")

MKAY = re.compile("^MKAY$")
MAEK = re.compile("^MAEK$")
A = re.compile("^A$")

IS_NOW_A = re.compile("^IS NOW A$")
VISIBLE = re.compile("^VISIBLE$")
GIMMEH = re.compile("^GIMMEH$")
O_RLY = re.compile("^O RLY\?$")
YA_RLY = re.compile("^YA RLY$")
MEBBE = re.compile("^MEBBE$")
NO_WAI = re.compile("^NO WAI$")
OIC = re.compile("^OIC$")
WTF = re.compile("^WTF\?$")
OMG = re.compile("^OMG$")
OMGWTF = re.compile("^OMGWTF$")
GTFO = re.compile("GTFO")
IM_IN_YR = re.compile("^IM IN YR$")
UPPIN = re.compile("^UPPIN$")
NERFIN = re.compile("^NERFIN$")
YR = re.compile("^YR$")
TIL = re.compile("^TIL$")
WILE = re.compile("^WILE$")
IM_OUTTA_YR = re.compile("^IM OUTTA YR$")

class Token:
    def __init__(self, lexeme, classification):
        self.lexeme = lexeme
        self.lexClassification = classification

class Lexemes:
    def __init__(self, file_lol = ""):
        self.lexers = []
        self.file_lol = file_lol

    def create_lexers(self):
        result = open(self.file_lol, "r+")


        for line in result:
            lex = line.lstrip()
            lex = re.split(r'(I HAS A|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BTW .*|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|ANY OF|ALL OF|BOTH SAEM|IS NOW A|O RLY\?|YA RLY|NO WAI|IM IN YR|IM OUTTA YR|\"[^\"]*\"| ,|\r\n|\r|\n| )', lex, re.DOTALL|re.MULTILINE)
            lex[:] = (value for value in lex if value != " ")
            lex[:] = (value for value in lex if value != "")
            for word in lex:

                if HAI.match(word):
                    self.lexers.append(Token(word, START_PROGRAM))

                elif KTHXBYE.match(word):
                    self.lexers.append(Token(word, END_PROGRAM))

                elif BTW.match(word):
                    self.lexers.append(Token(word, COMMENT))

                elif OBTW.match(word):
                    self.lexers.append(Token(word, MULTI_COMMENT_START))

                elif TLDR.match(word):
                    self.lexers.append(Token(word, MULTI_COMMENT_END))

                elif I_HAS_A.match(word):
                    self.lexers.append(Token(word, VAR_DEC))

                elif ITZ.match(word):
                    self.lexers.append(Token(word, VAR_ASSIGN))

                elif R.match(word):
                    self.lexers.append(Token(word, VAL_ASSIGN))

                elif AN.match(word):
                    self.lexers.append(Token(word, AN_KEYWORD))

                elif SUM_OF.match(word):
                    self.lexers.append(Token(word, ADD))

                elif DIFF_OF.match(word):
                    self.lexers.append(Token(word, SUB))

                elif PRODUKT_OF.match(word):
                    self.lexers.append(Token(word, MUL))

                elif QUOSHUNT_OF.match(word):
                    self.lexers.append(Token(word, DIV))

                elif MOD_OF.match(word):
                    self.lexers.append(Token(word, MOD))

                elif BIGGR_OF.match(word):
                    self.lexers.append(Token(word, MAX))

                elif SMALLR_OF.match(word):
                    self.lexers.append(Token(word, MIN))

                elif BOTH_OF.match(word):
                    self.lexers.append(Token(word, AND))

                elif EITHER_OF.match(word):
                    self.lexers.append(Token(word, OR))

                elif WON_OF.match(word):
                    self.lexers.append(Token(word, XOR))

                elif NOT.match(word):
                    self.lexers.append(Token(word, NOT_OF))

                elif ANY_OF.match(word):
                    self.lexers.append(Token(word, ANY))

                elif ALL_OF.match(word):
                    self.lexers.append(Token(word, ALL))

                elif BOTH_SAEM.match(word):
                    self.lexers.append(Token(word, EQUAL))

                elif DIFFRINT.match(word):
                    self.lexers.append(Token(word, NOT_EQUAL))

                elif SMOOSH.match(word):
                    self.lexers.append(Token(word, CONCATENATION))

                elif MKAY.match(word):
                    self.lexers.append(Token(word, MKAY_KEYWORD))

                elif MAEK.match(word):
                    self.lexers.append(Token(word, TYPECAST))

                elif A.match(word):
                    self.lexers.append(Token(word, ASSIGN_TYPECAST))

                elif IS_NOW_A.match(word):
                    self.lexers.append(Token(word, NEW_TYPE))

                elif VISIBLE.match(word):
                    self.lexers.append(Token(word, OUTPUT))

                elif GIMMEH.match(word):
                    self.lexers.append(Token(word, INPUT))

                elif O_RLY.match(word):
                    self.lexers.append(Token(word, IF_THEN))

                elif YA_RLY.match(word):
                    self.lexers.append(Token(word, IF))

                elif MEBBE.match(word):
                    self.lexers.append(Token(word, ELIF))

                elif NO_WAI.match(word):
                    self.lexers.append(Token(word, ELSE))

                elif OIC.match(word):
                    self.lexers.append(Token(word, END_IF))

                elif WTF.match(word):
                    self.lexers.append(Token(word, CASE_COND))

                elif OMG.match(word):
                    self.lexers.append(Token(word, CASE))

                elif OMGWTF.match(word):
                    self.lexers.append(Token(word, DEFAULT_CASE))

                elif GTFO.match(word):
                    self.lexers.append(Token(word, BREAK_CASE))

                elif IM_IN_YR.match(word):
                    self.lexers.append(Token(word, START_LOOP))

                elif UPPIN.match(word):
                    self.lexers.append(Token(word, INCREMENT))

                elif NERFIN.match(word):
                    self.lexers.append(Token(word, DECREMENT))

                elif YR.match(word):
                    self.lexers.append(Token(word, LOOP))

                elif TIL.match(word):
                    self.lexers.append(Token(word, LOOP_UNTIL))

                elif WILE.match(word):
                    self.lexers.append(Token(word, WHILE_LOOP))

                elif IM_OUTTA_YR.match(word):
                    self.lexers.append(Token(word, END_LOOP))

                elif troof.match(word):
                    self.lexers.append(Token(word, BOOLEAN))

                elif type_literal.match(word):
                    self.lexers.append(Token(word, TYPE_LITERAL))

                elif varident.match(word):
                    self.lexers.append(Token(word, VARIDENT))

                elif numbr.match(word):
                    self.lexers.append(Token(word, INTEGER))

                elif numbar.match(word):
                    self.lexers.append(Token(word, FLOAT))

                elif yarn.match(word):
                    self.lexers.append(Token(word, STRING))

                elif word == '\n':
                    self.lexers.append(Token('\\n', NEWLINES))
                else:
                    self.lexers.append(Token(word, UNKNOWN))
        self.lexers.pop(-1)
