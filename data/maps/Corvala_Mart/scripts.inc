Corvala_Mart_MapScripts::
	.byte 0

Corvala_Mart_Clerk::
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Corvala_Mart_Items
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Corvala_Mart_Items::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_NONE
