(define (domain meeting_1)
(:requirements :typing)
(:types John loc time)

(:predicates (coffee_ready ?j - John)
(have_five_minutes_for_breakfast ?j - John)
(have_five_minutes_for_coffee ?j - John)
(breakfast_ready ?j - John)
(can-move ?start - loc ?end - loc ?t - time)
(have_formal_meeting ?j - John)
(dressed_for_formal_meeting ?j - John)
(have_fifteen_minutes_for_dress ?j - John)
(have_five_minutes_for_lunch ?j - John)
(not_enough_lunch_time ?j - John)
(lunch_packed ?j - John)
(have_five_minutes_for_packlunch ?j - John)
(car_not_works ?j - John)
(at ?start - loc)
(not_have_coffee_beans ?j - John)
(have_fifteen_minutes_for_coffee ?j - John)
(have_ten_minutes_for_coffee ?j - John)
(have_twenty_minutes_for_breakfast ?j - John)
(have_ten_minutes_for_breakfast ?j - John)
(have_ten_minutes_for_dress ?j - John)
(have_twenty_minutes_for_meeting ?j - John)
(meeting_happened ?j - John)
(dressed_for_normal_meeting ?j - John)
(has_restaurant ?r - loc)
(meeting_available ?r - loc)
(food_at_home ?j - John)
(has_coffee ?r - loc)
)

(:action make_instant_coffee
:parameters (?j - John )
:precondition (and (have_five_minutes_for_coffee ?j) (not_have_coffee_beans ?j)
	    )
:effect (and (coffee_ready ?j) (not (have_five_minutes_for_coffee ?j))
		)
)

(:action coffee_near_home
:parameters (?j - John ?r - loc)
:precondition (and (have_ten_minutes_for_coffee ?j) (not_have_coffee_beans ?j) (has_coffee ?r) (at ?r)
	    )
:effect (and (coffee_ready ?j) (not (have_ten_minutes_for_coffee ?j))
		)
)

(:action drinks_coffee
:parameters (?j - John ?r - loc)
:precondition (and (have_five_minutes_for_coffee ?j) (has_coffee ?r) (at ?r)
	    )
:effect (and (coffee_ready ?j) (not (have_five_minutes_for_coffee ?j))
		)
)

(:action brew_coffee
:parameters (?j - John )
:precondition (and (have_fifteen_minutes_for_coffee ?j)
	    )
:effect (and (coffee_ready ?j) (not (have_fifteen_minutes_for_coffee ?j))
		)
)

(:action eats_small_breakfast
:parameters (?j - John )
:precondition (and (have_five_minutes_for_breakfast ?j) (food_at_home ?j)
	    )
:effect (and (breakfast_ready ?j) (not (have_five_minutes_for_breakfast ?j))
		)
)

(:action eats_breakfast_coffee
:parameters (?j - John ?r - loc)
:precondition (and (have_ten_minutes_for_breakfast ?j) (has_restaurant ?r) (at ?r)
	    )
:effect (and (breakfast_ready ?j) (coffee_ready ?j) (not (have_ten_minutes_for_breakfast ?j)) 
		)
)

(:action eats_breakfast
:parameters (?j - John ?r - loc)
:precondition (and (have_five_minutes_for_breakfast ?j) (has_restaurant ?r) (at ?r)
	    )
:effect (and (breakfast_ready ?j) (not (have_ten_minutes_for_breakfast ?j)) 
		)
)

(:action eats_large_breakfast
:parameters (?j - John )
:precondition (and (have_twenty_minutes_for_breakfast ?j) (food_at_home ?j)
	    )
:effect (and (breakfast_ready ?j) (not (have_twenty_minutes_for_breakfast ?j))
		)
)

(:action dress_formally
:parameters (?j - John )
:precondition (and (have_fifteen_minutes_for_dress ?j) (have_formal_meeting ?j)
	    )
:effect (and (dressed_for_formal_meeting ?j) (not (have_fifteen_minutes_for_dress ?j))
		)
)

(:action dress
:parameters (?j - John )
:precondition (and (have_ten_minutes_for_dress ?j)
	    )
:effect (and (not (have_ten_minutes_for_dress ?j)) (dressed_for_normal_meeting ?j)
		)
)

(:action packs_lunch
:parameters (?j - John )
:precondition (and (have_five_minutes_for_lunch ?j) (not_enough_lunch_time ?j)
	    )
:effect (and (lunch_packed ?j) (not (have_five_minutes_for_packlunch ?j))
		)
)

(:action goes
:parameters (?j - John ?t - time ?start - loc ?dest - loc)
:precondition (and (car_not_works ?j) (at ?start) (can-move ?start ?dest ?t)
	    )
:effect (and (not (at ?start)) (at ?dest)
		)
)

(:action has_formal_meeting
:parameters (?j - John ?r - loc )
:precondition (and (have_twenty_minutes_for_meeting ?j) (dressed_for_formal_meeting ?j) (meeting_available ?r) (at ?r)
	    )
:effect (and (meeting_happened ?j) (not (have_twenty_minutes_for_meeting ?j))
		)
)

(:action has_meeting
:parameters (?j - John ?r - loc)
:precondition (and (have_twenty_minutes_for_meeting ?j) (dressed_for_normal_meeting ?j) (meeting_available ?r) (at ?r)
	    )
:effect (and (meeting_happened ?j) (not (have_twenty_minutes_for_meeting ?j))
		)
)

)
