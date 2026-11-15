import pytest

from dotenv.variables import Literal, Variable, parse_variables


@pytest.mark.parametrize(
    "value,expected",
    [
        ("", []),
        ("a", [Literal(value="a")]),
        ("${a}", [Variable(name="a", default=None)]),
        ("${a:-b}", [Variable(name="a", default="b")]),
        (
            "${a}${b}",
            [
                Variable(name="a", default=None),
                Variable(name="b", default=None),
            ],
        ),
        (
            "a${b}c${d}e",
            [
                Literal(value="a"),
                Variable(name="b", default=None),
                Literal(value="c"),
                Variable(name="d", default=None),
                Literal(value="e"),
            ],
        ),
        # Unbraced references
        ("$a", [Variable(name="a", default=None)]),
        ("$_a", [Variable(name="_a", default=None)]),
        ("$a1_", [Variable(name="a1_", default=None)]),
        (
            "$a$b",
            [
                Variable(name="a", default=None),
                Variable(name="b", default=None),
            ],
        ),
        # Mixed braced and unbraced on the same line
        (
            "$a/${b}/$c",
            [
                Variable(name="a", default=None),
                Literal(value="/"),
                Variable(name="b", default=None),
                Literal(value="/"),
                Variable(name="c", default=None),
            ],
        ),
        (
            "x${a}y$b",
            [
                Literal(value="x"),
                Variable(name="a", default=None),
                Literal(value="y"),
                Variable(name="b", default=None),
            ],
        ),
        # Boundary characters terminate the unbraced name
        (
            "$a.txt",
            [
                Variable(name="a", default=None),
                Literal(value=".txt"),
            ],
        ),
        (
            "$a-b",
            [
                Variable(name="a", default=None),
                Literal(value="-b"),
            ],
        ),
        (
            "$a:-b",
            [
                Variable(name="a", default=None),
                Literal(value=":-b"),
            ],
        ),
        # Literal `$`: not followed by a name start or `{` stays as-is
        ("$", [Literal(value="$")]),
        ("$1", [Literal(value="$1")]),
        ("$-", [Literal(value="$-")]),
        ("$ a", [Literal(value="$ a")]),
        ("a$", [Literal(value="a$")]),
        (
            "$$a",
            [
                Literal(value="$"),
                Variable(name="a", default=None),
            ],
        ),
        (
            "$${a}",
            [
                Literal(value="$"),
                Variable(name="a", default=None),
            ],
        ),
    ],
)
def test_parse_variables(value, expected):
    result = parse_variables(value)

    assert list(result) == expected
