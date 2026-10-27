Havora_Harbor_MapScripts::
	.byte 0

Havora_Harbor_Sailor::
	lock
	faceplayer
	msgbox Havora_Harbor_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Havora_Harbor_Cancel
	setvar VAR_0x8004, SEAGALLOP_QUANTUM_PORT
	setvar VAR_0x8006, SEAGALLOP_VERMILION_CITY
	goto EventScript_SailToDest
Havora_Harbor_Cancel::
	release
	end

Havora_Harbor_Return::
	.string "Return to VERMILION CITY?$"


Havora_Harbor_Merchant::
	msgbox Havora_Harbor_Merchant_Text, MSGBOX_NPC
	end

Havora_Harbor_Merchant_Text::
	.string "Our stalls trade goods from across\nVIDRA. The city lies to the west!$"

Havora_Harbor_Dockworker::
	msgbox Havora_Harbor_Dockworker_Text, MSGBOX_NPC
	end

Havora_Harbor_Dockworker_Text::
	.string "Mind the seawall!\nThe ferry boards at the main pier.$"

Havora_Harbor_Visitor::
	msgbox Havora_Harbor_Visitor_Text, MSGBOX_NPC
	end

Havora_Harbor_Visitor_Text::
	.string "I came for the market and stayed\nfor the sea air.$"

Havora_Harbor_LighthouseSign::
	msgbox Havora_Harbor_LighthouseSign_Text, MSGBOX_SIGN
	end

Havora_Harbor_LighthouseSign_Text::
	.string "HAVORA HARBOR LIGHT\nA welcome home for every sailor.$"

Havora_Harbor_Fisher::
	msgbox Havora_Harbor_Fisher_Text, MSGBOX_NPC
	end

Havora_Harbor_Fisher_Text::
	.string "The tide brings fish this way.\nCare to cast a line?$"

Havora_Harbor_BeaconKeeper::
	msgbox Havora_Harbor_BeaconKeeper_Text, MSGBOX_NPC
	end

Havora_Harbor_BeaconKeeper_Text::
	.string "This light guides ships home.\nWe keep it burning every night.$"
