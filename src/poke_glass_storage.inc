// Storage shares the tablet's window/tile buffer. No PC screen allocation,
// duplicate box cache, or held-Pokemon buffer is needed: moves commit atomically.
static void GlassReadSlot(bool8 party, u8 box, u8 slot, struct Pokemon *mon)
{
    memset(mon, 0, sizeof(*mon));
    ZeroMonData(mon);
    if (party)
        *mon = gPlayerParty[slot];
    else if (GetBoxMonData(&gPokemonStoragePtr->boxes[box][slot], MON_DATA_SANITY_HAS_SPECIES))
        BoxMonToMon(&gPokemonStoragePtr->boxes[box][slot], mon);
}

static void GlassWriteSlot(bool8 party, u8 box, u8 slot, struct Pokemon *mon)
{
    if (party)
        gPlayerParty[slot] = *mon;
    else
    {
        if (!GetMonData(mon, MON_DATA_SANITY_HAS_SPECIES))
        {
            ZeroBoxMonAt(box, slot);
            return;
        }
        if (OW_PC_HEAL <= GEN_7) HealPokemon(mon);
        BoxMonRestorePP(&mon->box);
        SetBoxMonAt(box, slot, &mon->box);
    }
}

static u16 GlassBagItem(u16 index)
{
    u16 pocket, slot;
    for (pocket = 0; pocket < POCKETS_COUNT; pocket++)
    {
        if (pocket == POCKET_KEY_ITEMS || pocket == POCKET_TM_HM) continue;
        for (slot = 0; slot < gBagPockets[pocket].capacity; slot++)
        {
            u16 item = GetBagItemId(pocket, slot);
            if (item == ITEM_NONE || !GetBagItemQuantity(pocket, slot)
                || GetItemImportance(item) || ItemIsMail(item)) continue;
            if (index-- == 0) return item;
        }
    }
    return ITEM_NONE;
}

struct GlassStorageIcons
{
    u8 ids[PARTY_SIZE + IN_BOX_COUNT];
    u16 species[PARTY_SIZE + IN_BOX_COUNT];
    u32 personalities[PARTY_SIZE + IN_BOX_COUNT];
    u32 paletteMask;
};
static EWRAM_DATA struct GlassStorageIcons *sGlassStorageIcons = NULL;

static void GlassStoragePosition(u8 index, s16 *x, s16 *y)
{
    if (index < PARTY_SIZE) { *x = 28 + index % 2 * 26; *y = 42 + index / 2 * 36; }
    else { index -= PARTY_SIZE; *x = 88 + index % 6 * 24; *y = 42 + index / 6 * 20; }
}

static void DestroyGlassStorageIcons(void)
{
    u8 i;
    if (sGlassStorageIcons == NULL) return;
    for (i = 0; i < PARTY_SIZE + IN_BOX_COUNT; i++)
        if (sGlassStorageIcons->ids[i] < MAX_SPRITES)
            FreeAndDestroyMonIconSprite(&gSprites[sGlassStorageIcons->ids[i]]);
    for (i = 0; i < ARRAY_COUNT(gMonIconPaletteTable); i++)
        if (sGlassStorageIcons->paletteMask & (1u << i))
            FreeSpritePaletteByTag(gMonIconPaletteTable[i].tag);
    Free(sGlassStorageIcons);
    sGlassStorageIcons = NULL;
}

