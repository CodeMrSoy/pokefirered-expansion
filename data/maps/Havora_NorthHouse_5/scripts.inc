Havora_NorthHouse_5_MapScripts::
	.byte 0

Havora_NorthHouse_5_Resident::
	msgbox Havora_NorthHouse_5_Resident_Text, MSGBOX_NPC
	end
Havora_NorthHouse_5_Resident_Text::
	.string "This house looks out toward\nthe mountain and the stars.\pOn a clear night, the sea\nseems to hold a second sky.$"

Havora_NorthHouse_5_Researcher::
	msgbox Havora_NorthHouse_5_Researcher_Text, MSGBOX_NPC
	end
Havora_NorthHouse_5_Researcher_Text::
	.string "A trader in the market has\na genuine METEORITE.\pIt can change DEOXYS's form,\nand it isn't used up.\pStrange things find their\nway into a trading port!$"

Havora_NorthHouse_5_Pokemon::
	playmoncry SPECIES_CLEFAIRY, CRY_MODE_NORMAL
	msgbox Havora_NorthHouse_5_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_NorthHouse_5_Pokemon_Text::
	.string "CLEFAIRY: Clef!\pIt sways as though following\na tune from far away.$"
