<start> ::= <number> ;
<number> ::= <non_zero> <digits> | "0" ;
<non_zero> ::= "1" | "2" | "3"| "4" | "5" | "6" | "7" | "8" | "9" ;
<digits> ::= "" | <digit> <digits> ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

int(<number>) == 0;
int(<number>) == 1;
int(<number>) == 2;
int(<number>) == 3;
int(<number>) == 4;
int(<number>) == 5;
int(<number>) == 6;
int(<number>) == 7;
int(<number>) == 8;
int(<number>) == 9;
int(<number>) == 10;