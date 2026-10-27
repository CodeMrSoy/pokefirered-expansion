Havora_CliffHouse_5_MapScripts::
	.byte 0

Havora_CliffHouse_5_GymFan::
	msgbox Havora_CliffHouse_5_GymFan_Text, MSGBOX_NPC
	end
Havora_CliffHouse_5_GymFan_Text::
	.string "I live here with PIKACHU.\nWe're training for EIRIK.\pHe won't let you use your BAG,\nso I'm learning to plan\nahead instead of buying REVIVES.$"

Havora_CliffHouse_5_Pokemon::
	playmoncry SPECIES_PIKACHU, CRY_MODE_NORMAL
	msgbox Havora_CliffHouse_5_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_CliffHouse_5_Pokemon_Text::
	.string "PIKACHU: Pika!\pIts cheeks sparkle as it\npractices a battle stance.$"
