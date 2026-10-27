Havora_CliffHouse_3_MapScripts::
	.byte 0

Havora_CliffHouse_3_Baker::
	msgbox Havora_CliffHouse_3_Baker_Text, MSGBOX_NPC
	end
Havora_CliffHouse_3_Baker_Text::
	.string "I bake before the first ferry.\nThe kitchen is warm even\nwhen the harbor is cold.\pMy daughter helps me count\nthe loaves. Usually.$"

Havora_CliffHouse_3_Daughter::
	msgbox Havora_CliffHouse_3_Daughter_Text, MSGBOX_NPC
	end
Havora_CliffHouse_3_Daughter_Text::
	.string "Mum says we have twelve rolls.\nI counted eleven.\pJIGGLYPUFF looks very pleased\nwith itself...$"

Havora_CliffHouse_3_Pokemon::
	playmoncry SPECIES_JIGGLYPUFF, CRY_MODE_NORMAL
	msgbox Havora_CliffHouse_3_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_CliffHouse_3_Pokemon_Text::
	.string "JIGGLYPUFF: Jiggly!\pThere are crumbs beside it.\nIt looks away.$"
