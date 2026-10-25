//
// DO NOT MODIFY THIS FILE! It is auto-generated from src/data/trainers.party
//
// If you want to modify this file set COMPETITIVE_PARTY_SYNTAX to FALSE
// in include/config/general.h and remove this notice.
// Use sed -i '/^#line/d' 'src/data/trainers.h' to remove #line markers.
//

#line 1 "src/data/trainers.party"

#line 1
    [DIFFICULTY_NORMAL][TRAINER_NONE] =
    {
#line 2
        .trainerName = _("PH"),
#line 3
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER_1,
#line 4
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 6
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 7
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
        .partySize = 0,
        .party = (const struct TrainerMon[])
        {
        },
    },
#line 9
    [DIFFICULTY_NORMAL][TRAINER_AQUA_LEADER] =
    {
#line 10
        .trainerName = _("PH"),
#line 11
        .trainerClass = TRAINER_CLASS_AQUA_LEADER,
#line 12
        .trainerPic = TRAINER_PIC_AQUA_LEADER_ARCHIE,
        .encounterMusic_gender =
#line 14
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 15
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 16
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 18
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 20
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 19
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 22
    [DIFFICULTY_NORMAL][TRAINER_AQUA_GRUNT_M] =
    {
#line 23
        .trainerName = _("PH"),
#line 24
        .trainerClass = TRAINER_CLASS_TEAM_AQUA,
#line 25
        .trainerPic = TRAINER_PIC_AQUA_GRUNT_M,
        .encounterMusic_gender =
#line 27
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 28
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 29
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 31
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 33
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 32
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 35
    [DIFFICULTY_NORMAL][TRAINER_AQUA_GRUNT_F] =
    {
#line 36
        .trainerName = _("PH"),
#line 37
        .trainerClass = TRAINER_CLASS_TEAM_AQUA,
#line 38
        .trainerPic = TRAINER_PIC_AQUA_GRUNT_F,
        .encounterMusic_gender =
#line 40
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 41
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 42
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 44
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 46
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 45
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 48
    [DIFFICULTY_NORMAL][TRAINER_RS_AROMA_LADY] =
    {
#line 49
        .trainerName = _("PH"),
#line 50
        .trainerClass = TRAINER_CLASS_RS_AROMA_LADY,
#line 51
        .trainerPic = TRAINER_PIC_RS_AROMA_LADY,
        .encounterMusic_gender =
#line 53
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 54
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 55
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 57
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 59
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 58
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 61
    [DIFFICULTY_NORMAL][TRAINER_RS_RUIN_MANIAC] =
    {
#line 62
        .trainerName = _("PH"),
#line 63
        .trainerClass = TRAINER_CLASS_RS_RUIN_MANIAC,
#line 64
        .trainerPic = TRAINER_PIC_RS_RUIN_MANIAC,
        .encounterMusic_gender =
#line 66
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 67
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 68
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 70
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 72
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 71
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 74
    [DIFFICULTY_NORMAL][TRAINER_INTERVIEWER] =
    {
#line 75
        .trainerName = _("PH"),
#line 76
        .trainerClass = TRAINER_CLASS_INTERVIEWER,
#line 77
        .trainerPic = TRAINER_PIC_INTERVIEWER,
        .encounterMusic_gender =
#line 79
            TRAINER_ENCOUNTER_MUSIC_INTERVIEWER,
#line 80
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 81
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 83
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 85
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 84
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 87
    [DIFFICULTY_NORMAL][TRAINER_RS_TUBER_F] =
    {
#line 88
        .trainerName = _("PH"),
#line 89
        .trainerClass = TRAINER_CLASS_RS_TUBER_F,
#line 90
        .trainerPic = TRAINER_PIC_RS_TUBER_F,
        .encounterMusic_gender =
#line 92
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 93
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 94
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 96
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 98
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 97
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 100
    [DIFFICULTY_NORMAL][TRAINER_RS_TUBER_M] =
    {
#line 101
        .trainerName = _("PH"),
#line 102
        .trainerClass = TRAINER_CLASS_RS_TUBER_M,
#line 103
        .trainerPic = TRAINER_PIC_RS_TUBER_M,
        .encounterMusic_gender =
#line 105
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 106
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 107
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 109
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 111
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 110
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 113
    [DIFFICULTY_NORMAL][TRAINER_RS_COOLTRAINER_M] =
    {
#line 114
        .trainerName = _("PH"),
#line 115
        .trainerClass = TRAINER_CLASS_RS_COOLTRAINER,
#line 116
        .trainerPic = TRAINER_PIC_RS_COOLTRAINER_M,
        .encounterMusic_gender =
#line 118
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 119
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 120
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 122
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 124
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 123
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 126
    [DIFFICULTY_NORMAL][TRAINER_RS_COOLTRAINER_F] =
    {
#line 127
        .trainerName = _("PH"),
#line 128
        .trainerClass = TRAINER_CLASS_RS_COOLTRAINER,
#line 129
        .trainerPic = TRAINER_PIC_RS_COOLTRAINER_F,
        .encounterMusic_gender =
#line 131
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 132
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 133
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 135
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 137
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 136
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 139
    [DIFFICULTY_NORMAL][TRAINER_HEX_MANIAC] =
    {
#line 140
        .trainerName = _("PH"),
#line 141
        .trainerClass = TRAINER_CLASS_HEX_MANIAC,
#line 142
        .trainerPic = TRAINER_PIC_HEX_MANIAC,
        .encounterMusic_gender =
#line 144
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 145
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 146
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 148
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 150
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 149
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 152
    [DIFFICULTY_NORMAL][TRAINER_RS_LADY] =
    {
#line 153
        .trainerName = _("PH"),
#line 154
        .trainerClass = TRAINER_CLASS_RS_LADY,
#line 155
        .trainerPic = TRAINER_PIC_RS_LADY,
        .encounterMusic_gender =
#line 157
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 158
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 159
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 161
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 163
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 162
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 165
    [DIFFICULTY_NORMAL][TRAINER_RS_BEAUTY] =
    {
#line 166
        .trainerName = _("PH"),
#line 167
        .trainerClass = TRAINER_CLASS_RS_BEAUTY,
#line 168
        .trainerPic = TRAINER_PIC_RS_BEAUTY,
        .encounterMusic_gender =
#line 170
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 171
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 172
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 174
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 176
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 175
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 178
    [DIFFICULTY_NORMAL][TRAINER_RICH_BOY] =
    {
#line 179
        .trainerName = _("PH"),
#line 180
        .trainerClass = TRAINER_CLASS_RICH_BOY,
#line 181
        .trainerPic = TRAINER_PIC_RICH_BOY,
        .encounterMusic_gender =
#line 183
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 184
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 185
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 187
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 189
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 188
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 191
    [DIFFICULTY_NORMAL][TRAINER_RS_POKEMANIAC] =
    {
#line 192
        .trainerName = _("PH"),
#line 193
        .trainerClass = TRAINER_CLASS_RS_POKEMANIAC,
#line 194
        .trainerPic = TRAINER_PIC_RS_POKEMANIAC,
        .encounterMusic_gender =
#line 196
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 197
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 198
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 200
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 202
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 201
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 204
    [DIFFICULTY_NORMAL][TRAINER_RS_SWIMMER_M] =
    {
#line 205
        .trainerName = _("PH"),
#line 206
        .trainerClass = TRAINER_CLASS_RS_SWIMMER_M,
#line 207
        .trainerPic = TRAINER_PIC_RS_SWIMMER_M,
        .encounterMusic_gender =
#line 209
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 210
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 211
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 213
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 215
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 214
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 217
    [DIFFICULTY_NORMAL][TRAINER_RS_BLACK_BELT] =
    {
#line 218
        .trainerName = _("PH"),
#line 219
        .trainerClass = TRAINER_CLASS_RS_BLACK_BELT,
#line 220
        .trainerPic = TRAINER_PIC_RS_BLACK_BELT,
        .encounterMusic_gender =
#line 222
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 223
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 224
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 226
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 228
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 227
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 230
    [DIFFICULTY_NORMAL][TRAINER_GUITARIST] =
    {
#line 231
        .trainerName = _("PH"),
#line 232
        .trainerClass = TRAINER_CLASS_GUITARIST,
#line 233
        .trainerPic = TRAINER_PIC_GUITARIST,
        .encounterMusic_gender =
#line 235
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 236
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 237
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 239
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 241
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 240
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 243
    [DIFFICULTY_NORMAL][TRAINER_KINDLER] =
    {
#line 244
        .trainerName = _("PH"),
#line 245
        .trainerClass = TRAINER_CLASS_KINDLER,
#line 246
        .trainerPic = TRAINER_PIC_KINDLER,
        .encounterMusic_gender =
#line 248
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 249
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 250
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 252
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 254
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 253
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 256
    [DIFFICULTY_NORMAL][TRAINER_RS_CAMPER] =
    {
#line 257
        .trainerName = _("PH"),
#line 258
        .trainerClass = TRAINER_CLASS_RS_CAMPER,
#line 259
        .trainerPic = TRAINER_PIC_RS_CAMPER,
        .encounterMusic_gender =
#line 261
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 262
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 263
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 265
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 267
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 266
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 269
    [DIFFICULTY_NORMAL][TRAINER_BUG_MANIAC] =
    {
#line 270
        .trainerName = _("PH"),
#line 271
        .trainerClass = TRAINER_CLASS_BUG_MANIAC,
#line 272
        .trainerPic = TRAINER_PIC_BUG_MANIAC,
        .encounterMusic_gender =
#line 274
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 275
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 276
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 278
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 280
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 279
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 282
    [DIFFICULTY_NORMAL][TRAINER_RS_PSYCHIC_M] =
    {
#line 283
        .trainerName = _("PH"),
#line 284
        .trainerClass = TRAINER_CLASS_RS_PSYCHIC,
#line 285
        .trainerPic = TRAINER_PIC_RS_PSYCHIC_M,
        .encounterMusic_gender =
#line 287
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 288
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 289
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 291
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 293
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 292
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 295
    [DIFFICULTY_NORMAL][TRAINER_RS_PSYCHIC_F] =
    {
#line 296
        .trainerName = _("PH"),
#line 297
        .trainerClass = TRAINER_CLASS_RS_PSYCHIC,
#line 298
        .trainerPic = TRAINER_PIC_RS_PSYCHIC_F,
        .encounterMusic_gender =
#line 300
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 301
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 302
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 304
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 306
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 305
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 308
    [DIFFICULTY_NORMAL][TRAINER_RS_GENTLEMAN] =
    {
#line 309
        .trainerName = _("PH"),
#line 310
        .trainerClass = TRAINER_CLASS_RS_GENTLEMAN,
#line 311
        .trainerPic = TRAINER_PIC_RS_GENTLEMAN,
        .encounterMusic_gender =
#line 313
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 314
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 315
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 317
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 319
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 318
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 321
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_SIDNEY] =
    {
#line 322
        .trainerName = _("SIDNEY"),
#line 323
        .trainerClass = TRAINER_CLASS_RS_ELITE_FOUR,
#line 324
        .trainerPic = TRAINER_PIC_ELITE_FOUR_SIDNEY,
        .encounterMusic_gender =
#line 326
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 327
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 328
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 330
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 332
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 331
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 334
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_PHOEBE] =
    {
#line 335
        .trainerName = _("PHOEBE"),
#line 336
        .trainerClass = TRAINER_CLASS_RS_ELITE_FOUR,
#line 337
        .trainerPic = TRAINER_PIC_ELITE_FOUR_PHOEBE,
        .encounterMusic_gender =
#line 339
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 340
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 341
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 343
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 345
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 344
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 347
    [DIFFICULTY_NORMAL][TRAINER_LEADER_ROXANNE] =
    {
#line 348
        .trainerName = _("ROXANNE"),
#line 349
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 350
        .trainerPic = TRAINER_PIC_LEADER_ROXANNE,
        .encounterMusic_gender =
#line 352
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 353
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 354
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 356
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 358
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 357
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 360
    [DIFFICULTY_NORMAL][TRAINER_LEADER_BRAWLY] =
    {
#line 361
        .trainerName = _("BRAWLY"),
#line 362
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 363
        .trainerPic = TRAINER_PIC_LEADER_BRAWLY,
        .encounterMusic_gender =
#line 365
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 366
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 367
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 369
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 371
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 370
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 373
    [DIFFICULTY_NORMAL][TRAINER_LEADER_TATE_LIZA] =
    {
#line 374
        .trainerName = _("TATE&LIZA"),
#line 375
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 376
        .trainerPic = TRAINER_PIC_LEADER_TATE_AND_LIZA,
        .encounterMusic_gender =
#line 378
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 379
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 380
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 382
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 384
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 383
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 386
    [DIFFICULTY_NORMAL][TRAINER_SCHOOL_KID_M] =
    {
#line 387
        .trainerName = _("PH"),
#line 388
        .trainerClass = TRAINER_CLASS_SCHOOL_KID,
#line 389
        .trainerPic = TRAINER_PIC_SCHOOL_KID_M,
        .encounterMusic_gender =
#line 391
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 392
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 393
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 395
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 397
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 396
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 399
    [DIFFICULTY_NORMAL][TRAINER_SCHOOL_KID_F] =
    {
#line 400
        .trainerName = _("PH"),
#line 401
        .trainerClass = TRAINER_CLASS_SCHOOL_KID,
#line 402
        .trainerPic = TRAINER_PIC_SCHOOL_KID_F,
        .encounterMusic_gender =
#line 404
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 405
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 406
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 408
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 410
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 409
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 412
    [DIFFICULTY_NORMAL][TRAINER_SR_AND_JR] =
    {
#line 413
        .trainerName = _("PH"),
#line 414
        .trainerClass = TRAINER_CLASS_SR_AND_JR,
#line 415
        .trainerPic = TRAINER_PIC_SR_AND_JR,
        .encounterMusic_gender =
#line 417
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 418
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 419
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 421
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 423
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 422
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 425
    [DIFFICULTY_NORMAL][TRAINER_POKEFAN_M] =
    {
#line 426
        .trainerName = _("PH"),
#line 427
        .trainerClass = TRAINER_CLASS_POKEFAN,
#line 428
        .trainerPic = TRAINER_PIC_POKEFAN_M,
        .encounterMusic_gender =
#line 430
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 431
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 432
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 434
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 436
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 435
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 438
    [DIFFICULTY_NORMAL][TRAINER_POKEFAN_F] =
    {
#line 439
        .trainerName = _("PH"),
#line 440
        .trainerClass = TRAINER_CLASS_POKEFAN,
#line 441
        .trainerPic = TRAINER_PIC_POKEFAN_F,
        .encounterMusic_gender =
#line 443
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 444
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 445
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 447
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 449
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 448
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 451
    [DIFFICULTY_NORMAL][TRAINER_EXPERT_M] =
    {
#line 452
        .trainerName = _("PH"),
#line 453
        .trainerClass = TRAINER_CLASS_EXPERT,
#line 454
        .trainerPic = TRAINER_PIC_EXPERT_M,
        .encounterMusic_gender =
#line 456
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 457
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 458
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 460
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 462
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 461
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 464
    [DIFFICULTY_NORMAL][TRAINER_EXPERT_F] =
    {
#line 465
        .trainerName = _("PH"),
#line 466
        .trainerClass = TRAINER_CLASS_EXPERT,
#line 467
        .trainerPic = TRAINER_PIC_EXPERT_F,
        .encounterMusic_gender =
#line 469
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 470
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 471
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 473
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 475
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 474
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 477
    [DIFFICULTY_NORMAL][TRAINER_RS_YOUNGSTER] =
    {
#line 478
        .trainerName = _("PH"),
#line 479
        .trainerClass = TRAINER_CLASS_RS_YOUNGSTER,
#line 480
        .trainerPic = TRAINER_PIC_RS_YOUNGSTER,
        .encounterMusic_gender =
#line 482
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 483
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 484
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 486
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 488
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 487
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 490
    [DIFFICULTY_NORMAL][TRAINER_RS_CHAMPION] =
    {
#line 491
        .trainerName = _("PH"),
#line 492
        .trainerClass = TRAINER_CLASS_RS_CHAMPION,
#line 493
        .trainerPic = TRAINER_PIC_CHAMPION_STEVEN,
        .encounterMusic_gender =
#line 495
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 496
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 497
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 499
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 501
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 500
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 503
    [DIFFICULTY_NORMAL][TRAINER_RS_FISHERMAN] =
    {
#line 504
        .trainerName = _("PH"),
#line 505
        .trainerClass = TRAINER_CLASS_RS_FISHERMAN,
#line 506
        .trainerPic = TRAINER_PIC_RS_FISHERMAN,
        .encounterMusic_gender =
#line 508
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 509
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 510
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 512
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 514
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 513
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 516
    [DIFFICULTY_NORMAL][TRAINER_CYCLING_TRIATHLETE_M] =
    {
#line 517
        .trainerName = _("PH"),
#line 518
        .trainerClass = TRAINER_CLASS_TRIATHLETE,
#line 519
        .trainerPic = TRAINER_PIC_CYCLING_TRIATHLETE_M,
        .encounterMusic_gender =
#line 521
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 522
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 523
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 525
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 527
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 526
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 529
    [DIFFICULTY_NORMAL][TRAINER_CYCLING_TRIATHLETE_F] =
    {
#line 530
        .trainerName = _("PH"),
#line 531
        .trainerClass = TRAINER_CLASS_TRIATHLETE,
#line 532
        .trainerPic = TRAINER_PIC_CYCLING_TRIATHLETE_F,
        .encounterMusic_gender =
#line 534
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 535
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 536
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 538
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 540
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 539
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 542
    [DIFFICULTY_NORMAL][TRAINER_RUNNING_TRIATHLETE_M] =
    {
#line 543
        .trainerName = _("PH"),
#line 544
        .trainerClass = TRAINER_CLASS_TRIATHLETE,
#line 545
        .trainerPic = TRAINER_PIC_RUNNING_TRIATHLETE_M,
        .encounterMusic_gender =
#line 547
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 548
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 549
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 551
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 553
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 552
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 555
    [DIFFICULTY_NORMAL][TRAINER_RUNNING_TRIATHLETE_F] =
    {
#line 556
        .trainerName = _("PH"),
#line 557
        .trainerClass = TRAINER_CLASS_TRIATHLETE,
#line 558
        .trainerPic = TRAINER_PIC_RUNNING_TRIATHLETE_F,
        .encounterMusic_gender =
#line 560
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 561
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 562
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 564
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 566
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 565
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 568
    [DIFFICULTY_NORMAL][TRAINER_SWIMMING_TRIATHLETE_M] =
    {
#line 569
        .trainerName = _("PH"),
#line 570
        .trainerClass = TRAINER_CLASS_TRIATHLETE,
#line 571
        .trainerPic = TRAINER_PIC_SWIMMING_TRIATHLETE_M,
        .encounterMusic_gender =
#line 573
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 574
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 575
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 577
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 579
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 578
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 581
    [DIFFICULTY_NORMAL][TRAINER_SWIMMING_TRIATHLETE_F] =
    {
#line 582
        .trainerName = _("PH"),
#line 583
        .trainerClass = TRAINER_CLASS_TRIATHLETE,
#line 584
        .trainerPic = TRAINER_PIC_SWIMMING_TRIATHLETE_F,
        .encounterMusic_gender =
#line 586
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 587
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 588
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 590
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 592
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 591
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 594
    [DIFFICULTY_NORMAL][TRAINER_DRAGON_TAMER] =
    {
#line 595
        .trainerName = _("PH"),
#line 596
        .trainerClass = TRAINER_CLASS_DRAGON_TAMER,
#line 597
        .trainerPic = TRAINER_PIC_DRAGON_TAMER,
        .encounterMusic_gender =
#line 599
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 600
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 601
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 603
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 605
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 604
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 607
    [DIFFICULTY_NORMAL][TRAINER_RS_BIRD_KEEPER] =
    {
#line 608
        .trainerName = _("PH"),
#line 609
        .trainerClass = TRAINER_CLASS_RS_BIRD_KEEPER,
#line 610
        .trainerPic = TRAINER_PIC_RS_BIRD_KEEPER,
        .encounterMusic_gender =
#line 612
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 613
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 614
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 616
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 618
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 617
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 620
    [DIFFICULTY_NORMAL][TRAINER_NINJA_BOY] =
    {
#line 621
        .trainerName = _("PH"),
#line 622
        .trainerClass = TRAINER_CLASS_NINJA_BOY,
#line 623
        .trainerPic = TRAINER_PIC_NINJA_BOY,
        .encounterMusic_gender =
#line 625
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 626
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 627
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 629
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 631
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 630
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 633
    [DIFFICULTY_NORMAL][TRAINER_BATTLE_GIRL] =
    {
#line 634
        .trainerName = _("PH"),
#line 635
        .trainerClass = TRAINER_CLASS_BATTLE_GIRL,
#line 636
        .trainerPic = TRAINER_PIC_BATTLE_GIRL,
        .encounterMusic_gender =
#line 638
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 639
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 640
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 642
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 644
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 643
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 646
    [DIFFICULTY_NORMAL][TRAINER_PARASOL_LADY] =
    {
#line 647
        .trainerName = _("PH"),
#line 648
        .trainerClass = TRAINER_CLASS_PARASOL_LADY,
#line 649
        .trainerPic = TRAINER_PIC_PARASOL_LADY,
        .encounterMusic_gender =
#line 651
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 652
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 653
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 655
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 657
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 656
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 659
    [DIFFICULTY_NORMAL][TRAINER_RS_SWIMMER_F] =
    {
#line 660
        .trainerName = _("PH"),
#line 661
        .trainerClass = TRAINER_CLASS_RS_SWIMMER_F,
#line 662
        .trainerPic = TRAINER_PIC_RS_SWIMMER_F,
        .encounterMusic_gender =
#line 664
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 665
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 666
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 668
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 670
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 669
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 672
    [DIFFICULTY_NORMAL][TRAINER_RS_PICNICKER] =
    {
#line 673
        .trainerName = _("PH"),
#line 674
        .trainerClass = TRAINER_CLASS_RS_PICNICKER,
#line 675
        .trainerPic = TRAINER_PIC_RS_PICNICKER,
        .encounterMusic_gender =
#line 677
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 678
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 679
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 681
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 683
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 682
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 685
    [DIFFICULTY_NORMAL][TRAINER_RS_TWINS] =
    {
#line 686
        .trainerName = _("PH"),
#line 687
        .trainerClass = TRAINER_CLASS_RS_TWINS,
#line 688
        .trainerPic = TRAINER_PIC_RS_TWINS,
        .encounterMusic_gender =
#line 690
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 691
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 692
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 694
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 696
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 695
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 698
    [DIFFICULTY_NORMAL][TRAINER_RS_SAILOR] =
    {
#line 699
        .trainerName = _("PH"),
#line 700
        .trainerClass = TRAINER_CLASS_RS_SAILOR,
#line 701
        .trainerPic = TRAINER_PIC_RS_SAILOR,
        .encounterMusic_gender =
#line 703
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 704
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 705
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 707
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 709
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 708
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 711
    [DIFFICULTY_NORMAL][TRAINER_BOARDER_M] =
    {
#line 712
        .trainerName = _("PH"),
#line 713
        .trainerClass = TRAINER_CLASS_BOARDER,
#line 714
        .trainerPic = TRAINER_PIC_RS_YOUNGSTER,
        .encounterMusic_gender =
#line 716
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 717
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 718
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 720
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 722
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 721
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 724
    [DIFFICULTY_NORMAL][TRAINER_BOARDER_F] =
    {
#line 725
        .trainerName = _("PH"),
#line 726
        .trainerClass = TRAINER_CLASS_BOARDER,
#line 727
        .trainerPic = TRAINER_PIC_RS_YOUNGSTER,
        .encounterMusic_gender =
#line 729
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 730
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 731
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 733
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 735
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 734
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 737
    [DIFFICULTY_NORMAL][TRAINER_COLLECTOR] =
    {
#line 738
        .trainerName = _("PH"),
#line 739
        .trainerClass = TRAINER_CLASS_COLLECTOR,
#line 740
        .trainerPic = TRAINER_PIC_COLLECTOR,
        .encounterMusic_gender =
#line 742
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 743
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 744
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 746
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 748
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 747
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 750
    [DIFFICULTY_NORMAL][TRAINER_WALLY] =
    {
#line 751
        .trainerName = _("PH"),
#line 752
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 753
        .trainerPic = TRAINER_PIC_WALLY,
        .encounterMusic_gender =
#line 755
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 756
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 757
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 759
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 761
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 760
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 763
    [DIFFICULTY_NORMAL][TRAINER_BRENDAN] =
    {
#line 764
        .trainerName = _("PH"),
#line 765
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 766
        .trainerPic = TRAINER_PIC_RS_BRENDAN_1,
        .encounterMusic_gender =
#line 768
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 769
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 770
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 772
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 774
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 773
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 776
    [DIFFICULTY_NORMAL][TRAINER_BRENDAN_2] =
    {
#line 777
        .trainerName = _("PH"),
#line 778
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 779
        .trainerPic = TRAINER_PIC_RS_BRENDAN_1,
        .encounterMusic_gender =
#line 781
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 782
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 783
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 785
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 787
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 786
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 789
    [DIFFICULTY_NORMAL][TRAINER_BRENDAN_3] =
    {
#line 790
        .trainerName = _("PH"),
#line 791
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 792
        .trainerPic = TRAINER_PIC_RS_BRENDAN_1,
        .encounterMusic_gender =
#line 794
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 795
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 796
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 798
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 800
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 799
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 802
    [DIFFICULTY_NORMAL][TRAINER_MAY] =
    {
#line 803
        .trainerName = _("PH"),
#line 804
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 805
        .trainerPic = TRAINER_PIC_RS_MAY_1,
        .encounterMusic_gender =
#line 807
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 808
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 809
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 811
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 813
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 812
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 815
    [DIFFICULTY_NORMAL][TRAINER_MAY_2] =
    {
#line 816
        .trainerName = _("PH"),
#line 817
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 818
        .trainerPic = TRAINER_PIC_RS_MAY_1,
        .encounterMusic_gender =
#line 820
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 821
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 822
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 824
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 826
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 825
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 828
    [DIFFICULTY_NORMAL][TRAINER_MAY_3] =
    {
#line 829
        .trainerName = _("PH"),
#line 830
        .trainerClass = TRAINER_CLASS_PKMN_TRAINER,
#line 831
        .trainerPic = TRAINER_PIC_RS_MAY_1,
        .encounterMusic_gender =
#line 833
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 834
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 835
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 837
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 839
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 838
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 841
    [DIFFICULTY_NORMAL][TRAINER_RS_PKMN_BREEDER_M] =
    {
#line 842
        .trainerName = _("PH"),
#line 843
        .trainerClass = TRAINER_CLASS_RS_PKMN_BREEDER,
#line 844
        .trainerPic = TRAINER_PIC_RS_POKEMON_BREEDER_M,
        .encounterMusic_gender =
#line 846
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 847
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 848
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 850
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 852
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 851
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 854
    [DIFFICULTY_NORMAL][TRAINER_RS_PKMN_BREEDER_F] =
    {
#line 855
        .trainerName = _("PH"),
#line 856
        .trainerClass = TRAINER_CLASS_RS_PKMN_BREEDER,
#line 857
        .trainerPic = TRAINER_PIC_RS_POKEMON_BREEDER_F,
        .encounterMusic_gender =
#line 859
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 860
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 861
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 863
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 865
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 864
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 867
    [DIFFICULTY_NORMAL][TRAINER_RS_PKMN_RANGER_M] =
    {
#line 868
        .trainerName = _("PH"),
#line 869
        .trainerClass = TRAINER_CLASS_RS_PKMN_RANGER,
#line 870
        .trainerPic = TRAINER_PIC_RS_POKEMON_RANGER_M,
        .encounterMusic_gender =
#line 872
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 873
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 874
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 876
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 878
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 877
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 880
    [DIFFICULTY_NORMAL][TRAINER_RS_PKMN_RANGER_F] =
    {
#line 881
        .trainerName = _("PH"),
#line 882
        .trainerClass = TRAINER_CLASS_RS_PKMN_RANGER,
#line 883
        .trainerPic = TRAINER_PIC_RS_POKEMON_RANGER_F,
        .encounterMusic_gender =
#line 885
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 886
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 887
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 889
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 891
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 890
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 893
    [DIFFICULTY_NORMAL][TRAINER_MAXIE_MOSSDEEP] =
    {
#line 894
        .trainerName = _("MAXIE"),
#line 895
        .trainerClass = TRAINER_CLASS_MAGMA_LEADER,
#line 896
        .trainerPic = TRAINER_PIC_MAGMA_LEADER_MAXIE,
        .encounterMusic_gender =
#line 898
            TRAINER_ENCOUNTER_MUSIC_MAGMA,
#line 899
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 900
        .aiFlags = AI_FLAG_BASIC_TRAINER,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 902
            .species = SPECIES_MIGHTYENA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 904
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 903
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 906
            .species = SPECIES_CROBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 908
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 907
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 910
            .species = SPECIES_CAMERUPT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 912
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 911
            .lvl = 44,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 914
    [DIFFICULTY_NORMAL][TRAINER_MAGMA_GRUNT_M] =
    {
#line 915
        .trainerName = _("PH"),
#line 916
        .trainerClass = TRAINER_CLASS_TEAM_MAGMA,
#line 917
        .trainerPic = TRAINER_PIC_MAGMA_GRUNT_M,
        .encounterMusic_gender =
#line 919
            TRAINER_ENCOUNTER_MUSIC_MAGMA,
#line 920
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 921
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 923
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 925
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 924
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 927
    [DIFFICULTY_NORMAL][TRAINER_MAMGA_GRUNT_F] =
    {
#line 928
        .trainerName = _("PH"),
#line 929
        .trainerClass = TRAINER_CLASS_TEAM_MAGMA,
#line 930
        .trainerPic = TRAINER_PIC_MAGMA_GRUNT_F,
        .encounterMusic_gender =
#line 932
            TRAINER_ENCOUNTER_MUSIC_MAGMA,
#line 933
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 934
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 936
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 938
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 937
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 940
    [DIFFICULTY_NORMAL][TRAINER_RS_LASS] =
    {
#line 941
        .trainerName = _("PH"),
#line 942
        .trainerClass = TRAINER_CLASS_RS_LASS,
#line 943
        .trainerPic = TRAINER_PIC_RS_LASS,
        .encounterMusic_gender =
#line 945
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 946
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 947
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 949
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 951
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 950
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 953
    [DIFFICULTY_NORMAL][TRAINER_RS_BUG_CATCHER] =
    {
#line 954
        .trainerName = _("PH"),
#line 955
        .trainerClass = TRAINER_CLASS_RS_BUG_CATCHER,
#line 956
        .trainerPic = TRAINER_PIC_RS_BUG_CATCHER,
        .encounterMusic_gender =
#line 958
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 959
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 960
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 962
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 964
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 963
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 966
    [DIFFICULTY_NORMAL][TRAINER_RS_HIKER] =
    {
#line 967
        .trainerName = _("PH"),
#line 968
        .trainerClass = TRAINER_CLASS_RS_HIKER,
#line 969
        .trainerPic = TRAINER_PIC_RS_HIKER,
        .encounterMusic_gender =
#line 971
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 972
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 973
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 975
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 977
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 976
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 979
    [DIFFICULTY_NORMAL][TRAINER_RS_YOUNG_COUPLE] =
    {
#line 980
        .trainerName = _("PH"),
#line 981
        .trainerClass = TRAINER_CLASS_RS_YOUNG_COUPLE,
#line 982
        .trainerPic = TRAINER_PIC_RS_YOUNG_COUPLE,
        .encounterMusic_gender =
#line 984
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 985
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 986
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 988
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 990
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 989
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 992
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 994
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 993
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 996
    [DIFFICULTY_NORMAL][TRAINER_OLD_COUPLE] =
    {
#line 997
        .trainerName = _("PH"),
#line 998
        .trainerClass = TRAINER_CLASS_OLD_COUPLE,
#line 999
        .trainerPic = TRAINER_PIC_OLD_COUPLE,
        .encounterMusic_gender =
#line 1001
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 1002
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 1003
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1005
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1007
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1006
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1009
    [DIFFICULTY_NORMAL][TRAINER_RS_SIS_AND_BRO] =
    {
#line 1010
        .trainerName = _("PH"),
#line 1011
        .trainerClass = TRAINER_CLASS_RS_SIS_AND_BRO,
#line 1012
        .trainerPic = TRAINER_PIC_RS_SIS_AND_BRO,
        .encounterMusic_gender =
#line 1014
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 1015
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 1016
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1018
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1020
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1019
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1022
    [DIFFICULTY_NORMAL][TRAINER_AQUA_ADMIN_MATT] =
    {
#line 1023
        .trainerName = _("MATT"),
#line 1024
        .trainerClass = TRAINER_CLASS_AQUA_ADMIN,
#line 1025
        .trainerPic = TRAINER_PIC_AQUA_ADMIN_M,
        .encounterMusic_gender =
#line 1027
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 1028
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1029
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1031
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1033
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1032
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1035
    [DIFFICULTY_NORMAL][TRAINER_AQUA_ADMIN_SHELLY] =
    {
#line 1036
        .trainerName = _("SHELLY"),
#line 1037
        .trainerClass = TRAINER_CLASS_AQUA_ADMIN,
#line 1038
        .trainerPic = TRAINER_PIC_AQUA_ADMIN_F,
        .encounterMusic_gender =
#line 1040
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 1041
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1042
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1044
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1046
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1045
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1048
    [DIFFICULTY_NORMAL][TRAINER_TABITHA_MOSSDEEP] =
    {
#line 1049
        .trainerName = _("TABITHA"),
#line 1050
        .trainerClass = TRAINER_CLASS_MAGMA_ADMIN,
#line 1051
        .trainerPic = TRAINER_PIC_MAGMA_ADMIN_M,
        .encounterMusic_gender =
#line 1053
            TRAINER_ENCOUNTER_MUSIC_MAGMA,
#line 1054
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1055
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1057
            .species = SPECIES_CAMERUPT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1059
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 1058
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1061
            .species = SPECIES_MIGHTYENA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1063
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 1062
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1065
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1067
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 1066
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1069
    [DIFFICULTY_NORMAL][TRAINER_MAGMA_ADMIN_COURTNEY] =
    {
#line 1070
        .trainerName = _("COURTNEY"),
#line 1071
        .trainerClass = TRAINER_CLASS_MAGMA_ADMIN,
#line 1072
        .trainerPic = TRAINER_PIC_MAGMA_ADMIN_F,
        .encounterMusic_gender =
#line 1074
            TRAINER_ENCOUNTER_MUSIC_MAGMA,
#line 1075
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1076
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1078
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1080
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1079
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1082
    [DIFFICULTY_NORMAL][TRAINER_LEADER_WATTSON] =
    {
#line 1083
        .trainerName = _("WATTSON"),
#line 1084
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 1085
        .trainerPic = TRAINER_PIC_LEADER_WATTSON,
        .encounterMusic_gender =
#line 1087
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1088
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1089
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1091
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1093
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1092
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1095
    [DIFFICULTY_NORMAL][TRAINER_LEADER_FLANNERY] =
    {
#line 1096
        .trainerName = _("FLANNERY"),
#line 1097
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 1098
        .trainerPic = TRAINER_PIC_LEADER_FLANNERY,
        .encounterMusic_gender =
#line 1100
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1101
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1102
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1104
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1106
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1105
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1108
    [DIFFICULTY_NORMAL][TRAINER_LEADER_NORMAN] =
    {
#line 1109
        .trainerName = _("NORMAN"),
#line 1110
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 1111
        .trainerPic = TRAINER_PIC_LEADER_NORMAN,
        .encounterMusic_gender =
#line 1113
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1114
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1115
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1117
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1119
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1118
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1121
    [DIFFICULTY_NORMAL][TRAINER_LEADER_WINONA] =
    {
#line 1122
        .trainerName = _("WINONA"),
#line 1123
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 1124
        .trainerPic = TRAINER_PIC_LEADER_WINONA,
        .encounterMusic_gender =
#line 1126
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1127
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1128
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1130
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1132
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1131
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1134
    [DIFFICULTY_NORMAL][TRAINER_LEADER_WALLACE] =
    {
#line 1135
        .trainerName = _("WALLACE"),
#line 1136
        .trainerClass = TRAINER_CLASS_RS_LEADER,
#line 1137
        .trainerPic = TRAINER_PIC_LEADER_WALLACE,
        .encounterMusic_gender =
#line 1139
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1140
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1141
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1143
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1145
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1144
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1147
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_GLACIA] =
    {
#line 1148
        .trainerName = _("GLACIA"),
#line 1149
        .trainerClass = TRAINER_CLASS_RS_ELITE_FOUR,
#line 1150
        .trainerPic = TRAINER_PIC_ELITE_FOUR_GLACIA,
        .encounterMusic_gender =
#line 1152
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 1153
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1154
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1156
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1158
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1157
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1160
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_DRAKE] =
    {
#line 1161
        .trainerName = _("DRAKE"),
#line 1162
        .trainerClass = TRAINER_CLASS_RS_ELITE_FOUR,
#line 1163
        .trainerPic = TRAINER_PIC_ELITE_FOUR_DRAKE,
        .encounterMusic_gender =
#line 1165
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 1166
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1167
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1169
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1171
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1170
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1173
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_BEN] =
    {
#line 1174
        .trainerName = _("BEN"),
#line 1175
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1176
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1178
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1179
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1180
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1182
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1184
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1183
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1186
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1188
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1187
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1190
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_CALVIN] =
    {
#line 1191
        .trainerName = _("CALVIN"),
#line 1192
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1193
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1195
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1196
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1197
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1199
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1201
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1200
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1203
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_JOSH] =
    {
#line 1204
        .trainerName = _("JOSH"),
#line 1205
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1206
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1208
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1209
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1210
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1212
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1214
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1213
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1216
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1218
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1217
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1220
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1222
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1221
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1224
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_TIMMY] =
    {
#line 1225
        .trainerName = _("TIMMY"),
#line 1226
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1227
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1229
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1230
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1231
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1233
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1235
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1234
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1237
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1239
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1238
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1241
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_JOEY] =
    {
#line 1242
        .trainerName = _("JOEY"),
#line 1243
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1244
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1246
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1247
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1248
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1250
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1252
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1251
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1254
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1256
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1255
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1258
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_DAN] =
    {
#line 1259
        .trainerName = _("DAN"),
#line 1260
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1261
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1263
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1264
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1265
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1267
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1269
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1268
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1271
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_CHAD] =
    {
#line 1272
        .trainerName = _("CHAD"),
#line 1273
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1274
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1276
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1277
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1278
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1280
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1282
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1281
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1284
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1286
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1285
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1288
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_TYLER] =
    {
#line 1289
        .trainerName = _("TYLER"),
#line 1290
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1291
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1293
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1294
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1295
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1297
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1299
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1298
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1301
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_EDDIE] =
    {
#line 1302
        .trainerName = _("EDDIE"),
#line 1303
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1304
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1306
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1307
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1308
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1310
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1312
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1311
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1314
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_DILLON] =
    {
#line 1315
        .trainerName = _("DILLON"),
#line 1316
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1317
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1319
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1320
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1321
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1323
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1325
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1324
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1327
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1329
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1328
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1331
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_YASU] =
    {
#line 1332
        .trainerName = _("YASU"),
#line 1333
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1334
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1336
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1337
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1338
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1340
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1342
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1341
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1344
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1346
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1345
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1348
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1350
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1349
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1352
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_DAVE] =
    {
#line 1353
        .trainerName = _("DAVE"),
#line 1354
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1355
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1357
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1358
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1359
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1361
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1363
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1362
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1365
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1367
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1366
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1369
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_BEN_2] =
    {
#line 1370
        .trainerName = _("BEN"),
#line 1371
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 1372
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 1374
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1375
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1376
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1378
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1380
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 1379
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1382
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1384
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 1383
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1386
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_RICK] =
    {
#line 1387
        .trainerName = _("RICK"),
#line 1388
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1389
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1391
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1392
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1393
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1395
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1397
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1396
            .lvl = 6,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1399
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1401
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1400
            .lvl = 6,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1403
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_DOUG] =
    {
#line 1404
        .trainerName = _("DOUG"),
#line 1405
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1406
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1408
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1409
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1410
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1412
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1414
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1413
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1416
            .species = SPECIES_KAKUNA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1418
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1417
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1420
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1422
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1421
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1424
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_SAMMY] =
    {
#line 1425
        .trainerName = _("SAMMY"),
#line 1426
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1427
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1429
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1430
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1431
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1433
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1435
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1434
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1437
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_COLTON] =
    {
#line 1438
        .trainerName = _("COLTON"),
#line 1439
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1440
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1442
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1443
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1444
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1446
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1448
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1447
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1450
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1452
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1451
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1454
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1456
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1455
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1458
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_GREG] =
    {
#line 1459
        .trainerName = _("GREG"),
#line 1460
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1461
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1463
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1464
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1465
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 1467
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1469
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1468
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1471
            .species = SPECIES_KAKUNA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1473
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1472
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1475
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1477
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1476
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1479
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1481
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1480
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1483
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_JAMES] =
    {
#line 1484
        .trainerName = _("JAMES"),
#line 1485
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1486
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1488
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1489
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1490
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1492
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1494
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1493
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1496
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1498
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1497
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1500
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_KENT] =
    {
#line 1501
        .trainerName = _("KENT"),
#line 1502
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1503
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1505
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1506
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1507
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1509
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1511
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1510
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1513
            .species = SPECIES_KAKUNA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1515
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1514
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1517
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_ROBBY] =
    {
#line 1518
        .trainerName = _("ROBBY"),
#line 1519
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1520
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1522
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1523
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1524
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1526
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1528
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1527
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1530
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1532
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1531
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1534
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1536
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1535
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1538
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_CALE] =
    {
#line 1539
        .trainerName = _("CALE"),
#line 1540
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1541
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1543
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1544
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1545
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 1547
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1549
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1548
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1551
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1553
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1552
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1555
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1557
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1556
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1559
            .species = SPECIES_KAKUNA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1561
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1560
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1563
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_KEIGO] =
    {
#line 1564
        .trainerName = _("KEIGO"),
#line 1565
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1566
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1568
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1569
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1570
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1572
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1574
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1573
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1576
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1578
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1577
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1580
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1582
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1581
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1584
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_ELIJAH] =
    {
#line 1585
        .trainerName = _("ELIJAH"),
#line 1586
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1587
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1589
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1590
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1591
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1593
            .species = SPECIES_BUTTERFREE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1595
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1594
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1597
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_2] =
    {
#line 1598
        .trainerName = _("PH"),
#line 1599
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1600
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1602
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1603
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1604
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1606
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1608
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1607
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1610
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1612
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1611
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1614
            .species = SPECIES_VENONAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1616
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1615
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1618
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_BRENT] =
    {
#line 1619
        .trainerName = _("BRENT"),
#line 1620
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1621
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1623
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1624
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1625
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1627
            .species = SPECIES_BEEDRILL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1629
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1628
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1631
            .species = SPECIES_BEEDRILL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1633
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1632
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1635
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_CONNER] =
    {
#line 1636
        .trainerName = _("CONNER"),
#line 1637
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 1638
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 1640
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1641
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1642
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1644
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1646
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1645
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1648
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1650
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1649
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1652
            .species = SPECIES_VENONAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1654
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1653
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1656
    [DIFFICULTY_NORMAL][TRAINER_LASS_JANICE] =
    {
#line 1657
        .trainerName = _("JANICE"),
#line 1658
        .trainerClass = TRAINER_CLASS_LASS,
#line 1659
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1661
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1662
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1663
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1665
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1667
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1666
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1669
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1671
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1670
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1673
    [DIFFICULTY_NORMAL][TRAINER_LASS_SALLY] =
    {
#line 1674
        .trainerName = _("SALLY"),
#line 1675
        .trainerClass = TRAINER_CLASS_LASS,
#line 1676
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1678
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1679
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1680
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1682
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1684
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1683
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1686
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1688
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1687
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1690
    [DIFFICULTY_NORMAL][TRAINER_LASS_ROBIN] =
    {
#line 1691
        .trainerName = _("ROBIN"),
#line 1692
        .trainerClass = TRAINER_CLASS_LASS,
#line 1693
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1695
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1696
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1697
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1699
            .species = SPECIES_JIGGLYPUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1701
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1700
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1703
    [DIFFICULTY_NORMAL][TRAINER_LASS_CRISSY] =
    {
#line 1704
        .trainerName = _("CRISSY"),
#line 1705
        .trainerClass = TRAINER_CLASS_LASS,
#line 1706
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1708
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1709
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1710
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1712
            .species = SPECIES_PARAS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1714
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1713
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1716
            .species = SPECIES_PARAS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1718
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1717
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1720
            .species = SPECIES_PARASECT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1722
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1721
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1724
    [DIFFICULTY_NORMAL][TRAINER_LASS_MIRIAM] =
    {
#line 1725
        .trainerName = _("MIRIAM"),
#line 1726
        .trainerClass = TRAINER_CLASS_LASS,
#line 1727
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1729
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1730
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1731
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1733
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1735
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1734
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1737
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1739
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1738
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1741
    [DIFFICULTY_NORMAL][TRAINER_LASS_IRIS] =
    {
#line 1742
        .trainerName = _("IRIS"),
#line 1743
        .trainerClass = TRAINER_CLASS_LASS,
#line 1744
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1746
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1747
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1748
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 1750
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1752
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1751
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1754
    [DIFFICULTY_NORMAL][TRAINER_LASS_RELI] =
    {
#line 1755
        .trainerName = _("RELI"),
#line 1756
        .trainerClass = TRAINER_CLASS_LASS,
#line 1757
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1759
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1760
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1761
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1763
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1765
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1764
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1767
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1769
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1768
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1771
    [DIFFICULTY_NORMAL][TRAINER_LASS_ALI] =
    {
#line 1772
        .trainerName = _("ALI"),
#line 1773
        .trainerClass = TRAINER_CLASS_LASS,
#line 1774
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1776
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1777
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1778
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1780
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1782
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1781
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1784
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1786
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1785
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1788
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1790
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1789
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1792
    [DIFFICULTY_NORMAL][TRAINER_LASS_2] =
    {
#line 1793
        .trainerName = _("PH"),
#line 1794
        .trainerClass = TRAINER_CLASS_LASS,
#line 1795
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1797
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1798
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1799
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1801
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1803
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1802
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1805
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1807
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1806
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1809
    [DIFFICULTY_NORMAL][TRAINER_LASS_HALEY] =
    {
#line 1810
        .trainerName = _("HALEY"),
#line 1811
        .trainerClass = TRAINER_CLASS_LASS,
#line 1812
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1814
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1815
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1816
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1818
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1820
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1819
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1822
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1824
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1823
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1826
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1828
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1827
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1830
    [DIFFICULTY_NORMAL][TRAINER_LASS_ANN] =
    {
#line 1831
        .trainerName = _("ANN"),
#line 1832
        .trainerClass = TRAINER_CLASS_LASS,
#line 1833
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1835
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1836
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1837
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1839
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1841
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1840
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1843
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1845
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1844
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1847
    [DIFFICULTY_NORMAL][TRAINER_LASS_DAWN] =
    {
#line 1848
        .trainerName = _("DAWN"),
#line 1849
        .trainerClass = TRAINER_CLASS_LASS,
#line 1850
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1852
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1853
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1854
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1856
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1858
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1857
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1860
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1862
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1861
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1864
    [DIFFICULTY_NORMAL][TRAINER_LASS_PAIGE] =
    {
#line 1865
        .trainerName = _("PAIGE"),
#line 1866
        .trainerClass = TRAINER_CLASS_LASS,
#line 1867
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1869
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1870
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1871
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1873
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1875
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1874
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1877
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1879
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1878
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1881
    [DIFFICULTY_NORMAL][TRAINER_LASS_ANDREA] =
    {
#line 1882
        .trainerName = _("ANDREA"),
#line 1883
        .trainerClass = TRAINER_CLASS_LASS,
#line 1884
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1886
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1887
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1888
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 1890
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1892
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1891
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1894
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1896
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1895
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1898
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1900
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1899
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1902
    [DIFFICULTY_NORMAL][TRAINER_LASS_MEGAN] =
    {
#line 1903
        .trainerName = _("MEGAN"),
#line 1904
        .trainerClass = TRAINER_CLASS_LASS,
#line 1905
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1907
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1908
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1909
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 1911
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1913
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1912
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1915
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1917
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1916
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1919
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1921
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1920
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1923
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1925
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1924
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1927
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1929
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1928
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1931
    [DIFFICULTY_NORMAL][TRAINER_LASS_JULIA] =
    {
#line 1932
        .trainerName = _("JULIA"),
#line 1933
        .trainerClass = TRAINER_CLASS_LASS,
#line 1934
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1936
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1937
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1938
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1940
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1942
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1941
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1944
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1946
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1945
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1948
    [DIFFICULTY_NORMAL][TRAINER_LASS_KAY] =
    {
#line 1949
        .trainerName = _("KAY"),
#line 1950
        .trainerClass = TRAINER_CLASS_LASS,
#line 1951
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1953
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1954
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1955
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1957
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1959
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1958
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1961
            .species = SPECIES_WEEPINBELL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1963
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1962
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1965
    [DIFFICULTY_NORMAL][TRAINER_LASS_LISA] =
    {
#line 1966
        .trainerName = _("LISA"),
#line 1967
        .trainerClass = TRAINER_CLASS_LASS,
#line 1968
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 1970
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 1971
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1972
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1974
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1976
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1975
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1978
            .species = SPECIES_GLOOM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1980
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1979
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1982
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_EDMOND] =
    {
#line 1983
        .trainerName = _("EDMOND"),
#line 1984
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 1985
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 1987
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 1988
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 1989
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 1991
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1993
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1992
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 1995
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 1997
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 1996
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 1999
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_TREVOR] =
    {
#line 2000
        .trainerName = _("TREVOR"),
#line 2001
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2002
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2004
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2005
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2006
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2008
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2010
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2009
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2012
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2014
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2013
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2016
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_LEONARD] =
    {
#line 2017
        .trainerName = _("LEONARD"),
#line 2018
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2019
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2021
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2022
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2023
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2025
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2027
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2026
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2029
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_DUNCAN] =
    {
#line 2030
        .trainerName = _("DUNCAN"),
#line 2031
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2032
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2034
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2035
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2036
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2038
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2040
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2039
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2042
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2044
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2043
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2046
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2048
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2047
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2050
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_HUEY] =
    {
#line 2051
        .trainerName = _("HUEY"),
#line 2052
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2053
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2055
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2056
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2057
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2059
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2061
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2060
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2063
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2065
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2064
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2067
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_DYLAN] =
    {
#line 2068
        .trainerName = _("DYLAN"),
#line 2069
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2070
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2072
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2073
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2074
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2076
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2078
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2077
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2080
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2082
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2081
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2084
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2086
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2085
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2088
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_PHILLIP] =
    {
#line 2089
        .trainerName = _("PHILLIP"),
#line 2090
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2091
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2093
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2094
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2095
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2097
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2099
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2098
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2101
    [DIFFICULTY_NORMAL][TRAINER_SAILOR_DWAYNE] =
    {
#line 2102
        .trainerName = _("DWAYNE"),
#line 2103
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 2104
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 2106
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2107
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2108
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2110
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2112
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2111
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2114
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2116
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2115
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2118
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_LIAM] =
    {
#line 2119
        .trainerName = _("LIAM"),
#line 2120
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2121
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2123
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2124
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2125
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2127
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2129
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2128
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2130
                MOVE_TACKLE,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 2133
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2135
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2134
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2136
                MOVE_SCRATCH,
                MOVE_DEFENSE_CURL,
                MOVE_SAND_ATTACK,
            },
            },
        },
    },
#line 2140
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_SHANE] =
    {
#line 2141
        .trainerName = _("SHANE"),
#line 2142
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2143
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2145
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2146
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2147
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2149
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2151
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2150
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2153
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2155
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2154
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2157
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_ETHAN] =
    {
#line 2158
        .trainerName = _("ETHAN"),
#line 2159
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2160
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2162
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2163
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2164
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2166
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2168
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2167
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2170
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_RICKY] =
    {
#line 2171
        .trainerName = _("RICKY"),
#line 2172
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2173
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2175
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2176
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2177
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2179
            .species = SPECIES_SQUIRTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2181
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2180
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2183
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_JEFF] =
    {
#line 2184
        .trainerName = _("JEFF"),
#line 2185
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2186
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2188
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2189
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2190
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2192
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2194
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2193
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2196
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2198
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2197
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2200
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_2] =
    {
#line 2201
        .trainerName = _("PH"),
#line 2202
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2203
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2205
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2206
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2207
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2209
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2211
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2210
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2213
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_CHRIS] =
    {
#line 2214
        .trainerName = _("CHRIS"),
#line 2215
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2216
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2218
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2219
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2220
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2222
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2224
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2223
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2226
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2228
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2227
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2230
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_DREW] =
    {
#line 2231
        .trainerName = _("DREW"),
#line 2232
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 2233
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 2235
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 2236
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2237
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 2239
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2241
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2240
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2243
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2245
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2244
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2247
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2249
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2248
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2251
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2253
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2252
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2255
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_DIANA] =
    {
#line 2256
        .trainerName = _("DIANA"),
#line 2257
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2258
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2260
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2261
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2262
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2264
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2266
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2265
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2268
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_NANCY] =
    {
#line 2269
        .trainerName = _("NANCY"),
#line 2270
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2271
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2273
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2274
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2275
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2277
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2279
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2278
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2281
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2283
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2282
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2285
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ISABELLE] =
    {
#line 2286
        .trainerName = _("ISABELLE"),
#line 2287
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2288
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2290
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2291
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2292
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2294
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2296
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2295
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2298
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2300
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2299
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2302
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2304
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2303
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2306
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_KELSEY] =
    {
#line 2307
        .trainerName = _("KELSEY"),
#line 2308
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2309
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2311
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2312
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2313
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2315
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2317
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2316
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2319
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2321
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2320
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2323
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ALICIA] =
    {
#line 2324
        .trainerName = _("ALICIA"),
#line 2325
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2326
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2328
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2329
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2330
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 2332
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2334
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2333
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2336
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2338
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2337
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2340
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2342
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2341
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2344
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2346
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2345
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2348
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_CAITLIN] =
    {
#line 2349
        .trainerName = _("CAITLIN"),
#line 2350
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2351
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2353
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2354
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2355
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2357
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2359
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2358
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2361
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_HEIDI] =
    {
#line 2362
        .trainerName = _("HEIDI"),
#line 2363
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2364
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2366
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2367
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2368
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2370
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2372
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2371
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2374
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2376
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2375
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2378
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_CAROL] =
    {
#line 2379
        .trainerName = _("CAROL"),
#line 2380
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2381
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2383
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2384
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2385
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2387
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2389
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2388
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2391
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2393
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2392
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2395
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_SOFIA] =
    {
#line 2396
        .trainerName = _("SOFIA"),
#line 2397
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2398
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2400
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2401
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2402
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2404
            .species = SPECIES_JIGGLYPUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2406
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2405
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2408
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2410
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2409
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2412
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2414
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2413
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2416
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_MARTHA] =
    {
#line 2417
        .trainerName = _("MARTHA"),
#line 2418
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2419
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2421
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2422
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2423
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2425
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2427
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2426
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2429
            .species = SPECIES_BULBASAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2431
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2430
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2433
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_TINA] =
    {
#line 2434
        .trainerName = _("TINA"),
#line 2435
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2436
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2438
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2439
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2440
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2442
            .species = SPECIES_BULBASAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2444
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2443
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2446
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2448
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2447
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2450
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_HANNAH] =
    {
#line 2451
        .trainerName = _("HANNAH"),
#line 2452
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 2453
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 2455
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 2456
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2457
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 2459
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2461
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2460
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2463
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2465
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2464
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2467
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2469
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2468
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2471
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2473
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2472
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2475
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2477
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2476
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2479
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_MARK] =
    {
#line 2480
        .trainerName = _("MARK"),
#line 2481
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2482
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2484
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2485
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2486
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2488
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2490
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2489
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2492
            .species = SPECIES_LICKITUNG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2494
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2493
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2496
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_HERMAN] =
    {
#line 2497
        .trainerName = _("HERMAN"),
#line 2498
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2499
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2501
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2502
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2503
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2505
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2507
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2506
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2509
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2511
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2510
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2513
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_COOPER] =
    {
#line 2514
        .trainerName = _("COOPER"),
#line 2515
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2516
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2518
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2519
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2520
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2522
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2524
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2523
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2526
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2528
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2527
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2530
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2532
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2531
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2534
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_STEVE] =
    {
#line 2535
        .trainerName = _("STEVE"),
#line 2536
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2537
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2539
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2540
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2541
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2543
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2545
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2544
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2547
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2549
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2548
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2551
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_WINSTON] =
    {
#line 2552
        .trainerName = _("WINSTON"),
#line 2553
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2554
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2556
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2557
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2558
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2560
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2562
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2561
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2564
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_DAWSON] =
    {
#line 2565
        .trainerName = _("DAWSON"),
#line 2566
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2567
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2569
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2570
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2571
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2573
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2575
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2574
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2577
            .species = SPECIES_LAPRAS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2579
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2578
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2581
            .species = SPECIES_LICKITUNG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2583
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2582
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2585
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_ASHTON] =
    {
#line 2586
        .trainerName = _("ASHTON"),
#line 2587
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 2588
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 2590
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2591
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2592
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2594
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2596
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2595
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2598
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2600
            .iv = TRAINER_PARTY_IVS(3, 3, 3, 3, 3, 3),
#line 2599
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2602
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_JOVAN] =
    {
#line 2603
        .trainerName = _("JOVAN"),
#line 2604
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2605
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2607
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2608
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2609
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2611
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2613
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2612
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2615
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2617
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2616
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2619
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_MIGUEL] =
    {
#line 2620
        .trainerName = _("MIGUEL"),
#line 2621
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2622
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2624
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2625
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2626
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2628
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2630
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2629
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2632
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2634
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2633
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2636
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2638
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2637
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2640
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_AIDAN] =
    {
#line 2641
        .trainerName = _("AIDAN"),
#line 2642
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2643
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2645
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2646
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2647
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 2649
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2651
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2650
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2652
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_TACKLE,
                MOVE_CHARGE,
            },
            },
            {
#line 2657
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2659
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2658
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2660
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
            {
#line 2665
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2667
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2666
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2668
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_TACKLE,
                MOVE_CHARGE,
            },
            },
            {
#line 2673
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2675
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2674
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2676
                MOVE_SONIC_BOOM,
                MOVE_SUPERSONIC,
                MOVE_THUNDER_SHOCK,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 2681
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_GLENN] =
    {
#line 2682
        .trainerName = _("GLENN"),
#line 2683
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2684
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2686
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2687
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2688
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2690
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2692
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2691
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2694
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2696
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2695
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2698
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2700
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2699
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2702
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_LESLIE] =
    {
#line 2703
        .trainerName = _("LESLIE"),
#line 2704
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2705
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2707
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2708
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2709
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2711
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2713
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2712
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2714
                MOVE_SLUDGE,
                MOVE_SMOKESCREEN,
                MOVE_SMOG,
                MOVE_SELF_DESTRUCT,
            },
            },
        },
    },
#line 2719
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_1] =
    {
#line 2720
        .trainerName = _("PH"),
#line 2721
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2722
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2724
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2725
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2726
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2728
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2730
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2729
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2732
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2734
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2733
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2736
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2738
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2737
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2740
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_2] =
    {
#line 2741
        .trainerName = _("PH"),
#line 2742
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2743
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2745
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2746
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2747
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 2749
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2751
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2750
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2753
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2755
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2754
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2757
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2759
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2758
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2761
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2763
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2762
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2765
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_3] =
    {
#line 2766
        .trainerName = _("PH"),
#line 2767
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2768
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2770
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2771
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2772
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2774
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2776
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2775
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2778
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2780
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2779
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2782
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_ERIK] =
    {
#line 2783
        .trainerName = _("ERIK"),
#line 2784
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2785
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2787
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2788
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2789
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2791
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2793
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2792
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2795
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2797
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2796
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2799
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2801
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2800
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2803
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_AVERY] =
    {
#line 2804
        .trainerName = _("AVERY"),
#line 2805
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2806
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2808
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2809
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2810
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 2812
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2814
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2813
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2816
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2818
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2817
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2820
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2822
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2821
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2824
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2826
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2825
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2828
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_DEREK] =
    {
#line 2829
        .trainerName = _("DEREK"),
#line 2830
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2831
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2833
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2834
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2835
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2837
            .species = SPECIES_RAPIDASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2839
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2838
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2841
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_ZAC] =
    {
#line 2842
        .trainerName = _("ZAC"),
#line 2843
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 2844
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 2846
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 2847
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2848
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2850
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2852
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2851
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2854
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2856
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2855
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2858
    [DIFFICULTY_NORMAL][TRAINER_HIKER_MARCOS] =
    {
#line 2859
        .trainerName = _("MARCOS"),
#line 2860
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2861
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2863
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2864
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2865
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2867
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2869
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2868
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2871
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2873
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2872
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2875
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2877
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2876
            .lvl = 10,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2879
    [DIFFICULTY_NORMAL][TRAINER_HIKER_FRANKLIN] =
    {
#line 2880
        .trainerName = _("FRANKLIN"),
#line 2881
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2882
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2884
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2885
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2886
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2888
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2890
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2889
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2892
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2894
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2893
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2896
    [DIFFICULTY_NORMAL][TRAINER_HIKER_NOB] =
    {
#line 2897
        .trainerName = _("NOB"),
#line 2898
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2899
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2901
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2902
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2903
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 2905
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2907
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2906
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2909
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2911
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2910
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2913
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2915
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2914
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2917
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2919
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2918
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2921
    [DIFFICULTY_NORMAL][TRAINER_HIKER_WAYNE] =
    {
#line 2922
        .trainerName = _("WAYNE"),
#line 2923
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2924
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2926
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2927
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2928
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 2930
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2932
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2931
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2934
    [DIFFICULTY_NORMAL][TRAINER_HIKER_ALAN] =
    {
#line 2935
        .trainerName = _("ALAN"),
#line 2936
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2937
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2939
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2940
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2941
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2943
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2945
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2944
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2946
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 2951
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2953
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2952
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2954
                MOVE_HARDEN,
                MOVE_ROCK_THROW,
                MOVE_BIND,
                MOVE_SCREECH,
            },
            },
        },
    },
#line 2959
    [DIFFICULTY_NORMAL][TRAINER_HIKER_BRICE] =
    {
#line 2960
        .trainerName = _("BRICE"),
#line 2961
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2962
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2964
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2965
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2966
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 2968
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2970
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2969
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2972
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2974
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2973
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 2976
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2978
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2977
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 2980
    [DIFFICULTY_NORMAL][TRAINER_HIKER_CLARK] =
    {
#line 2981
        .trainerName = _("CLARK"),
#line 2982
        .trainerClass = TRAINER_CLASS_HIKER,
#line 2983
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 2985
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 2986
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 2987
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 2989
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2991
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2990
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 2992
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 2997
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 2999
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 2998
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3000
                MOVE_HARDEN,
                MOVE_ROCK_THROW,
                MOVE_BIND,
                MOVE_SCREECH,
            },
            },
        },
    },
#line 3005
    [DIFFICULTY_NORMAL][TRAINER_HIKER_TRENT] =
    {
#line 3006
        .trainerName = _("TRENT"),
#line 3007
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3008
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3010
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3011
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3012
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3014
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3016
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3015
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3018
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3020
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3019
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3022
    [DIFFICULTY_NORMAL][TRAINER_HIKER_DUDLEY] =
    {
#line 3023
        .trainerName = _("DUDLEY"),
#line 3024
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3025
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3027
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3028
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3029
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3031
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3033
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3032
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3034
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 3039
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3041
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3040
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3042
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 3047
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3049
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3048
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3050
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
        },
    },
#line 3055
    [DIFFICULTY_NORMAL][TRAINER_HIKER_ALLEN] =
    {
#line 3056
        .trainerName = _("ALLEN"),
#line 3057
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3058
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3060
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3061
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3062
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3064
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3066
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3065
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3067
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
        },
    },
#line 3072
    [DIFFICULTY_NORMAL][TRAINER_HIKER_ERIC] =
    {
#line 3073
        .trainerName = _("ERIC"),
#line 3074
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3075
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3077
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3078
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3079
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3081
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3083
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3082
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3085
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3087
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3086
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3089
    [DIFFICULTY_NORMAL][TRAINER_HIKER_LENNY] =
    {
#line 3090
        .trainerName = _("LENNY"),
#line 3091
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3092
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3094
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3095
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3096
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 3098
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3100
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3099
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3102
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3104
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3103
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3106
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3108
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3107
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3110
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3112
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3111
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3114
    [DIFFICULTY_NORMAL][TRAINER_HIKER_OLIVER] =
    {
#line 3115
        .trainerName = _("OLIVER"),
#line 3116
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3117
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3119
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3120
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3121
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3123
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3125
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3124
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3127
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3129
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3128
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3131
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3133
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3132
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3135
    [DIFFICULTY_NORMAL][TRAINER_HIKER_LUCAS] =
    {
#line 3136
        .trainerName = _("LUCAS"),
#line 3137
        .trainerClass = TRAINER_CLASS_HIKER,
#line 3138
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 3140
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3141
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3142
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3144
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3146
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3145
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3147
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 3152
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3154
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3153
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3155
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
        },
    },
#line 3160
    [DIFFICULTY_NORMAL][TRAINER_BIKER_JARED] =
    {
#line 3161
        .trainerName = _("JARED"),
#line 3162
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3163
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3165
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3166
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3167
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3169
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3171
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3170
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3172
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_POISON_GAS,
            },
            },
            {
#line 3177
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3179
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3178
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3180
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3185
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3187
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3186
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3188
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3193
    [DIFFICULTY_NORMAL][TRAINER_BIKER_MALIK] =
    {
#line 3194
        .trainerName = _("MALIK"),
#line 3195
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3196
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3198
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3199
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3200
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3202
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3204
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3203
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3205
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3210
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3212
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3211
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3213
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
        },
    },
#line 3218
    [DIFFICULTY_NORMAL][TRAINER_BIKER_ERNEST] =
    {
#line 3219
        .trainerName = _("ERNEST"),
#line 3220
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3221
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3223
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3224
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3225
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 3227
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3229
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3228
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3230
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3235
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3237
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3236
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3238
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3243
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3245
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3244
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3246
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3251
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3253
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3252
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3254
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3259
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3261
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3260
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3262
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
                MOVE_POUND,
            },
            },
        },
    },
#line 3267
    [DIFFICULTY_NORMAL][TRAINER_BIKER_ALEX] =
    {
#line 3268
        .trainerName = _("ALEX"),
#line 3269
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3270
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3272
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3273
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3274
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3276
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3278
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3277
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3279
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3284
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3286
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3285
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3287
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
            {
#line 3292
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3294
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3293
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3295
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3300
    [DIFFICULTY_NORMAL][TRAINER_BIKER_LAO] =
    {
#line 3301
        .trainerName = _("LAO"),
#line 3302
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3303
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3305
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3306
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3307
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3309
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3311
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3310
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3312
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
            {
#line 3317
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3319
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3318
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3320
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3325
    [DIFFICULTY_NORMAL][TRAINER_BIKER_1] =
    {
#line 3326
        .trainerName = _("PH"),
#line 3327
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3328
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3330
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3331
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3332
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3334
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3336
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3335
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3338
    [DIFFICULTY_NORMAL][TRAINER_BIKER_HIDEO] =
    {
#line 3339
        .trainerName = _("HIDEO"),
#line 3340
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3341
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3343
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3344
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3345
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3347
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3349
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3348
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3351
    [DIFFICULTY_NORMAL][TRAINER_BIKER_RUBEN] =
    {
#line 3352
        .trainerName = _("RUBEN"),
#line 3353
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3354
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3356
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3357
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3358
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3360
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3362
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3361
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3363
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3368
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3370
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3369
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3371
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3376
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3378
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3377
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3379
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3384
    [DIFFICULTY_NORMAL][TRAINER_BIKER_BILLY] =
    {
#line 3385
        .trainerName = _("BILLY"),
#line 3386
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3387
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3389
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3390
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3391
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3393
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3395
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3394
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3397
    [DIFFICULTY_NORMAL][TRAINER_BIKER_NIKOLAS] =
    {
#line 3398
        .trainerName = _("NIKOLAS"),
#line 3399
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3400
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3402
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3403
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3404
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3406
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3408
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3407
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3409
                MOVE_SPARK,
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_CHARGE,
            },
            },
            {
#line 3414
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3416
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3415
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3417
                MOVE_SPARK,
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_CHARGE,
            },
            },
        },
    },
#line 3422
    [DIFFICULTY_NORMAL][TRAINER_BIKER_JAXON] =
    {
#line 3423
        .trainerName = _("JAXON"),
#line 3424
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3425
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3427
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3428
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3429
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3431
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3433
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3432
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3434
                MOVE_SLUDGE,
                MOVE_SMOKESCREEN,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3439
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3441
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3440
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3442
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
        },
    },
#line 3447
    [DIFFICULTY_NORMAL][TRAINER_BIKER_WILLIAM] =
    {
#line 3448
        .trainerName = _("WILLIAM"),
#line 3449
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3450
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3452
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3453
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3454
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 3456
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3458
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3457
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3459
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3464
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3466
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3465
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3467
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3472
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3474
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3473
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3475
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3480
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3482
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3481
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3483
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3488
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3490
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3489
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3491
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SELF_DESTRUCT,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3496
    [DIFFICULTY_NORMAL][TRAINER_BIKER_LUKAS] =
    {
#line 3497
        .trainerName = _("LUKAS"),
#line 3498
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3499
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3501
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3502
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3503
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 3505
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3507
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3506
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3508
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3513
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3515
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3514
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3516
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3521
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3523
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3522
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3524
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
            {
#line 3529
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3531
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3530
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3532
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3537
    [DIFFICULTY_NORMAL][TRAINER_BIKER_ISAAC] =
    {
#line 3538
        .trainerName = _("ISAAC"),
#line 3539
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3540
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3542
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3543
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3544
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3546
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3548
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3547
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3549
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
            {
#line 3554
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3556
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3555
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3557
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
            {
#line 3562
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3564
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3563
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3565
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 3570
    [DIFFICULTY_NORMAL][TRAINER_BIKER_GERALD] =
    {
#line 3571
        .trainerName = _("GERALD"),
#line 3572
        .trainerClass = TRAINER_CLASS_BIKER,
#line 3573
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 3575
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3576
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3577
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3579
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3581
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3580
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3582
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 3587
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3589
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3588
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 3590
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
        },
    },
#line 3595
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_1] =
    {
#line 3596
        .trainerName = _("PH"),
#line 3597
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3598
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3600
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3601
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3602
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3604
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3606
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3605
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3608
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3610
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3609
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3612
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_2] =
    {
#line 3613
        .trainerName = _("PH"),
#line 3614
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3615
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3617
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3618
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3619
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3621
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3623
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3622
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3625
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_3] =
    {
#line 3626
        .trainerName = _("PH"),
#line 3627
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3628
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3630
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3631
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3632
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3634
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3636
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3635
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3638
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3640
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3639
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3642
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3644
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3643
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3646
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_QUINN] =
    {
#line 3647
        .trainerName = _("QUINN"),
#line 3648
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3649
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3651
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3652
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3653
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3655
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3657
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3656
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3659
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3661
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3660
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3663
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3665
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3664
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3667
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_RAMON] =
    {
#line 3668
        .trainerName = _("RAMON"),
#line 3669
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3670
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3672
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3673
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3674
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3676
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3678
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3677
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3680
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_DUSTY] =
    {
#line 3681
        .trainerName = _("DUSTY"),
#line 3682
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3683
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3685
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3686
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3687
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3689
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3691
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3690
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3693
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3695
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3694
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3697
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_ARNIE] =
    {
#line 3698
        .trainerName = _("ARNIE"),
#line 3699
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3700
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3702
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3703
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3704
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3706
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3708
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3707
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3710
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3712
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3711
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3714
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_4] =
    {
#line 3715
        .trainerName = _("PH"),
#line 3716
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3717
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3719
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3720
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3721
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3723
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3725
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3724
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3727
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3729
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3728
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3731
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_SIMON] =
    {
#line 3732
        .trainerName = _("SIMON"),
#line 3733
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3734
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3736
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3737
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3738
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3740
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3742
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3741
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3744
    [DIFFICULTY_NORMAL][TRAINER_BURGLAR_LEWIS] =
    {
#line 3745
        .trainerName = _("LEWIS"),
#line 3746
        .trainerClass = TRAINER_CLASS_BURGLAR,
#line 3747
        .trainerPic = TRAINER_PIC_BURGLAR,
        .encounterMusic_gender =
#line 3749
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 3750
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3751
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3753
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3755
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3754
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3757
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3759
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3758
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3761
    [DIFFICULTY_NORMAL][TRAINER_ENGINEER_BAILY] =
    {
#line 3762
        .trainerName = _("BAILY"),
#line 3763
        .trainerClass = TRAINER_CLASS_ENGINEER,
#line 3764
        .trainerPic = TRAINER_PIC_ENGINEER,
        .encounterMusic_gender =
#line 3766
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3767
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3768
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3770
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3772
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3771
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3774
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3776
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3775
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3778
    [DIFFICULTY_NORMAL][TRAINER_ENGINEER_BRAXTON] =
    {
#line 3779
        .trainerName = _("BRAXTON"),
#line 3780
        .trainerClass = TRAINER_CLASS_ENGINEER,
#line 3781
        .trainerPic = TRAINER_PIC_ENGINEER,
        .encounterMusic_gender =
#line 3783
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3784
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3785
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3787
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3789
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3788
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3791
    [DIFFICULTY_NORMAL][TRAINER_ENGINEER_BERNIE] =
    {
#line 3792
        .trainerName = _("BERNIE"),
#line 3793
        .trainerClass = TRAINER_CLASS_ENGINEER,
#line 3794
        .trainerPic = TRAINER_PIC_ENGINEER,
        .encounterMusic_gender =
#line 3796
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 3797
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3798
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3800
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3802
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3801
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3804
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3806
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3805
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3808
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3810
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3809
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3812
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_DALE] =
    {
#line 3813
        .trainerName = _("DALE"),
#line 3814
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3815
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3817
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3818
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3819
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3821
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3823
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3822
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3825
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3827
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3826
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3829
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3831
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3830
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3833
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_BARNY] =
    {
#line 3834
        .trainerName = _("BARNY"),
#line 3835
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3836
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3838
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3839
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3840
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3842
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3844
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3843
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3846
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3848
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3847
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3850
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3852
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3851
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3854
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_NED] =
    {
#line 3855
        .trainerName = _("NED"),
#line 3856
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3857
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3859
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3860
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3861
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 3863
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3865
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3864
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3867
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3869
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3868
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3871
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3873
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3872
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3875
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_CHIP] =
    {
#line 3876
        .trainerName = _("CHIP"),
#line 3877
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3878
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3880
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3881
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3882
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3884
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3886
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3885
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3888
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3890
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3889
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3892
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_HANK] =
    {
#line 3893
        .trainerName = _("HANK"),
#line 3894
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3895
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3897
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3898
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3899
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 3901
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3903
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3902
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3905
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_ELLIOT] =
    {
#line 3906
        .trainerName = _("ELLIOT"),
#line 3907
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3908
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3910
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3911
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3912
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 3914
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3916
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3915
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3918
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3920
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3919
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3922
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3924
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3923
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3926
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3928
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3927
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3930
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_RONALD] =
    {
#line 3931
        .trainerName = _("RONALD"),
#line 3932
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3933
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3935
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3936
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3937
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 3939
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3941
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3940
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3943
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3945
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3944
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3947
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3949
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3948
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3951
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3953
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3952
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3955
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_CLAUDE] =
    {
#line 3956
        .trainerName = _("CLAUDE"),
#line 3957
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3958
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3960
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3961
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3962
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 3964
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3966
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3965
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3968
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3970
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3969
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 3972
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_WADE] =
    {
#line 3973
        .trainerName = _("WADE"),
#line 3974
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 3975
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 3977
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 3978
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 3979
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 3981
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3983
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3982
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3985
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3987
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3986
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3989
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3991
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3990
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3993
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3995
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3994
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 3997
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 3999
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 3998
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4001
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4003
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4002
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4005
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_NOLAN] =
    {
#line 4006
        .trainerName = _("NOLAN"),
#line 4007
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 4008
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 4010
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 4011
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4012
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4014
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4016
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4015
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4018
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4020
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4019
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4022
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_ANDREW] =
    {
#line 4023
        .trainerName = _("ANDREW"),
#line 4024
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 4025
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 4027
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 4028
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4029
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4031
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4033
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4032
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4035
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4037
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4036
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4039
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_LUIS] =
    {
#line 4040
        .trainerName = _("LUIS"),
#line 4041
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4042
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4044
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4045
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4046
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4048
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4050
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4049
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4052
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4054
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4053
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4056
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_RICHARD] =
    {
#line 4057
        .trainerName = _("RICHARD"),
#line 4058
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4059
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4061
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4062
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4063
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4065
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4067
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4066
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4069
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4071
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4070
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4073
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_REECE] =
    {
#line 4074
        .trainerName = _("REECE"),
#line 4075
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4076
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4078
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4079
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4080
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4082
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4084
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4083
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4086
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4088
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4087
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4090
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4092
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4091
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4094
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_MATTHEW] =
    {
#line 4095
        .trainerName = _("MATTHEW"),
#line 4096
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4097
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4099
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4100
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4101
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4103
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4105
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4104
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4107
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4109
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4108
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4111
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_DOUGLAS] =
    {
#line 4112
        .trainerName = _("DOUGLAS"),
#line 4113
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4114
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4116
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4117
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4118
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 4120
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4122
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4121
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4124
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4126
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4125
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4128
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4130
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4129
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4132
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4134
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4133
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4136
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_DAVID] =
    {
#line 4137
        .trainerName = _("DAVID"),
#line 4138
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4139
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4141
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4142
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4143
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4145
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4147
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4146
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4149
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4151
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4150
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4153
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4155
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4154
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4157
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_TONY] =
    {
#line 4158
        .trainerName = _("TONY"),
#line 4159
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4160
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4162
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4163
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4164
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4166
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4168
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4167
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4170
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4172
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4171
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4174
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_AXLE] =
    {
#line 4175
        .trainerName = _("AXLE"),
#line 4176
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4177
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4179
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4180
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4181
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 4183
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4185
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4184
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4187
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4189
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4188
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4191
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4193
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4192
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4195
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4197
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4196
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4199
            .species = SPECIES_TENTACRUEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4201
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4200
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4203
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_BARRY] =
    {
#line 4204
        .trainerName = _("BARRY"),
#line 4205
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4206
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4208
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4209
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4210
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4212
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4214
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4213
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4216
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4218
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4217
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4220
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_DEAN] =
    {
#line 4221
        .trainerName = _("DEAN"),
#line 4222
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4223
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4225
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4226
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4227
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4229
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4231
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4230
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4233
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_DARRIN] =
    {
#line 4234
        .trainerName = _("DARRIN"),
#line 4235
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4236
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4238
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4239
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4240
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 4242
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4244
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4243
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4246
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4248
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4247
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4250
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4252
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4251
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4254
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4256
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4255
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4258
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_SPENCER] =
    {
#line 4259
        .trainerName = _("SPENCER"),
#line 4260
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4261
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4263
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4264
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4265
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4267
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4269
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4268
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4271
            .species = SPECIES_TENTACRUEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4273
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4272
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4275
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_JACK] =
    {
#line 4276
        .trainerName = _("JACK"),
#line 4277
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4278
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4280
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4281
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4282
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4284
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4286
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4285
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4288
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_JEROME] =
    {
#line 4289
        .trainerName = _("JEROME"),
#line 4290
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4291
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4293
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4294
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4295
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4297
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4299
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4298
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4301
            .species = SPECIES_WARTORTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4303
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4302
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4305
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_ROLAND] =
    {
#line 4306
        .trainerName = _("ROLAND"),
#line 4307
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 4308
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 4310
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 4311
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4312
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4314
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4316
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4315
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4318
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4320
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4319
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4322
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4324
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4323
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4326
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_KOJI] =
    {
#line 4327
        .trainerName = _("KOJI"),
#line 4328
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4329
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4331
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4332
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4333
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4335
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4337
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4336
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4339
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4341
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4340
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4343
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4345
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4344
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4347
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_LUKE] =
    {
#line 4348
        .trainerName = _("LUKE"),
#line 4349
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4350
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4352
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4353
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4354
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4356
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4358
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4357
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4360
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4362
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4361
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4364
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_CAMRON] =
    {
#line 4365
        .trainerName = _("CAMRON"),
#line 4366
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4367
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4369
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4370
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4371
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4373
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4375
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4374
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4377
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4379
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4378
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4381
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_RAUL] =
    {
#line 4382
        .trainerName = _("RAUL"),
#line 4383
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4384
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4386
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4387
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4388
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4390
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4392
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4391
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4394
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4396
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4395
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4398
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_ISAIAH] =
    {
#line 4399
        .trainerName = _("ISAIAH"),
#line 4400
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4401
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4403
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4404
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4405
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4407
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4409
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4408
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4411
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4413
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4412
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4415
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_ZEEK] =
    {
#line 4416
        .trainerName = _("ZEEK"),
#line 4417
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4418
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4420
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4421
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4422
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4424
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4426
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4425
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4428
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_JAMAL] =
    {
#line 4429
        .trainerName = _("JAMAL"),
#line 4430
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4431
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4433
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4434
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4435
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 4437
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4439
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4438
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4441
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4443
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4442
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4445
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4447
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4446
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4449
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4451
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4450
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4453
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_COREY] =
    {
#line 4454
        .trainerName = _("COREY"),
#line 4455
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4456
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4458
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4459
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4460
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4462
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4464
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4463
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4466
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4468
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4467
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4470
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_CHASE] =
    {
#line 4471
        .trainerName = _("CHASE"),
#line 4472
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 4473
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 4475
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4476
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4477
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4479
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4481
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4480
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4483
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4485
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4484
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4487
            .species = SPECIES_TENTACRUEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4489
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4488
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4491
    [DIFFICULTY_NORMAL][TRAINER_GAMER_HUGO] =
    {
#line 4492
        .trainerName = _("HUGO"),
#line 4493
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4494
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4496
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4497
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4498
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4500
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4502
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4501
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4504
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4506
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4505
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4508
    [DIFFICULTY_NORMAL][TRAINER_GAMER_JASPER] =
    {
#line 4509
        .trainerName = _("JASPER"),
#line 4510
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4511
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4513
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4514
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4515
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4517
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4519
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4518
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4521
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4523
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4522
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4525
    [DIFFICULTY_NORMAL][TRAINER_GAMER_DIRK] =
    {
#line 4526
        .trainerName = _("DIRK"),
#line 4527
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4528
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4530
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4531
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4532
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4534
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4536
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4535
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4538
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4540
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4539
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4542
    [DIFFICULTY_NORMAL][TRAINER_GAMER_DARIAN] =
    {
#line 4543
        .trainerName = _("DARIAN"),
#line 4544
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4545
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4547
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4548
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4549
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4551
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4553
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4552
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4555
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4557
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4556
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4559
    [DIFFICULTY_NORMAL][TRAINER_GAMER_STAN] =
    {
#line 4560
        .trainerName = _("STAN"),
#line 4561
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4562
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4564
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4565
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4566
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4568
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4570
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4569
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4572
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4574
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4573
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4576
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4578
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4577
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4580
    [DIFFICULTY_NORMAL][TRAINER_GAMER_1] =
    {
#line 4581
        .trainerName = _("PH"),
#line 4582
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4583
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4585
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4586
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4587
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4589
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4591
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4590
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4593
    [DIFFICULTY_NORMAL][TRAINER_GAMER_RICH] =
    {
#line 4594
        .trainerName = _("RICH"),
#line 4595
        .trainerClass = TRAINER_CLASS_GAMER,
#line 4596
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 4598
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4599
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4600
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4602
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4604
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4603
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4606
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4608
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4607
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4610
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_BRIDGET] =
    {
#line 4611
        .trainerName = _("BRIDGET"),
#line 4612
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4613
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4615
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4616
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4617
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 4619
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4621
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4620
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4623
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4625
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4624
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4627
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4629
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4628
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4631
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4633
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4632
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4635
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_TAMIA] =
    {
#line 4636
        .trainerName = _("TAMIA"),
#line 4637
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4638
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4640
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4641
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4642
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4644
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4646
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4645
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4648
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4650
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4649
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4652
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_LORI] =
    {
#line 4653
        .trainerName = _("LORI"),
#line 4654
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4655
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4657
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4658
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4659
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4661
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4663
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4662
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4665
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_LOLA] =
    {
#line 4666
        .trainerName = _("LOLA"),
#line 4667
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4668
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4670
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4671
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4672
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4674
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4676
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4675
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4678
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4680
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4679
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4682
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4684
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4683
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4686
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_SHEILA] =
    {
#line 4687
        .trainerName = _("SHEILA"),
#line 4688
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4689
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4691
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4692
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4693
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4695
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4697
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4696
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4699
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4701
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4700
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4703
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_TIFFANY] =
    {
#line 4704
        .trainerName = _("TIFFANY"),
#line 4705
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4706
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4708
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4709
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4710
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4712
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4714
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4713
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4716
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_NORA] =
    {
#line 4717
        .trainerName = _("NORA"),
#line 4718
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4719
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4721
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4722
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4723
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4725
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4727
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4726
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4729
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4731
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4730
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4733
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4735
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4734
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4737
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_MELISSA] =
    {
#line 4738
        .trainerName = _("MELISSA"),
#line 4739
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4740
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4742
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4743
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4744
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4746
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4748
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4747
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4750
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4752
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4751
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4754
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_GRACE] =
    {
#line 4755
        .trainerName = _("GRACE"),
#line 4756
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4757
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4759
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4760
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4761
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4763
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4765
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4764
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4767
            .species = SPECIES_WIGGLYTUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4769
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4768
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4771
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_OLIVIA] =
    {
#line 4772
        .trainerName = _("OLIVIA"),
#line 4773
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4774
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 4776
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4777
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4778
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4780
            .species = SPECIES_BULBASAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4782
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4781
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4784
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4786
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4785
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4788
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_LAUREN] =
    {
#line 4789
        .trainerName = _("LAUREN"),
#line 4790
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 4791
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4793
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4794
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4795
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4797
            .species = SPECIES_WEEPINBELL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4799
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4798
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4801
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4803
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4802
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4805
            .species = SPECIES_WEEPINBELL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4807
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4806
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4809
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_ANYA] =
    {
#line 4810
        .trainerName = _("ANYA"),
#line 4811
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4812
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4814
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4815
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4816
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 4818
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4820
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4819
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4822
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4824
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4823
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4826
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4828
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4827
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4830
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4832
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4831
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4834
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4836
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4835
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4838
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_ALICE] =
    {
#line 4839
        .trainerName = _("ALICE"),
#line 4840
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4841
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4843
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4844
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4845
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4847
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4849
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4848
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4851
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4853
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4852
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4855
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_CONNIE] =
    {
#line 4856
        .trainerName = _("CONNIE"),
#line 4857
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4858
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4860
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4861
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4862
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4864
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4866
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4865
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4868
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4870
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4869
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4872
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4874
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4873
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4876
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_SHIRLEY] =
    {
#line 4877
        .trainerName = _("SHIRLEY"),
#line 4878
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 4879
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 4881
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 4882
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4883
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4885
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4887
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4886
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4889
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4891
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4890
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4893
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4895
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4894
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4897
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_JOHAN] =
    {
#line 4898
        .trainerName = _("JOHAN"),
#line 4899
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 4900
        .trainerPic = TRAINER_PIC_PSYCHIC_M,
        .encounterMusic_gender =
#line 4902
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 4903
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4904
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 4906
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4908
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4907
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4910
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4912
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4911
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4914
            .species = SPECIES_MR_MIME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4916
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4915
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4918
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4920
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4919
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4922
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_TYRON] =
    {
#line 4923
        .trainerName = _("TYRON"),
#line 4924
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 4925
        .trainerPic = TRAINER_PIC_PSYCHIC_M,
        .encounterMusic_gender =
#line 4927
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 4928
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4929
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 4931
            .species = SPECIES_MR_MIME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4933
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4932
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4935
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4937
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4936
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4939
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_CAMERON] =
    {
#line 4940
        .trainerName = _("CAMERON"),
#line 4941
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 4942
        .trainerPic = TRAINER_PIC_PSYCHIC_M,
        .encounterMusic_gender =
#line 4944
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 4945
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4946
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4948
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4950
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4949
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4952
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4954
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4953
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4956
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4958
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4957
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4960
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_PRESTON] =
    {
#line 4961
        .trainerName = _("PRESTON"),
#line 4962
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 4963
        .trainerPic = TRAINER_PIC_PSYCHIC_M,
        .encounterMusic_gender =
#line 4965
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 4966
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4967
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 4969
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4971
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 4970
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4973
    [DIFFICULTY_NORMAL][TRAINER_ROCKER_RANDALL] =
    {
#line 4974
        .trainerName = _("RANDALL"),
#line 4975
        .trainerClass = TRAINER_CLASS_ROCKER,
#line 4976
        .trainerPic = TRAINER_PIC_ROCKER,
        .encounterMusic_gender =
#line 4978
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 4979
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 4980
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 4982
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4984
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4983
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4986
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4988
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4987
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 4990
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 4992
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 4991
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 4994
    [DIFFICULTY_NORMAL][TRAINER_ROCKER_LUCA] =
    {
#line 4995
        .trainerName = _("LUCA"),
#line 4996
        .trainerClass = TRAINER_CLASS_ROCKER,
#line 4997
        .trainerPic = TRAINER_PIC_ROCKER,
        .encounterMusic_gender =
#line 4999
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5000
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5001
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5003
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5005
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5004
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5007
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5009
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5008
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5011
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_DALTON] =
    {
#line 5012
        .trainerName = _("DALTON"),
#line 5013
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5014
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5016
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5017
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5018
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5020
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5022
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5021
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5024
            .species = SPECIES_MR_MIME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5026
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5025
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5028
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_NELSON] =
    {
#line 5029
        .trainerName = _("NELSON"),
#line 5030
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5031
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5033
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5034
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5035
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5037
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5039
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5038
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5041
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5043
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5042
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5045
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5047
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5046
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5049
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5051
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5050
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5053
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_KIRK] =
    {
#line 5054
        .trainerName = _("KIRK"),
#line 5055
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5056
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5058
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5059
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5060
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5062
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5064
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5063
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5066
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5068
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5067
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5070
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5072
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5071
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5074
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5076
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5075
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5078
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_SHAWN] =
    {
#line 5079
        .trainerName = _("SHAWN"),
#line 5080
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5081
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5083
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5084
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5085
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5087
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5089
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5088
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5091
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5093
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5092
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5095
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_GREGORY] =
    {
#line 5096
        .trainerName = _("GREGORY"),
#line 5097
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5098
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5100
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5101
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5102
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5104
            .species = SPECIES_MR_MIME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5106
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5105
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5107
                MOVE_PSYCHIC,
                MOVE_ROLE_PLAY,
                MOVE_DOUBLE_SLAP,
                MOVE_ENCORE,
            },
            },
        },
    },
#line 5156
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_KAYDEN] =
    {
#line 5157
        .trainerName = _("KAYDEN"),
#line 5158
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5159
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5161
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5162
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5163
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5165
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5167
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5166
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5169
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_NATE] =
    {
#line 5170
        .trainerName = _("NATE"),
#line 5171
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 5172
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 5174
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5175
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5176
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5178
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5180
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5179
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5182
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5184
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5183
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5186
    [DIFFICULTY_NORMAL][TRAINER_TAMER_PHIL] =
    {
#line 5187
        .trainerName = _("PHIL"),
#line 5188
        .trainerClass = TRAINER_CLASS_TAMER,
#line 5189
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 5191
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5192
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5193
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5195
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5197
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5196
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5199
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5201
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5200
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5203
    [DIFFICULTY_NORMAL][TRAINER_TAMER_EDGAR] =
    {
#line 5204
        .trainerName = _("EDGAR"),
#line 5205
        .trainerClass = TRAINER_CLASS_TAMER,
#line 5206
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 5208
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5209
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5210
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5212
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5214
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5213
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5216
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5218
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5217
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5220
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5222
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5221
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5224
    [DIFFICULTY_NORMAL][TRAINER_TAMER_JASON] =
    {
#line 5225
        .trainerName = _("JASON"),
#line 5226
        .trainerClass = TRAINER_CLASS_TAMER,
#line 5227
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 5229
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5230
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5231
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5233
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5235
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5234
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5237
    [DIFFICULTY_NORMAL][TRAINER_TAMER_COLE] =
    {
#line 5238
        .trainerName = _("COLE"),
#line 5239
        .trainerClass = TRAINER_CLASS_TAMER,
#line 5240
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 5242
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5243
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5244
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5246
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5248
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5247
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5250
            .species = SPECIES_TAUROS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5252
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5251
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5254
    [DIFFICULTY_NORMAL][TRAINER_TAMER_VINCENT] =
    {
#line 5255
        .trainerName = _("VINCENT"),
#line 5256
        .trainerClass = TRAINER_CLASS_TAMER,
#line 5257
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 5259
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5260
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5261
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5263
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5265
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5264
            .lvl = 44,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5267
            .species = SPECIES_GOLDUCK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5269
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5268
            .lvl = 44,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5271
    [DIFFICULTY_NORMAL][TRAINER_TAMER_JOHN] =
    {
#line 5272
        .trainerName = _("JOHN"),
#line 5273
        .trainerClass = TRAINER_CLASS_TAMER,
#line 5274
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 5276
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 5277
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5278
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5280
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5282
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5281
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5284
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5286
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5285
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5288
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5290
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5289
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5292
            .species = SPECIES_TAUROS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5294
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 5293
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5296
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_SEBASTIAN] =
    {
#line 5297
        .trainerName = _("SEBASTIAN"),
#line 5298
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5299
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5301
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5302
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5303
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5305
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5307
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5306
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5309
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5311
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5310
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5313
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_PERRY] =
    {
#line 5314
        .trainerName = _("PERRY"),
#line 5315
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5316
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5318
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5319
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5320
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 5322
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5324
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5323
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5326
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5328
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5327
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5330
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5332
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5331
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5334
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5336
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5335
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5338
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5340
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5339
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5342
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_ROBERT] =
    {
#line 5343
        .trainerName = _("ROBERT"),
#line 5344
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5345
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5347
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5348
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5349
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5351
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5353
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5352
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5355
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5357
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5356
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5359
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5361
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5360
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5363
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5365
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5364
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5367
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_DONALD] =
    {
#line 5368
        .trainerName = _("DONALD"),
#line 5369
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5370
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5372
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5373
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5374
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5376
            .species = SPECIES_FARFETCHD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5378
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5377
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5380
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_BENNY] =
    {
#line 5381
        .trainerName = _("BENNY"),
#line 5382
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5383
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5385
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5386
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5387
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5389
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5391
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5390
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5393
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5395
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5394
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5397
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_EDWIN] =
    {
#line 5398
        .trainerName = _("EDWIN"),
#line 5399
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5400
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5402
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5403
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5404
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5406
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5408
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5407
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5410
            .species = SPECIES_FARFETCHD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5412
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5411
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5414
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5416
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5415
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5418
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5420
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5419
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5422
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_CHESTER] =
    {
#line 5423
        .trainerName = _("CHESTER"),
#line 5424
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5425
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5427
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5428
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5429
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5431
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5433
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5432
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5435
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5437
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5436
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5439
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5441
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5440
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5443
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_WILTON] =
    {
#line 5444
        .trainerName = _("WILTON"),
#line 5445
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5446
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5448
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5449
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5450
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5452
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5454
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5453
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5456
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5458
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5457
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5460
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_RAMIRO] =
    {
#line 5461
        .trainerName = _("RAMIRO"),
#line 5462
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5463
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5465
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5466
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5467
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5469
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5471
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5470
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5473
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_JACOB] =
    {
#line 5474
        .trainerName = _("JACOB"),
#line 5475
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5476
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5478
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5479
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5480
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5482
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5484
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5483
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5486
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5488
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5487
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5490
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5492
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5491
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5494
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5496
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5495
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5498
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_ROGER] =
    {
#line 5499
        .trainerName = _("ROGER"),
#line 5500
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5501
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5503
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5504
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5505
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5507
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5509
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5508
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5511
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5513
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5512
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5515
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5517
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5516
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5519
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_REED] =
    {
#line 5520
        .trainerName = _("REED"),
#line 5521
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5522
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5524
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5525
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5526
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5528
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5530
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5529
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5532
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5534
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5533
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5536
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5538
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5537
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5540
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5542
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5541
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5544
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_KEITH] =
    {
#line 5545
        .trainerName = _("KEITH"),
#line 5546
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5547
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5549
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5550
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5551
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5553
            .species = SPECIES_FARFETCHD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5555
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5554
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5557
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5559
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5558
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5561
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_CARTER] =
    {
#line 5562
        .trainerName = _("CARTER"),
#line 5563
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5564
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5566
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5567
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5568
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5570
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5572
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5571
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5574
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5576
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5575
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5578
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5580
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5579
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5582
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_MITCH] =
    {
#line 5583
        .trainerName = _("MITCH"),
#line 5584
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5585
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5587
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5588
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5589
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5591
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5593
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5592
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5595
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5597
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5596
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5599
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5601
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5600
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5603
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5605
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5604
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5607
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_BECK] =
    {
#line 5608
        .trainerName = _("BECK"),
#line 5609
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5610
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5612
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5613
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5614
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5616
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5618
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5617
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5620
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5622
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5621
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5624
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_MARLON] =
    {
#line 5625
        .trainerName = _("MARLON"),
#line 5626
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 5627
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 5629
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 5630
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5631
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5633
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5635
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5634
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5637
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5639
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5638
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5641
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5643
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5642
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5645
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_KOICHI] =
    {
#line 5646
        .trainerName = _("KOICHI"),
#line 5647
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5648
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5650
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5651
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5652
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5654
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5654
            .heldItem = ITEM_BLACK_BELT,
#line 5656
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5655
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5658
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5658
            .heldItem = ITEM_BLACK_BELT,
#line 5660
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5659
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5662
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_MIKE] =
    {
#line 5663
        .trainerName = _("MIKE"),
#line 5664
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5665
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5667
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5668
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5669
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5671
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5671
            .heldItem = ITEM_BLACK_BELT,
#line 5673
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5672
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5675
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5675
            .heldItem = ITEM_BLACK_BELT,
#line 5677
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5676
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5679
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5679
            .heldItem = ITEM_BLACK_BELT,
#line 5681
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5680
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5683
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_HIDEKI] =
    {
#line 5684
        .trainerName = _("HIDEKI"),
#line 5685
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5686
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5688
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5689
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5690
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5692
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5692
            .heldItem = ITEM_BLACK_BELT,
#line 5694
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5693
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5696
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5696
            .heldItem = ITEM_BLACK_BELT,
#line 5698
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5697
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5700
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_AARON] =
    {
#line 5701
        .trainerName = _("AARON"),
#line 5702
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5703
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5705
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5706
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5707
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5709
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5709
            .heldItem = ITEM_BLACK_BELT,
#line 5711
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5710
            .lvl = 36,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5713
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_HITOSHI] =
    {
#line 5714
        .trainerName = _("HITOSHI"),
#line 5715
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5716
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5718
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5719
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5720
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5722
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5722
            .heldItem = ITEM_BLACK_BELT,
#line 5724
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5723
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5726
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5726
            .heldItem = ITEM_BLACK_BELT,
#line 5728
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5727
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5730
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5730
            .heldItem = ITEM_BLACK_BELT,
#line 5732
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5731
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5734
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_ATSUSHI] =
    {
#line 5735
        .trainerName = _("ATSUSHI"),
#line 5736
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5737
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5739
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5740
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5741
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5743
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5743
            .heldItem = ITEM_BLACK_BELT,
#line 5745
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5744
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5747
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5747
            .heldItem = ITEM_BLACK_BELT,
#line 5749
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5748
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5751
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_KIYO] =
    {
#line 5752
        .trainerName = _("KIYO"),
#line 5753
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5754
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5756
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5757
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5758
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5760
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5760
            .heldItem = ITEM_BLACK_BELT,
#line 5762
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5761
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5764
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_TAKASHI] =
    {
#line 5765
        .trainerName = _("TAKASHI"),
#line 5766
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5767
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5769
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5770
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5771
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5773
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5773
            .heldItem = ITEM_BLACK_BELT,
#line 5775
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5774
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5777
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5777
            .heldItem = ITEM_BLACK_BELT,
#line 5779
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5778
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5781
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5781
            .heldItem = ITEM_BLACK_BELT,
#line 5783
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5782
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5785
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_DAISUKE] =
    {
#line 5786
        .trainerName = _("DAISUKE"),
#line 5787
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 5788
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 5790
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 5791
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5792
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 5794
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5794
            .heldItem = ITEM_BLACK_BELT,
#line 5796
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5795
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5798
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5798
            .heldItem = ITEM_BLACK_BELT,
#line 5800
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5799
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 5802
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5802
            .heldItem = ITEM_BLACK_BELT,
#line 5804
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5803
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 5806
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_OAKS_LAB_SQUIRTLE] =
    {
#line 5807
        .trainerName = _("TERRY"),
#line 5808
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5809
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5811
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5812
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5813
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5815
            .species = SPECIES_SQUIRTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5817
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5816
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5818
                MOVE_TACKLE,
                MOVE_TAIL_WHIP,
            },
            },
        },
    },
#line 5821
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_OAKS_LAB_BULBASAUR] =
    {
#line 5822
        .trainerName = _("TERRY"),
#line 5823
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5824
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5826
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5827
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5828
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5830
            .species = SPECIES_BULBASAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5832
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5831
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5833
                MOVE_TACKLE,
                MOVE_GROWL,
            },
            },
        },
    },
#line 5836
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_OAKS_LAB_CHARMANDER] =
    {
#line 5837
        .trainerName = _("TERRY"),
#line 5838
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5839
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5841
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5842
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5843
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 5845
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5847
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 5846
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5848
                MOVE_SCRATCH,
                MOVE_GROWL,
            },
            },
        },
    },
#line 5851
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE] =
    {
#line 5852
        .trainerName = _("TERRY"),
#line 5853
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5854
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5856
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5857
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5858
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5860
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5862
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5861
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5863
                MOVE_TACKLE,
                MOVE_SAND_ATTACK,
            },
            },
            {
#line 5866
            .species = SPECIES_SQUIRTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5868
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5867
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5869
                MOVE_TACKLE,
                MOVE_TAIL_WHIP,
            },
            },
        },
    },
#line 5872
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_ROUTE22_EARLY_BULBASAUR] =
    {
#line 5873
        .trainerName = _("TERRY"),
#line 5874
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5875
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5877
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5878
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5879
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5881
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5883
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5882
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5884
                MOVE_TACKLE,
                MOVE_SAND_ATTACK,
            },
            },
            {
#line 5887
            .species = SPECIES_BULBASAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5889
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5888
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5890
                MOVE_TACKLE,
                MOVE_GROWL,
            },
            },
        },
    },
#line 5893
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER] =
    {
#line 5894
        .trainerName = _("TERRY"),
#line 5895
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5896
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5898
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5899
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5900
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 5902
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5904
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5903
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5905
                MOVE_TACKLE,
                MOVE_SAND_ATTACK,
            },
            },
            {
#line 5908
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5910
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5909
            .lvl = 9,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5911
                MOVE_SCRATCH,
                MOVE_GROWL,
            },
            },
        },
    },
#line 5914
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_CERULEAN_SQUIRTLE] =
    {
#line 5915
        .trainerName = _("TERRY"),
#line 5916
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5917
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5919
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5920
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5921
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5923
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5925
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5924
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5926
                MOVE_TACKLE,
                MOVE_SAND_ATTACK,
                MOVE_GUST,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 5931
            .species = SPECIES_ABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5933
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5932
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5934
                MOVE_TELEPORT,
            },
            },
            {
#line 5936
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5938
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5937
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5939
                MOVE_TACKLE,
                MOVE_TAIL_WHIP,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 5943
            .species = SPECIES_SQUIRTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5945
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5944
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5946
                MOVE_TACKLE,
                MOVE_TAIL_WHIP,
                MOVE_WITHDRAW,
                MOVE_WATER_GUN,
            },
            },
        },
    },
#line 5951
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_CERULEAN_BULBASAUR] =
    {
#line 5952
        .trainerName = _("TERRY"),
#line 5953
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5954
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5956
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5957
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5958
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5960
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5962
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5961
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5963
                MOVE_TACKLE,
                MOVE_SAND_ATTACK,
                MOVE_GUST,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 5968
            .species = SPECIES_ABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5970
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5969
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5971
                MOVE_TELEPORT,
            },
            },
            {
#line 5973
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5975
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5974
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5976
                MOVE_TACKLE,
                MOVE_TAIL_WHIP,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 5980
            .species = SPECIES_BULBASAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5982
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 5981
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 5983
                MOVE_SLEEP_POWDER,
                MOVE_POISON_POWDER,
                MOVE_VINE_WHIP,
                MOVE_LEECH_SEED,
            },
            },
        },
    },
#line 5988
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_CERULEAN_CHARMANDER] =
    {
#line 5989
        .trainerName = _("TERRY"),
#line 5990
        .trainerClass = TRAINER_CLASS_RIVAL_EARLY,
#line 5991
        .trainerPic = TRAINER_PIC_RIVAL_EARLY,
        .encounterMusic_gender =
#line 5993
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 5994
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 5995
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 5997
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 5999
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 5998
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6000
                MOVE_TACKLE,
                MOVE_SAND_ATTACK,
                MOVE_GUST,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 6005
            .species = SPECIES_ABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6007
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 6006
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6008
                MOVE_TELEPORT,
            },
            },
            {
#line 6010
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6012
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 6011
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6013
                MOVE_TACKLE,
                MOVE_TAIL_WHIP,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 6017
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6019
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 6018
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6020
                MOVE_METAL_CLAW,
                MOVE_EMBER,
                MOVE_GROWL,
                MOVE_SCRATCH,
            },
            },
        },
    },
#line 6025
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_TED] =
    {
#line 6026
        .trainerName = _("TED"),
#line 6027
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6028
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6030
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6031
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6032
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6034
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6036
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6035
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6038
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6040
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6039
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6042
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_CONNOR] =
    {
#line 6043
        .trainerName = _("CONNOR"),
#line 6044
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6045
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6047
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6048
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6049
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 6051
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6053
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6052
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6054
                MOVE_SCREECH,
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
            },
            },
            {
#line 6059
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6061
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6060
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6062
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 6067
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6069
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6068
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6070
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_SELF_DESTRUCT,
            },
            },
            {
#line 6075
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6077
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6076
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6078
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 6083
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_JERRY] =
    {
#line 6084
        .trainerName = _("JERRY"),
#line 6085
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6086
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6088
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6089
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6090
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6092
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6094
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6093
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6096
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6098
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6097
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6100
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6102
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6101
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6104
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_JOSE] =
    {
#line 6105
        .trainerName = _("JOSE"),
#line 6106
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6107
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6109
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6110
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6111
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6113
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6115
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6114
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6116
                MOVE_SPARK,
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_TACKLE,
            },
            },
            {
#line 6121
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6123
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6122
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6124
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 6129
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_RODNEY] =
    {
#line 6130
        .trainerName = _("RODNEY"),
#line 6131
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6132
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6134
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6135
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6136
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 6138
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6140
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6139
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6142
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_BEAU] =
    {
#line 6143
        .trainerName = _("BEAU"),
#line 6144
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6145
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6147
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6148
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6149
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 6151
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6153
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6152
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6154
                MOVE_SPARK,
                MOVE_THUNDER_WAVE,
                MOVE_SONIC_BOOM,
                MOVE_SUPERSONIC,
            },
            },
            {
#line 6159
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6161
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6160
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6162
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 6167
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6169
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6168
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6170
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 6175
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6177
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6176
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6178
                MOVE_SPARK,
                MOVE_THUNDER_WAVE,
                MOVE_SONIC_BOOM,
                MOVE_SUPERSONIC,
            },
            },
        },
    },
#line 6183
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_TAYLOR] =
    {
#line 6184
        .trainerName = _("TAYLOR"),
#line 6185
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6186
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6188
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6189
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6190
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 6192
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6194
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6193
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6195
                MOVE_SPARK,
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_TACKLE,
            },
            },
            {
#line 6200
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6202
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6201
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6203
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 6208
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6210
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6209
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6211
                MOVE_THUNDER_WAVE,
                MOVE_SONIC_BOOM,
                MOVE_SUPERSONIC,
                MOVE_THUNDER_SHOCK,
            },
            },
            {
#line 6216
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6218
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6217
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6219
                MOVE_THUNDER_WAVE,
                MOVE_SONIC_BOOM,
                MOVE_SUPERSONIC,
                MOVE_THUNDER_SHOCK,
            },
            },
            {
#line 6224
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6226
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6225
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6227
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_SELF_DESTRUCT,
            },
            },
        },
    },
#line 6232
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_JOSHUA] =
    {
#line 6233
        .trainerName = _("JOSHUA"),
#line 6234
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6235
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6237
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6238
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6239
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6241
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6243
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6242
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6245
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6247
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6246
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6249
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_PARKER] =
    {
#line 6250
        .trainerName = _("PARKER"),
#line 6251
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6252
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6254
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6255
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6256
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6258
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6260
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6259
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6262
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6264
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6263
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6266
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_ED] =
    {
#line 6267
        .trainerName = _("ED"),
#line 6268
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6269
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6271
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6272
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6273
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6275
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6277
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6276
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6278
                MOVE_SPARK,
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_TACKLE,
            },
            },
            {
#line 6283
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6285
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6284
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6286
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_TACKLE,
                MOVE_SMOG,
            },
            },
            {
#line 6291
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6293
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6292
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6294
                MOVE_SPARK,
                MOVE_THUNDER_WAVE,
                MOVE_SONIC_BOOM,
                MOVE_SUPERSONIC,
            },
            },
        },
    },
#line 6299
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_TRAVIS] =
    {
#line 6300
        .trainerName = _("TRAVIS"),
#line 6301
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6302
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6304
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6305
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6306
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6308
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6310
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6309
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6312
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6314
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6313
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6316
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_BRAYDON] =
    {
#line 6317
        .trainerName = _("BRAYDON"),
#line 6318
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6319
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6321
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6322
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6323
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6325
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6327
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6326
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6329
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6331
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6330
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6333
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6335
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6334
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6337
    [DIFFICULTY_NORMAL][TRAINER_SCIENTIST_IVAN] =
    {
#line 6338
        .trainerName = _("IVAN"),
#line 6339
        .trainerClass = TRAINER_CLASS_SCIENTIST,
#line 6340
        .trainerPic = TRAINER_PIC_SCIENTIST,
        .encounterMusic_gender =
#line 6342
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 6343
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6344
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6346
            .species = SPECIES_MAGNEMITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6348
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6347
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6350
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6352
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6351
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6354
    [DIFFICULTY_NORMAL][TRAINER_BOSS_GIOVANNI] =
    {
#line 6355
        .trainerName = _("GIOVANNI"),
#line 6356
        .trainerClass = TRAINER_CLASS_BOSS,
#line 6357
        .trainerPic = TRAINER_PIC_LEADER_GIOVANNI,
        .encounterMusic_gender =
#line 6359
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6360
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6361
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6363
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6365
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6364
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6367
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6369
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6368
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6371
            .species = SPECIES_KANGASKHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6373
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6372
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6375
    [DIFFICULTY_NORMAL][TRAINER_BOSS_GIOVANNI_2] =
    {
#line 6376
        .trainerName = _("GIOVANNI"),
#line 6377
        .trainerClass = TRAINER_CLASS_BOSS,
#line 6378
        .trainerPic = TRAINER_PIC_LEADER_GIOVANNI,
        .encounterMusic_gender =
#line 6380
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6381
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6382
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 6384
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6386
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6385
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6388
            .species = SPECIES_KANGASKHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6390
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6389
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6392
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6394
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6393
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6396
            .species = SPECIES_NIDOQUEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6398
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 6397
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6400
    [DIFFICULTY_NORMAL][TRAINER_LEADER_GIOVANNI] =
    {
#line 6401
        .trainerName = _("GIOVANNI"),
#line 6402
        .trainerClass = TRAINER_CLASS_LEADER,
#line 6403
        .trainerPic = TRAINER_PIC_LEADER_GIOVANNI,
        .encounterMusic_gender =
#line 6405
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6406
        .items = { ITEM_HYPER_POTION, ITEM_HYPER_POTION, ITEM_FULL_HEAL },
#line 6407
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6408
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 6410
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6412
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6411
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6413
                MOVE_TAKE_DOWN,
                MOVE_ROCK_BLAST,
                MOVE_SCARY_FACE,
                MOVE_EARTHQUAKE,
            },
            },
            {
#line 6418
            .species = SPECIES_DUGTRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6420
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6419
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6421
                MOVE_SLASH,
                MOVE_SAND_TOMB,
                MOVE_MUD_SLAP,
                MOVE_EARTHQUAKE,
            },
            },
            {
#line 6426
            .species = SPECIES_NIDOQUEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6428
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6427
            .lvl = 44,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6429
                MOVE_BODY_SLAM,
                MOVE_DOUBLE_KICK,
                MOVE_POISON_STING,
                MOVE_EARTHQUAKE,
            },
            },
            {
#line 6434
            .species = SPECIES_NIDOKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6436
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6435
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6437
                MOVE_THRASH,
                MOVE_DOUBLE_KICK,
                MOVE_POISON_STING,
                MOVE_EARTHQUAKE,
            },
            },
            {
#line 6442
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6444
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6443
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6445
                MOVE_TAKE_DOWN,
                MOVE_ROCK_BLAST,
                MOVE_SCARY_FACE,
                MOVE_EARTHQUAKE,
            },
            },
        },
    },
#line 6450
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT] =
    {
#line 6451
        .trainerName = _("GRUNT"),
#line 6452
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6453
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6455
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6456
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6457
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6459
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6461
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6460
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6463
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6465
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6464
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6467
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_2] =
    {
#line 6468
        .trainerName = _("GRUNT"),
#line 6469
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6470
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6472
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6473
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6474
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6476
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6478
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6477
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6480
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6482
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6481
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6484
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6486
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6485
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6488
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_3] =
    {
#line 6489
        .trainerName = _("GRUNT"),
#line 6490
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6491
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6493
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6494
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6495
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6497
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6499
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6498
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6501
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6503
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6502
            .lvl = 11,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6505
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_4] =
    {
#line 6506
        .trainerName = _("GRUNT"),
#line 6507
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6508
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6510
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6511
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6512
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6514
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6516
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6515
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6518
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6520
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6519
            .lvl = 13,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6522
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_5] =
    {
#line 6523
        .trainerName = _("GRUNT"),
#line 6524
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6525
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6527
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6528
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6529
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6531
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6533
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6532
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6535
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6537
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6536
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6539
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_6] =
    {
#line 6540
        .trainerName = _("GRUNT"),
#line 6541
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6542
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6544
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6545
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6546
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6548
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6550
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6549
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6552
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6554
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6553
            .lvl = 15,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6556
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_7] =
    {
#line 6557
        .trainerName = _("GRUNT"),
#line 6558
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6559
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6561
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6562
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6563
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6565
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6567
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6566
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6569
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6571
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6570
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6573
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_8] =
    {
#line 6574
        .trainerName = _("GRUNT"),
#line 6575
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6576
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6578
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6579
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6580
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6582
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6584
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6583
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6586
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6588
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6587
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6590
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_9] =
    {
#line 6591
        .trainerName = _("GRUNT"),
#line 6592
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6593
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6595
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6596
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6597
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6599
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6601
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6600
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6603
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6605
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6604
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6607
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_10] =
    {
#line 6608
        .trainerName = _("GRUNT"),
#line 6609
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6610
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6612
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6613
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6614
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6616
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6618
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6617
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6619
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
                MOVE_HARDEN,
            },
            },
            {
#line 6624
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6626
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6625
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6627
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
            {
#line 6631
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6633
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6632
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6634
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
        },
    },
#line 6638
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_11] =
    {
#line 6639
        .trainerName = _("GRUNT"),
#line 6640
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6641
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6643
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6644
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6645
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 6647
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6649
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6648
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6651
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6653
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6652
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6655
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6657
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6656
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6659
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6661
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6660
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6663
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_12] =
    {
#line 6664
        .trainerName = _("GRUNT"),
#line 6665
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6666
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6668
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6669
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6670
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6672
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6674
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6673
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6675
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
                MOVE_HARDEN,
            },
            },
            {
#line 6680
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6682
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6681
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6683
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
        },
    },
#line 6688
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_13] =
    {
#line 6689
        .trainerName = _("GRUNT"),
#line 6690
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6691
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6693
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6694
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6695
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 6697
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6699
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6698
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6700
                MOVE_BITE,
                MOVE_ASTONISH,
                MOVE_SUPERSONIC,
                MOVE_LEECH_LIFE,
            },
            },
            {
#line 6705
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6707
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6706
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6708
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
            {
#line 6712
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6714
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6713
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6715
                MOVE_SLUDGE,
                MOVE_DISABLE,
                MOVE_HARDEN,
                MOVE_POUND,
            },
            },
            {
#line 6720
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6722
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6721
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6723
                MOVE_BITE,
                MOVE_ASTONISH,
                MOVE_SUPERSONIC,
                MOVE_LEECH_LIFE,
            },
            },
            {
#line 6728
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6730
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6729
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 6731
                MOVE_HYPER_FANG,
                MOVE_QUICK_ATTACK,
                MOVE_TAIL_WHIP,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 6736
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_14] =
    {
#line 6737
        .trainerName = _("GRUNT"),
#line 6738
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6739
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6741
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6742
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6743
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6745
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6747
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6746
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6749
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6751
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6750
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6753
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6755
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6754
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6757
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_15] =
    {
#line 6758
        .trainerName = _("GRUNT"),
#line 6759
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6760
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6762
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6763
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6764
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6766
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6768
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6767
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6770
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6772
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6771
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6774
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_16] =
    {
#line 6775
        .trainerName = _("GRUNT"),
#line 6776
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6777
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6779
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6780
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6781
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6783
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6785
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6784
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6787
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6789
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6788
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6791
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6793
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6792
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6795
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_17] =
    {
#line 6796
        .trainerName = _("GRUNT"),
#line 6797
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6798
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6800
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6801
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6802
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6804
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6806
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6805
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6808
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6810
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6809
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6812
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6814
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6813
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6816
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_18] =
    {
#line 6817
        .trainerName = _("GRUNT"),
#line 6818
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6819
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6821
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6822
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6823
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6825
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6827
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6826
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6829
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6831
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6830
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6833
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_19] =
    {
#line 6834
        .trainerName = _("GRUNT"),
#line 6835
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6836
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6838
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6839
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6840
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6842
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6844
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6843
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6846
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6848
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6847
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6850
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6852
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6851
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6854
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_20] =
    {
#line 6855
        .trainerName = _("GRUNT"),
#line 6856
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6857
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6859
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6860
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6861
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6863
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6865
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6864
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6867
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6869
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6868
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6871
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_21] =
    {
#line 6872
        .trainerName = _("GRUNT"),
#line 6873
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6874
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6876
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6877
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6878
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 6880
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6882
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6881
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6884
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6886
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6885
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6888
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6890
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6889
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6892
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6894
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6893
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6896
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_22] =
    {
#line 6897
        .trainerName = _("GRUNT"),
#line 6898
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6899
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6901
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6902
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6903
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6905
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6907
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6906
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6909
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6911
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6910
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6913
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_23] =
    {
#line 6914
        .trainerName = _("GRUNT"),
#line 6915
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6916
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6918
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6919
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6920
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6922
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6924
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6923
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6926
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6928
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6927
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6930
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_24] =
    {
#line 6931
        .trainerName = _("GRUNT"),
#line 6932
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6933
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6935
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6936
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6937
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 6939
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6941
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6940
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6943
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6945
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6944
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6947
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6949
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6948
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6951
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6953
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6952
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6955
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6957
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6956
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6959
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_25] =
    {
#line 6960
        .trainerName = _("GRUNT"),
#line 6961
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6962
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6964
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6965
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6966
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 6968
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6970
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6969
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6972
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6974
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6973
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6976
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6978
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6977
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6980
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_26] =
    {
#line 6981
        .trainerName = _("GRUNT"),
#line 6982
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 6983
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 6985
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 6986
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 6987
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 6989
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6991
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6990
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 6993
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 6995
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 6994
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 6997
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_27] =
    {
#line 6998
        .trainerName = _("GRUNT"),
#line 6999
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7000
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7002
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7003
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7004
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 7006
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7008
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7007
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7010
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7012
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7011
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7014
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7016
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7015
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7018
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_28] =
    {
#line 7019
        .trainerName = _("GRUNT"),
#line 7020
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7021
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7023
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7024
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7025
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 7027
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7029
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7028
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7031
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_29] =
    {
#line 7032
        .trainerName = _("GRUNT"),
#line 7033
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7034
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7036
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7037
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7038
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 7040
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7042
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7041
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7044
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_30] =
    {
#line 7045
        .trainerName = _("GRUNT"),
#line 7046
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7047
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7049
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7050
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7051
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 7053
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7055
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7054
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7057
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7059
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7058
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7061
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_31] =
    {
#line 7062
        .trainerName = _("GRUNT"),
#line 7063
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7064
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7066
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7067
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7068
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 7070
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7072
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7071
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7074
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7076
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7075
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7078
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7080
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7079
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7082
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_32] =
    {
#line 7083
        .trainerName = _("GRUNT"),
#line 7084
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7085
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7087
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7088
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7089
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 7091
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7093
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7092
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7094
                MOVE_SCARY_FACE,
                MOVE_HYPER_FANG,
                MOVE_QUICK_ATTACK,
                MOVE_TAIL_WHIP,
            },
            },
            {
#line 7099
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7101
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7100
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7102
                MOVE_GLARE,
                MOVE_BITE,
                MOVE_POISON_STING,
                MOVE_LEER,
            },
            },
            {
#line 7107
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7109
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7108
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7110
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 7115
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7117
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7116
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7118
                MOVE_WING_ATTACK,
                MOVE_BITE,
                MOVE_ASTONISH,
                MOVE_SUPERSONIC,
            },
            },
        },
    },
#line 7123
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_33] =
    {
#line 7124
        .trainerName = _("GRUNT"),
#line 7125
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7126
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7128
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7129
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7130
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 7132
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7134
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7133
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7136
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7138
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7137
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7140
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_34] =
    {
#line 7141
        .trainerName = _("GRUNT"),
#line 7142
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7143
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7145
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7146
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7147
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 7149
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7151
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7150
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7153
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7155
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7154
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7157
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_35] =
    {
#line 7158
        .trainerName = _("GRUNT"),
#line 7159
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7160
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7162
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7163
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7164
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 7166
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7168
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7167
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7170
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7172
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7171
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7174
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7176
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7175
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7178
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7180
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7179
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7182
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_36] =
    {
#line 7183
        .trainerName = _("GRUNT"),
#line 7184
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7185
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7187
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7188
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7189
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 7191
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7193
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7192
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7195
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7197
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7196
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7199
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7201
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7200
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7203
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_37] =
    {
#line 7204
        .trainerName = _("GRUNT"),
#line 7205
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7206
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7208
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7209
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7210
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 7212
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7214
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7213
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7216
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7218
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7217
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7220
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7222
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7221
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7224
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_38] =
    {
#line 7225
        .trainerName = _("GRUNT"),
#line 7226
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7227
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7229
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7230
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7231
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 7233
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7235
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7234
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7237
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7239
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7238
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7241
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7243
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7242
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7245
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_39] =
    {
#line 7246
        .trainerName = _("GRUNT"),
#line 7247
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7248
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7250
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7251
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7252
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 7254
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7256
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7255
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7258
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_40] =
    {
#line 7259
        .trainerName = _("GRUNT"),
#line 7260
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7261
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7263
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7264
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7265
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7267
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7269
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7268
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7271
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7273
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7272
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7275
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7277
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7276
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7279
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7281
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7280
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7283
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7285
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7284
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7287
    [DIFFICULTY_NORMAL][TRAINER_TEAM_ROCKET_GRUNT_41] =
    {
#line 7288
        .trainerName = _("GRUNT"),
#line 7289
        .trainerClass = TRAINER_CLASS_TEAM_ROCKET,
#line 7290
        .trainerPic = TRAINER_PIC_ROCKET_GRUNT_M,
        .encounterMusic_gender =
#line 7292
            TRAINER_ENCOUNTER_MUSIC_AQUA,
#line 7293
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7294
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 7296
            .species = SPECIES_CUBONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7298
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7297
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7300
            .species = SPECIES_DROWZEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7302
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7301
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 7304
            .species = SPECIES_MAROWAK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7306
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 7305
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 7308
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_SAMUEL] =
    {
#line 7309
        .trainerName = _("SAMUEL"),
#line 7310
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7311
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7313
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7314
        .items = { ITEM_SUPER_POTION },
#line 7315
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7316
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7318
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7320
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7319
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7321
                MOVE_SLASH,
                MOVE_SWIFT,
                MOVE_SAND_ATTACK,
                MOVE_POISON_STING,
            },
            },
            {
#line 7326
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7328
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7327
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7329
                MOVE_SLASH,
                MOVE_SWIFT,
                MOVE_SAND_ATTACK,
                MOVE_POISON_STING,
            },
            },
            {
#line 7334
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7336
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7335
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7337
                MOVE_TAKE_DOWN,
                MOVE_ROCK_BLAST,
                MOVE_FURY_ATTACK,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 7342
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7344
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7343
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7345
                MOVE_FURY_ATTACK,
                MOVE_HORN_ATTACK,
                MOVE_POISON_STING,
                MOVE_DOUBLE_KICK,
            },
            },
            {
#line 7350
            .species = SPECIES_NIDOKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7352
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7351
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7353
                MOVE_THRASH,
                MOVE_DOUBLE_KICK,
                MOVE_POISON_STING,
                MOVE_FOCUS_ENERGY,
            },
            },
        },
    },
#line 7358
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_GEORGE] =
    {
#line 7359
        .trainerName = _("GEORGE"),
#line 7360
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7361
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7363
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7364
        .items = { ITEM_HYPER_POTION },
#line 7365
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7366
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7368
            .species = SPECIES_EXEGGUTOR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7370
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7369
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7371
                MOVE_EGG_BOMB,
                MOVE_CONFUSION,
                MOVE_STUN_SPORE,
                MOVE_SLEEP_POWDER,
            },
            },
            {
#line 7376
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7378
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7377
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7379
                MOVE_FURY_SWIPES,
                MOVE_SWIFT,
                MOVE_POISON_STING,
                MOVE_SAND_ATTACK,
            },
            },
            {
#line 7384
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7386
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7385
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7387
                MOVE_SPIKE_CANNON,
                MOVE_SPIKES,
                MOVE_AURORA_BEAM,
                MOVE_SUPERSONIC,
            },
            },
            {
#line 7392
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7394
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7393
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7395
                MOVE_SPARK,
                MOVE_SONIC_BOOM,
                MOVE_SCREECH,
                MOVE_LIGHT_SCREEN,
            },
            },
            {
#line 7400
            .species = SPECIES_ARCANINE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7402
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7401
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7403
                MOVE_FLAME_WHEEL,
                MOVE_ROAR,
                MOVE_BITE,
                MOVE_TAKE_DOWN,
            },
            },
        },
    },
#line 7408
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_COLBY] =
    {
#line 7409
        .trainerName = _("COLBY"),
#line 7410
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7411
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7413
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7414
        .items = { ITEM_HYPER_POTION },
#line 7415
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7416
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7418
            .species = SPECIES_KINGLER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7420
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7419
            .lvl = 41,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7421
                MOVE_GUILLOTINE,
                MOVE_STOMP,
                MOVE_MUD_SHOT,
                MOVE_BUBBLE,
            },
            },
            {
#line 7426
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7428
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7427
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7429
                MOVE_BODY_SLAM,
                MOVE_DOUBLE_SLAP,
                MOVE_WATER_GUN,
                MOVE_HYPNOSIS,
            },
            },
            {
#line 7434
            .species = SPECIES_TENTACRUEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7436
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7435
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7437
                MOVE_BARRIER,
                MOVE_WRAP,
                MOVE_BUBBLE_BEAM,
                MOVE_ACID,
            },
            },
            {
#line 7442
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7444
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7443
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7445
                MOVE_WATER_GUN,
                MOVE_SMOKESCREEN,
                MOVE_TWISTER,
                MOVE_LEER,
            },
            },
            {
#line 7450
            .species = SPECIES_BLASTOISE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7452
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7451
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7453
                MOVE_WATER_GUN,
                MOVE_BITE,
                MOVE_RAPID_SPIN,
                MOVE_RAIN_DANCE,
            },
            },
        },
    },
#line 7458
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_PAUL] =
    {
#line 7459
        .trainerName = _("PAUL"),
#line 7460
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7461
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7463
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7464
        .items = { ITEM_FULL_RESTORE },
#line 7465
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7466
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7468
            .species = SPECIES_SLOWPOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7470
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7469
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7471
                MOVE_HEADBUTT,
                MOVE_CONFUSION,
                MOVE_WATER_GUN,
                MOVE_DISABLE,
            },
            },
            {
#line 7476
            .species = SPECIES_SHELLDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7478
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7477
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7479
                MOVE_AURORA_BEAM,
                MOVE_CLAMP,
                MOVE_SUPERSONIC,
                MOVE_LEER,
            },
            },
            {
#line 7484
            .species = SPECIES_KINGLER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7486
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7485
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7487
                MOVE_GUILLOTINE,
                MOVE_STOMP,
                MOVE_MUD_SHOT,
                MOVE_BUBBLE,
            },
            },
            {
#line 7492
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7494
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7493
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7495
                MOVE_BUBBLE_BEAM,
                MOVE_SWIFT,
                MOVE_RECOVER,
                MOVE_RAPID_SPIN,
            },
            },
            {
#line 7500
            .species = SPECIES_GOLDUCK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7502
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7501
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7503
                MOVE_CONFUSION,
                MOVE_SCRATCH,
                MOVE_SCREECH,
                MOVE_DISABLE,
            },
            },
        },
    },
#line 7508
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_ROLANDO] =
    {
#line 7509
        .trainerName = _("ROLANDO"),
#line 7510
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7511
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7513
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7514
        .items = { ITEM_HYPER_POTION },
#line 7515
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7516
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7518
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7520
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7519
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7521
                MOVE_SUPER_FANG,
                MOVE_PURSUIT,
                MOVE_SCARY_FACE,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 7526
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7528
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7527
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7529
                MOVE_RAZOR_LEAF,
                MOVE_SLEEP_POWDER,
                MOVE_SWEET_SCENT,
                MOVE_SYNTHESIS,
            },
            },
            {
#line 7534
            .species = SPECIES_WARTORTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7536
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7535
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7537
                MOVE_WATER_GUN,
                MOVE_BITE,
                MOVE_RAPID_SPIN,
                MOVE_TAIL_WHIP,
            },
            },
            {
#line 7542
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7544
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7543
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7545
                MOVE_FLAMETHROWER,
                MOVE_SLASH,
                MOVE_SMOKESCREEN,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 7550
            .species = SPECIES_CHARIZARD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7552
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7551
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7553
                MOVE_FLAMETHROWER,
                MOVE_WING_ATTACK,
                MOVE_SMOKESCREEN,
                MOVE_SCARY_FACE,
            },
            },
        },
    },
