(define (problem p1) (:domain maze)
(:objects
start goal A E C F B D H - cell
)

(:init

(= (length start E) 2)
(= (length start A) 1)
(= (length start C) 6)
(= (length start F) 8)
(= (length start B) 12)
(= (length start D) 19)
(= (length start H) 21)
(= (length E goal) 3)
(= (length A goal) 6)
(= (length F goal) 7)
(= (length C goal) 5)
(= (length B goal) 7)
(= (length D goal) 2)
(= (length H goal) 4)



;(can_go start E)
;(can_go start A)
(can_go start C)
(can_go start F) 
(can_go start B)
(can_go start D)
(can_go start H) 
(can_go E goal)
(can_go A goal)
(can_go F goal)
(can_go C goal)
(can_go B goal)
(can_go D goal)
(can_go H goal)


(at start)
)

(:goal (at goal))

(:metric minimize (total-cost))
)
