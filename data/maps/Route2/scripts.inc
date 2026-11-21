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
	msgbox Route2_Text_PewterTrainerPractice
	release
	end

Route2_Text_PewterTrainerPractice::
	.string "I'm practicing near the rocks.\n"
	.string "I'll head back to Pewter soon.$"
