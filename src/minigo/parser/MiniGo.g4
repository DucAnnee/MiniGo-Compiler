//2252009

grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
def __init__(self, input=None, output:TextIO = sys.stdout):
    super().__init__(input, output)
    self.checkVersion("4.9.2")
    self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
    self._actions = None
    self._predicates = None
    self.preType = None

def emit(self):
    tk = self.type
    self.preType = tk;

    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();

def convertNL(self):
    ending_tokens = {
        self.ID, self.INT_LIT, self.FLOAT_LIT, self.STRING_LIT, self.BOOL_LIT, self.NIL_LIT,
        self.INT, self.FLOAT, self.STRING, self.BOOL, 
        self.RETURN, self.CONTINUE, self.BREAK,
        self.RP, self.RB, self.RC
    }
    if self.preType in ending_tokens:
        return True
    else:
        return False
}

options{
	language = Python3;
}

////////////////////////////////////////////////////////////////////////////////////////
///////////                           PARSER RULES                            //////////
////////////////////////////////////////////////////////////////////////////////////////

                          //------------ 4 Types -----------//

varType     : primType | ID | arrayType;
primType    : INT | FLOAT | STRING | BOOL ;

                          //-------- 4.5 Array Types -------//

dimsType    : (LB exp RB)+ ;
arrayType   : dimsLit (INT | FLOAT | STRING | BOOL | ID) ;


seminl      : (SEMICOLON NL* | NL+) ;

                   //=-=-=-=-=-= 6.6 Literal Expressions =-=-=-=-=-=//

                     //----------- 6.6.1 Array Literal -----------//

arrVal      : primitiveLit | structLit | NIL_LIT | ID ;
arrInitVal  : arrVal | LC arrInit RC ;
arrInit     : arrInitVal COMMA arrInit | arrInitVal ;
dimsLit     : (LB (INT_LIT | ID) RB)+ ;
arrayLit    : arrayType LC arrInit RC ;


                     //---------- 6.6.2 Struct Literal -----------//

structField : ID COLON exp ;
structFieldList: structField COMMA structFieldList | structField ;
structLit   : ID LC structFieldList? RC ;


                     //------- 6.7 Function & Method Call --------//

// funcCall    : (ID dims? DOT)? ID LP argList? RP ;
funcCall    : ID LP expList? RP ;
// methodCall  : ID DOT ID LP expList? RP ;



                   //=-=-=-=-=-=-=-=- 6 Expressions -=-=-=-=-=-=-=-=//

expList     : exp COMMA expList | exp ;

exp         : exp OR andExp | andExp ;
andExp      : andExp AND relExp | relExp ;
relExp      : relExp (EQ | NOT_EQ | LT | LE | GT | GE) plusMinusExp | plusMinusExp ;
plusMinusExp: plusMinusExp (PLUS | MINUS) mulDivModExp | mulDivModExp ;
mulDivModExp: mulDivModExp (MUL | DIV | MOD) notNegExp | notNegExp ;
notNegExp   : (MINUS | NOT) notNegExp | arrStructExp ;
arrStructExp: arrStructExp LB exp RB
            | arrStructExp DOT ID
            | arrStructExp DOT ID LP expList? RP
            | literalExp ;
literalExp  : ID 
            | primitiveLit
            | arrayLit
            | structLit
            | NIL_LIT
            | funcCall 
            | LP exp RP ;

primitiveLit: INT_LIT | FLOAT_LIT | STRING_LIT | BOOL_LIT ;


program     : NL* declList NL* EOF;
declList    : decl seminl declList | decl seminl;


                   //=-=-=-=-=-=-=-=- 5 Declaration -=-=-=-=-=-=-=-=//

decl        : varDecl | constDecl | funcDecl | methodDecl | structDecl | interfaceDecl ;


                     //--------- 5.1 Variable Declaration --------//

varDecl     : VAR ID (varType varInit | varInit | varType) ;
varInit     : DECLARE exp ;


                     //--------- 5.2 Constant Declaration --//

