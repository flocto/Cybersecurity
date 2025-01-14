# TODO: direction list operator?

from direction import Direction, Pivot
from charcoaltoken import CharcoalToken as CT
from unicodegrammars import UnicodeGrammars
from wolfram import (
    String, Rule, DelayedRule, Span, Repeated, RepeatedNull, PatternTest,
    Number, Expression
)
import re
from math import floor, ceil
from ast import literal_eval


def FindAll(haystack, needle):
    r = []
    if isinstance(haystack, str):
        index = haystack.find(needle)
        while True:
            if ~index:
                r += [index]
            else:
                return r
            index = haystack.find(needle, index + 1)
    else:
        return [i for i, item in (haystack.items() if isinstance(haystack, dict) else enumerate(haystack)) if item == needle]


def ListFind(haystack, needle):
    if isinstance(haystack, dict):
        for i, item in haystack.items():
            if item == needle:
                return i
        return None
    return haystack.index(needle) if needle in haystack else -1


def dedup(iterable):
    iterable = iterable[:]
    items = []
    i = 0
    for item in iterable:
        if item in items:
            del iterable[i]
        else:
            i += 1
            items += [item]
    return iterable


def iter_apply(iterable, function):
    clone = iterable[:]
    clone[:] = [function(item) for item in clone]
    return clone


def itersplit(iterable, number):
    result = []
    while len(iterable):
        result += [iterable[:number]]
        iterable = iterable[number:]
    return result


def _int(obj):
    if isinstance(obj, str) and re.match(r"\d+\.?\d*$", obj):
        return int(float(obj))
    return int(obj)


def product(item):
    result = 1
    for part in item:
        result *= part
    return result


def Negate(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        return item[1:] if item[:1] == "-" else "-" + item
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Negate)
    return -item


def Abs(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        return item[1:] if item[:1] == "-" else item
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Abs)
    return abs(item)


def Sum(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, int):
        item = abs(item)
        result = 0
        while item:
            result += item % 10
            item //= 10
        return result
    if isinstance(item, float):
        item = str(abs(item)).split("e")[0]
    if not hasattr(item, "__iter__"):
        item = str(item)
    if isinstance(item, str):
        if (all(c in "0123456789.-" for c in item) and
            item.count(".") < 2 and
            not "-" in item[1:]):
            return sum([0 if c < "0" else int(c) for c in item])
        return sum(map(literal_eval, re.findall(r"-?\d*\.?\d+|-?\d+", item)))
    if item:
        if isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        if isinstance(item[0], str):
            return "".join(item)
        if isinstance(item[0], String):
            return "".join(map(str, item))
        if isinstance(item[0], list):
            return sum(item, [])
        return sum(item)


def Product(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, int):
        item = abs(item)
        result = 1
        while item:
            result *= item % 10
            item //= 10
        return result
    if isinstance(item, float):
        item = format(abs(item), ".15e").split("e")[0].strip("0")
    if not hasattr(item, "__iter__"):
        item = str(item)
    if isinstance(item, str):
        if (all(c in "0123456789.-" for c in item) and
            item.count(".") < 2 and
            not "-" in item[1:]):
            return product([int(c) for c in item if c >= "0"])
        return product(map(literal_eval, re.findall(r"-?\d*\.?\d+|-?\d+", item)))
    if item and isinstance(item[0], Expression):
        item = iter_apply(item, lambda o: o.run())
    # TODO: cartesian product?
    # if isinstance(item[0], list):
    #     return sum(item, [])
    return product(item)


def vectorize(fn, afn=None, cast_string=True):
    def vectorized(left, right, c):
        if isinstance(left, String):
            left = str(left)
        if isinstance(right, String):
            right = str(right)
        if type(left) == Expression:
            left = left.run()
        if type(right) == Expression:
            right = right.run()
        left_type = type(left)
        right_type = type(right)
        left_is_iterable = (
            hasattr(left, "__iter__") and not isinstance(left, str)
        )
        right_is_iterable = (
            hasattr(right, "__iter__") and not isinstance(right, str)
        )
        if left_is_iterable or right_is_iterable:
            if left_is_iterable and right_is_iterable:
                result = afn(left, right, c) if afn else [
                    vectorized(l, r, c) for l, r in zip(left, right)
                ]
            else:
                result = (
                    [vectorized(item, right, c) for item in left]
                    if left_is_iterable else
                    [vectorized(left, item, c) for item in right]
                )
            result_type = type(left if left_is_iterable else right)
            try:
                return result_type(result)
            except:
                return result_type(result, left if left_is_iterable else right)
        if cast_string and left_type == str:
            left = literal_eval(left)
        if cast_string and right_type == str:
            right = literal_eval(right)
        return fn(left, right, c)

    return vectorized


