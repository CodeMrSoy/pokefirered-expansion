Havora_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Havora_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Havora_PokemonCenter_1F_OnTransition::
	goto_if_unset FLAG_QUANTUM_ARRIVED, Havora_PokemonCenter_1F_End
	setflag FLAG_QUANTUM_PORT_CENTER
	setrespawn HEAL_LOCATION_QUANTUM_PORT_CITY
Havora_PokemonCenter_1F_End::
	end

Havora_PokemonCenter_1F_Nurse::
	lock
	faceplayer
	call EventScript_PkmnCenterNurse
	release
	end
