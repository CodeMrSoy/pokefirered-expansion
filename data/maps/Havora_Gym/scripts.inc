Havora_Gym_MapScripts::
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
 msgbox HavoraTide_WelcomeText
 msgbox HavoraTide_HealText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 25
 special HavoraGym_Control
 msgbox HavoraTrial_HealedText
 goto HavoraTide_Release
HavoraTide_Switch0_0::
 lockall
 msgbox HavoraTide_Help0_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 0
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help0_0::
 .string "YELLOW: B up.\nOperate this switch?$"
HavoraTide_Switch0_1::
 lockall
 msgbox HavoraTide_Help0_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 0
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help0_1::
 .string "RED: A down, C up.\nOperate this switch?$"
HavoraTide_Switch1_0::
 lockall
 msgbox HavoraTide_Help1_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 1
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help1_0::
 .string "BLUE: A up, B up, C down.\nOperate this switch?$"
HavoraTide_Switch1_1::
 lockall
 msgbox HavoraTide_Help1_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 1
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help1_1::
 .string "RED: A down, C up.\nOperate this switch?$"
HavoraTide_Switch2_0::
 lockall
 msgbox HavoraTide_Help2_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 2
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help2_0::
 .string "GREEN: A up, B down, C down.\nOperate this switch?$"
HavoraTide_Switch2_1::
 lockall
 msgbox HavoraTide_Help2_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 2
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help2_1::
 .string "BLUE: A up, B up, C down.\nOperate this switch?$"
HavoraTide_Switch3_0::
 lockall
 msgbox HavoraTide_Help3_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 3
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help3_0::
 .string "YELLOW: B up.\nOperate this switch?$"
HavoraTide_Switch3_1::
 lockall
 msgbox HavoraTide_Help3_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 3
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help3_1::
 .string "GREEN: A up, B down, C down.\nOperate this switch?$"
HavoraTide_Switch4_0::
 lockall
 msgbox HavoraTide_Help4_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 4
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help4_0::
 .string "GREEN: A up, B down, C down.\nOperate this switch?$"
HavoraTide_Switch4_1::
 lockall
 msgbox HavoraTide_Help4_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 4
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help4_1::
 .string "RED: A down, C up.\nOperate this switch?$"
HavoraTide_Switch5_0::
 lockall
 msgbox HavoraTide_Help5_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 5
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help5_0::
 .string "YELLOW: B up.\nOperate this switch?$"
HavoraTide_Switch5_1::
 lockall
 msgbox HavoraTide_Help5_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 5
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help5_1::
 .string "RED: A down, C up.\nOperate this switch?$"
HavoraTide_Switch6_0::
 lockall
 msgbox HavoraTide_Help6_0, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 6
 setvar VAR_0x8006, 0
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help6_0::
 .string "BLUE: A up, B up, C down.\nOperate this switch?$"
HavoraTide_Switch6_1::
 lockall
 msgbox HavoraTide_Help6_1, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 30
 setvar VAR_0x8005, 6
 setvar VAR_0x8006, 1
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Help6_1::
 .string "GREEN: A up, B down, C down.\nOperate this switch?$"
HavoraTide_Travel::
 lockall
 msgbox HavoraTide_TravelText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 31
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 goto HavoraTide_Release
HavoraTide_Status::
 lockall
 setvar VAR_0x8004, 21
 special HavoraGym_Control
 msgbox HavoraTide_StatusText
 goto HavoraTide_Recovery
HavoraTide_Recovery::
 msgbox HavoraTide_ResetText, MSGBOX_YESNO
 goto_if_eq VAR_RESULT, NO, HavoraTide_Release
 setvar VAR_0x8004, 15
 special HavoraGym_Control
 goto_if_ne VAR_RESULT, 1, HavoraTide_Error
 waitstate
 releaseall
 warp MAP_HAVORA_GYM, 255, 3, 25
 waitstate
 end
HavoraTide_Error::
 goto_if_eq VAR_RESULT, 2, HavoraTide_NeedClearance
 goto_if_eq VAR_RESULT, 7, HavoraTide_NeedLevels
 msgbox HavoraTide_LimitText
 goto HavoraTide_Release
HavoraTide_NeedClearance::
 msgbox HavoraTide_ClearanceText
 goto HavoraTide_Release
HavoraTide_NeedLevels::
 msgbox HavoraTide_RouteText
HavoraTide_Release::
 releaseall
 end
HavoraTrial_Harbormaster::
 trainerbattle_double TRAINER_HAVORA_HARBORMASTER, HavoraTrial_HarbormasterIntro, HavoraTrial_HarbormasterLoss, HavoraTrial_TwoMons, HavoraTrial_HarbormasterWon
 msgbox HavoraTrial_HarbormasterAfter
 goto HavoraTide_Recovery
