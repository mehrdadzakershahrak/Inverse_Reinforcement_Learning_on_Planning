(define (problem scenario1) (:domain Meeting)
(:objects
	home mechanic rNearWork rNearHome work - loc
    need_five_minutes need_twentyfive_minutes need_thirtyfive_minutes need_ten_minutes need_fifteen_minutes - time
    j - John

)

(:init
(can-move home mechanic need_fifteen_minutes)
(can-move home rNearHome need_five_minutes)
(can-move rNearWork work need_five_minutes)
(can-move rNearHome work need_twentyfive_minutes)
(can-move home rNearWork need_twentyfive_minutes)
(can-move home work need_thirtyfive_minutes)
(can-move mechanic work need_ten_minutes)
(at home)
(not_have_coffee_beans j)
(have_five_minutes_for_coffee j)
(have_five_minutes_for_breakfast j)
(have_five_minutes_for_lunch j)
(not_enough_lunch_time j)
(have_fifteen_minutes_for_dress j)
(have_formall_meeting j)
(car_not_works j)
)

(:goal (and
(dressed_for_formal-meeting j)
(lunch_packed j)
(at work)
	)
)
)