static void UpdateGlassStorageIcons(u8 taskId)
{
    u8 i;
    s16 *d = gTasks[taskId].data;
    if (sGlassStorageIcons == NULL) return;
    for (i = 0; i < PARTY_SIZE + IN_BOX_COUNT; i++)
    {
        struct Pokemon mon;
        s16 x, y;
        u16 species;
        u32 personality;
        u8 *id = &sGlassStorageIcons->ids[i];
        GlassReadSlot(i < PARTY_SIZE, d[0], i < PARTY_SIZE ? i : i - PARTY_SIZE, &mon);
        species = GetMonData(&mon, MON_DATA_SANITY_HAS_SPECIES) ? GetMonData(&mon, MON_DATA_SPECIES_OR_EGG) : SPECIES_NONE;
        personality = GetMonData(&mon, MON_DATA_PERSONALITY);
        if (species != sGlassStorageIcons->species[i] || personality != sGlassStorageIcons->personalities[i])
        {
            if (*id < MAX_SPRITES) FreeAndDestroyMonIconSprite(&gSprites[*id]);
            *id = MAX_SPRITES;
            sGlassStorageIcons->species[i] = species;
            sGlassStorageIcons->personalities[i] = personality;
            if (species != SPECIES_NONE)
            {
                u8 pal;
                for (pal = 0; pal < ARRAY_COUNT(gMonIconPaletteTable); pal++)
                    if (IndexOfSpritePaletteTag(gMonIconPaletteTable[pal].tag) == 0xFF)
                        sGlassStorageIcons->paletteMask |= 1u << pal;
                LoadMonIconPalettePersonality(species, personality);
                GlassStoragePosition(i, &x, &y);
                *id = CreateMonIcon(species, SpriteCB_MonIcon, x, y, 0, personality);
                if (*id < MAX_SPRITES) gSprites[*id].oam.priority = 0;
            }
        }
        if (*id < MAX_SPRITES)
        {
            GlassStoragePosition(i, &x, &y);
            gSprites[*id].x = x;
            gSprites[*id].y = y;
            gSprites[*id].invisible = d[9] != 0;
            if (d[9] == 3 && i == d[2])
            {
                gSprites[*id].x = 44;
                gSprites[*id].y = 66;
                gSprites[*id].invisible = FALSE;
            }
        }
    }
}

