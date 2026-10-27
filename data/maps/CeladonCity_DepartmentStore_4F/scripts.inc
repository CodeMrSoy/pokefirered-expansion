CeladonCity_DepartmentStore_4F_MapScripts::
	.byte 0

HavoraDepartment_BattleGear::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_BattleGear_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_BattleGear_Stock::
	.2byte ITEM_LEFTOVERS
	.2byte ITEM_LIFE_ORB
	.2byte ITEM_CHOICE_BAND
	.2byte ITEM_CHOICE_SPECS
	.2byte ITEM_CHOICE_SCARF
	.2byte ITEM_FOCUS_SASH
	.2byte ITEM_ASSAULT_VEST
	.2byte ITEM_ROCKY_HELMET
	.2byte ITEM_AIR_BALLOON
	.2byte ITEM_CLEAR_AMULET
	.2byte ITEM_MENTAL_HERB
	.2byte ITEM_WHITE_HERB
	.2byte ITEM_FLAME_ORB
	.2byte ITEM_TOXIC_ORB
	.2byte ITEM_LIGHT_CLAY
	.2byte ITEM_DAMP_ROCK
	.2byte ITEM_HEAT_ROCK
	.2byte ITEM_SMOOTH_ROCK
	.2byte ITEM_ICY_ROCK
	.2byte ITEM_EJECT_BUTTON
	.2byte ITEM_RED_CARD
	.2byte ITEM_SAFETY_GOGGLES
	.2byte ITEM_NONE

HavoraDepartment_BattleSupplies::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_BattleSupplies_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_BattleSupplies_Stock::
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFENSE
	.2byte ITEM_X_SP_ATK
	.2byte ITEM_X_SP_DEF
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_ACCURACY
	.2byte ITEM_DIRE_HIT
	.2byte ITEM_GUARD_SPEC
	.2byte ITEM_NONE

HavoraDepartment_4F_Sign::
	msgbox HavoraDepartment_4F_Sign_Text, MSGBOX_SIGN
	end

HavoraDepartment_4F_Sign_Text::
	.string "4F: BATTLE ITEMS$"

HavoraDepartment_4F_Customer::
	msgbox HavoraDepartment_4F_Customer_Text, MSGBOX_NPC
	end

HavoraDepartment_4F_Customer_Text::
	.string "Held items work automatically.\nChoose gear to fit your team.\pEIRIK does not allow BAG use\nduring his Gym battle.$"
