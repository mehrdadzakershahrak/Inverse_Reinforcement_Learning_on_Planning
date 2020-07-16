(define (problem sc1) (:domain meeting_1)
(:objects
	home mechanic rNearWork rNearHome work - loc
    need_five_minutes need_twentyfive_minutes - time
    j - John

)

(:init
(can-move rNearWork work need_five_minutes)
(can-move home rNearWork need_twentyfive_minutes)
(at home)
(not_have_coffee_beans j)
(have_five_minutes_for_coffee j)
(have_five_minutes_for_breakfast j)
(have_five_minutes_for_lunch j)
;(not_enough_lunch_time j)
(have_fifteen_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(have_formal_meeting j)
(car_not_works j)
(meeting_available rNearWork)
(has_restaurant rNearWork)
(food_at_home j)
)

(:goal (and
(coffee_ready j)
(breakfast_ready j)
(dressed_for_formal_meeting j)
(meeting_happened j)
;(lunch_packed j)
(at work)
	)
)
)
