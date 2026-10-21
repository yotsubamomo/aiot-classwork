# 50_Startups.csv — provenance

The teacher's example dataset for the HW2 bonus (+1, the second problem of the dashboard's problem
drop-down; Brief V2 §2, §6; Spec V2 「50 Startups 內建資料」). It is bundled so that the 50 Startups
problem works offline from `file://` and inside the submission ZIP. This file is outside the
dashboard's static scan (only `.html`, `.css` and `.js` are scanned), so the source URL may be
written here (DA `derivation-SPEC-V2.md` I-2).

| Item | Value |
| --- | --- |
| Source URL (given by the teacher, SRC-4 / Brief V2 §2) | https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv |
| Source repository | `Avik-Jain/100-Days-Of-ML-Code`, path `datasets/50_Startups.csv` |
| Repository license | MIT (GitHub API `repos/Avik-Jain/100-Days-Of-ML-Code/license`: `spdx_id` `MIT`, `LICENSE` blob `005423138e7fa4fb18de5ab6533da00a09961731`); notice reproduced in `50_Startups.LICENSE.md` |
| Last commit touching the file | `5cd8936afb3aab9e7029ce21413cb32766153a74` (2018-07-10T05:20:42Z) |
| Branch head at retrieval | `master` @ `5d67810c1498082e7bb262cf6397d7861dfd9891` |
| Git blob of the file | `14ffb8609375f6d18079f92b721b3c0793b46439` (equal to `git hash-object --no-filters` of the bundled copy) |
| Retrieved | 2026-10-22 01:17:32 +08:00 (HTTP `date` 2026-10-21 17:17:32 GMT), `curl` GET, HTTP 200, `content-length` 2436, `access-control-allow-origin: *` |
| Bytes | 2,436; UTF-8 (ASCII only), no BOM; CRLF line ends; no line end after the last row |
| sha256 | `c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d` |
| Shape | header + 50 rows, 5 columns: `R&D Spend`, `Administration`, `Marketing Spend`, `State`, `Profit` |

- `50_Startups.csv` is the byte-for-byte copy (no conversion; `.gitattributes` pins `assets/data/**`
  as `-text`). `startups50.js` embeds the same text as a JS global (`window.HW2_STARTUPS50`) because
  a page opened from `file://` cannot read a local file with a network API; `tests/test_explore_static.py`
  checks that the embedded text, this file's sha256 and the `.csv` bytes are the same.
- The data goes through the same load contract and Exploratory run engine as a user dataset; it has
  no special path. It does not claim to meet the assignment's >13-feature condition (Brief V2 §4).
