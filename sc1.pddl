(define (problem scenario1) (:domain meeting_1)
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
)

(:goal (and
(coffee_ready  )
(have_five_minutes_for_breakfast  )
(have_five_minutes_for_coffee  )
(breakfast_ready  )
(can-move ?start-loc ?end-loc ?t-time)
(have_formall_meeting j)
(dressed_for_formal-meeting  )
(have_fifteen_minutes_for_dress  )
(have_five_minutes_for_lunch  )
(not_enough_lunch_time  )
(lunch_packed  )
(have_five_minutes_for_packlunch  )
(car_not_works  )
(at ?start - loc)
	    )
)
)