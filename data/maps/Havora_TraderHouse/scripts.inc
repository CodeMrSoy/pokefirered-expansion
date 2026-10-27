Havora_TraderHouse_MapScripts::
	.byte 0

Havora_TraderHouse_Merchant::
	msgbox Havora_TraderHouse_Merchant_Text, MSGBOX_NPC
	end
Havora_TraderHouse_Merchant_Text::
	.string "I live alone, but my house\nnever stays quiet for long.\pMEOWTH greets every ship\nthat brings me a parcel.$"

Havora_TraderHouse_Pokemon::
	playmoncry SPECIES_MEOWTH, CRY_MODE_NORMAL
	msgbox Havora_TraderHouse_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_TraderHouse_Pokemon_Text::
	.string "MEOWTH: Meow!\pIt is guarding a parcel\ntied with a shiny ribbon.$"
