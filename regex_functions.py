"""
# Copyright 2013 Fauzan Kadri, Nick Cheng, Brian Harrington,
# Danny Heap, 2013, 2014
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment

# Student code below this comment.


#Determines whether the given string is a valid regex
def is_regex(s):
    '''
    (str) -> bool

    >>> is_regex('((1.(0|2)*).((1*.(2.e*))*.0))')
    True
    >>> is_regex('(((0*.(0|e)*)*.(((1.e*))*.0)).0)')
    False
    >>> is_regex('((0*.(0**|e)*)*.(((0*|(1.e*))*.0)**.1*))')
    True
    >>> is_regex("(1.2)")
    True
    >>> is_regex("1.2")
    False

    Returns True iff s is a valid regex
    '''
    try:
        #base cases of leafs
        if s == '0' or s == '1' or s == '2' or s == 'e':
            return True
        else:
            #base case of star
            if s[-1] == '*':
                #last index has to be a star
                return is_regex(s[:-1])
            #if it is not a leaf then there has to be an outside opening and
            #closing brackets
            #this case will check if its false
            elif ((len(s) > 1 and s[0] != '(' and s[-1] != ')') or
                 (s[0] != '(' and s[-1] == ')') or
                 (s[0] == '(' and s[-1] != ')')):
                    return False
            #length 5 implies there has to be outside brackets with its
            #leaf and right being leaf with dot or bar in middle
            elif len(s) == 5 and s[0] == '(' and s[4] == ')':
                #remove bracket to make things simpler
                s = remove_bracket(s)
                #check whether the middle is a dot or bar
                if s[1] == '.' or s[1] == '|':
                    left = s[0]
                    right = s[2]
                    #check if left and right are leafs by recursion
                    return is_regex(left) and is_regex(right)
                return False
            else:
                #this will run if length is s is longer than 5
                index = 0
                #already checked for brackets before, this will remove it
                #to make things simpler
                s = remove_bracket(s)

                for i in range(0, len(s)):
                    #when checking for symbol, its left and right has to have
                    #same amount of open and close brackets
                    if s[i] == '.' or s[i] == '|':
                        left = s[:i]
                        right = s[i+1:]
                        index = i

                        if equal_brackets(left) and equal_brackets(right):
                            break  # desperate
                #after checking brackets, this will be true
                left = s[:index]
                right = s[index+1:]
                #multiple cases that it will be true for
                if len(left) != 0 and len(right) != 0:
                    if is_regex(left) and is_regex(right):
                        return True
                elif len(left) == 0:
                    return is_regex(right)
                elif len(right) == 0:
                    return is_regex(left)
        #if all fails
        return False
    #if any weird input, it will crash, to prevent it, return False
    except:
        return False


#checks whether there are same number of open and close brackets
def equal_brackets(s):
    '''
    (str) -> bool

    >>> equal_brackets('()')
    True
    >>> equal_brackets('(1.2)')
    True
    >>> equal_brackets('((1.2)*.1)')
    True

    Returns True iff there are the same number of '(' and ')' in s
    '''
    open_bracket = 0
    closed_bracket = 0

    #runs through each index to check
    for i in range(0, len(s)):
        if s[i] == '(':
            open_bracket += 1
        elif s[i] == ')':
            closed_bracket += 1
    #True if open and closed brackets are same
    return open_bracket == closed_bracket


#removes the outmost brackets
def remove_bracket(s):
    '''
    (str) -> str

    >>> remove_bracket('(1.2)')
    '1.2'
    >>> remove_bracket('((1.2).1)')
    '(1.2).1'

    Returns s after removing its outmost brackets.
    '''
    #find the brackets
    open_bracket = s.find('('[:])
    closed_bracket = s.rfind(')'[:])
    #if it couldnt find it, it will give -1. if it didnt, then remove it
    #else do nothing
    if open_bracket != -1 and closed_bracket != -1:
        s = s[open_bracket+1:closed_bracket]
    return s


#set of all valid regex
def all_regex_permutations(s):
    '''
    (str) -> set

    >>> a = all_regex_permutations('(1.2)')
    >>> b = {'(2.1)', '(1.2)'}
    >>> a == b
    True
    >>> a = all_regex_permutations('(1|2)*')
    >>> b = {'(1|2)*', '(2*|1)', '(1*|2)', '(2|1)*', '(2|1*)', '(1|2*)'}
    >>> a == b
    True

    Returns a set of all valid regex by getting the permutations of s
    '''
    #calls helper function
    s = perms(s)
    s = list(s)
    ret = set()

    #checks for which are regex and which arent
    for i in range(0, len(s)):
        if is_regex(s[i]):
            ret.add(s[i])
    #returns only valid regex as set
    return ret


def perms(s):
    '''
    (str) -> set

    >>> perms('abb') == {'bab', 'bba', 'abb'}
    True
    >>> a = perms('abc')
    >>> b = {'cba', 'acb', 'abc', 'bac', 'cab', 'bca'}
    >>> a == b
    True

    Returns a set of all permuations of s
    '''
    #base case
    if len(s) <= 1:
        return s

    #do permutations
    p = perms(s[1:])
    char = s[0]
    res = set()

    #get the letters and add them to both sides
    for x in p:
        for i in range(len(s)+1):
            res.add(x[:i] + char + x[i:])
    return res


#checks whether the given regex and answer are valid
def regex_match(r, s):
    '''
    (RegexTree, str) -> bool

    >>> regex_match(StarTree(Leaf('0')), '000010')
    False
    >>> regex_match(BarTree(Leaf('1'), StarTree(Leaf('0'))), '01')
    False
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '0')
    True
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '111110')
    True
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '1')
    False

    Returns True iff s matches to the Leafs of trees given, by the rules in
    handout.
    '''
    #base case
    if ((r.symbol == '0') or (r.symbol == '1') or
       (r.symbol == '2') or (r.symbol == 'e')):
        if r.symbol == 'e':
            if s == '':
                return True
        elif r.symbol == s:
            return True
    #for StarTree
    elif r.symbol == '*':
        #one of the cases
        if s == '':
            return True
        child = r.children[0]
        #cases if child is a Star
        if child.symbol == '*':
            return regex_match(child, s)
        #will check every element in s
        elif child.symbol == '|':
            for element in s:
                if not regex_match(child, element):
                    return True
            return False
        elif child.symbol == '.':
            count = 0
            length = len(s)
            #try every other element to see if they are valid
            while count < length - 1:
                if not regex_match(child, s[count] + s[count + 1]):
                    return False
                count += 2
            #cases where length is odd so it will check the last index of s
            if count < length:
                return regex_match(child, s[count])
            return True
        #cases for leaf
        else:
            for element in s:
                if not regex_match(child, element):
                    return False
            return True
        return False
    #DotTree
    elif r.symbol == '.':
        left = r.children[0]
        right = r.children[1]
        #for length if 0
        if len(s) == 0:
            return regex_match(left, '') and regex_match(right, '')
        #try every possible substring until one of them hits True. else False
        for i in range(0, len(s)):
            s1 = s[:i]
            s2 = s[i:]
            if regex_match(left, s1) and regex_match(right, s2):
                return True
            elif regex_match(left, s) and regex_match(right, ''):
                return True
            elif regex_match(left, '') and regex_match(right, s):
                return True
        return False
    #One of them or both of them have to be s
    elif r.symbol == '|':
        left = r.children[0]
        right = r.children[1]
        if regex_match(left, s) or regex_match(right, s):
            return True
        return False


#Creates a valid regex
def build_regex_tree(regex):
    '''
    (str) -> RegexTree

    >>> build_regex_tree('0')
    Leaf('0')
    >>> build_regex_tree('0*')
    StarTree(Leaf('0'))
    >>> build_regex_tree('(0.1)')
    DotTree(Leaf('0'), Leaf('1'))
    >>> build_regex_tree('(1|0)')
    BarTree(Leaf('1'), Leaf('0'))
    >>> build_regex_tree('(0*|1*)')
    BarTree(StarTree(Leaf('0')), StarTree(Leaf('1')))
    >>> build_regex_tree('((0.1).0)')
    DotTree(DotTree(Leaf('0'), Leaf('1')), Leaf('0'))

    REQ: regex must be valid

    Returns the RegexTree by converting regex
    '''
    #base case of leafs
    if regex == '0' or regex == '1' or regex == '2' or regex == 'e':
        return Leaf(regex)
    else:
        #StarTree will look at everything before the star
        if regex[-1] == '*':
            return StarTree(build_regex_tree(regex[:-1]))
        #length 5 implies there are 2 leafs with a dot or bar
        elif len(regex) == 5:
            regex = remove_bracket(regex)
            left = regex[0]
            right = regex[2]
            if regex[1] == '.':
                return DotTree(build_regex_tree(left), build_regex_tree(right))
            else:
                return BarTree(build_regex_tree(left), build_regex_tree(right))
        #break everything down into smaller chunks
        else:
            index = 0
            regex = remove_bracket(regex)
            #find the index of where the left and right exist
            for i in range(0, len(regex)):
                if regex[i] == '.' or regex[i] == '|':
                    left = regex[:i]
                    right = regex[i+1:]
                    index = i

                    #if this is true, implies we found left and right
                    if equal_brackets(left) and equal_brackets(right):
                        break

            left = regex[:index]
            right = regex[index+1:]
            symbol = regex[i]

            #possible cases for DotTree
            if symbol == '.':
                if len(left) != 0 and len(right) != 0:
                    return DotTree(build_regex_tree(left),
                                   build_regex_tree(right))
                #implies there is an empty Leaf
                elif len(left) == 0:
                    return DotTree(build_regex_tree('e'),
                                   build_regex_tree(right))
                elif len(right) == 0:
                    return DotTree(build_regex_tree(left),
                                   build_regex_tree('e'))
            #possible cases for BarTree
            else:
                if len(left) != 0 and len(right) != 0:
                    return BarTree(build_regex_tree(left),
                                   build_regex_tree(right))
                #implies there is an empty Leaf
                elif len(left) == 0:
                    return BarTree(build_regex_tree('e'),
                                   build_regex_tree(right))
                elif len(right) == 0:
                    return BarTree(build_regex_tree(left),
                                   build_regex_tree('e'))


if __name__ == '__main__':
    pass