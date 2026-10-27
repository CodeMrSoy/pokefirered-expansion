Havora_Outfitters_MapScripts::
	.byte 0

Havora_Outfitters_Owner::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	msgbox Havora_Outfitters_Welcome
	pokemart Havora_Outfitters_Stock
	msgbox Text_PleaseComeAgain
	release
	end
Havora_Outfitters_Welcome::
	.string "Setting out from HAVORA?\nWe stock travel essentials.$"
	.align 2
Havora_Outfitters_Stock::
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_NONE
Havora_Outfitters_Traveler::
	msgbox Havora_Outfitters_Traveler_Text, MSGBOX_NPC
	end
Havora_Outfitters_Traveler_Text::
	.string "I buy my supplies before\nheading out of town.\pGood boots are useful.\nSo is a well-stocked BAG!$"
