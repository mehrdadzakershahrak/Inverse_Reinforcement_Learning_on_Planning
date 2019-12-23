(define (problem p1) (:domain scavenger)
(:objects
	basement - roomOne
    hallway - roomTwo
    elecDoor - roomThree
)

(:init
(opens basement hallway)
(opens hallway elecDoor)
(at basement)

(basement_open basement)
(hallway_open hallway)
(electricDoor_open elecDoor)


)

(:goal (and
(exit elecDoor)
)
)
)