constDecl   : CONST ID DECLARE exp ;


                     //---- 5.3 Function & Method Declaration ----//

idList      : ID COMMA idList | ID ;
param       : (ID | idList) varType ;
paramList   : param COMMA paramList | param ;
receiver    : LP ID ID RP ;
funcFragment: ID LP paramList? RP varType? blockStmt; 
funcDecl    : FUNC funcFragment ;
methodDecl  : FUNC receiver funcFragment ;


                     //---------- 4.6 Struct Declaration ---------//

field       : (ID varType (SEMICOLON NL* | NL+));
fieldList   : NL* field fieldList | field ;
structDecl  : TYPE ID STRUCT (LC NL* fieldList NL* RC) ;


                     //-------- 4.7 Interface Declaration --------//

method      : ID LP paramList? RP varType? ;
methodList  : NL* method (SEMICOLON NL* | NL+) methodList | method seminl ;
interfaceDecl: TYPE ID INTERFACE (LC NL* methodList NL* RC);



                   //=-=-=-=-=-=-=-=-= 7 Statement =-=-=-=-=-=-=-=-=//

stmt        : (declStmt 
            | assignStmt 
            | ifStmt 
            | forStmt 
            | breakStmt 
            | contStmt 
            | callStmt 
            | returnStmt) seminl;

stmtList    : stmt stmtList | stmt;
blockStmt   : LC stmtList? RC;


                     //-------- 7.1 Declaration Statement --------//

declStmt    : (varDecl | constDecl) ;


                     //--------- 7.2 Assignment Statement --------//

assignOp    : ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN ;
lhsDims     : (LB (INT_LIT | ID | exp) RB)+ ;
lhs         : ID (lhsDims | DOT ID)* ;
assignStmt  : lhs assignOp exp ;


                     //------------- 7.3 If Statement ------------//

condBlock   : NL* LP NL* exp NL* RP NL* blockStmt ;
elifClause  : ELSE IF condBlock ;
elseClause  : ELSE NL* blockStmt ;
ifStmt      : IF condBlock (elifClause)* (elseClause)? ;


                     //------------ 7.4 For Statement ------------//

basicFor    : FOR exp blockStmt ;
forInit     : ID assignOp exp | VAR ID ? DECLARE exp ;
forUpdate   : ID assignOp exp ;
complexFor  : FOR forInit SEMICOLON exp SEMICOLON forUpdate blockStmt ;
rangeFor    : FOR (ID COMMA ID) ASSIGN RANGE exp blockStmt ;
forStmt     : basicFor | complexFor | rangeFor ;


                     //----------- 7.5 Break Statement -----------//

breakStmt   : BREAK ;


                     //---------- 7.6 Continue Statement ---------//

contStmt    : CONTINUE ;


                     //------------ 7.7 Call Statement -----------//

// callStmt    : (ID dims? DOT)* (funcCall | methodCall) (SEMICOLON NL* | NL+);
// callBase    : (ID dimsType? DOT) | (funcCall DOT)
// callBaseList: callBase callBaseList | callBase ;
// callStmt    : callBaseList? ID LP expList? RP ;

callBaseVal : ID | funcCall ;
callBase    : callBase dimsType
            | callBase DOT callBaseVal
            | callBaseVal; 

callStmt    : (callBase DOT)? funcCall ;


                     //---------- 7.8 Return Statement -----------//

returnStmt  : RETURN exp? ;



////////////////////////////////////////////////////////////////////////////////////////
///////////                           LEXER RULES                            ///////////
////////////////////////////////////////////////////////////////////////////////////////

                          //--------- 3.2 Comments ---------//
LINE_COMMENT: '//' ~[\r\n]* -> skip ;
// BLOCK_COMMENT : '/*' (BLOCK_COMMENT | ~'*' | '*' ~'/')* '*/' -> skip ;
BLOCK_COMMENT: '/*' (BLOCK_COMMENT | .)*? '*/' -> skip;


                          //-------- 3.3.2 Keywords --------//
