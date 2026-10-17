@ Retained Kanto encounters from retired areas. Numeric caught/hide flags stay stable.
QuantumRelocated_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, QuantumRelocated_TryRemoveCaught
	end

QuantumRelocated_TryRemoveCaught::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, EventScript_Return
	removeobject VAR_LAST_TALKED
	return

QuantumRelocated_Show_MEWTWO::
	setflag FLAG_HIDE_MEWTWO
	goto_if_set FLAG_FOUGHT_MEWTWO, EventScript_Return
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_Return
	clearflag FLAG_HIDE_MEWTWO
	return

QuantumRelocated_MEWTWO::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 20
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setwildbattle SPECIES_MEWTWO, 70
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, QuantumRelocated_MEWTWO_DefeatedMewtwo
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, QuantumRelocated_MEWTWO_RanFromMewtwo
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, QuantumRelocated_MEWTWO_RanFromMewtwo
	setflag FLAG_FOUGHT_MEWTWO
	release
	end

QuantumRelocated_MEWTWO_DefeatedMewtwo::
	setflag FLAG_FOUGHT_MEWTWO
	goto EventScript_RemoveStaticMon
	end

QuantumRelocated_MEWTWO_RanFromMewtwo::
	setvar VAR_0x8004, SPECIES_MEWTWO
	goto EventScript_MonFlewAway
	end


QuantumRelocated_Show_ARTICUNO::
	setflag FLAG_HIDE_ARTICUNO
	goto_if_set FLAG_FOUGHT_ARTICUNO, EventScript_Return
	clearflag FLAG_HIDE_ARTICUNO
	return

QuantumRelocated_ARTICUNO::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_ARTICUNO, 50
	waitse
	playmoncry SPECIES_ARTICUNO, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, QuantumRelocated_ARTICUNO_DefeatedArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, QuantumRelocated_ARTICUNO_RanFromArticuno
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, QuantumRelocated_ARTICUNO_RanFromArticuno
	setflag FLAG_FOUGHT_ARTICUNO
	release
	end

QuantumRelocated_ARTICUNO_DefeatedArticuno::
	setflag FLAG_FOUGHT_ARTICUNO
	goto EventScript_RemoveStaticMon
	end

QuantumRelocated_ARTICUNO_RanFromArticuno::
	setvar VAR_0x8004, SPECIES_ARTICUNO
	goto EventScript_MonFlewAway
	end




QuantumRelocated_Show_MOLTRES::
	setflag FLAG_HIDE_MOLTRES
	goto_if_set FLAG_FOUGHT_MOLTRES, EventScript_Return
	clearflag FLAG_HIDE_MOLTRES
	return

QuantumRelocated_MOLTRES::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_MOLTRES, 50
	waitse
	playmoncry SPECIES_MOLTRES, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, QuantumRelocated_MOLTRES_DefeatedMoltres
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, QuantumRelocated_MOLTRES_RanFromMoltres
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, QuantumRelocated_MOLTRES_RanFromMoltres
	setflag FLAG_FOUGHT_MOLTRES
	release
	end

QuantumRelocated_MOLTRES_DefeatedMoltres::
	setflag FLAG_FOUGHT_MOLTRES
	goto EventScript_RemoveStaticMon
	end

QuantumRelocated_MOLTRES_RanFromMoltres::
	setvar VAR_0x8004, SPECIES_MOLTRES
	goto EventScript_MonFlewAway
	end



QuantumRelocated_MewtwoOnTransition::
	call QuantumRelocated_Show_MEWTWO
	end
