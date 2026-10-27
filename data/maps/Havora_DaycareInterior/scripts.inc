Havora_DaycareInterior_MapScripts::
	.byte 0

Havora_DaycareInterior_EventScript_DaycareWoman::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	specialvar VAR_RESULT, GetDaycareState
	goto_if_eq VAR_RESULT, DAYCARE_EGG_WAITING, Havora_DaycareInterior_EggWaiting
	goto_if_eq VAR_RESULT, DAYCARE_ONE_MON, Havora_DaycareInterior_OneMonInDaycare
	goto_if_eq VAR_RESULT, DAYCARE_TWO_MONS, Havora_DaycareInterior_TwoMonsInDaycare
	msgbox DayCare_Text_WouldYouLikeUsToRaiseMon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_GiveMonToRaise
	msgbox DayCare_Text_FineThenComeAgain
	release
	end

Havora_DaycareInterior_GiveMonToRaise::
	specialvar VAR_RESULT, CountPartyNonEggMons
	goto_if_eq VAR_RESULT, 1, Havora_DaycareInterior_OnlyOneMonInParty
	msgbox DayCare_Text_WhichMonShouldWeRaise
	fadescreen FADE_TO_BLACK
	special ChooseSendDaycareMon
	waitstate
	goto_if_ge VAR_0x8004, PARTY_SIZE, Havora_DaycareInterior_ComeAgain
	specialvar VAR_RESULT, CountPartyAliveNonEggMons_IgnoreVar0x8004Slot
	goto_if_eq VAR_RESULT, 0, Havora_DaycareInterior_OnlyOneAliveMonInParty
	specialvar VAR_0x8005, GetSelectedMonNicknameAndSpecies
	waitse
	playmoncry VAR_0x8005, CRY_MODE_NORMAL
	msgbox DayCare_Text_WellRaiseYourMon
	waitmoncry
	special StoreSelectedPokemonInDaycare
	callnative UpdateFollowingPokemon
	incrementgamestat GAME_STAT_USED_DAYCARE
	specialvar VAR_RESULT, GetDaycareState
	goto_if_eq VAR_RESULT, DAYCARE_ONE_MON, Havora_DaycareInterior_CanRaiseOneMore
	release
	end

Havora_DaycareInterior_ComeAgain::
	msgbox DayCare_Text_ComeAgain
	release
	end

Havora_DaycareInterior_CanRaiseOneMore::
	msgbox DayCare_Text_WeCanRaiseOneMore, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_GiveMonToRaise
	goto Havora_DaycareInterior_ComeAgain
	end

Havora_DaycareInterior_OnlyOneMonInParty::
	msgbox DayCare_Text_YouHaveJustOneMon
	release
	end

Havora_DaycareInterior_OnlyOneAliveMonInParty::
	msgbox DayCare_Text_WhatWillYouBattleWith
	release
	end

Havora_DaycareInterior_EggWaiting::
	msgbox DayCare_Text_HusbandWasLookingForYou
	release
	end

Havora_DaycareInterior_MonHasGrownXLevels::
	msgbox DayCare_Text_YourMonHasGrownXLevels
	return

Havora_DaycareInterior_DisplayLevelsGained::
	specialvar VAR_RESULT, GetNumLevelsGainedFromDaycare
	call_if_ne VAR_RESULT, 0, Havora_DaycareInterior_MonHasGrownXLevels
	return

Havora_DaycareInterior_OneMonInDaycare::
	msgbox DayCare_Text_GoodToSeeYou
	setvar VAR_0x8004, 0
	call Havora_DaycareInterior_DisplayLevelsGained
	msgbox DayCare_Text_WeCanRaiseOneMore, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_GiveMonToRaise
	msgbox DayCare_Text_TakeYourMonBack, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_TryRetrieveMon
	goto Havora_DaycareInterior_ComeAgain
	end