HavoraTrial_HarbormasterWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 64
 special HavoraGym_Control
 msgbox HavoraTrial_HarbormasterAfter
 goto HavoraTide_Release
HavoraTrial_HarbormasterHint::
 msgbox HavoraTrial_HarbormasterHintText
 goto HavoraTide_Recovery
HavoraTrial_HarbormasterHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_HarbormasterIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_HarbormasterLoss::
 .string "This station is cleared!$"
HavoraTrial_HarbormasterAfter::
 .string "AL1 sails to AR2.\nGREEN raises A and drains B/C.$"
HavoraTrial_Crew::
 trainerbattle_double TRAINER_HAVORA_DOCK_CREW, HavoraTrial_CrewIntro, HavoraTrial_CrewLoss, HavoraTrial_TwoMons, HavoraTrial_CrewWon
 msgbox HavoraTrial_CrewAfter
 goto HavoraTide_Recovery
HavoraTrial_CrewWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 1
 special HavoraGym_Control
 msgbox HavoraTrial_CrewAfter
 goto HavoraTide_Release
HavoraTrial_CrewHint::
 msgbox HavoraTrial_CrewHintText
 goto HavoraTide_Recovery
HavoraTrial_CrewHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_CrewIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_CrewLoss::
 .string "This station is cleared!$"
HavoraTrial_CrewAfter::
 .string "AR3 sails to BL3 at MID.\nAR1 opens after every crew.$"
HavoraTrial_Diver::
 trainerbattle_double TRAINER_HAVORA_DIVER, HavoraTrial_DiverIntro, HavoraTrial_DiverLoss, HavoraTrial_TwoMons, HavoraTrial_DiverWon
 msgbox HavoraTrial_DiverAfter
 goto HavoraTide_Recovery
HavoraTrial_DiverWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 16
 special HavoraGym_Control
 msgbox HavoraTrial_DiverAfter
 goto HavoraTide_Release
HavoraTrial_DiverHint::
 msgbox HavoraTrial_DiverHintText
 goto HavoraTide_Recovery
HavoraTrial_DiverHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_DiverIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_DiverLoss::
 .string "This station is cleared!$"
HavoraTrial_DiverAfter::
 .string "BL3 reaches the island LEFT.\nBL1 sails to BR2 at B HIGH.$"
HavoraTrial_Engineer::
 trainerbattle_double TRAINER_HAVORA_ENGINEER, HavoraTrial_EngineerIntro, HavoraTrial_EngineerLoss, HavoraTrial_TwoMons, HavoraTrial_EngineerWon
 msgbox HavoraTrial_EngineerAfter
 goto HavoraTide_Recovery
HavoraTrial_EngineerWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 8
 special HavoraGym_Control
 msgbox HavoraTrial_EngineerAfter
 goto HavoraTide_Release
HavoraTrial_EngineerHint::
 msgbox HavoraTrial_EngineerHintText
 goto HavoraTide_Recovery
HavoraTrial_EngineerHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_EngineerIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_EngineerLoss::
 .string "This station is cleared!$"
HavoraTrial_EngineerAfter::
 .string "BR1 sails to CR2 when B and C\nare both HIGH.$"
HavoraTrial_FirstMate::
 trainerbattle_double TRAINER_HAVORA_FIRST_MATE, HavoraTrial_FirstMateIntro, HavoraTrial_FirstMateLoss, HavoraTrial_TwoMons, HavoraTrial_FirstMateWon
 msgbox HavoraTrial_FirstMateAfter
 goto HavoraTide_Recovery
HavoraTrial_FirstMateWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 32
 special HavoraGym_Control
 msgbox HavoraTrial_FirstMateAfter
 goto HavoraTide_Release
HavoraTrial_FirstMateHint::
 msgbox HavoraTrial_FirstMateHintText
 goto HavoraTide_Recovery
HavoraTrial_FirstMateHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_FirstMateIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_FirstMateLoss::
 .string "This station is cleared!$"
HavoraTrial_FirstMateAfter::
 .string "CL1 sails to BL2 at HIGH.\nAR3 needs A and B both MID.$"
HavoraTrial_Navigator::
 trainerbattle_double TRAINER_HAVORA_NAVIGATOR, HavoraTrial_NavigatorIntro, HavoraTrial_NavigatorLoss, HavoraTrial_TwoMons, HavoraTrial_NavigatorWon
 msgbox HavoraTrial_NavigatorAfter
 goto HavoraTide_Recovery
HavoraTrial_NavigatorWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 2
 special HavoraGym_Control
 msgbox HavoraTrial_NavigatorAfter
 goto HavoraTide_Release
HavoraTrial_NavigatorHint::
 msgbox HavoraTrial_NavigatorHintText
 goto HavoraTide_Recovery
HavoraTrial_NavigatorHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_NavigatorIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_NavigatorLoss::
 .string "This station is cleared!$"
