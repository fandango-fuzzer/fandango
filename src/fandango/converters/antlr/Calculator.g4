// https://www.inovex.de/de/blog/building-a-simple-calculator-with-antlr-in-python/

grammar Calculator;

expression 
	: NUMBER						# Number
	| '(' expression ')'			# Parentheses
	| expression TIMES expression	# Multiplication
	| expression DIV expression		# Division
	| expression PLUS expression	# Addition
	| expression MINUS expression	# Subtraction
;

PLUS : '+';
MINUS: '-';
TIMES: '*';
DIV  : '/';
NUMBER : [0-9]+;
WS : [ \r\n\t]+ -> skip;