
<!-- some hacks to hide the table of contents and make the links sidebar smaller, 
so the table has more screen real estate -->
<style>
.md-sidebar--secondary:not([hidden]){
  display: none 
}

.md-sidebar {
    width: 8rem
}

.md-typeset table td:first-child,
.md-typeset table th:first-child {
  max-width: 180px;
}

.md-typeset table td:last-child,
.md-typeset table th:last-child {
  min-width: 100px;
}

</style>

# ACCESS-ESM1.6 Experiments

The below lists published experiments, on Gadi, available for analysis and as the start point for perturbation experiments.

This data, and the configurations they are based on, are licensed by 
[CC-by-4.0](https://creativecommons.org/licenses/by/4.0/) and therefore can be freely shared, 
distributed and modified. Guidelines for acknoledgement are in [Conditions of Use](https://github.com/accESS-NRI/access-esm1.6-configs/#conditions-of-use).

Data in these experiments is in the models native format and meets the [ACCESS Data Output Specification](https://access-output-data-specifications.readthedocs.io). For data meeting the CMIP7 specification, please 
use an ESGF node.

Experiments can be found in the access-nri-intake catalog by their experiment name. ## IS THIS TRUE ?

| Experiment | Release Configuration | Description | Length (years) | Output Path |
| ---- | ---- | ---- | ---- | ---- | 
| [piControl-2026.04.07](https://github.com/ACCESS-NRI/access-esm1.6-experiments/tree/piControl-2026.04.07) | [release-piControl-1.1](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/release-piControl-1.1) | Pre-industrial control experiment forced by CO2 concentrations | 173 years             | `/g/data/jq44/access-nri/access-esm1p6/global/piControl/2026.04.07/` |
| [piControl-2026.04.22](https://github.com/ACCESS-NRI/access-esm1.6-experiments/tree/piControl-2026.04.22) | [release-piControl-1.1](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/release-piControl-1.1) | Pre-industrial control experiment forced by CO2 concentrations (follows *piControl-2026.04.07* ) | 856 years             | `/g/data/jq44/access-nri/access-esm1p6/global/piControl/2026.04.22/` |
| [esm-piControl-2026.04.14](https://github.com/ACCESS-NRI/access-esm1.6-experiments/tree/piControl-2026.04.14) | [release-esm-piControl-1.1](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/release-esm-piControl-1.1) | Pre-industrial control experiment forced by CO2 emissions | 1117 years             | `/g/data/jq44/access-nri/access-esm1p6/global/esm-piControl/2026.04.14/` |