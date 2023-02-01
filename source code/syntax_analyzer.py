# GROUP MEMBERS
# LORIA, BRIAN ANGELO I.
# DOLOR, RONEL DYLAN JOSHUA A.
# ENRIQUEZ, CHAD ANDREI A.

import tkinter.simpledialog as simpledialog
from tkinter import *
from lextypes import *
from lexer import *
from type_identifier import *
from syntax_analyzer import *
from symbol_table import *
import copy
import re

currentLine = 0

def print_tokens_lexeme(Tokens, Symbol_Table, Console_Output): # function used for debugging and checking Tokens lexemes
    for i in Tokens:
        print("PRINTING TOKENS LIST: TOKEN LEXEME:", i.lexeme, "TOKEN CLASSIFICATION:", i.lexClassification)

# <program> ::= HAI <linebreak> <statement> <linebreak> KTHXBYE
def program_abstraction(Tokens, Symbol_Table, Console_Output): # pass a Tokens_list here
    if Tokens[0].lexClassification == COMMENT:
        Tokens, error_type = singleline_comment_abstraction(Tokens, Symbol_Table, Console_Output)
        if error_type != None:
            print(error_type)

        program_abstraction(Tokens, Symbol_Table, Console_Output)
    elif Tokens[0].lexClassification == START_PROGRAM:
        Tokens.pop(0)
        statement_abstraction(Tokens, Symbol_Table, Console_Output)
        # print_tokens_lexeme(Tokens, Symbol_Table, Console_Output)
        if Tokens[0].lexClassification == END_PROGRAM:
            Tokens.pop(0)
            if len(Tokens) == 0:
                print("PROGRAM DONE")
            #else:
            #   Insert COMMENT ABSTRACTION HERE
    else:
        print("Error at line 1: Code Start Delimiter (HAI) not found")

