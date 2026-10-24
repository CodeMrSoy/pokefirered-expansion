HavoraNorthQuadrant_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, HavoraNorthQuadrant_PuzzleLoad
	map_script MAP_SCRIPT_ON_RESUME, HavoraNorthQuadrant_PuzzleResume
	.byte 0

HavoraNorthQuadrant_Coast::
	msgbox HavoraNorthQuadrant_Coast_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Coast_Text::
	.string "The DAY CARE is east of the square,\nright above the coastal cliffs.$"

HavoraNorthQuadrant_Services::
	msgbox HavoraNorthQuadrant_Services_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Services_Text::
	.string "Welcome to the northern square!\nThe CENTER and MART are right here.$"

HavoraNorthQuadrant_North::
	msgbox HavoraNorthQuadrant_North_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_North_Text::
	.string "The northern walk follows the cliffs.\nYou can see the whole port from there.$"

HavoraNorthQuadrant_Patient::
	msgbox HavoraNorthQuadrant_Patient_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Patient_Text::
	.string "My partner is feeling better.\nWe are off to the market now.$"

HavoraNorthQuadrant_Shopper::
	msgbox HavoraNorthQuadrant_Shopper_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Shopper_Text::
	.string "Supplies for the mountain trail.\nI always stop here before a climb.$"

HavoraNorthQuadrant_Tailor::
	msgbox HavoraNorthQuadrant_Tailor_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Tailor_Text::
	.string "Strong cloth and a good coat\nwill see you through a sea wind.$"

HavoraNorthQuadrant_Stargazer::
	msgbox HavoraNorthQuadrant_Stargazer_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Stargazer_Text::
	.string "One old impact rests by the lookout.\nThe great craters are farther uphill.$"

HavoraNorthQuadrant_QuayWalker::
	msgbox HavoraNorthQuadrant_QuayWalker_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_QuayWalker_Text::
	.string "These stairs wind down to the quay.\nI like the quieter way home.$"

HavoraNorthQuadrant_Hiker::
	msgbox HavoraNorthQuadrant_Hiker_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_Hiker_Text::
	.string "The mountain can wait until morning.\nTonight I will stay at the lodge.$"

HavoraNorthQuadrant_GardenBird::
	msgbox HavoraNorthQuadrant_GardenBird_Text, MSGBOX_NPC
	end

HavoraNorthQuadrant_GardenBird_Text::
	.string "The POKéMON rustles in the garden.$"

HavoraNorthQuadrant_PuzzleLoad::
	special HavoraPuzzle_OnLoad
	end

HavoraNorthQuadrant_PuzzleResume::
	special HavoraPuzzle_OnResume
	end

HavoraNorthQuadrant_PuzzleNotice::
	lockall
	msgbox HavoraNorthQuadrant_PuzzleRules, MSGBOX_DEFAULT
	goto HavoraNorthQuadrant_PuzzleAskReset

HavoraNorthQuadrant_PuzzleReset::
	lockall
HavoraNorthQuadrant_PuzzleAskReset::
	msgbox HavoraNorthQuadrant_ResetPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HavoraNorthQuadrant_PuzzleCancel
	closemessage
	special HavoraPuzzle_ResetState
	warp MAP_HAVORA_NORTH_QUADRANT, 20, 27
	waitstate
	releaseall
	end

HavoraNorthQuadrant_PuzzleCancel::
	closemessage
	releaseall
	end

HavoraNorthQuadrant_GateA::
	lockall
	msgbox HavoraNorthQuadrant_GateAText, MSGBOX_DEFAULT
	goto HavoraNorthQuadrant_PuzzleAskReset

HavoraNorthQuadrant_GateB::
	lockall
	msgbox HavoraNorthQuadrant_GateBText, MSGBOX_DEFAULT
	goto HavoraNorthQuadrant_PuzzleAskReset

HavoraNorthQuadrant_GateZ::
	lockall
	msgbox HavoraNorthQuadrant_GateZText, MSGBOX_DEFAULT
	goto HavoraNorthQuadrant_PuzzleAskReset

HavoraNorthQuadrant_PlateA::
	msgbox HavoraNorthQuadrant_PlateAText, MSGBOX_SIGN
	end

HavoraNorthQuadrant_PlateB::
	msgbox HavoraNorthQuadrant_PlateBText, MSGBOX_SIGN
	end

HavoraNorthQuadrant_PlateC::
	msgbox HavoraNorthQuadrant_PlateCText, MSGBOX_SIGN
	end

HavoraNorthQuadrant_PlateD::
	msgbox HavoraNorthQuadrant_PlateDText, MSGBOX_SIGN
	end

HavoraNorthQuadrant_PuzzleRules::
	.string "COUNTERWEIGHT GROVE\nSix stones. Three shafts.\p"
	.string "Weight the plates to lift gates.\nFilled shafts become paths.\p"
	.string "The final gate needs all shafts\nfilled and plates B, C, D held.\p"
	.string "L + R + SELECT opens reset\nfrom anywhere in the grove.$"

HavoraNorthQuadrant_ResetPrompt::
	.string "Reset the grove and return\nto its entrance?$"

HavoraNorthQuadrant_GateAText::
	.string "GATE A\nPlate A holds this gate open.$"

HavoraNorthQuadrant_GateBText::
	.string "GATE B\nPlate B holds this gate open.$"

HavoraNorthQuadrant_GateZText::
	.string "FOREST GATE\nFill all three shafts and keep\lplates B, C and D weighted.$"

HavoraNorthQuadrant_PlateAText::
	.string "PLATE A\nIts weight raises GATE A.$"

HavoraNorthQuadrant_PlateBText::
	.string "PLATE B\nIts weight raises GATE B and\lhelps unlock the FOREST GATE.$"

HavoraNorthQuadrant_PlateCText::
	.string "PLATE C\nA seal for the FOREST GATE.$"

HavoraNorthQuadrant_PlateDText::
	.string "PLATE D\nA seal for the FOREST GATE.$"
