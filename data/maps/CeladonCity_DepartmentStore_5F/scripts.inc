CeladonCity_DepartmentStore_5F_MapScripts::
	.byte 0

HavoraDepartment_Wings::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_Wings_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_Wings_Stock::
	.2byte ITEM_HEALTH_FEATHER
	.2byte ITEM_MUSCLE_FEATHER
	.2byte ITEM_RESIST_FEATHER
	.2byte ITEM_GENIUS_FEATHER
	.2byte ITEM_CLEVER_FEATHER
	.2byte ITEM_SWIFT_FEATHER
	.2byte ITEM_NONE

HavoraDepartment_Vitamins::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_Vitamins_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_Vitamins_Stock::
	.2byte ITEM_HP_UP
	.2byte ITEM_PROTEIN
	.2byte ITEM_IRON
	.2byte ITEM_CALCIUM
	.2byte ITEM_ZINC
	.2byte ITEM_CARBOS
	.2byte ITEM_PP_UP
	.2byte ITEM_PP_MAX
	.2byte ITEM_NONE

HavoraDepartment_5F_Sign::
	msgbox HavoraDepartment_5F_Sign_Text, MSGBOX_SIGN
	end

HavoraDepartment_5F_Sign_Text::
	.string "5F: TRAINING SUPPLIES$"

HavoraDepartment_5F_Customer::
	msgbox HavoraDepartment_5F_Customer_Text, MSGBOX_NPC
	end

HavoraDepartment_5F_Customer_Text::
	.string "Wings and vitamins raise EVs,\nnot IVs.\pChoose the stat you want\nyour POKEMON to train.$"