# <statement> ::= <statement> <linebreak> <statement>| <print> | <variable_declaration> | <comment> | <concatenate> | <input> | <if_statement> | <switch> | <variable_assignment>
def statement_abstraction(Tokens, Symbol_Table, Console_Output):
    while Tokens[0].lexClassification != END_PROGRAM:
        if Tokens[0].lexClassification == OUTPUT:
            Tokens, error_type = print_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification == VAR_DEC:
            Tokens, error_type = variable_declaration_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == NEWLINES:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == VARIDENT:
            Tokens, error_type = variable_assignment_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == INPUT:
            Tokens, error_type = input_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)
        elif Tokens[0].lexClassification == TYPECAST:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = typecast_abstraction(Tokens,Symbol_Table,Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == NEW_TYPE:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = is_now_abstraction_v2(Tokens,Symbol_Table,Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == CONCATENATION:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = concatenate_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == COMMENT:
            Tokens, error_type = singleline_comment_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == MULTI_COMMENT_START:
            Tokens, error_type = multiline_comment_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == START_LOOP:
            Tokens, error_type = loop_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == CASE_COND:
            Tokens.pop(0)
            Tokens, error_type = switch_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == IF_THEN:
            Tokens.pop(0)
            Tokens, error_type = if_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification in OPERATIONS:
            Symbol_Table.symbol_table["IT"] = operations_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification in BOOLEAN_EXPRESSIONS:
            Symbol_Table.symbol_table["IT"] = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification in DATA_TYPES:
            Symbol_Table.symbol_table["IT"] = equality_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        else:
            print("Error at line " + str(currentLine) + " LOLCODE syntax error")
            break

# <linebreak> ::= linebreak
def linebreak_abstraction(Tokens, Symbol_Table, Console_Output):
    global currentLine
    currentLine += 1
    Tokens.pop(0)
    return Tokens

# <print> ::= VISIBLE <printable>
def print_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    if Tokens[0].lexClassification == OUTPUT:
        Tokens.pop(0)

        return printable_abstraction(Tokens, Symbol_Table, Console_Output), error_type
    return Tokens, error_type
# <printable> ::= <printable> <printable> | varident | <literal> | <expr>
def printable_abstraction(Tokens, Symbol_Table, Console_Output):
    printed = []
    toDisplay = ""
    while(Tokens[0].lexClassification != NEWLINES):
        if Tokens[0].lexClassification in DATA_TYPES:
            printed.append(Tokens[0].lexeme)
            toDisplay += str(display_literal_abstraction(Tokens.pop(0), Symbol_Table, Console_Output))
        elif Tokens[0].lexClassification == VARIDENT:
            toDisplay += str(display_varident_abstraction(Tokens.pop(0), Symbol_Table, Console_Output))
        elif Tokens[0].lexClassification in OPERATIONS:
            toDisplay += str(operations_abstraction(Tokens, Symbol_Table, Console_Output))
        elif Tokens[0].lexClassification in BOOLEAN_EXPRESSIONS:
            toDisplay += str(boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output))
        elif Tokens[0].lexClassification == CONCATENATION:
            Tokens.pop(0)
            toDisplay += concatenate_abstraction(Tokens, Symbol_Table ,Console_Output)
        elif Tokens[0].lexClassification == AN_KEYWORD:
            Tokens.pop(0)
        else:
            print("Error at line" + str(currentLine) + " unknown expression")

    Console_Output.insert(END, toDisplay)
    linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

    return Tokens

# <literal> ::= numbr | numbar | yarn | troof | type
def display_literal_abstraction(Tokens, Symbol_Table, Console_Output):
    if Tokens.lexClassification == STRING:
        return Tokens.lexeme[1:-1]
    elif Tokens.lexClassification == INTEGER:
        return Tokens.lexeme
    elif Tokens.lexClassification == FLOAT:
        return Tokens.lexeme
    elif Tokens.lexClassification == BOOLEAN:
        return Tokens.lexeme
    else:
        print("Error at line " + str(currentLine) + " unknown variable type")

def display_varident_abstraction(Tokens, Symbol_Table, Console_Output):
    if Tokens.lexClassification == VARIDENT:
        if Tokens.lexeme in Symbol_Table.symbol_table:
            if Symbol_Table.symbol_table[Tokens.lexeme] != None:

                return(Symbol_Table.symbol_table[Tokens.lexeme])
            else:
                print("Error at line " + str(currentLine) + " variable identifier " + str(Tokens.lexeme) + " exists but has no assigned value")
        else:
            print("Error at line " + str(currentLine) + " variable identifier " + str(Tokens.lexeme) + " does not exist")

# <variable_declaration> DONE ::= I HAS A varident | I HAS A varident ITZ varident | I HAS A varident ITZ <operations>
def variable_declaration_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    Tokens.pop(0)
    Token = Tokens.pop(0)
    if Token.lexClassification == VARIDENT:
        if Token.lexeme in Symbol_Table.symbol_table:
            return Tokens
        else:
            Symbol_Table.symbol_table[Token.lexeme] = None
            if Tokens.pop(0).lexClassification == VAR_ASSIGN:
                if Tokens[0].lexClassification in OPERATIONS:
                    Symbol_Table.symbol_table[Token.lexeme] = operations_abstraction(Tokens, Symbol_Table, Console_Output)
                elif Tokens[0].lexClassification == CONCATENATION:
                    Symbol_Table.symbol_table[Token.lexeme] = concatenate_abstraction(Tokens, Symbol_Table)
                elif Tokens[0].lexClassification == STRING:
                    Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
                elif Tokens[0].lexClassification == FLOAT:
                    Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
                elif Tokens[0].lexClassification == INTEGER:
                    Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
                elif Tokens[0].lexClassification == BOOLEAN:
                    Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
                else:
                    error_type = "Error at line" + str(currentLine) + " variable declaration syntax error"

    return Tokens, error_type

# <variable_assignment> ::= varident R <literal> | varident R varident | varident R <expr>
def variable_assignment_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    Token = Tokens.pop(0)
    if Tokens[0].lexClassification == VAL_ASSIGN:
        Tokens.pop(0)
        if Token.lexeme in Symbol_Table.symbol_table:
            if Tokens[0].lexClassification in OPERATIONS:
                Symbol_Table.symbol_table[Token.lexeme] = operations_abstraction(Tokens, Symbol_Table, Console_Output)
            elif Tokens[0].lexClassification == CONCATENATION:
                Tokens.pop(0)
                Symbol_Table.symbol_table[Token.lexeme] = concatenate_abstraction(Tokens, Symbol_Table, Console_Output)
            elif Tokens[0].lexClassification == TYPECAST:
                Tokens.pop(0)
                Symbol_Table.symbol_table[Token.lexeme] = typecast_abstraction(Tokens, Symbol_Table, Console_Output)
            elif Tokens[0].lexClassification == STRING:
                Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
            elif Tokens[0].lexClassification == FLOAT:
                Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
            elif Tokens[0].lexClassification == INTEGER:
                Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
            elif Tokens[0].lexClassification == BOOLEAN:
                Symbol_Table.symbol_table[Token.lexeme] = Tokens.pop(0).lexeme
            elif Tokens[0].lexClassification == VARIDENT:
                Symbol_Table.symbol_table[Token.lexeme] = Symbol_Table.symbol_table[Tokens.pop(0).lexeme]
        else:
            error_type = "Error at line " + str(currentLine) +  " Variable" + Token + " is not defined."
    elif Tokens[0].lexClassification == NEW_TYPE:
        Tokens.insert(0, Token)
        Symbol_Table.symbol_table[Token.lexeme] = is_now_abstraction(Tokens, Symbol_Table, Console_Output)
    elif Tokens[0].lexClassification == NEWLINES:
        Symbol_Table.symbol_table["IT"] = Symbol_Table.symbol_table[Token.lexeme]
        Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
    return Tokens, error_type

# On the works...
def expression_abstraction(Tokens, Symbol_Table, Console_Output):
    lexType = Tokens[0].lexClassification
    while lexType != NEWLINES:
        if lexType in OPERATIONS:
            return(operations_abstraction(Tokens, Symbol_Table, Console_Output))
        else:
            return ("Error at line "+ str(currentLine) + " undefined operation")

    linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

def operations_abstraction(Tokens, Symbol_Table, Console_Output):
    lexType = Tokens[0].lexClassification
    if lexType == ADD:
        Tokens.pop(0)
        return addition_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == SUB:
        Tokens.pop(0)
        return subtraction_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == MUL:
        Tokens.pop(0)
        return multiplication_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == DIV:
        Tokens.pop(0)
        return division_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == MOD:
        Tokens.pop(0)
        return mod_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == MIN:
        Tokens.pop(0)
        return minimum_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == MAX:
        Tokens.pop(0)
        return maximum_abstraction(Tokens, Symbol_Table, Console_Output)
    else:
        return value_abstraction(Tokens, Symbol_Table, Console_Output)

def addition_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    return op1 + op2

def subtraction_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    return op1-op2

def multiplication_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    return op1*op2

def division_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    return op1/op2

def mod_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    return op1%op2

def minimum_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    if op1 > op2:
        return op2
    return op1

def maximum_abstraction(Tokens, Symbol_Table, Console_Output):
    op1 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    op2 = operations_abstraction(Tokens, Symbol_Table, Console_Output)
    op1, op2 = str(op1), str(op2)
    if op1.find(".") == True:
        op1 = float(op1)
    else:
        op1 = int(op1)
    if op2.find(".") == True:
        op2 = float(op2)
    else:
        op2 = int(op2)
    if op1 < op2:
        return op2
    return op1

def equality_abstraction(Tokens, Symbol_Table, Console_Output):
    lexType = Tokens[0].lexClassification
    if lexType == EQUAL:
        Tokens.pop(0)
        return both_same_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == NOT_EQUAL:
        Tokens.pop(0)
        return diffrint_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType in OPERATIONS:
        return operations_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType in DATA_TYPES:
        lexeme = Tokens.pop(0).lexeme
        return lexeme
    elif lexType == VARIDENT:
        lexeme = Tokens.pop(0).lexeme
        if lexeme in Symbol_Table.symbol_table:
            if Symbol_Table.symbol_table[lexeme] != None:
                return(Symbol_Table.symbol_table[lexeme])
            else:
                print("Error occured at line" + str(currentLine) + " variable identifier " + lexeme + " exists but has no assigned value")

        else:
            print("Error occured at line" + str(currentLine) + " variable identifier " + lexeme + " does not exist!")


def both_same_abstraction(Tokens, Symbol_Table, Console_Output):
    data1 = equality_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    data2 = equality_abstraction(Tokens, Symbol_Table, Console_Output)
    if str(data1) == str(data2):
        return "WIN"
    return "FAIL"

def diffrint_abstraction(Tokens, Symbol_Table, Console_Output):
    data1 = equality_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    data2 = equality_abstraction(Tokens, Symbol_Table, Console_Output)
    if str(data1) != str(data2):
        return "WIN"
    return "FAIL"

# <val>  ::= varident | numbr | numbar | troof ???
def value_abstraction(Tokens, Symbol_Table, Console_Output):
    Token = Tokens.pop(0)
    if Token.lexClassification == FLOAT or Token.lexClassification == INTEGER:
        return Token.lexeme
    elif Token.lexClassification == VARIDENT:
        if Token.lexeme in Symbol_Table.symbol_table:
            if Symbol_Table.symbol_table[Token.lexeme] != None:
                return(Symbol_Table.symbol_table[Token.lexeme])
            else:
                print("Error occured at line" + str(currentLine) + " variable identifier " + Token.lexeme + " exists but has no assigned value")

        else:
            print("Error occured at line" + str(currentLine) + " variable identifier " + Token.lexeme + " does not exist")

def boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output):
    lexType = Tokens[0].lexClassification
    if lexType == AND:
        Tokens.pop(0)
        return and_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == OR:
        Tokens.pop(0)
        return or_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == XOR:
        Tokens.pop(0)
        return xor_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == NOT_OF:
        Tokens.pop(0)
        return not_of_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == ALL:
        Tokens.pop(0)
        return all_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == ANY:
        Tokens.pop(0)
        return any_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == EQUAL:
        Tokens.pop(0)
        return both_same_abstraction(Tokens, Symbol_Table, Console_Output)
    elif lexType == NOT_EQUAL:
        Tokens.pop(0)
        return diffrint_abstraction(Tokens, Symbol_Table, Console_Output)
    else:
        return boolean_value_abstraction(Tokens, Symbol_Table, Console_Output)

