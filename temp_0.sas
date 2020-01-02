begin_version
3
end_version
begin_metric
0
end_metric
14
begin_variable
var0
-1
2
Atom glass_broken()
NegatedAtom glass_broken()
end_variable
begin_variable
var1
-1
2
Atom handle_released()
NegatedAtom handle_released()
end_variable
begin_variable
var2
-1
2
Atom has_accesskey()
NegatedAtom has_accesskey()
end_variable
begin_variable
var3
-1
2
Atom has_fireext()
NegatedAtom has_fireext()
end_variable
begin_variable
var4
-1
2
Atom has_ladder()
NegatedAtom has_ladder()
end_variable
begin_variable
var5
-1
2
Atom basement_open()
NegatedAtom basement_open()
end_variable
begin_variable
var6
-1
2
Atom no_fire()
NegatedAtom no_fire()
end_variable
begin_variable
var7
-1
4
Atom at(basement)
Atom at(elecdoor)
Atom at(hallway)
Atom at(start)
end_variable
begin_variable
var8
-1
2
Atom hallway_open()
NegatedAtom hallway_open()
end_variable
begin_variable
var9
-1
2
Atom has_flashlight()
NegatedAtom has_flashlight()
end_variable
begin_variable
var10
-1
2
Atom has_electricity()
NegatedAtom has_electricity()
end_variable
begin_variable
var11
-1
2
Atom activate_elecdoor()
NegatedAtom activate_elecdoor()
end_variable
begin_variable
var12
-1
2
Atom electricdoor_open()
NegatedAtom electricdoor_open()
end_variable
begin_variable
var13
-1
2
Atom exit(elecdoor)
NegatedAtom exit(elecdoor)
end_variable
0
begin_state
1
1
1
1
1
1
1
3
1
1
1
1
1
1
end_state
begin_goal
1
13 0
end_goal
16
begin_operator
break_with_stone hallway
1
7 2
1
0 0 -1 0
1
end_operator
begin_operator
get_accesskey basement
1
7 0
1
0 2 -1 0
1
end_operator
begin_operator
get_fireext hallway
2
7 2
0 0
1
0 3 -1 0
1
end_operator
begin_operator
get_flashlight elecdoor
1
7 1
1
0 9 -1 0
1
end_operator
begin_operator
get_ladder hallway
2
7 2
1 0
1
0 4 -1 0
1
end_operator
begin_operator
get_out elecdoor
2
7 1
12 0
1
0 13 -1 0
1
end_operator
begin_operator
goes_one_two basement hallway
1
5 0
1
0 7 0 2
1
end_operator
begin_operator
goes_two_three hallway elecdoor
1
8 0
1
0 7 2 1
1
end_operator
begin_operator
goes_zero_one start basement
0
1
0 7 3 0
1
end_operator
begin_operator
open_basement basement
2
7 0
2 0
1
0 5 -1 0
1
end_operator
begin_operator
open_roomtwo_window hallway
3
7 2
4 0
6 0
1
0 8 -1 0
1
end_operator
begin_operator
putout_fire hallway
2
7 2
3 0
1
0 6 -1 0
1
end_operator
begin_operator
release_emergency_handle hallway
1
7 2
1
0 1 -1 0
1
end_operator
begin_operator
run_generator elecdoor
2
7 1
9 0
1
0 10 -1 0
1
end_operator
begin_operator
use_electric_door elecdoor
3
11 0
7 1
10 0
1
0 12 -1 0
1
end_operator
begin_operator
use_key elecdoor
1
7 1
1
0 11 -1 0
1
end_operator
0
