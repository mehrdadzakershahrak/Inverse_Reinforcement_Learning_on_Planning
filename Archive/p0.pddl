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
(has_electricity)
(fire)

)

(:goal (and
(exit elecDoor)
)
)
)
