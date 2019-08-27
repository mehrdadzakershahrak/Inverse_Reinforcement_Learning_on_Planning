(define (domain Meeting)
(:requirements :typing)
(:types rover waypoint store camera mode lander objective)

(:predicates (at ?x - rover ?y - waypoint)
             (at_lander ?x - lander ?y - waypoint)
             (can_traverse ?r - rover ?x - waypoint ?y - waypoint)
)


(:action make_instant_coffee
:parameters (?j-John ?t-five_minutes)
:precondition (and (not_have_coffee_beans ?j) (have_five_minutes_for_coffee ?j)
	    )
:effect (and (coffee_ready ?j) (not (have_five_minutes_for_coffee ?j))
		)
)

(:action eats_small_breakfast
:parameters (?j-John ?t-five_minutes)
:precondition (and (have_five_minutes_for_breakfast ?j)
	    )
:effect (and (breakfast_ready ?j) (not (have_five_minutes_for_breakfast ?j))
		)
)


(:action dress_formally
:parameters (?j-John ?t-fifteen_minutes)
:precondition (and (have_formall_meeting ?j) (have_fifteen_minutes_for_dress ?j)
	    )
:effect (and (dressed_for_formal-meeting ?j) (not (have_fifteen_minutes_for_dress ?j))
		)
)


(:action packs_lunch
:parameters (?j-John ?t-five_minutes)
:precondition (and (not_enough_lunch_time ?j) (have_five_minutes_for_lunch ?j)
	    )
:effect (and (lunch_packed ?j) (not (have_five_minutes_for_packlunch ?j))
		)
)

(:action goes_with_taxi_home_restaurant
:parameters (?j-John ?t-twentyfive_minutes ?h-Home ?r-Restaurant) 
:precondition (and (car_not_works ?j) (at ?h ?j) (have_twentyfive_minutes_for_drive ?j)
	    )
:effect (and (not (have_twentyfive_minutes_for_drive ?j)) (not (at ?h ?j)) (at ?r ?j)
		)
)

(:action goes_with_taxi_restaurant_work
:parameters (?j-John ?t-twentyfive_minutes ?w-Work ?r-Restaurant) 
:precondition (and (car_not_works ?j) (at ?h ?j) (have_twentyfive_minutes_for_drive ?j)
	    )
:effect (and (not (have_twentyfive_minutes_for_drive ?j)) (not (at ?h ?j)) (at ?w ?j)
		)
)

(:action goes_with_bus
:parameters (?j-John ?t-thirtyfive_minutes ?h-Home ?w-work) 
:precondition (and (car_not_works ?j) (at ?h ?j) (have_thirtyfive_minutes_for_drive ?j)
	    )
:effect (and (not (have_thirtyfive_minutes_for_drive)) (not (at ?h ?j)) (at ?w ?j)
		)
)

(:action goes_to_mechanic
:parameters (?j-John ?t-fifteen_minutes ?h-Home ?m-Mechanic ?c-Car) 
:precondition (and (car_needs_maintenance ?j) (at ?h ?j) (have_fifteen_minutes_for_drive ?j)
	    )
:effect (and (not (have_fifteen_minutes_for_drive)) (not (at ?h ?j)) (at ?m ?j) (at ?c ?m)
		)
)

(:action goes_with_taxi_mechanic_work
:parameters (?j-John ?t-ten_minutes ?w-Work ?m-Mechanic ?c-Car) 
:precondition (and (at ?c ?m) (at ?m ?j) (have_twentyfive_minutes_for_drive ?j)
	    )
:effect (and (not (have_ten_minutes_for_drive ?j)) (not (at ?m ?j)) (at ?w ?j)
		)
)

(:action has_formal_meeting
:parameters (?j-John ?t-twenty_minutes) 
:precondition (and (have_twenty_minutes_for_meeting ?j) (dressed_for_formal-meeting ?j)
	    )
:effect (and (meeting_happened ?j) (not (have_twenty_minutes_for_meeting ?j))
		)
)

(:action has_meeting
:parameters (?j-John ?t-twenty_minutes)
:precondition (and (have_twenty_minutes_for_meeting ?j)
	    )
:effect (and (meeting_happened ?j) (not (have_twenty_minutes_for_meeting ?j))
		)
)

(:action has_remote_meeting
:parameters (?j-John ?t-twenty_minutes ?h-Home)
:precondition (and (have_twenty_minutes_for_meeting ?j) (at ?h ?j)
	    )
:effect (and (meeting_happened ?j) (not (have_twenty_minutes_for_meeting ?j))
		)
)

(:action walk
:parameters (?j-John ?t-five_minutes ?h-Home ?r-Restaurant) 
:precondition (and (car_not_works ?j) (at ?h ?j) (have_twentyfive_minutes_for_drive)
	    )
:effect (and (dressed_for_formal_meeting ?j) (not (have_twentyfive_minutes_for_drive ?j)) (not (at ?h ?j)) (at ?r ?j)
		)
)

)