static void DrawGlassStorage(u8 taskId)
{
    s16 *d = gTasks[taskId].data;
    u8 row, text[32];
    struct Pokemon mon;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    // Quiet the scenery behind dense management text without another buffer.
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(14, 4));
    HubRect(4, 10, 10, 220, 140);
    if (d[9] == 3)
    {
        u16 species, level, move;
        bool8 egg;
        GlassReadSlot(d[2] < PARTY_SIZE, d[0], d[2] < PARTY_SIZE ? d[2] : d[2] - PARTY_SIZE, &mon);
        species = GetMonData(&mon, MON_DATA_SPECIES);
        egg = GetMonData(&mon, MON_DATA_IS_EGG);
        GetMonData(&mon, MON_DATA_NICKNAME, text);
        StringGet_Nickname(text);
        StatsTextFit(16, 14, 145, text);
        if (!egg)
        {
            StatsText(169, 14, COMPOUND_STRING("Lv."));
            level = GetMonData(&mon, MON_DATA_LEVEL);
            StatsNumber(218, 14, level);
            StatsText(16, 30, gTypesInfo[gSpeciesInfo[species].types[0]].name);
            if (gSpeciesInfo[species].types[1] != gSpeciesInfo[species].types[0])
                StatsText(71, 30, gTypesInfo[gSpeciesInfo[species].types[1]].name);
            StatsText(88, 48, COMPOUND_STRING("Nature"));
            StatsText(88, 61, gNaturesInfo[GetMonData(&mon, MON_DATA_HIDDEN_NATURE)].name);
            StatsText(88, 81, GetMonData(&mon, MON_DATA_HELD_ITEM) == ITEM_NONE ? COMPOUND_STRING("No held item") : GetItemName(GetMonData(&mon, MON_DATA_HELD_ITEM)));
            StatsText(16, 93, COMPOUND_STRING("Ability:"));
            StatsText(76, 93, gAbilitiesInfo[GetMonAbility(&mon)].name);
            for (row = 0; row < MAX_MON_MOVES; row++)
            {
                move = GetMonData(&mon, MON_DATA_MOVE1 + row);
                StringCopyN(text, move ? gMovesInfo[move].name : COMPOUND_STRING("-"), sizeof(text) - 1);
                text[sizeof(text) - 1] = EOS;
                while (GetStringWidth(FONT_SMALL, text, 0) > 95 && StringLength(text))
                    text[StringLength(text) - 1] = EOS;
                StatsText(16 + row % 2 * 108, 108 + row / 2 * 13, text);
            }
        }
        else StatsText(88, 61, COMPOUND_STRING("An Egg. Keep it safe."));
        StatsText(16, 136, COMPOUND_STRING("A/B:Back"));
        goto copy;
    }
    if (d[9] == 2)
    {
        GlassReadSlot(d[3], d[5], d[4], &mon);
        GetMonData(&mon, MON_DATA_NICKNAME, text);
        StringGet_Nickname(text);
        StatsText(18, 20, COMPOUND_STRING("Release POKéMON?"));
        StatsText(18, 43, text);
        StatsText(18, 65, COMPOUND_STRING("This cannot be undone."));
        StatsText(18, 113, COMPOUND_STRING("A:Release  B:Keep"));
        goto copy;
    }
    if (d[9] == 1)
    {
        StatsText(16, 14, COMPOUND_STRING("Give held item"));
        for (row = 0; row < 6; row++)
        {
            u16 index = d[10] / 6 * 6 + row, item = GlassBagItem(index);
            if (item == ITEM_NONE) break;
            HubRect(index == d[10] ? 6 : 4, 17, 32 + row * 11, 190, 11);
            CopyItemName(item, text);
            StatsTextFit(22, 32 + row * 11, 181, text);
        }
        StatsText(18, 113, COMPOUND_STRING("A:Give  B:Cancel"));
        goto copy;
    }
    StatsText(16, 14, COMPOUND_STRING("PARTY"));
    StatsTextFit(80, 14, 84, gPokemonStoragePtr->boxNames[d[0]]);
    StatsNumber(211, 14, d[0] + 1);
    StatsText(212, 14, COMPOUND_STRING("/6"));
    StatsText(170, 14, COMPOUND_STRING("L/R"));
    for (row = 0; row < PARTY_SIZE + IN_BOX_COUNT; row++)
    {
        s16 x, y;
        bool8 party = row < PARTY_SIZE;
        u8 slot = party ? row : row - PARTY_SIZE;
        bool8 source = d[6] && d[3] == party && d[4] == slot && (party || d[5] == d[0]);
        GlassStoragePosition(row, &x, &y);
        HubRect(d[2] == row ? 6 : source ? 9 : 3, x - 12, y - 10, 24, 20);
        HubRect(d[2] == row ? 5 : 4, x - 11, y - 9, 22, 18);
        if (source) StatsText(x - 9, y - 8, COMPOUND_STRING(">"));
    }
    HubRect(6, 70, 29, 1, 100);
    if (d[7] == 1)
        StatsText(14, 138, COMPOUND_STRING("Keep one able POKéMON."));
    else if (d[7] == 2)
        StatsText(14, 138, COMPOUND_STRING("Remove MAIL first."));
    else if (d[7] == 3)
        StatsText(14, 138, COMPOUND_STRING("BAG full. Item unchanged."));
    else if (d[7] == 4)
        StatsText(14, 138, COMPOUND_STRING("Item moved to BAG."));
    else if (d[7] == 5)
        StatsText(14, 138, COMPOUND_STRING("Held item given."));
    else if (d[7] == 6)
        StatsText(14, 138, COMPOUND_STRING("Eggs cannot be released."));
    else if (d[6])
        StatsText(14, 138, COMPOUND_STRING("A:Place SELECT:Release B:Cancel"));
    else
        StatsText(14, 138, COMPOUND_STRING("A:Move SELECT:Item START:Info"));