#line 7558
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_GILBERT] =
    {
#line 7559
        .trainerName = _("GILBERT"),
#line 7560
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7561
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7563
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7564
        .items = { ITEM_HYPER_POTION },
#line 7565
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7566
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7568
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7570
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7569
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7571
                MOVE_WING_ATTACK,
                MOVE_FEATHER_DANCE,
                MOVE_WHIRLWIND,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 7576
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7578
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7577
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7579
                MOVE_DRILL_PECK,
                MOVE_MIRROR_MOVE,
                MOVE_PURSUIT,
                MOVE_LEER,
            },
            },
            {
#line 7584
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7586
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7585
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7587
                MOVE_PAY_DAY,
                MOVE_FAINT_ATTACK,
                MOVE_SCREECH,
                MOVE_BITE,
            },
            },
            {
#line 7592
            .species = SPECIES_LICKITUNG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7594
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7593
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7595
                MOVE_SLAM,
                MOVE_DISABLE,
                MOVE_WRAP,
                MOVE_SUPERSONIC,
            },
            },
            {
#line 7600
            .species = SPECIES_TAUROS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7602
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7601
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7603
                MOVE_HORN_ATTACK,
                MOVE_SCARY_FACE,
                MOVE_SWAGGER,
                MOVE_TAIL_WHIP,
            },
            },
        },
    },
