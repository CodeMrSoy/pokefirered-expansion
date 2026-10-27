Havora_HarborInn_MapScripts::
	.byte 0

Havora_HarborInn_Resident::
	lock
	faceplayer
	msgbox Havora_HarborInn_RestText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Havora_HarborInn_Release
	special HealPlayerParty
	msgbox Havora_HarborInn_RestedText
Havora_HarborInn_Release::
	release
	end
Havora_HarborInn_RestText::
	.string "Welcome to the harbor inn.\nYou look ready for a rest.\pSit a while? We'll look after\nyour POKEMON, free of charge.$"
Havora_HarborInn_RestedText::
	.string "Your POKEMON are rested!\nSafe travels, wherever you sail.$"
Havora_HarborInn_Guest::
	msgbox Havora_HarborInn_Guest_Text, MSGBOX_NPC
	end
Havora_HarborInn_Guest_Text::
	.string "My ship leaves in the morning.\nTonight, I'm happy to sit\nsomewhere that doesn't sway!$"
