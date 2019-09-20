(define (problem sc8) (:domain meeting_1)
(:objects
	home mechanic rNearWork rNearHome work - loc
    need_five_minutes need_twentyfive_minutes - time
    j - John

)

(:init
(can-move home rNearHome need_five_minutes)
(can-move rNearHome home need_five_minutes)
(can-move home rNearWork need_twentyfive_minutes)
(can-move rNearWork work need_five_minutes)
(at home)
(have_ten_minutes_for_coffee j)
(not_have_coffee_beans j)
(have_fifteen_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(have_five_minutes_for_breakfast j)
(have_formal_meeting j)
(car_not_works j)
(meeting_available home)
(has_restaurant rNearHome)
(has_coffee rNearHome)
)

(:goal (and
(meeting_happened j)
(breakfast_ready j)
(coffee_ready j)
(at work)
	)
)
)