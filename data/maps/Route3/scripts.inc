Route3_MapScripts::
	.byte 0

Route3_EventScript_Youngster::
	lock
	faceplayer
	msgbox Route3_Text_TunnelFromCeruleanTiring
	living_world_aside LIVING_WORLD_ROUTE3_WALKER
	release
	end

Route3_EventScript_RouteSign::
	msgbox Route3_Text_RouteSign, MSGBOX_SIGN
	end