def Incremented(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = literal_eval(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Incremented)
    return item + 1


def Decremented(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = literal_eval(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Decremented)
    return item - 1


def Doubled(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = literal_eval(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Doubled)
    return item * 2


def Halved(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = literal_eval(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Halved)
    return item / 2 if item % 2 else item // 2


def SquareRoot(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        item = literal_eval(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, SquareRoot)
    return item ** 0.5


def Lower(item):
    if isinstance(item, int) or isinstance(item, float):
        return str(item)
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        return item.lower()
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Lower)


def Min(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        return item and min(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return min(item) if item else None
    return floor(item)


def Max(item):
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        return item and max(item)
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return max(item) if item else None
    return ceil(item)


def Upper(item):
    if isinstance(item, int) or isinstance(item, float):
        return str(item)
    if isinstance(item, Expression):
        item = item.run()
    if isinstance(item, String):
        item = str(item)
    if isinstance(item, str):
        return item.upper()
    if hasattr(item, "__iter__"):
        if item and isinstance(item[0], Expression):
            item = iter_apply(item, lambda o: o.run())
        return iter_apply(item, Upper)


def direction(dir):
    if isinstance(dir, String):
        dir = str(dir)
    cls = type(dir)
    if cls == Direction:
        return dir
    elif cls == int:
        return [
            Direction.right, Direction.up_right, Direction.up,
            Direction.up_left, Direction.left, Direction.down_left,
            Direction.down, Direction.down_right
        ][dir % 8]
    elif cls == str:
        cleaned = re.sub("[^a-z]", "", dir.lower()[:5])
        lookup = {
            "r": Direction.right,
            "ri": Direction.right,
            "rig": Direction.right,
            "righ": Direction.right,
            "right": Direction.right,
            "ur": Direction.up_right,
            "upr": Direction.up_right,
            "upri": Direction.up_right,
            "uprig": Direction.up_right,
            "u": Direction.up,
            "up": Direction.up,
            "ul": Direction.up_left,
            "upl": Direction.up_left,
            "uple": Direction.up_left,
            "uplef": Direction.up_left,
            "l": Direction.left,
            "le": Direction.left,
            "lef": Direction.left,
            "left": Direction.left,
            "dl": Direction.down_left,
            "downl": Direction.down_left,
            "d": Direction.down,
            "do": Direction.down,
            "dow": Direction.down,
            "down": Direction.down,
            "dr": Direction.down_right,
            "downr": Direction.down_right
        }
        if cleaned in lookup:
            return lookup[cleaned]
        elif any(c in dir for c in "0123456789"):
            return [
                Direction.right, Direction.up_right, Direction.up,
                Direction.up_left, Direction.left, Direction.down_left,
                Direction.down, Direction.down_right
            ][int(re.search(r"\d+", dir).group()) % 8]
        else:
            return 0

InterpreterProcessor = {
    CT.Arrow: [
        lambda r: lambda c: Direction.left,
        lambda r: lambda c: Direction.up,
        lambda r: lambda c: Direction.right,
        lambda r: lambda c: Direction.down,
        lambda r: lambda c: Direction.up_left,
        lambda r: lambda c: Direction.up_right,
        lambda r: lambda c: Direction.down_right,
        lambda r: lambda c: Direction.down_left,
        lambda r: lambda c: direction(r[1](c))
    ],
    CT.Multidirectional: [
        lambda r: lambda c: r[0](c) + r[1](c),
        lambda r: lambda c: [
            Direction.right, Direction.down, Direction.left, Direction.up
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.down_right, Direction.down_left, Direction.up_left,
            Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.right, Direction.down_right,
            Direction.down, Direction.down_left,
            Direction.left, Direction.up_left,
            Direction.up, Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [Direction.down, Direction.up] + r[1](c),
        lambda r: lambda c: [Direction.right, Direction.left] + r[1](c),
        lambda r: lambda c: [
            Direction.down_right, Direction.up_left
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.down_left, Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.down_right, Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [Direction.down_left, Direction.up_left] + r[1](c),
        lambda r: lambda c: [
            Direction.down_right, Direction.down_left
        ] + r[1](c),
        lambda r: lambda c: [
            Direction.down_right, Direction.down, Direction.up,
            Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [Direction.right, Direction.up] + r[1](c),
        lambda r: lambda c: [
            Direction.right, Direction.down, Direction.left
        ] + r[1](c),
        lambda r: lambda c: [Direction.up_left, Direction.up_right] + r[1](c),
        lambda r: lambda c: [
            Direction.down, Direction.up_left, Direction.up_right
        ] + r[1](c),
        lambda r: lambda c: [Direction.down_left, Direction.left] + r[1](c),
        lambda r: lambda c: [Direction.down, Direction.left] + r[1](c),
        lambda r: lambda c: [Direction.right, Direction.up] + r[1](c),
        lambda r: lambda c: [Direction.right, Direction.down] + r[1](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: [direction(item) for item in r[1](c)],
        lambda r: lambda c: []
    ],
    CT.Side: [lambda r: lambda c: (r[0](c), r[1](c))],
    CT.EOF: [lambda r: None],
    CT.String: [lambda r: r],
    CT.Number: [lambda r: r],
    CT.Name: [lambda r: r],
    CT.S: [lambda r: None] * 2,
    CT.Span: [
        lambda r: lambda c: Span(r[0](c), r[2](c), r[4](c)),
        lambda r: lambda c: Span(r[0](c), None, r[3](c)),
        lambda r: lambda c: Span(r[0](c), r[2](c)),
        lambda r: lambda c: Span(r[0](c)),
        lambda r: lambda c: Span(None, r[1](c), r[3](c)),
        lambda r: lambda c: Span(None, r[1](c)),
        lambda r: lambda c: Span(None, None, r[2](c)),
        lambda r: lambda c: Span()
    ],

    CT.Arrows: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CT.Sides: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CT.Expressions: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CT.WolframExpressions: [
        lambda r: lambda c: [r[0](c)] + r[1](c),
        lambda r: lambda c: [r[0](c)]
    ],
    CT.PairExpressions: [
        lambda r: lambda c: [(r[0](c), r[1](c))] + r[2](c),
        lambda r: lambda c: [(r[0](c), r[1](c))]
    ],
    CT.Cases: [
        lambda r: lambda c: [(r[0](c), r[1])] + r[2](c),
        lambda r: lambda c: []
    ],

    CT.List: [
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: []
    ] * 2,
    CT.WolframList: [
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: []
    ] * 2,
    CT.Dictionary: [
        lambda r: lambda c: dict(r[1](c)),
        lambda r: lambda c: {}
    ] * 2,

    CT.WolframExpression: [
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[0](c)
    ],
    CT.Expression: [
        lambda r: lambda c: r[0],
        lambda r: lambda c: r[0],
        lambda r: lambda c: c.Retrieve(r[0]),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: c.Lambdafy(r[1]),
        lambda r: lambda c: c.Lambdafy(r[1]),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[0](r[1], r[2], r[3], r[4], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), r[3](c), r[4](c), c),
        lambda r: lambda c: r[0](r[1], r[2], r[3], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), r[3](c), c),
        lambda r: lambda c: r[0](r[1], r[2], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), c),
        lambda r: lambda c: r[0](r[1], c),
        lambda r: lambda c: r[0](r[1](c), c),
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: r[0](r[1], r[2], r[3], r[4], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), r[3](c), r[4](c), c),
        lambda r: lambda c: r[0](r[1], r[2], r[3], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), r[3](c), c),
        lambda r: lambda c: r[0](r[1], r[2], c),
        lambda r: lambda c: r[0](r[1](c), r[2](c), c),
        lambda r: lambda c: r[0](r[1], c),
        lambda r: lambda c: r[0](r[1](c), c)
    ],
    CT.ExpressionOrEOF: [
        lambda r: lambda c: r[0](c),
        lambda r: lambda c: c.Input()
    ],
    CT.Nilary: [
        lambda r: lambda c: c.InputString(),
        lambda r: lambda c: c.InputNumber(),
        lambda r: lambda c: c.Input(),
        lambda r: lambda c: c.Random(),
        lambda r: lambda c: c.PeekAll(),
        lambda r: lambda c: c.PeekMoore(),
        lambda r: lambda c: c.PeekVonNeumann(),
        lambda r: lambda c: c.Peek(),
        lambda r: lambda c: c.x,
        lambda r: lambda c: c.y
    ],
    CT.Unary: [
        lambda r: lambda item, c: Negate(item),
        lambda r: lambda item, c: (
            len(item) if hasattr(item, "__iter__") else len(str(item))
        ),
        lambda r: lambda item, c: int(not item),
        lambda r: lambda item, c: c.Cast(item),
        lambda r: lambda item, c: c.Random(item),
        lambda r: lambda item, c: c.Evaluate(item),
        lambda r: lambda item, c: item.pop(),
        lambda r: lambda item, c: Lower(item),
        lambda r: lambda item, c: Upper(item),
        lambda r: lambda item, c: Min(item),
        lambda r: lambda item, c: Max(item),
        lambda r: lambda item, c: c.ChrOrd(item),
        lambda r: lambda item, c: (
            item[::-1]
            if hasattr(item, "__iter__") else
            int(
                ("-" + str(item)[:0:-1])
                if str(item)[:1] == "-" else
                str(item)[::-1]
            )
            if isinstance(item, int) else
            float(
                ("-" + str(item)[:0:-1])
                if str(item)[:1] == "-" else
                str(item)[::-1]
            )
            if isinstance(item, float) else
            str(item)[::-1]
        ),
        lambda r: lambda item, c: c.Retrieve(item),
        lambda r: lambda item, c: Repeated(item),
        lambda r: lambda item, c: RepeatedNull(item),
        lambda r: lambda item, c: item[:],
        lambda r: lambda item, c: (
            list(range(int(item) + 1))
            if isinstance(item, int) or isinstance(item, float) else
            list(map(chr, range(ord(item) + 1)))
        ),
        lambda r: lambda item, c: (
            list(range(int(item)))
            if isinstance(item, int) or isinstance(item, float) else
            list(map(chr, range(ord(item))))
        ),
        lambda r: lambda item, c: (
            ~int(item)
            if isinstance(item, int) or isinstance(item, float) else
            (~int(float(str(item)) if "." in item else str(item)))
        ),
        lambda r: lambda item, c: Abs(item),
        lambda r: lambda item, c: Sum(item),
        lambda r: lambda item, c: Product(item),
        lambda r: lambda item, c: Incremented(item),
        lambda r: lambda item, c: Decremented(item),
        lambda r: lambda item, c: Doubled(item),
        lambda r: lambda item, c: Halved(item),
        lambda r: lambda item, c: eval(item),
        lambda r: lambda item, c: SquareRoot(item)
    ],
    CT.Binary: [
        lambda r: lambda left, right, c: c.Add(left, right),
        lambda r: lambda left, right, c: c.Subtract(left, right),
        lambda r: lambda left, right, c: c.Multiply(left, right),
        lambda r: lambda left, right, c: c.Divide(left, right),
        lambda r: lambda left, right, c: c.Divide(left, right, False),
        lambda r: vectorize(
            lambda left, right, c: left % right,
            cast_string=False
        ),
        lambda r: lambda left, right, c: int(left == right),
        lambda r: lambda left, right, c: int(left < right),
        lambda r: lambda left, right, c: int(left > right),
        lambda r: vectorize(lambda left, right, c: left & right),
        lambda r: vectorize(lambda left, right, c:
            String(left) | String(right)
            if isinstance(left, str) and isinstance(right, str) else
            left | right,
            cast_string=False
        ),
        lambda r: lambda left, right, c: (
            list(range(int(left), int(right) + 1))
            if isinstance(left, int) or isinstance(left, float) else
            list(map(chr, range(ord(left), ord(right) + 1)))
        ),
        lambda r: lambda left, right, c: (
            list(range(int(left), int(right)))
            if isinstance(left, int) or isinstance(left, float) else
            list(map(chr, range(ord(left), ord(right))))
            if isinstance(left, str) and isinstance(right, str) else
            c.CycleChop(left, right)
        ),
        lambda r: vectorize(lambda left, right, c: left ** right),
        lambda r: lambda left, right, c: 
        (
            (left[right] if right in left else None)
            if isinstance(left, dict) else
            left[int(right) % len(left)]
            if isinstance(left, list) or isinstance(left, str) else
            (   
                getattr(left, right)
                if (print(left, right, isinstance(right, str), hasattr(left, right)) or isinstance(right, str)) and hasattr(left, right) else
                left[right % len(left)]  # default to iterable
            )
        ),
        lambda r: lambda left, right, c: left.append(right) or left,
        lambda r: lambda left, right, c: str(right).join(map(str, left)),
        lambda r: lambda left, right, c: (
            list(map(int, str(left).split(str(right))))
            if isinstance(left, int) or isinstance(left, float) else
            itersplit(left, int(right))
            if isinstance(right, int) or isinstance(right, float) else
            left.split(right)
            if isinstance(left, str) and isinstance(right, str) else
            [item.split(right) for item in left]
            if hasattr(left, "__getitem__") and isinstance(right, str) else
            re.split("|".join(map(re.escape, map(str, right))), left)
        ),
        lambda r: lambda left, right, c: FindAll(left, right),
        lambda r: lambda left, right, c: (
            left.find(right)
            if isinstance(left, str) else
            ListFind(left, right)
        ),
        lambda r: lambda left, right, c: " " * (int(right) - len(str(left))) + str(left),
        lambda r: lambda left, right, c: str(left) + " " * (int(right) - len(str(left))),
        lambda r: lambda left, right, c: list(left.values()).count(right) if isinstance(left, dict) else left.count(right),
        lambda r: lambda left, right, c: Rule(left, right),
        lambda r: lambda left, right, c: DelayedRule(left, right),
        lambda r: lambda left, right, c: PatternTest(left, right),
        lambda r: lambda left, right, c: left[_int(right):],
        lambda r: lambda left, right, c: c.Base(left, right),
        lambda r: lambda left, right, c: c.BaseString(left, right)
    ],
    CT.Ternary: [lambda r: lambda x, y, z, c: x[_int(y):_int(z)]],
    CT.Quarternary: [lambda r: lambda x, y, z, w, c: x[
        _int(y):_int(z):_int(w)
    ]],
    CT.LazyUnary: [],
    CT.LazyBinary: [
        lambda r: lambda left, right, c: left(c) and right(c),
        lambda r: lambda left, right, c: left(c) or right(c)
    ],
    CT.LazyTernary: [
        lambda r: lambda x, y, z, c: c.Ternary(x, y, z)
    ],
    CT.LazyQuarternary: [],
    CT.OtherOperator: [
        lambda r: lambda c: c.PeekDirection(r[1](c), r[2](c)),
        lambda r: lambda c: c.Map(r[1](c), r[2]),
        lambda r: lambda c: c.Map(r[1](c), r[2], string_map=True),
        lambda r: lambda c: c.Any(r[1](c), r[2]),
        lambda r: lambda c: c.All(r[1](c), r[2]),
        lambda r: lambda c: c.Filter(r[1](c), r[2]),
        lambda r: lambda c: c.EvaluateVariable(r[1](c), r[2](c)),
        lambda r: lambda c: c.EvaluateVariable(r[1](c), [r[2](c)]),
        lambda r: lambda c: c.EvaluateVariable(r[1](c), [])
    ],

    CT.Program: [
        lambda r: lambda c: ((r[0](c) or True) and r[2](c)),
        lambda r: lambda c: None
    ],
    CT.NonEmptyProgram: [
        lambda r: lambda c: ((r[0](c) or True) and r[2](c)),
        lambda r: lambda c: r[0](c)
    ],
    CT.Body: [
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[1](c),
        lambda r: lambda c: r[0](c)
    ],
    CT.Command: [
        lambda r: lambda c: c.InputString(r[1]),
        lambda r: lambda c: c.InputNumber(r[1]),
        lambda r: lambda c: c.Input(r[1]),
        lambda r: lambda c: c.Evaluate(r[1](c), True),
        lambda r: lambda c: c.Print(r[1](c), directions=[r[0](c)]),
        lambda r: lambda c: c.Print(r[0](c)),
        lambda r: lambda c: c.Multiprint(r[2](c), directions=dedup(r[1](c))),
        lambda r: lambda c: c.Multiprint(r[1](c)),
        lambda r: lambda c: c.Polygon(r[1](c), r[2](c)),
        lambda r: lambda c: c.Polygon(
            [[(side, length) for side in r[1](c)] for length in [r[2](c)]][0],
            r[3](c)
        ),
        lambda r: lambda c: c.Polygon(r[1](c), r[2](c), fill=False),
        lambda r: lambda c: c.Polygon(
            [[(side, length) for side in r[1](c)] for length in [r[2](c)]][0],
            r[3](c), fill=False
        ),
        lambda r: lambda c: c.Rectangle(r[1](c), r[2](c)),
        lambda r: lambda c: c.Rectangle(r[1](c)),
        lambda r: lambda c: c.Oblong(r[1](c), r[2](c), r[3](c)),
        lambda r: lambda c: c.Oblong(r[1](c), r[2](c)),
        lambda r: lambda c: c.Rectangle(r[1](c), r[2](c), r[3](c)),
        lambda r: lambda c: c.Rectangle(r[1](c), r[2](c)),
        lambda r: lambda c: c.Move(r[0](c)),
        lambda r: lambda c: c.Move(r[1](c)),
        lambda r: lambda c: c.Move(r[2](c), r[1](c)),
        lambda r: lambda c: c.Move(r[1](c), r[2](c)),
        lambda r: lambda c: c.Pivot(Pivot.left, r[1](c)),
        lambda r: lambda c: c.Pivot(Pivot.left),
        lambda r: lambda c: c.Pivot(Pivot.right, r[1](c)),
        lambda r: lambda c: c.Pivot(Pivot.right),
        lambda r: lambda c: c.Jump(r[1](c), r[2](c)),
        lambda r: lambda c: c.RotateTransform(r[1](c)),
        lambda r: lambda c: c.RotateTransform(),
        lambda r: lambda c: c.ReflectTransform(r[1](c)),
        lambda r: lambda c: c.ReflectTransform(r[1](c)),
        lambda r: lambda c: c.ReflectTransform(),
        lambda r: lambda c: c.RotatePrism(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotatePrism(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotatePrism(anchor=r[1](c)),
        lambda r: lambda c: c.RotatePrism(r[1], number=True),
        lambda r: lambda c: c.RotatePrism(r[1](c)),
        lambda r: lambda c: c.RotatePrism(),
        lambda r: lambda c: c.ReflectMirror(r[1](c)),
        lambda r: lambda c: c.ReflectMirror(r[1](c)),
        lambda r: lambda c: c.ReflectMirror(),
        lambda r: lambda c: c.RotateCopy(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotateCopy(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotateCopy(anchor=r[1](c)),
        lambda r: lambda c: c.RotateCopy(r[1], number=True),
        lambda r: lambda c: c.RotateCopy(r[1](c)),
        lambda r: lambda c: c.RotateCopy(),
        lambda r: lambda c: c.ReflectCopy(r[1](c)),
        lambda r: lambda c: c.ReflectCopy(r[1](c)),
        lambda r: lambda c: c.ReflectCopy(),
        lambda r: lambda c: c.RotateOverlap(
            r[2], r[1](c), overlap=r[4](c), number=True
        ),
        lambda r: lambda c: c.RotateOverlap(r[2](c), r[1](c), overlap=r[3](c)),
        lambda r: lambda c: c.RotateOverlap(anchor=r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateOverlap(
            r[1], overlap=r[3](c), number=True
        ),
        lambda r: lambda c: c.RotateOverlap(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateOverlap(overlap=r[1](c)),
        lambda r: lambda c: c.RotateOverlap(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotateOverlap(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotateOverlap(anchor=r[1](c)),
        lambda r: lambda c: c.RotateOverlap(r[1], number=True),
        lambda r: lambda c: c.RotateOverlap(r[1](c)),
        lambda r: lambda c: c.RotateOverlap(),
        lambda r: lambda c: c.RotateShutter(
            r[2], r[1](c), overlap=r[4](c), number=True
        ),
        lambda r: lambda c: c.RotateShutter(r[2](c), r[1](c), overlap=r[3](c)),
        lambda r: lambda c: c.RotateShutter(anchor=r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateShutter(
            r[1], overlap=r[3](c), number=True
        ),
        lambda r: lambda c: c.RotateShutter(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.RotateShutter(overlap=r[1](c)),
        lambda r: lambda c: c.RotateShutter(r[2], r[1](c), number=True),
        lambda r: lambda c: c.RotateShutter(r[2](c), r[1](c)),
        lambda r: lambda c: c.RotateShutter(anchor=r[1](c)),
        lambda r: lambda c: c.RotateShutter(r[1], number=True),
        lambda r: lambda c: c.RotateShutter(r[1](c)),
        lambda r: lambda c: c.RotateShutter(),
        lambda r: lambda c: c.ReflectOverlap(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectOverlap(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectOverlap(overlap=r[1](c)),
        lambda r: lambda c: c.ReflectOverlap(r[1](c)),
        lambda r: lambda c: c.ReflectOverlap(r[1](c)),
        lambda r: lambda c: c.ReflectOverlap(),
        lambda r: lambda c: c.ReflectButterfly(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectButterfly(r[1](c), overlap=r[2](c)),
        lambda r: lambda c: c.ReflectButterfly(overlap=r[1](c)),
        lambda r: lambda c: c.ReflectButterfly(r[1](c)),
        lambda r: lambda c: c.ReflectButterfly(r[1](c)),
        lambda r: lambda c: c.ReflectButterfly(),
        lambda r: lambda c: c.Rotate(r[1](c)),
        lambda r: lambda c: c.Rotate(),
        lambda r: lambda c: c.Reflect(r[1](c)),
        lambda r: lambda c: c.Reflect(),
        lambda r: lambda c: c.Copy(r[1](c), r[2](c)),
        lambda r: lambda c: c.For(r[1], r[2]),
        lambda r: lambda c: c.While(r[1], r[2]),
        lambda r: lambda c: c.If(r[1], r[2], r[3]),
        lambda r: lambda c: c.If(r[1], r[2], lambda c: None),
        lambda r: lambda c: c.Assign(r[1](c), r[2](c), r[3](c)),
        lambda r: lambda c: c.Assign(r[1](c), r[2]),
        lambda r: lambda c: c.Assign(r[2](c), r[1](c)),
        lambda r: lambda c: c.Fill(r[1](c)),
        lambda r: lambda c: c.SetBackground(r[1](c)),
        lambda r: lambda c: c.Dump(),
        lambda r: lambda c: c.RefreshFor(r[1](c), r[2], r[3]),
        lambda r: lambda c: c.RefreshWhile(r[1](c), r[2], r[3]),
        lambda r: lambda c: c.Refresh(r[1](c)),
        lambda r: lambda c: c.Refresh(),
        lambda r: lambda c: c.ToggleTrim(),
        lambda r: lambda c: c.Crop(r[1](c), r[2](c)),
        lambda r: lambda c: c.Crop(r[1](c)),
        lambda r: lambda c: c.Clear(False),
        lambda r: lambda c: c.Extend(r[1](c), r[2](c)),
        lambda r: lambda c: c.Extend(r[1](c)),
        lambda r: lambda c: r[1](c).append(r[2](c)),
        lambda r: lambda c: dict(r[3](c)).get(r[2](c), r[4])(c),
        lambda r: lambda c: dict(r[3](c)).get(
            r[2](c), lambda *arguments: None
        )(c),
        lambda r: lambda c: dict(r[3](c)).get(r[2](c), r[4])(c),
        lambda r: lambda c: dict(r[3](c)).get(
            r[2](c), lambda *arguments: None
        )(c),
        lambda r: lambda c: dict(r[2](c)).get(r[1](c), r[3])(c),
        lambda r: lambda c: dict(r[2](c)).get(
            r[1](c), lambda *arguments: None
        )(c),
        lambda r: lambda c: c.Map(r[1](c), r[2], True),
        lambda r: lambda c: c.ExecuteVariable(r[1](c), r[2](c)),
        lambda r: lambda c: c.ExecuteVariable(r[1](c), [r[2](c)]),
        lambda r: lambda c: c.MapAssignLeft(r[3], r[2](c), r[1]),
        lambda r: lambda c: c.MapAssign(r[2], r[1]),
        lambda r: lambda c: c.MapAssignRight(r[3], r[2](c), r[1]),
        lambda r: lambda c: c.MapAssign(r[2], r[1]),
        lambda r: lambda c: exec(r[1](c))
    ]
}
