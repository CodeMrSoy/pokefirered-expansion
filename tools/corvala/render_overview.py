"""Render both tide previews with outdoor residents at event coordinates."""
from PIL import Image
from build_cove import R,read

people={'OLD_MAN_1':('old_man_1','pink',32),'WOMAN_2':('woman_2','white',32),
        'FISHER':('fisher','white',32),'LITTLE_GIRL':('little_girl','pink',16),
        'WOMAN_1':('woman_1','green',32),'BOY':('boy','green',32)}
events=read(R/'data/maps/Corvala_Town/map.json')['object_events']
for phase in ['low','high']:
    im=Image.open(R/f'docs/corvala/{phase}-tide-playable.png').convert('RGBA')
    for ev in sorted(events,key=lambda e:e['y']):
        gfx=ev['graphics_id'].removeprefix('OBJ_EVENT_GFX_')
        if gfx.startswith('SPECIES('):
            species=gfx[8:-1].lower();path=R/f'graphics/pokemon/{species}/overworld.png'
            pal=R/f'graphics/pokemon/{species}/overworld_normal.pal';w=h=32
        else:
            name,color,h=people[gfx];w=16
            path=R/f'graphics/object_events/pics/people/{name}.png'
            pal=R/f'graphics/object_events/palettes/npc_{color}.pal'
        sprite=Image.open(path).crop((0,0,w,h))
        sprite.putpalette(sum([list(map(int,s.split())) for s in pal.read_text().splitlines()[3:19]],[]))
        mask=Image.frombytes('L',(w,h),bytes(255 if v else 0 for v in sprite.tobytes()))
        im.paste(sprite.convert('RGBA'),(ev['x']*16+8-w//2,ev['y']*16+16-h),mask)
    im.convert('RGB').save(R/f'docs/corvala/{phase}-tide-residents.png')
