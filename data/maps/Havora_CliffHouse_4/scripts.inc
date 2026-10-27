Havora_CliffHouse_4_MapScripts::
	.byte 0

Havora_CliffHouse_4_RetiredSailor::
	msgbox Havora_CliffHouse_4_RetiredSailor_Text, MSGBOX_NPC
	end
Havora_CliffHouse_4_RetiredSailor_Text::
	.string "I spent forty years at sea.\nNow I watch the ships\nfrom our own window.\pBest berth I ever found.$"

Havora_CliffHouse_4_Partner::
	msgbox Havora_CliffHouse_4_Partner_Text, MSGBOX_NPC
	end
Havora_CliffHouse_4_Partner_Text::
	.string "He tells the same sea stories\nto PIDGEY every morning.\pThe little thing keeps coming\nback. It must like them.$"

Havora_CliffHouse_4_Pokemon::
	playmoncry SPECIES_PIDGEY, CRY_MODE_NORMAL
	msgbox Havora_CliffHouse_4_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_CliffHouse_4_Pokemon_Text::
	.string "PIDGEY: Prrroo!\pIt seems to be listening\nto the old sailor's story.$"
