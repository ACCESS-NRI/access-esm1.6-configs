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
