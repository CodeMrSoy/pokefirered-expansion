Route25_MapScripts::
	.byte 0

Route25_EventScript_SeaCottageSign::
	msgbox Route25_Text_SeaCottageSign, MSGBOX_SIGN
	end

Route25_EventScript_Man::
	lock
	faceplayer
	msgbox Route25_Text_AreYouHereAlone
	living_world_aside LIVING_WORLD_ROUTE25_RESIDENT
	release
	end
