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

static void DrawGlassStorage(u8 taskId)
{
    s16 *d = gTasks[taskId].data;
    u8 row, side, text[32];
    struct Pokemon mon;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    // Quiet the scenery behind dense management text without another buffer.
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(14, 4));
    HubRect(4, 10, 10, 220, 140);
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
            StatsText(22, 32 + row * 11, text);
        }
        StatsText(18, 113, COMPOUND_STRING("A:Give  B:Cancel"));
        goto copy;
    }
    StatsText(16, 14, COMPOUND_STRING("PARTY"));
    StatsText(128, 14, gPokemonStoragePtr->boxNames[d[0]]);
    StatsNumber(211, 14, d[0] + 1);
    StatsText(212, 14, COMPOUND_STRING("/6"));
    for (side = 0; side < 2; side++)
        for (row = 0; row < PARTY_SIZE; row++)
        {
            u8 index = side ? d[1] * PARTY_SIZE + row : row;
            u8 x = side ? 128 : 16, y = 28 + row * 14;
            bool8 selected = d[2] == side * PARTY_SIZE + row;
            bool8 source = d[6] && d[3] == !side && d[4] == index && (d[3] || d[5] == d[0]);
            HubRect(selected ? 5 : 4, x - 2, y, side ? 100 : 108, 14);
            GlassReadSlot(!side, d[0], index, &mon);
            if (GetMonData(&mon, MON_DATA_SANITY_HAS_SPECIES))
            {
                GetMonData(&mon, MON_DATA_NICKNAME, text);
                StringGet_Nickname(text);
            }
            else StringCopy(text, COMPOUND_STRING("-"));
            StatsText(x + 7, y, text);
            if (source) StatsText(x, y, COMPOUND_STRING(">"));
        }
    HubRect(6, 12, 111, 216, 1);
    StatsText(18, 112, COMPOUND_STRING("Page"));
    StatsNumber(52, 112, d[1] + 1);
    StatsText(53, 112, COMPOUND_STRING("/5"));
    StatsNumber(186, 112, CountMonsInBox(d[0]));
    StatsText(187, 112, COMPOUND_STRING("/30"));
    if (d[7] == 1)
        StatsText(16, 124, COMPOUND_STRING("Keep one able POKéMON."));
    else if (d[7] == 2)
        StatsText(16, 124, COMPOUND_STRING("Remove MAIL first."));
    else if (d[7] == 3)
        StatsText(16, 124, COMPOUND_STRING("BAG full. Item unchanged."));
    else if (d[7] == 4)
        StatsText(16, 124, COMPOUND_STRING("Item moved to BAG."));
    else if (d[7] == 5)
        StatsText(16, 124, COMPOUND_STRING("Held item given."));
    else if (d[7] == 6)
        StatsText(16, 124, COMPOUND_STRING("Eggs cannot be released."));
    else if (d[6])
        StatsText(16, 124, COMPOUND_STRING("A:Place SELECT:Release B:Cancel"));
    else
        StatsText(16, 124, COMPOUND_STRING("A:Move  SELECT:Held item"));
    StatsText(16, 136, COMPOUND_STRING("L/R:Box START:Page B:Back"));
copy:
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
    slot = party ? d[2] : d[1] * PARTY_SIZE + d[2] - PARTY_SIZE;
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
    else if (JOY_NEW(START_BUTTON)) d[1] = (d[1] + 1) % 5;
    else if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT)) d[2] = (d[2] + PARTY_SIZE) % (PARTY_SIZE * 2);
    else if (JOY_NEW(DPAD_UP)) d[2] = d[2] % PARTY_SIZE ? d[2] - 1 : d[2] + PARTY_SIZE - 1;
    else if (JOY_NEW(DPAD_DOWN)) d[2] = d[2] % PARTY_SIZE < PARTY_SIZE - 1 ? d[2] + 1 : d[2] - PARTY_SIZE + 1;
    else return;
    PlaySE(SE_SELECT);
    DrawGlassStorage(taskId);
}

static void OpenGlassStorage(void)
{
    u8 taskId;
    if (!OpenTabletWindow()) return;
    taskId = CreateTask(Task_PokeGlassStorage, 80);
    if (taskId == TASK_NONE)
    {
        CloseHub();
        RestoreTabletAppearance();
        ScriptContext_Enable();
        return;
    }
    gTasks[taskId].data[0] = gPokemonStoragePtr->currentBox < TOTAL_BOXES_COUNT ? gPokemonStoragePtr->currentBox : 0;
    DrawGlassStorage(taskId);
}
