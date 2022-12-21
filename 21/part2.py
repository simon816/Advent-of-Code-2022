import sys
from collections import namedtuple
import functools

mapping = {}

for line in sys.stdin.readlines():
    name, expr = line.strip().split(': ')
    mapping[name] = int(expr) if expr.isdigit() else expr

Add = namedtuple('Add', 'list')
Eq = namedtuple('Eq', 'left right')
Div = namedtuple('Div', 'left right')
Sub = namedtuple('Sub', 'left right')
Mul = namedtuple('Mul', 'list')

def create_expr(name, eq=False):
    if name == 'humn':
        return 'X'
    v = mapping[name]
    if type(v) == int:
        return v
    left, op, right = v.split(' ')
    if op == '/':
        op = '//'
    if eq:
        op = '=='
    left = create_expr(left)
    right = create_expr(right)
    if op == '+':
        if type(left) == int and type(right) == int:
            return left + right
        l = []
        if isinstance(left, Add):
            l.extend(left.list)
        else:
            l.append(left)
        if isinstance(right, Add):
            l.extend(right.list)
        else:
            l.append(right)
        return Add(l)
    if op == '*':
        if type(left) == int and type(right) == int:
            return left * right
        l = []
        if isinstance(left, Mul):
            l.extend(left.list)
        else:
            l.append(left)
        if isinstance(right, Mul):
            l.extend(right.list)
        else:
            l.append(right)
        return Mul(l)
    if op == '-':
        if type(left) == int and type(right) == int:
            return left - right
        return Sub(left, right)
    if op == '//':
        if type(left) == int and type(right) == int:
            return left // right
        return Div(left, right)
    if op == '==':
        return Eq(left, right)
    assert False

def to_str(e):
    if type(e) == int:
        return str(e)
    if e == 'X':
        return 'X'
    if isinstance(e, Add):
        return ' + '.join('(' + to_str(v) + ')' for v in e.list)
    if isinstance(e, Mul):
        return ' * '.join('(' + to_str(v) + ')' for v in e.list)
    if isinstance(e, Sub):
        return '(%s) - (%s)' % (to_str(e.left), to_str(e.right))
    if isinstance(e, Div):
        return '(%s) // (%s)' % (to_str(e.left), to_str(e.right))
    if isinstance(e, Eq):
        return '(%s) == (%s)' % (to_str(e.left), to_str(e.right))
    assert False, e

def simplify(e):
    if type(e) == int:
        return e
    if e == 'X':
        return 'X'
    if isinstance(e, Eq):
        l = simplify(e.left)
        r = simplify(e.right)
        # Find the constant side
        if type(l) == int:
            l, r = r, l
        # it should exist
        assert type(r) == int
        if isinstance(l, Mul):
            const = 1
            var = []
            for v in l.list:
                if type(v) == int:
                    const *= v
                else:
                    var.append(v)
            if const != 1:
                assert len(var) == 1
                return simplify(Eq(var[0], r // const))
            assert False
        if isinstance(l, Div) and type(l.right) == int:
            return simplify(Eq(l.left, r * l.right))
        if isinstance(l, Sub):
            if type(l.left) == int:
                return simplify(Eq(Add([r, l.right]), l.left))
            if type(l.right) == int:
                return simplify(Eq(l.left, r + l.right))
        if isinstance(l, Add):
            const = 0
            var = []
            for v in l.list:
                if type(v) == int:
                    const += v
                else:
                    var.append(v)
            if const != 0:
                assert len(var) == 1
                return simplify(Eq(var[0], r - const))
            assert False
        return Eq(l, r)
    return e

root = create_expr('root', True)
print(to_str(simplify(root)))
