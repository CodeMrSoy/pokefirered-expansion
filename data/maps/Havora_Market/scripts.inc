Havora_Market_MapScripts::
	.byte 0

Havora_Market_Guide::
	msgbox Havora_Market_Guide_Text, MSGBOX_NPC
	end

Havora_Market_Guide_Text::
	.string "This is HAVORA's market district!\nHomes north, shops and harbor south.$"

Havora_Market_Resident::
	msgbox Havora_Market_Resident_Text, MSGBOX_NPC
	end

Havora_Market_Resident_Text::
	.string "The flower beds soften all this stone.\nI love living near the waterfront.$"

Havora_Market_Harbor::
	msgbox Havora_Market_Harbor_Text, MSGBOX_NPC
	end

Havora_Market_Harbor_Text::
	.string "The ferry pier is just south of here.\nYou can walk straight to the harbor.$"

Havora_Market_Fisher::
	msgbox Havora_Market_Fisher_Text, MSGBOX_NPC
	end

Havora_Market_Fisher_Text::
	.string "Fresh fish arrive with the morning tide.\nThe market never stays quiet for long.$"

Havora_Market_Supplies::
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_Stock::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_NONE

Havora_Market_MarketCustomer::
	msgbox Havora_Market_MarketCustomer_Text, MSGBOX_NPC
	end

Havora_Market_MarketCustomer_Text::
	.string "A gift from HAVORA for my family.\nWhich stall would you choose?$"

Havora_Market_MarketTraveler::
	msgbox Havora_Market_MarketTraveler_Text, MSGBOX_NPC
	end

Havora_Market_MarketTraveler_Text::
	.string "The houses climb right up the cliffs.\nI have never seen a port like it.$"
Havora_Market_HealingBerries::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_HealingBerries_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_HealingBerries_Stock::
	.2byte ITEM_ORAN_BERRY
	.2byte ITEM_SITRUS_BERRY
	.2byte ITEM_CHERI_BERRY
	.2byte ITEM_CHESTO_BERRY
	.2byte ITEM_PECHA_BERRY
	.2byte ITEM_RAWST_BERRY
	.2byte ITEM_ASPEAR_BERRY
	.2byte ITEM_PERSIM_BERRY
	.2byte ITEM_LUM_BERRY
	.2byte ITEM_LEPPA_BERRY
	.2byte ITEM_NONE

Havora_Market_Medicine::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_Medicine_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_Medicine_Stock::
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_REVIVE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_NONE

Havora_Market_Refreshments::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_Refreshments_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_Refreshments_Stock::
	.2byte ITEM_FRESH_WATER
	.2byte ITEM_SODA_POP
	.2byte ITEM_LEMONADE
	.2byte ITEM_MOOMOO_MILK
	.2byte ITEM_BERRY_JUICE
	.2byte ITEM_LAVA_COOKIE
	.2byte ITEM_OLD_GATEAU
	.2byte ITEM_CASTELIACONE
	.2byte ITEM_BIG_MALASADA
	.2byte ITEM_NONE

Havora_Market_FriendshipBerries::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_FriendshipBerries_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_FriendshipBerries_Stock::
	.2byte ITEM_POMEG_BERRY
	.2byte ITEM_KELPSY_BERRY
	.2byte ITEM_QUALOT_BERRY
	.2byte ITEM_HONDEW_BERRY
	.2byte ITEM_GREPA_BERRY
	.2byte ITEM_TAMATO_BERRY
	.2byte ITEM_NONE

Havora_Market_ResistanceBerries::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_ResistanceBerries_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_ResistanceBerries_Stock::
	.2byte ITEM_OCCA_BERRY
	.2byte ITEM_PASSHO_BERRY
	.2byte ITEM_WACAN_BERRY
	.2byte ITEM_RINDO_BERRY
	.2byte ITEM_YACHE_BERRY
	.2byte ITEM_CHOPLE_BERRY
	.2byte ITEM_KEBIA_BERRY
	.2byte ITEM_SHUCA_BERRY
	.2byte ITEM_COBA_BERRY
	.2byte ITEM_PAYAPA_BERRY
	.2byte ITEM_TANGA_BERRY
	.2byte ITEM_CHARTI_BERRY
	.2byte ITEM_KASIB_BERRY
	.2byte ITEM_HABAN_BERRY
	.2byte ITEM_COLBUR_BERRY
	.2byte ITEM_BABIRI_BERRY
	.2byte ITEM_CHILAN_BERRY
	.2byte ITEM_ROSELI_BERRY
	.2byte ITEM_NONE

