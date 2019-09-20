(define (problem sc9) (:domain meeting_1)
(:objects
	home mechanic rNearWork rNearHome work - loc
    need_five_minutes need_twentyfive_minutes - time
    j - John

)

(:init
(can-move home rNearHome need_five_minutes)
(can-move rNearHome work need_twentyfive_minutes)
(at home)
(not_enough_lunch_time j)
(have_five_minutes_for_lunch j)
(have_ten_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(have_five_minutes_for_breakfast j)
(have_normal_meeting j)
(car_not_works j)
(meeting_available work)
(has_restaurant rNearHome)
)

(:goal (and
(meeting_happened j)
(breakfast_ready j)
(lunch_packed j)
(at work)
	)
)
)