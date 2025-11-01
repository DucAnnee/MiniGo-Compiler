import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    def test_000(self):
        input = """
func main() {putInt(5);};
"""
        expect = "5"
        self.assertTrue(TestCodeGen.test(input, expect, 500))

    def test_001(self):
        input = """
func main() {var a int = 20;  putInt(a);};
"""
        expect = "20"
        self.assertTrue(TestCodeGen.test(input, expect, 501))

    def test_002(self):
        input = """
var a int = 10; func main() { putInt(a);};
"""
        expect = "10"
        self.assertTrue(TestCodeGen.test(input, expect, 502))

    def test_003(self):
        input = Program(
            [
                FuncDecl(
                    "main",
                    [],
                    VoidType(),
                    Block([FuncCall("putInt", [IntLiteral(25)])]),
                )
            ]
        )
        expect = "25"
        self.assertTrue(TestCodeGen.test(input, expect, 503))

    def test_004(self):
        input = Program(
            [
                FuncDecl(
                    "main",
                    [],
                    VoidType(),
                    Block(
                        [
                            VarDecl("a", IntType(), IntLiteral(500)),
                            FuncCall("putInt", [Id("a")]),
                        ]
                    ),
                )
            ]
        )
        expect = "500"
        self.assertTrue(TestCodeGen.test(input, expect, 504))

    def test_005(self):
        input = Program(
            [
                VarDecl("a", IntType(), IntLiteral(5000)),
                FuncDecl(
                    "main", [], VoidType(), Block([FuncCall("putInt", [Id("a")])])
                ),
            ]
        )
        expect = "5000"
        self.assertTrue(TestCodeGen.test(input, expect, 505))

    def test_006(self):
        input = """
func main() {
    var a float = 3.0;
    putFloat(1 + a)
}
"""
        expect = "4.0"
        self.assertTrue(TestCodeGen.test(input, expect, 506))

    def test_007(self):
        input = """
func main() {
    putIntLn(2 - 3)
    putFloatLn(2 - 3.0)
    putFloatLn(2.0 - 3)
    putFloatLn(2.0 - 3.0)
}
"""
        expect = "-1\n-1.0\n-1.0\n-1.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 507))

    def test_008(self):
        input = """
func main() {
    putIntLn(2 * 3)
    putFloatLn(2 * 3.0)
    putFloatLn(2.0 * 3)
    putFloatLn(2.0 * 3.0)
}
"""
        expect = "6\n6.0\n6.0\n6.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 508))

    def test_009(self):
        input = """
func main() {
    putIntLn(5 / 2)
    putFloatLn(5 / 2.0)
    putFloatLn(5.0 / 2)
    putFloatLn(5.0 / 2.0)
}
"""
        expect = "2\n2.5\n2.5\n2.5\n"
        self.assertTrue(TestCodeGen.test(input, expect, 509))

    def test_010(self):
        input = """
func main() {
    putIntLn(5 % 2)
    putIntLn(2 % 5)
}
"""
        expect = "1\n2\n"
        self.assertTrue(TestCodeGen.test(input, expect, 510))

    def test_011(self):
        input = """
func main() {
    putBoolLn(5 > 2)
    putBoolLn(5 < 2)
    putBoolLn(5 <= 5)
    putBoolLn(5 >= 5)
    putBoolLn(5 == 5)
    putBoolLn(5 != 5)
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 511))

    def test_012(self):
        input = """
