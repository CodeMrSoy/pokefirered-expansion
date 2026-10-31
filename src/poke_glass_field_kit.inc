static void UseGlassFieldTool(u16 item);

static void DrawGlassFieldKit(u8 taskId)
{
    s16 *d = gTasks[taskId].data;
    u8 i, owned = 0;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(14, 4));
    StatsText(16, 14, COMPOUND_STRING("FIELD KIT"));
    for (i = 0; i < 7; i++)
    {
        bool8 collected = FieldTool_IsOwned(i);
        if (collected) owned++;
        HubRect(i == d[0] ? 5 : 4, 84, 31 + i * 12, 140, 12);
        StatsText(88, 31 + i * 12, GetItemName(FieldTool_GetItem(i)));
        StatsText(211, 31 + i * 12, collected ? COMPOUND_STRING("+") : COMPOUND_STRING("-"));
    }
    StatsNumber(204, 14, owned);
    StatsText(205, 14, COMPOUND_STRING("/7"));
    StatsText(16, 122, d[2] ? COMPOUND_STRING("Tool or GYM BADGE required.")
        : FieldTool_IsOwned(d[0]) ? COMPOUND_STRING("Ready for your next expedition.")
        : COMPOUND_STRING("Find this tool on your journey."));
    StatsText(16, 136, COMPOUND_STRING("A:Use  Up/Down:Tool  B:Back"));
    if (d[3] < MAX_SPRITES) DestroySpriteAndFreeResources(&gSprites[d[3]]);
    d[3] = FieldTool_CreateLargeSprite(FieldTool_GetItem(d[0]), 0xD133, 46, 72);
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static void Task_PokeGlassFieldKit(u8 taskId)
{
    s16 *d = gTasks[taskId].data;
    if (gPaletteFade.active) return;
    if (d[1] < 2) { d[1]++; return; }
    if (JOY_NEW(B_BUTTON))
    {
        if (d[3] < MAX_SPRITES) DestroySpriteAndFreeResources(&gSprites[d[3]]);
        SetPokeGlassBlend(TRUE);
        CloseHub();
        d[2] = d[3] = 0;
        gTasks[taskId].func = Task_CloseTablet;
    }
    else if (JOY_NEW(A_BUTTON))
    {
        if (!FieldTool_IsOwned(d[0]) || !FieldMove_IsUnlocked(d[0]))
        { d[2] = TRUE; DrawGlassFieldKit(taskId); }
        else
        {
            u16 item = FieldTool_GetItem(d[0]);
            if (d[3] < MAX_SPRITES) DestroySpriteAndFreeResources(&gSprites[d[3]]);
            DestroyTask(taskId);
            UseGlassFieldTool(item);
        }
    }
    else if (JOY_REPEAT(DPAD_UP | DPAD_DOWN))
    {
        d[0] = (d[0] + (JOY_REPEAT(DPAD_UP) ? 6 : 1)) % 7;
        d[2] = FALSE;
        DrawGlassFieldKit(taskId);
    }
}

static void ShowGlassFieldKit(void)
{
    u8 taskId;
    FieldTools_MigrateInventory();
    if (!OpenTabletWindow()) return;
    taskId = CreateTask(Task_PokeGlassFieldKit, 80);
    if (taskId == TASK_NONE) { ScriptContext_Enable(); return; }
    gTasks[taskId].data[3] = MAX_SPRITES;
    DrawGlassFieldKit(taskId);
}
