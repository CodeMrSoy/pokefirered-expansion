PewterCity_Mart_MapScripts::
	.byte 0

PewterCity_Mart_EventScript_Youngster::
	msgbox PewterCity_Mart_Text_BoughtWeirdFishFromShadyGuy, MSGBOX_NPC
	end

PewterCity_Mart_EventScript_Boy::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	msgbox PewterCity_Mart_Text_GoodThingsIfRaiseMonsDiligently
	living_world_aside LIVING_WORLD_EVOLUTION_MART
	callnative LivingWorld_BeginPalletOptional
	.byte LIVING_WORLD_EVOLUTION_CHECKOUT
	gotonative LivingWorld_WaitForDialogue
	goto_if_eq VAR_RESULT, TRUE, PewterCity_Mart_EventScript_ApprenticeCheckout
	callnative LivingWorld_BeginPalletOptional
	.byte LIVING_WORLD_EVOLUTION_PITCH
	gotonative LivingWorld_WaitForDialogue
	goto_if_ne VAR_RESULT, TRUE, PewterCity_Mart_EventScript_ResidentDone
	msgbox gLivingWorldDialogue, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, PewterCity_Mart_EventScript_ResidentDone
	living_world_aside LIVING_WORLD_EVOLUTION_SUPPORT
PewterCity_Mart_EventScript_ResidentDone::
	release
	end

PewterCity_Mart_EventScript_ApprenticeCheckout::
	msgbox gLivingWorldDialogue, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, PewterCity_Mart_EventScript_ResidentDone
	pokemart PewterCity_Mart_Items
	msgbox Text_PleaseComeAgain
	release
	end

PewterCity_Mart_EventScript_Clerk::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart PewterCity_Mart_Items
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
PewterCity_Mart_Items::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_NONE
	release
	end