func main() {
    putBoolLn(5.0 > 2.0)
    putBoolLn(5.0 < 2.0)
    putBoolLn(5.0 <= 5.0)
    putBoolLn(5.0 >= 5.0)
    putBoolLn(5.0 == 5.0)
    putBoolLn(5.0 != 5.0)
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 512))

    def test_013(self):
        input = """
func main() {
    var a float = 12.0;
    putFloat(1 + a)
}
"""
        expect = "13.0"
        self.assertTrue(TestCodeGen.test(input, expect, 513))

    def test_014(self):
        input = """
func main() {
    var a boolean = 2 + 2 > 3;
    var b int = 2 * 3
    putBoolLn(a && b > 5 || b <= 5)
    putBoolLn(a || b > 5 && b <= 5)
}
"""
        expect = "true\ntrue\n"
        self.assertTrue(TestCodeGen.test(input, expect, 514))

    def test_015(self):
        input = """
func main() {
    putBoolLn(! true)
    putBoolLn(! false)
    putIntLn(-2)
    putFloatLn(-2.0)
}
"""
        expect = "false\ntrue\n-2\n-2.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 515))

    def test_016(self):
        input = """
func foo() int {return 1;}

func main() {
    putInt(foo())
}
"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 516))

    def test_017(self):
        input = """
func main() {
    putIntLn(4 - 3)
    putFloatLn(4 - 3.0)
    putFloatLn(4.0 - 3)
    putFloatLn(4.0 - 3.0)
}
"""
        expect = "1\n1.0\n1.0\n1.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 517))

    def test_018(self):
        input = """
func main() {
    putIntLn(4 * 3)
    putFloatLn(4 * 3.0)
    putFloatLn(4.0 * 3)
    putFloatLn(4.0 * 3.0)
}
"""
        expect = "12\n12.0\n12.0\n12.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 518))

    def test_019(self):
        input = """
func fooString(a string) string { return a; }
func fooInt(a int) int {  return a; }
func fooBool(a boolean) boolean { return a; }
func fooFloat(a float) float {  return a; }

func main() {
    putInt(fooInt(3));
    putFloat(fooFloat(4.5));
    putString(fooString("helloworld"));
    putBool(fooBool(false));
}
"""
        expect = "34.5helloworldfalse"
        self.assertTrue(TestCodeGen.test(input, expect, 519))

    def test_020(self):
        input = """
func main() {
    var a float = 3.0;
    putFloatLn(1 + a)
}
"""
        expect = "4.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 520))

    def test_021(self):
        input = """
func main() {
    putBoolLn(! false)
    putBoolLn(! true)
    putFloatLn(-12.0)
    putIntLn(-12)
}
"""
        expect = "true\nfalse\n-12.0\n-12\n"
        self.assertTrue(TestCodeGen.test(input, expect, 521))

    def test_022(self):
        input = """
func main() {
    putIntLn(6 % 2)
    putIntLn(2 % 6)
}
"""
        expect = "0\n2\n"
        self.assertTrue(TestCodeGen.test(input, expect, 522))

    def test_023(self):
        input = """
func main() {
    var a boolean = 1 + 1 > 3;
    var b int = 2 * 4
    putBoolLn(a && b > 3 || b <= 3)
    putBoolLn(a || b > 3 && b <= 3)
}
"""
        expect = "false\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 523))

    def test_024(self):
        input = """
var a int = 555; func main() { putIntLn(a);};
"""
        expect = "555\n"
        self.assertTrue(TestCodeGen.test(input, expect, 524))

    def test_025(self):
        input = """
var a = 10;
func main() {
    b := a + 10;
    putInt(a)
    putInt(b)
}
"""
        expect = "1020"
        self.assertTrue(TestCodeGen.test(input, expect, 525))

    def test_026(self):
        input = """
func main() {
    putBoolLn(3.0 > 1.0)
    putBoolLn(3.0 < 1.0)
    putBoolLn(3.0 <= 3.0)
    putBoolLn(3.0 >= 3.0)
    putBoolLn(3.0 == 3.0)
    putBoolLn(3.0 != 3.0)
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 526))

    def test_027(self):
        input = """
func main() {
    putIntLn(5 * 2)
    putFloatLn(5 * 2.0)
    putFloatLn(5.0 * 2)
    putFloatLn(5.0 * 2.0)
}
"""
        expect = "10\n10.0\n10.0\n10.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 527))

    def test_028(self):
        input = """
func main() {
    putBoolLn(6 > 3)
    putBoolLn(6 < 3)
    putBoolLn(6 <= 6)
    putBoolLn(6 >= 6)
    putBoolLn(6 == 6)
    putBoolLn(6 != 6)
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 528))

    def test_029(self):
        input = """