def and_abstraction(Tokens, Symbol_Table, Console_Output):
    troof1 = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    troof2 = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if troof1 == "WIN" and troof2 == "WIN":
        return "WIN"
    return "FAIL"

def or_abstraction(Tokens, Symbol_Table, Console_Output):
    troof1 = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    troof2 = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if troof1 == "WIN" or troof2 == "WIN":
        return "WIN"
    return "FAIL"

def xor_abstraction(Tokens, Symbol_Table, Console_Output):
    troof1 = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification == AN_KEYWORD:
        Tokens.pop(0)
    troof2 = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if ((troof1 == "WIN") and not(troof2 == "WIN")) or (not(troof1 == "WIN") and (troof2 == "WIN")):
        return "WIN"
    return "FAIL"

def not_of_abstraction(Tokens, Symbol_Table, Console_Output):
    troof = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
    if troof == "WIN":
        return "FAIL"
    return "WIN"

def all_abstraction(Tokens, Symbol_Table, Console_Output):

    win_Flag = True
    while Tokens[0].lexClassification != MKAY_KEYWORD:
        troof = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)

        if Tokens[0].lexClassification == AN_KEYWORD:
            Tokens.pop(0)

        if (troof == "FAIL"):
            win_Flag = False

    Tokens.pop(0)
    if win_Flag:
        return "WIN"
    return "FAIL"

def any_abstraction(Tokens, Symbol_Table, Console_Output):
    win_Flag = False
    while Tokens[0].lexClassification != MKAY_KEYWORD:
        troof = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)

        if Tokens[0].lexClassification == AN_KEYWORD:
            Tokens.pop(0)

        if (troof == "WIN"):
            win_Flag = True

    Tokens.pop(0)

    if win_Flag:
        return "WIN"
    return "FAIL"

def boolean_value_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    Token = Tokens.pop(0)
    if Token.lexClassification == BOOLEAN:
        return Token.lexeme
    elif Token.lexClassification == VARIDENT:
        if Token.lexeme in Symbol_Table.symbol_table:
            if Symbol_Table.symbol_table[Token.lexeme] != None:
                troof = re.compile("^(WIN|FAIL)$")
                if troof.match(Symbol_Table.symbol_table[Token.lexeme]):
                    return(Symbol_Table.symbol_table[Token.lexeme])
                else:
                    error_type = ("Error occured at line " + str(currentLine) + " variable identifier " + Token.lexeme + " exists but is of type YARN, INTEGER, OR FLOAT.")
            else:
                error_type = ("Error occured at line" + str(currentLine) + " variable identifier " + Token.lexeme + " exists but has no assigned value")

        else:
            error_type = ("Error occured at line" + str(currentLine) + " variable identifier " + Token.lexeme + " does not exist")
    return Tokens, error_type

