Corvala_Town_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Corvala_Town_OnLoad
	.byte 0

Corvala_Town_OnLoad::
	callnative CorvalaTide_OnLoad
	end

Corvala_Dock_HarborGuide::
	msgbox Corvala_Dock_HarborGuide_Text, MSGBOX_NPC
	end

Corvala_Dock_HarborGuide_Text::
	.string "The tide turns every hour.\nEven hours are low tide.\pOdd hours bring high tide.\nThe docks stay above the water.$"

Corvala_Dock_ReefWatcher::
	msgbox Corvala_Dock_ReefWatcher_Text, MSGBOX_NPC
	end

Corvala_Dock_ReefWatcher_Text::
	.string "Wild POKéMON hide in the sand.\nWatch your step near the reef!\pThe wooden docks are a safe\nplace to rest your team.$"

Corvala_Dock_NetMender::
	msgbox Corvala_Dock_NetMender_Text, MSGBOX_NPC
	end

Corvala_Dock_NetMender_Text::
	.string "I mend nets while the tide is low.\nWhen it rises, I go fishing.\pThe sea keeps its own schedule.\nI just try to keep up!$"

Corvala_Dock_ShellCollector::
	msgbox Corvala_Dock_ShellCollector_Text, MSGBOX_NPC
	end

Corvala_Dock_ShellCollector_Text::
	.string "I found a shell that whistles!\nListen...\pOh. That was the wind.$"

Corvala_Dock_CoralKeeper::
	msgbox Corvala_Dock_CoralKeeper_Text, MSGBOX_NPC
	end

Corvala_Dock_CoralKeeper_Text::
	.string "These reefs are alive.\nPlease leave the coral here.\pTake a memory home instead!$"

Corvala_Dock_TideLookout::
	msgbox Corvala_Dock_TideLookout_Text, MSGBOX_NPC
	end

Corvala_Dock_TideLookout_Text::
	.string "High tide covers the sand and\nthe lower cliff below the GYM.\pVisit the GYM when the tide is\nlow. I wait here on the docks!$"

Corvala_Dock_DockCorsola::
	msgbox Corvala_Dock_DockCorsola_Text, MSGBOX_NPC
	end

Corvala_Dock_DockCorsola_Text::
	.string "CORSOLA: Cor! Corsola!\nIt basks in the salty breeze.\pThe fisher keeps an eye on it\nwhile mending the nets.$"

Corvala_Dock_DockMareanie::
	msgbox Corvala_Dock_DockMareanie_Text, MSGBOX_NPC
	end

Corvala_Dock_DockMareanie_Text::
	.string "MAREANIE waves its tentacles.\nIt seems curious about you.\pThe coral keeper makes sure\nit leaves the reef alone.$"

Corvala_Dock_DockCorsolaHome::
	msgbox Corvala_Dock_DockCorsolaHome_Text, MSGBOX_NPC
	end

Corvala_Dock_DockCorsolaHome_Text::
	.string "CORSOLA: Cor! Cor!\nIt is resting beside the hut.\pTiny flecks of sand sparkle\non its coral branches.$"
