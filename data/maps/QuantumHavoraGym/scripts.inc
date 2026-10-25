QuantumHavoraGym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, HavoraTrial_Load
	map_script MAP_SCRIPT_ON_RESUME, HavoraTrial_Resume
	.byte 0

HavoraTrial_Resume::
	special HavoraGym_OnResume
	end

HavoraTrial_Load::
	special HavoraGym_OnLoad
	end

HavoraTrial_Welcome::
	msgbox HavoraTrial_WelcomeText, MSGBOX_NPC
	end

HavoraTrial_Gangway::
	lockall
	msgbox HavoraTrial_GangwayText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HavoraTrial_Release
	setvar VAR_0x8004, 1
	special HavoraGym_Control
	goto HavoraTrial_Release

HavoraTrial_Tide::
	lockall
	setvar VAR_0x8004, 7
	special HavoraGym_Control
	goto_if_eq VAR_RESULT, 1, HavoraTrial_LowerTide
	msgbox HavoraTrial_TideText, MSGBOX_YESNO
	goto HavoraTrial_TideConfirm
HavoraTrial_LowerTide::
	msgbox HavoraTrial_LowerText, MSGBOX_YESNO
HavoraTrial_TideConfirm::
	goto_if_eq VAR_RESULT, NO, HavoraTrial_Release
	setvar VAR_0x8004, 2
	goto HavoraTrial_Run

HavoraTrial_Board::
	lockall
	msgbox HavoraTrial_BoardText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HavoraTrial_Release
	setvar VAR_0x8004, 3
	goto HavoraTrial_Run

HavoraTrial_UpperGangway::
	lockall
	setvar VAR_0x8004, 4
	special HavoraGym_Control
	goto_if_eq VAR_RESULT, 6, HavoraTrial_NavigatorRequired
	msgbox HavoraTrial_UpperText
	goto HavoraTrial_Release

HavoraTrial_Reset::
	lockall
	msgbox HavoraTrial_ResetText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HavoraTrial_Release
	setvar VAR_0x8004, 5
	special HavoraGym_Control
	goto HavoraTrial_Release

HavoraTrial_Run::
	special HavoraGym_Control
	goto_if_eq VAR_RESULT, 2, HavoraTrial_CrewRequired
	goto_if_eq VAR_RESULT, 3, HavoraTrial_EastRequired
	goto_if_eq VAR_RESULT, 5, HavoraTrial_LevelRequired
	goto_if_ne VAR_RESULT, 1, HavoraTrial_Release
	waitstate
	goto HavoraTrial_Release
HavoraTrial_CrewRequired::
	msgbox HavoraTrial_CrewRequiredText
	goto HavoraTrial_Release
HavoraTrial_EastRequired::
	msgbox HavoraTrial_EastRequiredText
	goto HavoraTrial_Release
HavoraTrial_LevelRequired::
	msgbox HavoraTrial_LevelRequiredText
	goto HavoraTrial_Release
HavoraTrial_NavigatorRequired::
	msgbox HavoraTrial_NavigatorRequiredText
HavoraTrial_Release::
	releaseall
	end

HavoraTrial_Crew::
	trainerbattle_double TRAINER_HAVORA_DOCK_CREW, HavoraTrial_CrewIntro, HavoraTrial_CrewLoss, HavoraTrial_TwoMons, HavoraTrial_CrewWon
	msgbox HavoraTrial_CrewAfter, MSGBOX_NPC
	end
HavoraTrial_CrewWon::
	setvar VAR_HAVORA_GYM_PROGRESS, 1
	msgbox HavoraTrial_CrewAfter
	releaseall
	end
HavoraTrial_Navigator::
	trainerbattle_double TRAINER_HAVORA_NAVIGATOR, HavoraTrial_NavIntro, HavoraTrial_NavLoss, HavoraTrial_TwoMons, HavoraTrial_NavWon
	msgbox HavoraTrial_NavAfter, MSGBOX_NPC
	end
HavoraTrial_NavWon::
	setvar VAR_HAVORA_GYM_PROGRESS, 3
	msgbox HavoraTrial_NavAfter
	releaseall
	end
HavoraTrial_Captain::
	trainerbattle_double TRAINER_HAVORA_CAPTAIN, HavoraTrial_CaptainIntro, HavoraTrial_CaptainLoss, HavoraTrial_TwoMons, HavoraTrial_CaptainWon
	msgbox HavoraTrial_CaptainAfter, MSGBOX_NPC
	end
HavoraTrial_CaptainWon::
	setvar VAR_HAVORA_GYM_PROGRESS, 7
	setvar VAR_0x8004, 6
	special HavoraGym_Control
	msgbox HavoraTrial_CrestText
	msgbox HavoraTrial_CaptainAfter
	releaseall
	end

HavoraTrial_WelcomeText::
	.string "Welcome to the CAPTAIN'S TRIAL!\nEvery battle here is a double.\pUse the red winch to lower the\ngangway, then board the launch.\pThe east crew controls the lock.\nHigh water reaches the upper berth.\pThe green bell resets the boat\nand gangways. Battles stay won.$"
HavoraTrial_GangwayText::
	.string "RED WINCH\nChange the entrance gangway?$"
HavoraTrial_TideText::
	.string "LOW WATER\nRaise the eastern lock?$"
HavoraTrial_LowerText::
	.string "HIGH WATER\nLower the eastern lock?$"
HavoraTrial_BoardText::
	.string "LAUNCH LANDING\nCall or board the vessel?$"
HavoraTrial_UpperText::
	.string "The captain's gangway is lowered!$"
HavoraTrial_ResetText::
	.string "Ring the green bell to reset\nthe launch and gangways?$"
HavoraTrial_CrewRequiredText::
	.string "The east crew must clear you\nto operate the lock wheel.$"
HavoraTrial_EastRequiredText::
	.string "The vessel must be inside the\neastern lock before it can lift.$"
HavoraTrial_LevelRequiredText::
	.string "The launch is at the other\nwater level. Use the blue wheel.$"
HavoraTrial_NavigatorRequiredText::
	.string "The navigator must clear you\nto lower the captain's gangway.$"
HavoraTrial_TwoMons::
	.string "A crew needs two partners.\nBring two battle-ready POKéMON.$"
HavoraTrial_CrewIntro::
	.string "A sturdy deckhand and a lookout.\nLet's see your partners work!$"
HavoraTrial_CrewLoss::
	.string "You're clear to work the lock!$"
HavoraTrial_CrewAfter::
	.string "Keep the launch in the eastern\nlock and turn the blue wheel.\pRide at high water to reach\nthe navigator's upper berth.$"
HavoraTrial_NavIntro::
	.string "Wind, waves, and two partners.\nCan you keep your course?$"
HavoraTrial_NavLoss::
	.string "A fine course, well sailed!$"
HavoraTrial_NavAfter::
	.string "Use the yellow winch to lower\nthe captain's gangway.$"
HavoraTrial_CaptainIntro::
	.string "I'm Captain EIRIK. A crew's\nstrength lies in its trust.\pShow me how your partners\nweather a storm together!$"
HavoraTrial_CaptainLoss::
	.string "You've earned your berth!$"
HavoraTrial_CrestText::
	.string "You earned the HARBOR CREST!$"
HavoraTrial_CaptainAfter::
	.string "The HARBOR CREST marks you as\na trusted partner of this port.\pThe starboard gangways are open.\nThey lead straight to the exit.$"
