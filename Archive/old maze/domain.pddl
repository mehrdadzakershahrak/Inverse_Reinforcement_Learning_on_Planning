(define (domain maze)
(:requirements :typing :action-costs)
(:types cell - object
)

(:predicates 
(at ?cell - cell)
(can_go ?cell - cell ?cell - cell)
)

(:functions 
    (length ?pointA - cell ?pointB - cell)
    (total-cost)
)

(:action goes
:parameters (?start - cell ?dest - cell) 
:precondition (and (at ?start) (can_go ?start ?dest)
              )
:effect (and (at ?dest) (not (at ?start)) (increase (total-cost) (length ?start ?dest))
		)
)

)
