QuantumHavoraNorthQuay_MapScripts::
	.byte 0

QuantumHavoraNorthQuay_Guide::
	msgbox QuantumHavoraNorthQuay_Guide_Text, MSGBOX_NPC
	end

QuantumHavoraNorthQuay_Guide_Text::
	.string "This is HAVORA's market district!\nHomes north, shops and harbor south.$"

QuantumHavoraNorthQuay_Resident::
	msgbox QuantumHavoraNorthQuay_Resident_Text, MSGBOX_NPC
	end

QuantumHavoraNorthQuay_Resident_Text::
	.string "The flower beds soften all this stone.\nI love living near the waterfront.$"

QuantumHavoraNorthQuay_Harbor::
	msgbox QuantumHavoraNorthQuay_Harbor_Text, MSGBOX_NPC
	end

QuantumHavoraNorthQuay_Harbor_Text::
	.string "The ferry pier is just south of here.\nYou can walk straight to the harbor.$"

QuantumHavoraNorthQuay_Fisher::
	msgbox QuantumHavoraNorthQuay_Fisher_Text, MSGBOX_NPC
	end

QuantumHavoraNorthQuay_Fisher_Text::
	.string "Fresh fish arrive with the morning tide.\nThe market never stays quiet for long.$"

QuantumHavoraNorthQuay_Supplies::
	lock
	faceplayer
	message Text_MayIHelpYou
	waitmessage
	pokemart QuantumHavoraNorthQuay_Stock
	msgbox Text_PleaseComeAgain
	release
	end

	.align 2
QuantumHavoraNorthQuay_Stock::
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_NONE
