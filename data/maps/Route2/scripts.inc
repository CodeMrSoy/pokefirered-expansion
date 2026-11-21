Route2_MapScripts::
	.byte 0

Route2_EventScript_RouteSign::
	msgbox Route2_Text_RouteSign, MSGBOX_SIGN
	end

Route2_EventScript_DiglettsCaveSign::
	msgbox Route2_Text_DiglettsCave, MSGBOX_SIGN
	end

Route2_EventScript_PewterTrainer::
	lock
	faceplayer
	living_world_aside LIVING_WORLD_SOCIETY_TRAINER
	goto_if_eq VAR_RESULT, TRUE, Route2_EventScript_PewterTrainerRelease
	msgbox Route2_Text_PewterTrainerPractice
Route2_EventScript_PewterTrainerRelease::
	release
	end

Route2_Text_PewterTrainerPractice::
	.string "I'm practicing near the rocks.\n"
	.string "I'll head back to Pewter soon.$"

Route2_EventScript_Volunteer::
	lock
	faceplayer
	msgbox Route2_Text_Volunteer
	living_world_aside LIVING_WORLD_SOCIETY_RESEARCHER
	release
	end

Route2_Text_Volunteer::
	.string "I'm taking notes for the Museum.$"
