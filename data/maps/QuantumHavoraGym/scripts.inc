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
 lockall
 msgbox HavoraTrial_WelcomeText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraLock_Release
 setvar VAR_0x8004, 25
 special HavoraGym_Control
 msgbox HavoraTrial_HealedText
 releaseall
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
 warp MAP_QUANTUM_HAVORA_GYM, 255, 3, 25
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
 goto_if_eq VAR_RESULT, 9, HavoraLock_ArtworkReview
 goto_if_eq VAR_RESULT, 2, HavoraLock_CrewError
 goto_if_eq VAR_RESULT, 6, HavoraLock_NavError
 goto_if_eq VAR_RESULT, 7, HavoraLock_LevelError
 goto_if_eq VAR_RESULT, 5, HavoraLock_DockError
 goto_if_eq VAR_RESULT, 8, HavoraLock_MoorError
 msgbox HavoraLock_BlockedText
 goto HavoraLock_Release
HavoraLock_ArtworkReview::
 msgbox HavoraLock_ArtworkReviewText
 goto HavoraLock_Release
HavoraLock_ArtworkReviewText::
 .string "The lock system is being refitted.\nWater controls are offline.$"
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
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 1
 special HavoraGym_Control
 msgbox HavoraTrial_CrewAfter
 releaseall
 end
HavoraTrial_Navigator::
 setvar VAR_0x8004, 23
 setvar VAR_0x8005, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTrial_Clearance
 trainerbattle_double TRAINER_HAVORA_NAVIGATOR, HavoraTrial_NavIntro, HavoraTrial_NavLoss, HavoraTrial_TwoMons, HavoraTrial_NavigatorWon
 msgbox HavoraTrial_NavAfter, MSGBOX_NPC
 end
HavoraTrial_NavigatorWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 2
 special HavoraGym_Control
 msgbox HavoraTrial_NavAfter
 releaseall
 end
HavoraTrial_Engineer::
 setvar VAR_0x8004, 23
 setvar VAR_0x8005, 3
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTrial_Clearance
 trainerbattle_double TRAINER_HAVORA_ENGINEER, HavoraTrial_EngineerIntro, HavoraTrial_EngineerLoss, HavoraTrial_TwoMons, HavoraTrial_EngineerWon
 msgbox HavoraTrial_EngineerAfter, MSGBOX_NPC
 end
HavoraTrial_EngineerWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 8
 special HavoraGym_Control
 msgbox HavoraTrial_EngineerAfter
 releaseall
 end
HavoraTrial_Diver::
 setvar VAR_0x8004, 23
 setvar VAR_0x8005, 11
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTrial_Clearance
 trainerbattle_double TRAINER_HAVORA_DIVER, HavoraTrial_DiverIntro, HavoraTrial_DiverLoss, HavoraTrial_TwoMons, HavoraTrial_DiverWon
 msgbox HavoraTrial_DiverAfter, MSGBOX_NPC
 end
HavoraTrial_DiverWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 16
 special HavoraGym_Control
 msgbox HavoraTrial_DiverAfter
 releaseall
 end
HavoraTrial_FirstMate::
 setvar VAR_0x8004, 23
 setvar VAR_0x8005, 27
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTrial_Clearance
 trainerbattle_double TRAINER_HAVORA_FIRST_MATE, HavoraTrial_FirstMateIntro, HavoraTrial_FirstMateLoss, HavoraTrial_TwoMons, HavoraTrial_FirstMateWon
 msgbox HavoraTrial_FirstMateAfter, MSGBOX_NPC
 end
HavoraTrial_FirstMateWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 32
 special HavoraGym_Control
 msgbox HavoraTrial_FirstMateAfter
 releaseall
 end
HavoraTrial_Captain::
 setvar VAR_0x8004, 24
 special HavoraGym_Control
 goto_if_eq VAR_RESULT, 2, HavoraTrial_Clearance
 goto_if_eq VAR_RESULT, 3, HavoraTrial_FullCrew
 trainerbattle_double TRAINER_HAVORA_CAPTAIN, HavoraTrial_CaptainIntro, HavoraTrial_CaptainLoss, HavoraTrial_TwoMons, HavoraTrial_CaptainWon
 msgbox HavoraTrial_CaptainAfter, MSGBOX_NPC
 end
HavoraTrial_CaptainWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 4
 special HavoraGym_Control
 setvar VAR_0x8004, 6
 special HavoraGym_Control
 msgbox HavoraTrial_CrestText
 msgbox HavoraTrial_CaptainAfter
 releaseall
 end
HavoraTrial_Clearance::
 msgbox HavoraTrial_ClearanceText, MSGBOX_NPC
 end
HavoraTrial_FullCrew::
 msgbox HavoraTrial_FullCrewText, MSGBOX_NPC
 end
HavoraTrial_WelcomeText::
 .string "Welcome to the CAPTAIN'S TRIAL!\nSix crews test your teamwork.\pBoats stay at fixed berths.\nEqual water opens lock gates.\pLower shelves flood in place.\nGreen levers reset machinery.\pNeed your crew healed before\nyou set sail?$"
HavoraTrial_HealedText::
 .string "Your crew is ready to sail!$"
HavoraTrial_ClearanceText::
 .string "Earn clearance in this order:\nDeckhand, Navigator, Engineer,\pDiver, then First Mate.\nThe captain awaits them all.$"
HavoraTrial_FullCrewText::
 .string "My trial is six against six!\nBring six battle-ready POKéMON.\pThe steward at the entrance\nwill heal your crew for free.$"
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

HavoraTrial_EngineerIntro::
 .string "Steel, wind, and good timing.\nLet's put your crew to work!$"
HavoraTrial_EngineerLoss::
 .string "Fine work on both stations!$"
HavoraTrial_EngineerAfter::
 .string "The diver waits on the service\nisland. Secure the cargo deck.$"
HavoraTrial_DiverIntro::
 .string "Down in a wreck, slow and\nsteady wins the salvage!$"
HavoraTrial_DiverLoss::
 .string "You kept your bearings!$"
HavoraTrial_DiverAfter::
 .string "Find the First Mate on C's\nouter quay before the captain.$"
HavoraTrial_FirstMateIntro::
 .string "A storm's coming. Can your\npartners sail through it?$"
HavoraTrial_FirstMateLoss::
 .string "You're ready for the captain!$"
HavoraTrial_FirstMateAfter::
 .string "You may tension the final\ncargo bridge. Bring six aboard!$"
