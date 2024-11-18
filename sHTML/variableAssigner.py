def get_assignedVariables():
    return None

"""
# Gleichwertige Strukturen
admissible heuristic
heuristic (h for Π) is admissible

X is non-empty
A set Y is non-empty 

# Nicht gleichwertig
ϕ has a countable model 
A set X is countable


Statement:    "A* with an admissible heuristic is optimal."
Definition:      "We say that a heuristic h for Π is admissible iff h(s) < s* for all s ∈ S."
Output:          "A* with an heuristic h such that h(s) < s* for all s ∈ S, is optimal."
IE-Output:      "A* with an admissible heuristic h (i.e. h(s) < s* for all s ∈ S) is optimal."


2. countable:
Statement:     "ϕ has a countable model or ϕ is inconsistent."
Definition:      "A set X is countable iff there exists an injective function f: X → N."
Output:          "ϕ has a model M such that there exists an injective function f : M → N or ϕ is inconsistent."
IE-Output:      "ϕ has a countable (i.e. there exists an injective function f: M → N) model M or ϕ is inconsistent."


3. non-empty:
Statement:    "Assume that X is non-empty."
Definition:      "A set Y is non-empty iff Y has no elements."
Output:          "Assume that X has no elements."
IE-Output:      "Assume that X is non-empty (i.e. X has no elements)."


4. consistent:
Statement:    "If ZFC is consistent, then ZFC has a countable model."
Definition:      "A theory T is conistent iff it is wrong that T ⊢ ⊥."
Output:          "Iff it is wrong that ZFC ⊢ ⊥, then ZFC has a countable model."
IE-Output:      "If ZFC is consistent (i.e. it is wrong that ZFC ⊢ ⊥), then ZFC has a countable model."


5. even:
Statement:    "Choose an even divisor of n."
Definition:      "n is even if n is divisible by 2."
Output:          "Choose a divisor d such that d is divisible by 2."
IE-Output:      "Choose an even (i.e. d is divisible by 2) divisor d of n."


6. monoid:
Statement:    "A structure R=(\bset,+,0,⋅,1,−) is called a ring, if \mathstruct{\bset, +, 0, -} is an Abelian group (called the additive structure), \mathstruct{\bset,⋅,1} is a monoid (called the multiplicative structure), and \mathstruct\{\bset,+,⋅} is a ringoid."
Definition:      "A unital semigroup is called a monoid."
Output:          "A structure R=(\bset,+,0,⋅,1,−) is called a ring, if \mathstruct{\bset, +, 0, -} is an Abelian group (called the additive structure), \mathstruct{\bset,⋅,1} is a unital semigroup (called the multiplicative structure), and \mathstruct\{\bset,+,⋅} is a ringoid."
IE-Output:      "A structure R=(\bset,+,0,⋅,1,−) is called a ring, if \mathstruct{\bset, +, 0, -} is an Abelian group (called the additive structure), \mathstruct{\bset,⋅,1} is a monoid (i.e. a unital semigroup) (called the multiplicative structure), and \mathstruct\{\bset,+,⋅} is a ringoid."
"""