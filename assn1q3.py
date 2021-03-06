#!/usr/bin/python3
import sys
import os
import re

# Python version python3

# function for check operation(Connectives) order
def operator_ord(o1, o2):
    order = {'!': 3, '&': 2, '|': 2, '>': 1, '<': 1}
    if o1 == '(' or o2 == '(':
        return False
    elif o2 == ')':
        return True
    else:
        if order[o1] < order[o2]:
            return False
        else:
            return True


# transfer the Sequent into first order logic format
# First translate Sequent from infix to prefix
# then call 'prefix_to_fol' to transfer to first order logic format
def to_fol_form(string):
    if string == "":
        return ""
    prefix_s = ''
    stack1 = []
    tem_s = ''
    for s in string[::-1]:
        if s == '(':
            tem_s += ')'
        elif s == ')':
            tem_s += '('
        else:
            tem_s += s
    for s in tem_s:
        if s.isalpha():
            prefix_s = s + prefix_s
        else:
            while len(stack1) and operator_ord(stack1[-1], s):
                op = stack1.pop()
                prefix_s = op + prefix_s
            if len(stack1) == 0 or s != ')':
                stack1.append(s)
            else:
                stack1.pop()
    if len(stack1):
        prefix_s = ''.join(stack1) + prefix_s
    return prefix_to_fol(prefix_s)


# transfer the prefix Sequent into first order logic format
def prefix_to_fol(string):
    stack = []
    for s in string[::-1]:
        if s.isalpha():
            stack.append(s)
        elif s == "!":
            atom = stack.pop()
            stack.append("neg(" + atom + ")")
        else:
            e1 = stack.pop()
            e2 = stack.pop()
            connective = ""
            if s == "&":
                connective = "and("
            elif s == "|":
                connective = "or("
            elif s == ">":
                connective = "imp("
            elif s == "<":
                connective = "iff("
            stack.append(connective + e1 + ", " + e2 + ")")
    return stack.pop()


# transfer from first order logic format to original Sequent format
def fol_to_normal(string):
    string = string.replace("neg", "!")
    string = string.replace("and", "&")
    string = string.replace("or", "|")
    string = string.replace("imp", ">")
    string = string.replace("iff", "<")
    get_seq = re.findall(r'\[[^\[]*\]', string)
    left = split_with_comma(get_seq[0])
    right = split_with_comma(get_seq[1])
    right_s = []
    for i in right:
        right_s.append(get_content(i))
    left_s = []
    for i in left:
        left_s.append(get_content(i))
    result = "[" + ", ".join(left_s) + "]" + " seq " + \
             "[" + ", ".join(right_s) + "]"
    return result


# transform a single formulae from fol to original form
# for example 'iff(p, q)' will become 'p iff q'
def get_content(string):
    result = ""
    if len(string) == 1:
        return string
    if string != "":
        if string[0] == '&' or string[0] == '|' \
                or string[0] == '>' or string[0] == '<':
            sub = split_with_comma(string[2:])
            l = get_content(sub[0])
            r = get_content(sub[1])
            if len(l) == 1:
                result += l
            else:
                result += '(' + l + ')'
            if string[0] == '&':
                result += " and "
            elif string[0] == '|':
                result += " or "
            elif string[0] == '>':
                result += " imp "
            else:
                result += " iff "
            if len(r) == 1:
                result += r
            else:
                result += '(' + r + ')'
        elif string[0] == '!':
            sub = split_with_comma(string[2:])
            c = get_content(sub[0])
            result += "neg "
            if len(c) == 1:
                result += c
            else:
                result += '(' + c + ')'
    return result


# split string with correct content
# for example string [imp(q, p), and(q, p)]
# will get array ['imp(q, p)', 'and(q, p)']
# Another example string 'or(a, b), c)'
# will get array ['or(a, b)', 'c']
def split_with_comma(string):
    result = []
    ele = ""
    count = 0
    for i in string:
        if i == ',' and count == 0:
            result.append(ele)
            ele = ""
        elif i == '(':
            count += 1
            ele += i
        elif i == ')':
            if count > 0:
                count -= 1
                ele += i
            else:
                result.append(ele)
                return result
        elif i != '[' and i != ']':
            ele += i
    result.append(ele)
    return result


# read the input arguments
input_f = sys.argv[1]

# transfer the special Connectives to a symbol
# 'neg' to '!', 'and' to '&', 'or' to '|'
# 'imp' to '>', 'iff' to '<'
input_f = input_f.replace("neg", "!")
input_f = input_f.replace("and", "&")
input_f = input_f.replace("or", "|")
input_f = input_f.replace("imp", ">")
input_f = input_f.replace("iff", "<")

# remove the '[' and ']' and the space
input_f = input_f.replace("[", "")
input_f = input_f.replace("]", "")
input_f = input_f.replace(" ", "")

# split with 'seq' to get right part and left part
b = input_f.split("seq")

# transfer right part and left part into first order logic format
formulae_list = []
for j in b[0].split(","):
    fm = to_fol_form(j)
    formulae_list.append(fm)
right_part = ", ".join(formulae_list)
formulae_list.clear()
for j in b[1].split(","):
    fm = to_fol_form(j)
    formulae_list.append(fm)
left_part = ", ".join(formulae_list)

# get final query which can used in prolog
final = "rule_hw(seq([" + right_part + "], [" + left_part + "]))."

# call the prolog file 'assn1q3_prolog.pl' with query to get answer
command = "swipl -s assn1q3_prolog.pl -g \"" + final + "\" -t halt. --quiet"
get_result = os.popen(command)
info = get_result.readlines()

# if the answer is empty, then print false
if not info:
    print("false")
else:
    # else answer will be true
    print("true")
    output_formula = []
    output_rule = []
    len_max = 0
    # the output's formula is in first order logic format
    # so need transfer back to original format
    for line in info:
        line = line.strip('\r\n')
        # the output also contain the rule
        # split the output, part 1 is step(formula), part 2 is rule
        line_ele = re.split('\s+', line)
        # use part 1, transfer each step from fol format to original
        fm_part = fol_to_normal(line_ele[0])
        if len(fm_part) > len_max:
            len_max = len(fm_part)
        output_formula.append(fm_part)
        output_rule.append(line_ele[1])
    len_max += len(str(len(output_formula)))

    # output the steps and the rule
    for index in range(len(output_formula)):
        output_f = str(index + 1) + "." + output_formula[index]
        print(output_f, end="")
        print(" "*(len_max - len(output_f) + 4), end="")
        print(output_rule[index])
    print("QED.")
