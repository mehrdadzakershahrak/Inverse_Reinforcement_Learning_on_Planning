(define (problem sc5) (:domain meeting_1)
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
(have_five_minutes_for_lunch j)
(not_enough_lunch_time j)
(have_fifteen_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(have_formal_meeting j)
(car_not_works j)
(meeting_available work)
)

(:goal (and
(coffee_ready j)
(meeting_happened j)
(lunch_packed j)
(at work)
	)
)
)