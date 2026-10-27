Havora_CliffHouse_2_MapScripts::
	.byte 0

Havora_CliffHouse_2_Resident::
	msgbox Havora_CliffHouse_2_Resident_Text, MSGBOX_NPC
	end
Havora_CliffHouse_2_Resident_Text::
	.string "My partner works at the docks.\nWhen the shift ends, we watch\nthe ferries from up here.\pA busy port can still be\na quiet place to call home.$"

Havora_CliffHouse_2_Dockworker::
	msgbox Havora_CliffHouse_2_Dockworker_Text, MSGBOX_NPC
	end
Havora_CliffHouse_2_Dockworker_Text::
	.string "EIRIK trains the crews to\nwork together in doubles.\pA harbor needs teamwork.\nSo does a good POKEMON team.$"

Havora_CliffHouse_2_Pokemon::
	playmoncry SPECIES_MEOWTH, CRY_MODE_NORMAL
	msgbox Havora_CliffHouse_2_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_CliffHouse_2_Pokemon_Text::
	.string "MEOWTH: Mrrrow!\pIt has claimed the warmest\nspot in the house.$"
