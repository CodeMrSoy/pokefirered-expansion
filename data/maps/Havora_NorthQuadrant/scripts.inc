Havora_NorthQuadrant_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Havora_NorthQuadrant_PuzzleLoad
	map_script MAP_SCRIPT_ON_RESUME, Havora_NorthQuadrant_PuzzleResume
	.byte 0

Havora_NorthQuadrant_Coast::
	msgbox Havora_NorthQuadrant_Coast_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Coast_Text::
	.string "The DAY CARE is east of the square,\nright above the coastal cliffs.$"

Havora_NorthQuadrant_Services::
	msgbox Havora_NorthQuadrant_Services_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Services_Text::
	.string "Welcome to the northern square!\nThe CENTER and MART are right here.$"

Havora_NorthQuadrant_North::
	msgbox Havora_NorthQuadrant_North_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_North_Text::
	.string "The northern walk follows the cliffs.\nYou can see the whole port from there.$"

Havora_NorthQuadrant_Patient::
	msgbox Havora_NorthQuadrant_Patient_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Patient_Text::
	.string "My partner is feeling better.\nWe are off to the market now.$"

Havora_NorthQuadrant_Shopper::
	msgbox Havora_NorthQuadrant_Shopper_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Shopper_Text::
	.string "Supplies for the mountain trail.\nI always stop here before a climb.$"

Havora_NorthQuadrant_Tailor::
	msgbox Havora_NorthQuadrant_Tailor_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Tailor_Text::
	.string "Strong cloth and a good coat\nwill see you through a sea wind.$"

Havora_NorthQuadrant_Stargazer::
	msgbox Havora_NorthQuadrant_Stargazer_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Stargazer_Text::
	.string "One old impact rests by the lookout.\nThe great craters are farther uphill.$"

Havora_NorthQuadrant_QuayWalker::
	msgbox Havora_NorthQuadrant_QuayWalker_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_QuayWalker_Text::
	.string "These stairs wind down to the quay.\nI like the quieter way home.$"

Havora_NorthQuadrant_Hiker::
	msgbox Havora_NorthQuadrant_Hiker_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_Hiker_Text::
	.string "The mountain can wait until morning.\nTonight I will stay at the lodge.$"

Havora_NorthQuadrant_GardenBird::
	msgbox Havora_NorthQuadrant_GardenBird_Text, MSGBOX_NPC
	end

Havora_NorthQuadrant_GardenBird_Text::
	.string "The POKéMON rustles in the garden.$"

Havora_NorthQuadrant_PuzzleLoad::
	special HavoraPuzzle_OnLoad
	end

Havora_NorthQuadrant_PuzzleResume::
	special HavoraPuzzle_OnResume
	end

Havora_NorthQuadrant_PuzzleNotice::
	lockall
	msgbox Havora_NorthQuadrant_PuzzleRules, MSGBOX_DEFAULT
	goto Havora_NorthQuadrant_PuzzleAskReset

Havora_NorthQuadrant_PuzzleReset::
	lockall
Havora_NorthQuadrant_PuzzleAskReset::
	msgbox Havora_NorthQuadrant_ResetPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Havora_NorthQuadrant_PuzzleCancel
	closemessage
	special HavoraPuzzle_ResetState
	warp MAP_HAVORA_NORTH_QUADRANT, 20, 27
	waitstate
	releaseall
	end

Havora_NorthQuadrant_PuzzleCancel::
	closemessage
	releaseall
	end

Havora_NorthQuadrant_GateA::
	lockall
	msgbox Havora_NorthQuadrant_GateAText, MSGBOX_DEFAULT
	goto Havora_NorthQuadrant_PuzzleAskReset

Havora_NorthQuadrant_GateB::
	lockall
	msgbox Havora_NorthQuadrant_GateBText, MSGBOX_DEFAULT
	goto Havora_NorthQuadrant_PuzzleAskReset

Havora_NorthQuadrant_GateZ::
	lockall
	msgbox Havora_NorthQuadrant_GateZText, MSGBOX_DEFAULT
	goto Havora_NorthQuadrant_PuzzleAskReset

Havora_NorthQuadrant_PlateA::
	msgbox Havora_NorthQuadrant_PlateAText, MSGBOX_SIGN
	end

Havora_NorthQuadrant_PlateB::
	msgbox Havora_NorthQuadrant_PlateBText, MSGBOX_SIGN
	end

Havora_NorthQuadrant_PlateC::
	msgbox Havora_NorthQuadrant_PlateCText, MSGBOX_SIGN
	end

Havora_NorthQuadrant_PlateD::
	msgbox Havora_NorthQuadrant_PlateDText, MSGBOX_SIGN
	end

Havora_NorthQuadrant_PuzzleRules::
	.string "COUNTERWEIGHT GROVE\nSix stones. Three shafts.\p"
	.string "Match the colored plate marks\nto the gate marks.\p"
	.string "The final gate needs all shafts\nfilled and plates B, C, D held.\p"
	.string "L + R + SELECT opens reset\nfrom anywhere in the grove.$"

Havora_NorthQuadrant_ResetPrompt::
	.string "Reset the grove and return\nto its entrance?$"

Havora_NorthQuadrant_GateAText::
	.string "RED GATE\nWeight the red button.$"

Havora_NorthQuadrant_GateBText::
	.string "BLUE GATE\nWeight the blue button.$"

Havora_NorthQuadrant_GateZText::
	.string "FOREST GATE\nFill all three shafts and keep\lplates B, C and D weighted.$"

Havora_NorthQuadrant_PlateAText::
	.string "RED BUTTON (A)\nIts weight raises GATE A.$"

Havora_NorthQuadrant_PlateBText::
	.string "BLUE BUTTON (B)\nIts weight raises GATE B and\lhelps unlock the FOREST GATE.$"

Havora_NorthQuadrant_PlateCText::
	.string "YELLOW BUTTON (C)\nA seal for the FOREST GATE.$"

Havora_NorthQuadrant_PlateDText::
	.string "GREEN BUTTON (D)\nA seal for the FOREST GATE.$"
