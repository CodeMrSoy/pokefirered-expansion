VidraDraft_EnterForest::
	lockall
	warp MAP_VIDRA_DRAFT_WESTERNFOREST, 255, 80, 74
	waitstate
	releaseall
	end

VidraDraft_WesternForest_MapScripts::
	.byte 0

VidraDraft_WesternForest_Sign0::
	msgbox VidraDraft_WesternForest_Sign0_Text, MSGBOX_SIGN
	end

VidraDraft_WesternForest_Sign0_Text::
	.string "HAVORA lies beyond the grove.\nThe forest splits farther inside.$"

VidraDraft_WesternForest_Sign1::
	msgbox VidraDraft_WesternForest_Sign1_Text, MSGBOX_SIGN
	end

VidraDraft_WesternForest_Sign1_Text::
	.string "WEST: CORVALA PASSAGE\nNORTH: RAINFALL ROUTE$"

VidraDraft_WesternForest_Travel0::
	lockall
	warp MAP_HAVORA_NORTH_QUADRANT, 255, 10, 12
	waitstate
	releaseall
	end

VidraDraft_CorvalaPassage_MapScripts::
	.byte 0


VidraDraft_RainfallRoute_MapScripts::
	.byte 0

VidraDraft_RainfallRoute_Sign0::
	msgbox VidraDraft_RainfallRoute_Sign0_Text, MSGBOX_SIGN
	end

VidraDraft_RainfallRoute_Sign0_Text::
	.string "RAINFALL ROUTE\nNorth to VEYDEN.$"

VidraDraft_Veyden_MapScripts::
	.byte 0

VidraDraft_Veyden_Door0::
	msgbox VidraDraft_Veyden_Door0_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door0_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Veyden_Door1::
	msgbox VidraDraft_Veyden_Door1_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door1_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Veyden_Door2::
	msgbox VidraDraft_Veyden_Door2_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door2_Text::
	.string "POKEMON CENTER site.\nInterior planned for the next pass.$"

VidraDraft_Veyden_Door3::
	msgbox VidraDraft_Veyden_Door3_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door3_Text::
	.string "MART site.\nInterior planned for the next pass.$"

VidraDraft_Veyden_Door4::
	msgbox VidraDraft_Veyden_Door4_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door4_Text::
	.string "GYM site.\nPuzzle and leader come later.$"

VidraDraft_Veyden_Door5::
	msgbox VidraDraft_Veyden_Door5_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door5_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Veyden_Door6::
	msgbox VidraDraft_Veyden_Door6_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Door6_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Veyden_Sign7::
	msgbox VidraDraft_Veyden_Sign7_Text, MSGBOX_SIGN
	end

VidraDraft_Veyden_Sign7_Text::
	.string "VEYDEN\nEast: LYRVIK / North: NORVYN$"

VidraDraft_LakewoodRoute_MapScripts::
	.byte 0

VidraDraft_LakewoodRoute_Sign0::
	msgbox VidraDraft_LakewoodRoute_Sign0_Text, MSGBOX_SIGN
	end

VidraDraft_LakewoodRoute_Sign0_Text::
	.string "WEST: VEYDEN\nEAST: LYRVIK$"

VidraDraft_Lyrvik_MapScripts::
	.byte 0

VidraDraft_Lyrvik_Door0::
	msgbox VidraDraft_Lyrvik_Door0_Text, MSGBOX_SIGN
	end

VidraDraft_Lyrvik_Door0_Text::
	.string "POKEMON CENTER site.\nInterior planned for the next pass.$"

VidraDraft_Lyrvik_Door1::
	msgbox VidraDraft_Lyrvik_Door1_Text, MSGBOX_SIGN
	end

VidraDraft_Lyrvik_Door1_Text::
	.string "MART site.\nInterior planned for the next pass.$"

VidraDraft_Lyrvik_Door2::
	msgbox VidraDraft_Lyrvik_Door2_Text, MSGBOX_SIGN
	end

VidraDraft_Lyrvik_Door2_Text::
	.string "GYM site.\nPuzzle and leader come later.$"

VidraDraft_Lyrvik_Door3::
	msgbox VidraDraft_Lyrvik_Door3_Text, MSGBOX_SIGN
	end

VidraDraft_Lyrvik_Door3_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Lyrvik_Door4::
	msgbox VidraDraft_Lyrvik_Door4_Text, MSGBOX_SIGN
	end

VidraDraft_Lyrvik_Door4_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Lyrvik_Sign5::
	msgbox VidraDraft_Lyrvik_Sign5_Text, MSGBOX_SIGN
	end

VidraDraft_Lyrvik_Sign5_Text::
	.string "LYRVIK TOWN\nA quiet home beside the lake.$"

VidraDraft_HighlandAscent_MapScripts::
	.byte 0

VidraDraft_HighlandAscent_Sign0::
	msgbox VidraDraft_HighlandAscent_Sign0_Text, MSGBOX_SIGN
	end

VidraDraft_HighlandAscent_Sign0_Text::
	.string "HIGHLAND ASCENT\nThe trail climbs toward NORVYN.$"

VidraDraft_Norvyn_MapScripts::
	.byte 0

VidraDraft_Norvyn_Door0::
	msgbox VidraDraft_Norvyn_Door0_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door0_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Norvyn_Door1::
	msgbox VidraDraft_Norvyn_Door1_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door1_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Norvyn_Door2::
	msgbox VidraDraft_Norvyn_Door2_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door2_Text::
	.string "GYM site.\nPuzzle and leader come later.$"

VidraDraft_Norvyn_Door3::
	msgbox VidraDraft_Norvyn_Door3_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door3_Text::
	.string "POKEMON CENTER site.\nInterior planned for the next pass.$"

VidraDraft_Norvyn_Door4::
	msgbox VidraDraft_Norvyn_Door4_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door4_Text::
	.string "MART site.\nInterior planned for the next pass.$"

VidraDraft_Norvyn_Door5::
	msgbox VidraDraft_Norvyn_Door5_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door5_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Norvyn_Door6::
	msgbox VidraDraft_Norvyn_Door6_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Door6_Text::
	.string "A village home.\nInterior planned for the next pass.$"

VidraDraft_Norvyn_Sign7::
	msgbox VidraDraft_Norvyn_Sign7_Text, MSGBOX_SIGN
	end

VidraDraft_Norvyn_Sign7_Text::
	.string "NORVYN TOWN\nShelter beneath the frozen peaks.$"

VidraDraft_Corvala_MapScripts::
	.byte 0