#line 7608
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_OWEN] =
    {
#line 7609
        .trainerName = _("OWEN"),
#line 7610
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7611
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7613
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7614
        .items = { ITEM_HYPER_POTION },
#line 7615
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7616
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7618
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7620
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7619
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7621
                MOVE_SCRATCH,
                MOVE_POISON_STING,
                MOVE_DOUBLE_KICK,
                MOVE_BITE,
            },
            },
            {
#line 7626
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7628
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7627
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7629
                MOVE_HORN_ATTACK,
                MOVE_POISON_STING,
                MOVE_DOUBLE_KICK,
                MOVE_LEER,
            },
            },
            {
#line 7634
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7636
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7635
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7637
                MOVE_SUPER_FANG,
                MOVE_PURSUIT,
                MOVE_SCARY_FACE,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 7642
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7644
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7643
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7645
                MOVE_FURY_SWIPES,
                MOVE_SWIFT,
                MOVE_SLASH,
                MOVE_POISON_STING,
            },
            },
            {
#line 7650
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7652
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7651
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7653
                MOVE_ROCK_BLAST,
                MOVE_SCARY_FACE,
                MOVE_STOMP,
                MOVE_TAIL_WHIP,
            },
            },
        },
    },
#line 7658
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_BERKE] =
    {
#line 7659
        .trainerName = _("BERKE"),
#line 7660
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7661
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7663
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7664
        .items = { ITEM_FULL_RESTORE },
#line 7665
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7666
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7668
            .species = SPECIES_SEEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7670
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7669
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7671
                MOVE_TAKE_DOWN,
                MOVE_AURORA_BEAM,
                MOVE_ICY_WIND,
                MOVE_GROWL,
            },
            },
            {
#line 7676
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7678
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7677
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7679
                MOVE_ROCK_BLAST,
                MOVE_MAGNITUDE,
                MOVE_ROCK_THROW,
                MOVE_MUD_SPORT,
            },
            },
            {
#line 7684
            .species = SPECIES_KINGLER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7686
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7685
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7687
                MOVE_GUILLOTINE,
                MOVE_STOMP,
                MOVE_MUD_SHOT,
                MOVE_BUBBLE,
            },
            },
            {
#line 7692
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7694
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7693
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7695
                MOVE_SLAM,
                MOVE_SANDSTORM,
                MOVE_DRAGON_BREATH,
                MOVE_ROCK_THROW,
            },
            },
            {
#line 7700
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7702
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7701
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7703
                MOVE_SPIKE_CANNON,
                MOVE_AURORA_BEAM,
                MOVE_SUPERSONIC,
                MOVE_PROTECT,
            },
            },
        },
    },
