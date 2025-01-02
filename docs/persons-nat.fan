<start> ::= <person_name> "," <age>;
<person_name> ::= <first_name> " " <last_name>;
<first_name> ::= <name> | "Alice" | "Bob" | "Eve" | "Pablo Diego José Francisco de Paula Juan Nepomuceno Cipriano de la Santísima Trinidad";
<last_name> ::= <name> | "Doe" | "Smith" | "Ruiz Picasso";
<name> ::= <ascii_uppercase_letter><ascii_lowercase_letter>+;
<age> ::= <digit>+;