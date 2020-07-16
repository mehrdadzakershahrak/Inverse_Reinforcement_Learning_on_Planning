(define (problem sc3) (:domain meeting_1)
(:objects
	home mechanic rNearWork rNearHome work - loc
    need_five_minutes need_ten_minutes need_fifteen_minutes - time
    j - John

)

(:init
(can-move home mechanic need_fifteen_minutes)
(can-move mechanic work need_ten_minutes)
(can-move work rNearWork need_five_minutes)
(can-move rNearWork work need_five_minutes)
(at home)
(not_have_coffee_beans j)
(have_five_minutes_for_coffee j)
(have_five_minutes_for_breakfast j)
(have_five_minutes_for_lunch j)
(not_enough_lunch_time j)
(have_ten_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(car_not_works j)
(has_restaurant rNearWork)
(meeting_available work)
)

(:goal (and
(breakfast_ready j)
(dressed_for_normal_meeting j)
(meeting_happened j)
(lunch_packed j)
(at work)
	)
)
)