#line 7708
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_YUJI] =
    {
#line 7709
        .trainerName = _("YUJI"),
#line 7710
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7711
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7713
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7714
        .items = { ITEM_HYPER_POTION },
#line 7715
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7716
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7718
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7720
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7719
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7721
                MOVE_SLASH,
                MOVE_SWIFT,
                MOVE_SAND_ATTACK,
                MOVE_POISON_STING,
            },
            },
            {
#line 7726
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7728
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7727
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7729
                MOVE_ROCK_BLAST,
                MOVE_MAGNITUDE,
                MOVE_MUD_SPORT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 7734
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7736
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7735
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7737
                MOVE_DRAGON_BREATH,
                MOVE_SANDSTORM,
                MOVE_ROCK_THROW,
                MOVE_BIND,
            },
            },
            {
#line 7742
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7744
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7743
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7745
                MOVE_ROCK_BLAST,
                MOVE_MAGNITUDE,
                MOVE_ROLLOUT,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 7750
            .species = SPECIES_MAROWAK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7752
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7751
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7753
                MOVE_BONEMERANG,
                MOVE_HEADBUTT,
                MOVE_LEER,
                MOVE_GROWL,
            },
            },
        },
    },
#line 7758
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_WARREN] =
    {
#line 7759
        .trainerName = _("WARREN"),
#line 7760
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7761
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 7763
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7764
        .items = { ITEM_HYPER_POTION },
#line 7765
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7766
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7768
            .species = SPECIES_MAROWAK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7770
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7769
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7771
                MOVE_BONEMERANG,
                MOVE_HEADBUTT,
                MOVE_LEER,
                MOVE_GROWL,
            },
            },
            {
#line 7776
            .species = SPECIES_MAROWAK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7778
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7777
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7779
                MOVE_BONEMERANG,
                MOVE_HEADBUTT,
                MOVE_LEER,
                MOVE_GROWL,
            },
            },
            {
#line 7784
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7786
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7785
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7787
                MOVE_TAKE_DOWN,
                MOVE_ROCK_BLAST,
                MOVE_FURY_ATTACK,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 7792
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7794
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7793
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7795
                MOVE_FURY_SWIPES,
                MOVE_BITE,
                MOVE_POISON_STING,
                MOVE_DOUBLE_KICK,
            },
            },
            {
#line 7800
            .species = SPECIES_NIDOQUEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7802
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7801
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7803
                MOVE_BODY_SLAM,
                MOVE_BITE,
                MOVE_POISON_STING,
                MOVE_DOUBLE_KICK,
            },
            },
        },
    },
