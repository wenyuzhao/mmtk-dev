## Overview

This repo contains scripts used for running java workloads in a methodologically
sound setting.

### Assumptions

The system assumes one or more _running_ machines and an _analysis_ machine.
The scripts within this repo consider just the _running_ machine.   Other tools
(such as plotty) need to be used on the _analysis_ machine.

### Presumed directory structure

The scripts presume that analysis and running machines have a similar directory
structure.

For example, when using JikesRVM, for a paper `gc-pldi-2019`, the following
directory structure might be used on the analysis machines:

```
results/gc-pldi-2019/running <this repo>
results/gc-pldi-2019/running/build/<rvm builds here>
results/gc-pldi-2019/probes <probes repo>
results/gc-pldi-2019/advice <rvm advice repo>
```
