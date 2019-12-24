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

(fire)
(has_electricity)


)

(:goal (and
(exit elecDoor)
)
)
)
