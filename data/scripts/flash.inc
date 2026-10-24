EventScript_FldEffFlash::
	setflashlevel 1
	releaseall
	end

EventScript_LanternRequired::
	lockall
	msgbox Text_LanternRequired, MSGBOX_DEFAULT
	releaseall
	end

Text_LanternRequired:
	.string "It's too dark to enter safely.\n"
	.string "You'll need a LANTERN.$"
