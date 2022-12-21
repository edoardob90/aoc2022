#!/usr/bin/env wolframscript
(* ::Package:: *)

input = StringSplit[$ScriptInputString, "\n"];

(*
Read the input as a list of symbolic rules
*)

rules = Flatten @ StringCases[input, id : (WordCharacter..) ~~ ": " ~~ op__ :> ToExpression /@ (id -> op)];


(* ::Subsubsection:: *)
(*Part 1*)


(*
Define a function that extracts the known rules (those that assign a symbol to a number)
and applies them on the remaining rules
*) 


replaceRules[rules_] :=
    With[{r = Cases[rules, HoldPattern[_ -> _Integer]]},
        Complement[rules, r] /. r
    ]


(*
We repeatedly apply the function to our input rules until the list contains only 1 rule
That's going to be the "root" rule
*)


part1 = root /. NestWhile[replaceRules, rules, Length @ # > 1&];


Print["The 'root' monkey will yell is "~~ToString@part1]


(* ::Subsubsection:: *)
(*Part 2*)


(*
We must replace the + in root with a ==
and then the number in "humn -> 5" with an unknown symbol to be determined.

In practice, we replace Plus with Equal in the root rule, and we delete the
"humn -> 5" rule, replacing directly every occurence of "humn" with "X"
*)


updateRules[rules_] :=
    With[{
        root = FirstPosition[rules, root -> _],
        me = FirstPosition[rules, humn -> _]
    },
        Delete[ReplacePart[rules, root -> First @ rules[[root]] /. Plus
             -> Equal], me] /. humn -> X
    ]


(*
We run again the "replaceRules" function until the original list of rules no longer changes
*)


result = FixedPoint[replaceRules, updateRules[rules]];


(*
Now, we need to transform the result in a list of equations.
First, we remove the "root" rule which is just an equality test.
Second, we convert all the remaining rules into equalities
*)


eqns = result /. HoldPattern[root -> x_ == y_] :> x -> y /. Rule -> Equal


(*
The answer is the solution to the resulting system of equations
*)


unks = Cases[eqns, _Symbol, All]; (* These are all our unknowns *)

part2 = X /. Solve[eqns, unks] // First;

Print["Our number that will pass 'root' equality test is " ~~ ToString @ part2]
