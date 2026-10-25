HavoraDaycare_MapScripts::
	.byte 0

HavoraDaycare_Caretaker::
	goto HavoraDaycare_DaycareMan

HavoraDaycare_Caretaker_Text::
	.string "The sea breeze keeps this place calm.\nCome inside if your partner needs care.$"

HavoraDaycare_Mon::
	msgbox HavoraDaycare_Mon_Text, MSGBOX_NPC
	end

HavoraDaycare_Mon_Text::
	.string "The POKéMON looks happy and relaxed.$"

HavoraDaycare_Visitor::
	msgbox HavoraDaycare_Visitor_Text, MSGBOX_NPC
	end

HavoraDaycare_Visitor_Text::
	.string "My partner loves this quiet garden.\nWe can hear the sea below the cliffs.$"

HavoraDaycare_CoastView::
	msgbox HavoraDaycare_CoastView_Text, MSGBOX_NPC
	end

HavoraDaycare_CoastView_Text::
	.string "The cliffs protect the little field.\nPlease keep the gate clear.$"

HavoraDaycare_DaycareMan::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	special GetDaycareMonNicknames
	specialvar VAR_RESULT, GetDaycareState
	goto_if_eq VAR_RESULT, DAYCARE_EGG_WAITING, HavoraDaycare_DaycareEggWaiting
	goto_if_eq VAR_RESULT, DAYCARE_ONE_MON, HavoraDaycare_CheckOnOneMon
	goto_if_eq VAR_RESULT, DAYCARE_TWO_MONS, HavoraDaycare_CheckOnTwoMons
	msgbox DayCare_Text_ImDaycareManSpeakToMyWife
	release
	end

HavoraDaycare_DaycareEggWaiting::
	msgbox DayCare_Text_DoYouWantEgg, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, HavoraDaycare_DaycareAcceptEgg
	msgbox DayCare_Text_IWillKeepDoYouWantIt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, HavoraDaycare_DaycareAcceptEgg
	msgbox DayCare_Text_IllKeepIt
	clearflag FLAG_PENDING_DAYCARE_EGG
	special RejectEggFromDayCare
	release
	end

HavoraDaycare_DaycareAcceptEgg::
	specialvar VAR_RESULT, CalculatePlayerPartyCount
	goto_if_ne VAR_RESULT, PARTY_SIZE, HavoraDaycare_DaycareReceivedEgg
	msgbox DayCare_Text_YouHaveNoRoomForIt
	release
	end

HavoraDaycare_DaycareReceivedEgg::
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

HavoraDaycare_CheckOnOneMon::
	special GetDaycareMonNicknames
	msgbox DayCare_Text_YourMonIsDoingFine
	release
	end

HavoraDaycare_CheckOnTwoMons::
	special GetDaycareMonNicknames
	msgbox DayCare_Text_YourMonsAreDoingFine
	special SetDaycareCompatibilityString
	special ShowFieldMessageStringVar4
	waitmessage
	waitbuttonpress
	release
	end
