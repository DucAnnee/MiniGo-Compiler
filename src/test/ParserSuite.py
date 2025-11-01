import unittest
from TestUtils import TestParser


class ParserSuite(unittest.TestCase):
    def test_000(self):
        self.assertTrue(
            TestParser.checkParser(
                """var a [2][3][4]int = [2]int{1,2,3};""",
                "successful",
                200,
            )
        )

    def test_001(self):
        self.assertTrue(
            TestParser.checkParser(
                """var a = 0;""",
                "successful",
                201,
            )
        )

    def test_002(self):
        self.assertTrue(
            TestParser.checkParser(
                """var a int = 0;""",
                "successful",
                202,
            )
        )

    def test_003(self):
        self.assertTrue(
            TestParser.checkParser(
                """var a hehe = 0;""",
                "successful",
                203,
            )
        )

    def test_004(self):
        self.assertTrue(
            TestParser.checkParser(
                """var a float""",
                "Error on line 1 col 12: <EOF>",
                204,
            )
        )

    def test_005(self):
        self.assertTrue(
            TestParser.checkParser(
                """var a int
                """,
                "successful",
                205,
            )
        )

    def test_006(self):
        self.assertTrue(
            TestParser.checkParser(
                """const a = 0;""",
                "successful",
                206,
            )
        )

    def test_007(self):
        self.assertTrue(
            TestParser.checkParser(
                """const a = Cat{name: "Acorn", breed: "unknown"};""",
                "successful",
                207,
            )
        )

    def test_008(self):
        self.assertTrue(
            TestParser.checkParser(
                """const a = 100+50;""",
                "successful",
                208,
            )
        )

    def test_009(self):
        self.assertTrue(
            TestParser.checkParser(
                """const int a = 100;""",
                "Error on line 1 col 7: int",
                209,
            )
        )

    def test_010(self):
        self.assertTrue(
            TestParser.checkParser(
                """const int a = [1][2]arr{{1,2,3},{4,5}};""",
                "Error on line 1 col 7: int",
                210,
            )
        )

    def test_011(self):
        self.assertTrue(
            TestParser.checkParser(
                """
                func add() int {
                    
                }
                """,
                "successful",
                211,
            )
        )

    def test_012(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add(a int, b int) int {
                return a + b;
            }
        """,
                "successful",
                212,
            )
        )

    def test_013(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add() {
                return ;
            }
        """,
                "successful",
                213,
            )
        )

    def test_014(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add(a,b int) int {
                return a + b;
            }
        """,
                "successful",
                214,
            )
        )

    def test_015(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add(a,b int) {
                return a + b;
            }
        """,
                "successful",
                215,
            )
        )

    def test_016(self):
        self.assertTrue(
            TestParser.checkParser(
                """
             func add() {
                return ;
            }
        """,
                "successful",
                216,
            )
        )

    def test_017(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add() int {
            
            }
        """,
                "successful",
                217,
            )
        )

    def test_018(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add() hehe {
                return ;
            }
        """,
                "successful",
                218,
            )
        )

    def test_019(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func _(a int) float {
                return ;
            }
        """,
                "successful",
                219,
            )
        )

    def test_020(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func add(a,b int) int {return;}
            func minus() imastruct {return;}
        """,
                "successful",
                220,
            )
        )

    def test_021(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func (c Calculator) add(a,b int) int {return;}
        """,
                "successful",
                221,
            )
        )

    def test_022(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func (c Calculator) Add(x int) int {
                c.value += x;
                return c.value;
            }
        """,
                "successful",
                222,
            )
        )

    def test_023(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func (p Person) getAge() int {
                return p.age;
                return;
                break; break
            }
        """,
                "successful",
                223,
            )
        )

    def test_024(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func (r Receiver) foo() Receiver {
                return r;
            }
        """,
                "successful",
                224,
            )
        )

    def test_025(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func (f Foo) bar() {
                continue;
                INeedSleep();
            }
        """,
                "successful",
                225,
            )
        )

    def test_026(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            const x = 0b11;
        """,
                "successful",
                226,
            )
        )

    def test_027(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x = [1]int{1};
        """,
                "successful",
                227,
            )
        )

    def test_028(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x = [1.0]int{1};
        """,
                "Error on line 2 col 22: 1.0",
                228,
            )
        )

    def test_029(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x imastruct = IDontKnow{};  
        """,
                "successful",
                229,
            )
        )

    def test_030(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x imastruct = IDontKnow{a: 1, b: 2, c: 1 + 2};  
        """,
                "successful",
                230,
            )
        )

    def test_031(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x randomtype = a >= 2 <= 3 > 5;
        """,
                "successful",
                231,
            )
        )

    def test_032(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x = a.b.c.d[e][f].g.h[i];
        """,
                "successful",
                232,
            )
        )

    def test_033(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x int = a[1][2][1+2];
        """,
                "successful",
                233,
            )
        )

    def test_034(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x randomtype = foo(1,2).bar(3).baz()[4].qux();
        """,
                "successful",
                234,
            )
        )

    def test_035(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            const x = (-1 + 1.0 - 3) >= 3;
        """,
                "successful",
                235,
            )
        )

    def test_036(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x = ((((1+2)))) + 3;
        """,
                "successful",
                236,
            )
        )

    def test_037(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x boolean = true;
        """,
                "successful",
                237,
            )
        )

    def test_038(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x boolean = a || b && c;
        """,
                "successful",
                238,
            )
        )

    def test_039(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x boolean = a == b != c < d <= d > e >= f;
        """,
                "successful",
                239,
            )
        )

    def test_040(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x boolean = a + b - c * d / e % f;
        """,
                "successful",
                240,
            )
        )

    def test_041(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            const x = !a - b + (-c);
        """,
                "successful",
                241,
            )
        )

    def test_042(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var a randomtype = b[0][1][2][3][4][5][6][7][8][9];
        """,
                "successful",
                242,
            )
        )

    def test_043(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                x := 1; 
                x += 2;
                x /= a[2].b[3].c[4];
                x %= 5;
                x *= 6;
                break;
                continue
            }
        """,
                "successful",
                243,
            )
        )

    def test_044(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                a.c[2].d[3].e.f += (1 / 2) > 4;
            }
        """,
                "successful",
                244,
            )
        )

    def test_045(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                a.foo() += 100 + 50;
            } 
        """,
                "Error on line 3 col 25: +=",
                245,
            )
        )

    def test_046(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                a[1+2&&3] += foo().b[4];
            }
        """,
                "successful",
                246,
            )
        )

    def test_047(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                 if (x > 10) {
                     println("x is greater than 10");
                 } else if (x == 10) {
                     println("x is equal to 10");
                 } else {
                     println("x is less than 10");
                 }
            }
        """,
                "successful",
                247,
            )
        )

    def test_048(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                if (x > 10) {return;}
            }
        """,
                "successful",
                248,
            )
        )

    def test_049(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                if (x > 10) {
                    return;
                } else if (x == 10) {
                    printLn("x is equal to 10");
                }
            }
        """,
                "successful",
                249,
            )
        )

    def test_050(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                if (x > 10) {
                    return;
                } else {
                    printLn("x is less than 10");
                }
            }
        """,
                "successful",
                250,
            )
        )

    def test_051(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for i < 10 {
                    println("i is less than 10");
                }
            }
        """,
                "successful",
                251,
            )
        )

    def test_052(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for (i > 10 && i < 20) {   
                    println("i is between 10 and 20");
                }
            }
        """,
                "successful",
                252,
            )
        )

    def test_053(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for true + 1 + foo().bar {
                    return;
                }
            }
        """,
                "successful",
                253,
            )
        )

    def test_054(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for 1 {
                    return;
                }
            }
        """,
                "successful",
                254,
            )
        )

    def test_055(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for i := 0; i < 10; i += 1 {
                    return i;
                }
            } 
        """,
                "successful",
                255,
            )
        )

    def test_056(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for it := 11+2; it <= 100; it /= 2 {
                    println(it);
                    continue;
                }
            }
        """,
                "successful",
                256,
            )
        )

    def test_057(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for var i = 0; i < 10; i += 1 {
                    return i;
                }
            }
        """,
                "successful",
                257,
            )
        )

    def test_058(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for i := (2 + b.foo()[2] && true - 1110); i < 10; i += 1 {
                    print(i);
                }
            }
        """,
                "successful",
                258,
            )
        )

    def test_059(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for index, value := range array {
                    println(index, value);
                }
            }
        """,
                "successful",
                259,
            )
        )

    def test_060(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for _, val := range arr[0] {
                    println(val);
                }
            }
        """,
                "successful",
                260,
            )
        )

    def test_061(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for i := 0; i < 10; i += 1 { 
                    if (i == 5) {
                        break;
                    } else { continue; }
                }
            }
        """,
                "successful",
                261,
            )
        )

    def test_062(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z += 1;
            }
        """,
                "successful",
                262,
            )
        )

    def test_063(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            
        """,
                "Error on line 3 col 9: <EOF>",
                263,
            )
        )

    def test_064(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {return;}
            func test1() {return arr;}
            func test2() {print("lets go");}
            """,
                "successful",
                264,
            )
        )

    def test_065(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                if (x.foo().bar[2]) {
                    x := 2;
                } else if (a && b || c) {
                    x := c;
                } else {
                    return;
                }
            }
        """,
                "successful",
                265,
            )
        )

    def test_066(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                var arr = [1][2]a{{1,2},{3,4}};
            }
        """,
                "successful",
                266,
            )
        )

    def test_067(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                var arr = [1][2]a{{"true","false"},{true,false}}; 
            }
        """,
                "successful",
                267,
            )
        )

    def test_068(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                var arr = [1.0][2]a{{1,2},{3,4}};
                var arr = [1][2]a{{1,2},{3,4}};
                break;
            }
        """,
                "Error on line 3 col 28: 1.0",
                268,
            )
        )

    def test_069(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                break;
                continue;
                return;
            }
        """,
                "successful",
                269,
            )
        )

    def test_070(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                return
                return a + b[1].c
                break; break
                return a
            }
        """,
                "successful",
                270,
            )
        )

    def test_071(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for i := 0; i < 10; i += 1 {
                    for j := 0; j < 10; j += 1 {
                        if (i == j) {
                            break;
                        }
                    }
                }
            }
        """,
                "successful",
                271,
            )
        )

    def test_072(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                for _, val := range arr[0] {
                    for _, val := range arr[1] {
                        for _, val := range arr[2] {
                            print (val);
                        }
                    }
                }
            }
        """,
                "successful",
                272,
            )
        )

    def test_073(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            const x = [1]int{{0x11, 0b11}, {0B0101, 0O12, 0o22}}; 
        """,
                "successful",
                273,
            )
        )

    def test_074(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            const a = [c1][c2]int{{1,2},{3,4}};
        """,
                "successful",
                274,
            )
        )

    def test_075(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var a;
        """,
                "Error on line 2 col 18: ;",
                275,
            )
        )

    def test_076(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var a = {a,b,c};
        """,
                "Error on line 2 col 21: {",
                276,
            )
        )

    def test_077(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                a.foo(1+2, a[2].b[3].c[4]) += 1;
            }
        """,
                "Error on line 3 col 44: +=",
                277,
            )
        )

    def test_078(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            type Calculator struct {
                i int = 2;
            }
        """,
                "Error on line 3 col 23: =",
                278,
            )
        )

    def test_079(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            type Calculator struct {
                model string ;
                price float ;
            }
        """,
                "successful",
                279,
            )
        )

    def test_080(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var i Person;
        """,
                "successful",
                280,
            )
        )

    def test_081(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                i := Person{name: "John", age: 20};
                print(i.name);
            }
        """,
                "successful",
                281,
            )
        )

    def test_082(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            type Calculator interface {
                add(a, b int) int;
                sub(a, b int) int;
                reset()
                display(msg string)
            }
        """,
                "successful",
                282,
            )
        )

    def test_083(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var arr [5]int;
        """,
                "successful",
                283,
            )
        )

    def test_084(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var multi_arr [5][5]int;
        """,
                "successful",
                284,
            )
        )

    def test_085(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            type Calculator interface {
                add(a int, c,d float, e randomtype); reset()
             }
        """,
                "successful",
                285,
            )
        )

    def test_086(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test(x, y int)            int         {return ;};
        """,
                "successful",
                286,
            )
        )

    def test_087(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func (c int) add(a, b int) int (return ;)
        """,
                "Error on line 2 col 21: int",
                287,
            )
        )

    def test_088(self):
        self.assertTrue(
            TestParser.checkParser(
                """ 

""",
                "Error on line 3 col 1: <EOF>",
                288,
            )
        )

    def test_089(self):
        self.assertTrue(
            TestParser.checkParser(
                """
                                                            func test() {
                                                                var a [2][3]int;
                                                            };
        """,
                "successful",
                289,
            )
        )

    def test_090(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            var x int = 10;
            var y = "hello";
            var z int;
        """,
                "successful",
                290,
            )
        )

    def test_091(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            // This is a comment

""",
                "Error on line 4 col 1: <EOF>",
                291,
            )
        )

    def test_092(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            // test def
            func test() {
                var a int = 10;
            }
            func foo() {
                break ;
            }
        """,
                "successful",
                292,
            )
        )

    def test_093(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test(a, b int) boolean {
                if (true) {
                    return a;
                } else {
                    return b;
                }
            }
        """,
                "successful",
                293,
            )
        )

    def test_094(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                var x = 10; 
                foo(); 
                y := bar()[1];
                return ;
            }
        """,
                "successful",
                294,
            )
        )

    def test_095(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                if (1) {
                    return ;
                } else if (2) {
                    return ;
                } else {
                    return ;
                }
            }
        """,
                "successful",
                295,
            )
        )

    def test_096(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            type Calculator interface {

            }
        """,
                "Error on line 4 col 13: }",
                296,
            )
        )

    def test_097(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            type Calculatro struct {

            }
        """,
                "Error on line 4 col 13: }",
                297,
            )
        )

    def test_098(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test(a) [2]int {}
        """,
                "Error on line 2 col 24: )",
                298,
            )
        )

    def test_099(self):
        self.assertTrue(
            TestParser.checkParser(
                """
            func test() {
                const a = 10;
                var x int = 0;
                x := 1
                b += 1 - 2 && 4;
                var b string = "hello";
                if (b == "hello") {
                    return true;
                } else {
                    return false;
                }
                var arr [5]int = [2]a{1,2,3,4,5};
                for _, val := range arr {
                    println(val);
                }
            }
        """,
                "successful",
                299,
            )
        )
