#include "global.h"
#include "gflib.h"
#include "menu.h"
#include "string_util.h"
#include "poke_glass.h"

// Word-wrapped pages share the actual small-font metrics across native apps.
// The caller owns clearing its panel. Never print beyond the requested rows.
u16 PokeGlassPrintTextPageWithFont(u8 window, u16 x, u16 y, u16 width, u16 rows, u16 page, const u8 *text, u8 font)
{
    static const u8 colors[] = {0, 8, 4};
    u8 clean[512], line[256];
    u16 start = 0, row = 0;
    if (!rows || !width) return 0;
    {
        u32 i;
        for (i = 0; i < sizeof(clean) - 1 && text[i] != EOS; i++) clean[i] = text[i];
        clean[i] = EOS;
    }
    clean[sizeof(clean) - 1] = EOS;
    StripExtCtrlCodes(clean);
    while (clean[start] != EOS)
    {
        u16 count = 0, split = 0;
        while (clean[start + count] != EOS && clean[start + count] != CHAR_NEWLINE && count < sizeof(line) - 2)
        {
            line[count] = clean[start + count];
            line[count + 1] = EOS;
            if (GetStringWidth(font, line, 0) > width) break;
            if (line[count] == CHAR_SPACE) split = count;
            count++;
        }
        if (clean[start + count] != EOS && clean[start + count] != CHAR_NEWLINE && split) count = split;
        if (!count) count = 1;
        memcpy(line, clean + start, count);
        line[count] = EOS;
        FitPokeGlassText(line, font, width);
        if (window != WINDOW_NONE && row / rows == page)
            AddTextPrinterParameterized3(window, font, x, y + (row % rows) * 13, colors, TEXT_SKIP_DRAW, line);
        start += count;
        while (clean[start] == CHAR_SPACE || clean[start] == CHAR_NEWLINE) start++;
        row++;
    }
    return max(1, (row + rows - 1) / rows);
}

u16 PokeGlassPrintTextPage(u8 window, u16 x, u16 y, u16 width, u16 rows, u16 page, const u8 *text)
{
    return PokeGlassPrintTextPageWithFont(window, x, y, width, rows, page, text, FONT_SMALL);
}
