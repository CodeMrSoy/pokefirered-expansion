Havora_DaycareExterior_MapScripts::
	.byte 0

Havora_DaycareExterior_Caretaker::
	goto Havora_DaycareExterior_DaycareMan

Havora_DaycareExterior_Caretaker_Text::
	.string "The sea breeze keeps this place calm.\nCome inside if your partner needs care.$"

Havora_DaycareExterior_Mon::
	msgbox Havora_DaycareExterior_Mon_Text, MSGBOX_NPC
	end

Havora_DaycareExterior_Mon_Text::
	.string "The POKéMON looks happy and relaxed.$"

Havora_DaycareExterior_Visitor::
	msgbox Havora_DaycareExterior_Visitor_Text, MSGBOX_NPC
	end

Havora_DaycareExterior_Visitor_Text::
	.string "My partner loves this quiet garden.\nWe can hear the sea below the cliffs.$"

Havora_DaycareExterior_CoastView::
	msgbox Havora_DaycareExterior_CoastView_Text, MSGBOX_NPC
	end

Havora_DaycareExterior_CoastView_Text::
	.string "The cliffs protect the little field.\nPlease keep the gate clear.$"

Havora_DaycareExterior_DaycareMan::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	special GetDaycareMonNicknames
	specialvar VAR_RESULT, GetDaycareState
	goto_if_eq VAR_RESULT, DAYCARE_EGG_WAITING, Havora_DaycareExterior_DaycareEggWaiting
	goto_if_eq VAR_RESULT, DAYCARE_ONE_MON, Havora_DaycareExterior_CheckOnOneMon
	goto_if_eq VAR_RESULT, DAYCARE_TWO_MONS, Havora_DaycareExterior_CheckOnTwoMons
	msgbox DayCare_Text_ImDaycareManSpeakToMyWife
	release
	end

Havora_DaycareExterior_DaycareEggWaiting::
	msgbox DayCare_Text_DoYouWantEgg, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareExterior_DaycareAcceptEgg
	msgbox DayCare_Text_IWillKeepDoYouWantIt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Havora_DaycareExterior_DaycareAcceptEgg
	msgbox DayCare_Text_IllKeepIt
	clearflag FLAG_PENDING_DAYCARE_EGG
	special RejectEggFromDayCare
	release
	end

Havora_DaycareExterior_DaycareAcceptEgg::
	specialvar VAR_RESULT, CalculatePlayerPartyCount
	goto_if_ne VAR_RESULT, PARTY_SIZE, Havora_DaycareExterior_DaycareReceivedEgg
	msgbox DayCare_Text_YouHaveNoRoomForIt
	release
	end

Havora_DaycareExterior_DaycareReceivedEgg::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	message DayCare_Text_ReceivedEgg
	call EventScript_RestorePrevTextColor
	playfanfare MUS_LEVEL_UP
	waitfanfare
	waitbuttonpress
	msgbox DayCare_Text_TakeGoodCareOfIt
	special GiveEggFromDaycare
	clearflag FLAG_PENDING_DAYCARE_EGG
	release
	end

Havora_DaycareExterior_CheckOnOneMon::
	special GetDaycareMonNicknames
	msgbox DayCare_Text_YourMonIsDoingFine
	release
	end

Havora_DaycareExterior_CheckOnTwoMons::
	special GetDaycareMonNicknames
	msgbox DayCare_Text_YourMonsAreDoingFine
	special SetDaycareCompatibilityString
	special ShowFieldMessageStringVar4
	waitmessage
	waitbuttonpress
	release
	end
