"""Install Corvala's authored residents, dialogue and reef encounter tables."""
import argparse,copy
from build_cove import R,read,write,words

DOCKS=[
 ('HarborGuide','OLD_MAN_1',44,17,'The tide turns every hour.\\nEven hours are low tide.\\pOdd hours bring high tide.\\nThe docks stay above the water.'),
 ('ReefWatcher','WOMAN_2',28,27,'Wild POKéMON hide in the sand.\\nWatch your step near the reef!\\pThe wooden docks are a safe\\nplace to rest your team.'),
 ('NetMender','FISHER',21,31,'I mend nets while the tide is low.\\nWhen it rises, I go fishing.\\pThe sea keeps its own schedule.\\nI just try to keep up!'),
 ('ShellCollector','LITTLE_GIRL',16,35,'I found a shell that whistles!\\nListen...\\pOh. That was the wind.'),
 ('CoralKeeper','WOMAN_1',48,25,'These reefs are alive.\\nPlease leave the coral here.\\pTake a memory home instead!'),
 ('TideLookout','BOY',38,40,'High tide covers the sand and\\nthe lower cliff below the GYM.\\pVisit the GYM when the tide is\\nlow. I wait here on the docks!'),
 ('DockCorsola','SPECIES(CORSOLA)',23,31,r'CORSOLA: Cor! Corsola!\nIt basks in the salty breeze.\pThe fisher keeps an eye on it\nwhile mending the nets.'),
 ('DockMareanie','SPECIES(MAREANIE)',40,39,r'MAREANIE waves its tentacles.\nIt seems curious about you.\pThe coral keeper makes sure\nit leaves the reef alone.'),
 ('DockCorsolaHome','SPECIES(CORSOLA)',36,37,r'CORSOLA: Cor! Cor!\nIt is resting beside the hut.\pTiny flecks of sand sparkle\non its coral branches.'),
]
HOUSES=[
 'My grandfather drove the first\\npilings into this sand.\\pThe sea can come and go.\\nOur home stays right here.',
 'The tide changes on the hour.\\nCheck the clock before exploring.\\pHead back to the docks when\\nyou have finished on the reef.',
 'I keep drawings of every coral\\nI find. No two are alike!\\pSome POKéMON hide in the sand\\nbetween the coral heads.',
 'A loose knot can ruin a net.\\nA tight knot can save a catch.\\pMy apprentice says I tell that\\nstory every day. I probably do.',
 'Everyone arrives through that\\ncave. News travels with them.\\pStay awhile. The cove looks\\ndifferent when the tide turns.',
]

def main():
 town=read(R/'data/maps/Corvala_Town/map.json');bs=words(R/'data/layouts/Corvala_Town/map.bin')
 template=read(R/'data/maps/Corvala_House1/map.json')['object_events'][0]
 town['object_events']=[v for v in town['object_events'] if not v['script'].startswith('Corvala_Dock_')]
 text='Corvala_Town_MapScripts::\n\tmap_script MAP_SCRIPT_ON_LOAD, Corvala_Town_OnLoad\n\t.byte 0\n\nCorvala_Town_OnLoad::\n\tcallnative CorvalaTide_OnLoad\n\tend\n'
 for name,gfx,x,y,dialogue in DOCKS:
  assert not bs[y*64+x]&0xc00
  ev=copy.deepcopy(template);label='Corvala_Dock_'+name
  ev.update(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=bs[y*64+x]>>12,script=label)
  town['object_events'].append(ev)
  text+=f'\n{label}::\n\tmsgbox {label}_Text, MSGBOX_NPC\n\tend\n\n{label}_Text::\n\t.string "{dialogue}$"\n'
 write(R/'data/maps/Corvala_Town/map.json',town);write(R/'data/maps/Corvala_Town/scripts.inc',text)
 for i,dialogue in enumerate(HOUSES,1):
  name=f'Corvala_House{i}'
  write(R/f'data/maps/{name}/scripts.inc',f'{name}_MapScripts::\n\t.byte 0\n\n{name}_Resident::\n\tmsgbox {name}_Resident_Text, MSGBOX_NPC\n\tend\n\n{name}_Resident_Text::\n\t.string "{dialogue}$"\n')
 data=read(R/'src/data/wild_encounters.json');enc=data['wild_encounter_groups'][0]['encounters']
 enc[:]=[v for v in enc if v['map']!='MAP_CORVALA_TOWN']
 def table(rate,species,lo=18,hi=22):
  return {'encounter_rate':rate,'mons':[{'min_level':lo,'max_level':hi,'species':'SPECIES_'+s} for s in species]}
 enc.append({'map':'MAP_CORVALA_TOWN','base_label':'sCorvalaTown',
  'land_mons':table(12,['KRABBY','SANDYGAST','SANDSHREW','DWEBBLE','BINACLE','SHELLOS','KRABBY','CORSOLA','STARYU','MAREANIE','WIMPOD','PYUKUMUKU']),
  'water_mons':table(4,['TENTACOOL','HORSEA','WINGULL','CORSOLA','MANTYKE']),
  'fishing_mons':table(20,['MAGIKARP','KRABBY','KRABBY','HORSEA','STARYU','HORSEA','CORSOLA','STARYU','MAREANIE','KINGLER'])})
 write(R/'src/data/wild_encounters.json',data)
 print('Installed six dock residents, three friendly Pokemon, five house dialogues and Corvala sand/Surf/fishing encounters')

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
 if not args.write:ap.error('--write is required')
 main()
