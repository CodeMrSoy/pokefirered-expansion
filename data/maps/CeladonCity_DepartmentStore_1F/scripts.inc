CeladonCity_DepartmentStore_1F_MapScripts::
	.byte 0

CeladonCity_DepartmentStore_1F_EventScript_Receptionist::
	goto_if_classic CeladonCity_DepartmentStore_ClassicReceptionist
	msgbox CeladonCity_DepartmentStore_1F_Text_WelcomeToDeptStore, MSGBOX_NPC
	end

CeladonCity_DepartmentStore_1F_EventScript_LayoutSign::
	msgbox CeladonCity_DepartmentStore_1F_Text_FloorDescriptions, MSGBOX_SIGN
	end

CeladonCity_DepartmentStore_1F_EventScript_FloorSign::
	msgbox CeladonCity_DepartmentStore_1F_Text_ServiceCounter, MSGBOX_SIGN
	end

HavoraDepartment_CounterTutor::
	goto EventScript_CounterTutor
	end

CeladonCity_DepartmentStore_ClassicReceptionist::
	msgbox CeladonCity_DepartmentStore_ClassicWelcome, MSGBOX_NPC
	end

CeladonCity_DepartmentStore_ClassicWelcome::
	.string "Welcome to CELADON DEPT. STORE!\p"
	.string "Our floors offer POKé BALLS,\n"
	.string "evolution items and much more!$"