Havora_DaycareInterior_TryRetrieveMon::
	specialvar VAR_RESULT, CalculatePlayerPartyCount
	goto_if_eq VAR_RESULT, PARTY_SIZE, Havora_DaycareInterior_NoRoomInParty
	specialvar VAR_RESULT, GetDaycareState
	setvar VAR_0x8004, 0
	goto_if_eq VAR_RESULT, DAYCARE_ONE_MON, Havora_DaycareInterior_CostPrompt
	special ShowDaycareLevelMenu
	waitstate
	copyvar VAR_0x8004, VAR_RESULT
	goto_if_eq VAR_RESULT, DAYCARE_EXITED_LEVEL_MENU, Havora_DaycareInterior_ComeAgain
	goto Havora_DaycareInterior_CostPrompt
	end

Havora_DaycareInterior_CostPrompt::
	special GetDaycareCost
	msgbox DayCare_Text_ItWillCostX, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_CheckEnoughMoney
	goto Havora_DaycareInterior_ComeAgain
	end

Havora_DaycareInterior_CheckEnoughMoney::
	specialvar VAR_RESULT, IsEnoughForCostInVar0x8005
	goto_if_eq VAR_RESULT, TRUE, Havora_DaycareInterior_RetrieveMon
	msgbox DayCare_Text_NotEnoughMoney
	release
	end

Havora_DaycareInterior_RetrieveMon::
	applymovement LOCALID_HAVORA_DAYCARE_WOMAN, Havora_DaycareInterior_Movement_RetrieveMon
	waitmovement 0
	specialvar VAR_RESULT, TakePokemonFromDaycare
	special SubtractMoneyFromVar0x8005
	playse SE_RS_SHOP
	msgbox DayCare_Text_HeresYourMon
	waitse
	playmoncry VAR_RESULT, CRY_MODE_NORMAL
	textcolor NPC_TEXT_COLOR_NEUTRAL
	msgbox DayCare_Text_TookBackMon
	call EventScript_RestorePrevTextColor
	waitmoncry
	specialvar VAR_RESULT, GetDaycareState
	goto_if_eq VAR_RESULT, DAYCARE_ONE_MON, Havora_DaycareInterior_AskRetrieveOtherMon
	goto Havora_DaycareInterior_ComeAgain
	end

Havora_DaycareInterior_AskRetrieveOtherMon::
	msgbox DayCare_Text_TakeOtherOneBackToo, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_TryRetrieveMon
	goto Havora_DaycareInterior_ComeAgain
	end

Havora_DaycareInterior_NoRoomInParty::
	msgbox DayCare_Text_YourPartyIsFull
	release
	end

Havora_DaycareInterior_Movement_RetrieveMon::
	delay_16
	delay_16
	face_right
	delay_16
	delay_16
	face_left
	delay_16
	delay_16
	face_up
	walk_slower_up
	set_invisible
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	face_down
	set_visible
	walk_slower_down
	step_end

@ Unused. Possibly a commented script, or a typo end added to the above Movement script
Havora_DaycareInterior_EventScript_UnusedEnd::
	end

Havora_DaycareInterior_TwoMonsInDaycare::
	msgbox DayCare_Text_GoodToSeeYou
	setvar VAR_0x8004, 0
	call Havora_DaycareInterior_DisplayLevelsGained
	setvar VAR_0x8004, 1
	call Havora_DaycareInterior_DisplayLevelsGained
	msgbox DayCare_Text_TakeYourMonBack, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareInterior_TryRetrieveMon
	msgbox DayCare_Text_ComeAgain
	release
	end

@ Unused
Havora_DaycareInterior_EventScript_UnusedRetrieveMon::
	special ShowDaycareLevelMenu
	waitstate
	goto_if_eq VAR_RESULT, 2, Havora_DaycareInterior_ComeAgain
	copyvar VAR_0x8004, VAR_RESULT
	specialvar VAR_RESULT, TakePokemonFromDaycare
	msgbox DayCare_Text_HeresYourMon
	msgbox DayCare_Text_ComeAgain
	release
	end
