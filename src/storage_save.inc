// Flash keeps the 14-box layout so existing checksums, rotation and backups
// remain compatible. Empty retired slots are serialized as zeroes.
STATIC_ASSERT(sizeof(struct LegacyPokemonStorage) == 34144, LegacyStorageFlashLayout);
STATIC_ASSERT(TOTAL_BOXES_COUNT <= LEGACY_BOXES_COUNT, StorageBoxCapacity);

static u8 *StorageByteAt(u32 offset)
{
#define STORAGE_RANGE(member) \
    if (offset >= offsetof(struct LegacyPokemonStorage, member) \
     && offset < offsetof(struct LegacyPokemonStorage, member) + sizeof(gPokemonStoragePtr->member)) \
        return (u8 *)&gPokemonStoragePtr->member + offset - offsetof(struct LegacyPokemonStorage, member)
    STORAGE_RANGE(currentBox);
    STORAGE_RANGE(boxes);
    STORAGE_RANGE(boxNames);
    STORAGE_RANGE(boxWallpapers);
    STORAGE_RANGE(fusions);
#undef STORAGE_RANGE
    return NULL;
}

static void SerializeStorageSector(u16 sectorId, u16 size)
{
    u32 offset = (sectorId - SECTOR_ID_PKMN_STORAGE_START) * SECTOR_DATA_SIZE;
    u16 i;
    for (i = 0; i < size; i++)
    {
        u8 *byte = StorageByteAt(offset + i);
        gReadWriteSector->data[i] = byte == NULL ? 0 : *byte;
    }
}

static bool8 ImportLegacyStorage(const struct LegacyPokemonStorage *legacy)
{
    u16 box, slot, target = 0, count = 0;
    for (box = 0; box < LEGACY_BOXES_COUNT; box++)
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
            if (GetBoxMonData((struct BoxPokemon *)&legacy->boxes[box][slot], MON_DATA_SANITY_HAS_SPECIES))
                count++;
    if (count > TOTAL_BOXES_COUNT * IN_BOX_COUNT)
        return FALSE;

    // Keep the first six boxes' positions, names and wallpapers unchanged.
    memcpy(gPokemonStoragePtr->boxes, legacy->boxes, sizeof(gPokemonStoragePtr->boxes));
    memcpy(gPokemonStoragePtr->boxNames, legacy->boxNames, sizeof(gPokemonStoragePtr->boxNames));
    memcpy(gPokemonStoragePtr->boxWallpapers, legacy->boxWallpapers, sizeof(gPokemonStoragePtr->boxWallpapers));
    memcpy(gPokemonStoragePtr->fusions, legacy->fusions, sizeof(gPokemonStoragePtr->fusions));
    gPokemonStoragePtr->currentBox = legacy->currentBox < TOTAL_BOXES_COUNT ? legacy->currentBox : 0;
    if (VarGet(VAR_PC_BOX_TO_SEND_MON) >= TOTAL_BOXES_COUNT)
        VarSet(VAR_PC_BOX_TO_SEND_MON, 0);
    for (box = TOTAL_BOXES_COUNT; box < LEGACY_BOXES_COUNT; box++)
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
        {
            struct BoxPokemon *mon = (struct BoxPokemon *)&legacy->boxes[box][slot];
            if (!GetBoxMonData(mon, MON_DATA_SANITY_HAS_SPECIES))
                continue;
            while (GetBoxMonData(&gPokemonStoragePtr->boxes[target / IN_BOX_COUNT][target % IN_BOX_COUNT], MON_DATA_SANITY_HAS_SPECIES))
                target++;
            gPokemonStoragePtr->boxes[target / IN_BOX_COUNT][target % IN_BOX_COUNT] = *mon;
        }
    return TRUE;
}