var a float = 2.0;
func main() {
    putFloatLn(a)
    var a float = 4;
    putFloatLn(a)
    a := 0
    putFloat(a)
}
"""
        expect = "2.0\n4.0\n0.0"
        self.assertTrue(TestCodeGen.test(input, expect, 529))

    def test_030(self):
        input = """
func main() {
    putIntLn(7 % 3)
    putIntLn(3 % 7)
}
"""
        expect = "1\n3\n"
        self.assertTrue(TestCodeGen.test(input, expect, 530))

    def test_031(self):
        input = """
func main() {
    var a [3] int = [3] int {10, 20, 30};
    putInt(a[0])
}
"""
        expect = "10"
        self.assertTrue(TestCodeGen.test(input, expect, 531))

    def test_032(self):
        input = """
func main() {
    var a [2][3] int = [2][3] int {{10, 20, 30}, {40, 50, 60}};
    putInt(a[1][0])
}
"""
        expect = "40"
        self.assertTrue(TestCodeGen.test(input, expect, 532))

    def test_033(self):
        input = """
func main() {
    var a float = 13.0;
    putFloatLn(1 + a)
}
"""
        expect = "14.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 533))

    def test_034(self):
        input = """
func main() {
    var a [2] int;
    a[0] := 200
    a[1] += a[0] + a[0]
    putInt(a[1])
}
"""
        expect = "400"
        self.assertTrue(TestCodeGen.test(input, expect, 534))

    def test_035(self):
        input = """
func main() {
    var a [2][3] int;
    a[a[1][1]] := [3] int {10,20,30}
    putIntLn(a[0][0] + a[0][2])
}
"""
        expect = "40\n"
        self.assertTrue(TestCodeGen.test(input, expect, 535))

    def test_036(self):
        input = """
func main() {
    var a [2][3] float;
    a[0][0] += 3.0
    putFloat(a[0][0] + a[0][1])
}
"""
        expect = "3.0"
        self.assertTrue(TestCodeGen.test(input, expect, 536))

    def test_037(self):
        input = """
func main() {
    putIntLn(1 * 3)
    putFloatLn(1 * 3.0)
    putFloatLn(1.0 * 3)
    putFloatLn(1.0 * 3.0)
}
"""
        expect = "3\n3.0\n3.0\n3.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 537))

    def test_038(self):
        input = """
var a [2][3] int = [2][3] int {{10, 20, 30}, {40, 50, 60}};
func main() {
    putInt(a[0][2])
}
"""
        expect = "30"
        self.assertTrue(TestCodeGen.test(input, expect, 538))

    def test_039(self):
        input = """
func main() {
    var a [1] int ;
    a[0] := 10
    putIntLn(a[0]);
}
"""
        expect = "10\n"
        self.assertTrue(TestCodeGen.test(input, expect, 539))

    def test_040(self):
        input = """
func main() {
    var a [1][1][1] int  = [1][1][1] int {{{0}}};
    a[0][0][0] := 0
    putInt(a[0][0][0]);
}
"""
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 540))

    def test_041(self):
        input = """
func main() {
    putIntLn(9 % 3)
    putIntLn(3 % 9)
}
"""
        expect = "0\n3\n"
        self.assertTrue(TestCodeGen.test(input, expect, 541))

    def test_042(self):
        input = """
func main() {
    if (true) {
        putFloat(12.2)
    }
}
"""
        expect = "12.2"
        self.assertTrue(TestCodeGen.test(input, expect, 542))

    def test_043(self):
        input = """