#line 7808
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_MARY] =
    {
#line 7809
        .trainerName = _("MARY"),
#line 7810
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7811
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 7813
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7814
        .items = { ITEM_SUPER_POTION },
#line 7815
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7816
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7818
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7820
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7819
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7821
                MOVE_WRAP,
                MOVE_STUN_SPORE,
                MOVE_POISON_POWDER,
                MOVE_GROWTH,
            },
            },
            {
#line 7826
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7828
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7827
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7829
                MOVE_POISON_POWDER,
                MOVE_STUN_SPORE,
                MOVE_ABSORB,
                MOVE_SWEET_SCENT,
            },
            },
            {
#line 7834
            .species = SPECIES_WEEPINBELL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7836
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7835
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7837
                MOVE_VINE_WHIP,
                MOVE_STUN_SPORE,
                MOVE_POISON_POWDER,
                MOVE_GROWTH,
            },
            },
            {
#line 7842
            .species = SPECIES_GLOOM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7844
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7843
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7845
                MOVE_ABSORB,
                MOVE_STUN_SPORE,
                MOVE_POISON_POWDER,
                MOVE_SWEET_SCENT,
            },
            },
            {
#line 7850
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7852
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7851
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7853
                MOVE_RAZOR_LEAF,
                MOVE_SLEEP_POWDER,
                MOVE_VINE_WHIP,
                MOVE_LEECH_SEED,
            },
            },
        },
    },
#line 7858
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_CAROLINE] =
    {
#line 7859
        .trainerName = _("CAROLINE"),
#line 7860
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7861
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 7863
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7864
        .items = { ITEM_HYPER_POTION },
#line 7865
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7866
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7868
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7870
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7869
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7871
                MOVE_RAZOR_LEAF,
                MOVE_ACID,
                MOVE_STUN_SPORE,
                MOVE_POISON_POWDER,
            },
            },
            {
#line 7876
            .species = SPECIES_WEEPINBELL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7878
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7877
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7879
                MOVE_RAZOR_LEAF,
                MOVE_ACID,
                MOVE_SLEEP_POWDER,
                MOVE_POISON_POWDER,
            },
            },
            {
#line 7884
            .species = SPECIES_VICTREEBEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7886
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7885
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7887
                MOVE_RAZOR_LEAF,
                MOVE_ACID,
                MOVE_STUN_SPORE,
                MOVE_SLEEP_POWDER,
            },
            },
            {
#line 7892
            .species = SPECIES_PARAS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7894
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7893
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7895
                MOVE_GROWTH,
                MOVE_SLASH,
                MOVE_LEECH_LIFE,
                MOVE_STUN_SPORE,
            },
            },
            {
#line 7900
            .species = SPECIES_PARASECT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7902
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7901
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7903
                MOVE_SPORE,
                MOVE_SLASH,
                MOVE_LEECH_LIFE,
                MOVE_POISON_POWDER,
            },
            },
        },
    },
#line 7908
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_ALEXA] =
    {
#line 7909
        .trainerName = _("ALEXA"),
#line 7910
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7911
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 7913
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7914
        .items = { ITEM_FULL_RESTORE },
#line 7915
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7916
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7918
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7920
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7919
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7921
                MOVE_LIGHT_SCREEN,
                MOVE_COSMIC_POWER,
                MOVE_DOUBLE_SLAP,
                MOVE_ENCORE,
            },
            },
            {
#line 7926
            .species = SPECIES_JIGGLYPUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7928
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7927
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7929
                MOVE_SING,
                MOVE_BODY_SLAM,
                MOVE_ROLLOUT,
                MOVE_DISABLE,
            },
            },
            {
#line 7934
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7936
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7935
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7937
                MOVE_PAY_DAY,
                MOVE_FAINT_ATTACK,
                MOVE_BITE,
                MOVE_SCREECH,
            },
            },
            {
#line 7942
            .species = SPECIES_DEWGONG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7944
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7943
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7945
                MOVE_SHEER_COLD,
                MOVE_TAKE_DOWN,
                MOVE_REST,
                MOVE_AURORA_BEAM,
            },
            },
            {
#line 7950
            .species = SPECIES_CHANSEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7952
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7951
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7953
                MOVE_SING,
                MOVE_EGG_BOMB,
                MOVE_SOFT_BOILED,
                MOVE_MINIMIZE,
            },
            },
        },
    },
#line 7958
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_SHANNON] =
    {
#line 7959
        .trainerName = _("SHANNON"),
#line 7960
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 7961
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 7963
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 7964
        .items = { ITEM_FULL_RESTORE },
#line 7965
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 7966
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 7968
            .species = SPECIES_BEEDRILL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7970
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7969
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7971
                MOVE_PIN_MISSILE,
                MOVE_TWINEEDLE,
                MOVE_AGILITY,
                MOVE_PURSUIT,
            },
            },
            {
#line 7976
            .species = SPECIES_BUTTERFREE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7978
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7977
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7979
                MOVE_SAFEGUARD,
                MOVE_PSYBEAM,
                MOVE_GUST,
                MOVE_SUPERSONIC,
            },
            },
            {
#line 7984
            .species = SPECIES_PARASECT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7986
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7985
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7987
                MOVE_SPORE,
                MOVE_LEECH_LIFE,
                MOVE_SLASH,
                MOVE_GROWTH,
            },
            },
            {
#line 7992
            .species = SPECIES_VENONAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 7994
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 7993
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 7995
                MOVE_PSYBEAM,
                MOVE_STUN_SPORE,
                MOVE_LEECH_LIFE,
                MOVE_DISABLE,
            },
            },
            {
#line 8000
            .species = SPECIES_VENOMOTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8002
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8001
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8003
                MOVE_PSYBEAM,
                MOVE_GUST,
                MOVE_SUPERSONIC,
                MOVE_LEECH_LIFE,
            },
            },
        },
    },
#line 8008
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_NAOMI] =
    {
#line 8009
        .trainerName = _("NAOMI"),
#line 8010
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 8011
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 8013
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 8014
        .items = { ITEM_HYPER_POTION },
#line 8015
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8016
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8018
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8020
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8019
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8021
                MOVE_FURY_SWIPES,
                MOVE_SCREECH,
                MOVE_FAINT_ATTACK,
                MOVE_PAY_DAY,
            },
            },
            {
#line 8026
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8028
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8027
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8029
                MOVE_AGILITY,
                MOVE_TAKE_DOWN,
                MOVE_FIRE_SPIN,
                MOVE_STOMP,
            },
            },
            {
#line 8034
            .species = SPECIES_RAPIDASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8036
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8035
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8037
                MOVE_FURY_ATTACK,
                MOVE_FIRE_SPIN,
                MOVE_STOMP,
                MOVE_GROWL,
            },
            },
            {
#line 8042
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8044
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8043
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8045
                MOVE_FLAMETHROWER,
                MOVE_CONFUSE_RAY,
                MOVE_QUICK_ATTACK,
                MOVE_IMPRISON,
            },
            },
            {
#line 8050
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8052
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8051
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8053
                MOVE_SAFEGUARD,
                MOVE_WILL_O_WISP,
                MOVE_CONFUSE_RAY,
                MOVE_FIRE_SPIN,
            },
            },
        },
    },
#line 8058
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_BROOKE] =
    {
#line 8059
        .trainerName = _("BROOKE"),
#line 8060
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 8061
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 8063
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 8064
        .items = { ITEM_FULL_RESTORE },
#line 8065
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8066
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8068
            .species = SPECIES_TANGELA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8070
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8069
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8071
                MOVE_SLAM,
                MOVE_BIND,
                MOVE_MEGA_DRAIN,
                MOVE_INGRAIN,
            },
            },
            {
#line 8076
            .species = SPECIES_GLOOM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8078
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8077
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8079
                MOVE_ACID,
                MOVE_MOONLIGHT,
                MOVE_SLEEP_POWDER,
                MOVE_STUN_SPORE,
            },
            },
            {
#line 8084
            .species = SPECIES_VILEPLUME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8086
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8085
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8087
                MOVE_MEGA_DRAIN,
                MOVE_ACID,
                MOVE_STUN_SPORE,
                MOVE_AROMATHERAPY,
            },
            },
            {
#line 8092
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8094
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8093
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8095
                MOVE_RAZOR_LEAF,
                MOVE_SWEET_SCENT,
                MOVE_GROWL,
                MOVE_LEECH_SEED,
            },
            },
            {
#line 8100
            .species = SPECIES_VENUSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8102
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8101
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8103
                MOVE_RAZOR_LEAF,
                MOVE_GROWTH,
                MOVE_SLEEP_POWDER,
                MOVE_POISON_POWDER,
            },
            },
        },
    },
#line 8108
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_AUSTINA] =
    {
#line 8109
        .trainerName = _("AUSTINA"),
#line 8110
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 8111
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 8113
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 8114
        .items = { ITEM_FULL_RESTORE },
#line 8115
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8116
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8118
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8120
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8119
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8121
                MOVE_HORN_DRILL,
                MOVE_ROCK_BLAST,
                MOVE_SCARY_FACE,
                MOVE_STOMP,
            },
            },
            {
#line 8126
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8128
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8127
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8129
                MOVE_DOUBLE_KICK,
                MOVE_FURY_SWIPES,
                MOVE_BITE,
                MOVE_FLATTER,
            },
            },
            {
#line 8134
            .species = SPECIES_NIDOQUEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8136
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8135
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8137
                MOVE_BODY_SLAM,
                MOVE_DOUBLE_KICK,
                MOVE_BITE,
                MOVE_GROWL,
            },
            },
            {
#line 8142
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8144
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8143
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8145
                MOVE_HORN_ATTACK,
                MOVE_POISON_STING,
                MOVE_FOCUS_ENERGY,
                MOVE_LEER,
            },
            },
            {
#line 8150
            .species = SPECIES_NIDOKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8152
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8151
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8153
                MOVE_THRASH,
                MOVE_DOUBLE_KICK,
                MOVE_POISON_STING,
                MOVE_PECK,
            },
            },
        },
    },
#line 8158
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_JULIE] =
    {
#line 8159
        .trainerName = _("JULIE"),
#line 8160
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 8161
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 8163
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 8164
        .items = { ITEM_HYPER_POTION },
#line 8165
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8166
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8168
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8170
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8169
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8171
                MOVE_FURY_SWIPES,
                MOVE_BITE,
                MOVE_SCREECH,
                MOVE_FAINT_ATTACK,
            },
            },
            {
#line 8176
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8178
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8177
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8179
                MOVE_FLAMETHROWER,
                MOVE_WILL_O_WISP,
                MOVE_CONFUSE_RAY,
                MOVE_GRUDGE,
            },
            },
            {
#line 8184
            .species = SPECIES_RAPIDASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8186
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8185
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8187
                MOVE_FURY_ATTACK,
                MOVE_FIRE_SPIN,
                MOVE_TAKE_DOWN,
                MOVE_AGILITY,
            },
            },
            {
#line 8192
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8194
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8193
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8195
                MOVE_THUNDERBOLT,
                MOVE_THUNDER_WAVE,
                MOVE_DOUBLE_TEAM,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 8200
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8202
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8201
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8203
                MOVE_THUNDER,
                MOVE_THUNDER_WAVE,
                MOVE_SLAM,
                MOVE_DOUBLE_TEAM,
            },
            },
        },
    },
#line 8208
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_LORELEI] =
    {
#line 8209
        .trainerName = _("LORELEI"),
#line 8210
        .trainerClass = TRAINER_CLASS_ELITE_FOUR,
#line 8211
        .trainerPic = TRAINER_PIC_ELITE_FOUR_LORELEI,
        .encounterMusic_gender =
#line 8213
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 8214
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 8215
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8216
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 8217
        .mugshotColor = MUGSHOT_COLOR_PURPLE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8219
            .species = SPECIES_DEWGONG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8221
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8220
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8222
                MOVE_ICE_BEAM,
                MOVE_SURF,
                MOVE_HAIL,
                MOVE_SAFEGUARD,
            },
            },
            {
#line 8227
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8229
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8228
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8230
                MOVE_SPIKES,
                MOVE_PROTECT,
                MOVE_HAIL,
                MOVE_DIVE,
            },
            },
            {
#line 8235
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8237
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8236
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8238
                MOVE_ICE_BEAM,
                MOVE_SURF,
                MOVE_AMNESIA,
                MOVE_YAWN,
            },
            },
            {
#line 8243
            .species = SPECIES_JYNX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8245
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8244
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8246
                MOVE_ICE_PUNCH,
                MOVE_DOUBLE_SLAP,
                MOVE_LOVELY_KISS,
                MOVE_ATTRACT,
            },
            },
            {
#line 8251
            .species = SPECIES_LAPRAS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8251
            .heldItem = ITEM_SITRUS_BERRY,
#line 8253
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8252
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8254
                MOVE_CONFUSE_RAY,
                MOVE_ICE_BEAM,
                MOVE_SURF,
                MOVE_BODY_SLAM,
            },
            },
        },
    },
#line 8259
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_BRUNO] =
    {
#line 8260
        .trainerName = _("BRUNO"),
#line 8261
        .trainerClass = TRAINER_CLASS_ELITE_FOUR,
#line 8262
        .trainerPic = TRAINER_PIC_ELITE_FOUR_BRUNO,
        .encounterMusic_gender =
#line 8264
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 8265
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 8266
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8267
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 8268
        .mugshotColor = MUGSHOT_COLOR_GREEN,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8270
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8272
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8271
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8273
                MOVE_EARTHQUAKE,
                MOVE_ROCK_TOMB,
                MOVE_IRON_TAIL,
                MOVE_ROAR,
            },
            },
            {
#line 8278
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8280
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8279
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8281
                MOVE_SKY_UPPERCUT,
                MOVE_MACH_PUNCH,
                MOVE_ROCK_TOMB,
                MOVE_COUNTER,
            },
            },
            {
#line 8286
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8288
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8287
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8289
                MOVE_MEGA_KICK,
                MOVE_FORESIGHT,
                MOVE_BRICK_BREAK,
                MOVE_FACADE,
            },
            },
            {
#line 8294
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8296
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8295
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8297
                MOVE_DOUBLE_EDGE,
                MOVE_EARTHQUAKE,
                MOVE_IRON_TAIL,
                MOVE_SAND_TOMB,
            },
            },
            {
#line 8302
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8302
            .heldItem = ITEM_SITRUS_BERRY,
#line 8304
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8303
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8305
                MOVE_CROSS_CHOP,
                MOVE_BULK_UP,
                MOVE_SCARY_FACE,
                MOVE_ROCK_TOMB,
            },
            },
        },
    },
#line 8310
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_AGATHA] =
    {
#line 8311
        .trainerName = _("AGATHA"),
#line 8312
        .trainerClass = TRAINER_CLASS_ELITE_FOUR,
#line 8313
        .trainerPic = TRAINER_PIC_ELITE_FOUR_AGATHA,
        .encounterMusic_gender =
#line 8315
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 8316
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 8317
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8318
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 8319
        .mugshotColor = MUGSHOT_COLOR_PINK,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8321
            .species = SPECIES_GENGAR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8323
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8322
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8324
                MOVE_SHADOW_PUNCH,
                MOVE_CONFUSE_RAY,
                MOVE_TOXIC,
                MOVE_DOUBLE_TEAM,
            },
            },
            {
#line 8329
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8331
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8330
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8332
                MOVE_CONFUSE_RAY,
                MOVE_POISON_FANG,
                MOVE_AIR_CUTTER,
                MOVE_BITE,
            },
            },
            {
#line 8337
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8339
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8338
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8340
                MOVE_HYPNOSIS,
                MOVE_DREAM_EATER,
                MOVE_CURSE,
                MOVE_MEAN_LOOK,
            },
            },
            {
#line 8345
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8347
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8346
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8348
                MOVE_SLUDGE_BOMB,
                MOVE_SCREECH,
                MOVE_IRON_TAIL,
                MOVE_BITE,
            },
            },
            {
#line 8353
            .species = SPECIES_GENGAR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8353
            .heldItem = ITEM_SITRUS_BERRY,
#line 8355
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8354
            .lvl = 58,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8356
                MOVE_SHADOW_BALL,
                MOVE_SLUDGE_BOMB,
                MOVE_HYPNOSIS,
                MOVE_NIGHTMARE,
            },
            },
        },
    },
#line 8361
    [DIFFICULTY_NORMAL][TRAINER_ELITE_FOUR_LANCE] =
    {
#line 8362
        .trainerName = _("LANCE"),
#line 8363
        .trainerClass = TRAINER_CLASS_ELITE_FOUR,
#line 8364
        .trainerPic = TRAINER_PIC_ELITE_FOUR_LANCE,
        .encounterMusic_gender =
#line 8366
            TRAINER_ENCOUNTER_MUSIC_ELITE_FOUR,
#line 8367
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 8368
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8369
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 8370
        .mugshotColor = MUGSHOT_COLOR_BLUE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8372
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8374
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8373
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8375
                MOVE_HYPER_BEAM,
                MOVE_DRAGON_RAGE,
                MOVE_TWISTER,
                MOVE_BITE,
            },
            },
            {
#line 8380
            .species = SPECIES_DRAGONAIR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8382
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8381
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8383
                MOVE_HYPER_BEAM,
                MOVE_SAFEGUARD,
                MOVE_DRAGON_RAGE,
                MOVE_OUTRAGE,
            },
            },
            {
#line 8388
            .species = SPECIES_DRAGONAIR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8390
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8389
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8391
                MOVE_HYPER_BEAM,
                MOVE_SAFEGUARD,
                MOVE_THUNDER_WAVE,
                MOVE_OUTRAGE,
            },
            },
            {
#line 8396
            .species = SPECIES_AERODACTYL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8398
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8397
            .lvl = 58,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8399
                MOVE_HYPER_BEAM,
                MOVE_ANCIENT_POWER,
                MOVE_WING_ATTACK,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 8404
            .species = SPECIES_DRAGONITE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8404
            .heldItem = ITEM_SITRUS_BERRY,
#line 8406
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 8405
            .lvl = 60,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8407
                MOVE_HYPER_BEAM,
                MOVE_SAFEGUARD,
                MOVE_OUTRAGE,
                MOVE_WING_ATTACK,
            },
            },
        },
    },
#line 8412
    [DIFFICULTY_NORMAL][TRAINER_LEADER_BROCK] =
    {
#line 8413
        .trainerName = _("BROCK"),
#line 8414
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8415
        .trainerPic = TRAINER_PIC_LEADER_BROCK,
        .encounterMusic_gender =
#line 8417
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8418
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8419
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 8421
            .species = SPECIES_GEODUDE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8423
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8422
            .lvl = 12,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8424
                MOVE_TACKLE,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 8427
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8429
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8428
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8430
                MOVE_TACKLE,
                MOVE_BIND,
                MOVE_ROCK_TOMB,
            },
            },
        },
    },
#line 8434
    [DIFFICULTY_NORMAL][TRAINER_LEADER_MISTY] =
    {
#line 8435
        .trainerName = _("MISTY"),
#line 8436
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8437
        .trainerPic = TRAINER_PIC_LEADER_MISTY,
        .encounterMusic_gender =
#line 8439
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 8440
        .items = { ITEM_SUPER_POTION },
#line 8441
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8442
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 8444
            .species = SPECIES_STARYU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8446
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8445
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8447
                MOVE_TACKLE,
                MOVE_HARDEN,
                MOVE_RECOVER,
                MOVE_WATER_PULSE,
            },
            },
            {
#line 8452
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8454
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8453
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8455
                MOVE_SWIFT,
                MOVE_RECOVER,
                MOVE_RAPID_SPIN,
                MOVE_WATER_PULSE,
            },
            },
        },
    },
#line 8460
    [DIFFICULTY_NORMAL][TRAINER_LEADER_LT_SURGE] =
    {
#line 8461
        .trainerName = _("LT. SURGE"),
#line 8462
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8463
        .trainerPic = TRAINER_PIC_LEADER_LT_SURGE,
        .encounterMusic_gender =
#line 8465
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8466
        .items = { ITEM_SUPER_POTION, ITEM_FULL_HEAL },
#line 8467
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8468
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 8470
            .species = SPECIES_VOLTORB,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8472
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8471
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8473
                MOVE_SONIC_BOOM,
                MOVE_TACKLE,
                MOVE_SCREECH,
                MOVE_SHOCK_WAVE,
            },
            },
            {
#line 8478
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8480
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8479
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8481
                MOVE_QUICK_ATTACK,
                MOVE_THUNDER_WAVE,
                MOVE_DOUBLE_TEAM,
                MOVE_SHOCK_WAVE,
            },
            },
            {
#line 8486
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8488
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8487
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8489
                MOVE_QUICK_ATTACK,
                MOVE_THUNDER_WAVE,
                MOVE_DOUBLE_TEAM,
                MOVE_SHOCK_WAVE,
            },
            },
        },
    },
#line 8494
    [DIFFICULTY_NORMAL][TRAINER_LEADER_ERIKA] =
    {
#line 8495
        .trainerName = _("ERIKA"),
#line 8496
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8497
        .trainerPic = TRAINER_PIC_LEADER_ERIKA,
        .encounterMusic_gender =
#line 8499
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 8500
        .items = { ITEM_HYPER_POTION, ITEM_FULL_HEAL },
#line 8501
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8502
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 8504
            .species = SPECIES_VICTREEBEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8506
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8505
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8507
                MOVE_STUN_SPORE,
                MOVE_ACID,
                MOVE_POISON_POWDER,
                MOVE_GIGA_DRAIN,
            },
            },
            {
#line 8512
            .species = SPECIES_TANGELA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8514
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8513
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8515
                MOVE_POISON_POWDER,
                MOVE_CONSTRICT,
                MOVE_INGRAIN,
                MOVE_GIGA_DRAIN,
            },
            },
            {
#line 8520
            .species = SPECIES_VILEPLUME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8522
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8521
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8523
                MOVE_SLEEP_POWDER,
                MOVE_ACID,
                MOVE_STUN_SPORE,
                MOVE_GIGA_DRAIN,
            },
            },
        },
    },
#line 8528
    [DIFFICULTY_NORMAL][TRAINER_LEADER_KOGA] =
    {
#line 8529
        .trainerName = _("KOGA"),
#line 8530
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8531
        .trainerPic = TRAINER_PIC_LEADER_KOGA,
        .encounterMusic_gender =
#line 8533
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8534
        .items = { ITEM_HYPER_POTION, ITEM_HYPER_POTION, ITEM_FULL_HEAL },
#line 8535
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8536
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 8538
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8540
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8539
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8541
                MOVE_SELF_DESTRUCT,
                MOVE_SLUDGE,
                MOVE_SMOKESCREEN,
                MOVE_TOXIC,
            },
            },
            {
#line 8546
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8548
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8547
            .lvl = 39,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8549
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_ACID_ARMOR,
                MOVE_TOXIC,
            },
            },
            {
#line 8554
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8556
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8555
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8557
                MOVE_SELF_DESTRUCT,
                MOVE_SLUDGE,
                MOVE_SMOKESCREEN,
                MOVE_TOXIC,
            },
            },
            {
#line 8562
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8564
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8563
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8565
                MOVE_TACKLE,
                MOVE_SLUDGE,
                MOVE_SMOKESCREEN,
                MOVE_TOXIC,
            },
            },
        },
    },
#line 8570
    [DIFFICULTY_NORMAL][TRAINER_LEADER_BLAINE] =
    {
#line 8571
        .trainerName = _("BLAINE"),
#line 8572
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8573
        .trainerPic = TRAINER_PIC_LEADER_BLAINE,
        .encounterMusic_gender =
#line 8575
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8576
        .items = { ITEM_HYPER_POTION, ITEM_HYPER_POTION, ITEM_FULL_HEAL },
#line 8577
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8578
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 8580
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8582
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8581
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8583
                MOVE_BITE,
                MOVE_ROAR,
                MOVE_TAKE_DOWN,
                MOVE_FIRE_BLAST,
            },
            },
            {
#line 8588
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8590
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8589
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8591
                MOVE_STOMP,
                MOVE_BOUNCE,
                MOVE_FIRE_SPIN,
                MOVE_FIRE_BLAST,
            },
            },
            {
#line 8596
            .species = SPECIES_RAPIDASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8598
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8597
            .lvl = 42,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8599
                MOVE_STOMP,
                MOVE_BOUNCE,
                MOVE_FIRE_SPIN,
                MOVE_FIRE_BLAST,
            },
            },
            {
#line 8604
            .species = SPECIES_ARCANINE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8606
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8605
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8607
                MOVE_BITE,
                MOVE_ROAR,
                MOVE_TAKE_DOWN,
                MOVE_FIRE_BLAST,
            },
            },
        },
    },
