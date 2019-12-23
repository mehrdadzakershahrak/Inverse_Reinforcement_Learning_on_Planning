begin_version
3
end_version
begin_metric
0
end_metric
6
begin_variable
var0
-1
2
Atom basement_open()
NegatedAtom basement_open()
end_variable
begin_variable
var1
-1
2
Atom lock_open()
NegatedAtom lock_open()
end_variable
begin_variable
var2
-1
4
Atom at(basement)
Atom at(elecdoor)
Atom at(hallway)
Atom at(start)
end_variable
begin_variable
var3
-1
2
Atom hallway_open()
NegatedAtom hallway_open()
end_variable
begin_variable
var4
-1
2
Atom electricdoor_open()
NegatedAtom electricdoor_open()
end_variable
begin_variable
var5
-1
2
Atom exit(elecdoor)
NegatedAtom exit(elecdoor)
end_variable
0
begin_state
1
1
3
1
1
1
end_state
begin_goal
1
5 0
end_goal
9
begin_operator
get_out elecdoor
2
2 1
4 0
1
0 5 -1 0
1
end_operator
begin_operator
goes_one_two basement hallway
1
0 0
1
0 2 0 2
1
end_operator
begin_operator
goes_two_three hallway elecdoor
1
3 0
1
0 2 2 1
1
end_operator
begin_operator
goes_zero_one start basement
1
1 0
1
0 2 3 0
1
end_operator
begin_operator
open_basement basement
1
2 0
1
0 0 -1 0
1
end_operator
begin_operator
open_roomtwo_door hallway
1
2 2
1
0 3 -1 0
1
end_operator
begin_operator
open_roomtwo_window hallway
1
2 2
1
0 3 -1 0
1
end_operator
begin_operator
pick_lock start
1
2 3
1
0 1 -1 0
1
end_operator
begin_operator
use_electric_door elecdoor
1
2 1
1
0 4 -1 0
1
end_operator
0
