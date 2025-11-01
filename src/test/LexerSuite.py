import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):
    def test_000(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "thisavar and thistoo", "thisavar,and,thistoo,<EOF>", 100
            )
        )

    def test_001(self):
        self.assertTrue(TestLexer.checkLexeme("x", "x,<EOF>", 101))

    def test_002(self):
        self.assertTrue(
            TestLexer.checkLexeme("_thayPhungdeptrai", "_thayPhungdeptrai,<EOF>", 102)
        )

    def test_003(self):
        self.assertTrue(TestLexer.checkLexeme("abc123", "abc123,<EOF>", 103))

    def test_004(self):
        self.assertTrue(
            TestLexer.checkLexeme("my-variable", "my,-,variable,<EOF>", 104)
        )

    def test_005(self):
        self.assertTrue(TestLexer.checkLexeme("ab?sVN", "ab,ErrorToken ?", 105))

    def test_006(self):
        self.assertTrue(TestLexer.checkLexeme("_", "_,<EOF>", 106))

    def test_007(self):
        self.assertTrue(TestLexer.checkLexeme("[]", "[,],<EOF>", 107))

    def test_008(self):
        self.assertTrue(TestLexer.checkLexeme("()", "(,),<EOF>", 108))

    def test_009(self):
        self.assertTrue(TestLexer.checkLexeme("{}", "{,},<EOF>", 109))

    def test_010(self):
        self.assertTrue(TestLexer.checkLexeme("if", "if,<EOF>", 110))

    def test_011(self):
        self.assertTrue(TestLexer.checkLexeme("else", "else,<EOF>", 111))

    def test_012(self):
        self.assertTrue(TestLexer.checkLexeme("for", "for,<EOF>", 112))

    def test_013(self):
        self.assertTrue(TestLexer.checkLexeme("return", "return,<EOF>", 113))

    def test_014(self):
        self.assertTrue(TestLexer.checkLexeme("func", "func,<EOF>", 114))

    def test_015(self):
        self.assertTrue(TestLexer.checkLexeme("type", "type,<EOF>", 115))

    def test_016(self):
        self.assertTrue(TestLexer.checkLexeme("break", "break,<EOF>", 116))

    def test_017(self):
        self.assertTrue(TestLexer.checkLexeme("struct", "struct,<EOF>", 117))

    def test_018(self):
        self.assertTrue(TestLexer.checkLexeme("interface", "interface,<EOF>", 118))

    def test_019(self):
        self.assertTrue(TestLexer.checkLexeme("string", "string,<EOF>", 119))

    def test_020(self):
        self.assertTrue(TestLexer.checkLexeme("int", "int,<EOF>", 120))

    def test_021(self):
        self.assertTrue(TestLexer.checkLexeme("float", "float,<EOF>", 121))

    def test_022(self):
        self.assertTrue(TestLexer.checkLexeme("boolean", "boolean,<EOF>", 122))

    def test_023(self):
        self.assertTrue(TestLexer.checkLexeme("const", "const,<EOF>", 123))

    def test_024(self):
        self.assertTrue(TestLexer.checkLexeme("var", "var,<EOF>", 124))

    def test_025(self):
        self.assertTrue(TestLexer.checkLexeme("continue", "continue,<EOF>", 125))

    def test_026(self):
        self.assertTrue(TestLexer.checkLexeme("range", "range,<EOF>", 126))

    def test_027(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "if else for return func type break struct interface string int float boolean const var continue range",
                "if,else,for,return,func,type,break,struct,interface,string,int,float,boolean,const,var,continue,range,<EOF>",
                127,
            )
        )

    def test_028(self):
        self.assertTrue(TestLexer.checkLexeme("+", "+,<EOF>", 128))

    def test_029(self):
        self.assertTrue(TestLexer.checkLexeme("-", "-,<EOF>", 129))

    def test_030(self):
        self.assertTrue(TestLexer.checkLexeme("*", "*,<EOF>", 130))

    def test_031(self):
        self.assertTrue(TestLexer.checkLexeme("/", "/,<EOF>", 131))

    def test_032(self):
        self.assertTrue(TestLexer.checkLexeme("%", "%,<EOF>", 132))

    def test_033(self):
        self.assertTrue(TestLexer.checkLexeme("+-*/%", "+,-,*,/,%,<EOF>", 133))

    def test_034(self):
        self.assertTrue(TestLexer.checkLexeme("==", "==,<EOF>", 134))

    def test_035(self):
        self.assertTrue(TestLexer.checkLexeme("!=", "!=,<EOF>", 135))

    def test_036(self):
        self.assertTrue(TestLexer.checkLexeme("<", "<,<EOF>", 136))

    def test_037(self):
        self.assertTrue(TestLexer.checkLexeme("<=", "<=,<EOF>", 137))

    def test_038(self):
        self.assertTrue(TestLexer.checkLexeme(">", ">,<EOF>", 138))

    def test_039(self):
        self.assertTrue(TestLexer.checkLexeme(">=", ">=,<EOF>", 139))

    def test_040(self):
        self.assertTrue(
            TestLexer.checkLexeme("== != < <= > >=", "==,!=,<,<=,>,>=,<EOF>", 140)
        )

    def test_041(self):
        self.assertTrue(TestLexer.checkLexeme("&&", "&&,<EOF>", 141))

    def test_042(self):
        self.assertTrue(TestLexer.checkLexeme("||", "||,<EOF>", 142))

    def test_043(self):
        self.assertTrue(TestLexer.checkLexeme("!", "!,<EOF>", 143))

    def test_044(self):
        self.assertTrue(TestLexer.checkLexeme("&&||!", "&&,||,!,<EOF>", 144))

    def test_045(self):
        self.assertTrue(TestLexer.checkLexeme(":=", ":=,<EOF>", 145))

    def test_046(self):
        self.assertTrue(TestLexer.checkLexeme("+=", "+=,<EOF>", 146))

    def test_047(self):
        self.assertTrue(TestLexer.checkLexeme("-=", "-=,<EOF>", 147))

    def test_048(self):
        self.assertTrue(TestLexer.checkLexeme("*=", "*=,<EOF>", 148))

    def test_049(self):
        self.assertTrue(TestLexer.checkLexeme("/=", "/=,<EOF>", 149))

    def test_050(self):
        self.assertTrue(TestLexer.checkLexeme("%=", "%=,<EOF>", 150))

    def test_051(self):
        self.assertTrue(TestLexer.checkLexeme("=", "=,<EOF>", 151))

    def test_052(self):
        self.assertTrue(
            TestLexer.checkLexeme(":=+=-=*=/=%==", ":=,+=,-=,*=,/=,%=,=,<EOF>", 152)
        )

    def test_053(self):
        self.assertTrue(TestLexer.checkLexeme(".", ".,<EOF>", 153))

    def test_054(self):
        self.assertTrue(TestLexer.checkLexeme(",", ",,<EOF>", 154))

    def test_055(self):
        self.assertTrue(TestLexer.checkLexeme(";", ";,<EOF>", 155))

    def test_056(self):
        self.assertTrue(TestLexer.checkLexeme(":", ":,<EOF>", 156))

    def test_057(self):
        self.assertTrue(TestLexer.checkLexeme(",;:", ",,;,:,<EOF>", 157))

    def test_058(self):
        self.assertTrue(TestLexer.checkLexeme("123", "123,<EOF>", 158))

    def test_059(self):
        self.assertTrue(TestLexer.checkLexeme("0123", "0,123,<EOF>", 159))

    def test_060(self):
        self.assertTrue(TestLexer.checkLexeme("0b101", "0b101,<EOF>", 160))

    def test_061(self):
        self.assertTrue(TestLexer.checkLexeme("0B1101", "0B1101,<EOF>", 161))

    def test_062(self):
        self.assertTrue(TestLexer.checkLexeme("0o12", "0o12,<EOF>", 162))

    def test_063(self):
        self.assertTrue(TestLexer.checkLexeme("0O77", "0O77,<EOF>", 163))

    def test_064(self):
        self.assertTrue(TestLexer.checkLexeme("0x1A", "0x1A,<EOF>", 164))

    def test_065(self):
        self.assertTrue(TestLexer.checkLexeme("0XFF", "0XFF,<EOF>", 165))

    def test_066(self):
        self.assertTrue(TestLexer.checkLexeme("1.0", "1.0,<EOF>", 166))

    def test_067(self):
        self.assertTrue(TestLexer.checkLexeme("1.0e1", "1.0e1,<EOF>", 167))

    def test_068(self):
        self.assertTrue(TestLexer.checkLexeme("1.e1", "1.e1,<EOF>", 168))

    def test_069(self):
        self.assertTrue(TestLexer.checkLexeme("1.E1", "1.E1,<EOF>", 169))

    def test_070(self):
        self.assertTrue(TestLexer.checkLexeme("0.", "0.,<EOF>", 170))

    def test_071(self):
        self.assertTrue(
            TestLexer.checkLexeme(""" "hello" """, """"hello",<EOF>""", 171)
        )

    def test_072(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                """ "string with newline\\n" """,
                """"string with newline\\n",<EOF>""",
                172,
            )
        )

    def test_073(self):
        self.assertTrue(TestLexer.checkLexeme("true", "true,<EOF>", 173))

    def test_074(self):
        self.assertTrue(TestLexer.checkLexeme("false", "false,<EOF>", 174))

    def test_075(self):
        self.assertTrue(TestLexer.checkLexeme("true,false", "true,,,false,<EOF>", 175))

    def test_076(self):
        self.assertTrue(TestLexer.checkLexeme("nil", "nil,<EOF>", 176))

    def test_077(self):
        self.assertTrue(
            TestLexer.checkLexeme("var arr [5]int", "var,arr,[,5,],int,<EOF>", 177)
        )

    def test_078(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "var multi_arr [2][5]int;",
                "var,multi_arr,[,2,],[,5,],int,;,<EOF>",
                178,
            )
        )

    def test_079(self):
        self.assertTrue(
            TestLexer.checkLexeme("//im a comment, what do you expect", "<EOF>", 179)
        )

    def test_080(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "/* I'm also a comment but im a chunky one */", "<EOF>", 180
            )
        )

    def test_081(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "/* im /* a /* nested /* one */ */ */ */", "<EOF>", 181
            )
        )

    def test_082(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "/* hehe // what /* it should stop here right */", "<EOF>", 182
            )
        )

    def test_083(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                ' "remember to close your strings',
                'Unclosed string: "remember to close your strings',
                183,
            )
        )

    def test_084(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                """ "Serve your sentence and dont esacpe\\f" """,
                'Illegal escape in string: "Serve your sentence and dont esacpe\\f',
                184,
            )
        )

    def test_085(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                "+ - * / % == != > < <= >= && || ! = += -= *= /= %= :=",
                "+,-,*,/,%,==,!=,>,<,<=,>=,&&,||,!,=,+=,-=,*=,/=,%=,:=,<EOF>",
                185,
            )
        )

    def test_086(self):
        self.assertTrue(TestLexer.checkLexeme("\t\f\r ", "<EOF>", 186))

    def test_087(self):
        self.assertTrue(
            TestLexer.checkLexeme(""" "\\r \\r \\r" """, '"\\r \\r \\r",<EOF>', 187)
        )

    def test_088(self):
        self.assertTrue(TestLexer.checkLexeme("?", "ErrorToken ?", 188))

    def test_089(self):
        self.assertTrue(TestLexer.checkLexeme("@", "ErrorToken @", 189))

    def test_090(self):
        self.assertTrue(
            TestLexer.checkLexeme(""" 123" """, '123,Unclosed string: " ', 190)
        )

    def test_091(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                """ "123
        " """,
                'Unclosed string: "123',
                191,
            )
        )

    def test_092(self):
        self.assertTrue(TestLexer.checkLexeme("1.0E+1", "1.0E+1,<EOF>", 192))

    def test_093(self):
        self.assertTrue(TestLexer.checkLexeme("1.0Ee1", "1.0,Ee1,<EOF>", 193))

    def test_094(self):
        self.assertTrue(TestLexer.checkLexeme("0xll", "0,xll,<EOF>", 194))

    def test_095(self):
        self.assertTrue(
            TestLexer.checkLexeme(
                """p := Person{name: "Alice", age: 30}""",
                """p,:=,Person,{,name,:,"Alice",,,age,:,30,},<EOF>""",
                195,
            )
        )

    def test_096(self):
        self.assertTrue(
            TestLexer.checkLexeme("func hello()", "func,hello,(,),<EOF>", 196)
        )

    def test_097(self):
        self.assertTrue(TestLexer.checkLexeme("var z int", "var,z,int,<EOF>", 197))

    def test_098(self):
        self.assertTrue(TestLexer.checkLexeme("-012", "-,0,12,<EOF>", 198))

    def test_099(self):
        self.assertTrue(
            TestLexer.checkLexeme("var y = 100;", "var,y,=,100,;,<EOF>", 199)
        )