var a int = 1
func main() {
    if (a >= 0) {
        putBool(true)
    } else {
        putBool(false)
    }
}
"""
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 543))

    def test_044(self):
        input = """
func main() {
    var i = 5;
    for i > 2 {
        putInt(i);
        i -= 1;
    }
    putInt(i);
}
"""
        expect = "5432"
        self.assertTrue(TestCodeGen.test(input, expect, 544))

    def test_045(self):
        input = """
func main() {
    var i int;
    for i := 0; i < 10; i += 1 {
        putInt(i)
    }
    putIntLn(i)
}
"""
        expect = "012345678910\n"
        self.assertTrue(TestCodeGen.test(input, expect, 545))

    def test_046(self):
        input = """
const a = "have a nice day"
func main() {
    putStringLn(a)
}
"""
        expect = "have a nice day\n"
        self.assertTrue(TestCodeGen.test(input, expect, 546))

    def test_047(self):
        input = """
const a = 2
func main() {
    var b [a] int;
    putInt(b[0]);
    b[0] := 30;
    b[1] := 40;
    putInt(b[0]);
    putInt(b[1]);
}
"""
        expect = "03040"
        self.assertTrue(TestCodeGen.test(input, expect, 547))

    def test_048(self):
        input = """
func main() {
    var i int;
    for i := 0; i < 10; i += 1 {
        if (i % 2 == 0) {
            continue;
        }
        putIntLn(i);
    }
    putIntLn(i);
}
"""
        expect = "1\n3\n5\n7\n9\n10\n"
        self.assertTrue(TestCodeGen.test(input, expect, 548))

    def test_049(self):
        input = """
type Monitor interface {display();}
type LGTV struct {freq int;}
func (l LGTV) display() {putIntLn(l.freq);}

func main(){
    var m LGTV = LGTV {freq: 165}
    putIntLn(m.freq)
    m.display()
}
"""
        expect = "165\n165\n"
        self.assertTrue(TestCodeGen.test(input, expect, 549))

    def test_050(self):
        input = """
func main() {
    var i = 3;
    for i > 0 {
        putInt(i);
        i -= 1;
    }
    putInt(i);
}
"""
        expect = "3210"
        self.assertTrue(TestCodeGen.test(input, expect, 550))

    def test_051(self):
        input = """
type Calculator struct {price int;}

func main(){
    var c Calculator
    c.price := 100
    putInt(c.price)
}
"""
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 551))

    def test_052(self):
        input = """
var a string = "iwannakms"; func main() { putStringLn(a);};
"""
        expect = "iwannakms\n"
        self.assertTrue(TestCodeGen.test(input, expect, 552))

    def test_053(self):
        input = """
var a int = 0
func main() {
    if (a == 1) {
        putBool(true)
    } else {
        putBool(false)
    }
}
"""
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 553))

    def test_054(self):
        input = """
type Fruit struct {price int;}

func main(){
    var f Fruit
    f.price := 10
    putInt(f.price)
}
"""
        expect = "10"
        self.assertTrue(TestCodeGen.test(input, expect, 554))

    def test_055(self):
        input = """
func main() {var a int = 20;  putIntLn(a);};
"""
        expect = "20\n"
        self.assertTrue(TestCodeGen.test(input, expect, 555))

    def test_056(self):
        input = """
type Fruit struct {price int;}
type Basket struct {price int; fruit Fruit;}

func main(){
    var b Basket
    b.fruit := Fruit {price: 10}
    b.fruit.price := 100
    putInt(b.fruit.price)
}
"""
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 556))

    def test_057(self):
        input = """
type Monitor interface {display();}
type LGTV struct {freq int;}
func (l LGTV) display() {putIntLn(l.freq);}

func main(){
    var m LGTV = nil
    m := LGTV {freq: 165}
    putIntLn(m.freq)
    m.display()
}
"""
        expect = "165\n165\n"
        self.assertTrue(TestCodeGen.test(input, expect, 557))

    def test_058(self):
        input = """
