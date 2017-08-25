import sys
import os


def operator_ord(o1, o2):
    order = {'!': 3, '&': 2, '|': 2, '>': 1, '<':1}
    if o1 == '(' or o2 == '(':
        return False
    elif o2 == ')':
        return True
    else:
        if order[o1] < order[o2]:
            return False
        else:
            return True


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
            while len(stack1) and operator_ord(stack1[-1],s):
                op = stack1.pop()
                prefix_s = op + prefix_s
            if len(stack1) == 0 or s != ')':
                stack1.append(s)
            else:
                stack1.pop()
    if len(stack1):
        prefix_s = ''.join(stack1) + prefix_s
    stack2 = []
    for s in prefix_s[::-1]:
        if s.isalpha():
            stack2.append(s)
        elif s == "!":
            atom = stack2.pop()
            stack2.append("neg(" + atom + ")")
        else:
            e1 = stack2.pop()
            e2 = stack2.pop()
            if s == "&":
                connective = "and("
            elif s == "|":
                connective = "or("
            elif s == ">":
                connective = "imp("
            elif s == ">":
                connective = "iff("
            stack2.append(connective + e1 + ", " + e2 + ")")
    return stack2.pop()


input_f = sys.argv[1]
input_f = input_f.replace("neg", "!")
input_f = input_f.replace("and", "&")
input_f = input_f.replace("or", "|")
input_f = input_f.replace("imp", ">")
input_f = input_f.replace("iff", "<")
input_f = input_f.replace("[", "")
input_f = input_f.replace("]", "")
input_f = input_f.replace(" ", "")
b = input_f.split("seq")
formulae_list = []
for j in b[0].split(","):
    fm = to_fol_form(j)
    formulae_list.append(fm)
right = ", ".join(formulae_list)
formulae_list.clear()
for j in b[1].split(","):
    fm = to_fol_form(j)
    formulae_list.append(fm)
left = ", ".join(formulae_list)
final = "rule_hw(seq([" + right + "], [" + left + "]))."
command = "swipl -s assn1q3_prolog.pl -g \"" + final + "\" -t halt. --quiet"
result = os.popen(command)
info = result.readlines()
if info == []:
    print("false")
else:
    print("true")
    for line in info:
        line = line.strip('\r\n')
        print(line)

