Havora_CliffHouse_1_MapScripts::
	.byte 0

Havora_CliffHouse_1_Parent::
	msgbox Havora_CliffHouse_1_Parent_Text, MSGBOX_NPC
	end
Havora_CliffHouse_1_Parent_Text::
	.string "We moved here for work\nat the docks.\pOur little one already knows\nmore sailors than we do!$"

Havora_CliffHouse_1_Partner::
	msgbox Havora_CliffHouse_1_Partner_Text, MSGBOX_NPC
	end
Havora_CliffHouse_1_Partner_Text::
	.string "MACHOP carries the shopping.\nMy partner carries our child.\pI carry the list, which is\nclearly the hardest job.$"

Havora_CliffHouse_1_Child::
	msgbox Havora_CliffHouse_1_Child_Text, MSGBOX_NPC
	end
Havora_CliffHouse_1_Child_Text::
	.string "MACHOP is my best friend!\nWe're building a tiny boat.\pIt only has to fit a berry.$"

Havora_CliffHouse_1_Pokemon::
	playmoncry SPECIES_MACHOP, CRY_MODE_NORMAL
	msgbox Havora_CliffHouse_1_Pokemon_Text, MSGBOX_NPC
	waitmoncry
	end
Havora_CliffHouse_1_Pokemon_Text::
	.string "MACHOP: Machop!\pIt proudly shows you\na tiny wooden boat.$"
