"""Compare local GGUF candidates with identical Pallet dialogue and decision prompts."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from inference import windows_launcher_environment
from worker import ResidentWorker

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("runtime", type=Path)
parser.add_argument("models", type=Path, nargs="+")
args = parser.parse_args()

grammar=r'''root ::= line "\n" line
line ::= [A-Z] [A-Za-z0-9 ,'?-]{3,25} [.!?]
'''
decision='root ::= "SAY_DIALOGUE" | "REMEMBER_EVENT" | "ADJUST_RELATIONSHIP" | "PROPOSE_OPTIONAL_QUEST"'
def chat(system,user):
 return f'<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n'
system="You are Watts, the friendly Pallet Town PC repairman. Practical, gently joking. You love Electric Pokemon. Write TWO short NPC sentences, each 4 to 7 words. Each line must be a complete spoken sentence. Roleplay only."
cases=[
 ('pikachu',grammar,system,"The player shows you Pikachu for the first time. Pikachu's cheeks can spark. Warn it about your PC."),
 ('squirtle',grammar,system,"The player shows you Squirtle for the first time. It has a sturdy shell. Mention the pond nearby."),
 ('return',grammar,system,"The player shows you the same Pikachu again. You remember it from a previous visit. Say that you remember it."),
 ('quiet',decision,"You are Watts. Choose one action. Only propose a quest if you remember meeting the player's Pikachu and they show it again. If the player shows an unfamiliar Pokemon, remember it. Otherwise choose SAY_DIALOGUE.", "No Pokemon is visible. You have no memory of this player."),
 ('visit',decision,"You are Watts. Choose one action. Only propose a quest if you remember meeting the player's Pikachu and they show it again. If the player shows an unfamiliar Pokemon, remember it. Otherwise choose SAY_DIALOGUE.", "The player shows you Pikachu and you remember it from a previous visit. You want to meet a Squirtle.")
]
for path in args.models:
 name = path.name
 w=ResidentWorker(args.runtime,windows_launcher_environment,timeout=40,model=path)
 try:
  w.start()
  pid=w.process.pid
  for idx,g,s,u in cases:
   out,metrics=w.generate(g,chat(s,u))
   print(name,idx,repr(out),metrics,flush=True)
  status = Path(f'/proc/{pid}/status')
  memory = [line for line in status.read_text().splitlines() if line.startswith(('VmRSS:', 'VmHWM:'))] if status.is_file() else []
  print(name, path.stat().st_size, memory, flush=True)
 finally: w.close()