IF          : 'if' ;
ELSE        : 'else' ;
FOR         : 'for' ;
RETURN      : 'return' ;
FUNC        : 'func' ;
TYPE        : 'type' ;
BREAK       : 'break' ;
STRUCT      : 'struct' ;
INTERFACE   : 'interface' ;
STRING      : 'string' ;
INT         : 'int' ;
FLOAT       : 'float' ;
BOOL        : 'boolean' ;
CONST       : 'const' ;
VAR         : 'var' ;
CONTINUE    : 'continue' ;
RANGE       : 'range' ;

                          //-------- 3.3.3 Operators -------//

// Arithmetic Operators 
PLUS        : '+' ; 
MINUS       : '-' ; 
MUL         : '*' ; 
DIV         : '/' ; 
MOD         : '%' ; 

// Relational Operators 
EQ          : '==' ; 
NOT_EQ      : '!=' ; 
LT          : '<'  ; 
LE          : '<=' ; 
GT          : '>'  ; 
GE          : '>=' ; 

// Logical Operators 
AND         : '&&' ; 
OR          : '||' ; 
NOT         : '!'  ; 

// Assignment Operators 
ASSIGN      : ':=' ;
PLUS_ASSIGN : '+=' ; 
MINUS_ASSIGN: '-=' ; 
MUL_ASSIGN  : '*=' ; 
DIV_ASSIGN  : '/=' ; 
MOD_ASSIGN  : '%=' ; 
DECLARE     : '='  ;


// Dot Operator 
DOT         : '.'  ;

                          //------- 3.3.4 Separators -------//
LP      : '(' ; 
RP      : ')' ; 
LC      : '{' ; 
RC      : '}' ; 
LB    : '[' ; 
RB    : ']' ; 
COMMA       : ',' ; 
SEMICOLON   : ';' ;
COLON       : ':' ;

                          //-------- 3.3.5 Literals --------//
// Integer Literal
INT_LIT     : DEC_LIT 
            | BIN_LIT
            | OCT_LIT
            | HEX_LIT ;
            
DEC_LIT     : '0' | [1-9] [0-9]* ;
BIN_LIT     : '0' [bB] [01]+ ;
OCT_LIT     : '0' [oO] [0-7]+ ;
HEX_LIT     : '0' [xX] [0-9a-fA-F]+ ;

// Float Literal
fragment EXPONENT: [eE] [+-]? [0-9]+ ;
FLOAT_LIT   : ('0' | [0-9]+) '.' [0-9]* EXPONENT? ;

// String Literal
STRING_LIT  : '"' ( '\\' [ntr"\\] | ~[\\"\r\n] )* '"' ;

// Boolean Literal
BOOL_LIT    : 'true' | 'false' ;

// NIL Literal
NIL_LIT     : 'nil' ;

                          //------ 3.3.1 Identifiers -------//
ID          : [a-zA-Z_][a-zA-Z_0-9]*;



NL: ('\r'? '\n') {
  if self.convertNL():
    self.type = self.SEMICOLON;
    self.text = self.text.replace(self.text, ';');
  else:
    self.skip();
  };

WS: [ \t\f\r]+ -> skip; 

fragment CHAR : ~[\n\\"] | ('\\' [ntr"\\]) ;

ERROR_CHAR: . {raise ErrorToken(self.text)};
UNCLOSE_STRING: '"' CHAR* ('\r\n' | '\n' | EOF) {
  if self.text[-2:] == '\r\n':
    raise UncloseString(self.text[:-2]);
  elif self.text[-1] == '\n':
    raise UncloseString(self.text[:-1]);
  else:
    raise UncloseString(self.text);
  };
ILLEGAL_ESCAPE: '"' CHAR* '\\' ~[rnt"\\] {
  raise IllegalEscape(self.text);
  };
