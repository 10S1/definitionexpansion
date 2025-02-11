# A CNL for Maths (in the sTeX world)

(ongoing research work)

Goal: Have a "reasonably semantic" CNL for mathematics that allows us to do textual transformations, e.g. to convert a general definition into a more specific one.

## Design decisions

* **Linguistic variants**: While they do not carry semantic information, we may want to maintain them throughout the transformation process. That requires them to be stored in the AST even though they are not semantically relevant. To balance this, the variants are stored as a suffix to the rules. The unsuffixed variants are the "canonical" ones. Variants may not exist in all languages. In this case, the canonical form should used.
* **Ambiguity of sentence function**: The sentence "x is even iff x is divisible by 2" can be read as a definition or as a theorem. In the grammar, we would get two different readings. If "even" is marked as definiens, we can use a filtering step after parsing to discard the reading as a theorem. Note that the reading as a definition is one of the variants linguistic variants for defining a property (e.g. "x is called even iff ..." is another variant, which wouldn't have the same ambiguity).

