CeladonCity_DepartmentStore_2F_MapScripts::
	.byte 0

HavoraDepartment_Balls::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_Balls_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_Balls_Stock::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_PREMIER_BALL
	.2byte ITEM_HEAL_BALL
	.2byte ITEM_NET_BALL
	.2byte ITEM_NEST_BALL
	.2byte ITEM_NONE

HavoraDepartment_SpecialBalls::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart HavoraDepartment_SpecialBalls_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
HavoraDepartment_SpecialBalls_Stock::
	.2byte ITEM_DIVE_BALL
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_LUXURY_BALL
	.2byte ITEM_NONE

HavoraDepartment_2F_Sign::
	msgbox HavoraDepartment_2F_Sign_Text, MSGBOX_SIGN
	end

HavoraDepartment_2F_Sign_Text::
	.string "2F: POKE BALLS$"

HavoraDepartment_2F_Customer::
	msgbox HavoraDepartment_2F_Customer_Text, MSGBOX_NPC
	end

HavoraDepartment_2F_Customer_Text::
	.string "Different POKE BALLS suit\ndifferent encounters.\pApricorn-made balls are not\nstocked here.$"
