#ifndef GUARD_HAVORA_PUZZLE_H
#define GUARD_HAVORA_PUZZLE_H

struct ObjectEvent;
void HavoraPuzzle_OnLoad(void);
void HavoraPuzzle_OnResume(void);
void HavoraPuzzle_ResetState(void);
bool8 HavoraPuzzle_TryResetShortcut(void);
bool8 HavoraPuzzle_CanPushBoulder(const struct ObjectEvent *, s16, s16);
bool8 HavoraPuzzle_CanEnterPit(const struct ObjectEvent *, s16, s16);
bool8 HavoraPuzzle_OnBoulderMoved(struct ObjectEvent *);
void HavoraPuzzle_RecordCut(u16, u8, u8);

#endif