# <switch> ::= WTF? <omg> OMGWTF <linebreak> <statements> <linebreak> OIC
def switch_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
    if Tokens[0].lexClassification != BREAK_CASE:
        omg_abstraction(Tokens, Symbol_Table, Console_Output)
    else:
        error_type = "Error occured at line" + str(currentLine) + " invalid switch case syntax"
    return Tokens, error_type

# <omg> ::= OMG <literal> <linebreak> <statements> <linebreak> GTFO <linebreak> | OMG <literal> <linebreak> <statements> GTFO <linebreak> <omg>
def omg_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    lexType = Tokens.pop(0)
    if lexType.lexClassification == CASE:
        if Tokens.pop(0).lexeme == Symbol_Table.symbol_table["IT"]:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
            conditional_statement_abstraction(Tokens, Symbol_Table, Console_Output)
        else:
            while Tokens[0].lexClassification != BREAK_CASE:
                if Tokens[0].lexClassification == NEWLINES:
                    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
                else:
                    Tokens.pop(0)

            Tokens.pop(0)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
            omg_abstraction(Tokens, Symbol_Table, Console_Output)

    elif lexType.lexClassification == DEFAULT_CASE:
        Tokens.pop(0)
        conditional_statement_abstraction(Tokens, Symbol_Table, Console_Output)

    return Tokens, error_type

def if_abstraction(Tokens, Symbol_Table, Console_Output):
    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
    if Symbol_Table.symbol_table["IT"] == "WIN":
        if Tokens.pop(0).lexClassification == IF:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
            return (conditional_statement_abstraction(Tokens, Symbol_Table, Console_Output)), None

    elif Symbol_Table.symbol_table["IT"] == "FAIL":
        nested = -1;
        while (Tokens[0].lexClassification != ELSE and nested != 0) or (Tokens[0].lexClassification == ELSE and nested != 0) or (Tokens[0].lexClassification != ELSE and nested == 0):
            if Tokens[0].lexClassification == IF:
                nested +=1
            if Tokens[0].lexClassification == ELSE:
                nested -=1
            if Tokens[0].lexClassification == NEWLINES:
                Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
            else:
                Tokens.pop(0)
        if Tokens.pop(0).lexClassification == ELSE:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
            return (conditional_statement_abstraction(Tokens, Symbol_Table, Console_Output)), None

    else:
        return Tokens, ("Error at line " + str(currentLine) + " invalid if-else syntax")
    return Tokens, None


def conditional_statement_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    while Tokens[0].lexClassification != END_IF:

        if Tokens[0].lexClassification == OUTPUT:
            Tokens, error_type = print_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == VAR_DEC:
            Tokens = variable_declaration_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == NEWLINES:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == VARIDENT:
            Tokens = variable_assignment_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == INPUT:
            Tokens, error_type = input_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == TYPECAST:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = typecast_abstraction(Tokens,Symbol_Table)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table)

        elif Tokens[0].lexClassification == CONCATENATION:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = concatenate_abstraction(Tokens, Symbol_Table)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == CASE_COND:
            Tokens.pop(0)
            Tokens, error_type = switch_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == COMMENT:
            Tokens = singleline_comment_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == MULTI_COMMENT_START:
            Tokens, error_type = multiline_comment_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == IF_THEN:
            Tokens.pop(0)
            Tokens, error_type = if_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == START_LOOP:
            Tokens, error_type = loop_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification in OPERATIONS:
            Symbol_Table.symbol_table["IT"] = operations_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification in BOOLEAN_EXPRESSIONS:
            Symbol_Table.symbol_table["IT"] = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification in DATA_TYPES:
            Symbol_Table.symbol_table["IT"] = value_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == ELSE:
            while Tokens[0].lexClassification != END_IF:
                if Tokens[0].lexClassification == NEWLINES:
                    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
                else:
                    Tokens.pop(0)

        elif Tokens[0].lexClassification == BREAK_CASE:
            while Tokens[0].lexClassification != END_IF:
                if Tokens[0].lexClassification == NEWLINES:
                    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
                else:
                    Tokens.pop(0)

        else:
            error_type = ("Error at line " + str(currentLine) + " invalid conditional statement syntax")

    Tokens.pop(0)
    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
    return Tokens

def singleline_comment_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    if Tokens[0].lexClassification == COMMENT:
        Tokens.pop(0)
        if Tokens[0].lexClassification == NEWLINES:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        else:
            error_type = ("Error at line" + str(currentLine) + "Invalid syntax after BTW")
    else:
        error_type = ("Error at line" + str(currentLine) + " comment syntax error")

    return Tokens, error_type

