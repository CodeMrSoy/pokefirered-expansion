#include "global.h"
#include "gflib.h"
#include "item.h"
#include "poke_glass.h"
#include "constants/items.h"

// Bag-only summaries retain item effects. Field tools and other
// inventory contexts keep their original descriptions. Stable IDs are audited
// against the compiled item table rather than an independently copied list.
static const u8 *BagDescription(u16 item)
{
    static const u8 lens[] = _("Boosts Sp. Atk EVs; lowers Speed.");
    static const u8 band[] = _("Boosts Sp. Def EVs; lowers Speed.");
    static const u8 glass[] = _("Tablet: Pokédex, Storage, maps and stats.");
    static const u8 back[] = _("Return to PokéGlass.");
    switch (item)
    {
    case ITEM_POWER_LENS: return lens;
    case ITEM_POWER_BAND: return band;
    case ITEM_POKEGLASS: return glass;
    case ITEMS_COUNT: return back;
    }
    return GetItemDescription(item);
}

u16 PokeGlassPrintBagDescription(u8 window, u16 item, u16 page)
{
    const u8 *source = BagDescription(item);
    u8 text[512], font = FONT_SMALL;
    u16 i, length = 0, pages;
    // Original descriptions contain hard line breaks for the old wide list.
    // Reflow their complete text to this panel instead of preserving those breaks.
    for (i = 0; source[i] != EOS && length < sizeof(text) - 1; i++)
    {
        u8 c = source[i] == CHAR_NEWLINE ? CHAR_SPACE : source[i];
        if (c == CHAR_SPACE && (!length || text[length - 1] == CHAR_SPACE)) continue;
        text[length++] = c;
    }
    text[length] = EOS;
    pages = PokeGlassPrintTextPageWithFont(WINDOW_NONE, 2, 0, 84, 3, 0, text, font);
    if (pages > 1)
    {
        font = FONT_SMALL_NARROW;
        pages = PokeGlassPrintTextPageWithFont(WINDOW_NONE, 2, 0, 84, 3, 0, text, font);
    }
    if (pages > 1) font = FONT_SMALL_NARROWER;
    // Keep a safe paging fallback for future, unaudited items; every current
    // item shown in this grid fits page zero without truncation or ellipses.
    return PokeGlassPrintTextPageWithFont(window, 2, 0, 84, 3, page, text, font);
}
