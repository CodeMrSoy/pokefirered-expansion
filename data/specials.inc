@ 'requests_effects' should be set to 1 if the special contains a call
@ to 'Script_RequestEffects', which allows it to be analyzed with
@ 'RunScriptImmediatelyUntilEffect'.
.macro def_special ptr:req, requests_effects=0, retired=0
.global SPECIAL_\ptr
.set SPECIAL_\ptr, __special__
.set __special__, __special__ + 1
	.if \retired == 1
	.4byte NullFieldSpecial
	.elseif \requests_effects == 0
	.4byte \ptr
	.else
	.4byte \ptr + ROM_SIZE
	.endif
.endm

.set __special__, 0
		.align 2
gSpecials::
	def_special HealPlayerParty
	def_special SetCableClubWarp
	def_special DoCableClubWarp
	def_special ReturnFromLinkRoom
	def_special CleanupLinkRoomState
	def_special ExitLinkRoom
	def_special NullFieldSpecial  @ Secret Base specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special PlayerHasMulch
	def_special Bag_ChooseMulch
	def_special CanWaterBerryPlot
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special ObjectEventInteractionWaterBerryTree
	def_special PlayerHasBerries
	def_special TryBattleLinkup, retired=TRUE
	def_special TryTradeLinkup, retired=TRUE
	def_special TryRecordMixLinkup, retired=TRUE
	def_special CloseLink
	def_special EnterColosseumPlayerSpot
	def_special EnterTradeSeat, retired=TRUE
	def_special StartWiredCableClubTrade, retired=TRUE
	def_special CableClub_AskSaveTheGame
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special SavePlayerParty
	def_special LoadPlayerParty
	def_special ChooseHalfPartyForBattle
	def_special Script_ShowLinkTrainerCard, retired=TRUE
	def_special ObjectEventInteractionGetBerryTreeData
	def_special ObjectEventInteractionGetBerryName
	def_special ObjectEventInteractionGetBerryCountString
	def_special Bag_ChooseBerry
	def_special ObjectEventInteractionPlantBerryTree
	def_special ObjectEventInteractionPickBerryTree
	def_special ObjectEventInteractionRemoveBerryTree
	def_special IsEnigmaBerryValid
	def_special GetTrainerBattleMode
	def_special ShowTrainerIntroSpeech
	def_special ShowTrainerCantBattleSpeech
	def_special Script_HasTrainerBeenFought
	def_special EndTrainerApproach
	def_special PlayTrainerEncounterMusic
	def_special ShouldTryRematchBattle
	def_special IsTrainerReadyForRematch
	def_special BattleSetup_StartRematchBattle
	def_special ShowPokemonStorageSystemPC, retired=TRUE
	def_special HasEnoughMonsForDoubleBattle
	def_special NullFieldSpecial  @ Hoenn TV specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special HasLeadMonBeenRenamed
	def_special NullFieldSpecial  @ Contest specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special TryContestLinkup, retired=TRUE
	def_special Field_AskSaveTheGame
	def_special DoWateringBerryTreeAnim
	def_special ShowEasyChatScreen, retired=TRUE
	def_special ShowEasyChatMessage, retired=TRUE
	def_special NullFieldSpecial  @ Mauville Man specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special GetHeracrossSizeRecordInfo
	def_special CompareHeracrossSize
	def_special GetMagikarpSizeRecordInfo
	def_special CompareMagikarpSize
	def_special NameRaterWasNicknameChanged
	def_special BufferMonNickname
	def_special IsMonOTIDNotPlayers
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special BufferRandomHobbyOrLifestyleString
	def_special NullFieldSpecial
	def_special RegisteredItemHandleBikeSwap
	def_special CalculatePlayerPartyCount
	def_special CountPartyNonEggMons
	def_special CountPartyAliveNonEggMons_IgnoreVar0x8004Slot
	def_special NullFieldSpecial  @ Contest specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial  @ Mauville Gym specials
	def_special NullFieldSpecial
	def_special ShowFieldMessageStringVar4
	def_special DrawWholeMapView
	def_special GetPlayerXY
	def_special NullFieldSpecial  @ Mauville/Petalburg Gym specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special GetPlayerTrainerIdOnesDigit
	def_special BufferBigGuyOrBigGirlString
	def_special BufferSonOrDaughterString
	def_special SetHiddenItemFlag
	def_special NullFieldSpecial  @ Cable Car specials
	def_special NullFieldSpecial
	def_special Overworld_PlaySpecialMapMusic
	def_special StartWallClock
	def_special Special_ViewWallClock
	def_special NullFieldSpecial
	def_special StartOldManTutorialBattle, retired=TRUE
	def_special ChangePokemonNickname
	def_special ChoosePartyMon
	def_special NullFieldSpecial  @ Berry Blender/Roulette specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special Script_IsFanClubMemberFanOfPlayer
	def_special Script_GetNumFansOfPlayerInTrainerFanClub
	def_special Script_BufferFanClubTrainerName
	def_special Script_TryLoseFansFromPlayTimeAfterLinkBattle
	def_special Script_TryLoseFansFromPlayTime
	def_special Script_SetPlayerGotFirstFans
	def_special Script_UpdateTrainerFanClubGameClear
	def_special Script_TryGainNewFanFromCounter
	def_special RockSmashWildEncounter
	def_special NullFieldSpecial  @ Gabby and Ty specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special GetBattleOutcome
	def_special GetDaycareMonNicknames
	def_special GetDaycareState
	def_special RejectEggFromDayCare
	def_special GiveEggFromDaycare
	def_special SetDaycareCompatibilityString
	def_special GetSelectedMonNicknameAndSpecies
	def_special StoreSelectedPokemonInDaycare
	def_special ChooseSendDaycareMon
	def_special ShowDaycareLevelMenu
	def_special GetNumLevelsGainedFromDaycare
	def_special GetDaycareCost
	def_special TakePokemonFromDaycare
	def_special ScriptHatchMon
	def_special EggHatch
	def_special DaycareMonReceivedMail
	def_special ShowBattleRecords, retired=TRUE
	def_special IsEnoughForCostInVar0x8005
	def_special SubtractMoneyFromVar0x8005
	def_special TryFieldPoisonWhiteOut
	def_special SetCB2WhiteOut
	def_special NullFieldSpecial  @ Rotating gate puzzle specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial  @ SS Tidal specials
	def_special NullFieldSpecial
	def_special EnterSafariMode
	def_special ExitSafariMode
	def_special GetWeekCount
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special GetPokedexCount
	def_special GetProfOaksRatingMessage
	def_special AnimatePcTurnOn
	def_special AnimatePcTurnOff
	def_special GetElevatorFloor
	def_special NullFieldSpecial  @ Lottery Corner specials
	def_special NullFieldSpecial
	def_special ChooseMonForMoveRelearner
	def_special SelectMoveDeleterMove
	def_special MoveDeleterForgetMove
	def_special BufferMoveDeleterNicknameAndMove
	def_special GetNumMovesSelectedMonHas
	def_special TeachMoveRelearnerMove
	def_special NullFieldSpecial  @ Hoenn Cycling Road specials
	def_special NullFieldSpecial
	def_special GetPlayerAvatarBike
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special GetLeadMonFriendship
	def_special BattleTowerMapScript2, retired=TRUE
	def_special ChooseNextBattleTowerTrainer, retired=TRUE
	def_special CheckPartyBattleTowerBanlist, retired=TRUE
	def_special PrintBattleTowerTrainerGreeting, retired=TRUE
	def_special BufferEReaderTrainerGreeting
	def_special StartSpecialBattle
	def_special SetBattleTowerProperty, retired=TRUE
	def_special BattleTowerUtil, retired=TRUE
	def_special SetBattleTowerParty, retired=TRUE
	def_special SaveBattleTowerProgress, retired=TRUE
	def_special BattleTower_SoftReset, retired=TRUE
	def_special DetermineBattleTowerPrize, retired=TRUE
	def_special GiveBattleTowerPrize, retired=TRUE
	def_special AwardBattleTowerRibbons, retired=TRUE
	def_special ChooseBattleTowerPlayerParty, retired=TRUE
	def_special ValidateEReaderTrainer
	def_special NullFieldSpecial
	def_special ReducePlayerPartyToSelectedMons
	def_special BedroomPC, retired=TRUE
	def_special PlayerPC, retired=TRUE
	def_special ShowTownMap
	def_special GetInGameTradeSpeciesInfo
	def_special CreateInGameTradePokemon
	def_special DoInGameTradeScene
	def_special GetTradeSpecies
	def_special NullFieldSpecial  @ Misc Hoenn specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special CreatePCMenu, retired=TRUE
	def_special HallOfFamePCBeginFade
	def_special ShowDiploma, retired=TRUE
	def_special NullFieldSpecial  @ Check lead mon Contest strength specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special LookThroughPorthole
	def_special DoSoftReset
	def_special EnterHallOfFame
	def_special AnimateElevator
	def_special NullFieldSpecial  @ ShowGlassWorkshopMenu
	def_special SpawnCameraObject
	def_special RemoveCameraObject
	def_special NullFieldSpecial  @ Misc Hoenn specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special BufferEReaderTrainerName
	def_special GetRandomSlotMachineId
	def_special GetPlayerFacingDirection, requests_effects=TRUE
	def_special NullFieldSpecial  @ Abandoned Ship room key specials
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special LeadMonHasEffortRibbon
	def_special GiveLeadMonEffortRibbon
	def_special AreLeadMonEVsMaxedOut
	def_special Script_FacePlayer
	def_special Script_ClearHeldMovement
	def_special InitRoamer, retired=TRUE
	def_special NullFieldSpecial
	def_special PlayerHasGrassPokemonInParty
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special IsStarterFirstStageInParty
	def_special NullFieldSpecial
	def_special IsThereRoomInAnyBoxForMorePokemon
	def_special NullFieldSpecial
	def_special DrawElevatorCurrentFloorWindow
	def_special NullFieldSpecial
	def_special IsPokerusInParty
	def_special SetIcefallCaveCrackedIceMetatiles
	def_special ShakeScreen
	def_special StartGroudonKyogreBattle
	def_special BattleSetup_StartLegendaryBattle
	def_special StartRegiBattle
	def_special SetUpTrainerMovement
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special StartDroughtWeatherBlend
	def_special DoDiveWarp
	def_special DoFallWarp
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special SetEReaderTrainerGfxId
	def_special BattleSetup_StartLatiBattle
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special ScriptGetPartyMonSpecies
	def_special IsSelectedMonEgg
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special LoadPlayerBag
	def_special Script_FadeOutMapMusic
	def_special NullFieldSpecial
	def_special NullFieldSpecial
	def_special HasAllKantoMons
	def_special IsMonOTNameNotPlayers
	def_special NullFieldSpecial
	def_special Dummy_TryEnableBravoTrainerBattleTower, retired=TRUE
	def_special DoesPartyHaveEnigmaBerry
	def_special DoSpecialTrainerBattle
	def_special SetPostgameFlags
	def_special StartMarowakBattle
	def_special ForcePlayerOntoBike
	def_special ListMenu
	def_special ReturnToListMenu
	def_special DoPicboxCancel
	def_special SetVermilionTrashCans
	def_special SeafoamIslandsB4F_CurrentDumpsPlayerOnLand
	def_special SampleResortGorgeousMonAndReward
	def_special CheckAddCoins
	def_special GetDaycarePokemonCount
	def_special CloseElevatorCurrentFloorWindow
	def_special ForcePlayerToStartSurfing
	def_special GetStarterSpecies
	def_special SetSeenMon
	def_special VsSeekerResetObjectMovementAfterChargeComplete
	def_special ShouldShowBoxWasFullMessage
	def_special ChangeBoxPokemonNickname
	def_special UpdateTrainerCardPhotoIcons
	def_special StickerManGetBragFlags
	def_special SetUsedPkmnCenterQuestLogEvent
	def_special IsWirelessAdapterConnected, retired=TRUE
	def_special TryBecomeLinkLeader, retired=TRUE
	def_special TryJoinLinkGroup, retired=TRUE
	def_special RunUnionRoom, retired=TRUE
	def_special ShowWirelessCommunicationScreen, retired=TRUE
	def_special EnableNationalPokedex
	def_special SetWalkingIntoSignVars
	def_special DisableMsgBoxWalkaway
	def_special VsSeekerFreezeObjectsAfterChargeComplete
	def_special SetFlavorTextFlagFromSpecialVars
	def_special UpdatePickStateFromSpecialVar8005
	def_special OverworldWhiteOutGetMoneyLoss
	def_special PutMonInRoute5Daycare
	def_special GetCostToWithdrawRoute5DaycareMon
	def_special IsThereMonInRoute5Daycare
	def_special GetNumLevelsGainedForRoute5DaycareMon
	def_special TakePokemonFromRoute5Daycare
	def_special DoSeagallopFerryScene
	def_special DoesPlayerPartyContainSpecies
	def_special Script_SetHelpContext
	def_special BackupHelpContext
	def_special RestoreHelpContext
	def_special ValidateSavedWonderCard
	def_special SetUnlockedPokedexFlags
	def_special InitUnionRoom, retired=TRUE
	def_special BufferUnionRoomPlayerName, retired=TRUE
	def_special QuestLog_StartRecordingInputsAfterDeferredEvent
	def_special GetMartClerkObjectId
	def_special GetMysteryGiftCardStat
	def_special GetQuestLogState
	def_special QuestLog_CutRecording
	def_special WonderNews_GetRewardInfo
	def_special GetPCBoxToSendMon
	def_special OpenMuseumFossilPic
	def_special CloseMuseumFossilPic
	def_special ChooseMonForMoveTutor
	def_special ChooseMonForWirelessMinigame, retired=TRUE
	def_special SetBattledTrainerFlag
	def_special SetHelpContextForMap
	def_special DoSSAnneDepartureCutscene
	def_special IsPokemonJumpSpeciesInParty, retired=TRUE
	def_special IsNationalPokedexEnabled
	def_special CallTrainerTowerFunc, retired=TRUE
	def_special ShowPokemonJumpRecords, retired=TRUE
	def_special BufferTMHMMoveName
	def_special DaisyMassageServices
	def_special HelpSystem_Disable
	def_special HelpSystem_Enable
	def_special SetPostgameFlags
	def_special HasAtLeastOneBerry
	def_special DisplayBerryPowderVendorMenu
	def_special RemoveBerryPowderVendorMenu
	def_special Script_HasEnoughBerryPowder
	def_special Script_TakeBerryPowder
	def_special PrintPlayerBerryPowderAmount
	def_special DoPokemonLeagueLightingEffect
	def_special ShowBerryCrushRankings, retired=TRUE
	def_special CapeBrinkGetMoveToTeachLeadPokemon
	def_special HasLearnedAllMovesFromCapeBrinkTutor
	def_special DoCredits
	def_special ShowDodrioBerryPickingRecords, retired=TRUE
	def_special DrawSeagallopDestinationMenu
	def_special GetSelectedSeagallopDestination
	def_special GetSeagallopNumber
	def_special GetPlayerFacingDirection, requests_effects=TRUE
	def_special DoDeoxysTriangleInteraction
	def_special SetDeoxysTrianglePalette
	def_special IsPlayerLeftOfVermilionSailor
	def_special IsBadEggInParty
	def_special ReadTrainerTowerAndValidate, retired=TRUE
	def_special HasAllMons
	def_special IsPlayerNotInTrainerTowerLobby, retired=TRUE
	def_special BrailleCursorToggle
	def_special Script_ResetUnionRoomTrade, retired=TRUE
	def_special PlayerPartyContainsSpeciesWithPlayerID
	def_special AnimateTeleporterHousing
	def_special IsDodrioInParty, retired=TRUE
	def_special AnimateTeleporterCable
	def_special InitElevatorFloorSelectMenuPos
	def_special UpdateLoreleiDollCollection
	def_special LoopWingFlapSound
	def_special CreateEnemyEventMon
	def_special GetNumberSprayStrength
	def_special GetSprayId
	def_special GetLastUsedSprayType
	def_special TrySkyBattle
	def_special TryPrepareSecondApproachingTrainer
	def_special OpenPokeGlassPokedex
	def_special OpenPokeGlassMap
	def_special OpenPokeGlassParty
	def_special OpenPokeGlassStats
	def_special StartPokeGlassIntro
	def_special OpenPokeGlassWardrobe
	def_special OpenPokeGlassStorage
gSpecialsEnd::
