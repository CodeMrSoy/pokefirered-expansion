EventScript_PC::
	releaseall
	end

@ For when the player first arrives on One Island
EventScript_PCDisabled::
	msgbox OneIsland_PokemonCenter_1F_Text_UsualPCServicesUnavailable
	releaseall
	end

EventScript_PCMainMenu::
	message Text_AccessWhichPC
	waitmessage
	special CreatePCMenu
	waitstate
	goto EventScript_ChoosePCMenu
	end

EventScript_ChoosePCMenu::
	switch VAR_RESULT
	case 0, EventScript_AccessPokemonStorage
	case 1, EventScript_AccessPlayersPC
	case 2, EventScript_AccessProfOaksPC
	case 3, EventScript_AccessHallOfFame
	case 4, EventScript_TurnOffPC
	case SCR_MENU_CANCEL, EventScript_TurnOffPC
	end

EventScript_AccessPlayersPC::
	playse SE_PC_LOGIN
	msgbox Text_AccessedPlayersPC
	special PlayerPC
	waitstate
	goto EventScript_PCMainMenu
	end

EventScript_AccessPokemonStorage::
	playse SE_PC_LOGIN
	call_if_unset FLAG_SYS_NOT_SOMEONES_PC, EventScript_AccessSomeonesPC
	call_if_set FLAG_SYS_NOT_SOMEONES_PC, EventScript_AccessBillsPC
	msgbox Text_OpenedPkmnStorage
	special ShowPokemonStorageSystemPC
	waitstate
	setvar VAR_0x8004, HELPCONTEXT_PC
	special Script_SetHelpContext
	goto EventScript_PCMainMenu
	end

EventScript_AccessSomeonesPC::
	msgbox Text_AccessedSomeonesPC
	return

EventScript_AccessBillsPC::
	msgbox Text_AccessedBillsPC
	return

EventScript_TurnOffPC::
	setvar VAR_0x8004, 0
	playse SE_PC_OFF
	special AnimatePcTurnOff
	special SetHelpContextForMap
	releaseall
	end

EventScript_AccessHallOfFame::
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_TurnOffPC
	playse SE_PC_LOGIN
	setvar VAR_0x8004, HELPCONTEXT_PC_MISC
	special BackupHelpContext
	special Script_SetHelpContext
	special HallOfFamePCBeginFade
	waitstate
	special RestoreHelpContext
	goto EventScript_ChoosePCMenu
	end

EventScript_AccessProfOaksPC::
	goto_if_unset FLAG_SYS_POKEDEX_GET, EventScript_TurnOffPC
	playse SE_PC_LOGIN
	msgbox Text_AccessedProfOaksPC
	msgbox Text_HavePokedexRated, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ExitOaksPC
	setflag FLAG_OAKS_RATING_IS_VIA_PC
	call PokedexRating_EventScript_Rate
	clearflag FLAG_OAKS_RATING_IS_VIA_PC
	goto EventScript_ExitOaksPC
	end

EventScript_ExitOaksPC::
	msgbox Text_ClosedLinkToProfOaksPC
	goto EventScript_PCMainMenu
	end

EventScript_AccessPokeGlass::
	lockall
	playse SE_SELECT
	special StartPokeGlassIntro
	waitstate
EventScript_PokeGlassMenu::
	lockall
	multichoice 7, 3, MULTICHOICE_POKEGLASS, FALSE
	switch VAR_RESULT
	case 0, EventScript_PokeGlassPokedex
	case 1, EventScript_PokeGlassParty
	case 2, EventScript_PokeGlassStorage
	case 3, EventScript_PokeGlassStats
	case 4, EventScript_PokeGlassMap
	case 5, EventScript_PokeGlassSystemApp
	case 6, EventScript_PokeGlassSystemApp
	case 7, EventScript_PokeGlassSystemApp
	case 8, EventScript_PokeGlassSystemApp
	case 9, EventScript_PokeGlassSystemApp
	case 10, EventScript_PokeGlassSystemApp
	case 11, EventScript_PokeGlassSystemApp
	case SCR_MENU_CANCEL, EventScript_PokeGlassClose
	end

EventScript_PokeGlassPokedex::
	goto_if_unset FLAG_SYS_POKEDEX_GET, EventScript_PokeGlassMenu
	special OpenPokeGlassPokedex
	waitstate
	goto EventScript_PokeGlassMenu
	end

EventScript_PokeGlassStorage::
	goto_if_set FLAG_SYS_PC_STORAGE_DISABLED, EventScript_PokeGlassStorageDisabled
	playse SE_PC_LOGIN
	special OpenPokeGlassStorage
	waitstate
	goto EventScript_PokeGlassMenu
	end

EventScript_PokeGlassParty::
	getpartysize
	compare VAR_RESULT, 0
	goto_if_eq EventScript_PokeGlassMenu
	special OpenPokeGlassParty
	waitstate
	goto EventScript_PokeGlassMenu
	end

EventScript_PokeGlassMap::
	special OpenPokeGlassMap
	waitstate
	goto EventScript_PokeGlassMenu
	end

EventScript_PokeGlassStats::
	getpartysize
	compare VAR_RESULT, 0
	goto_if_eq EventScript_PokeGlassMenu
	special OpenPokeGlassStats
	waitstate
	goto EventScript_PokeGlassMenu
	end

EventScript_PokeGlassSystemApp::
	special OpenPokeGlassSystemApp
	waitstate
	goto EventScript_PokeGlassMenu
	end

EventScript_PokeGlassClose::
	releaseall
	end

EventScript_PokeGlassStorageDisabled::
	msgbox OneIsland_PokemonCenter_1F_Text_UsualPCServicesUnavailable
	goto EventScript_PokeGlassMenu
	end