#line 8612
    [DIFFICULTY_NORMAL][TRAINER_LEADER_SABRINA] =
    {
#line 8613
        .trainerName = _("SABRINA"),
#line 8614
        .trainerClass = TRAINER_CLASS_LEADER,
#line 8615
        .trainerPic = TRAINER_PIC_LEADER_SABRINA,
        .encounterMusic_gender =
#line 8617
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 8618
        .items = { ITEM_HYPER_POTION, ITEM_HYPER_POTION, ITEM_FULL_HEAL },
#line 8619
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8620
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 8622
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8624
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8623
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8625
                MOVE_PSYBEAM,
                MOVE_REFLECT,
                MOVE_FUTURE_SIGHT,
                MOVE_CALM_MIND,
            },
            },
            {
#line 8630
            .species = SPECIES_MR_MIME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8632
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8631
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8633
                MOVE_BARRIER,
                MOVE_PSYBEAM,
                MOVE_BATON_PASS,
                MOVE_CALM_MIND,
            },
            },
            {
#line 8638
            .species = SPECIES_VENOMOTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8640
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8639
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8641
                MOVE_PSYBEAM,
                MOVE_GUST,
                MOVE_LEECH_LIFE,
                MOVE_SUPERSONIC,
            },
            },
            {
#line 8646
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8648
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8647
            .lvl = 43,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8649
                MOVE_PSYCHIC,
                MOVE_RECOVER,
                MOVE_FUTURE_SIGHT,
                MOVE_CALM_MIND,
            },
            },
        },
    },
#line 8654
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_THOMAS] =
    {
#line 8655
        .trainerName = _("THOMAS"),
#line 8656
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 8657
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 8659
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 8660
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8661
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 8663
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8665
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8664
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8667
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8669
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8668
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8671
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_ARTHUR] =
    {
#line 8672
        .trainerName = _("ARTHUR"),
#line 8673
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 8674
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 8676
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 8677
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8678
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 8680
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8682
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8681
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8684
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8686
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8685
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8688
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_TUCKER] =
    {
#line 8689
        .trainerName = _("TUCKER"),
#line 8690
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 8691
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 8693
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 8694
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8695
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 8697
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8699
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8698
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8701
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_NORTON] =
    {
#line 8702
        .trainerName = _("NORTON"),
#line 8703
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 8704
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 8706
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 8707
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8708
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 8710
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8712
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8711
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8714
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_WALTER] =
    {
#line 8715
        .trainerName = _("WALTER"),
#line 8716
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 8717
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 8719
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 8720
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8721
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 8723
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8725
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8724
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8727
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8729
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 8728
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8731
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_SS_ANNE_SQUIRTLE] =
    {
#line 8732
        .trainerName = _("TERRY"),
#line 8733
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8734
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8736
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8737
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8738
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 8740
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8742
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8741
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8744
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8746
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8745
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8748
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8750
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8749
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8752
            .species = SPECIES_WARTORTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8754
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8753
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8756
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_SS_ANNE_BULBASAUR] =
    {
#line 8757
        .trainerName = _("TERRY"),
#line 8758
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8759
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8761
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8762
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8763
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 8765
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8767
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8766
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8769
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8771
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8770
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8773
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8775
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8774
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8777
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8779
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8778
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8781
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_SS_ANNE_CHARMANDER] =
    {
#line 8782
        .trainerName = _("TERRY"),
#line 8783
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8784
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8786
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8787
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8788
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 8790
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8792
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8791
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8794
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8796
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8795
            .lvl = 16,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8798
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8800
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 8799
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8802
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8804
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8803
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8806
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_POKEMON_TOWER_SQUIRTLE] =
    {
#line 8807
        .trainerName = _("TERRY"),
#line 8808
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8809
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8811
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8812
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8813
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8815
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8817
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8816
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8819
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8821
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8820
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8823
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8825
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8824
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8827
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8829
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8828
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8831
            .species = SPECIES_WARTORTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8833
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8832
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8835
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_POKEMON_TOWER_BULBASAUR] =
    {
#line 8836
        .trainerName = _("TERRY"),
#line 8837
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8838
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8840
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8841
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8842
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8844
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8846
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8845
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8848
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8850
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8849
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8852
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8854
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8853
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8856
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8858
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8857
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8860
            .species = SPECIES_IVYSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8862
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8861
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8864
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_POKEMON_TOWER_CHARMANDER] =
    {
#line 8865
        .trainerName = _("TERRY"),
#line 8866
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8867
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8869
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8870
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8871
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8873
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8875
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8874
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8877
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8879
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8878
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8881
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8883
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8882
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8885
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8887
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8886
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8889
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8891
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8890
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8893
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_SILPH_SQUIRTLE] =
    {
#line 8894
        .trainerName = _("TERRY"),
#line 8895
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8896
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8898
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8899
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8900
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8902
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8904
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8903
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8906
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8908
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8907
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8910
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8912
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8911
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8914
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8916
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8915
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8918
            .species = SPECIES_BLASTOISE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8920
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 8919
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8922
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_SILPH_BULBASAUR] =
    {
#line 8923
        .trainerName = _("TERRY"),
#line 8924
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8925
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8927
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8928
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8929
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8931
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8933
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8932
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8935
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8937
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8936
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8939
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8941
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8940
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8943
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8945
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8944
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8947
            .species = SPECIES_VENUSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8949
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 8948
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8951
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_SILPH_CHARMANDER] =
    {
#line 8952
        .trainerName = _("TERRY"),
#line 8953
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8954
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8956
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8957
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8958
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 8960
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8962
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8961
            .lvl = 37,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8964
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8966
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8965
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8968
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8970
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8969
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8972
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8974
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 8973
            .lvl = 35,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 8976
            .species = SPECIES_CHARIZARD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8978
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 8977
            .lvl = 40,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 8980
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE] =
    {
#line 8981
        .trainerName = _("TERRY"),
#line 8982
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 8983
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 8985
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 8986
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 8987
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 8989
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8991
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 8990
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 8992
                MOVE_FEATHER_DANCE,
                MOVE_WING_ATTACK,
                MOVE_GUST,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 8997
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 8999
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 8998
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9000
                MOVE_TAKE_DOWN,
                MOVE_HORN_DRILL,
                MOVE_ROCK_BLAST,
                MOVE_FURY_ATTACK,
            },
            },
            {
#line 9005
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9007
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9006
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9008
                MOVE_FLAME_WHEEL,
                MOVE_TAKE_DOWN,
                MOVE_LEER,
                MOVE_AGILITY,
            },
            },
            {
#line 9013
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9015
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9014
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9016
                MOVE_SOLAR_BEAM,
                MOVE_SLEEP_POWDER,
                MOVE_POISON_POWDER,
                MOVE_STUN_SPORE,
            },
            },
            {
#line 9021
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9023
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9022
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9024
                MOVE_PSYCHIC,
                MOVE_CALM_MIND,
                MOVE_FUTURE_SIGHT,
                MOVE_DISABLE,
            },
            },
            {
#line 9029
            .species = SPECIES_BLASTOISE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9031
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 9030
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9032
                MOVE_WATER_GUN,
                MOVE_RAIN_DANCE,
                MOVE_BITE,
                MOVE_RAPID_SPIN,
            },
            },
        },
    },
#line 9037
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_ROUTE22_LATE_BULBASAUR] =
    {
#line 9038
        .trainerName = _("TERRY"),
#line 9039
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 9040
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 9042
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9043
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9044
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 9046
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9048
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9047
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9049
                MOVE_FEATHER_DANCE,
                MOVE_WING_ATTACK,
                MOVE_GUST,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 9054
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9056
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9055
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9057
                MOVE_TAKE_DOWN,
                MOVE_HORN_DRILL,
                MOVE_ROCK_BLAST,
                MOVE_FURY_ATTACK,
            },
            },
            {
#line 9062
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9064
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9063
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9065
                MOVE_HYDRO_PUMP,
                MOVE_TWISTER,
                MOVE_LEER,
                MOVE_RAIN_DANCE,
            },
            },
            {
#line 9070
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9072
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9071
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9073
                MOVE_FLAME_WHEEL,
                MOVE_TAKE_DOWN,
                MOVE_LEER,
                MOVE_AGILITY,
            },
            },
            {
#line 9078
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9080
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9079
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9081
                MOVE_PSYCHIC,
                MOVE_CALM_MIND,
                MOVE_FUTURE_SIGHT,
                MOVE_DISABLE,
            },
            },
            {
#line 9086
            .species = SPECIES_VENUSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9088
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 9087
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9089
                MOVE_RAZOR_LEAF,
                MOVE_SWEET_SCENT,
                MOVE_GROWTH,
                MOVE_SYNTHESIS,
            },
            },
        },
    },
#line 9094
    [DIFFICULTY_NORMAL][TRAINER_RIVAL_ROUTE22_LATE_CHARMANDER] =
    {
#line 9095
        .trainerName = _("TERRY"),
#line 9096
        .trainerClass = TRAINER_CLASS_RIVAL_LATE,
#line 9097
        .trainerPic = TRAINER_PIC_RIVAL_LATE,
        .encounterMusic_gender =
#line 9099
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9100
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9101
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 9103
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9105
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9104
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9106
                MOVE_FEATHER_DANCE,
                MOVE_WING_ATTACK,
                MOVE_GUST,
                MOVE_QUICK_ATTACK,
            },
            },
            {
#line 9111
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9113
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9112
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9114
                MOVE_TAKE_DOWN,
                MOVE_HORN_DRILL,
                MOVE_ROCK_BLAST,
                MOVE_FURY_ATTACK,
            },
            },
            {
#line 9119
            .species = SPECIES_EXEGGCUTE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9121
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9120
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9122
                MOVE_SOLAR_BEAM,
                MOVE_SLEEP_POWDER,
                MOVE_POISON_POWDER,
                MOVE_STUN_SPORE,
            },
            },
            {
#line 9127
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9129
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9128
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9130
                MOVE_HYDRO_PUMP,
                MOVE_TWISTER,
                MOVE_LEER,
                MOVE_RAIN_DANCE,
            },
            },
            {
#line 9135
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9137
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 9136
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9138
                MOVE_PSYCHIC,
                MOVE_CALM_MIND,
                MOVE_FUTURE_SIGHT,
                MOVE_DISABLE,
            },
            },
            {
#line 9143
            .species = SPECIES_CHARIZARD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9145
            .iv = TRAINER_PARTY_IVS(30, 30, 30, 30, 30, 30),
#line 9144
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9146
                MOVE_FLAMETHROWER,
                MOVE_WING_ATTACK,
                MOVE_SLASH,
                MOVE_SCARY_FACE,
            },
            },
        },
    },
#line 9151
    [DIFFICULTY_NORMAL][TRAINER_CHAMPION_FIRST_SQUIRTLE] =
    {
#line 9152
        .trainerName = _("TERRY"),
#line 9153
        .trainerClass = TRAINER_CLASS_CHAMPION,
#line 9154
        .trainerPic = TRAINER_PIC_CHAMPION_RIVAL,
        .encounterMusic_gender =
#line 9156
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9157
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE, ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 9158
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9159
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 9160
        .mugshotColor = MUGSHOT_COLOR_YELLOW,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 9162
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9164
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9163
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9165
                MOVE_AERIAL_ACE,
                MOVE_FEATHER_DANCE,
                MOVE_SAND_ATTACK,
                MOVE_WHIRLWIND,
            },
            },
            {
#line 9170
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9172
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9171
            .lvl = 57,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9173
                MOVE_PSYCHIC,
                MOVE_FUTURE_SIGHT,
                MOVE_RECOVER,
                MOVE_REFLECT,
            },
            },
            {
#line 9178
            .species = SPECIES_RHYDON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9180
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9179
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9181
                MOVE_TAKE_DOWN,
                MOVE_EARTHQUAKE,
                MOVE_ROCK_TOMB,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 9186
            .species = SPECIES_ARCANINE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9188
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9187
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9189
                MOVE_EXTREME_SPEED,
                MOVE_FLAMETHROWER,
                MOVE_ROAR,
                MOVE_BITE,
            },
            },
            {
#line 9194
            .species = SPECIES_EXEGGUTOR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9196
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9195
            .lvl = 61,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9197
                MOVE_GIGA_DRAIN,
                MOVE_EGG_BOMB,
                MOVE_SLEEP_POWDER,
                MOVE_LIGHT_SCREEN,
            },
            },
            {
#line 9202
            .species = SPECIES_BLASTOISE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9202
            .heldItem = ITEM_SITRUS_BERRY,
#line 9204
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9203
            .lvl = 63,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9205
                MOVE_HYDRO_PUMP,
                MOVE_RAIN_DANCE,
                MOVE_SKULL_BASH,
                MOVE_BITE,
            },
            },
        },
    },
#line 9210
    [DIFFICULTY_NORMAL][TRAINER_CHAMPION_FIRST_BULBASAUR] =
    {
#line 9211
        .trainerName = _("TERRY"),
#line 9212
        .trainerClass = TRAINER_CLASS_CHAMPION,
#line 9213
        .trainerPic = TRAINER_PIC_CHAMPION_RIVAL,
        .encounterMusic_gender =
#line 9215
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9216
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE, ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 9217
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9218
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 9219
        .mugshotColor = MUGSHOT_COLOR_YELLOW,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 9221
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9223
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9222
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9224
                MOVE_AERIAL_ACE,
                MOVE_FEATHER_DANCE,
                MOVE_SAND_ATTACK,
                MOVE_WHIRLWIND,
            },
            },
            {
#line 9229
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9231
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9230
            .lvl = 57,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9232
                MOVE_PSYCHIC,
                MOVE_FUTURE_SIGHT,
                MOVE_RECOVER,
                MOVE_REFLECT,
            },
            },
            {
#line 9237
            .species = SPECIES_RHYDON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9239
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9238
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9240
                MOVE_TAKE_DOWN,
                MOVE_EARTHQUAKE,
                MOVE_ROCK_TOMB,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 9245
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9247
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9246
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9248
                MOVE_HYDRO_PUMP,
                MOVE_DRAGON_RAGE,
                MOVE_BITE,
                MOVE_THRASH,
            },
            },
            {
#line 9253
            .species = SPECIES_ARCANINE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9255
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9254
            .lvl = 61,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9256
                MOVE_EXTREME_SPEED,
                MOVE_FLAMETHROWER,
                MOVE_ROAR,
                MOVE_BITE,
            },
            },
            {
#line 9261
            .species = SPECIES_VENUSAUR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9261
            .heldItem = ITEM_SITRUS_BERRY,
#line 9263
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9262
            .lvl = 63,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9264
                MOVE_SOLAR_BEAM,
                MOVE_SYNTHESIS,
                MOVE_SUNNY_DAY,
                MOVE_GROWTH,
            },
            },
        },
    },
#line 9269
    [DIFFICULTY_NORMAL][TRAINER_CHAMPION_FIRST_CHARMANDER] =
    {
#line 9270
        .trainerName = _("TERRY"),
#line 9271
        .trainerClass = TRAINER_CLASS_CHAMPION,
#line 9272
        .trainerPic = TRAINER_PIC_CHAMPION_RIVAL,
        .encounterMusic_gender =
#line 9274
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9275
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE, ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 9276
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9277
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
#line 9278
        .mugshotColor = MUGSHOT_COLOR_YELLOW,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 9280
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9282
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9281
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9283
                MOVE_AERIAL_ACE,
                MOVE_FEATHER_DANCE,
                MOVE_SAND_ATTACK,
                MOVE_WHIRLWIND,
            },
            },
            {
#line 9288
            .species = SPECIES_ALAKAZAM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9290
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9289
            .lvl = 57,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9291
                MOVE_PSYCHIC,
                MOVE_FUTURE_SIGHT,
                MOVE_RECOVER,
                MOVE_REFLECT,
            },
            },
            {
#line 9296
            .species = SPECIES_RHYDON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9298
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9297
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9299
                MOVE_TAKE_DOWN,
                MOVE_EARTHQUAKE,
                MOVE_ROCK_TOMB,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 9304
            .species = SPECIES_EXEGGUTOR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9306
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9305
            .lvl = 59,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9307
                MOVE_GIGA_DRAIN,
                MOVE_EGG_BOMB,
                MOVE_SLEEP_POWDER,
                MOVE_LIGHT_SCREEN,
            },
            },
            {
#line 9312
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9314
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9313
            .lvl = 61,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9315
                MOVE_HYDRO_PUMP,
                MOVE_DRAGON_RAGE,
                MOVE_BITE,
                MOVE_THRASH,
            },
            },
            {
#line 9320
            .species = SPECIES_CHARIZARD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9320
            .heldItem = ITEM_SITRUS_BERRY,
#line 9322
            .iv = TRAINER_PARTY_IVS(31, 31, 31, 31, 31, 31),
#line 9321
            .lvl = 63,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9323
                MOVE_FIRE_BLAST,
                MOVE_AERIAL_ACE,
                MOVE_SLASH,
                MOVE_FIRE_SPIN,
            },
            },
        },
    },
#line 9328
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_PATRICIA] =
    {
#line 9329
        .trainerName = _("PATRICIA"),
#line 9330
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9331
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9333
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9334
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9335
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9337
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9339
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9338
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9341
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_CARLY] =
    {
#line 9342
        .trainerName = _("CARLY"),
#line 9343
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9344
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9346
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9347
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9348
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9350
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9352
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9351
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9354
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_HOPE] =
    {
#line 9355
        .trainerName = _("HOPE"),
#line 9356
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9357
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9359
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9360
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9361
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9363
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9365
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9364
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9367
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_PAULA] =
    {
#line 9368
        .trainerName = _("PAULA"),
#line 9369
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9370
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9372
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9373
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9374
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9376
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9378
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9377
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9380
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_LAUREL] =
    {
#line 9381
        .trainerName = _("LAUREL"),
#line 9382
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9383
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9385
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9386
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9387
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9389
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9391
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9390
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9393
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9395
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9394
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9397
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_JODY] =
    {
#line 9398
        .trainerName = _("JODY"),
#line 9399
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9400
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9402
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9403
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9404
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9406
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9408
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9407
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9410
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_TAMMY] =
    {
#line 9411
        .trainerName = _("TAMMY"),
#line 9412
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9413
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9415
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9416
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9417
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9419
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9421
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9420
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9423
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_RUTH] =
    {
#line 9424
        .trainerName = _("RUTH"),
#line 9425
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9426
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9428
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9429
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9430
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9432
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9434
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9433
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9436
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_KARINA] =
    {
#line 9437
        .trainerName = _("KARINA"),
#line 9438
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9439
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9441
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9442
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9443
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9445
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9447
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9446
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9449
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_JANAE] =
    {
#line 9450
        .trainerName = _("JANAE"),
#line 9451
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9452
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9454
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9455
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9456
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9458
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9460
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9459
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9462
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_ANGELICA] =
    {
#line 9463
        .trainerName = _("ANGELICA"),
#line 9464
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9465
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9467
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9468
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9469
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9471
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9473
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9472
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9475
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9477
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9476
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9479
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9481
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9480
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9483
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_EMILIA] =
    {
#line 9484
        .trainerName = _("EMILIA"),
#line 9485
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9486
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9488
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9489
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9490
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9492
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9494
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9493
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9496
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_JENNIFER] =
    {
#line 9497
        .trainerName = _("JENNIFER"),
#line 9498
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9499
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9501
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9502
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9503
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9505
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9507
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9506
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9509
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_1] =
    {
#line 9510
        .trainerName = _("PH"),
#line 9511
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9512
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9514
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9515
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9516
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9518
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9520
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9519
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9522
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_2] =
    {
#line 9523
        .trainerName = _("PH"),
#line 9524
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9525
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9527
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9528
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9529
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9531
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9533
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9532
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9535
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_3] =
    {
#line 9536
        .trainerName = _("PH"),
#line 9537
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9538
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9540
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9541
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9542
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9544
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9546
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9545
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9548
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_4] =
    {
#line 9549
        .trainerName = _("PH"),
#line 9550
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9551
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9553
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9554
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9555
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9557
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9559
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9558
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9561
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_5] =
    {
#line 9562
        .trainerName = _("PH"),
#line 9563
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9564
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9566
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9567
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9568
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9570
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9572
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9571
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9574
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_6] =
    {
#line 9575
        .trainerName = _("PH"),
#line 9576
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9577
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9579
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9580
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9581
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9583
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9585
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9584
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9587
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9589
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9588
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9591
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9593
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9592
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9595
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_7] =
    {
#line 9596
        .trainerName = _("PH"),
#line 9597
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9598
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9600
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9601
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9602
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9604
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9606
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9605
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9608
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_8] =
    {
#line 9609
        .trainerName = _("PH"),
#line 9610
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9611
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9613
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9614
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9615
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9617
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9619
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9618
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9621
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_AMANDA] =
    {
#line 9622
        .trainerName = _("AMANDA"),
#line 9623
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9624
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9626
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9627
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9628
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9630
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9632
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9631
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9634
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9636
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9635
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9638
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_STACY] =
    {
#line 9639
        .trainerName = _("STACY"),
#line 9640
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9641
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9643
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9644
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9645
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 9647
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9649
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9648
            .lvl = 38,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9651
    [DIFFICULTY_NORMAL][TRAINER_CHANNELER_TASHA] =
    {
#line 9652
        .trainerName = _("TASHA"),
#line 9653
        .trainerClass = TRAINER_CLASS_CHANNELER,
#line 9654
        .trainerPic = TRAINER_PIC_CHANNELER,
        .encounterMusic_gender =
#line 9656
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 9657
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9658
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9660
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9662
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9661
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9664
            .species = SPECIES_GASTLY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9666
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9665
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9668
            .species = SPECIES_HAUNTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9670
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9669
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9672
    [DIFFICULTY_NORMAL][TRAINER_HIKER_JEREMY] =
    {
#line 9673
        .trainerName = _("JEREMY"),
#line 9674
        .trainerClass = TRAINER_CLASS_HIKER,
#line 9675
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 9677
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 9678
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9679
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9681
            .species = SPECIES_MACHOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9683
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9682
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9685
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9687
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9686
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9689
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ALMA] =
    {
#line 9690
        .trainerName = _("ALMA"),
#line 9691
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9692
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9694
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9695
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9696
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9698
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9700
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9699
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9702
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9704
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9703
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9706
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9708
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9707
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9710
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_SUSIE] =
    {
#line 9711
        .trainerName = _("SUSIE"),
#line 9712
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9713
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9715
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9716
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9717
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 9719
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9721
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9720
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9723
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9725
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9724
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9727
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9729
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9728
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9731
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9733
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9732
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9735
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9737
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9736
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9739
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_VALERIE] =
    {
#line 9740
        .trainerName = _("VALERIE"),
#line 9741
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9742
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9744
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9745
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9746
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9748
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9750
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9749
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9752
            .species = SPECIES_POLIWAG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9754
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9753
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9756
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_GWEN] =
    {
#line 9757
        .trainerName = _("GWEN"),
#line 9758
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9759
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9761
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9762
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9763
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 9765
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9767
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9766
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9769
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9771
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9770
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9773
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9775
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9774
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9777
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9779
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9778
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9781
    [DIFFICULTY_NORMAL][TRAINER_BIKER_VIRGIL] =
    {
#line 9782
        .trainerName = _("VIRGIL"),
#line 9783
        .trainerClass = TRAINER_CLASS_BIKER,
#line 9784
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 9786
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9787
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9788
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9790
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9792
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9791
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9793
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 9798
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9800
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9799
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9801
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
            {
#line 9806
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9808
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9807
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 9809
                MOVE_SMOKESCREEN,
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
            },
            },
        },
    },
#line 9814
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_FLINT] =
    {
#line 9815
        .trainerName = _("FLINT"),
#line 9816
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 9817
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 9819
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9820
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9821
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9823
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9825
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9824
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9827
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9829
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9828
            .lvl = 14,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9831
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_MISSY] =
    {
#line 9832
        .trainerName = _("MISSY"),
#line 9833
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9834
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9836
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9837
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9838
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9840
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9842
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9841
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9844
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9846
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9845
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9848
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_IRENE] =
    {
#line 9849
        .trainerName = _("IRENE"),
#line 9850
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9851
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9853
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9854
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9855
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9857
            .species = SPECIES_TENTACOOL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9859
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9858
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9861
            .species = SPECIES_HORSEA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9863
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9862
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9865
            .species = SPECIES_SEEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9867
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9866
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9869
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_DANA] =
    {
#line 9870
        .trainerName = _("DANA"),
#line 9871
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9872
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9874
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9875
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9876
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9878
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9880
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9879
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9882
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9884
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9883
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9886
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9888
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9887
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9890
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ARIANA] =
    {
#line 9891
        .trainerName = _("ARIANA"),
#line 9892
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9893
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9895
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9896
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9897
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 9899
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9901
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9900
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9903
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9905
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9904
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9907
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9909
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9908
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9911
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9913
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9912
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9915
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_LEAH] =
    {
#line 9916
        .trainerName = _("LEAH"),
#line 9917
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9918
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9920
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9921
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9922
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9924
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9926
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9925
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9928
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9930
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9929
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9932
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_JUSTIN] =
    {
#line 9933
        .trainerName = _("JUSTIN"),
#line 9934
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 9935
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 9937
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 9938
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9939
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 9941
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9943
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9942
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9945
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9947
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9946
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9949
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_YAZMIN] =
    {
#line 9950
        .trainerName = _("YAZMIN"),
#line 9951
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9952
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9954
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9955
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9956
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9958
            .species = SPECIES_BELLSPROUT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9960
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9959
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9962
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9964
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9963
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9966
            .species = SPECIES_TANGELA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9968
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9967
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9970
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_KINDRA] =
    {
#line 9971
        .trainerName = _("KINDRA"),
#line 9972
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9973
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9975
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9976
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9977
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 9979
            .species = SPECIES_GLOOM,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9981
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9980
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9983
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9985
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9984
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 9987
            .species = SPECIES_ODDISH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 9989
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 9988
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 9991
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_BECKY] =
    {
#line 9992
        .trainerName = _("BECKY"),
#line 9993
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 9994
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 9996
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 9997
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 9998
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10000
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10002
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10001
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10004
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10006
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10005
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10008
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_CELIA] =
    {
#line 10009
        .trainerName = _("CELIA"),
#line 10010
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 10011
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 10013
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 10014
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10015
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10017
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10019
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10018
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10021
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_BROOKS] =
    {
#line 10022
        .trainerName = _("BROOKS"),
#line 10023
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 10024
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 10026
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 10027
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10028
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10030
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10032
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10031
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10034
    [DIFFICULTY_NORMAL][TRAINER_GENTLEMAN_LAMAR] =
    {
#line 10035
        .trainerName = _("LAMAR"),
#line 10036
        .trainerClass = TRAINER_CLASS_GENTLEMAN,
#line 10037
        .trainerPic = TRAINER_PIC_GENTLEMAN,
        .encounterMusic_gender =
#line 10039
            TRAINER_ENCOUNTER_MUSIC_RICH,
#line 10040
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10041
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10043
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10045
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10044
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10047
            .species = SPECIES_PONYTA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10049
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10048
            .lvl = 17,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10051
    [DIFFICULTY_NORMAL][TRAINER_TWINS_ELI_ANNE] =
    {
#line 10052
        .trainerName = _("ELI & ANNE"),
#line 10053
        .trainerClass = TRAINER_CLASS_TWINS,
#line 10054
        .trainerPic = TRAINER_PIC_TWINS,
        .encounterMusic_gender =
#line 10056
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 10057
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10058
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10060
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10062
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10061
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10064
            .species = SPECIES_JIGGLYPUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10066
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10065
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10068
    [DIFFICULTY_NORMAL][TRAINER_COOL_COUPLE_RAY_TYRA] =
    {
#line 10069
        .trainerName = _("RAY & TYRA"),
#line 10070
        .trainerClass = TRAINER_CLASS_COOL_COUPLE,
#line 10071
        .trainerPic = TRAINER_PIC_COOL_COUPLE,
        .encounterMusic_gender =
#line 10073
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 10074
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10075
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10077
            .species = SPECIES_NIDOQUEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10079
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 10078
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 10080
                MOVE_SUPERPOWER,
                MOVE_BODY_SLAM,
                MOVE_DOUBLE_KICK,
                MOVE_POISON_STING,
            },
            },
            {
#line 10085
            .species = SPECIES_NIDOKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10087
            .iv = TRAINER_PARTY_IVS(12, 12, 12, 12, 12, 12),
#line 10086
            .lvl = 45,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 10088
                MOVE_MEGAHORN,
                MOVE_THRASH,
                MOVE_DOUBLE_KICK,
                MOVE_POISON_STING,
            },
            },
        },
    },
