QuantumHarbor_MapScripts::
	.byte 0

QuantumHarbor_Sailor::
	lock
	faceplayer
	msgbox QuantumHarbor_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, QuantumHarbor_Cancel
	setvar VAR_0x8004, SEAGALLOP_QUANTUM_PORT
	setvar VAR_0x8006, SEAGALLOP_VERMILION_CITY
	goto EventScript_SailToDest
QuantumHarbor_Cancel::
	release
	end

QuantumHarbor_Return::
	.string "Return to VERMILION CITY?$"

@ The in-progress harbor art uses a walkable water tile at the city exit.
@ Preserve the painted tilemap and make its existing warp respond to a step.
QuantumHarbor_ExitToCity::
	lockall
	warp MAP_QUANTUM_PORT_CITY, 1
	waitstate
	releaseall
	end