def loop_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    if Tokens[0].lexClassification == START_LOOP:
        print(Tokens[0].lexeme)
        Tokens.pop(0)
        if Tokens[0].lexClassification == VARIDENT:
            label = Tokens.pop(0).lexeme
            if Tokens[0].lexClassification == INCREMENT:
                Tokens, error_type = increment_decrement_abstraction(Tokens, Symbol_Table, "UPPIN", Console_Output)
            elif Tokens[0].lexClassification == DECREMENT:
                Tokens, error_type = increment_decrement_abstraction(Tokens, Symbol_Table, "NERFIN", Console_Output)
            else:
                pass
            if Tokens.pop(0).lexClassification == END_LOOP:
                if Tokens[0].lexClassification == VARIDENT:
                    if Tokens[0].lexeme == label:
                        Tokens.pop(0)
                        return Tokens, error_type
                    else:
                        #Error type: Wrong label
                        error_type = ("Error at line" + str(currentLine) + ": Invalid Loop Identifier!")
                else:
                    # Error type : Missing loop label
                    error_type = ("Error at line" + str(currentLine) + ": Missing Loop Identifier!")
            else:
                # Error type: Missing Loop End - "IM OUTTA YR"
                error_type = ("Error at line" + str(currentLine) + ": Missing End Loop Keyword!")
        else:
            #print here invalid loop name
            error_type = ("Error at line" + str(currentLine) + ": Invalid Loop Identifier!")
    return Tokens, error_type

def increment_decrement_abstraction(Tokens, Symbol_Table, operation, Console_Output):
    error_type = None
    Tokens.pop(0)
    if Tokens[0].lexClassification == LOOP:
        Tokens.pop(0)
        if Tokens[0].lexClassification == VARIDENT:
            if Tokens[0].lexeme in Symbol_Table.symbol_table:
                if Symbol_Table.symbol_table[Tokens[0].lexeme] != None:
                    integer = re.compile("^-?[0-9]+$")
                    if integer.match(Symbol_Table.symbol_table[Tokens[0].lexeme]):
                        key = Tokens.pop(0).lexeme
                        if Tokens[0].lexClassification == LOOP_UNTIL:
                            Tokens.pop(0)
                            Tokens = til_abstraction(Tokens, Symbol_Table, key, operation, Console_Output)
                            return Tokens, error_type
                        elif Tokens[0].lexClassification == WHILE_LOOP:
                            Tokens.pop(0)
                            Tokens = wile_abstraction(Tokens, Symbol_Table, key, operation, Console_Output)
                            return Tokens, error_type
                        else:
                            # Error Type : Not TIL or WILE
                            error_type = ("Error at line" + str(currentLine) + ": Invalid Loop Expression!")
                    else:
                        # Errortype : VARIABLE IS NOT OF TYPE INTEGER
                        error_type = ("Error at line" + str(currentLine) + ": Variable can not be incremented/decremented!")
                else:
                    # Return error_type no value
                    error_type = ("Error occured at line" + str(currentLine) + " variable identifier " + Tokens[0].lexeme + " exists but has no assigned value")
            else:
                # return error_type does not exist
                error_type = ("Error occured at line" + str(currentLine) + " variable identifier " + Tokens[0].lexeme + " does not exist")


        else:
            # print here cant increment non-variable
            pass
    else:
        #print here invalid Loop syntax
        pass
    return Tokens, error_type

def til_abstraction(Tokens, Symbol_Table, key, operation, Console_Output):
    conditionList = []
    codeblockList = []
    while Tokens[0].lexClassification != NEWLINES:
        conditionList.append(Tokens.pop(0))

    linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

    while Tokens[0].lexClassification != END_LOOP:
        codeblockList.append(Tokens.pop(0))

    loopList = copy.deepcopy(conditionList)
    loopStatementlist = copy.deepcopy(codeblockList)
    while boolean_expression_abstraction(loopList, Symbol_Table, Console_Output) != "WIN":
        loop_statement_abstraction(loopStatementlist, Symbol_Table, Console_Output)
        if operation == "UPPIN":
            Symbol_Table.symbol_table[key] = str(int(Symbol_Table.symbol_table[key]) + 1)
        elif operation == "NERFIN":
            Symbol_Table.symbol_table[key] = str(int(Symbol_Table.symbol_table[key]) - 1)
        loopList = copy.deepcopy(conditionList)
        loopStatementlist = copy.deepcopy(codeblockList)

    return Tokens

def wile_abstraction(Tokens, Symbol_Table, key, operation, Console_Output):
    conditionList = []
    codeblockList = []
    while Tokens[0].lexClassification != NEWLINES:
        conditionList.append(Tokens.pop(0))

    linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

    while Tokens[0].lexClassification != END_LOOP:
        codeblockList.append(Tokens.pop(0))

    loopList = copy.deepcopy(conditionList)
    loopStatementlist = copy.deepcopy(codeblockList)
    while boolean_expression_abstraction(loopList, Symbol_Table, Console_Output) != "FAIL":
        loop_statement_abstraction(loopStatementlist, Symbol_Table, Console_Output)
        if operation == "UPPIN":
            Symbol_Table.symbol_table[key] = str(int(Symbol_Table.symbol_table[key]) + 1)
        elif operation == "NERFIN":
            Symbol_Table.symbol_table[key] = str(int(Symbol_Table.symbol_table[key]) - 1)
        loopList = copy.deepcopy(conditionList)
        loopStatementlist = copy.deepcopy(codeblockList)

    return Tokens