#line 10093
    [DIFFICULTY_NORMAL][TRAINER_YOUNG_COUPLE_GIA_JES] =
    {
#line 10094
        .trainerName = _("GIA & JES"),
#line 10095
        .trainerClass = TRAINER_CLASS_YOUNG_COUPLE,
#line 10096
        .trainerPic = TRAINER_PIC_YOUNG_COUPLE,
        .encounterMusic_gender =
#line 10098
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 10099
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10100
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10102
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10104
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10103
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10106
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10108
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10107
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10110
    [DIFFICULTY_NORMAL][TRAINER_TWINS_KIRI_JAN] =
    {
#line 10111
        .trainerName = _("KIRI & JAN"),
#line 10112
        .trainerClass = TRAINER_CLASS_TWINS,
#line 10113
        .trainerPic = TRAINER_PIC_TWINS,
        .encounterMusic_gender =
#line 10115
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 10116
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10117
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10119
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10121
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10120
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10123
            .species = SPECIES_SQUIRTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10125
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10124
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10127
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_KIN_RON_MYA] =
    {
#line 10128
        .trainerName = _("RON & MYA"),
#line 10129
        .trainerClass = TRAINER_CLASS_CRUSH_KIN,
#line 10130
        .trainerPic = TRAINER_PIC_CRUSH_KIN,
        .encounterMusic_gender =
#line 10132
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 10133
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10134
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10136
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10136
            .heldItem = ITEM_BLACK_BELT,
#line 10138
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 10137
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10140
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10140
            .heldItem = ITEM_BLACK_BELT,
#line 10142
            .iv = TRAINER_PARTY_IVS(6, 6, 6, 6, 6, 6),
#line 10141
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10144
    [DIFFICULTY_NORMAL][TRAINER_YOUNG_COUPLE_LEA_JED] =
    {
#line 10145
        .trainerName = _("LEA & JED"),
#line 10146
        .trainerClass = TRAINER_CLASS_YOUNG_COUPLE,
#line 10147
        .trainerPic = TRAINER_PIC_YOUNG_COUPLE,
        .encounterMusic_gender =
#line 10149
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 10150
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10151
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10153
            .species = SPECIES_RAPIDASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10155
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10154
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10157
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10159
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10158
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10161
    [DIFFICULTY_NORMAL][TRAINER_SIS_AND_BRO_LIA_LUC] =
    {
#line 10162
        .trainerName = _("LIA & LUC"),
#line 10163
        .trainerClass = TRAINER_CLASS_SIS_AND_BRO,
#line 10164
        .trainerPic = TRAINER_PIC_SIS_AND_BRO,
        .encounterMusic_gender =
#line 10166
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 10167
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10168
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10170
            .species = SPECIES_GOLDEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10172
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10171
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10174
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10176
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10175
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10178
    [DIFFICULTY_NORMAL][TRAINER_SIS_AND_BRO_LIL_IAN] =
    {
#line 10179
        .trainerName = _("LIL & IAN"),
#line 10180
        .trainerClass = TRAINER_CLASS_SIS_AND_BRO,
#line 10181
        .trainerPic = TRAINER_PIC_SIS_AND_BRO,
        .encounterMusic_gender =
#line 10183
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 10184
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10185
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10187
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10189
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10188
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10191
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10193
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10192
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10195
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_3] =
    {
#line 10196
        .trainerName = _("PH"),
#line 10197
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10198
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10200
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10201
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10202
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10204
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10206
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10205
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10208
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_4] =
    {
#line 10209
        .trainerName = _("PH"),
#line 10210
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10211
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10213
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10214
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10215
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10217
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10219
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10218
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10221
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_5] =
    {
#line 10222
        .trainerName = _("PH"),
#line 10223
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10224
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10226
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10227
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10228
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10230
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10232
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10231
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10234
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_6] =
    {
#line 10235
        .trainerName = _("PH"),
#line 10236
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10237
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10239
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10240
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10241
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10243
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10245
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10244
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10247
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_7] =
    {
#line 10248
        .trainerName = _("PH"),
#line 10249
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10250
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10252
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10253
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10254
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10256
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10258
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10257
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10260
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_8] =
    {
#line 10261
        .trainerName = _("PH"),
#line 10262
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10263
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10265
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10266
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10267
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10269
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10271
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10270
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10273
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_BEN_3] =
    {
#line 10274
        .trainerName = _("BEN"),
#line 10275
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10276
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10278
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10279
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10280
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10282
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10284
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10283
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10286
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10288
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10287
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10290
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_BEN_4] =
    {
#line 10291
        .trainerName = _("BEN"),
#line 10292
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10293
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10295
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10296
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10297
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10299
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10301
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 10300
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10303
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10305
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 10304
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10307
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_CHAD_2] =
    {
#line 10308
        .trainerName = _("CHAD"),
#line 10309
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10310
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10312
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10313
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10314
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10316
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10318
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10317
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10320
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10322
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10321
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10324
    [DIFFICULTY_NORMAL][TRAINER_LASS_RELI_2] =
    {
#line 10325
        .trainerName = _("RELI"),
#line 10326
        .trainerClass = TRAINER_CLASS_LASS,
#line 10327
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 10329
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 10330
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10331
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10333
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10335
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10334
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10337
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10339
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10338
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10341
    [DIFFICULTY_NORMAL][TRAINER_LASS_RELI_3] =
    {
#line 10342
        .trainerName = _("RELI"),
#line 10343
        .trainerClass = TRAINER_CLASS_LASS,
#line 10344
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 10346
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 10347
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10348
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10350
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10352
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10351
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10354
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10356
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10355
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10358
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_TIMMY_2] =
    {
#line 10359
        .trainerName = _("TIMMY"),
#line 10360
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10361
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10363
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10364
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10365
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 10367
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10369
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10368
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10371
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10373
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10372
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10375
            .species = SPECIES_ZUBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10377
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10376
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10379
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_TIMMY_3] =
    {
#line 10380
        .trainerName = _("TIMMY"),
#line 10381
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10382
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10384
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10385
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10386
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 10388
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10390
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10389
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10392
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10394
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10393
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10396
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10398
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10397
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10400
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_TIMMY_4] =
    {
#line 10401
        .trainerName = _("TIMMY"),
#line 10402
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10403
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10405
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10406
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10407
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 10409
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10411
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 10410
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10413
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10415
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 10414
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10417
            .species = SPECIES_GOLBAT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10419
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 10418
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10421
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_CHAD_3] =
    {
#line 10422
        .trainerName = _("CHAD"),
#line 10423
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10424
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10426
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10427
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10428
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10430
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10432
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10431
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10434
            .species = SPECIES_SANDSHREW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10436
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10435
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10438
    [DIFFICULTY_NORMAL][TRAINER_LASS_JANICE_2] =
    {
#line 10439
        .trainerName = _("JANICE"),
#line 10440
        .trainerClass = TRAINER_CLASS_LASS,
#line 10441
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 10443
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 10444
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10445
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10447
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10449
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10448
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10451
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10453
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 10452
            .lvl = 20,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10455
    [DIFFICULTY_NORMAL][TRAINER_LASS_JANICE_3] =
    {
#line 10456
        .trainerName = _("JANICE"),
#line 10457
        .trainerClass = TRAINER_CLASS_LASS,
#line 10458
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 10460
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 10461
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10462
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10464
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10466
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10465
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10468
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10470
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10469
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10472
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_CHAD_4] =
    {
#line 10473
        .trainerName = _("CHAD"),
#line 10474
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10475
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10477
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10478
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10479
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10481
            .species = SPECIES_ARBOK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10483
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 10482
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10485
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10487
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 10486
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10489
    [DIFFICULTY_NORMAL][TRAINER_HIKER_FRANKLIN_2] =
    {
#line 10490
        .trainerName = _("FRANKLIN"),
#line 10491
        .trainerClass = TRAINER_CLASS_HIKER,
#line 10492
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 10494
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 10495
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10496
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10498
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10500
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 10499
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10502
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10504
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 10503
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10506
    [DIFFICULTY_NORMAL][TRAINER_PKMN_PROF_PROF_OAK] =
    {
#line 10507
        .trainerName = _("PROF. OAK"),
#line 10508
        .trainerClass = TRAINER_CLASS_PKMN_PROF,
#line 10509
        .trainerPic = TRAINER_PIC_PROFESSOR_OAK,
        .encounterMusic_gender =
#line 10511
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10512
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10513
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10515
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10517
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10516
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10519
    [DIFFICULTY_NORMAL][TRAINER_PLAYER_BRENDAN] =
    {
#line 10520
        .trainerName = _("BRENDAN"),
#line 10521
        .trainerClass = TRAINER_CLASS_PLAYER,
#line 10522
        .trainerPic = TRAINER_PIC_RS_BRENDAN_2,
        .encounterMusic_gender =
#line 10524
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10525
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10526
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10528
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10530
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10529
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10532
    [DIFFICULTY_NORMAL][TRAINER_PLAYER_MAY] =
    {
#line 10533
        .trainerName = _("MAY"),
#line 10534
        .trainerClass = TRAINER_CLASS_PLAYER,
#line 10535
        .trainerPic = TRAINER_PIC_RS_MAY_2,
        .encounterMusic_gender =
#line 10537
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 10538
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10539
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10541
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10543
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10542
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10545
    [DIFFICULTY_NORMAL][TRAINER_PLAYER_RED] =
    {
#line 10546
        .trainerName = _("RED"),
#line 10547
        .trainerClass = TRAINER_CLASS_PLAYER,
#line 10548
        .trainerPic = TRAINER_PIC_RED,
        .encounterMusic_gender =
#line 10550
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10551
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10552
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10554
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10556
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10555
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10558
    [DIFFICULTY_NORMAL][TRAINER_PLAYER_LEAF] =
    {
#line 10559
        .trainerName = _("LEAF"),
#line 10560
        .trainerClass = TRAINER_CLASS_PLAYER,
#line 10561
        .trainerPic = TRAINER_PIC_LEAF,
        .encounterMusic_gender =
#line 10563
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 10564
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10565
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10567
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10569
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10568
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10902
    [DIFFICULTY_NORMAL][TRAINER_BIKER_2] =
    {
#line 10903
        .trainerName = _("PH"),
#line 10904
        .trainerClass = TRAINER_CLASS_BIKER,
#line 10905
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 10907
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10908
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10909
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 10911
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10913
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10912
            .lvl = 5,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10915
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_ANTHONY] =
    {
#line 10916
        .trainerName = _("ANTHONY"),
#line 10917
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10918
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10920
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10921
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10922
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10924
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10926
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10925
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10928
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10930
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10929
            .lvl = 8,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10932
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_CHARLIE] =
    {
#line 10933
        .trainerName = _("CHARLIE"),
#line 10934
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 10935
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 10937
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10938
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10939
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 10941
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10943
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10942
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10945
            .species = SPECIES_CATERPIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10947
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10946
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10949
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10951
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10950
            .lvl = 7,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10953
    [DIFFICULTY_NORMAL][TRAINER_TWINS_ELI_ANNE_2] =
    {
#line 10954
        .trainerName = _("ELI & ANNE"),
#line 10955
        .trainerClass = TRAINER_CLASS_TWINS,
#line 10956
        .trainerPic = TRAINER_PIC_TWINS,
        .encounterMusic_gender =
#line 10958
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 10959
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 10960
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 10962
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10964
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10963
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10966
            .species = SPECIES_JIGGLYPUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10968
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 10967
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10970
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_JOHNSON] =
    {
#line 10971
        .trainerName = _("JOHNSON"),
#line 10972
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 10973
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 10975
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10976
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10977
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 10979
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10981
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10980
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10983
            .species = SPECIES_EKANS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10985
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10984
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 10987
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 10989
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 10988
            .lvl = 34,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 10991
    [DIFFICULTY_NORMAL][TRAINER_BIKER_RICARDO] =
    {
#line 10992
        .trainerName = _("RICARDO"),
#line 10993
        .trainerClass = TRAINER_CLASS_BIKER,
#line 10994
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 10996
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 10997
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 10998
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 11000
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 11002
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 11001
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 11003
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
            {
#line 11008
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 11010
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 11009
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 11011
                MOVE_SLUDGE,
                MOVE_SMOG,
                MOVE_TACKLE,
                MOVE_POISON_GAS,
            },
            },
            {
#line 11016
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 11018
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 11017
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 11019
                MOVE_MINIMIZE,
                MOVE_SLUDGE,
                MOVE_DISABLE,
                MOVE_POUND,
            },
            },
        },
    },
#line 11024
    [DIFFICULTY_NORMAL][TRAINER_BIKER_JAREN] =
    {
#line 11025
        .trainerName = _("JAREN"),
#line 11026
        .trainerClass = TRAINER_CLASS_BIKER,
#line 11027
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 11029
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 11030
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 11031
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 11033
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 11035
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 11034
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 11037
            .species = SPECIES_GRIMER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 11039
            .iv = TRAINER_PARTY_IVS(0, 0, 0, 0, 0, 0),
#line 11038
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 12364
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_MARK_2] =
    {
#line 12365
        .trainerName = _("MARK"),
#line 12366
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 12367
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 12369
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 12370
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 12371
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 12373
            .species = SPECIES_RHYHORN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 12375
            .iv = TRAINER_PARTY_IVS(10, 10, 10, 10, 10, 10),
#line 12374
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 12377
            .species = SPECIES_LICKITUNG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 12379
            .iv = TRAINER_PARTY_IVS(10, 10, 10, 10, 10, 10),
#line 12378
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13057
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_KELSEY_2] =
    {
#line 13058
        .trainerName = _("KELSEY"),
#line 13059
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13060
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13062
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13063
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13064
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13066
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13068
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13067
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13070
            .species = SPECIES_NIDORAN_F,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13072
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13071
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13074
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_KELSEY_3] =
    {
#line 13075
        .trainerName = _("KELSEY"),
#line 13076
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13077
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13079
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13080
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13081
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13083
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13085
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13084
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13087
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13089
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13088
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13091
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_KELSEY_4] =
    {
#line 13092
        .trainerName = _("KELSEY"),
#line 13093
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13094
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13096
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13097
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13098
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13100
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13102
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13101
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13104
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13106
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13105
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13108
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_RICKY_2] =
    {
#line 13109
        .trainerName = _("RICKY"),
#line 13110
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13111
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13113
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13114
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13115
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 13117
            .species = SPECIES_SQUIRTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13119
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13118
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13121
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_RICKY_3] =
    {
#line 13122
        .trainerName = _("RICKY"),
#line 13123
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13124
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13126
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13127
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13128
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 13130
            .species = SPECIES_WARTORTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13132
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13131
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13134
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_RICKY_4] =
    {
#line 13135
        .trainerName = _("RICKY"),
#line 13136
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13137
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13139
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13140
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13141
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 13143
            .species = SPECIES_WARTORTLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13145
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13144
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13147
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_JEFF_2] =
    {
#line 13148
        .trainerName = _("JEFF"),
#line 13149
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13150
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13152
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13153
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13154
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13156
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13158
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13157
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13160
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13162
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13161
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13164
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_JEFF_3] =
    {
#line 13165
        .trainerName = _("JEFF"),
#line 13166
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13167
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13169
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13170
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13171
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13173
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13175
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13174
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13177
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13179
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13178
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13181
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_JEFF_4] =
    {
#line 13182
        .trainerName = _("JEFF"),
#line 13183
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13184
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13186
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13187
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13188
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13190
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13192
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13191
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13194
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13196
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13195
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13198
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ISABELLE_2] =
    {
#line 13199
        .trainerName = _("ISABELLE"),
#line 13200
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13201
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13203
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13204
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13205
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13207
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13209
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13208
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13211
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13213
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13212
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13215
            .species = SPECIES_PIDGEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13217
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 13216
            .lvl = 18,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13219
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ISABELLE_3] =
    {
#line 13220
        .trainerName = _("ISABELLE"),
#line 13221
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13222
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13224
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13225
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13226
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13228
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13230
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13229
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13232
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13234
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13233
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13236
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13238
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13237
            .lvl = 26,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13240
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ISABELLE_4] =
    {
#line 13241
        .trainerName = _("ISABELLE"),
#line 13242
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13243
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13245
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13246
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13247
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13249
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13251
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13250
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13253
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13255
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13254
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13257
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13259
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13258
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13261
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_YASU_2] =
    {
#line 13262
        .trainerName = _("YASU"),
#line 13263
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 13264
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 13266
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13267
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13268
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13270
            .species = SPECIES_RATTATA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13272
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13271
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13274
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13276
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13275
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13278
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13280
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13279
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13282
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_YASU_3] =
    {
#line 13283
        .trainerName = _("YASU"),
#line 13284
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 13285
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 13287
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13288
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13289
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13291
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13293
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13292
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13295
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13297
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13296
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13299
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13301
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13300
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13303
    [DIFFICULTY_NORMAL][TRAINER_ENGINEER_BERNIE_2] =
    {
#line 13304
        .trainerName = _("BERNIE"),
#line 13305
        .trainerClass = TRAINER_CLASS_ENGINEER,
#line 13306
        .trainerPic = TRAINER_PIC_ENGINEER,
        .encounterMusic_gender =
#line 13308
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13309
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13310
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13312
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13314
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13313
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13316
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13318
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13317
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13320
            .species = SPECIES_MAGNETON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13322
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13321
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13324
    [DIFFICULTY_NORMAL][TRAINER_GAMER_DARIAN_2] =
    {
#line 13325
        .trainerName = _("DARIAN"),
#line 13326
        .trainerClass = TRAINER_CLASS_GAMER,
#line 13327
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 13329
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13330
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13331
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13333
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13335
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13334
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13337
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13339
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13338
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13341
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_CHRIS_2] =
    {
#line 13342
        .trainerName = _("CHRIS"),
#line 13343
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13344
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13346
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13347
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13348
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13350
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13352
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13351
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13354
            .species = SPECIES_CHARMANDER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13356
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13355
            .lvl = 24,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13358
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_CHRIS_3] =
    {
#line 13359
        .trainerName = _("CHRIS"),
#line 13360
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13361
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13363
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13364
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13365
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13367
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13369
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13368
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13371
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13373
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13372
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13375
    [DIFFICULTY_NORMAL][TRAINER_CAMPER_CHRIS_4] =
    {
#line 13376
        .trainerName = _("CHRIS"),
#line 13377
        .trainerClass = TRAINER_CLASS_CAMPER,
#line 13378
        .trainerPic = TRAINER_PIC_CAMPER,
        .encounterMusic_gender =
#line 13380
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13381
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13382
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13384
            .species = SPECIES_ARCANINE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13386
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13385
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13388
            .species = SPECIES_CHARMELEON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13390
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13389
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13392
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ALICIA_2] =
    {
#line 13393
        .trainerName = _("ALICIA"),
#line 13394
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13395
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13397
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13398
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13399
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 13401
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13403
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13402
            .lvl = 25,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13405
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ALICIA_3] =
    {
#line 13406
        .trainerName = _("ALICIA"),
#line 13407
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13408
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13410
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13411
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13412
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 13414
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13416
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13415
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13418
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_ALICIA_4] =
    {
#line 13419
        .trainerName = _("ALICIA"),
#line 13420
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13421
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13423
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13424
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13425
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 13427
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13429
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13428
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13431
    [DIFFICULTY_NORMAL][TRAINER_HIKER_JEREMY_2] =
    {
#line 13432
        .trainerName = _("JEREMY"),
#line 13433
        .trainerClass = TRAINER_CLASS_HIKER,
#line 13434
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 13436
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 13437
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13438
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13440
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13442
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13441
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13444
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13446
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13445
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13448
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_MARK_3] =
    {
#line 13449
        .trainerName = _("MARK"),
#line 13450
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 13451
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 13453
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 13454
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13455
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13457
            .species = SPECIES_RHYDON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13459
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 13458
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13461
            .species = SPECIES_LICKITUNG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13463
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 13462
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13465
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_HERMAN_2] =
    {
#line 13466
        .trainerName = _("HERMAN"),
#line 13467
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 13468
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 13470
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 13471
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13472
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13474
            .species = SPECIES_MAROWAK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13476
            .iv = TRAINER_PARTY_IVS(10, 10, 10, 10, 10, 10),
#line 13475
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13478
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13480
            .iv = TRAINER_PARTY_IVS(10, 10, 10, 10, 10, 10),
#line 13479
            .lvl = 29,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13482
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_HERMAN_3] =
    {
#line 13483
        .trainerName = _("HERMAN"),
#line 13484
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 13485
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 13487
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 13488
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13489
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13491
            .species = SPECIES_MAROWAK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13493
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 13492
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13495
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13497
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 13496
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13499
    [DIFFICULTY_NORMAL][TRAINER_HIKER_TRENT_2] =
    {
#line 13500
        .trainerName = _("TRENT"),
#line 13501
        .trainerClass = TRAINER_CLASS_HIKER,
#line 13502
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 13504
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 13505
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13506
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13508
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13510
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13509
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13512
            .species = SPECIES_GRAVELER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13514
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13513
            .lvl = 31,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13516
    [DIFFICULTY_NORMAL][TRAINER_LASS_MEGAN_2] =
    {
#line 13517
        .trainerName = _("MEGAN"),
#line 13518
        .trainerClass = TRAINER_CLASS_LASS,
#line 13519
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 13521
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 13522
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13523
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 13525
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13527
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13526
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13529
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13531
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13530
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13533
            .species = SPECIES_NIDORAN_M,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13535
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13534
            .lvl = 23,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13537
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13539
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13538
            .lvl = 21,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13541
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13543
            .iv = TRAINER_PARTY_IVS(4, 4, 4, 4, 4, 4),
#line 13542
            .lvl = 22,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13545
    [DIFFICULTY_NORMAL][TRAINER_LASS_MEGAN_3] =
    {
#line 13546
        .trainerName = _("MEGAN"),
#line 13547
        .trainerClass = TRAINER_CLASS_LASS,
#line 13548
        .trainerPic = TRAINER_PIC_LASS,
        .encounterMusic_gender =
#line 13550
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 13551
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13552
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 13554
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13556
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13555
            .lvl = 46,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13558
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13560
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13559
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13562
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13564
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13563
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13566
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13568
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13567
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13570
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13572
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13571
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13574
    [DIFFICULTY_NORMAL][TRAINER_SUPER_NERD_GLENN_2] =
    {
#line 13575
        .trainerName = _("GLENN"),
#line 13576
        .trainerClass = TRAINER_CLASS_SUPER_NERD,
#line 13577
        .trainerPic = TRAINER_PIC_SUPER_NERD,
        .encounterMusic_gender =
#line 13579
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 13580
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13581
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13583
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13585
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13584
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13587
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13589
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13588
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13591
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13593
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13592
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13595
    [DIFFICULTY_NORMAL][TRAINER_GAMER_RICH_2] =
    {
#line 13596
        .trainerName = _("RICH"),
#line 13597
        .trainerClass = TRAINER_CLASS_GAMER,
#line 13598
        .trainerPic = TRAINER_PIC_GAMER,
        .encounterMusic_gender =
#line 13600
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13601
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13602
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13604
            .species = SPECIES_GROWLITHE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13606
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13605
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13608
            .species = SPECIES_VULPIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13610
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13609
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13612
    [DIFFICULTY_NORMAL][TRAINER_BIKER_JAREN_2] =
    {
#line 13613
        .trainerName = _("JAREN"),
#line 13614
        .trainerClass = TRAINER_CLASS_BIKER,
#line 13615
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 13617
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13618
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13619
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13621
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13623
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13622
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13625
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13627
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13626
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13629
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_ELLIOT_2] =
    {
#line 13630
        .trainerName = _("ELLIOT"),
#line 13631
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 13632
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 13634
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 13635
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13636
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 13638
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13640
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13639
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13642
            .species = SPECIES_CLOYSTER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13644
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13643
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13646
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13648
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13647
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13650
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13652
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13651
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13654
    [DIFFICULTY_NORMAL][TRAINER_ROCKER_LUCA_2] =
    {
#line 13655
        .trainerName = _("LUCA"),
#line 13656
        .trainerClass = TRAINER_CLASS_ROCKER,
#line 13657
        .trainerPic = TRAINER_PIC_ROCKER,
        .encounterMusic_gender =
#line 13659
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13660
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13661
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13663
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13665
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13664
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13667
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13669
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13668
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13671
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_SHEILA_2] =
    {
#line 13672
        .trainerName = _("SHEILA"),
#line 13673
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 13674
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 13676
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 13677
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13678
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13680
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13682
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13681
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13684
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13686
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13685
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13688
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_ROBERT_2] =
    {
#line 13689
        .trainerName = _("ROBERT"),
#line 13690
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13691
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13693
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13694
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13695
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 13697
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13699
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13698
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13701
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13703
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13702
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13705
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13707
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13706
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13709
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13711
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13710
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13713
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_ROBERT_3] =
    {
#line 13714
        .trainerName = _("ROBERT"),
#line 13715
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13716
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13718
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13719
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13720
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 13722
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13724
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13723
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13726
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13728
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13727
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13730
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13732
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13731
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13734
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13736
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13735
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13738
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_SUSIE_2] =
    {
#line 13739
        .trainerName = _("SUSIE"),
#line 13740
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13741
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13743
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13744
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13745
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 13747
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13749
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13748
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13751
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13753
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13752
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13755
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13757
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13756
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13759
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13761
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13760
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13763
            .species = SPECIES_MEOWTH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13765
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13764
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13767
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_SUSIE_3] =
    {
#line 13768
        .trainerName = _("SUSIE"),
#line 13769
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13770
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13772
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13773
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13774
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 13776
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13778
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13777
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13780
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13782
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13781
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13784
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13786
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13785
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13788
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13790
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13789
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13792
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13794
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13793
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13796
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_SUSIE_4] =
    {
#line 13797
        .trainerName = _("SUSIE"),
#line 13798
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13799
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13801
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13802
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13803
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 13805
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13807
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13806
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13809
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13811
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13810
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13813
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13815
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13814
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13817
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13819
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13818
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13821
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13823
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 13822
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13825
    [DIFFICULTY_NORMAL][TRAINER_BIKER_LUKAS_2] =
    {
#line 13826
        .trainerName = _("LUKAS"),
#line 13827
        .trainerClass = TRAINER_CLASS_BIKER,
#line 13828
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 13830
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 13831
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13832
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 13834
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13836
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13835
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13838
            .species = SPECIES_KOFFING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13840
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13839
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13842
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13844
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13843
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13846
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13848
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13847
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13850
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_BENNY_2] =
    {
#line 13851
        .trainerName = _("BENNY"),
#line 13852
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13853
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13855
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13856
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13857
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13859
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13861
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13860
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13863
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13865
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13864
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13867
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_BENNY_3] =
    {
#line 13868
        .trainerName = _("BENNY"),
#line 13869
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13870
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13872
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13873
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13874
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13876
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13878
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13877
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13880
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13882
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13881
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13884
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_MARLON_2] =
    {
#line 13885
        .trainerName = _("MARLON"),
#line 13886
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13887
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13889
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13890
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13891
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13893
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13895
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13894
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13897
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13899
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13898
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13901
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13903
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13902
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13905
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_MARLON_3] =
    {
#line 13906
        .trainerName = _("MARLON"),
#line 13907
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13908
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13910
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13911
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13912
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13914
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13916
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13915
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13918
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13920
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13919
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13922
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13924
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13923
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13926
    [DIFFICULTY_NORMAL][TRAINER_BEAUTY_GRACE_2] =
    {
#line 13927
        .trainerName = _("GRACE"),
#line 13928
        .trainerClass = TRAINER_CLASS_BEAUTY,
#line 13929
        .trainerPic = TRAINER_PIC_BEAUTY,
        .encounterMusic_gender =
#line 13931
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 13932
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13933
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13935
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13937
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13936
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13939
            .species = SPECIES_WIGGLYTUFF,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13941
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13940
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13943
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_CHESTER_2] =
    {
#line 13944
        .trainerName = _("CHESTER"),
#line 13945
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13946
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13948
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13949
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13950
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13952
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13954
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13953
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13956
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13958
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13957
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13960
            .species = SPECIES_DODUO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13962
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13961
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13964
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_CHESTER_3] =
    {
#line 13965
        .trainerName = _("CHESTER"),
#line 13966
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 13967
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 13969
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 13970
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13971
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 13973
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13975
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13974
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13977
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13979
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13978
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13981
            .species = SPECIES_DODRIO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13983
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 13982
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 13985
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_BECKY_2] =
    {
#line 13986
        .trainerName = _("BECKY"),
#line 13987
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 13988
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 13990
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 13991
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 13992
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 13994
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 13996
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13995
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 13998
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14000
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 13999
            .lvl = 32,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14002
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_BECKY_3] =
    {
#line 14003
        .trainerName = _("BECKY"),
#line 14004
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 14005
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 14007
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14008
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14009
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14011
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14013
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14012
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14015
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14017
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14016
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14019
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_BECKY_4] =
    {
#line 14020
        .trainerName = _("BECKY"),
#line 14021
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 14022
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 14024
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14025
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14026
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14028
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14030
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14029
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14032
            .species = SPECIES_RAICHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14034
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14033
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14036
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_KIN_RON_MYA_2] =
    {
#line 14037
        .trainerName = _("RON & MYA"),
#line 14038
        .trainerClass = TRAINER_CLASS_CRUSH_KIN,
#line 14039
        .trainerPic = TRAINER_PIC_CRUSH_KIN,
        .encounterMusic_gender =
#line 14041
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14042
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14043
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14045
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14045
            .heldItem = ITEM_BLACK_BELT,
#line 14047
            .iv = TRAINER_PARTY_IVS(13, 13, 13, 13, 13, 13),
#line 14046
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14049
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14049
            .heldItem = ITEM_BLACK_BELT,
#line 14051
            .iv = TRAINER_PARTY_IVS(13, 13, 13, 13, 13, 13),
#line 14050
            .lvl = 33,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14053
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_KIN_RON_MYA_3] =
    {
#line 14054
        .trainerName = _("RON & MYA"),
#line 14055
        .trainerClass = TRAINER_CLASS_CRUSH_KIN,
#line 14056
        .trainerPic = TRAINER_PIC_CRUSH_KIN,
        .encounterMusic_gender =
#line 14058
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14059
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14060
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14062
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14062
            .heldItem = ITEM_BLACK_BELT,
#line 14064
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14063
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14066
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14066
            .heldItem = ITEM_BLACK_BELT,
#line 14068
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14067
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14070
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_KIN_RON_MYA_4] =
    {
#line 14071
        .trainerName = _("RON & MYA"),
#line 14072
        .trainerClass = TRAINER_CLASS_CRUSH_KIN,
#line 14073
        .trainerPic = TRAINER_PIC_CRUSH_KIN,
        .encounterMusic_gender =
#line 14075
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14076
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14077
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14079
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14079
            .heldItem = ITEM_BLACK_BELT,
#line 14081
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14080
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14083
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14083
            .heldItem = ITEM_BLACK_BELT,
#line 14085
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14084
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14087
    [DIFFICULTY_NORMAL][TRAINER_BIKER_RUBEN_2] =
    {
#line 14088
        .trainerName = _("RUBEN"),
#line 14089
        .trainerClass = TRAINER_CLASS_BIKER,
#line 14090
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 14092
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 14093
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14094
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 14096
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14098
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14097
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14100
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14102
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14101
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14104
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14106
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14105
            .lvl = 48,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14108
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_CAMRON_2] =
    {
#line 14109
        .trainerName = _("CAMRON"),
#line 14110
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 14111
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 14113
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 14114
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14115
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14117
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14119
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14118
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14121
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14123
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14122
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14125
    [DIFFICULTY_NORMAL][TRAINER_BIKER_JAXON_2] =
    {
#line 14126
        .trainerName = _("JAXON"),
#line 14127
        .trainerClass = TRAINER_CLASS_BIKER,
#line 14128
        .trainerPic = TRAINER_PIC_BIKER,
        .encounterMusic_gender =
#line 14130
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 14131
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14132
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14134
            .species = SPECIES_WEEZING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14136
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14135
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14138
            .species = SPECIES_MUK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14140
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14139
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14142
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_ISAIAH_2] =
    {
#line 14143
        .trainerName = _("ISAIAH"),
#line 14144
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 14145
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 14147
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 14148
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14149
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14151
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14153
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14152
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14155
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14157
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14156
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14159
    [DIFFICULTY_NORMAL][TRAINER_CUE_BALL_COREY_2] =
    {
#line 14160
        .trainerName = _("COREY"),
#line 14161
        .trainerClass = TRAINER_CLASS_CUE_BALL,
#line 14162
        .trainerPic = TRAINER_PIC_CUE_BALL,
        .encounterMusic_gender =
#line 14164
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 14165
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14166
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14168
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14170
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14169
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14172
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14174
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14173
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14176
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_JACOB_2] =
    {
#line 14177
        .trainerName = _("JACOB"),
#line 14178
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 14179
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 14181
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14182
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14183
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 14185
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14187
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 14186
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14189
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14191
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 14190
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14193
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14195
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 14194
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14197
            .species = SPECIES_SPEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14199
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 14198
            .lvl = 28,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14201
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_JACOB_3] =
    {
#line 14202
        .trainerName = _("JACOB"),
#line 14203
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 14204
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 14206
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14207
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14208
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 14210
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14212
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14211
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14214
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14216
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14215
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14218
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14220
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14219
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14222
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14224
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14223
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14226
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_ALICE_2] =
    {
#line 14227
        .trainerName = _("ALICE"),
#line 14228
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 14229
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 14231
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 14232
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14233
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14235
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14237
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14236
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14239
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14241
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14240
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14243
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_DARRIN_2] =
    {
#line 14244
        .trainerName = _("DARRIN"),
#line 14245
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 14246
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 14248
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 14249
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14250
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 14252
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14254
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14253
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14256
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14258
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14257
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14260
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14262
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14261
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14264
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14266
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14265
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14268
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_MISSY_2] =
    {
#line 14269
        .trainerName = _("MISSY"),
#line 14270
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 14271
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 14273
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14274
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14275
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14277
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14279
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14278
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14281
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14283
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14282
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14285
    [DIFFICULTY_NORMAL][TRAINER_PICNICKER_MISSY_3] =
    {
#line 14286
        .trainerName = _("MISSY"),
#line 14287
        .trainerClass = TRAINER_CLASS_PICNICKER,
#line 14288
        .trainerPic = TRAINER_PIC_PICNICKER,
        .encounterMusic_gender =
#line 14290
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14291
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14292
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14294
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14296
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14295
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14298
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14300
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14299
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14302
    [DIFFICULTY_NORMAL][TRAINER_FISHERMAN_WADE_2] =
    {
#line 14303
        .trainerName = _("WADE"),
#line 14304
        .trainerClass = TRAINER_CLASS_FISHERMAN,
#line 14305
        .trainerPic = TRAINER_PIC_FISHERMAN,
        .encounterMusic_gender =
#line 14307
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 14308
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14309
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 6,
        .party = (const struct TrainerMon[])
        {
            {
#line 14311
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14313
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14312
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14315
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14317
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14316
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14319
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14321
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14320
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14323
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14325
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14324
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14327
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14329
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14328
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14331
            .species = SPECIES_MAGIKARP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14333
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14332
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14335
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_JACK_2] =
    {
#line 14336
        .trainerName = _("JACK"),
#line 14337
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 14338
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 14340
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 14341
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14342
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 14344
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14346
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14345
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14348
    [DIFFICULTY_NORMAL][TRAINER_SIS_AND_BRO_LIL_IAN_2] =
    {
#line 14349
        .trainerName = _("LIL & IAN"),
#line 14350
        .trainerClass = TRAINER_CLASS_SIS_AND_BRO,
#line 14351
        .trainerPic = TRAINER_PIC_SIS_AND_BRO,
        .encounterMusic_gender =
#line 14353
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 14354
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14355
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14357
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14359
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14358
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14361
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14363
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14362
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14365
    [DIFFICULTY_NORMAL][TRAINER_SIS_AND_BRO_LIL_IAN_3] =
    {
#line 14366
        .trainerName = _("LIL & IAN"),
#line 14367
        .trainerClass = TRAINER_CLASS_SIS_AND_BRO,
#line 14368
        .trainerPic = TRAINER_PIC_SIS_AND_BRO,
        .encounterMusic_gender =
#line 14370
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 14371
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14372
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14374
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14376
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14375
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14378
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14380
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14379
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14382
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_FINN_2] =
    {
#line 14383
        .trainerName = _("FINN"),
#line 14384
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 14385
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 14387
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 14388
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14389
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 14391
            .species = SPECIES_STARMIE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14393
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14392
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14395
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_GIRL_SHARON_2] =
    {
#line 14396
        .trainerName = _("SHARON"),
#line 14397
        .trainerClass = TRAINER_CLASS_CRUSH_GIRL,
#line 14398
        .trainerPic = TRAINER_PIC_CRUSH_GIRL,
        .encounterMusic_gender =
#line 14400
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14401
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14402
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14404
            .species = SPECIES_MANKEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14404
            .heldItem = ITEM_BLACK_BELT,
#line 14406
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14405
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14408
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14408
            .heldItem = ITEM_BLACK_BELT,
#line 14410
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14409
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14412
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_GIRL_SHARON_3] =
    {
#line 14413
        .trainerName = _("SHARON"),
#line 14414
        .trainerClass = TRAINER_CLASS_CRUSH_GIRL,
#line 14415
        .trainerPic = TRAINER_PIC_CRUSH_GIRL,
        .encounterMusic_gender =
#line 14417
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14418
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14419
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14421
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14421
            .heldItem = ITEM_BLACK_BELT,
#line 14423
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14422
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14425
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14425
            .heldItem = ITEM_BLACK_BELT,
#line 14427
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14426
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14429
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_GIRL_TANYA_2] =
    {
#line 14430
        .trainerName = _("TANYA"),
#line 14431
        .trainerClass = TRAINER_CLASS_CRUSH_GIRL,
#line 14432
        .trainerPic = TRAINER_PIC_CRUSH_GIRL,
        .encounterMusic_gender =
#line 14434
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14435
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14436
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14438
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14438
            .heldItem = ITEM_BLACK_BELT,
#line 14440
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14439
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14442
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14442
            .heldItem = ITEM_BLACK_BELT,
#line 14444
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14443
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14446
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_GIRL_TANYA_3] =
    {
#line 14447
        .trainerName = _("TANYA"),
#line 14448
        .trainerClass = TRAINER_CLASS_CRUSH_GIRL,
#line 14449
        .trainerPic = TRAINER_PIC_CRUSH_GIRL,
        .encounterMusic_gender =
#line 14451
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14452
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14453
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14455
            .species = SPECIES_HITMONLEE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14455
            .heldItem = ITEM_BLACK_BELT,
#line 14457
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14456
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14459
            .species = SPECIES_HITMONCHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14459
            .heldItem = ITEM_BLACK_BELT,
#line 14461
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14460
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14463
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_SHEA_2] =
    {
#line 14464
        .trainerName = _("SHEA"),
#line 14465
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 14466
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 14468
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14469
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14470
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14472
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14472
            .heldItem = ITEM_BLACK_BELT,
#line 14474
            .iv = TRAINER_PARTY_IVS(21, 21, 21, 21, 21, 21),
#line 14473
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14476
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14476
            .heldItem = ITEM_BLACK_BELT,
#line 14478
            .iv = TRAINER_PARTY_IVS(21, 21, 21, 21, 21, 21),
#line 14477
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14480
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_SHEA_3] =
    {
#line 14481
        .trainerName = _("SHEA"),
#line 14482
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 14483
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 14485
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14486
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14487
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14489
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14489
            .heldItem = ITEM_BLACK_BELT,
#line 14491
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14490
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14493
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14493
            .heldItem = ITEM_BLACK_BELT,
#line 14495
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14494
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14497
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_HUGH_2] =
    {
#line 14498
        .trainerName = _("HUGH"),
#line 14499
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 14500
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 14502
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14503
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14504
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14506
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14506
            .heldItem = ITEM_BLACK_BELT,
#line 14508
            .iv = TRAINER_PARTY_IVS(21, 21, 21, 21, 21, 21),
#line 14507
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14510
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14510
            .heldItem = ITEM_BLACK_BELT,
#line 14512
            .iv = TRAINER_PARTY_IVS(21, 21, 21, 21, 21, 21),
#line 14511
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14514
    [DIFFICULTY_NORMAL][TRAINER_BLACK_BELT_HUGH_3] =
    {
#line 14515
        .trainerName = _("HUGH"),
#line 14516
        .trainerClass = TRAINER_CLASS_BLACK_BELT,
#line 14517
        .trainerPic = TRAINER_PIC_BLACK_BELT,
        .encounterMusic_gender =
#line 14519
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14520
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14521
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14523
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14523
            .heldItem = ITEM_BLACK_BELT,
#line 14525
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14524
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14527
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14527
            .heldItem = ITEM_BLACK_BELT,
#line 14529
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14528
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14531
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_KIN_MIK_KIA_2] =
    {
#line 14532
        .trainerName = _("MIK & KIA"),
#line 14533
        .trainerClass = TRAINER_CLASS_CRUSH_KIN,
#line 14534
        .trainerPic = TRAINER_PIC_CRUSH_KIN,
        .encounterMusic_gender =
#line 14536
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14537
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14538
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14540
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14540
            .heldItem = ITEM_BLACK_BELT,
#line 14542
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14541
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14544
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14544
            .heldItem = ITEM_BLACK_BELT,
#line 14546
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 14545
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14548
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_KIN_MIK_KIA_3] =
    {
#line 14549
        .trainerName = _("MIK & KIA"),
#line 14550
        .trainerClass = TRAINER_CLASS_CRUSH_KIN,
#line 14551
        .trainerPic = TRAINER_PIC_CRUSH_KIN,
        .encounterMusic_gender =
#line 14553
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14554
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14555
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14557
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14557
            .heldItem = ITEM_BLACK_BELT,
#line 14559
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14558
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14561
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14561
            .heldItem = ITEM_BLACK_BELT,
#line 14563
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14562
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14565
    [DIFFICULTY_NORMAL][TRAINER_TUBER_AMIRA_2] =
    {
#line 14566
        .trainerName = _("AMIRA"),
#line 14567
        .trainerClass = TRAINER_CLASS_TUBER,
#line 14568
        .trainerPic = TRAINER_PIC_TUBER_F,
        .encounterMusic_gender =
#line 14570
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14571
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14572
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 14574
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14576
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14575
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14578
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14580
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14579
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14582
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14584
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14583
            .lvl = 47,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14586
    [DIFFICULTY_NORMAL][TRAINER_TWINS_JOY_MEG_2] =
    {
#line 14587
        .trainerName = _("JOY & MEG"),
#line 14588
        .trainerClass = TRAINER_CLASS_TWINS,
#line 14589
        .trainerPic = TRAINER_PIC_TWINS,
        .encounterMusic_gender =
#line 14591
            TRAINER_ENCOUNTER_MUSIC_TWINS,
#line 14592
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14593
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14595
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14597
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14596
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14599
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14601
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 14600
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14603
    [DIFFICULTY_NORMAL][TRAINER_PAINTER_RAYNA_2] =
    {
#line 14604
        .trainerName = _("RAYNA"),
#line 14605
        .trainerClass = TRAINER_CLASS_PAINTER,
#line 14606
        .trainerPic = TRAINER_PIC_PAINTER,
        .encounterMusic_gender =
#line 14608
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 14609
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14610
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 14612
            .species = SPECIES_SMEARGLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14614
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14613
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14615
                MOVE_CROSS_CHOP,
                MOVE_MEGAHORN,
                MOVE_DOUBLE_EDGE,
                MOVE_SELF_DESTRUCT,
            },
            },
        },
    },
#line 14620
    [DIFFICULTY_NORMAL][TRAINER_YOUNGSTER_DESTIN_2] =
    {
#line 14621
        .trainerName = _("DESTIN"),
#line 14622
        .trainerClass = TRAINER_CLASS_YOUNGSTER,
#line 14623
        .trainerPic = TRAINER_PIC_YOUNGSTER,
        .encounterMusic_gender =
#line 14625
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 14626
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14627
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14629
            .species = SPECIES_RATICATE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14631
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14630
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14633
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14635
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14634
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14637
    [DIFFICULTY_NORMAL][TRAINER_PKMN_BREEDER_ALIZE_2] =
    {
#line 14638
        .trainerName = _("ALIZE"),
#line 14639
        .trainerClass = TRAINER_CLASS_PKMN_BREEDER,
#line 14640
        .trainerPic = TRAINER_PIC_POKEMON_BREEDER,
        .encounterMusic_gender =
#line 14642
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 14643
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14644
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 14646
            .species = SPECIES_PIKACHU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14648
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 14647
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14650
            .species = SPECIES_CLEFAIRY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14652
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 14651
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14654
            .species = SPECIES_MARILL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14656
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 14655
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14658
    [DIFFICULTY_NORMAL][TRAINER_YOUNG_COUPLE_GIA_JES_2] =
    {
#line 14659
        .trainerName = _("GIA & JES"),
#line 14660
        .trainerClass = TRAINER_CLASS_YOUNG_COUPLE,
#line 14661
        .trainerPic = TRAINER_PIC_YOUNG_COUPLE,
        .encounterMusic_gender =
#line 14663
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14664
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14665
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14667
            .species = SPECIES_NIDORINA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14669
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 14668
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14671
            .species = SPECIES_NIDORINO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14673
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 14672
            .lvl = 30,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14675
    [DIFFICULTY_NORMAL][TRAINER_YOUNG_COUPLE_GIA_JES_3] =
    {
#line 14676
        .trainerName = _("GIA & JES"),
#line 14677
        .trainerClass = TRAINER_CLASS_YOUNG_COUPLE,
#line 14678
        .trainerPic = TRAINER_PIC_YOUNG_COUPLE,
        .encounterMusic_gender =
#line 14680
            TRAINER_ENCOUNTER_MUSIC_GIRL,
#line 14681
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 14682
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14684
            .species = SPECIES_NIDOKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14686
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14685
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14688
            .species = SPECIES_NIDOQUEEN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14690
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14689
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14692
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_MILO_2] =
    {
#line 14693
        .trainerName = _("MILO"),
#line 14694
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 14695
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 14697
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14698
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14699
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14701
            .species = SPECIES_PIDGEOTTO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14703
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14702
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14705
            .species = SPECIES_PIDGEOT,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14707
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14706
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14709
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_CHAZ_2] =
    {
#line 14710
        .trainerName = _("CHAZ"),
#line 14711
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 14712
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 14714
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14715
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14716
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14718
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14720
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14719
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14722
            .species = SPECIES_FEAROW,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14724
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14723
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14726
    [DIFFICULTY_NORMAL][TRAINER_BIRD_KEEPER_HAROLD_2] =
    {
#line 14727
        .trainerName = _("HAROLD"),
#line 14728
        .trainerClass = TRAINER_CLASS_BIRD_KEEPER,
#line 14729
        .trainerPic = TRAINER_PIC_BIRD_KEEPER,
        .encounterMusic_gender =
#line 14731
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14732
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14733
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14735
            .species = SPECIES_NOCTOWL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14737
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14736
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14739
            .species = SPECIES_NOCTOWL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14741
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14740
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14743
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_NICOLE_2] =
    {
#line 14744
        .trainerName = _("NICOLE"),
#line 14745
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 14746
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 14748
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 14749
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14750
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 14752
            .species = SPECIES_MARILL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14754
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14753
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14756
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_JACLYN_2] =
    {
#line 14757
        .trainerName = _("JACLYN"),
#line 14758
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 14759
        .trainerPic = TRAINER_PIC_PSYCHIC_F,
        .encounterMusic_gender =
#line 14761
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14762
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14763
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 14765
            .species = SPECIES_NATU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14767
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14766
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14768
                MOVE_PSYCHIC,
                MOVE_CONFUSE_RAY,
                MOVE_FUTURE_SIGHT,
                MOVE_WISH,
            },
            },
            {
#line 14773
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14775
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14774
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14776
                MOVE_PSYCHIC,
                MOVE_HEADBUTT,
                MOVE_AMNESIA,
                MOVE_YAWN,
            },
            },
            {
#line 14781
            .species = SPECIES_KADABRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14783
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14782
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14784
                MOVE_PSYCHIC,
                MOVE_FUTURE_SIGHT,
                MOVE_RECOVER,
                MOVE_REFLECT,
            },
            },
        },
    },
#line 14789
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_SAMIR_2] =
    {
#line 14790
        .trainerName = _("SAMIR"),
#line 14791
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 14792
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 14794
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 14795
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14796
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 14798
            .species = SPECIES_GYARADOS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14800
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14799
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14802
    [DIFFICULTY_NORMAL][TRAINER_HIKER_EARL_2] =
    {
#line 14803
        .trainerName = _("EARL"),
#line 14804
        .trainerClass = TRAINER_CLASS_HIKER,
#line 14805
        .trainerPic = TRAINER_PIC_HIKER,
        .encounterMusic_gender =
#line 14807
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 14808
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14809
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14811
            .species = SPECIES_ONIX,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14813
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14812
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14815
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14817
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14816
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14819
    [DIFFICULTY_NORMAL][TRAINER_RUIN_MANIAC_LARRY_2] =
    {
#line 14820
        .trainerName = _("LARRY"),
#line 14821
        .trainerClass = TRAINER_CLASS_RUIN_MANIAC,
#line 14822
        .trainerPic = TRAINER_PIC_RUIN_MANIAC,
        .encounterMusic_gender =
#line 14824
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 14825
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14826
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14828
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14830
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14829
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14832
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14834
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14833
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14836
    [DIFFICULTY_NORMAL][TRAINER_POKEMANIAC_HECTOR_2] =
    {
#line 14837
        .trainerName = _("HECTOR"),
#line 14838
        .trainerClass = TRAINER_CLASS_POKEMANIAC,
#line 14839
        .trainerPic = TRAINER_PIC_POKEMANIAC,
        .encounterMusic_gender =
#line 14841
            TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS,
#line 14842
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14843
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14845
            .species = SPECIES_RHYDON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14847
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 14846
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14849
            .species = SPECIES_KANGASKHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14851
            .iv = TRAINER_PARTY_IVS(18, 18, 18, 18, 18, 18),
#line 14850
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14853
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_DARIO_2] =
    {
#line 14854
        .trainerName = _("DARIO"),
#line 14855
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 14856
        .trainerPic = TRAINER_PIC_PSYCHIC_M,
        .encounterMusic_gender =
#line 14858
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14859
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14860
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 14862
            .species = SPECIES_GIRAFARIG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14864
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14863
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14865
                MOVE_CRUNCH,
                MOVE_PSYBEAM,
                MOVE_ODOR_SLEUTH,
                MOVE_AGILITY,
            },
            },
        },
    },
#line 14870
    [DIFFICULTY_NORMAL][TRAINER_PSYCHIC_RODETTE_2] =
    {
#line 14871
        .trainerName = _("RODETTE"),
#line 14872
        .trainerClass = TRAINER_CLASS_PSYCHIC,
#line 14873
        .trainerPic = TRAINER_PIC_PSYCHIC_F,
        .encounterMusic_gender =
#line 14875
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14876
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14877
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 14879
            .species = SPECIES_NATU,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14881
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14880
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14882
                MOVE_PSYCHIC,
                MOVE_CONFUSE_RAY,
                MOVE_WISH,
                MOVE_FUTURE_SIGHT,
            },
            },
            {
#line 14887
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14889
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14888
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14890
                MOVE_PSYCHIC,
                MOVE_DISABLE,
                MOVE_PSYCH_UP,
                MOVE_FUTURE_SIGHT,
            },
            },
            {
#line 14895
            .species = SPECIES_HYPNO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14897
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14896
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14898
                MOVE_PSYCHIC,
                MOVE_HYPNOSIS,
                MOVE_PSYCH_UP,
                MOVE_FUTURE_SIGHT,
            },
            },
        },
    },
#line 14903
    [DIFFICULTY_NORMAL][TRAINER_JUGGLER_MASON_2] =
    {
#line 14904
        .trainerName = _("MASON"),
#line 14905
        .trainerClass = TRAINER_CLASS_JUGGLER,
#line 14906
        .trainerPic = TRAINER_PIC_JUGGLER,
        .encounterMusic_gender =
#line 14908
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 14909
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14910
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 14912
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14914
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14913
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14916
            .species = SPECIES_PINECO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14918
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14917
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14920
            .species = SPECIES_ELECTRODE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14922
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14921
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14924
            .species = SPECIES_PINECO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14926
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 14925
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 14928
    [DIFFICULTY_NORMAL][TRAINER_PKMN_RANGER_NICOLAS_2] =
    {
#line 14929
        .trainerName = _("NICOLAS"),
#line 14930
        .trainerClass = TRAINER_CLASS_PKMN_RANGER,
#line 14931
        .trainerPic = TRAINER_PIC_POKEMON_RANGER_M,
        .encounterMusic_gender =
#line 14933
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14934
        .items = { ITEM_FULL_RESTORE },
#line 14935
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14936
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14938
            .species = SPECIES_VICTREEBEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14940
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14939
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14941
                MOVE_RAZOR_LEAF,
                MOVE_ACID,
                MOVE_STUN_SPORE,
                MOVE_WRAP,
            },
            },
            {
#line 14946
            .species = SPECIES_VICTREEBEL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14948
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14947
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14949
                MOVE_RAZOR_LEAF,
                MOVE_ACID,
                MOVE_SLEEP_POWDER,
                MOVE_SLAM,
            },
            },
        },
    },
#line 14954
    [DIFFICULTY_NORMAL][TRAINER_PKMN_RANGER_MADELINE_2] =
    {
#line 14955
        .trainerName = _("MADELINE"),
#line 14956
        .trainerClass = TRAINER_CLASS_PKMN_RANGER,
#line 14957
        .trainerPic = TRAINER_PIC_POKEMON_RANGER_F,
        .encounterMusic_gender =
#line 14959
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 14960
        .items = { ITEM_FULL_RESTORE },
#line 14961
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14962
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 14964
            .species = SPECIES_VILEPLUME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14966
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14965
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14967
                MOVE_PETAL_DANCE,
                MOVE_MOONLIGHT,
                MOVE_ACID,
                MOVE_SLEEP_POWDER,
            },
            },
            {
#line 14972
            .species = SPECIES_VILEPLUME,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14974
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 14973
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 14975
                MOVE_PETAL_DANCE,
                MOVE_MOONLIGHT,
                MOVE_ACID,
                MOVE_STUN_SPORE,
            },
            },
        },
    },
#line 14980
    [DIFFICULTY_NORMAL][TRAINER_CRUSH_GIRL_CYNDY_2] =
    {
#line 14981
        .trainerName = _("CYNDY"),
#line 14982
        .trainerClass = TRAINER_CLASS_CRUSH_GIRL,
#line 14983
        .trainerPic = TRAINER_PIC_CRUSH_GIRL,
        .encounterMusic_gender =
#line 14985
            TRAINER_ENCOUNTER_MUSIC_INTENSE,
#line 14986
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 14987
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 14989
            .species = SPECIES_PRIMEAPE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14989
            .heldItem = ITEM_BLACK_BELT,
#line 14991
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14990
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14993
            .species = SPECIES_HITMONTOP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14993
            .heldItem = ITEM_BLACK_BELT,
#line 14995
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14994
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 14997
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 14997
            .heldItem = ITEM_BLACK_BELT,
#line 14999
            .iv = TRAINER_PARTY_IVS(20, 20, 20, 20, 20, 20),
#line 14998
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15001
    [DIFFICULTY_NORMAL][TRAINER_TAMER_EVAN_2] =
    {
#line 15002
        .trainerName = _("EVAN"),
#line 15003
        .trainerClass = TRAINER_CLASS_TAMER,
#line 15004
        .trainerPic = TRAINER_PIC_TAMER,
        .encounterMusic_gender =
#line 15006
            TRAINER_ENCOUNTER_MUSIC_HIKER,
#line 15007
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15008
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 15010
            .species = SPECIES_SANDSLASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15012
            .iv = TRAINER_PARTY_IVS(19, 19, 19, 19, 19, 19),
#line 15011
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15014
            .species = SPECIES_LICKITUNG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15016
            .iv = TRAINER_PARTY_IVS(19, 19, 19, 19, 19, 19),
#line 15015
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15018
            .species = SPECIES_URSARING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15020
            .iv = TRAINER_PARTY_IVS(19, 19, 19, 19, 19, 19),
#line 15019
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15022
    [DIFFICULTY_NORMAL][TRAINER_PKMN_RANGER_JACKSON_2] =
    {
#line 15023
        .trainerName = _("JACKSON"),
#line 15024
        .trainerClass = TRAINER_CLASS_PKMN_RANGER,
#line 15025
        .trainerPic = TRAINER_PIC_POKEMON_RANGER_M,
        .encounterMusic_gender =
#line 15027
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 15028
        .items = { ITEM_FULL_RESTORE },
#line 15029
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15030
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 15032
            .species = SPECIES_TANGELA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15034
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15033
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15035
                MOVE_SLAM,
                MOVE_MEGA_DRAIN,
                MOVE_BIND,
                MOVE_INGRAIN,
            },
            },
            {
#line 15040
            .species = SPECIES_EXEGGUTOR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15042
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15041
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15043
                MOVE_CONFUSION,
                MOVE_EGG_BOMB,
                MOVE_STUN_SPORE,
                MOVE_REFLECT,
            },
            },
            {
#line 15048
            .species = SPECIES_EXEGGUTOR,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15050
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15049
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15051
                MOVE_CONFUSION,
                MOVE_EGG_BOMB,
                MOVE_SLEEP_POWDER,
                MOVE_STOMP,
            },
            },
        },
    },
#line 15056
    [DIFFICULTY_NORMAL][TRAINER_PKMN_RANGER_KATELYN_2] =
    {
#line 15057
        .trainerName = _("KATELYN"),
#line 15058
        .trainerClass = TRAINER_CLASS_PKMN_RANGER,
#line 15059
        .trainerPic = TRAINER_PIC_POKEMON_RANGER_F,
        .encounterMusic_gender =
#line 15061
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 15062
        .items = { ITEM_FULL_RESTORE },
#line 15063
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15064
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 1,
        .party = (const struct TrainerMon[])
        {
            {
#line 15066
            .species = SPECIES_CHANSEY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15068
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15067
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15069
                MOVE_EGG_BOMB,
                MOVE_DEFENSE_CURL,
                MOVE_MINIMIZE,
                MOVE_SOFT_BOILED,
            },
            },
        },
    },
#line 15074
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_LEROY_2] =
    {
#line 15075
        .trainerName = _("LEROY"),
#line 15076
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 15077
        .trainerPic = TRAINER_PIC_COOLTRAINER_M,
        .encounterMusic_gender =
#line 15079
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 15080
        .items = { ITEM_FULL_RESTORE },
#line 15081
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15082
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 15084
            .species = SPECIES_RHYDON,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15086
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15085
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15087
                MOVE_EARTHQUAKE,
                MOVE_HORN_DRILL,
                MOVE_ROCK_BLAST,
                MOVE_SCARY_FACE,
            },
            },
            {
#line 15092
            .species = SPECIES_SLOWBRO,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15094
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15093
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15095
                MOVE_PSYCHIC,
                MOVE_HEADBUTT,
                MOVE_AMNESIA,
                MOVE_DISABLE,
            },
            },
            {
#line 15100
            .species = SPECIES_KANGASKHAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15102
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15101
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15103
                MOVE_DIZZY_PUNCH,
                MOVE_BITE,
                MOVE_ENDURE,
                MOVE_REVERSAL,
            },
            },
            {
#line 15108
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15110
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15109
            .lvl = 52,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15111
                MOVE_CROSS_CHOP,
                MOVE_VITAL_THROW,
                MOVE_REVENGE,
                MOVE_SEISMIC_TOSS,
            },
            },
            {
#line 15116
            .species = SPECIES_URSARING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15118
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15117
            .lvl = 55,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15119
                MOVE_SLASH,
                MOVE_FAINT_ATTACK,
                MOVE_SNORE,
                MOVE_REST,
            },
            },
        },
    },
#line 15124
    [DIFFICULTY_NORMAL][TRAINER_COOLTRAINER_MICHELLE_2] =
    {
#line 15125
        .trainerName = _("MICHELLE"),
#line 15126
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
#line 15127
        .trainerPic = TRAINER_PIC_COOLTRAINER_F,
        .encounterMusic_gender =
#line 15129
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 15130
        .items = { ITEM_HYPER_POTION },
#line 15131
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15132
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 5,
        .party = (const struct TrainerMon[])
        {
            {
#line 15134
            .species = SPECIES_PERSIAN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15136
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15135
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15137
                MOVE_SLASH,
                MOVE_SCREECH,
                MOVE_FAINT_ATTACK,
                MOVE_BITE,
            },
            },
            {
#line 15142
            .species = SPECIES_DEWGONG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15144
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15143
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15145
                MOVE_ICE_BEAM,
                MOVE_TAKE_DOWN,
                MOVE_ICY_WIND,
                MOVE_SHEER_COLD,
            },
            },
            {
#line 15150
            .species = SPECIES_NINETALES,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15152
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15151
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15153
                MOVE_FLAMETHROWER,
                MOVE_CONFUSE_RAY,
                MOVE_WILL_O_WISP,
                MOVE_GRUDGE,
            },
            },
            {
#line 15158
            .species = SPECIES_RAPIDASH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15160
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15159
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15161
                MOVE_BOUNCE,
                MOVE_AGILITY,
                MOVE_FIRE_SPIN,
                MOVE_TAKE_DOWN,
            },
            },
            {
#line 15166
            .species = SPECIES_GIRAFARIG,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15168
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15167
            .lvl = 56,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15169
                MOVE_CRUNCH,
                MOVE_PSYBEAM,
                MOVE_STOMP,
                MOVE_ODOR_SLEUTH,
            },
            },
        },
    },
#line 15174
    [DIFFICULTY_NORMAL][TRAINER_COOL_COUPLE_LEX_NYA_2] =
    {
#line 15175
        .trainerName = _("LEX & NYA"),
#line 15176
        .trainerClass = TRAINER_CLASS_COOL_COUPLE,
#line 15177
        .trainerPic = TRAINER_PIC_COOL_COUPLE,
        .encounterMusic_gender =
#line 15179
            TRAINER_ENCOUNTER_MUSIC_COOL,
#line 15180
        .items = { ITEM_FULL_RESTORE, ITEM_FULL_RESTORE },
#line 15181
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 15182
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 15184
            .species = SPECIES_MILTANK,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15186
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15185
            .lvl = 57,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15187
                MOVE_BODY_SLAM,
                MOVE_MILK_DRINK,
                MOVE_GROWL,
                MOVE_DEFENSE_CURL,
            },
            },
            {
#line 15192
            .species = SPECIES_TAUROS,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15194
            .iv = TRAINER_PARTY_IVS(26, 26, 26, 26, 26, 26),
#line 15193
            .lvl = 57,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15195
                MOVE_TAKE_DOWN,
                MOVE_SCARY_FACE,
                MOVE_PURSUIT,
                MOVE_SWAGGER,
            },
            },
        },
    },
#line 15200
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_COLTON_2] =
    {
#line 15201
        .trainerName = _("COLTON"),
#line 15202
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 15203
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 15205
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 15206
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15207
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 15209
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15211
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 15210
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15213
            .species = SPECIES_WEEDLE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15215
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 15214
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15217
            .species = SPECIES_METAPOD,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15219
            .iv = TRAINER_PARTY_IVS(2, 2, 2, 2, 2, 2),
#line 15218
            .lvl = 19,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15221
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_COLTON_3] =
    {
#line 15222
        .trainerName = _("COLTON"),
#line 15223
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 15224
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 15226
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 15227
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15228
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 15230
            .species = SPECIES_BUTTERFREE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15232
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 15231
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15234
            .species = SPECIES_KAKUNA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15236
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 15235
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15238
            .species = SPECIES_BUTTERFREE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15240
            .iv = TRAINER_PARTY_IVS(7, 7, 7, 7, 7, 7),
#line 15239
            .lvl = 27,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15242
    [DIFFICULTY_NORMAL][TRAINER_BUG_CATCHER_COLTON_4] =
    {
#line 15243
        .trainerName = _("COLTON"),
#line 15244
        .trainerClass = TRAINER_CLASS_BUG_CATCHER,
#line 15245
        .trainerPic = TRAINER_PIC_BUG_CATCHER,
        .encounterMusic_gender =
#line 15247
            TRAINER_ENCOUNTER_MUSIC_MALE,
#line 15248
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15249
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 3,
        .party = (const struct TrainerMon[])
        {
            {
#line 15251
            .species = SPECIES_BUTTERFREE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15253
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 15252
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15255
            .species = SPECIES_BEEDRILL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15257
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 15256
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15259
            .species = SPECIES_BUTTERFREE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15261
            .iv = TRAINER_PARTY_IVS(14, 14, 14, 14, 14, 14),
#line 15260
            .lvl = 51,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15263
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_MATTHEW_2] =
    {
#line 15264
        .trainerName = _("MATTHEW"),
#line 15265
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 15266
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 15268
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 15269
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15270
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 15272
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15274
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 15273
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15276
            .species = SPECIES_POLIWRATH,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15278
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 15277
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15280
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_MALE_TONY_2] =
    {
#line 15281
        .trainerName = _("TONY"),
#line 15282
        .trainerClass = TRAINER_CLASS_SWIMMER_M,
#line 15283
        .trainerPic = TRAINER_PIC_SWIMMER_M,
        .encounterMusic_gender =
#line 15285
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 15286
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15287
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 15289
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15291
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 15290
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15293
            .species = SPECIES_SEADRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15295
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 15294
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15297
    [DIFFICULTY_NORMAL][TRAINER_SWIMMER_FEMALE_MELISSA_2] =
    {
#line 15298
        .trainerName = _("MELISSA"),
#line 15299
        .trainerClass = TRAINER_CLASS_SWIMMER_F,
#line 15300
        .trainerPic = TRAINER_PIC_SWIMMER_F,
        .encounterMusic_gender =
#line 15302
            TRAINER_ENCOUNTER_MUSIC_FEMALE,
#line 15303
        .battleType = TRAINER_BATTLE_TYPE_SINGLES,
#line 15304
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 15306
            .species = SPECIES_POLIWHIRL,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15308
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 15307
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
            {
#line 15310
            .species = SPECIES_SEAKING,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15312
            .iv = TRAINER_PARTY_IVS(9, 9, 9, 9, 9, 9),
#line 15311
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            },
        },
    },
#line 15735
    [DIFFICULTY_NORMAL][TRAINER_HAVORA_DOCK_CREW] =
    {
#line 15736
        .trainerName = _("DOCK CREW"),
#line 15737
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 15738
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 15740
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 15741
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 15742
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 15744
            .species = SPECIES_MACHOKE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15746
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15745
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15747
                MOVE_BRICK_BREAK,
                MOVE_ROCK_SLIDE,
                MOVE_PROTECT,
                MOVE_HELPING_HAND,
            },
            },
            {
#line 15752
            .species = SPECIES_PELIPPER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15754
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15753
            .lvl = 49,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15755
                MOVE_WATER_PULSE,
                MOVE_AIR_SLASH,
                MOVE_PROTECT,
                MOVE_TAILWIND,
            },
            },
        },
    },