HavoraTrial_NavigatorAfter::
 .string "CR1 sails to CL2.\nPrepare B MID for the island.$"
HavoraTrial_Lockkeeper::
 trainerbattle_double TRAINER_HAVORA_LOCKKEEPER, HavoraTrial_LockkeeperIntro, HavoraTrial_LockkeeperLoss, HavoraTrial_TwoMons, HavoraTrial_LockkeeperWon
 msgbox HavoraTrial_LockkeeperAfter
 goto HavoraTide_Recovery
HavoraTrial_LockkeeperWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 128
 special HavoraGym_Control
 msgbox HavoraTrial_LockkeeperAfter
 goto HavoraTide_Release
HavoraTrial_LockkeeperHint::
 msgbox HavoraTrial_LockkeeperHintText
 goto HavoraTide_Recovery
HavoraTrial_LockkeeperHintText::
 .string "Battle this crew, then operate\na switch to unlock departure.$"
HavoraTrial_LockkeeperIntro::
 .string "I've spotted a challenger!\nShow me your teamwork!$"
HavoraTrial_LockkeeperLoss::
 .string "This station is cleared!$"
HavoraTrial_LockkeeperAfter::
 .string "Depart RIGHT for AR3 at\nA/B MID; then return to B.$"
HavoraTrial_Captain::
 lockall
 setvar VAR_0x8004, 24
 special HavoraGym_Control
 goto_if_eq VAR_RESULT, 2, HavoraTrial_Clearance
 goto_if_eq VAR_RESULT, 3, HavoraTrial_FullCrew
 trainerbattle_double TRAINER_HAVORA_CAPTAIN, HavoraTrial_CaptainIntro, HavoraTrial_CaptainLoss, HavoraTrial_TwoMons, HavoraTrial_CaptainWon
 msgbox HavoraTrial_CaptainAfter
 goto HavoraTide_Recovery
HavoraTrial_CaptainWon::
 setvar VAR_0x8004, 22
 setvar VAR_0x8005, 4
 special HavoraGym_Control
 setvar VAR_0x8004, 6
 special HavoraGym_Control
 msgbox HavoraTrial_CrestText
 msgbox HavoraTrial_CaptainAfter
 goto HavoraTide_Recovery
HavoraTrial_Clearance::
 msgbox HavoraTrial_ClearanceText
 goto HavoraTide_Release
HavoraTrial_FullCrew::
 msgbox HavoraTrial_FullCrewText
 goto HavoraTide_Release
HavoraTide_WelcomeText::
 .string "Crews spot you across the quay.\nWin, then work their switches.\pGREEN: A up, B down, C down.\nRED: A down, C up.\pYELLOW: B up.\nBLUE: A up, B up, C down.\pAll levels wrap both ways.\nHIGH up becomes LOW.\pUse outbound pads marked 1.\nPads marked 2 receive arrivals.\pAR3 departs for BL3 at MID.\nThe island receives on the left\pand departs on the right.\nDrain C to reach EIRIK's bunker.$"
HavoraTide_HealText::
 .string "Heal your crew for the trial?$"
HavoraTrial_HealedText::
 .string "Your crew is ready!$"
HavoraTide_TravelText::
 .string "Board the boat to this pad's\nfixed partner? One-way sailing.$"
HavoraTide_StatusText::
 .string "{STR_VAR_1}\pCrews cleared: {STR_VAR_2}/7.\nSwitch stations used: {STR_VAR_3}/7.$"
HavoraTide_ResetText::
 .string "Drain all sections and return\nto the entrance? Victories and\pswitch clearances will be kept.$"
HavoraTide_ClearanceText::
 .string "Battle this station's trainer\nand operate a switch first.$"
HavoraTide_RouteText::
 .string "The lift or island is out of\nreach at these water levels.$"
HavoraTide_LimitText::
 .string "No change is possible. Check\nthe water limits and your pad.$"
HavoraTrial_ClearanceText::
 .string "Operate switches at all seven\nstations and defeat their crews.\pMy bunker must be fully drained.$"
HavoraTrial_FullCrewText::
 .string "My trial is six against six!\nBring six battle-ready POKéMON.\pThe entrance steward can heal\nyour crew for free.$"
HavoraTrial_TwoMons::
 .string "Bring two battle-ready POKéMON\nfor this double battle.$"
HavoraTrial_CaptainIntro::
 .string "Every tide, every station!\nI am Captain EIRIK.\pShow me the teamwork that\nbrought you to my bunker!$"
HavoraTrial_CaptainLoss::
 .string "You've earned your berth!$"
HavoraTrial_CrestText::
 .string "You earned the HAVORA CREST!$"
HavoraTrial_CaptainAfter::
 .string "The HAVORA CREST marks you as\na trusted partner of this port.$"
