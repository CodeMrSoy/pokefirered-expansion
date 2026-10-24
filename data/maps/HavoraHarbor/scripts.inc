HavoraHarbor_MapScripts::
	.byte 0

HavoraHarbor_Sailor::
	lock
	faceplayer
	msgbox HavoraHarbor_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HavoraHarbor_Cancel
	setvar VAR_0x8004, SEAGALLOP_QUANTUM_PORT
	setvar VAR_0x8006, SEAGALLOP_VERMILION_CITY
	goto EventScript_SailToDest
HavoraHarbor_Cancel::
	release
	end

HavoraHarbor_Return::
	.string "Return to VERMILION CITY?$"


HavoraHarbor_Merchant::
	msgbox HavoraHarbor_Merchant_Text, MSGBOX_NPC
	end

HavoraHarbor_Merchant_Text::
	.string "Our stalls trade goods from across\nVIDRA. The city lies to the west!$"

HavoraHarbor_Dockworker::
	msgbox HavoraHarbor_Dockworker_Text, MSGBOX_NPC
	end

HavoraHarbor_Dockworker_Text::
	.string "Mind the seawall!\nThe ferry boards at the main pier.$"

HavoraHarbor_Visitor::
	msgbox HavoraHarbor_Visitor_Text, MSGBOX_NPC
	end

HavoraHarbor_Visitor_Text::
	.string "I came for the market and stayed\nfor the sea air.$"

HavoraHarbor_LighthouseSign::
	msgbox HavoraHarbor_LighthouseSign_Text, MSGBOX_SIGN
	end

HavoraHarbor_LighthouseSign_Text::
	.string "HAVORA HARBOR LIGHT\nA welcome home for every sailor.$"

HavoraHarbor_Fisher::
	msgbox HavoraHarbor_Fisher_Text, MSGBOX_NPC
	end

HavoraHarbor_Fisher_Text::
	.string "The tide brings fish this way.\nCare to cast a line?$"

HavoraHarbor_BeaconKeeper::
	msgbox HavoraHarbor_BeaconKeeper_Text, MSGBOX_NPC
	end

HavoraHarbor_BeaconKeeper_Text::
	.string "This light guides ships home.\nWe keep it burning every night.$"
