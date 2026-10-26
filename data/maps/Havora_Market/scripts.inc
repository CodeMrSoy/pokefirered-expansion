Havora_Market_MapScripts::
	.byte 0

Havora_Market_Guide::
	msgbox Havora_Market_Guide_Text, MSGBOX_NPC
	end

Havora_Market_Guide_Text::
	.string "This is HAVORA's market district!\nHomes north, shops and harbor south.$"

Havora_Market_Resident::
	msgbox Havora_Market_Resident_Text, MSGBOX_NPC
	end

Havora_Market_Resident_Text::
	.string "The flower beds soften all this stone.\nI love living near the waterfront.$"

Havora_Market_Harbor::
	msgbox Havora_Market_Harbor_Text, MSGBOX_NPC
	end

Havora_Market_Harbor_Text::
	.string "The ferry pier is just south of here.\nYou can walk straight to the harbor.$"

Havora_Market_Fisher::
	msgbox Havora_Market_Fisher_Text, MSGBOX_NPC
	end

Havora_Market_Fisher_Text::
	.string "Fresh fish arrive with the morning tide.\nThe market never stays quiet for long.$"

Havora_Market_Supplies::
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_Stock::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_NONE

Havora_Market_MarketCustomer::
	msgbox Havora_Market_MarketCustomer_Text, MSGBOX_NPC
	end

Havora_Market_MarketCustomer_Text::
	.string "A gift from HAVORA for my family.\nWhich stall would you choose?$"

Havora_Market_MarketTraveler::
	msgbox Havora_Market_MarketTraveler_Text, MSGBOX_NPC
	end

Havora_Market_MarketTraveler_Text::
	.string "The houses climb right up the cliffs.\nI have never seen a port like it.$"
