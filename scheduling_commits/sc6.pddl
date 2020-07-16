(define (problem sc6) (:domain meeting_1)
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
(have_fifteen_minutes_for_dress j)
(have_twenty_minutes_for_meeting j)
(have_five_minutes_for_breakfast j)
(have_formal_meeting j)
(car_not_works j)
(meeting_available rNearWork)
(has_restaurant rNearWork)
)

(:goal (and
(meeting_happened j)
(breakfast_ready j)
(at work)
	)
)
)