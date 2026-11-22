// Optional fixed parties inserted alongside the generated trainer table.
[DIFFICULTY_NORMAL][TRAINER_PEWTER_PRACTICE_ROCK] = {
    .trainerName = _("GUIDE"),
    .trainerClass = TRAINER_CLASS_CAMPER,
    .trainerPic = TRAINER_PIC_CAMPER,
    .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
    .battleType = TRAINER_BATTLE_TYPE_SINGLES,
    .aiFlags = AI_FLAG_QUANTUM_GYM_TRAINER,
    .partySize = 1,
    .party = (const struct TrainerMon[]) {
        {.species = SPECIES_GEODUDE, .lvl = 10, .moves = {MOVE_TACKLE, MOVE_DEFENSE_CURL}},
    },
},
[DIFFICULTY_NORMAL][TRAINER_PEWTER_PRACTICE_TRAIL] = {
    .trainerName = _("GUIDE"),
    .trainerClass = TRAINER_CLASS_CAMPER,
    .trainerPic = TRAINER_PIC_CAMPER,
    .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE,
    .battleType = TRAINER_BATTLE_TYPE_SINGLES,
    .aiFlags = AI_FLAG_QUANTUM_GYM_TRAINER,
    .partySize = 1,
    .party = (const struct TrainerMon[]) {
        {.species = SPECIES_SANDSHREW, .lvl = 11, .moves = {MOVE_SCRATCH, MOVE_SAND_ATTACK}},
    },
},
