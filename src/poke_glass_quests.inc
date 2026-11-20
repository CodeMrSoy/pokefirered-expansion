// Shared field overlay: the launcher and NPC offers use the same window owner.
static EWRAM_DATA u8 sQuestIds[QUEST_DEFINITION_COUNT];
static EWRAM_DATA u8 sQuestCount, sQuestCursor, sQuestFilter, sQuestDetail, sQuestTextPage, sQuestTextPages;
static EWRAM_DATA bool8 sQuestOfferNpc, sQuestOfferNo;
static EWRAM_DATA u8 sQuestOfferId;
static EWRAM_DATA bool8 sQuestRewardBlocked;
static void Task_GlassQuestBook(u8 taskId);
static void Task_GlassQuestOffer(u8 taskId);

static void QuestUiCommit(void)
{
    // Keep the map visible without competing with dense quest text.
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(15, 2));
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}
static void QuestUiClose(u8 taskId)
{
    SetPokeGlassBlend(TRUE);
    CloseHub();
    gTasks[taskId].data[2] = 0;
    gTasks[taskId].data[3] = FALSE;
    gTasks[taskId].data[4] = FALSE;
    gTasks[taskId].func = Task_CloseTablet;
}
static void QuestUiList(void)
{
    u8 id;
    sQuestCount = 0;
    for (id = 0; id < QUEST_DEFINITION_COUNT; id++)
    {
        const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
        u8 state = QuestBook_GetState(id);
        if (!QuestBook_IsVisible(id)) continue;
        if (sQuestFilter == 1 && q->optional) continue;
        if (sQuestFilter == 2 && !q->optional) continue;
        if (sQuestFilter == 3 && state != QUEST_COMPLETED && state != QUEST_CLAIMED) continue;
        sQuestIds[sQuestCount++] = id;
    }
    if (sQuestCursor >= sQuestCount) sQuestCursor = 0;
}
static const u8 *QuestStatus(u8 state)
{
    static const u8 names[][10] = {_("UNKNOWN"), _("AVAILABLE"), _("ACTIVE"), _("COMPLETE"), _("CLAIMED"), _("DECLINED"), _("FAILED")};
    return names[state <= QUEST_FAILED ? state : 0];
}
static void QuestRewardText(u16 id, u8 *text)
{
    const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
    u8 *end;
    if (!q->rewardQuantity) { StringCopy(text, COMPOUND_STRING("No extra reward. Story rewards are given by their original NPCs.")); return; }
    end = StringCopy(text, GetItemName(q->rewardItem));
    end = StringAppend(end, COMPOUND_STRING(" x"));
    ConvertIntToDecimalStringN(end, q->rewardQuantity, STR_CONV_MODE_LEFT_ALIGN, 2);
    if (QuestBook_GetState(id) == QUEST_CLAIMED) StringAppend(text, COMPOUND_STRING("\nAlready claimed."));
}
static void DrawGlassQuestBook(void)
{
    static const u8 filters[4][5] = {_("ALL"), _("MAIN"), _("SIDE"), _("DONE")};
    u8 row, first = sQuestCursor >= 5 ? sQuestCursor - 4 : 0;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    HubRect(4, 12, 12, 216, 136);
    HubRect(6, 12, 42, 96, 91); HubRect(4, 13, 43, 94, 89);
    HubRect(6, 112, 42, 116, 91); HubRect(4, 113, 43, 114, 89);
    StatsText(16, 13, COMPOUND_STRING("QUEST BOOK"));
    StatsText(166, 13, filters[sQuestFilter]);
    if (!QuestBook_IsReady())
    {
        PokeGlassPrintTextPage(sHubWindow, 16, 45, 204, 6, 0, COMPOUND_STRING("Quest data is unavailable. Existing reserved save data was left untouched."));
        StatsText(16, 136, COMPOUND_STRING("B: Back")); QuestUiCommit(); return;
    }
    if (!sQuestCount)
    {
        StatsText(16, 28, COMPOUND_STRING("No quests in this category."));
        PokeGlassPrintTextPage(sHubWindow, 17, 60, 84, 5, 0, COMPOUND_STRING("Explore and speak with people to discover quests."));
    }
    for (row = first; row < sQuestCount && row < first + 5; row++)
    {
        u8 id = sQuestIds[row], y = 59 + (row - first) * 14, state = QuestBook_GetState(id);
        const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
        if (row == sQuestCursor) HubRect(5, 14, y, 92, 13);
        HubRect(state == QUEST_COMPLETED || state == QUEST_CLAIMED ? 8 : 6, 16, y + 4, 3, 5);
        if (QuestBook_GetTracked() == id) HubRect(10, 16, y + 4, 3, 5);
        StatsTextFit(22, y, 82, q->title);
    }
    StatsText(17, 44, filters[sQuestFilter]);
    sQuestTextPages = 1;
    if (sQuestCount)
    {
        u8 id = sQuestIds[sQuestCursor], state = QuestBook_GetState(id);
        const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
        const u8 *body;
        u8 reward[160], heading[32];
        StatsTextFit(16, 28, 208, q->title);
        if (sQuestDetail >= q->objectiveCount + 3) sQuestDetail = 0;
        if (sQuestDetail < q->objectiveCount)
        {
            u8 *end = StringCopy(heading, COMPOUND_STRING("OBJECTIVE "));
            end = ConvertIntToDecimalStringN(end, sQuestDetail + 1, STR_CONV_MODE_LEFT_ALIGN, 1);
            *end++ = CHAR_SLASH; ConvertIntToDecimalStringN(end, q->objectiveCount, STR_CONV_MODE_LEFT_ALIGN, 1);
            body = q->objectives[sQuestDetail];
            if (QuestBook_GetCompletedObjectives(id) & (1 << sQuestDetail)) HubRect(8, 217, 46, 5, 5);
        }
        else if (sQuestDetail == q->objectiveCount) { StringCopy(heading, COMPOUND_STRING("STORY")); body = q->description; }
        else if (sQuestDetail == q->objectiveCount + 1) { StringCopy(heading, COMPOUND_STRING("LOCATION")); body = q->location; }
        else { StringCopy(heading, COMPOUND_STRING("REWARDS")); QuestRewardText(id, reward); body = reward; }
        StatsTextFit(116, 44, 98, heading);
        sQuestTextPages = PokeGlassPrintTextPage(sHubWindow, 116, 59, 108, 4, sQuestTextPage, body);
        StatsText(116, 119, COMPOUND_STRING("<>: Info"));
        if (sQuestTextPages > 1) HubRect(8, 220, 128, 4, 2);
        if (sQuestRewardBlocked) StatsText(16, 136, COMPOUND_STRING("Bag full. Collect your reward later."));
        else if (state == QUEST_ACTIVE) StatsText(16, 136, COMPOUND_STRING("A: Track  SELECT: Filter  B: Back"));
        else if (state == QUEST_COMPLETED) StatsText(16, 136, q->optional ? COMPOUND_STRING("A: Claim  SELECT: Filter  B: Back") : COMPOUND_STRING("A: Archive  SELECT: Filter  B: Back"));
        else if (state == QUEST_AVAILABLE || state == QUEST_DECLINED) StatsText(16, 136, COMPOUND_STRING("A: Offer  SELECT: Filter  B: Back"));
        else StatsText(16, 136, COMPOUND_STRING("LEFT/RIGHT: Info   B: Back"));
        StatsTextFit(49, 44, 55, QuestStatus(state));
    }
    else StatsText(16, 136, COMPOUND_STRING("SELECT: Filter  B: Back"));
    QuestUiCommit();
}
static void DrawGlassQuestOffer(void)
{
    const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(sQuestOfferId);
    u8 state = QuestBook_GetState(sQuestOfferId), objective = QuestBook_GetObjective(sQuestOfferId);
    u8 rewards[160];
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    HubRect(4, 12, 12, 216, 136);
    HubRect(5, 14, 14, 212, 17);
    StatsTextFit(18, 15, 204, q->title);
    StatsText(18, 34, QuestStatus(state));
    PokeGlassPrintTextPage(sHubWindow, 18, 50, 202, 3, 0,
        objective < q->objectiveCount ? q->objectives[objective] : COMPOUND_STRING("All objectives complete. Thank you for your field work!"));
    StatsText(18, 92, COMPOUND_STRING("REWARDS"));
    QuestRewardText(sQuestOfferId, rewards);
    PokeGlassPrintTextPage(sHubWindow, 18, 105, 202, 2, 0, rewards);
    if (sQuestRewardBlocked) StatsText(18, 135, COMPOUND_STRING("Bag full. Please return later."));
    else if (state == QUEST_AVAILABLE || state == QUEST_DECLINED)
        StatsText(18, 135, sQuestOfferNo ? COMPOUND_STRING("Accept    > Decline    A: Confirm") : COMPOUND_STRING("> Accept    Decline    A: Confirm"));
    else StatsText(18, 135, state == QUEST_COMPLETED ? COMPOUND_STRING("A: Claim reward    B: Later") : COMPOUND_STRING("A/B: Return"));
    QuestUiCommit();
}
static void QuestUiReturnFromOffer(u8 taskId)
{
    if (sQuestOfferNpc) QuestUiClose(taskId);
    else { QuestUiList(); sQuestTextPage = 0; DrawGlassQuestBook(); gTasks[taskId].func = Task_GlassQuestBook; }
}
static void Task_GlassQuestOffer(u8 taskId)
{
    u8 state;
    if (gPaletteFade.active) return;
    state = QuestBook_GetState(sQuestOfferId);
    if (JOY_NEW(DPAD_UP | DPAD_DOWN | DPAD_LEFT | DPAD_RIGHT) && (state == QUEST_AVAILABLE || state == QUEST_DECLINED))
    { sQuestOfferNo ^= 1; PlaySE(SE_SELECT); DrawGlassQuestOffer(); }
    if (JOY_NEW(B_BUTTON))
    {
        if (state == QUEST_AVAILABLE || state == QUEST_DECLINED) QuestBook_Decline(sQuestOfferId);
        QuestUiReturnFromOffer(taskId);
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        if (state == QUEST_AVAILABLE || state == QUEST_DECLINED)
        {
            if (sQuestOfferNo) QuestBook_Decline(sQuestOfferId);
            else QuestBook_Accept(sQuestOfferId);
        }
        else if (state == QUEST_COMPLETED && !QuestBook_ClaimReward(sQuestOfferId))
        { sQuestRewardBlocked = TRUE; DrawGlassQuestOffer(); return; }
        QuestUiReturnFromOffer(taskId);
    }
}
static void Task_GlassQuestBook(u8 taskId)
{
    u8 old = sQuestCursor;
    if (gPaletteFade.active) return;
    if (JOY_NEW(B_BUTTON)) { QuestUiClose(taskId); return; }
    if (JOY_NEW(SELECT_BUTTON))
    {
        sQuestRewardBlocked = FALSE;
        sQuestFilter = (sQuestFilter + 1) % 4; sQuestCursor = 0; QuestUiList(); sQuestDetail = sQuestTextPage = 0;
    }
    else if (sQuestCount && JOY_REPEAT(DPAD_UP)) sQuestCursor = sQuestCursor ? sQuestCursor - 1 : sQuestCount - 1;
    else if (sQuestCount && JOY_REPEAT(DPAD_DOWN)) sQuestCursor = (sQuestCursor + 1) % sQuestCount;
    else if (sQuestCount && JOY_NEW(DPAD_RIGHT))
    {
        if (++sQuestTextPage >= sQuestTextPages) { sQuestTextPage = 0; sQuestDetail++; }
    }
    else if (sQuestCount && JOY_NEW(DPAD_LEFT))
    {
        if (sQuestTextPage) sQuestTextPage--;
        else { const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(sQuestIds[sQuestCursor]); sQuestDetail = sQuestDetail ? sQuestDetail - 1 : q->objectiveCount + 2; }
    }
    else if (sQuestCount && JOY_NEW(A_BUTTON))
    {
        u8 id = sQuestIds[sQuestCursor], state = QuestBook_GetState(id);
        if (state == QUEST_AVAILABLE || state == QUEST_DECLINED)
        {
            sQuestOfferId = id; sQuestOfferNpc = sQuestOfferNo = FALSE;
            DrawGlassQuestOffer(); gTasks[taskId].func = Task_GlassQuestOffer; return;
        }
        if (state == QUEST_ACTIVE) QuestBook_Track(QuestBook_GetTracked() == id ? QUEST_NONE : id);
        else if (state == QUEST_COMPLETED) sQuestRewardBlocked = !QuestBook_ClaimReward(id);
    }
    else return;
    PlaySE(SE_SELECT);
    if (old != sQuestCursor)
    {
        sQuestRewardBlocked = FALSE;
        u8 id = sQuestIds[sQuestCursor], objective = QuestBook_GetObjective(id);
        const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
        sQuestDetail = objective < q->objectiveCount ? objective : 0; sQuestTextPage = 0;
    }
    DrawGlassQuestBook();
}
static void ShowGlassQuestBook(void)
{
    u8 task;
    QuestBook_Load(); QuestBook_Update();
    if (!OpenTabletWindow()) return;
    QuestUiList(); sQuestDetail = sQuestTextPage = 0; sQuestRewardBlocked = FALSE;
    DrawGlassQuestBook();
    task = CreateTask(Task_GlassQuestBook, 80);
    if (task == TASK_NONE) { CloseHub(); ScriptContext_Enable(); }
}
bool8 QuestBook_OfferFromScript(struct ScriptContext *ctx)
{
    u8 task;
    u16 id = gSpecialVar_0x8004;
    const struct QuantumQuestDefinition *q;
    Script_RequestEffects(SCREFF_V1 | SCREFF_SAVE | SCREFF_HARDWARE);
    gSpecialVar_Result = FALSE;
    QuestBook_Load();
    q = QuestBook_GetDefinition(id);
    if (!q || !q->optional || !QuestBook_Discover(id)) return FALSE;
    QuestBook_NotifyNpc(id);
    HideFieldMessageBox();
    if (!OpenTabletWindow()) return FALSE;
    sQuestOfferId = id; sQuestOfferNpc = TRUE; sQuestOfferNo = sQuestRewardBlocked = FALSE;
    DrawGlassQuestOffer();
    task = CreateTask(Task_GlassQuestOffer, 80);
    if (task == TASK_NONE) { CloseHub(); RestoreTabletAppearance(); ScriptContext_Enable(); return FALSE; }
    gSpecialVar_Result = TRUE;
    return TRUE;
}
