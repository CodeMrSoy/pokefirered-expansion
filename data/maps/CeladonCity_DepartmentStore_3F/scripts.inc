CeladonCity_DepartmentStore_3F_MapScripts::
	.byte 0

HavoraDepartment_Stones::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_Stones_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_Stones_Stock::
	.2byte ITEM_FIRE_STONE
	.2byte ITEM_WATER_STONE
	.2byte ITEM_THUNDER_STONE
	.2byte ITEM_LEAF_STONE
	.2byte ITEM_ICE_STONE
	.2byte ITEM_SUN_STONE
	.2byte ITEM_MOON_STONE
	.2byte ITEM_SHINY_STONE
	.2byte ITEM_DUSK_STONE
	.2byte ITEM_DAWN_STONE
	.2byte ITEM_NONE

HavoraDepartment_Evolution::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_Evolution_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_Evolution_Stock::
	.2byte ITEM_LINKING_CORD
	.2byte ITEM_METAL_COAT
	.2byte ITEM_DRAGON_SCALE
	.2byte ITEM_UPGRADE
	.2byte ITEM_DUBIOUS_DISC
	.2byte ITEM_PROTECTOR
	.2byte ITEM_ELECTIRIZER
	.2byte ITEM_MAGMARIZER
	.2byte ITEM_REAPER_CLOTH
	.2byte ITEM_DEEP_SEA_TOOTH
	.2byte ITEM_DEEP_SEA_SCALE
	.2byte ITEM_PRISM_SCALE
	.2byte ITEM_SACHET
	.2byte ITEM_WHIPPED_DREAM
	.2byte ITEM_OVAL_STONE
	.2byte ITEM_RAZOR_CLAW
	.2byte ITEM_RAZOR_FANG
	.2byte ITEM_SWEET_APPLE
	.2byte ITEM_TART_APPLE
	.2byte ITEM_CRACKED_POT
	.2byte ITEM_CHIPPED_POT
	.2byte ITEM_BLACK_AUGURITE
	.2byte ITEM_PEAT_BLOCK
	.2byte ITEM_AUSPICIOUS_ARMOR
	.2byte ITEM_MALICIOUS_ARMOR
	.2byte ITEM_NONE

HavoraDepartment_3F_Sign::
	msgbox HavoraDepartment_3F_Sign_Text, MSGBOX_SIGN
	end

HavoraDepartment_3F_Sign_Text::
	.string "3F: EVOLUTION ITEMS$"

HavoraDepartment_3F_Customer::
	msgbox HavoraDepartment_3F_Customer_Text, MSGBOX_NPC
	end

HavoraDepartment_3F_Customer_Text::
	.string "Stones and evolution items\nare sold at separate counters.$"
