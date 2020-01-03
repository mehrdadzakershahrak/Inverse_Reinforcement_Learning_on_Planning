(define (problem p1) (:domain scavenger)
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
$(fire)
$(lock_open)
$(need_electric)


)

(:goal (and
(exit elecDoor)
)
)
)
