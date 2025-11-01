import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):

    def test_000(self):
        input = """
        var a int = 1;
        var a int = 2;
        """
        input = Program(
            [
                VarDecl("a", IntType(), IntLiteral(1)),
                VarDecl("a", IntType(), IntLiteral(2)),
            ]
        )
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test_001(self):
        input = """
        const a int = 1;
        const a float = 1.0;
        """
        input = Program(
            [
                ConstDecl("a", IntType(), IntLiteral(1)),
                ConstDecl("a", FloatType(), FloatLiteral(1.0)),
            ]
        )
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_002(self):
        input = """
        var a = 10;
        var b = 20;
        var a = 30;
        """
        input = Program(
            [
                VarDecl("a", IntType(), IntLiteral(10)),
                VarDecl("b", IntType(), IntLiteral(20)),
                VarDecl("a", IntType(), IntLiteral(30)),
            ]
        )
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_003(self):
        input = """
        func add(x, y int) int { return x + y; }
        func add(a, b int) int { return a + b + 1; }
        """
        input = Program(
            [
                FuncDecl(
                    "add",
                    [ParamDecl("x", IntType()), ParamDecl("y", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("x"), Id("y")))]),
                ),
                FuncDecl(
                    "add",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block(
                        [
                            Return(
                                BinaryOp(
                                    "+", BinaryOp("+", Id("a"), Id("b")), IntLiteral(1)
                                )
                            )
                        ],
                    ),
                ),
            ]
        )
        expect = "Redeclared Function: add\n"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_004(self):
        input = """
        type STRUCT struct { a int; }
        type STRUCT struct { a string; }
        """
        input = Program(
            [
                StructType("STRUCT", [("a", IntType())], []),
                StructType("STRUCT", [("a", StringType())], []),
            ]
        )
        expect = "Redeclared Type: STRUCT\n"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_005(self):
        input = """
        type STRUCT struct { a int; }
        func (v STRUCT) foo() { return 1; }
        func (v STRUCT) foo() { return 0; }
        """
        input = Program(
            [
                StructType("STRUCT", [("a", IntType())], []),
                MethodDecl(
                    "v",
                    Id("STRUCT"),
                    FuncDecl(
                        "foo",
                        [],
                        VoidType(),
                        Block(
                            [
                                Return(IntLiteral(1)),
                            ]
                        ),
                    ),
                ),
                MethodDecl(
                    "v",
                    Id("STRUCT"),
                    FuncDecl(
                        "foo",
                        [],
                        VoidType(),
                        Block(
                            [
                                Return(IntLiteral(0)),
                            ]
                        ),
                    ),
                ),
            ]
        )
        expect = "Redeclared Method: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_006(self):
        input = """
        var x = 5;
        var y = 10;
        const x = 15;
        """
        input = Program(
            [
                VarDecl("x", None, IntLiteral(5)),
                VarDecl("y", None, IntLiteral(10)),
                ConstDecl("x", None, IntLiteral(15)),
            ]
        )

        expect = "Redeclared Constant: x\n"
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_007(self):
        input = """
        const pi = 3.14;
        func foo () {return;}
        func foo () {return;}
        """
        input = Program(
            [
                ConstDecl("pi", FloatType(), FloatLiteral(3.14)),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
            ]
        )
        expect = "Redeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_008(self):
        input = """
        func foo () {return;}
        const foo = 3.14;
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
                ConstDecl("foo", FloatType(), FloatLiteral(3.14)),
            ]
        )
        expect = "Redeclared Constant: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_009(self):
        input = """
        type Person struct {
            name string;
            name int;
        }
        """
        input = Program(
            [
                StructType(
                    "Person",
                    [
                        ("name", StringType()),
                        ("name", IntType()),
                    ],
                    [],
                )
            ]
        )
        expect = "Redeclared Field: name\n"
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_010(self):
        input = """
        func (p Person) speak() { return; }
        func (p Person) speak() { return; }
        """
        input = Program(
            [
                StructType("Person", [("name", StringType())], []),
                MethodDecl(
                    "p",
                    Id("Person"),
                    FuncDecl(
                        "speak",
                        [],
                        VoidType(),
                        Block([Return(None)]),
                    ),
                ),
                MethodDecl(
                    "p",
                    Id("Person"),
                    FuncDecl(
                        "speak",
                        [],
                        VoidType(),
                        Block([Return(None)]),
                    ),
                ),
            ]
        )
        expect = "Redeclared Method: speak\n"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_011(self):
        input = """
        var count = 1;
        var total = 2;
        func count() { return; }
        """
        input = Program(
            [
                VarDecl("count", None, IntLiteral(1)),
                VarDecl("total", None, IntLiteral(2)),
                FuncDecl(
                    "count",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
            ]
        )
        expect = "Redeclared Function: count\n"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_012(self):
        input = """
        type HOUSE struct {
            name string;
            address string;
            floor int;
            floor float;
        }
        """
        input = Program(
            [
                StructType(
                    "HOUSE",
                    [
                        ("name", StringType()),
                        ("address", StringType()),
                        ("floor", IntType()),
                        ("floor", FloatType()),
                    ],
                    [],
                )
            ]
        )
        expect = "Redeclared Field: floor\n"
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_013(self):
        input = """
        type Vehicle interface {
            drive();
            drive(gear int);
        }
        """
        input = Program(
            [
                InterfaceType(
                    "Vehicle",
                    [
                        Prototype("drive", [VoidType()], VoidType()),
                        Prototype("drive", [IntType()], VoidType()),
                    ],
                ),
            ]
        )
        expect = "Redeclared Prototype: drive\n"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_014(self):
        input = """
        func (v STRUCT) putIntLn () {return;}
        func (v STRUCT) getInt () {return;}
        func (v STRUCT) getInt () {return;}
        type STRUCT struct {
            foo int;
        }
        """
        input = Program(
            [
                StructType("STRUCT", [("foo", IntType())], []),
                MethodDecl(
                    "v",
                    Id("STRUCT"),
                    FuncDecl("putIntLn", [], VoidType(), Block([Return(None)])),
                ),
                MethodDecl(
                    "v",
                    Id("STRUCT"),
                    FuncDecl("getInt", [], VoidType(), Block([Return(None)])),
                ),
                MethodDecl(
                    "v",
                    Id("STRUCT"),
                    FuncDecl("getInt", [], VoidType(), Block([Return(None)])),
                ),
            ]
        )
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_015(self):
        input = """
        type CAR interface {
            honk();
            honk(times int);
        }
        """
        input = Program(
            [
                InterfaceType(
                    "CAR",
                    [
                        Prototype("honk", [VoidType()], VoidType()),
                        Prototype("honk", [IntType()], VoidType()),
                    ],
                ),
            ]
        )
        expect = "Redeclared Prototype: honk\n"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_016(self):
        input = """
        func add(a int, b int) int { return a + b; }
        func add(a int, b int) int { return a - b; }
        """
        input = Program(
            [
                FuncDecl(
                    "add",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("a"), Id("b")))]),
                ),
                FuncDecl(
                    "add",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("-", Id("a"), Id("b")))]),
                ),
            ]
        )
        expect = "Redeclared Function: add\n"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_017(self):
        input = """
        func foo (a, a int) {return;}
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [ParamDecl("a", IntType()), ParamDecl("a", IntType())],
                    VoidType(),
                    Block([Return(None)]),
                ),
            ]
        )
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_018(self):
        input = """
        func foo () int {
            var a = 1;
            var b = 1;
            const b = 1;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    IntType(),
                    Block(
                        [
                            VarDecl("a", IntType(), IntLiteral(1)),
                            VarDecl("b", IntType(), IntLiteral(1)),
                            ConstDecl("b", IntType(), IntLiteral(1)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Redeclared Constant: b\n"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_019(self):
        input = """
        func foo () int {
            var a = 1;
            var b = 1;
            const b = 1;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    IntType(),
                    Block(
                        [
                            VarDecl("a", IntType(), IntLiteral(1)),
                            VarDecl("b", IntType(), IntLiteral(1)),
                            ConstDecl("b", IntType(), IntLiteral(1)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Redeclared Constant: b\n"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_020(self):
        input = """
        var a = 10;
        func foo(a int) { return; }
        var a = 20;
        """
        input = Program(
            [
                VarDecl("a", IntType(), IntLiteral(10)),
                FuncDecl(
                    "foo",
                    [ParamDecl("a", IntType())],
                    VoidType(),
                    Block([Return(None)]),
                ),
                VarDecl("a", IntType(), IntLiteral(20)),
            ]
        )
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test_021(self):
        input = """
        type Person struct { name string; }
        func (p Person) greet() { return; }
        var p Person;
        func (p Person) greet() { return; }
        """
        input = Program(
            [
                StructType("Person", [("name", StringType())], []),
                MethodDecl(
                    "p",
                    Id("Person"),
                    FuncDecl("greet", [], VoidType(), Block([Return(None)])),
                ),
                VarDecl("p", Id("Person"), None),
                MethodDecl(
                    "p",
                    Id("Person"),
                    FuncDecl("greet", [], VoidType(), Block([Return(None)])),
                ),
            ]
        )
        expect = "Redeclared Method: greet\n"
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_022(self):
        input = """
        type shape struct { side int; }
        var square = 1;
        type square struct { side int; }
        """
        input = Program(
            [
                StructType("shape", [("side", IntType())], []),
                VarDecl("square", IntType(), IntLiteral(1)),
                StructType("square", [("side", IntType())], []),
            ]
        )
        expect = "Redeclared Type: square\n"
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_023(self):
        input = """
        func sum(a int, b int) int { return a + b; }
        func sum(a int, b int) int { return a * b; }
        var a = sum(3, 4);
        """
        input = Program(
            [
                FuncDecl(
                    "sum",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("a"), Id("b")))]),
                ),
                FuncDecl(
                    "sum",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("*", Id("a"), Id("b")))]),
                ),
                VarDecl(
                    "a", IntType(), FuncCall("sum", [IntLiteral(3), IntLiteral(4)])
                ),
            ]
        )
        expect = "Redeclared Function: sum\n"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_024(self):
        input = """
        type person struct { name string; }
        func (p person) greet(p, p person) { return; }
        """
        input = Program(
            [
                StructType("person", [("name", StringType())], []),
                FuncDecl(
                    "greet",
                    [ParamDecl("p", Id("person")), ParamDecl("p", Id("person"))],
                    VoidType(),
                    Block([Return(None)]),
                ),
            ]
        )
        expect = "Redeclared Parameter: p\n"
        self.assertTrue(TestChecker.test(input, expect, 424))

    def test_025(self):
        input = """
        type cat struct { name string; }
        func (c cat) meow() { return; }
        func (p cat) meow() { return; }
        """
        input = Program(
            [
                StructType("cat", [("name", StringType())], []),
                MethodDecl(
                    "c",
                    Id("cat"),
                    FuncDecl("meow", [], VoidType(), Block([Return(None)])),
                ),
                MethodDecl(
                    "p",
                    Id("cat"),
                    FuncDecl("meow", [], VoidType(), Block([Return(None)])),
                ),
            ]
        )
        expect = "Redeclared Method: meow\n"
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_026(self):
        input = """
        const max = 100;
        func test() {
            const max = 200;
            const max = 300;
        }
        """
        input = Program(
            [
                ConstDecl("max", IntType(), IntLiteral(100)),
                FuncDecl(
                    "test",
                    [],
                    VoidType(),
                    Block(
                        [
                            ConstDecl("max", IntType(), IntLiteral(200)),
                            ConstDecl("max", IntType(), IntLiteral(300)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Redeclared Constant: max\n"
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_027(self):
        input = """
        func main() { return; }
        func main() { return; }
        """
        input = Program(
            [
                FuncDecl(
                    "main",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
                FuncDecl(
                    "main",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
            ]
        )
        expect = "Redeclared Function: main\n"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_028(self):
        input = """
        type container struct {
            size int;
            size float;
        }
        """
        input = Program(
            [
                StructType(
                    "container",
                    [
                        ("size", IntType()),
                        ("size", FloatType()),
                    ],
                    [],
                )
            ]
        )
        expect = "Redeclared Field: size\n"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_029(self):
        input = """
        func getString() {return;}
        """
        input = Program([FuncDecl("getString", [], VoidType(), Block([Return(None)]))])
        expect = "Redeclared Function: getString\n"
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_030(self):
        input = """
        var x = 10;
        var z = foo;
        """
        input = Program(
            [
                VarDecl("x", IntType(), IntLiteral(10)),
                VarDecl("z", None, Id("foo")),
            ]
        )
        expect = "Undeclared Identifier: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_031(self):
        input = """
        const pi = 3.14;
        const area = pie;
        """
        input = Program(
            [
                ConstDecl("pi", FloatType(), FloatLiteral(3.14)),
                VarDecl("area", FloatType(), Id("pie")),
            ]
        )
        expect = "Undeclared Identifier: pie\n"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_032(self):
        input = """
        var result = square(3, 4);
        """
        input = Program(
            [
                VarDecl(
                    "result",
                    IntType(),
                    FuncCall("square", [IntLiteral(3), IntLiteral(4)]),
                ),
            ]
        )
        expect = "Undeclared Function: square\n"
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test_033(self):
        input = """
        type person struct { name string; }
        func foo() {
            var p person;
            p.age = 30;
        }
        """
        input = Program(
            [
                StructType("person", [("name", StringType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("p", Id("person"), None),
                            Assign(FieldAccess(Id("p"), "age"), IntLiteral(30)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: age\n"
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_034(self):
        input = """
        var a = 10;
        var b = a + c;
        """
        input = Program(
            [
                VarDecl("a", IntType(), IntLiteral(10)),
                VarDecl("b", IntType(), BinaryOp("+", Id("a"), Id("c"))),
            ]
        )
        expect = "Undeclared Identifier: c\n"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_035(self):
        input = """
        func greet() { return; }
        func hello() { greet(); }
        func foo() {
            sayhello();
        } 
        """
        input = Program(
            [
                FuncDecl(
                    "greet",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
                FuncDecl(
                    "hello",
                    [],
                    VoidType(),
                    Block([FuncCall("greet", [])]),
                ),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block([FuncCall("sayhello", [])]),
                ),
            ]
        )
        expect = "Undeclared Function: sayhello\n"
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_036(self):
        input = """
        type car struct { speed int; }
        func foo() {
            var mycar car;
            mycar.color = "red";
        }
        """
        input = Program(
            [
                StructType("car", [("speed", IntType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("mycar", Id("car"), None),
                            BinaryOp(
                                "=",
                                FieldAccess(Id("mycar"), "color"),
                                StringLiteral("red"),
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: color\n"
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_037(self):
        input = """
        type sphere struct {
            radius int;
        }

        func (s sphere) surface () {
            const res = s.diameter;
        }
        """
        input = Program(
            [
                StructType("sphere", [("radius", IntType())], []),
                MethodDecl(
                    "s",
                    Id("sphere"),
                    FuncDecl(
                        "surface",
                        [],
                        VoidType(),
                        Block(
                            [
                                ConstDecl(
                                    "res", IntType(), FieldAccess(Id("s"), "diameter")
                                )
                            ]
                        ),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: diameter\n"
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_038(self):
        input = """
        type circle struct { radius float; }
        func foo() {
            var c circle;
            c.diameter = 20;
        }
        """
        input = Program(
            [
                StructType("circle", [("radius", FloatType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("c", Id("circle"), None),
                            Assign(FieldAccess(Id("c"), "diameter"), IntLiteral(20)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: diameter\n"
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_039(self):
        input = """
        var x = 10;
        var y = x + z;
        """
        input = Program(
            [
                VarDecl("x", IntType(), IntLiteral(10)),
                VarDecl("y", IntType(), BinaryOp("+", Id("x"), Id("z"))),
            ]
        )
        expect = "Undeclared Identifier: z\n"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_040(self):
        input = """
        var x = 10;
        var y = x + z;
        """
        input = Program(
            [
                VarDecl("x", IntType(), IntLiteral(10)),
                VarDecl("y", IntType(), BinaryOp("+", Id("x"), Id("z"))),
            ]
        )
        expect = "Undeclared Identifier: z\n"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_041(self):
        input = """
        const radius = 5;
        var area = 3.14 * radius * radius;
        var volume = area * height;
        """
        input = Program(
            [
                ConstDecl("radius", IntType(), IntLiteral(5)),
                VarDecl(
                    "area",
                    IntType(),
                    BinaryOp(
                        "*", IntLiteral(3.14), BinaryOp("*", Id("radius"), Id("radius"))
                    ),
                ),
                VarDecl("volume", IntType(), BinaryOp("*", Id("area"), Id("height"))),
            ]
        )
        expect = "Undeclared Identifier: height\n"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_042(self):
        input = """
        func add(a int, b int) int { return a + b; }
        var sum = add(x, y);
        var result = sum + 10;
        """
        input = Program(
            [
                FuncDecl(
                    "add",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("a"), Id("b")))]),
                ),
                VarDecl("sum", IntType(), FuncCall("add", [Id("x"), Id("y")])),
                VarDecl("result", IntType(), BinaryOp("+", Id("sum"), IntLiteral(10))),
            ]
        )
        expect = "Undeclared Identifier: x\n"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_043(self):
        input = """
        type student struct { name string; }
        func (s student) foo() {
            s.age = 20;
        }
        """
        input = Program(
            [
                StructType("student", [("name", StringType())], []),
                MethodDecl(
                    "s",
                    Id("student"),
                    FuncDecl(
                        "foo",
                        [],
                        VoidType(),
                        Block([Assign(FieldAccess(Id("s"), "age"), IntLiteral(20))]),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: age\n"
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_044(self):
        input = """
        func multiply(a int, b int) int { return a * b; }
        func foo() {
            result = multiply(3, 4);
            multiply(resut, result);
        }
        """
        input = Program(
            [
                FuncDecl(
                    "multiply",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("*", Id("a"), Id("b")))]),
                ),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl(
                                "result",
                                IntType(),
                                FuncCall("multiply", [IntLiteral(3), IntLiteral(4)]),
                            ),
                            FuncCall("multiply", [Id("resut"), Id("result")]),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: FuncCall(multiply,[Id(resut),Id(result)])\n"
        self.assertTrue(TestChecker.test(input, expect, 444))

    def test_045(self):
        input = """
        const maxspeed = 120;
        const maxweight = 200;
        var accel = carspeed * maxweight
        """
        input = Program(
            [
                ConstDecl("maxspeed", IntType(), IntLiteral(120)),
                ConstDecl("maxweight", IntType(), IntLiteral(200)),
                VarDecl(
                    "accel", IntType(), BinaryOp("*", Id("carspeed"), Id("maxweight"))
                ),
            ]
        )
        expect = "Undeclared Identifier: carspeed\n"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_046(self):
        input = """
        type box struct { length int; }
        var b box;
        var volume = b.length * b.width;
        """
        input = Program(
            [
                StructType("box", [("length", IntType())], []),
                VarDecl("b", Id("box"), None),
                VarDecl(
                    "volume",
                    IntType(),
                    BinaryOp(
                        "*",
                        FieldAccess(Id("b"), "length"),
                        FieldAccess(Id("b"), "width"),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: width\n"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_047(self):
        input = """
        func griit() { return; }
        var message = greet("hello");
        """
        input = Program(
            [
                FuncDecl(
                    "griit",
                    [],
                    VoidType(),
                    Block([Return(None)]),
                ),
                VarDecl(
                    "message", StringType(), FuncCall("greet", [StringLiteral("hello")])
                ),
            ]
        )
        expect = "Undeclared Function: greet\n"
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_048(self):
        input = """
        type circle struct { radius float; }
        var c circle;
        var circumference = 2 * 3.14 * c.diameter;
        """
        input = Program(
            [
                StructType("circle", [("radius", FloatType())], []),
                VarDecl("c", Id("circle"), None),
                VarDecl(
                    "circumference",
                    FloatType(),
                    BinaryOp(
                        "*",
                        IntLiteral(2),
                        BinaryOp(
                            "*", FloatLiteral(3.14), FieldAccess(Id("c"), "diameter")
                        ),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: diameter\n"
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_049(self):
        input = """
        type player struct {
            age int;
            height int;
            weight int;
        }
        var p player;
        const age = p.age;
        const skill = p.skill;
        """
        input = Program(
            [
                StructType(
                    "player",
                    [("age", IntType()), ("height", IntType()), ("weight", IntType())],
                    [],
                ),
                VarDecl("p", Id("player"), None),
                ConstDecl("age", IntType(), FieldAccess(Id("p"), "age")),
                ConstDecl("skill", IntType(), FieldAccess(Id("p"), "skill")),
            ]
        )
        expect = "Undeclared Field: skill\n"
        self.assertTrue(TestChecker.test(input, expect, 449))

    def test_050(self):
        input = """
        type shape struct { width int; height int; }
        func (s shape) area() int { return s.width * s.height; }
        func (s shape) foo() {
            area := s.volume;
        }
        """
        input = Program(
            [
                StructType("shape", [("width", IntType()), ("height", IntType())], []),
                MethodDecl(
                    "s",
                    Id("shape"),
                    FuncDecl(
                        "area",
                        [],
                        IntType(),
                        Block(
                            [
                                Return(
                                    BinaryOp(
                                        "*",
                                        FieldAccess(Id("s"), "width"),
                                        FieldAccess(Id("s"), "height"),
                                    )
                                )
                            ]
                        ),
                    ),
                ),
                MethodDecl(
                    "s",
                    Id("shape"),
                    FuncDecl(
                        "foo",
                        [],
                        VoidType(),
                        Block([Assign(Id("area"), FieldAccess(Id("s"), "volume"))]),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: volume\n"
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_051(self):
        input = """
        func calculate(a int, b int) int { return a + b; }
        func foo() int {
            return calculat(3, 4);
        }
        """
        input = Program(
            [
                FuncDecl(
                    "calculate",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("a"), Id("b")))]),
                ),
                FuncDecl(
                    "foo",
                    [],
                    IntType(),
                    Block(
                        [Return(FuncCall("calculat", [IntLiteral(3), IntLiteral(4)]))]
                    ),
                ),
            ]
        )
        expect = "Undeclared Function: calculat\n"
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_052(self):
        input = """
        func circle() float {
            const pi = 3.14;
            var area = pi * r * r;
            var r = 10;
            var result = radius;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "circle",
                    [],
                    FloatType(),
                    Block(
                        [
                            ConstDecl("pi", FloatType(), FloatLiteral(3.14)),
                            VarDecl("r", IntType(), IntLiteral(10)),
                            VarDecl(
                                "area",
                                FloatType(),
                                BinaryOp(
                                    "*", Id("pi"), BinaryOp("*", Id("r"), Id("r"))
                                ),
                            ),
                            VarDecl("result", FloatType(), Id("radius")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Undeclared Identifier: radius\n"
        self.assertTrue(TestChecker.test(input, expect, 452))

    def test_053(self):
        input = """
        type car struct { speed int; }
        func (c car) mycarcolor() {
            c.color = "red";
        }
        """
        input = Program(
            [
                StructType("car", [("speed", IntType())], []),
                MethodDecl(
                    "c",
                    Id("car"),
                    FuncDecl(
                        "mycarcolor",
                        [],
                        VoidType(),
                        Block(
                            [
                                Assign(
                                    FieldAccess(Id("c"), "color"), StringLiteral("red")
                                )
                            ]
                        ),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: color\n"
        self.assertTrue(TestChecker.test(input, expect, 453))

    def test_054(self):
        input = """
        type circle struct { radius float; }
        func foo() {
            var c circle;
            c.diameter = 20;
        }
        """
        input = Program(
            [
                StructType("circle", [("radius", FloatType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("c", Id("circle"), None),
                            Assign(FieldAccess(Id("c"), "diameter"), IntLiteral(20)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: diameter\n"
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_055(self):
        input = """
        const maxsize = 100;
        func test() {
            var maxsize = 50;
            maxsize := minsize;
        }
        """
        input = Program(
            [
                ConstDecl("maxsize", IntType(), IntLiteral(100)),
                FuncDecl(
                    "test",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("maxsize", IntType(), IntLiteral(50)),
                            Assign(Id("maxsize"), Id("minsize")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Undeclared Identifier: minsize\n"
        self.assertTrue(TestChecker.test(input, expect, 455))

    def test_056(self):
        input = """
        type person struct { name string; }
        func (p person) getage() {
            hisage := p.age
        }
        """
        input = Program(
            [
                StructType("person", [("name", StringType())], []),
                MethodDecl(
                    "p",
                    Id("person"),
                    FuncDecl(
                        "getage",
                        [],
                        VoidType(),
                        Block([Assign(Id("hisage"), FieldAccess(Id("p"), "age"))]),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: age\n"
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_057(self):
        input = """
        func add(a int, b int) int { return a + b; }
        func result() {
            var sum = add(x, y);
        }
        """
        input = Program(
            [
                FuncDecl(
                    "add",
                    [ParamDecl("a", IntType()), ParamDecl("b", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("a"), Id("b")))]),
                ),
                FuncDecl(
                    "result",
                    [],
                    VoidType(),
                    Block(
                        [VarDecl("sum", IntType(), FuncCall("add", [Id("x"), Id("y")]))]
                    ),
                ),
            ]
        )
        expect = "Undeclared Identifier: x\n"
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_058(self):
        input = """
        var x = 5;
        const x = y + 10;
        """
        input = Program(
            [
                VarDecl("x", IntType(), IntLiteral(5)),
                ConstDecl("x", IntType(), BinaryOp("+", Id("y"), IntLiteral(10))),
            ]
        )
        expect = "Redeclared Constant: x\n"
        self.assertTrue(TestChecker.test(input, expect, 458))

    def test_059(self):
        input = """
        type student struct { name string; age int; }
        func (s student) setgrade() {
            s.grade = "a";
        }
        """
        input = Program(
            [
                StructType("student", [("name", StringType()), ("age", IntType())], []),
                MethodDecl(
                    "s",
                    Id("student"),
                    FuncDecl(
                        "setgrade",
                        [],
                        VoidType(),
                        Block(
                            [Assign(FieldAccess(Id("s"), "grade"), StringLiteral("a"))]
                        ),
                    ),
                ),
            ]
        )
        expect = "Undeclared Field: grade\n"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_060(self):
        input = """
        func foo() {
            var a = 10;
            var b = 10.5;
            a = b;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("a", IntType(), IntLiteral(10)),
                            VarDecl("b", FloatType(), FloatLiteral(10.5)),
                            Assign(Id("a"), Id("b")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 460))

    def test_061(self):
        input = """
        func foo() {
            var x = true;
            var y = 100;
            x = y;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("x", BoolType(), BooleanLiteral(True)),
                            VarDecl("y", IntType(), IntLiteral(100)),
                            Assign(Id("x"), Id("y")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(x),Id(y))\n"
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_062(self):
        input = """
        func foo() int {
            var a = 1.2;
            return a;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    IntType(),
                    Block(
                        [VarDecl("a", FloatType(), FloatLiteral(1.2)), Return(Id("a"))]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Return(Id(a))\n"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_063(self):
        input = """
        func foo() [2] float {
            return [2] float {1.0, 2.0};
            return [2] int {1, 2};
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    ArrayType([IntLiteral(2)], FloatType()),
                    Block(
                        [
                            Return(
                                ArrayLiteral(
                                    [IntLiteral(2)],
                                    FloatType(),
                                    [FloatLiteral(1.0), FloatLiteral(2.0)],
                                )
                            ),
                            Return(
                                ArrayLiteral(
                                    [IntLiteral(2)],
                                    IntType(),
                                    [IntLiteral(1), IntLiteral(2)],
                                )
                            ),
                        ]
                    ),
                )
            ]
        )
        expect = "Type Mismatch: Return(ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]))\n"
        self.assertTrue(TestChecker.test(input, expect, 463))

    def test_064(self):
        input = """
        func foo() {
            var a[2] int;
            var b[3] int;
            a := b
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("a", ArrayType([IntLiteral(2)], IntType()), None),
                            VarDecl("b", ArrayType([IntLiteral(3)], IntType()), None),
                            Assign(Id("a"), Id("b")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 464))

    def test_065(self):
        input = """
        func bar(a [2] int) {
            bar([2] int {1,2})
            bar([2] string {"1","2"})
        }
        """
        input = Program(
            [
                FuncDecl(
                    "bar",
                    [ParamDecl("a", ArrayType([IntLiteral(2)], IntType()))],
                    VoidType(),
                    Block(
                        [
                            FuncCall(
                                "bar",
                                [
                                    ArrayLiteral(
                                        [IntLiteral(2)],
                                        IntType(),
                                        [IntLiteral(1), IntLiteral(2)],
                                    )
                                ],
                            ),
                            FuncCall(
                                "bar",
                                [
                                    ArrayLiteral(
                                        [IntLiteral(2)],
                                        StringType(),
                                        [StringLiteral("1"), StringLiteral("2")],
                                    )
                                ],
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: FuncCall(bar,[ArrayLiteral([IntLiteral(2)],StringType,[StringLiteral(1),StringLiteral(2)])])\n"
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_066(self):
        input = """
        func foo() {
            var a[2] int;
            var b[3] int;
            a := b
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("a", ArrayType([IntLiteral(2)], IntType()), None),
                            VarDecl("b", ArrayType([IntLiteral(3)], IntType()), None),
                            Assign(Id("a"), Id("b")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test_067(self):
        input = """
        func foo(x int, y int) { return x+y; }
        func bar() {
            var a = 10;
            var b = 20.0;
            foo(a, b);
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [ParamDecl("x", IntType()), ParamDecl("y", IntType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("x"), Id("y")))]),
                ),
                FuncDecl(
                    "bar",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("a", IntType(), IntLiteral(10)),
                            VarDecl("b", FloatType(), FloatLiteral(20.0)),
                            FuncCall("foo", [Id("a"), Id("b")]),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: FuncCall(foo,[Id(a),Id(b)])\n"
        self.assertTrue(TestChecker.test(input, expect, 467))

    def test_068(self):
        input = """
        func foo() {
            var a[2] int;
            var b[3] int;
            a := b
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("a", ArrayType([IntLiteral(2)], IntType()), None),
                            VarDecl("b", ArrayType([IntLiteral(3)], IntType()), None),
                            Assign(Id("a"), Id("b")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test_069(self):
        input = """
        func coconut(a [2] float) {
            coconut([2] float {1.0,2.0})
            coconut([2] int {1,2})
        }
        """
        input = Program(
            [
                FuncDecl(
                    "coconut",
                    [ParamDecl("a", ArrayType([IntLiteral(2)], FloatType()))],
                    VoidType(),
                    Block(
                        [
                            FuncCall(
                                "coconut",
                                [
                                    ArrayLiteral(
                                        [IntLiteral(2)],
                                        FloatType(),
                                        [FloatLiteral(1.0), FloatLiteral(2.0)],
                                    )
                                ],
                            ),
                            FuncCall(
                                "coconut",
                                [
                                    ArrayLiteral(
                                        [IntLiteral(2)],
                                        IntType(),
                                        [IntLiteral(1), IntLiteral(2)],
                                    )
                                ],
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: FuncCall(coconut,[ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)])])\n"
        self.assertTrue(TestChecker.test(input, expect, 469))

    def test_070(self):
        input = """
        type Car1 struct {seats int;}
        type Car2 interface {honk();}

        func (c Car1) honk() {return;}

        var car1 [2] Car1;
        var car2 [2] Car2 = car1;
        """
        input = Program(
            [
                StructType("Car1", [("seats", IntType())], []),
                InterfaceType("Car2", [Prototype("honk", [], VoidType())]),
                MethodDecl(
                    "c",
                    Id("Car1"),
                    FuncDecl(
                        "honk",
                        [],
                        VoidType(),
                        Block([Return(None)]),
                    ),
                ),
                VarDecl("car1", ArrayType([IntLiteral(2)], Id("Car1")), None),
                VarDecl("car2", ArrayType([IntLiteral(2)], Id("Car2")), Id("car1")),
            ]
        )
        expect = "Type Mismatch: VarDecl(car2,ArrayType(Id(Car2),[IntLiteral(2)]),Id(car1))\n"
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test_071(self):
        input = """
        var a[2] int;
        var b[2] float;
        func foo() {
            a := b
        }
        """
        input = Program(
            [
                VarDecl("a", ArrayType([IntLiteral(2)], IntType()), None),
                VarDecl("b", ArrayType([IntLiteral(2)], FloatType()), None),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block([Assign(Id("a"), Id("b"))]),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(a),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_072(self):
        input = """
        func foo (b int) {
            var array = [3] int {1,2,3}
            var index = 1.0;
            var value int;

            for index, value := range  array {
                return;
            }
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [ParamDecl("b", IntType())],
                    VoidType(),
                    Block(
                        [
                            VarDecl(
                                "array",
                                ArrayType([IntLiteral(3)], IntType()),
                                ArrayLiteral(
                                    [IntLiteral(3)],
                                    IntType(),
                                    [IntLiteral(1), IntLiteral(2), IntLiteral(3)],
                                ),
                            ),
                            VarDecl("index", FloatType(), FloatLiteral(1.0)),
                            VarDecl("value", IntType(), None),
                            ForEach(
                                Id("index"),
                                Id("value"),
                                Id("array"),
                                Block([Return(None)]),
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = (
            "Type Mismatch: ForEach(Id(index),Id(value),Id(array),Block([Return()]))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 472))

    def test_073(self):
        input = """
        var a = 10;
        var b = a + "10";
        """
        input = Program(
            [
                VarDecl("a", IntType(), IntLiteral(10)),
                VarDecl("b", StringType(), BinaryOp("+", Id("a"), StringLiteral("10"))),
            ]
        )
        expect = "Type Mismatch: BinaryOp(Id(a),+,StringLiteral(10))\n"
        self.assertTrue(TestChecker.test(input, expect, 473))

    def test_074(self):
        input = """
        func multiply(x int, y float) float { return x * y; }
        var result = multiply(2, 3.5);
        var area = result + "string";
        """
        input = Program(
            [
                FuncDecl(
                    "multiply",
                    [ParamDecl("x", IntType()), ParamDecl("y", FloatType())],
                    FloatType(),
                    Block([Return(BinaryOp("*", Id("x"), Id("y")))]),
                ),
                VarDecl(
                    "result",
                    FloatType(),
                    FuncCall("multiply", [IntLiteral(2), FloatLiteral(3.5)]),
                ),
                VarDecl(
                    "area",
                    StringType(),
                    BinaryOp("+", Id("result"), StringLiteral("string")),
                ),
            ]
        )
        expect = "Type Mismatch: BinaryOp(Id(result),+,StringLiteral(string))\n"
        self.assertTrue(TestChecker.test(input, expect, 474))

    def test_075(self):
        input = """
        type shape struct { width int; height int; }
        func foo() {
            var shape shape;
            shape.width = 5.0;
        }
        """
        input = Program(
            [
                StructType("shape", [("width", IntType()), ("height", IntType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("shape", Id("shape"), None),
                            Assign(
                                FieldAccess(Id("shape"), "width"), FloatLiteral(5.0)
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = (
            "Type Mismatch: Assign(FieldAccess(Id(shape),width),FloatLiteral(5.0))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 475))

    def test_076(self):
        input = """
        var arr = [1, 2, 3];
        var sum = arr[0] + "test";
        """
        input = Program(
            [
                VarDecl(
                    "arr",
                    ArrayType([IntLiteral(3)], IntType()),
                    ArrayLiteral(
                        [IntLiteral(3)],
                        IntType(),
                        [IntLiteral(1), IntLiteral(2), IntLiteral(3)],
                    ),
                ),
                VarDecl(
                    "sum",
                    StringType(),
                    BinaryOp(
                        "+",
                        ArrayCell(Id("arr"), [IntLiteral(0)]),
                        StringLiteral("test"),
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: BinaryOp(ArrayCell(Id(arr),[IntLiteral(0)]),+,StringLiteral(test))\n"
        self.assertTrue(TestChecker.test(input, expect, 476))

    def test_077(self):
        input = """
        type animal struct { sound string; }
        func (dog animal) setsound(){
            dog.sound = 10;
        }
        """
        input = Program(
            [
                StructType("animal", [("sound", StringType())], []),
                MethodDecl(
                    "dog",
                    Id("animal"),
                    FuncDecl(
                        "setsound",
                        [],
                        VoidType(),
                        Block(
                            [Assign(FieldAccess(Id("dog"), "sound"), IntLiteral(10))]
                        ),
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(FieldAccess(Id(dog),sound),IntLiteral(10))\n"
        self.assertTrue(TestChecker.test(input, expect, 477))

    def test_078(self):
        input = """
        type FOO struct {a int; b FOO;}
        var x FOO;
        var y = x.b.a;
        var z = y.x;
        """
        input = Program(
            [
                StructType("FOO", [("a", IntType()), ("b", Id("FOO"))], []),
                VarDecl("x", Id("FOO"), None),
                VarDecl("y", IntType(), FieldAccess(Id("x"), "b")),
                VarDecl("z", IntType(), FieldAccess(Id("y"), "x")),
            ]
        )
        expect = "Type Mismatch: VarDecl(y,IntType,FieldAccess(Id(x),b))\n"
        self.assertTrue(TestChecker.test(input, expect, 478))

    def test_079(self):
        input = """
        var a [2][2] int;
        var b = a[1.0];
        """
        input = Program(
            [
                VarDecl(
                    "a",
                    ArrayType([IntLiteral(2)], ArrayType([IntLiteral(2)], IntType())),
                    None,
                ),
                VarDecl("b", IntType(), ArrayCell(Id("a"), [FloatLiteral(1.0)])),
            ]
        )
        expect = "Type Mismatch: ArrayCell(Id(a),[FloatLiteral(1.0)])\n"
        self.assertTrue(TestChecker.test(input, expect, 479))

    def test_080(self):
        input = """
        var x [2][3] int;
        var y = x[1];
        var z [3] int = y;
        var w [3] string = y;
        """
        input = Program(
            [
                VarDecl(
                    "x",
                    ArrayType([IntLiteral(2)], ArrayType([IntLiteral(3)], IntType())),
                    None,
                ),
                VarDecl(
                    "y",
                    ArrayType([IntLiteral(3)], IntType()),
                    ArrayCell(Id("x"), [IntLiteral(1)]),
                ),
                VarDecl("z", ArrayType([IntLiteral(3)], IntType()), Id("y")),
                VarDecl("w", ArrayType([IntLiteral(3)], StringType()), Id("y")),
            ]
        )
        expect = (
            "Type Mismatch: VarDecl(w,ArrayType(StringType,[IntLiteral(3)]),Id(y))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 480))

    def test_081(self):
        input = """
        func foo(a [2] float) {
            foo([2] float {3.14,3.1415})
            foo([2] boolean {true,false})
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [ParamDecl("a", ArrayType([IntLiteral(2)], FloatType()))],
                    VoidType(),
                    Block(
                        [
                            FuncCall(
                                "foo",
                                [
                                    ArrayLiteral(
                                        [IntLiteral(2)],
                                        FloatType(),
                                        [FloatLiteral(3.14), FloatLiteral(3.1415)],
                                    )
                                ],
                            ),
                            FuncCall(
                                "foo",
                                [
                                    ArrayLiteral(
                                        [IntLiteral(2)],
                                        BoolType(),
                                        [BooleanLiteral(True), BooleanLiteral(False)],
                                    )
                                ],
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: FuncCall(foo,[ArrayLiteral([IntLiteral(2)],BoolType,[BooleanLiteral(true),BooleanLiteral(false)])])\n"
        self.assertTrue(TestChecker.test(input, expect, 481))

    def test_082(self):
        input = """
        type Box struct { length int; }
        func foo() {
            var b Box;
            b.length = 10.5;
        }
        """
        input = Program(
            [
                StructType("Box", [("length", IntType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("b", Id("Box"), None),
                            Assign(FieldAccess(Id("b"), "length"), FloatLiteral(10.5)),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(FieldAccess(Id(b),length),FloatLiteral(10.5))\n"
        self.assertTrue(TestChecker.test(input, expect, 482))

    def test_083(self):
        input = """
        func multiply(a int, b float) float { return a * b; }
        var result = multiply(2, 3.5);
        var area = result + "text";
        """
        input = Program(
            [
                FuncDecl(
                    "multiply",
                    [ParamDecl("a", IntType()), ParamDecl("b", FloatType())],
                    FloatType(),
                    Block([Return(BinaryOp("*", Id("a"), Id("b")))]),
                ),
                VarDecl(
                    "result",
                    FloatType(),
                    FuncCall("multiply", [IntLiteral(2), FloatLiteral(3.5)]),
                ),
                VarDecl(
                    "area",
                    StringType(),
                    BinaryOp("+", Id("result"), StringLiteral("text")),
                ),
            ]
        )
        expect = "Type Mismatch: BinaryOp(Id(result),+,StringLiteral(text))\n"
        self.assertTrue(TestChecker.test(input, expect, 483))

    def test_084(self):
        input = """
        type Rectangle struct { width int; height int; }
        func (r Rectangle) setWidth() {
            r.width = "100";
        }
        """
        input = Program(
            [
                StructType(
                    "Rectangle", [("width", IntType()), ("height", IntType())], []
                ),
                MethodDecl(
                    "r",
                    Id("Rectangle"),
                    FuncDecl(
                        "setWidth",
                        [],
                        VoidType(),
                        Block(
                            [
                                Assign(
                                    FieldAccess(Id("r"), "width"), StringLiteral("100")
                                )
                            ]
                        ),
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(FieldAccess(Id(r),width),StringLiteral(100))\n"
        self.assertTrue(TestChecker.test(input, expect, 484))

    def test_085(self):
        input = """
        var foo = [2] float {69, 96}
        var bar [3] int = foo
        """
        input = Program(
            [
                VarDecl(
                    "foo",
                    ArrayType([IntLiteral(2)], FloatType()),
                    ArrayLiteral(
                        [IntLiteral(2)],
                        FloatType(),
                        [FloatLiteral(69), FloatLiteral(96)],
                    ),
                ),
                VarDecl("bar", ArrayType([IntLiteral(3)], IntType()), Id("foo")),
            ]
        )
        expect = (
            "Type Mismatch: VarDecl(bar,ArrayType(IntType,[IntLiteral(3)]),Id(foo))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test_086(self):
        input = """
        func foo() {
            var x = 5.0;
            var y = "string";
            x = y;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("x", FloatType(), FloatLiteral(5.0)),
                            VarDecl("y", StringType(), StringLiteral("string")),
                            Assign(Id("x"), Id("y")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(x),Id(y))\n"
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_087(self):
        input = """
        var pi int = 3.14;
        """
        input = Program(
            [
                VarDecl("pi", IntType(), FloatLiteral(3.14)),
            ]
        )
        expect = "Type Mismatch: VarDecl(pi,IntType,FloatLiteral(3.14))\n"
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_088(self):
        input = """
        var a [4][6] int;
        var b = a[3.14];
        """
        input = Program(
            [
                VarDecl(
                    "a",
                    ArrayType([IntLiteral(4)], ArrayType([IntLiteral(6)], IntType())),
                    None,
                ),
                VarDecl("b", IntType(), ArrayCell(Id("a"), [FloatLiteral(3.14)])),
            ]
        )
        expect = "Type Mismatch: ArrayCell(Id(a),[FloatLiteral(3.14)])\n"
        self.assertTrue(TestChecker.test(input, expect, 488))

    def test_089(self):
        input = """
        func identity(a int) int { return a; }
        var result = identity(4.5);
        """
        input = Program(
            [
                FuncDecl(
                    "identity",
                    [ParamDecl("a", IntType())],
                    IntType(),
                    Block([Return(Id("a"))]),
                ),
                VarDecl("result", IntType(), FuncCall("identity", [FloatLiteral(4.5)])),
            ]
        )
        expect = "Type Mismatch: FuncCall(identity,[FloatLiteral(4.5)])\n"
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test_090(self):
        input = """
        func greet(name string) string {
            return "Hello, " + name;
        }
        var result = greet(10);
        """
        input = Program(
            [
                FuncDecl(
                    "greet",
                    [ParamDecl("name", StringType())],
                    StringType(),
                    Block(
                        [Return(BinaryOp("+", StringLiteral("Hello, "), Id("name")))]
                    ),
                ),
                VarDecl("result", StringType(), FuncCall("greet", [IntLiteral(10)])),
            ]
        )
        expect = "Type Mismatch: FuncCall(greet,[IntLiteral(10)])\n"
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test_091(self):
        input = """
        type Shape struct { width int; height int; }
        func foo () {
            var shape Shape;
            shape.width = "width";
        }
        """
        input = Program(
            [
                StructType("Shape", [("width", IntType()), ("height", IntType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("shape", Id("Shape"), None),
                            Assign(
                                FieldAccess(Id("shape"), "width"),
                                StringLiteral("width"),
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = (
            "Type Mismatch: Assign(FieldAccess(Id(shape),width),StringLiteral(width))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test_092(self):
        input = """
        var a = [3] int {1, 2, 3};
        var b = [3] string { "a", "b", "c" };
        var c = a + b;
        """
        input = Program(
            [
                VarDecl(
                    "a",
                    ArrayType([IntLiteral(3)], IntType()),
                    ArrayLiteral(
                        [IntLiteral(3)],
                        IntType(),
                        [IntLiteral(1), IntLiteral(2), IntLiteral(3)],
                    ),
                ),
                VarDecl(
                    "b",
                    ArrayType([IntLiteral(3)], StringType()),
                    ArrayLiteral(
                        [IntLiteral(3)],
                        StringType(),
                        [StringLiteral("a"), StringLiteral("b"), StringLiteral("c")],
                    ),
                ),
                VarDecl(
                    "c",
                    ArrayType([IntLiteral(3)], StringType()),
                    BinaryOp("+", Id("a"), Id("b")),
                ),
            ]
        )
        expect = "Type Mismatch: BinaryOp(Id(a),+,Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_093(self):
        input = """
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_094(self):
        input = """
        func add(x int, y string) int {
            return x + y;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "add",
                    [ParamDecl("x", IntType()), ParamDecl("y", StringType())],
                    IntType(),
                    Block([Return(BinaryOp("+", Id("x"), Id("y")))]),
                ),
            ]
        )
        expect = "Type Mismatch: BinaryOp(Id(x),+,Id(y))\n"
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_095(self):
        input = """
        func foo() {
            var x = 10;
            var y = "test";
            x := y;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("x", IntType(), IntLiteral(10)),
                            VarDecl("y", StringType(), StringLiteral("test")),
                            Assign(Id("x"), Id("y")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(x),Id(y))\n"
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test_096(self):
        input = """
        func foo() {
            var x = 10;
            var y = "test";
            x := y;
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("x", IntType(), IntLiteral(10)),
                            VarDecl("y", StringType(), StringLiteral("test")),
                            Assign(Id("x"), Id("y")),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: Assign(Id(x),Id(y))\n"
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test_097(self):
        input = """
        type car struct { speed int; }
        func foo() {
            var mycar car;
            mycar.speed := 5.5;
        }
        """
        input = Program(
            [
                StructType("car", [("speed", IntType())], []),
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("mycar", Id("car"), None),
                            Assign(
                                FieldAccess(Id("mycar"), "speed"), FloatLiteral(5.5)
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = (
            "Type Mismatch: Assign(FieldAccess(Id(mycar),speed),FloatLiteral(5.5))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_098(self):
        input = """
        type struct struct {a int;}
        type interface interface {foo();}

        func (s struct) foo() {return;}

        var b [2] struct;
        var a [2] interface = b;
        """
        input = Program(
            [
                StructType("struct", [("a", IntType())], []),
                InterfaceType("interface", [Prototype("foo", [], VoidType())]),
                MethodDecl(
                    "s",
                    Id("struct"),
                    FuncDecl(
                        "foo",
                        [],
                        VoidType(),
                        Block([Return(None)]),
                    ),
                ),
                VarDecl("b", ArrayType([IntLiteral(2)], Id("struct")), None),
                VarDecl("a", ArrayType([IntLiteral(2)], Id("interface")), Id("b")),
            ]
        )
        expect = (
            "Type Mismatch: VarDecl(a,ArrayType(Id(interface),[IntLiteral(2)]),Id(b))\n"
        )
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test_099(self):
        input = """
        type shape struct { width int; height int; }
        func foo() {
            var s shape;
            s.width = "width";
        }
        """
        input = Program(
            [
                FuncDecl(
                    "foo",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("s", Id("shape"), None),
                            Assign(
                                FieldAccess(Id("s"), "width"), StringLiteral("width")
                            ),
                        ]
                    ),
                ),
            ]
        )
        expect = "Type Mismatch: FieldAccess(Id(s),width)\n"
        self.assertTrue(TestChecker.test(input, expect, 499))