#line 15760
    [DIFFICULTY_NORMAL][TRAINER_HAVORA_NAVIGATOR] =
    {
#line 15761
        .trainerName = _("NAVIGATOR"),
#line 15762
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 15763
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 15765
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 15766
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 15767
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 2,
        .party = (const struct TrainerMon[])
        {
            {
#line 15769
            .species = SPECIES_LANTURN,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15771
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15770
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15772
                MOVE_SURF,
                MOVE_THUNDERBOLT,
                MOVE_PROTECT,
                MOVE_THUNDER_WAVE,
            },
            },
            {
#line 15777
            .species = SPECIES_SKARMORY,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15779
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15778
            .lvl = 50,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15780
                MOVE_STEEL_WING,
                MOVE_AERIAL_ACE,
                MOVE_PROTECT,
                MOVE_TAILWIND,
            },
            },
        },
    },
#line 15785
    [DIFFICULTY_NORMAL][TRAINER_HAVORA_CAPTAIN] =
    {
#line 15786
        .trainerName = _("EIRIK"),
#line 15787
        .trainerClass = TRAINER_CLASS_SAILOR,
#line 15788
        .trainerPic = TRAINER_PIC_SAILOR,
        .encounterMusic_gender =
#line 15790
            TRAINER_ENCOUNTER_MUSIC_SWIMMER,
#line 15791
        .battleType = TRAINER_BATTLE_TYPE_DOUBLES,
#line 15792
        .aiFlags = AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY,
        .partySize = 4,
        .party = (const struct TrainerMon[])
        {
            {
#line 15794
            .species = SPECIES_PELIPPER,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15796
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15795
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15797
                MOVE_SURF,
                MOVE_HURRICANE,
                MOVE_PROTECT,
                MOVE_TAILWIND,
            },
            },
            {
#line 15802
            .species = SPECIES_MAGNEZONE,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15804
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15803
            .lvl = 53,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15805
                MOVE_THUNDERBOLT,
                MOVE_FLASH_CANNON,
                MOVE_PROTECT,
                MOVE_LIGHT_SCREEN,
            },
            },
            {
#line 15810
            .species = SPECIES_MACHAMP,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15812
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15811
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15813
                MOVE_BRICK_BREAK,
                MOVE_ROCK_SLIDE,
                MOVE_PROTECT,
                MOVE_HELPING_HAND,
            },
            },
            {
#line 15818
            .species = SPECIES_KINGDRA,
            .gender = TRAINER_MON_RANDOM_GENDER,
#line 15820
            .iv = TRAINER_PARTY_IVS(15, 15, 15, 15, 15, 15),
#line 15819
            .lvl = 54,
            .nature = NATURE_HARDY,
            .dynamaxLevel = MAX_DYNAMAX_LEVEL,
            .moves = {
#line 15821
                MOVE_SURF,
                MOVE_DRAGON_PULSE,
                MOVE_PROTECT,
                MOVE_RAIN_DANCE,
            },
            },
        },
    },
