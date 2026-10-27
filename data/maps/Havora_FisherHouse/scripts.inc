Havora_FisherHouse_MapScripts::
	.byte 0

Havora_FisherHouse_Owner::
	msgbox Havora_FisherHouse_Owner_Text, MSGBOX_NPC
	end
Havora_FisherHouse_Owner_Text::
	.string "Welcome! We fish the harbor\nand bring our catch to market.\pTry different rods and spots.\nThe sea has room for more\nthan one kind of POKEMON.$"

Havora_FisherHouse_Child::
	msgbox Havora_FisherHouse_Child_Text, MSGBOX_NPC
	end
Havora_FisherHouse_Child_Text::
	.string "I watch the fishing boats\nfrom the window.\pOne day I'll have a little\nboat and a partner of my own!$"

Havora_FisherHouse_Pokemon::
	playmoncry SPECIES_PSYDUCK, CRY_MODE_NORMAL
	msgbox Havora_FisherHouse_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_FisherHouse_Pokemon_Text::
	.string "PSYDUCK: Psy?\pIt is staring into an empty\nbucket as if expecting a fish.$"