def loop_statement_abstraction(Tokens, Symbol_Table, Console_Output):
    while len(Tokens) != 0:
        if Tokens[0].lexClassification == OUTPUT:
            Tokens, error_type = print_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification == VAR_DEC:
            Tokens, error_type = variable_declaration_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == NEWLINES:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == VARIDENT:
            Tokens, error_type = variable_assignment_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == INPUT:
            Tokens, error_type = input_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == TYPECAST:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = typecast_abstraction(Tokens,Symbol_Table)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table)

        elif Tokens[0].lexClassification == CONCATENATION:
            Tokens.pop(0)
            Symbol_Table.symbol_table["IT"] = concatenate_abstraction(Tokens, Symbol_Table)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        elif Tokens[0].lexClassification == COMMENT:
            Tokens, error_type = singleline_comment_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == MULTI_COMMENT_START:
            Tokens, error_type = multiline_comment_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == START_LOOP:
            Tokens, error_type = loop_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == CASE_COND:
            Tokens.pop(0)
            Tokens, error_type = switch_abstraction(Tokens, Symbol_Table, Console_Output)
            if error_type != None:
                print(error_type)

        elif Tokens[0].lexClassification == IF_THEN:
            Tokens.pop(0)
            Tokens, error_type = if_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification in OPERATIONS:
            Symbol_Table.symbol_table["IT"] = operations_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification in BOOLEAN_EXPRESSIONS:
            Symbol_Table.symbol_table["IT"] = boolean_expression_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        elif Tokens[0].lexClassification in DATA_TYPES:
            Symbol_Table.symbol_table["IT"] = equality_abstraction(Tokens, Symbol_Table, Console_Output)
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)

        else:
            print("Error at line " + str(currentLine) + " LOLCODE syntax error")
            break

# unused
def multiline_comment_abstraction(Tokens, Symbol_Table, Console_Output):
    while Tokens[0].lexClassification != MULTI_COMMENT_END:
        if Tokens[0].lexClassification == NEWLINES:
            Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
        else:
            Tokens.pop(0).lexeme
    Tokens.pop(0)
    Tokens = linebreak_abstraction(Tokens, Symbol_Table, Console_Output)
    return Tokens, None

def input_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    Tokens.pop(0)
    if Tokens[0].lexClassification == VARIDENT:
        if Tokens[0].lexeme in Symbol_Table.symbol_table:
            gimmeh_input = simpledialog.askstring("Input", "Enter some text:")
            if numbar.match(gimmeh_input) or numbr.match(gimmeh_input):
                print("IS A NUMBER")
                Symbol_Table.symbol_table[Tokens[0].lexeme] = gimmeh_input
            else:
                Symbol_Table.symbol_table[Tokens[0].lexeme] = str('"' + gimmeh_input + '"')
            Tokens.pop(0)
        else:
            error_type = "Error at line " + str(currentLine) + " variable Identifier " + str(Tokens[0].lexeme) + " does not exist."
    else:
        error_type = "Error at line " + str(currentLine) + " expected variable identifier after GIMMEH"
    Tokens.pop(0)
    return Tokens, error_type

def concatenate_abstraction(Tokens, Symbol_Table, Console_Output):
    string = ""
    while Tokens[0].lexClassification != NEWLINES:
        if Tokens[0].lexClassification in DATA_TYPES:
            string = string + str(Tokens[0].lexeme).replace("\"", "")
            Tokens.pop(0)
            if Tokens[0].lexClassification == AN_KEYWORD:
                Tokens.pop(0)
        elif Tokens[0].lexClassification == VARIDENT:
            if Tokens[0].lexeme in Symbol_Table.symbol_table:
                string = string + str(Symbol_Table.symbol_table[Tokens[0].lexeme][1:-1])
                Tokens.pop(0)
                if Tokens[0].lexClassification == AN_KEYWORD:
                    Tokens.pop(0)
            else:
                error_type = "Error at line " + str(currentLine) + " variable Identifier " + str(Tokens[0].lexeme) + " does not exist."
        else:
            error_type = "Error at line " + str(currentLine) + " expected data type but found " + str(Tokens[0].lexClassification) + ""
    return string

