QuantumHavoraGym_MapScripts::
 map_script MAP_SCRIPT_ON_LOAD, HavoraTrial_Load
 map_script MAP_SCRIPT_ON_RESUME, HavoraTrial_Resume
 .byte 0
HavoraTrial_Load::
 special HavoraGym_OnLoad
 end
HavoraTrial_Resume::
 special HavoraGym_OnResume
 end
HavoraTrial_Welcome::
 msgbox HavoraTrial_WelcomeText, MSGBOX_NPC
 end
HavoraLock_ABForward::
 lockall
 msgbox HavoraLock_ABForwardText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 10
 setvar VAR_0x8005, 0
 setvar VAR_0x8006, 1
 goto HavoraLock_Run
HavoraLock_ABReverse::
 lockall
 msgbox HavoraLock_ABReverseText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 10
 setvar VAR_0x8005, 1
 setvar VAR_0x8006, 0
 goto HavoraLock_Run
HavoraLock_BCForward::
 lockall
 msgbox HavoraLock_BCForwardText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 10
 setvar VAR_0x8005, 1
 setvar VAR_0x8006, 2
 goto HavoraLock_Run
HavoraLock_BCReverse::
 lockall
 msgbox HavoraLock_BCReverseText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 10
 setvar VAR_0x8005, 2
 setvar VAR_0x8006, 1
 goto HavoraLock_Run
HavoraLock_Board0::
 lockall
 setvar VAR_0x8005, 0
 setvar VAR_0x8004, 20
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraLock_Error
 waitstate
 goto_if_eq VAR_RESULT, 127, HavoraLock_Release
 copyvar VAR_0x8006, VAR_RESULT
 setvar VAR_0x8004, 11
 goto HavoraLock_Run
HavoraLock_Board1::
 lockall
 setvar VAR_0x8005, 1
 setvar VAR_0x8004, 20
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraLock_Error
 waitstate
 goto_if_eq VAR_RESULT, 127, HavoraLock_Release
 copyvar VAR_0x8006, VAR_RESULT
 setvar VAR_0x8004, 11
 goto HavoraLock_Run
HavoraLock_ServiceMoor::
 lockall
 msgbox HavoraLock_ServiceMoorText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 12
 goto HavoraLock_Run
HavoraLock_Chain::
 lockall
 msgbox HavoraLock_ChainText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 13
 goto HavoraLock_Run
HavoraLock_FinalMoor::
 lockall
 msgbox HavoraLock_FinalMoorText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 14
 goto HavoraLock_Run
HavoraLock_Status::
 lockall
 setvar VAR_0x8004, 21
 special HavoraGym_Control
 msgbox HavoraLock_StatusText
 goto HavoraLock_Release
HavoraLock_Reset::
 lockall
 msgbox HavoraLock_ResetText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 15
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraLock_Error
 waitstate
 releaseall
 warp MAP_QUANTUM_HAVORA_GYM, 255, 3, 48
 waitstate
 end
HavoraLock_Run::
 special HavoraGym_Control
 goto_if_eq VAR_RESULT, 1, HavoraLock_Wait
 goto_if_eq VAR_RESULT, 0, HavoraLock_Release
 goto HavoraLock_Error
HavoraLock_Wait::
 waitstate
 goto_if_eq VAR_0x8004, 12, HavoraLock_MoorDone
 goto_if_eq VAR_0x8004, 13, HavoraLock_ChainDone
 goto_if_eq VAR_0x8004, 14, HavoraLock_BridgeDone
 goto HavoraLock_Release
HavoraLock_MoorDone::
 msgbox HavoraLock_MoorDoneText
 goto HavoraLock_Release
HavoraLock_ChainDone::
 msgbox HavoraLock_ChainDoneText
 goto HavoraLock_Release
HavoraLock_BridgeDone::
 msgbox HavoraLock_BridgeDoneText
 goto HavoraLock_Release
HavoraLock_Error::
 goto_if_eq VAR_RESULT, 2, HavoraLock_CrewError
 goto_if_eq VAR_RESULT, 6, HavoraLock_NavError
 goto_if_eq VAR_RESULT, 7, HavoraLock_LevelError
 goto_if_eq VAR_RESULT, 5, HavoraLock_DockError
 goto_if_eq VAR_RESULT, 8, HavoraLock_MoorError
 msgbox HavoraLock_BlockedText
 goto HavoraLock_Release
