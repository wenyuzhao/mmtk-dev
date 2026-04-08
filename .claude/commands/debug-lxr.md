# TLDR

Under current branches, run `uv run mmtk-jdk r --gc LXR -n 5 --heap 400M --bench pmd --no-weak-refs --no-class-unloading -b` will crash (see below for crash info).

But adding the following to `mmtk-openjdk/mmtk/Cargo.toml` will make it run successfully:

```toml
[profile.dev]
panic = "abort"
```

Fix this bug.

# The output of the correct run

```
===== DaCapo 23.11-chopin pmd starting warmup 1 =====
PMD checked 601 files.
===== DaCapo 23.11-chopin pmd completed warmup 1 in 20925 msec =====
===== DaCapo 23.11-chopin pmd starting warmup 2 =====
PMD checked 601 files.
===== DaCapo 23.11-chopin pmd completed warmup 2 in 11567 msec =====
===== DaCapo 23.11-chopin pmd starting warmup 3 =====
PMD checked 601 files.
===== DaCapo 23.11-chopin pmd completed warmup 3 in 11345 msec =====
===== DaCapo 23.11-chopin pmd starting warmup 4 =====
PMD checked 601 files.
===== DaCapo 23.11-chopin pmd completed warmup 4 in 11674 msec =====
===== DaCapo 23.11-chopin pmd starting =====
PMD checked 601 files.
============================ MMTk Statistics Totals ============================
GC      time.other      time.stw
48      6149.71 6179.71
Total time: 12329.42 ms
------------------------------ End MMTk Statistics -----------------------------
===== DaCapo 23.11-chopin pmd PASSED in 12329 msec =====
```

# The output of the failed run

```
===== DaCapo 23.11-chopin pmd starting warmup 1 =====
PMD checked 601 files.
Digest validation failed for pmd-report.txt, expecting 0x9ac4266f6d867118bf6365f3c935b97526705c2c found 0x9f2ab2e2e08d1ba4df32cff305cd81c9c753e50f
===== DaCapo 23.11-chopin pmd FAILED warmup =====
===== DaCapo 23.11-chopin pmd starting warmup 2 =====
PMD checked 601 files.
Digest validation failed for pmd-report.txt, expecting 0x9ac4266f6d867118bf6365f3c935b97526705c2c found 0x3ba253515b33bda2ca7d67aaa73c0f078ae1147a
===== DaCapo 23.11-chopin pmd FAILED warmup =====
===== DaCapo 23.11-chopin pmd starting warmup 3 =====
PMD checked 601 files.
Digest validation failed for pmd-report.txt, expecting 0x9ac4266f6d867118bf6365f3c935b97526705c2c found 0x3ba253515b33bda2ca7d67aaa73c0f078ae1147a
===== DaCapo 23.11-chopin pmd FAILED warmup =====
===== DaCapo 23.11-chopin pmd starting warmup 4 =====
PMD checked 601 files.
Digest validation failed for pmd-report.txt, expecting 0x9ac4266f6d867118bf6365f3c935b97526705c2c found 0xe3f43479eb1af29de589d8346ca6f95e90b2d15f
===== DaCapo 23.11-chopin pmd FAILED warmup =====
===== DaCapo 23.11-chopin pmd starting =====
PMD checked 601 files.
============================ MMTk Statistics Totals ============================
GC      time.other      time.stw
44      5614.69 6086.80
Total time: 11701.49 ms
------------------------------ End MMTk Statistics -----------------------------
Digest validation failed for pmd-report.txt, expecting 0x9ac4266f6d867118bf6365f3c935b97526705c2c found 0xb267a9f6b8d3ce4af93555b16e66ac0b5cfc54a7
===== DaCapo 23.11-chopin pmd FAILED =====
Validation FAILED for pmd default
```

The failure is related to failed Digest validation, not a panic/segfault.

# pmd output file for digest validations

After running pmd, the file for digest validations is at `mmtk-dev/scratch/pmd-report.txt`.

I've copied the files for the above two runs to `mmtk-dev/pmd-report-ok.txt` and `mmtk-dev/pmd-report-err.txt`.

The difference between the two file is at L1898

```diff
- src/main/java/net/sourceforge/pmd/cache/CachedRuleViolation.java:22:	DataClass:	The class 'CachedRuleViolation' is suspected to be a Data Class (WOC=16.667%, NOPA=0, NOAM=10, WMC=17)
+ src/main/java/net/sourceforge/pmd/cache/CachedRuleViolation.java:22:	DataClass:	The class 'CachedRuleViolation' is suspected to be a Data Class (WOC=0.000%, NOPA=0, NOAM=10, WMC=17)
```

# Note

* the current LXR implementation does not support weak refs and class unloading, always pass `--no-weak-refs --no-class-unloading` to disable them.
* The dacapo version: https://github.com/dacapobench/dacapobench/tree/v23.11-chopin