var a string = "what a nice evening"; func main() { putStringLn(a);};
"""
        expect = "what a nice evening\n"
        self.assertTrue(TestCodeGen.test(input, expect, 558))

    def test_059(self):
        input = """
func main() {
    var i int;
    for i := 0; i < 9; i += 1 {
        if (i % 3 == 0) {
            continue;
        }
        putIntLn(i);
    }
    putIntLn(i);
}
"""
        expect = "1\n2\n4\n5\n7\n8\n9\n"
        self.assertTrue(TestCodeGen.test(input, expect, 559))

    def test_060(self):
        input = """
type Cpu struct {price int;}
type Mainboard struct {price int; cpu Cpu;}

func main(){
    var m Mainboard
    m.cpu := Cpu {price: 1000}
    m.cpu.price := 100
    putInt(m.cpu.price)
}
"""
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 560))

    def test_061(self):
        input = """
var a boolean = false; func main() { putBoolLn(a);};
"""
        expect = "false\n"
        self.assertTrue(TestCodeGen.test(input, expect, 561))

    def test_062(self):
        input = """
type Sound interface { makeSound(); }
type Animal struct { typ string; }
func (a Animal) makeSound() { putStringLn(a.typ); }
func main() {
    var animals [2]Sound;
    animals[0] := Animal {typ: "cat"};
    animals[1] := Animal {typ: "dog"};
    animals[0].makeSound(); 
    animals[1].makeSound();
}
"""
        expect = "cat\ndog\n"
        self.assertTrue(TestCodeGen.test(input, expect, 562))

    def test_063(self):
        input = """
func main() {
    var i int = 10;
    for var i int = 0; i < 2; i += 1 {
        putIntLn(i)
    }
    putInt(i)
}
"""
        expect = "0\n1\n10"
        self.assertTrue(TestCodeGen.test(input, expect, 563))

    def test_064(self):
        input = """
type Calculator interface { calc(a int, b int) int; }
type Casio struct {number int;}
func (c Casio) calc(a int, b int) int {
    return a + b;
}
func main() {
    var c Calculator = Casio {};
    var result int = c.calc(1, 2);
    putIntLn(result);
}
"""
        expect = "3\n"
        self.assertTrue(TestCodeGen.test(input, expect, 564))

    def test_065(self):
        input = """
const a = "helloworld"
func main() {
    putString(a)
}
"""
        expect = "helloworld"
        self.assertTrue(TestCodeGen.test(input, expect, 565))

    def test_066(self):
        input = """
func main() {var a int = 90;  putIntLn(a);};
"""
        expect = "90\n"
        self.assertTrue(TestCodeGen.test(input, expect, 566))

    def test_067(self):
        input = """
type Person struct {
    name string;
    age int;
}
func (p Person) getInfo() {
    putStringLn(p.name);
    putIntLn(p.age);
}
func main() {
    var people [2]Person = [2]Person{Person{name: "Jack", age: 19},Person{name: "Jenny", age: 18}};
    people[0].getInfo();
    people[1].getInfo();
}
"""
        expect = "Jack\n19\nJenny\n18\n"
        self.assertTrue(TestCodeGen.test(input, expect, 567))

    def test_068(self):
        input = """
type Monitor interface {display();}
type LGTV struct {freq int;}
func (l LGTV) display() {putIntLn(l.freq);}

func main(){
    var m LGTV
    m := LGTV {freq: 165}
    putIntLn(m.freq)
    m.display()
}
"""
        expect = "165\n165\n"
        self.assertTrue(TestCodeGen.test(input, expect, 568))

    def test_069(self):
        input = """
func main() {
    putIntLn(3 - 1)
    putFloatLn(3 - 1.0)
    putFloatLn(3.0 - 1)
    putFloatLn(3.0 - 1.0)
}
"""
        expect = "2\n2.0\n2.0\n2.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 569))

    def test_070(self):
        input = """
