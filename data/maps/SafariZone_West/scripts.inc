SafariZone_West_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SafariZone_West_AdventureItems
	.byte 0

SafariZone_West_EventScript_RestHouseSign::
	msgbox SafariZone_West_Text_RestHouse, MSGBOX_SIGN
	end

SafariZone_West_EventScript_LostTeethNotice::
	msgbox SafariZone_West_Text_PleaseFindWardensLostTeeth, MSGBOX_SIGN
	end

SafariZone_West_EventScript_TrainerTips::
	msgbox SafariZone_West_Text_SearchForSecretHouse, MSGBOX_SIGN
	end

SafariZone_West_EventScript_AreaSign::
	msgbox SafariZone_West_Text_AreaSign, MSGBOX_SIGN
	end

SafariZone_West_AdventureItems::
	goto_if_classic SafariZone_West_ClassicGoldTeeth
	setobjectxyperm 1, 11, 17
	end

SafariZone_West_ClassicGoldTeeth::
	setobjectxyperm 1, 28, 14
	end