copy:
    UpdateGlassStorageIcons(taskId);
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static void Task_PokeGlassStorage(u8 taskId)
{
    s16 *d = gTasks[taskId].data;
    bool8 party;
    u8 slot;
    struct Pokemon source, target;
    if (gPaletteFade.active) return;
    if (d[8] < 2) { d[8]++; return; }
    party = d[2] < PARTY_SIZE;
    slot = party ? d[2] : d[2] - PARTY_SIZE;
    if (d[9] == 3)
    {
        if (JOY_NEW(A_BUTTON | B_BUTTON | START_BUTTON))
        { d[9] = 0; DrawGlassStorage(taskId); }
        return;
    }
    if (d[9] == 2)
    {
        if (JOY_NEW(B_BUTTON)) d[9] = 0;
        else if (JOY_NEW(A_BUTTON))
        {
            u16 item;
            GlassReadSlot(d[3], d[5], d[4], &source);
            item = GetMonData(&source, MON_DATA_HELD_ITEM);
            d[7] = 0;
            if (GetMonData(&source, MON_DATA_IS_EGG)) d[7] = 6;
            else if (ItemIsMail(item)) d[7] = 2;
            else if (d[3] && !CountPartyAliveNonEggMonsExcept(d[4])) d[7] = 1;
            else if (item && !AddBagItem(item, 1)) d[7] = 3;
            else
            {
                ZeroMonData(&source);
                GlassWriteSlot(d[3], d[5], d[4], &source);
                CompactPartySlots();
                CalculatePlayerPartyCount();
                d[6] = FALSE;
            }
            d[9] = 0;
        }
        else return;
        DrawGlassStorage(taskId);
        return;
    }
    if (d[9] == 1)
    {
        if (JOY_NEW(B_BUTTON)) d[9] = FALSE;
        else if (JOY_NEW(DPAD_UP) && d[10]) d[10]--;
        else if (JOY_NEW(DPAD_DOWN) && GlassBagItem(d[10] + 1)) d[10]++;
        else if (JOY_NEW(A_BUTTON))
        {
            u16 item = GlassBagItem(d[10]);
            if (item != ITEM_NONE && RemoveBagItem(item, 1))
            {
                if (party) SetMonData(&gPlayerParty[slot], MON_DATA_HELD_ITEM, &item);
                else SetBoxMonData(&gPokemonStoragePtr->boxes[d[0]][slot], MON_DATA_HELD_ITEM, &item);
                d[7] = 5;
            }
            d[9] = FALSE;
        }
        else return;
        DrawGlassStorage(taskId);
        return;
    }
    if (JOY_NEW(B_BUTTON))
    {
        if (d[6]) d[6] = 0;
        else
        {
            DestroyGlassStorageIcons();
            gPokemonStoragePtr->currentBox = d[0];
            SetPokeGlassBlend(TRUE);
            CloseHub();
            d[2] = d[3] = 0;
            gTasks[taskId].func = Task_CloseTablet;
            return;
        }
    }
    else if (JOY_NEW(A_BUTTON))
    {
        GlassReadSlot(party, d[0], slot, &target);
        d[7] = 0;
        if (!d[6])
        {
            if (!GetMonData(&target, MON_DATA_SANITY_HAS_SPECIES)) return;
            d[3] = party; d[4] = slot; d[5] = d[0]; d[6] = TRUE;
        }
        else if (!(party && slot > gPlayerPartyCount))
        {
            GlassReadSlot(d[3], d[5], d[4], &source);
            if (party != d[3])
            {
                struct Pokemon *leaving = party ? &target : &source;
                struct Pokemon *entering = party ? &source : &target;
                u8 partySlot = party ? slot : d[4];
                if (ItemIsMail(GetMonData(leaving, MON_DATA_HELD_ITEM))) d[7] = 2;
                else if (CountPartyAliveNonEggMonsExcept(partySlot) == 0
                    && (!GetMonData(entering, MON_DATA_SANITY_HAS_SPECIES) || GetMonData(entering, MON_DATA_IS_EGG)
                        || (OW_PC_HEAL > GEN_7 && !GetMonData(entering, MON_DATA_HP)))) d[7] = 1;
                if (!d[7] && OW_PC_HEAL <= GEN_7 && GetMonData(entering, MON_DATA_SANITY_HAS_SPECIES))
                    HealPokemon(entering);
            }
            if (!d[7])
            {
                GlassWriteSlot(d[3], d[5], d[4], &target);
                GlassWriteSlot(party, d[0], slot, &source);
                CompactPartySlots();
                CalculatePlayerPartyCount();
                d[6] = FALSE;
            }
        }
    }
    else if (JOY_NEW(SELECT_BUTTON) && d[6]) d[9] = 2;
    else if (JOY_NEW(SELECT_BUTTON))
    {
        u16 item, none = ITEM_NONE;
        GlassReadSlot(party, d[0], slot, &target);
        item = GetMonData(&target, MON_DATA_HELD_ITEM);
        d[7] = 0;
        if (!GetMonData(&target, MON_DATA_SANITY_HAS_SPECIES)) return;
        if (ItemIsMail(item)) d[7] = 2;
        else if (item != ITEM_NONE)
        {
            if (!AddBagItem(item, 1)) d[7] = 3;
            else
            {
                if (party) SetMonData(&gPlayerParty[slot], MON_DATA_HELD_ITEM, &none);
                else SetBoxMonData(&gPokemonStoragePtr->boxes[d[0]][slot], MON_DATA_HELD_ITEM, &none);
                d[7] = 4;
            }
        }
        else if (!GetMonData(&target, MON_DATA_IS_EGG) && GlassBagItem(0))
        {
            d[9] = TRUE;
            d[10] = 0;
        }
    }
    else if (JOY_NEW(L_BUTTON | R_BUTTON))
        d[0] = (d[0] + (JOY_NEW(L_BUTTON) ? TOTAL_BOXES_COUNT - 1 : 1)) % TOTAL_BOXES_COUNT;
    else if (JOY_NEW(START_BUTTON))
    {
        GlassReadSlot(party, d[0], slot, &target);
        if (!GetMonData(&target, MON_DATA_SANITY_HAS_SPECIES)) return;
        d[9] = 3;
    }
    else if (JOY_NEW(DPAD_UP))
        d[2] = party ? (d[2] + 4) % PARTY_SIZE : PARTY_SIZE + (slot + 24) % IN_BOX_COUNT;
    else if (JOY_NEW(DPAD_DOWN))
        d[2] = party ? (d[2] + 2) % PARTY_SIZE : PARTY_SIZE + (slot + 6) % IN_BOX_COUNT;
    else if (JOY_NEW(DPAD_LEFT))
        d[2] = party ? (d[2] % 2 ? d[2] - 1 : PARTY_SIZE + d[2] / 2 * 12 + 5)
            : (slot % 6 ? d[2] - 1 : min(slot / 6 / 2, 2) * 2 + 1);
    else if (JOY_NEW(DPAD_RIGHT))
        d[2] = party ? (d[2] % 2 ? PARTY_SIZE + d[2] / 2 * 12 : d[2] + 1)
            : (slot % 6 < 5 ? d[2] + 1 : min(slot / 6 / 2, 2) * 2);
    else return;
    PlaySE(SE_SELECT);
    DrawGlassStorage(taskId);
}

static void OpenGlassStorage(void)
{
    u8 taskId;
    if (!OpenTabletWindow()) return;
    sGlassStorageIcons = AllocZeroed(sizeof(*sGlassStorageIcons));
    if (sGlassStorageIcons == NULL) { ScriptContext_Enable(); return; }
    memset(sGlassStorageIcons->ids, MAX_SPRITES, sizeof(sGlassStorageIcons->ids));
    taskId = CreateTask(Task_PokeGlassStorage, 80);
    if (taskId == TASK_NONE)
    {
        DestroyGlassStorageIcons();
        CloseHub();
        RestoreTabletAppearance();
        ScriptContext_Enable();
        return;
    }
    gTasks[taskId].data[0] = gPokemonStoragePtr->currentBox < TOTAL_BOXES_COUNT ? gPokemonStoragePtr->currentBox : 0;
    DrawGlassStorage(taskId);
}
