## Wrong number of prognostic fields in init dump

Tilo suggested to run this command:

```
module load python2
python ~access/apps/pythonlib/umfile_utils/um_fields_subset.py -x 95,171,172,173,174,176,177,178,179,180,181,184,185,186,187,188,189,192,250,413,414,415,416,33001,33002 -i restart_dump.astart -o restart_dump.astart2
```

so I did.

## Wrong day

Ran this command:

```
module load python2
~access/data/ACCESS_CMIP5/utils/change_dump_date.py restart_dump.astart <<< "1 1 1"
```

Which is also copied from the AM-09.init script. 

Still errors, setting `MODEL_BASIS_TIME` to 1/1/1978, see if that helps.

ran the above change to `restart_dump.astart` again with 1978 1 1.

This seems to have done the trick, the model is running now.

Scott also recommended historical's warm-start scripts, need to look into that.

But for now it's working.

## Model running, but I think the data is off

Restarting with 'corrected' historical files

## Changing start dump

Holger, you can try to run the payu version with the following restart file:



/scratch/p66/txz599/archive/AM-09-t1/restart/atm/AM-09-t1.astart-19780101



This restart file has already the correct number of expected prognostic fields, so no further processing required.

Not identical, try again with non-corrected


## Tilo's directories
/g/data/p66/txz599/ACCESS-ESM1p5/exp/AM-09-t1
/scratch/p66/txz599/archive/AM-09-t1/


## My own ksh run was successful. 
/scratch/w35/hxw599/exp/AM-09
The final absolute Norm is:
```
  Final Absolute Norm :   9.476114947009368E-003
  Final Absolute Norm :   9.263593553513758E-003
  Final Absolute Norm :   8.666711488850787E-003
  Final Absolute Norm :   8.694108134046526E-003
  Final Absolute Norm :   9.565927145833091E-003
  Final Absolute Norm :   8.337744422816816E-003
  Final Absolute Norm :   9.181470990641743E-003
  Final Absolute Norm :   7.638193879830560E-003
  Final Absolute Norm :   8.416312129883008E-003
  Final Absolute Norm :   8.060406845402416E-003
```

## Trace Gasses

Tilo's script modifies the MMR of various trace gasses every year. I don't think this should have any effect, because `l_clmchfcg` is set to True, so it should take the values out of the arrays. But still, I'll try it.

At the moment, the year is hardcoded in the script, so that needs to change before it can run if that is an issue...

