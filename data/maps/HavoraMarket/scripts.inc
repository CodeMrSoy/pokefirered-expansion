HavoraMarket_MapScripts::
	.byte 0

HavoraMarket_Guide::
	msgbox HavoraMarket_Guide_Text, MSGBOX_NPC
	end

HavoraMarket_Guide_Text::
	.string "This is HAVORA's market district!\nHomes north, shops and harbor south.$"

HavoraMarket_Resident::
	msgbox HavoraMarket_Resident_Text, MSGBOX_NPC
	end

HavoraMarket_Resident_Text::
	.string "The flower beds soften all this stone.\nI love living near the waterfront.$"

HavoraMarket_Harbor::
	msgbox HavoraMarket_Harbor_Text, MSGBOX_NPC
	end

HavoraMarket_Harbor_Text::
	.string "The ferry pier is just south of here.\nYou can walk straight to the harbor.$"

HavoraMarket_Fisher::
	msgbox HavoraMarket_Fisher_Text, MSGBOX_NPC
	end

HavoraMarket_Fisher_Text::
	.string "Fresh fish arrive with the morning tide.\nThe market never stays quiet for long.$"

HavoraMarket_Supplies::
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraMarket_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraMarket_Stock::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_NONE

HavoraMarket_MarketCustomer::
	msgbox HavoraMarket_MarketCustomer_Text, MSGBOX_NPC
	end

HavoraMarket_MarketCustomer_Text::
	.string "A gift from HAVORA for my family.\nWhich stall would you choose?$"

HavoraMarket_MarketTraveler::
	msgbox HavoraMarket_MarketTraveler_Text, MSGBOX_NPC
	end

HavoraMarket_MarketTraveler_Text::
	.string "The houses climb right up the cliffs.\nI have never seen a port like it.$"
