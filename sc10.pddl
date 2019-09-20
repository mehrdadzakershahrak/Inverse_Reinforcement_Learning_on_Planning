(define (problem sc10) (:domain meeting_1)
(:objects
	home mechanic rNearWork rNearHome work - loc
    need_thirtyfive_minutes - time
    j - John

)

(:init
(can-move home work need_thirtyfive_minutes)
(at home)
(have_five_minutes_for_coffee j)
(not_have_coffee_beans j)
(have_fifteen_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(have_five_minutes_for_breakfast j)
(have_formal_meeting j)
(car_not_works j)
(meeting_available work)
(food_at_home j)
)

(:goal (and
(meeting_happened j)
(breakfast_ready j)
(coffee_ready j)
(at work)
	)
)
)