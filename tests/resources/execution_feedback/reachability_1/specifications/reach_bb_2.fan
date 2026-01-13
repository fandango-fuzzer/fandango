<start> ::= <alphanums>
<alphanums> ::= <alphanum> <alphanums> | <alphanum>

minimizing DynamicAnalysis(str(<start>)).DistanceToBB("f9.c", "3")