const a = "10diemppl"
func main() {
    putString(a)
}
"""
        expect = "10diemppl"
        self.assertTrue(TestCodeGen.test(input, expect, 570))

    def test_071(self):
        input = """
func main() {
    var a float = 1.0;
    putFloat(1 + a)
}
"""
        expect = "2.0"
        self.assertTrue(TestCodeGen.test(input, expect, 571))

    def test_072(self):
        input = """
func main() {
    var a int = 99;
    putInt(1 + a)
}
"""
        expect = "100"
        self.assertTrue(TestCodeGen.test(input, expect, 572))

    def test_073(self):
        input = """
func main() {
    var a boolean = 2 + 2 > 3;
    putBoolLn(a)
}
"""
        expect = "true\n"
        self.assertTrue(TestCodeGen.test(input, expect, 573))

    def test_074(self):
        input = """
func main() {var a int = 900;  putInt(a);};
"""
        expect = "900"
        self.assertTrue(TestCodeGen.test(input, expect, 574))

    def test_075(self):
        input = """
type Calculator interface { calc(a int, b int) int; }
type Vinacal struct {number int;}
func (v Vinacal) calc(a int, b int) int {
    return a + b;
}
func main() {
    var c Calculator = Vinacal {};
    var result int = c.calc(1, 2);
    putIntLn(result);
}
"""
        expect = "3\n"
        self.assertTrue(TestCodeGen.test(input, expect, 575))

    def test_076(self):
        input = """
func main() {
    putIntLn(3 / 2);
    putFloatLn(3 / 2.0);
    putFloatLn(3.0 / 2);
    putFloatLn(3.0 / 2.0);
}
"""
        expect = "1\n1.5\n1.5\n1.5\n"
        self.assertTrue(TestCodeGen.test(input, expect, 576))

    def test_077(self):
        input = """
var a boolean = true; 
func main() { 
    putBoolLn(a);
}
"""
        expect = "true\n"
        self.assertTrue(TestCodeGen.test(input, expect, 577))

    def test_078(self):
        input = """
func main() {
    putIntLn(10 - 2);
    putFloatLn(10 - 2.0);
    putFloatLn(10.0 - 2);
    putFloatLn(10.0 - 2.0);
}
"""
        expect = "8\n8.0\n8.0\n8.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 578))

    def test_079(self):
        input = """
func main() {
    putBoolLn(4 > 0);
    putBoolLn(4 < 0);
    putBoolLn(4 <= 4);
    putBoolLn(4 >= 4);
    putBoolLn(4 == 4);
    putBoolLn(4 != 4);
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 579))

    def test_080(self):
        input = """
func main() {
    var a [1][1] int  = [1][1] int {{0}};
    a[0][0] := 0;
    putIntLn(a[0][0]);
}
"""
        expect = "0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 580))

    def test_081(self):
        input = """
var a int = 81; func main() { putInt(a);};
"""
        expect = "81"
        self.assertTrue(TestCodeGen.test(input, expect, 581))

    def test_082(self):
        input = """
func main() {
    var a int = 3;
    putFloat(1.0 + a)
}
"""
        expect = "4.0"
        self.assertTrue(TestCodeGen.test(input, expect, 582))

    def test_083(self):
        input = """
func main() {
    var a float = 0.0;
    putFloat(1 + a)
}
"""
        expect = "1.0"
        self.assertTrue(TestCodeGen.test(input, expect, 583))

    def test_084(self):
        input = """
func main() {
    putIntLn(8 - 2)
    putFloatLn(8 - 2.0)
    putFloatLn(8.0 - 2)
    putFloatLn(8.0 - 2.0)
}
"""
        expect = "6\n6.0\n6.0\n6.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 584))

    def test_085(self):
        input = """
func foo(){
    a := 0; 
    putInt(a)
}
var a int = 1
func main(){
    foo()
    putInt(a)
}
"""
        expect = "01"
        self.assertTrue(TestCodeGen.test(input, expect, 585))

    def test_086(self):
        input = """
func main() {
    putIntLn(2 % 3)
    putIntLn(3 % 2)
}
"""
        expect = "2\n1\n"
        self.assertTrue(TestCodeGen.test(input, expect, 586))

    def test_087(self):
        input = """
const a = "good morning";
func main() {
    putString(a);
}
"""
        expect = "good morning"
        self.assertTrue(TestCodeGen.test(input, expect, 587))

    def test_088(self):
        input = """
func main() {
    var a int = 19;
    putInt(1 + a)
}
"""
        expect = "20"
        self.assertTrue(TestCodeGen.test(input, expect, 588))

    def test_089(self):
        input = """
func main() {var a int = 90;  putInt(a);};
"""
        expect = "90"
        self.assertTrue(TestCodeGen.test(input, expect, 589))

    def test_090(self):
        input = """
func main() {
    putIntLn(2 / 2)
    putFloatLn(2 / 2.0)
    putFloatLn(2.0 / 2)
    putFloatLn(2.0 / 2.0)
}
"""
        expect = "1\n1.0\n1.0\n1.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 590))

    def test_091(self):
        input = """
func main() {
    putBoolLn(9 > 3)
    putBoolLn(9 < 1)
    putBoolLn(9 <= 9)
    putBoolLn(9 >= 9)
    putBoolLn(9 == 9)
    putBoolLn(9 != 9)
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 591))

    def test_092(self):
        input = """
