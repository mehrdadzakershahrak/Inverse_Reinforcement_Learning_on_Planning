(define (domain scavenger)
(:requirements :typing)
(:types loc - object
		roomZero roomOne roomTwo roomThree - loc
)

(:predicates (has_password)
(has_accesskey)
(basement_open)
(hallway_open)
(at ?room - loc)
(has_electricity)
(can_go ?start - loc ?dest - loc)
(electricDoor_open)
(glass_broken)
(has_flashlight)
(handle_released)
(lock_open)
(no_fire)
(door_unjammed)
(exit ?room - loc)
(has_fireExt)
(has_hammer)
(has_ladder)
(has_key)
(need_electric)
(activate_elecDoor)
(fire)
)

(:action pick_lock
:parameters (?room - roomZero) 
:precondition (and (at ?room) 
	    )
:effect (and (lock_open)
		)
)

(:action access_computer
:parameters (?room - roomOne) 
:precondition (and (at ?room)
	    )
:effect (and (has_password)
		)
)

(:action get_accesskey
:parameters (?room - roomOne) 
:precondition (and (at ?room) 
	    )
:effect (and (has_accesskey)
		)
)

(:action open_basement
:parameters (?room - roomOne) 
:precondition (and (at ?room) (has_password) 
	    )
:effect (and (basement_open)
		)
)

(:action break_with_stone
:parameters (?room - roomTwo) 
:precondition (and (at ?room)
	    )
:effect (and (glass_broken)
		)
)

(:action get_fireExt
:parameters (?room - roomTwo) 
:precondition (and (at ?room) (glass_broken) (fire)
	    )
:effect (and (has_fireExt) 
		)
)

(:action putout_fire
:parameters (?room - roomTwo) 
:precondition (and (at ?room) (has_fireExt)
	    )
:effect (and (no_fire) 
		)
)


(:action get_hammer
:parameters (?room - roomTwo) 
:precondition (and (at ?room) (glass_broken)
	    )
:effect (and (has_hammer)
		)
)

(:action release_emergency_handle
:parameters (?room - roomTwo) 
:precondition (and (at ?room)
	    )
:effect (and (handle_released)
		)
)

(:action get_Ladder
:parameters (?room - roomTwo) 
:precondition (and (at ?room) (handle_released) 
	    )
:effect (and (has_ladder)
		)
)

(:action open_roomTwo_window
:parameters (?room - roomTwo) 
:precondition (and (at ?room) (no_fire) (has_ladder) (has_hammer) 
	    )
:effect (and (hallway_open)
		)
)

(:action open_roomTwo_door
:parameters (?room - roomTwo) 
:precondition (and (at ?room) (door_unjammed) (no_fire)
	    )
:effect (and (hallway_open)
		)
)

(:action get_Key
:parameters (?room - roomOne) 
:precondition (and (at ?room)
	    )
:effect (and (has_Key)
		)
)

(:action use_Key
:parameters (?room - roomThree) 
:precondition (and (at ?room) (has_key)
	    )
:effect (and (activate_elecDoor)
		)
)

(:action get_FlashLight
:parameters (?room - roomThree) 
:precondition (and (at ?room)
	    )
:effect (and (has_flashlight)
		)
)

(:action run_Generator
:parameters (?room - roomThree) 
:precondition (and (at ?room) (has_flashlight) (need_electric)
	    )
:effect (and (has_electricity)
		)
)

(:action use_electric_door
:parameters (?room - roomThree) 
:precondition (and (at ?room) (has_electricity) (activate_elecDoor) 
	    )
:effect (and (electricDoor_open)
		)
)

(:action goes_zero_one
:parameters (?start - roomZero ?dest - roomOne) 
:precondition (and (at ?start) (can_go ?start ?dest) (lock_open)
	    )
:effect (and (at ?dest) (not (at ?start))
		)
)

(:action goes_one_two
:parameters (?start - roomOne ?dest - roomTwo) 
:precondition (and (at ?start) (can_go ?start ?dest) (basement_open)
	    )
:effect (and (at ?dest) (not (at ?start))
		)
)

(:action goes_two_three
:parameters (?start - roomTwo ?dest - roomThree) 
:precondition (and (at ?start) (can_go ?start ?dest) (hallway_open)
	    )
:effect (and (at ?dest) (not (at ?start))
		)
)

(:action get_out
:parameters (?three - roomThree) 
:precondition (and (at ?Three) (electricDoor_open)
	    )
:effect (and (exit ?three)
		)
)



)