HavoraLock_CrewError::
 msgbox HavoraLock_CrewText
 goto HavoraLock_Release
HavoraLock_NavError::
 msgbox HavoraLock_NavText
 goto HavoraLock_Release
HavoraLock_LevelError::
 msgbox HavoraLock_LimitText
 goto HavoraLock_Release
HavoraLock_MoorError::
 msgbox HavoraLock_MoorErrorText
 goto HavoraLock_Release
HavoraLock_DockError::
 msgbox HavoraLock_DockText
HavoraLock_Release::
 releaseall
 end
HavoraLock_MoorDoneText::
 .string "The mooring has been adjusted.\nCheck the cargo bridge.$"
HavoraLock_ChainDoneText::
 .string "The outer chain is free!$"
HavoraLock_BridgeDoneText::
 .string "The cargo bridge is secured!\nYou can reach the captain now.$"
HavoraLock_MoorErrorText::
 .string "The mooring cannot move yet.\nCheck the cargo boat and water.\pThe outer mooring also needs\nits maintenance chain released.$"
HavoraLock_ABForwardText::
 .string "TRANSFER A TO B\nMove one water level?$"
HavoraLock_ABReverseText::
 .string "TRANSFER B TO A\nMove one water level?$"
HavoraLock_BCForwardText::
 .string "TRANSFER B TO C\nMove one water level?$"
HavoraLock_BCReverseText::
 .string "TRANSFER C TO B\nMove one water level?$"
HavoraLock_ServiceMoorText::
 .string "SERVICE MOORING\nSecure or release the bridge?$"
HavoraLock_ChainText::
 .string "MAINTENANCE WINCH\nRelease the outer chain?$"
HavoraLock_FinalMoorText::
 .string "OUTER MOORING\nTension the final cargo bridge?$"
HavoraLock_StatusText::
 .string "{STR_VAR_1}\pEach transfer moves one level.\nEqual levels open a boat gate.$"
HavoraLock_ResetText::
 .string "Reset the whole lock system?\nTrainer victories are kept.$"
HavoraLock_BlockedText::
 .string "This route is blocked.\nCheck the water and moorings.$"
HavoraLock_CrewText::
 .string "The dock crew must clear you\nto operate this manifold.$"
HavoraLock_NavText::
 .string "The navigator must clear you\nto operate the control terrace.$"
HavoraLock_LimitText::
 .string "The donor is already LOW, or\nthe receiver is already HIGH.$"
HavoraLock_DockText::
 .string "No free boat is moored at this\nlanding and water level.$"

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
 .string "Welcome to the CAPTAIN'S TRIAL!\nEvery battle here is a double.\pMove one water level at a time.\nEqual levels open boat gates.\pClimb ladders to dry controls.\nLow docks flood as water rises.\pBoth boats matter. Green levers\nreset locks, but keep victories.$"
HavoraTrial_TwoMons::
	.string "A crew needs two partners.\nBring two battle-ready POKéMON.$"
HavoraTrial_CrewIntro::
	.string "A deckhand and a lookout.\nLet's see your partners work!$"
HavoraTrial_CrewLoss::
	.string "You're clear to work the lock!$"
HavoraTrial_CrewAfter::
 .string "You may now use the B/C pump.\nWatch which landings stay dry.$"
HavoraTrial_NavIntro::
	.string "Wind, waves, and two partners.\nCan you keep your course?$"
HavoraTrial_NavLoss::
	.string "A fine course, well sailed!$"
HavoraTrial_NavAfter::
 .string "The control terrace is yours.\nLeave yourself a way back.$"
HavoraTrial_CaptainIntro::
	.string "I'm Captain EIRIK. A crew's\nstrength lies in its trust.\pShow me how your partners\nweather a storm together!$"
HavoraTrial_CaptainLoss::
	.string "You've earned your berth!$"
HavoraTrial_CrestText::
	.string "You earned the HAVORA CREST!$"
HavoraTrial_CaptainAfter::
	.string "The HAVORA CREST marks you as\na trusted partner of this port.\pBoth partners earned this seal.\nUse a green lever to return.$"
