(define (problem p3) (:domain scavenger)
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
(has_fireExt)
(has_ladder)
(need_electric)
(fire)





)

(:goal (and
(exit elecDoor)
)
)
)
