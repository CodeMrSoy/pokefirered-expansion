QuantumHarbor_MapScripts::
	.byte 0

QuantumHarbor_Sailor::
	lock
	faceplayer
	msgbox QuantumHarbor_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, QuantumHarbor_Cancel
	setvar VAR_0x8004, SEAGALLOP_QUANTUM_PORT
	setvar VAR_0x8006, SEAGALLOP_VERMILION_CITY
	goto EventScript_SailToDest
QuantumHarbor_Cancel::
	release
	end

QuantumHarbor_Return::
	.string "Return to VERMILION CITY?$"


QuantumHarbor_Merchant::
	msgbox QuantumHarbor_Merchant_Text, MSGBOX_NPC
	end

QuantumHarbor_Merchant_Text::
	.string "Our stalls trade goods from across\nVIDRA. The city lies to the west!$"

QuantumHarbor_Dockworker::
	msgbox QuantumHarbor_Dockworker_Text, MSGBOX_NPC
	end

QuantumHarbor_Dockworker_Text::
	.string "Mind the seawall!\nThe ferry boards at the main pier.$"

QuantumHarbor_Visitor::
	msgbox QuantumHarbor_Visitor_Text, MSGBOX_NPC
	end

QuantumHarbor_Visitor_Text::
	.string "I came for the market and stayed\nfor the sea air.$"

QuantumHarbor_LighthouseSign::
	msgbox QuantumHarbor_LighthouseSign_Text, MSGBOX_SIGN
	end

QuantumHarbor_LighthouseSign_Text::
	.string "HAVORA HARBOR LIGHT\nA welcome home for every sailor.$"
