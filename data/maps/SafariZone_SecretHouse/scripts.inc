SafariZone_SecretHouse_MapScripts::
	.byte 0

SafariZone_SecretHouse_EventScript_Attendant::
	lock
	faceplayer
	goto_if_set FLAG_GOT_HM03, SafariZone_SecretHouse_EventScript_ExplainSurf
	msgbox SafariZone_SecretHouse_Text_CongratsYouveWon
	checkitemspace ITEM_HM03
	goto_if_eq VAR_RESULT, FALSE, SafariZone_SecretHouse_EventScript_NoRoomForHM03
	giveitem_msg SafariZone_SecretHouse_Text_ReceivedHM03FromAttendant, ITEM_HM03
	msgbox SafariZone_SecretHouse_Text_ExplainSurf
	setflag FLAG_GOT_HM03
	release
	end

SafariZone_SecretHouse_EventScript_NoRoomForHM03::
	msgbox SafariZone_SecretHouse_Text_DontHaveRoomForPrize
	release
	end

SafariZone_SecretHouse_EventScript_ExplainSurf::
	msgbox SafariZone_SecretHouse_Text_ExplainSurf
	release
	end


SafariZone_SecretHouse_EventScript_StellarTraveler::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_SAFARI_STELLAR_TICKET, SafariZone_SecretHouse_StellarTravelerAfterGift
	checkitem ITEM_STELLAR_TICKET, 1
	goto_if_eq VAR_RESULT, TRUE, SafariZone_SecretHouse_StellarTravelerHasTicket
	msgbox SafariZone_SecretHouse_Text_KogaWentToVidra
	giveitem ITEM_STELLAR_TICKET, 1
	goto_if_eq VAR_RESULT, FALSE, SafariZone_SecretHouse_StellarTravelerNoRoom
	setflag FLAG_RECEIVED_SAFARI_STELLAR_TICKET
	msgbox SafariZone_SecretHouse_Text_StellarFerryDirections
	release
	end

SafariZone_SecretHouse_StellarTravelerHasTicket::
	setflag FLAG_RECEIVED_SAFARI_STELLAR_TICKET
SafariZone_SecretHouse_StellarTravelerAfterGift::
	goto_if_set FLAG_KOGA_RETURNED_FROM_HAVORA, SafariZone_SecretHouse_StellarTravelerKogaReturned
	goto_if_set FLAG_BADGE05_GET, SafariZone_SecretHouse_StellarTravelerKogaReturned
	goto_if_set FLAG_DEFEATED_KOGA, SafariZone_SecretHouse_StellarTravelerKogaReturned
	msgbox SafariZone_SecretHouse_Text_StellarFerryDirections
	release
	end

SafariZone_SecretHouse_StellarTravelerKogaReturned::
	msgbox SafariZone_SecretHouse_Text_KogaReturned
	release
	end

SafariZone_SecretHouse_StellarTravelerNoRoom::
	msgbox SafariZone_SecretHouse_Text_NoRoomForTicket
	release
	end

SafariZone_SecretHouse_Text_KogaWentToVidra::
	.string "Looking for KOGA? You missed him!\p"
	.string "He said he was heading to VIDRA,\n"
	.string "the next region over.\p"
	.string "He wanted to buy battle items\n"
	.string "at HAVORA's market.\p"
	.string "I've got an extra STELLAR TICKET.\n"
	.string "Here, you can have it!$"

SafariZone_SecretHouse_Text_StellarFerryDirections::
	.string "Show your STELLAR TICKET at\n"
	.string "VERMILION CITY's ferry dock.\p"
	.string "The ferry will take you to HAVORA\n"
	.string "on VIDRA. Try the market!$"

SafariZone_SecretHouse_Text_KogaReturned::
	.string "I heard KOGA is back at his GYM\n"
	.string "in FUCHSIA CITY.\p"
	.string "Keep your STELLAR TICKET.\n"
	.string "You can visit VIDRA again!$"

SafariZone_SecretHouse_Text_NoRoomForTicket::
	.string "Your BAG is full. Make room,\n"
	.string "then come back for my ticket.$"