def typecast_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    if Tokens[0].lexClassification == VARIDENT:
        if Tokens[0].lexeme in Symbol_Table.symbol_table:
            varident = Tokens.pop(0)
            if Tokens[0].lexClassification == ASSIGN_TYPECAST:
                Tokens.pop(0)
            if Tokens[0].lexClassification == TYPE_LITERAL:
                type = Tokens.pop(0)
                if get_type(Symbol_Table.symbol_table[varident.lexeme]) == "Empty" or get_type(Symbol_Table.symbol_table[varident.lexeme]) == "NOOB":
                    if type.lexeme == "TROOF":
                        return "FAIL"
                    elif type.lexeme == "NUMBR":
                        return 0
                    elif type.lexeme == "NUMBAR":
                        return 0
                    elif type.lexeme == "YARN":
                        return "\"\""
                    elif type.lexeme == "NOOB":
                        return Symbol_Table.symbol_table[varident.lexeme]
                elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == INTEGER:
                    if type.lexeme == "TROOF":
                        if int(Symbol_Table.symbol_table[varident.lexeme]) == 0:
                            return "FAIL"
                        else:
                            return "WIN"
                    elif type.lexeme == "NUMBAR":
                        return float(Symbol_Table.symbol_table[varident.lexeme])
                    elif type.lexeme == "YARN":
                        return "\"" + str(Symbol_Table.symbol_table[varident.lexeme]) + "\""
                    elif type.lexeme == "NUMBR":
                        return Symbol_Table.symbol_table[varident.lexeme]
                    else:
                        # Error_type invalid typecast to NOOB
                        pass

                elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == FLOAT:
                    if type.lexeme == "TROOF":
                        if float(Symbol_Table.symbol_table[varident.lexeme]) == 0:
                            return "FAIL"
                        else:
                            return "WIN"
                    elif type.lexeme == "NUMBR":
                        return int(Symbol_Table.symbol_table[varident.lexeme][:Symbol_Table.symbol_table[varident.lexeme].find('.')])
                    elif type.lexeme == "YARN":
                        print("bruh")
                        return "\""+str(Symbol_Table.symbol_table[varident.lexeme][:Symbol_Table.symbol_table[varident.lexeme].find('.')+3])+"\""
                    elif type.lexeme == "NUMBAR":
                        return Symbol_Table.symbol_table[varident.lexeme]
                    else:
                        # Error_type invalid typecast to NOOB
                        pass

                elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == STRING:
                    if type.lexeme == "TROOF":
                        if Symbol_Table.symbol_table[varident.lexeme] == "\"\"":
                            return "FAIL"
                        else:
                            # Error_type invalid troof value!
                            return "WIN"
                    elif type.lexeme == "NUMBR":
                        numbr = re.compile("^-?[0-9]+$")
                        if numbr.match(Symbol_Table.symbol_table[varident.lexeme]):
                            return int(Symbol_Table.symbol_table[varident.lexeme])
                        else:
                            # Error_type invalid integer value!
                            pass
                    elif type.lexeme == "NUMBAR":
                        numbar = re.compile("^-?[0-9]*\.[0-9]+$")
                        if numbar.match(Symbol_Table.symbol_table[varident.lexeme]):
                            return float(Symbol_Table.symbol_table[varident.lexeme])
                        else:
                            # Error_type invalid integer value!
                            pass
                    elif type.lexeme == "YARN":
                        return Symbol_Table.symbol_table[varident.lexeme]
                    else:
                        # Error_type invalid typecast to NOOB
                        pass
                elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == BOOLEAN:
                    if type.lexeme == "NUMBAR":
                        if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                            return 0
                        elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                            return 1.0
                        else:
                            # Error_type boolean variable cant be typecasted to float!
                            pass
                    elif type.lexeme == "NUMBR":
                        if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                            return 0
                        elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                            return 1
                        else:
                            # Error_type boolean variable cant be typecasted to integer!
                            pass
                    elif type.lexeme == "YARN":
                        if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                            return "\"FAIL\""
                        elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                            return "\"WIN\""
                        else:
                            # Error_type boolean variable cant be typecasted to string!
                            pass
                    elif type.lexeme == "TROOF":
                        return Symbol_Table.symbol_table[varident.lexeme]
                    else:
                        # Error_type invalid typecast to NOOB
                        pass
                else:
                    # Error_type invalid data_type   ------ MAYBE UNNECESSARY?
                    pass
            else:
                # Error_type Expected data type; found Tokens[0].lexClassification!
                pass
        else:
            #Error_type variable does not exist!
            pass
    else:
        #Error_type expected varident found lexClassification
        pass

def is_now_abstraction(Tokens, Symbol_Table, Console_Output):
    error_type = None
    if Tokens[0].lexClassification == VARIDENT:
        if Tokens[0].lexeme in Symbol_Table.symbol_table:
            varident = Tokens.pop(0)
            if Tokens[0].lexClassification == NEW_TYPE:
                Tokens.pop(0)
                if Tokens[0].lexClassification == TYPE_LITERAL:
                    type = Tokens.pop(0)
                    if get_type(Symbol_Table.symbol_table[varident.lexeme]) == "Empty" or get_type(Symbol_Table.symbol_table[varident.lexeme]) == "NOOB":
                        if type.lexeme == "TROOF":
                            return "FAIL"
                        elif type.lexeme == "NUMBR":
                            return 0
                        elif type.lexeme == "NUMBAR":
                            return 0
                        elif type.lexeme == "YARN":
                            return "\"\""
                        elif type.lexeme == "NOOB":
                            return Symbol_Table.symbol_table[varident.lexeme]
                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == INTEGER:
                        if type.lexeme == "TROOF":
                            if int(Symbol_Table.symbol_table[varident.lexeme]) == 0:
                                return "FAIL"
                            else:
                                return "WIN"
                        elif type.lexeme == "NUMBAR":
                            return float(Symbol_Table.symbol_table[varident.lexeme])
                        elif type.lexeme == "YARN":
                            return "\"" + str(Symbol_Table.symbol_table[varident.lexeme]) + "\""
                        elif type.lexeme == "NUMBR":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass

                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == FLOAT:
                        if type.lexeme == "TROOF":
                            if float(Symbol_Table.symbol_table[varident.lexeme]) == 0:
                                return "FAIL"
                            else:
                                return "WIN"
                        elif type.lexeme == "NUMBR":
                            return int(Symbol_Table.symbol_table[varident.lexeme][:Symbol_Table.symbol_table[varident.lexeme].find('.')])
                        elif type.lexeme == "YARN":
                            print("bruh")
                            return "\""+str(Symbol_Table.symbol_table[varident.lexeme][:Symbol_Table.symbol_table[varident.lexeme].find('.')+3])+"\""
                        elif type.lexeme == "NUMBAR":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass

                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == STRING:
                        if type.lexeme == "TROOF":
                            if Symbol_Table.symbol_table[varident.lexeme] == "\"\"":
                                return "FAIL"
                            else:
                                # Error_type invalid troof value!
                                return "WIN"
                        elif type.lexeme == "NUMBR":
                            numbr = re.compile("^-?[0-9]+$")
                            if numbr.match(Symbol_Table.symbol_table[varident.lexeme]):
                                return int(Symbol_Table.symbol_table[varident.lexeme])
                            else:
                                # Error_type invalid integer value!
                                pass
                        elif type.lexeme == "NUMBAR":
                            numbar = re.compile("^-?[0-9]*\.[0-9]+$")
                            if numbar.match(Symbol_Table.symbol_table[varident.lexeme]):
                                return float(Symbol_Table.symbol_table[varident.lexeme])
                            else:
                                # Error_type invalid integer value!
                                pass
                        elif type.lexeme == "YARN":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass
                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == BOOLEAN:
                        if type.lexeme == "NUMBAR":
                            if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                                return 0
                            elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                                return 1.0
                            else:
                                # Error_type boolean variable cant be typecasted to float!
                                pass
                        elif type.lexeme == "NUMBR":
                            if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                                return 0
                            elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                                return 1
                            else:
                                # Error_type boolean variable cant be typecasted to integer!
                                pass
                        elif type.lexeme == "YARN":
                            if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                                return "\"FAIL\""
                            elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                                return "\"WIN\""
                            else:
                                # Error_type boolean variable cant be typecasted to string!
                                pass
                        elif type.lexeme == "TROOF":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass
                    else:
                        # Error_type invalid data_type   ------ MAYBE UNNECESSARY?
                        pass
                else:
                    # Error_type Expected data type; found Tokens[0].lexClassification!
                    pass
            else:
                # Error_type Expected an IS_NOW_A_KEYWORD; found Tokens[0].lexClassification!
                pass
        else:
            #Error_type variable does not exist!
            pass
    else:
        #Error_type expected varident found lexClassification
        pass

