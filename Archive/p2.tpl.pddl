(define (problem p2) (:domain scavenger)
(:objects
	start - roomZero
    basement - roomOne
    hallway - roomTwo
    elecDoor - roomThree
)

(:init
(can_go start basement)
(can_go basement hallway)
(can_go hallway elecDoor)
(at start)

; Situation variables
$HAS_LADDER
$FIRE
$NEED_ELECTRIC


)

(:goal (and
(exit elecDoor)
)
)
)