Havora_Market_BattleBerries::
	goto_if_questlog EventScript_ReleaseEnd
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart Havora_Market_BattleBerries_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
Havora_Market_BattleBerries_Stock::
	.2byte ITEM_FIGY_BERRY
	.2byte ITEM_WIKI_BERRY
	.2byte ITEM_MAGO_BERRY
	.2byte ITEM_AGUAV_BERRY
	.2byte ITEM_IAPAPA_BERRY
	.2byte ITEM_LIECHI_BERRY
	.2byte ITEM_GANLON_BERRY
	.2byte ITEM_SALAC_BERRY
	.2byte ITEM_PETAYA_BERRY
	.2byte ITEM_APICOT_BERRY
	.2byte ITEM_NONE

Havora_Market_SoldOut::
	msgbox Havora_Market_SoldOut_Text, MSGBOX_NPC
	end

Havora_Market_SoldOut_Text::
	.string "Sold out for today!\nThe next shipment is still at sea.$"

Havora_Market_Meteorite::
	lock
	faceplayer
	checkitem ITEM_METEORITE
	goto_if_eq VAR_RESULT, TRUE, Havora_Market_MeteoriteOwned
	msgbox Havora_Market_MeteoriteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Havora_Market_MeteoriteEnd
	checkmoney 10000
	goto_if_eq VAR_RESULT, FALSE, Havora_Market_MeteoriteNoMoney
	checkitemspace ITEM_METEORITE
	goto_if_eq VAR_RESULT, FALSE, Havora_Market_MeteoriteNoRoom
	additem ITEM_METEORITE
	goto_if_eq VAR_RESULT, FALSE, Havora_Market_MeteoriteNoRoom
	removemoney 10000
	msgbox Havora_Market_MeteoriteBought
	goto Havora_Market_MeteoriteEnd
Havora_Market_MeteoriteOwned::
	msgbox Havora_Market_MeteoriteOwnedText
	goto Havora_Market_MeteoriteEnd
Havora_Market_MeteoriteNoMoney::
	msgbox Havora_Market_MeteoriteNoMoneyText
	goto Havora_Market_MeteoriteEnd
Havora_Market_MeteoriteNoRoom::
	msgbox Havora_Market_MeteoriteNoRoomText
	goto Havora_Market_MeteoriteEnd
Havora_Market_MeteoriteEnd::
	release
	end
Havora_Market_MeteoriteOffer::
	.string "A genuine METEORITE! It can\nchange DEOXYS's form.\pIt costs ¥10,000.\nWould you like to buy it?$"
Havora_Market_MeteoriteBought::
	.string "The METEORITE is yours!\nYou can use it more than once.$"
Havora_Market_MeteoriteOwnedText::
	.string "You already have a METEORITE.\nOne will do the job!$"
Havora_Market_MeteoriteNoMoneyText::
	.string "You don't have enough money.$"
Havora_Market_MeteoriteNoRoomText::
	.string "Make room in your BAG first.$"

EventScript_HavoraDoorLocked::
	lockall
	msgbox Havora_DoorLocked_Text
	releaseall
	end
Havora_DoorLocked_Text::
	.string "It's locked.$"

Havora_Market_WalkingResident1::
	msgbox Havora_Market_WalkingResident1_Text, MSGBOX_NPC
	end
Havora_Market_WalkingResident1_Text::
	.string "I came for a bottle of milk.\nSomehow I bought berries\nfor the whole week too.$"

Havora_Market_WalkingResident2::
	msgbox Havora_Market_WalkingResident2_Text, MSGBOX_NPC
	end
Havora_Market_WalkingResident2_Text::
	.string "My partner knows every stall.\nI just follow the smell\nof something good to eat.$"
