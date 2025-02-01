------ FANDANGO FORMAT ------

<INDENT> ::= '<INDENT>';
<DEDENT> ::= '<DEDENT>';

<start> ::= <featureModel>;
<featureModel> ::= <namespace>? <NEWLINE>? <includes>? <NEWLINE>? <imports>? <NEWLINE>? <features>? <NEWLINE>? <constraints>? <EOF>;
<includes> ::= 'include' <NEWLINE> <INDENT> <includeLine>* <DEDENT>;
<includeLine> ::= <languageLevel> <NEWLINE>;

<namespace> ::= 'namespace' <reference>;

<imports> ::= 'imports' <NEWLINE> <INDENT> <importLine>* <DEDENT>;
<importLine> ::= ns=<reference> ('as' alias=<reference>)? <NEWLINE>;


------ ANTLR FORMAT ------

grammar UVL;
importLine: ns=reference ('as' alias=reference)? NEWLINE;

features: 'features' NEWLINE INDENT feature DEDENT;

group
    : ORGROUP groupSpec          # OrGroup
    | ALTERNATIVE groupSpec # AlternativeGroup
    | OPTIONAL groupSpec    # OptionalGroup
    | MANDATORY groupSpec   # MandatoryGroup
    | CARDINALITY groupSpec    # CardinalityGroup
    ;

groupSpec: NEWLINE INDENT feature+ DEDENT;

feature: featureType? reference featureCardinality? attributes? NEWLINE (INDENT group+ DEDENT)?;

featureCardinality: 'cardinality' CARDINALITY;

attributes: OPEN_BRACE (attribute (COMMA attribute)*)? CLOSE_BRACE;

attribute
    : valueAttribute
    | constraintAttribute;

valueAttribute: key value?;

key: id;
value: BOOLEAN | FLOAT | INTEGER | STRING | attributes | vector;
vector: OPEN_BRACK (value (COMMA value)*)? CLOSE_BRACK;

constraintAttribute
    : 'constraint' constraint               # SingleConstraintAttribute
    | 'constraints' constraintList          # ListConstraintAttribute
    ;
constraintList: OPEN_BRACK (constraint (COMMA constraint)*)? CLOSE_BRACK;

constraints: 'constraints' NEWLINE INDENT constraintLine* DEDENT;

constraintLine: constraint NEWLINE;

constraint
    : equation                              # EquationConstraint
    | reference                             # LiteralConstraint
    | OPEN_PAREN constraint CLOSE_PAREN     # ParenthesisConstraint
    | NOT constraint                        # NotConstraint
    | constraint AND constraint             # AndConstraint
    | constraint OR constraint              # OrConstraint
    | constraint IMPLICATION constraint     # ImplicationConstraint
    | constraint EQUIVALENCE constraint     # EquivalenceConstraint
	;

equation
    : expression EQUAL expression           # EqualEquation
    | expression LOWER expression           # LowerEquation
    | expression GREATER expression         # GreaterEquation
    | expression LOWER_EQUALS expression    # LowerEqualsEquation
    | expression GREATER_EQUALS expression  # GreaterEqualsEquation
    | expression NOT_EQUALS expression      # NotEqualsEquation
    ;

expression:
    FLOAT                                   # FloatLiteralExpression
    | INTEGER                               # IntegerLiteralExpression
    | STRING                                # StringLiteralExpression
    | aggregateFunction                     # AggregateFunctionExpression
    | reference                             # LiteralExpression
    | OPEN_PAREN expression CLOSE_PAREN     # BracketExpression
    | expression ADD expression             # AddExpression
    | expression SUB expression             # SubExpression
    | expression MUL expression             # MulExpression
    | expression DIV expression             # DivExpression
    ;

aggregateFunction
    : 'sum' OPEN_PAREN (reference COMMA)? reference CLOSE_PAREN    # SumAggregateFunction
    | 'avg' OPEN_PAREN (reference COMMA)? reference CLOSE_PAREN    # AvgAggregateFunction
    | stringAggregateFunction                                      # StringAggregateFunctionExpression
    | numericAggregateFunction                                     # NumericAggregateFunctionExpression
    ;

stringAggregateFunction
    : 'len' OPEN_PAREN reference CLOSE_PAREN        # LengthAggregateFunction
    ;

numericAggregateFunction
    : 'floor' OPEN_PAREN reference CLOSE_PAREN      # FloorAggregateFunction
    | 'ceil' OPEN_PAREN reference CLOSE_PAREN       # CeilAggregateFunction
    ;

reference: (id '.')* id;
id: ID_STRICT | ID_NOT_STRICT;
featureType: 'String' | 'Integer' | BOOLEAN_KEY | 'Real';



languageLevel: majorLevel ('.' (minorLevel | '*'))?;
majorLevel: BOOLEAN_KEY | 'Arithmetic' | 'Type';
minorLevel: 'group-cardinality' | 'feature-cardinality' | 'aggregate-function' | 'string-constraints';

ORGROUP: 'or';
ALTERNATIVE: 'alternative';
OPTIONAL: 'optional';
MANDATORY: 'mandatory';
CARDINALITY: OPEN_BRACK INTEGER ('..' (INTEGER | '*'))? CLOSE_BRACK;

NOT: '!';
AND: '&';
OR: '|';
EQUIVALENCE: '<=>';
IMPLICATION: '=>';

EQUAL: '==';
LOWER: '<';
LOWER_EQUALS: '<=';
GREATER: '>';
GREATER_EQUALS: '>=';
NOT_EQUALS: '!=';

DIV: '/';
MUL: '*';
ADD: '+';
SUB: '-';

FLOAT: '-'?[0-9]*[.][0-9]+;
INTEGER: '0' | '-'?[1-9][0-9]*;
BOOLEAN: 'true' | 'false';

BOOLEAN_KEY : 'Boolean';

COMMA: ',';


ID_NOT_STRICT: '"'~[\r\n".]+'"';
ID_STRICT: [a-zA-Z]([a-zA-Z0-9_] | '#' | '§' | '%' | '?' | '\\' | '\'' | 'ä' | 'ü' | 'ö' | 'ß' | ';')*;

STRING: '\''~[\r\n'.]+'\'';

SKIP_
  : ( SPACES | COMMENT ) -> skip
  ;

 fragment COMMENT
  : '//' ~[\r\n\f]*
  | OPEN_COMMENT .* CLOSE_COMMENT
  ;

  fragment SPACES
   : [ \t]+
   ;