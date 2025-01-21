#!/g/data/vk83/apps/payu/1.1.5/bin/python
# Copyright 2020 Scott Wales
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Expects land use dataset and restart file as arguments.

import mule
import xarray
import os
import shutil
import sys
import tempfile

class ReplaceOp(mule.DataOperator):
    def __init__(self, da):
        self.da = da

    def new_field(self, source):
        return source

    def transform(self, source, result):
        # Use the pseudo level (lbuser5) to select appropriate vegtype
        return self.da.isel(vegtype = source.lbuser5 - 1).data

landuse = xarray.open_dataset(sys.argv[1]).fraction
restart = sys.argv[2]

stash_landfrac = 216
stash_landfrac_lastyear = 835

mf = mule.DumpFile.from_file(restart)

year = mf.fixed_length_header.t2_year
# Expect to be updating once per year so should have month=1 and day=1
month = mf.fixed_length_header.t2_month
day = mf.fixed_length_header.t2_day
if month != 1 or day != 1:
    raise ValueError(f"Unexpected month, day in update_landuse.py {month} {day}")

print(f'Updating land use for year {year}')

out = mf.copy()
out.validate = lambda *args, **kwargs: True

set_current_landuse = ReplaceOp(landuse.sel(time=f'{year:04d}-01-01'))
set_previous_landuse = ReplaceOp(landuse.sel(time=f'{year-1:04d}-01-01'))

for f in mf.fields:
    if f.lbuser4 == stash_landfrac:
        f = set_current_landuse(f)

    if f.lbuser4 == stash_landfrac_lastyear:
        f = set_previous_landuse(f)

    out.fields.append(f)

temp = tempfile.NamedTemporaryFile()
out.to_file(temp.name)

shutil.copy(temp.name, restart)