def is_now_abstraction_v2(Tokens, Symbol_Table, Console_Output):
    error_type = None
    if Tokens[0].lexClassification == NEW_TYPE:
        Tokens.pop(0)
        if Tokens[0].lexClassification == VARIDENT:
            if Tokens[0].lexeme in Symbol_Table.symbol_table:
                varident = Tokens.pop(0)
                if Tokens[0].lexClassification == TYPE_LITERAL:
                    type = Tokens.pop(0)
                    if get_type(Symbol_Table.symbol_table[varident.lexeme]) == "Empty" or get_type(Symbol_Table.symbol_table[varident.lexeme]) == "NOOB":
                        if type.lexeme == "TROOF":
                            return "FAIL"
                        elif type.lexeme == "NUMBR":
                            return 0
                        elif type.lexeme == "NUMBAR":
                            return 0
                        elif type.lexeme == "YARN":
                            return "\"\""
                        elif type.lexeme == "NOOB":
                            return Symbol_Table.symbol_table[varident.lexeme]
                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == INTEGER:
                        if type.lexeme == "TROOF":
                            if int(Symbol_Table.symbol_table[varident.lexeme]) == 0:
                                return "FAIL"
                            else:
                                return "WIN"
                        elif type.lexeme == "NUMBAR":
                            return float(Symbol_Table.symbol_table[varident.lexeme])
                        elif type.lexeme == "YARN":
                            return "\"" + str(Symbol_Table.symbol_table[varident.lexeme]) + "\""
                        elif type.lexeme == "NUMBR":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass

                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == FLOAT:
                        if type.lexeme == "TROOF":
                            if float(Symbol_Table.symbol_table[varident.lexeme]) == 0:
                                return "FAIL"
                            else:
                                return "WIN"
                        elif type.lexeme == "NUMBR":
                            return int(Symbol_Table.symbol_table[varident.lexeme][:Symbol_Table.symbol_table[varident.lexeme].find('.')])
                        elif type.lexeme == "YARN":
                            print("bruh")
                            return "\""+str(Symbol_Table.symbol_table[varident.lexeme][:Symbol_Table.symbol_table[varident.lexeme].find('.')+3])+"\""
                        elif type.lexeme == "NUMBAR":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass

                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == STRING:
                        if type.lexeme == "TROOF":
                            if Symbol_Table.symbol_table[varident.lexeme] == "\"\"":
                                return "FAIL"
                            else:
                                # Error_type invalid troof value!
                                return "WIN"
                        elif type.lexeme == "NUMBR":
                            numbr = re.compile("^-?[0-9]+$")
                            if numbr.match(Symbol_Table.symbol_table[varident.lexeme]):
                                return int(Symbol_Table.symbol_table[varident.lexeme])
                            else:
                                # Error_type invalid integer value!
                                pass
                        elif type.lexeme == "NUMBAR":
                            numbar = re.compile("^-?[0-9]*\.[0-9]+$")
                            if numbar.match(Symbol_Table.symbol_table[varident.lexeme]):
                                return float(Symbol_Table.symbol_table[varident.lexeme])
                            else:
                                # Error_type invalid integer value!
                                pass
                        elif type.lexeme == "YARN":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass
                    elif get_type(Symbol_Table.symbol_table[varident.lexeme]) == BOOLEAN:
                        if type.lexeme == "NUMBAR":
                            if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                                return 0
                            elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                                return 1.0
                            else:
                                # Error_type boolean variable cant be typecasted to float!
                                pass
                        elif type.lexeme == "NUMBR":
                            if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                                return 0
                            elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                                return 1
                            else:
                                # Error_type boolean variable cant be typecasted to integer!
                                pass
                        elif type.lexeme == "YARN":
                            if Symbol_Table.symbol_table[varident.lexeme] == "FAIL":
                                return "\"FAIL\""
                            elif Symbol_Table.symbol_table[varident.lexeme] == "WIN":
                                return "\"WIN\""
                            else:
                                # Error_type boolean variable cant be typecasted to string!
                                pass
                        elif type.lexeme == "TROOF":
                            return Symbol_Table.symbol_table[varident.lexeme]
                        else:
                            # Error_type invalid typecast to NOOB
                            pass
                    else:
                        # Error_type invalid data_type   ------ MAYBE UNNECESSARY?
                        pass
                else:
                    # Error_type Expected data type; found Tokens[0].lexClassification!
                    pass
            else:
                # Error_type Expected an IS_NOW_A_KEYWORD; found Tokens[0].lexClassification!
                pass
