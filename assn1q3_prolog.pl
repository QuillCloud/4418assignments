% checking if the list elements are all atom
all_atom([]).

all_atom([H|T]):-
    atom(H),
    all_atom(T).

% P1 Rule
% If λ, ζ are strings of atomic formulae,
% then λ ⊢ ζ is a theorem if some atomic formula occurs
% on both side of the sequent ⊢
rule_hw(seq(X, Y)):-
    all_atom(X),
    all_atom(Y),
    member(E, X),
    member(E, Y),
    format('~w P1\n', seq(X, Y)),
    !.

% P2a Rule
% If φ, ζ⊢λ, ρ,then ζ⊢λ, ¬φ, ρ
rule_hw(seq(X, Y)):-
    member(neg(E), Y),
    delete(Y, neg(E), Y_NEW),
    rule_hw(seq([E|X], Y_NEW)),
    format('~w P2a\n', seq(X, Y)),
    !.

% P2b Rule
% If λ, ρ⊢π, φ,then λ, ¬φ, ρ⊢π
rule_hw(seq(X, Y)):-
    member(neg(E), X),
    delete(X, neg(E), X_NEW),
    rule_hw(seq(X_NEW, [E|Y])),
    format('~w P2b\n', seq(X, Y)),
    !.

% P3a Rule
% If ζ⊢λ, φ, ρ and ζ⊢λ, ψ, ρ,then ζ⊢λ, φ∧ψ, ρ
rule_hw(seq(X, Y)):-
    member(and(E1, E2), Y),
    delete(Y, and(E1, E2), Y_NEW),
    rule_hw(seq(X, [E1|Y_NEW])),
    rule_hw(seq(X, [E2|Y_NEW])),
    format('~w P3a\n', seq(X, Y)),
    !.

% P3b Rule
% If λ, φ, ψ, ρ⊢π,then λ, φ∧ψ, ρ⊢π
rule_hw(seq(X, Y)):-
    member(and(E1, E2), X),
    delete(X, and(E1, E2), X1),
    append([E1, E2], X1, X_NEW),
    rule_hw(seq(X_NEW, Y)),
    format('~w P3b\n', seq(X, Y)),
    !.

% P4a Rule
% If ζ⊢λ, φ, ψ, ρ,then ζ⊢λ, φ∨ψ, ρ
rule_hw(seq(X, Y)):-
    member(or(E1, E2), Y),
    delete(Y, or(E1, E2), Y1),
    append([E1, E2], Y1, Y_NEW),
    rule_hw(seq(X, Y_NEW)),
    format('~w P4a\n', seq(X, Y)),
    !.

% P4b Rule
% If λ, φ, ρ⊢π and λ, ψ, ρ⊢π,then λ, φ∨ψ, ρ⊢π
rule_hw(seq(X, Y)):-
    member(or(E1, E2), X),
    delete(X, or(E1, E2), X_NEW),
    rule_hw(seq([E1|X_NEW], Y)),
    rule_hw(seq([E2|X_NEW], Y)),
    format('~w P4b\n', seq(X, Y)),
    !.

% P5a Rule
% If ζ, φ⊢λ, ψ, ρ,then ζ⊢λ, φ→ψ, ρ
rule_hw(seq(X, Y)):-
    member(imp(E1, E2), Y),
    delete(Y, imp(E1, E2), Y_NEW),
    rule_hw(seq([E1|X], [E2|Y_NEW])),
    format('~w P5a\n', seq(X, Y)),
    !.

% P5b Rule
% If λ, ψ, ρ⊢π and λ, ρ⊢π, φ,then λ, φ→ψ, ρ⊢π
rule_hw(seq(X, Y)):-
    member(imp(E1, E2), X),
    delete(X, imp(E1, E2), X_NEW),
    rule_hw(seq([E2|X_NEW], Y)),
    rule_hw(seq(X_NEW, [E1|Y])),
    format('~w P5b\n', seq(X, Y)),
    !.

% P6a Rule
% If φ, ζ⊢λ, ψ, ρ and ψ, ζ⊢λ, φ, ρ,then ζ⊢λ, φ↔ψ, ρ
rule_hw(seq(X, Y)):-
    member(iff(E1, E2), Y),
    delete(Y, iff(E1, E2), Y_NEW),
    rule_hw(seq([E1|X], [E2|Y_NEW])),
    rule_hw(seq([E2|X], [E1|Y_NEW])),
    format('~w P6a\n', seq(X, Y)),
    !.

% P6b Rule
% If φ, ψ, λ, ρ⊢π and λ, ρ⊢π, φ, ψ,then λ, φ↔ψ,ρ⊢π
rule_hw(seq(X, Y)):-
    member(iff(E1, E2), X),
    delete(X, iff(E1, E2), X1),
    append([E1, E2], X1, X_NEW), rule_hw(seq(X_NEW, Y)),
    append([E1, E2], Y, Y_NEW), rule_hw(seq(X1, Y_NEW)),
    format('~w P6b\n', seq(X, Y)),
    !.

