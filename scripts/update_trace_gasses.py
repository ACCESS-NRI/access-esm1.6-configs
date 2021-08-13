#!/usr/bin/env python3
import f90nml
import os

year="1978"

with open("work/INPUT/trgas_rcp_historical_ESM.dat", 'r') as tr_file:
    while True:
        line = tr_file.readline()
        if line.startswith(year):
            break


print(line)


(y, CO2_MMR, CH4MMR, N2OMMR, C11MMR, C12MMR, C113MMR, HCFC22MMR, HFC125MMR, HFC134AMMR) = (
    float(v) for v in line.split())

print(CO2_MMR, CH4MMR, N2OMMR, C11MMR, C12MMR, C113MMR, HCFC22MMR, HFC125MMR, HFC134AMMR)

nmls = f90nml.read('work/namelists')
nmls['run_radiation']['co2_mmr'] = CO2_MMR
nmls['run_radiation']['ch4mmr'] = CH4MMR
nmls['run_radiation']['n2ommr'] = N2OMMR
nmls['run_radiation']['c11mmr'] = C11MMR
nmls['run_radiation']['c12mmr'] = C12MMR
nmls['run_radiation']['c113mmr'] = C113MMR
nmls['run_radiation']['hcfc22mmr'] = HCFC22MMR
nmls['run_radiation']['hfc125mmr'] = HFC125MMR
nmls['run_radiation']['hfc134ammr'] = HFC134AMMR
os.system('rm work/namelists')
nmls.write('work/namelists')
