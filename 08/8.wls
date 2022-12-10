#!/usr/bin/env wolframscript
(* ::Package:: *)

input = Map[FromDigits, Characters /@ StringSplit[$ScriptInputString, "\n"], {2}]


(* ::Text:: *)
(*A function that tells whether a point is visible anywhere from outside the forest matrix*)


VisibleQ[p_, {x_, y_}, matrix_] :=
    Block[{sx, dx, up, do},
        With[{row = matrix[[x, ;;]], col = matrix[[;;, y]]},
            {sx, dx} = TakeDrop[row, y];
            {up, do} = TakeDrop[col, x];
            AllTrue[Most @ sx, p > #&] || AllTrue[dx, p > #&] || AllTrue[
                Most @ up, p > #&] || AllTrue[do, p > #&]
        ]
    ]


(* ::Subsubsection:: *)
(*Part 1*)


p1 = Count[MapIndexed[VisibleQ[#1, #2, input]&, input,
     {2}], True, {2}]

Print["Total number of visible trees: " ~~ ToString @ p1]


(* ::Subsubsection:: *)
(*Part 2*)


(* ::Text:: *)
(*A function that, given a value x and a list, increments a counter until it reaches a value that is the same as or larger than x*)


counter[value_][list_] :=
    Catch[
        list === {} && Throw[0];
        Block[{total = 0},
            Scan[
                Which[
                    # < value,
                        ++total
                    ,
                    # > value || # == value,
                        Throw[++total]
                ]&
                ,
                list
            ];
            Throw[total]
        ]
    ]


pick[{x_, y_}, data_] :=
    Block[{row = data[[x, ;;]], col = data[[;;, y]], sx, dx, up, do},
        
        {sx, dx} = TakeDrop[row, y];
        {up, do} = TakeDrop[col, x];
        {data[[x, y]], {Most /* Reverse @ sx, dx, Most /* Reverse @ up,
             do}}
    ]


p2 = MaximalBy[Map[Map[counter[#[[1]]], #[[2]]]&, Flatten[MapIndexed[
    pick[#2, input]&, input, {2}], 1]], Apply[Times]] // Flatten /* Apply[
    Times];

Print["Highest scenic score: " ~~ ToString[p2]]


(* ::Text:: *)
(**)