func foo(){
    a := 0; 
    putInt(a)
}
var a int = 1
func main(){
    foo()
    putInt(a)
}
"""
        expect = "01"
        self.assertTrue(TestCodeGen.test(input, expect, 592))

    def test_093(self):
        input = """
func main() {
    putIntLn(4 - 0)
    putFloatLn(4 - 0.0)
    putFloatLn(4.0 - 0)
    putFloatLn(4.0 - 0.0)
}
"""
        expect = "4\n4.0\n4.0\n4.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 593))

    def test_094(self):
        input = """
func main() {
    putBoolLn(4.0 > 2.0)
    putBoolLn(4.0 < 2.0)
    putBoolLn(4.0 <= 4.0)
    putBoolLn(4.0 >= 4.0)
    putBoolLn(4.0 == 4.0)
    putBoolLn(4.0 != 4.0)
}
"""
        expect = "true\nfalse\ntrue\ntrue\ntrue\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 594))

    def test_095(self):
        input = """
type Person struct {
    name string;
    age int;
}
func (p Person) getInfo() {
    putStringLn(p.name);
    putIntLn(p.age);
}
func main() {
    var people [2]Person = [2]Person{Person{name: "John", age: 19},Person{name: "Anna", age: 18}};
    people[0].getInfo();
    people[1].getInfo();
}
"""
        expect = "John\n19\nAnna\n18\n"
        self.assertTrue(TestCodeGen.test(input, expect, 595))

    def test_096(self):
        input = """
func main() {
    var a float = 11.0;
    putFloatLn(2 + a)
}
"""
        expect = "13.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 596))

    def test_097(self):
        input = """
func main() {
    putFloat(-12.0)
    putBool(! false)
    putBool(! true)
    putInt(-12)
}
"""
        expect = "-12.0truefalse-12"
        self.assertTrue(TestCodeGen.test(input, expect, 597))

    def test_098(self):
        input = """
func main() {
    putIntLn(7 * 4)
    putFloatLn(7 * 4.0)
    putFloatLn(7.0 * 4)
    putFloatLn(7.0 * 4.0)
}
"""
        expect = "28\n28.0\n28.0\n28.0\n"
        self.assertTrue(TestCodeGen.test(input, expect, 598))

    def test_099(self):
        input = """
func main() {var a int = 20;  putInt(a);};
"""
        expect = "20"
        self.assertTrue(TestCodeGen.test(input, expect, 599))
