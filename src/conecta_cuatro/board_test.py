import pytest
from board import *
from conecta_cuatro.settings import *


def test_has_vertical_victory():
    vertical = Board.from_list([["o", "x", "x", "x"],
                               [None,None,None,None],
                                [None,None,None,None],
                                 [None,None,None,None]])
    
    assert vertical.is_victory("x")
    assert vertical.is_victory("o") == False

def test_has_horizontal_victory():
    horizontal = Board.from_list([["o", "x", "x", None],
                                 ["x",None,None,None],
                                 ["x",None,None,None],
                                 ["x",None,None,None]])
    
    assert horizontal.is_victory("x")
    assert horizontal.is_victory("o") == False
    

def test__has_ascending_victory():
    ascending = Board.from_list([["x", None, None, None],
                                [None,"x","o",None],
                                [None,"o","x",None],
                                ["x",None,None,"o"]])
    
    assert ascending.is_victory("x") == True
    assert ascending.is_victory("o") == False

def test__has_descending_victory():
    descending = Board.from_list([["x", None, None, "x"],
                                   [None,"o","x",None],
                                   [None,"x",None,None],
                                    ["o",None,None,None]]) 
    
    assert descending.is_victory("x") 
    assert descending.is_victory("o") == False