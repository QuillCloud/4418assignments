% checking if the list elements are all atom
all_atom([]).

all_atom([H|T]):-
    atom(H),
    all_atom(T).

% P1
rule_hw(seq(X, Y)):-
    all_atom(X),
    all_atom(Y),
    member(E, X),
    member(E, Y),
    format('~w P1\n', seq(X, Y)),
    !.

% P2a
rule_hw(seq(X, Y)):-
    member(neg(E), Y),
    delete(Y, neg(E), Y_NEW),
    rule_hw(seq([E|X], Y_NEW)),
    format('~w P2a\n', seq(X, Y)),
    !.

% P2b
rule_hw(seq(X, Y)):-
    member(neg(E), X),
    delete(X, neg(E), X_NEW),
    rule_hw(seq(X_NEW, [E|Y])),
    format('~w P2b\n', seq(X, Y)),
    !.

% P3a
rule_hw(seq(X, Y)):-
    member(and(E1, E2), Y),
    delete(Y, and(E1, E2), Y_NEW),
    rule_hw(seq(X, [E1|Y_NEW])),
    rule_hw(seq(X, [E2|Y_NEW])),
    format('~w P3a\n', seq(X, Y)),
    !.

% P3b
rule_hw(seq(X, Y)):-
    member(and(E1, E2), X),
    delete(X, and(E1, E2), X1),
    append([E1, E2], X1, X_NEW),
    rule_hw(seq(X_NEW, Y)),
    format('~w P3b\n', seq(X, Y)),
    !.

% P4a
rule_hw(seq(X, Y)):-
    member(or(E1, E2), Y),
    delete(Y, or(E1, E2), Y1),
    append([E1, E2], Y1, Y_NEW),
    rule_hw(seq(X, Y_NEW)),
    format('~w P4a\n', seq(X, Y)),
    !.

% P4b
rule_hw(seq(X, Y)):-
    member(or(E1, E2), X),
    delete(X, or(E1, E2), X_NEW),
    rule_hw(seq([E1|X_NEW], Y)),
    rule_hw(seq([E2|X_NEW], Y)),
    format('~w P4b\n', seq(X, Y)),
    !.

% P5a
rule_hw(seq(X, Y)):-
    member(imp(E1, E2), Y),
    delete(Y, imp(E1, E2), Y_NEW),
    rule_hw(seq([E1|X], [E2|Y_NEW])),
    format('~w P5a\n', seq(X, Y)),
    !.

% P5b
rule_hw(seq(X, Y)):-
    member(imp(E1, E2), X),
    delete(X, imp(E1, E2), X_NEW),
    rule_hw(seq([E2|X_NEW], Y)),
    rule_hw(seq(X_NEW, [E1|Y])),
    format('~w P5b\n', seq(X, Y)),
    !.

% P6a
rule_hw(seq(X, Y)):-
    member(iff(E1, E2), Y),
    delete(Y, iff(E1, E2), Y_NEW),
    rule_hw(seq([E1|X], [E2|Y_NEW])),
    rule_hw(seq([E2|X], [E1|Y_NEW])),
    format('~w P6a\n', seq(X, Y)),
    !.

% P6b
rule_hw(seq(X, Y)):-
    member(iff(E1, E2), X),
    delete(X, iff(E1, E2), X1),
    append([E1, E2], X1, X_NEW), rule_hw(seq(X_NEW, Y)),
    append([E1, E2], Y, Y_NEW), rule_hw(seq(X1, Y_NEW)),
    format('~w P6b\n', seq(X, Y)),
    !.

