# PaperPrep

Research code v0.2: acknowledged revocation across stateful firewall failover.

The current review PDF is in `paper/`. The ZIP in `archive/` and README.txt are the earlier 16 November package, including raw logs and pilot files; their manuscript and metadata are historical. No PowerPoint file was supplied.

## Reproduce
Requires Python 3.10+ (standard library only). Run `python3 extended_model.py > reproduced_python_results.json`. Compare with `evidence/python_results.json`.

For TLC, use Java (recorded run: OpenJDK 21.0.13) and the official tla2tools.jar. Follow README.txt for the exact recorded hash, download URL and `python3 run_tlc.py /path/to/tla2tools.jar`. The runner creates configurations and logs; evidence/ must exist. Recorded runs used one worker and a 512 MB heap.

## Software metadata
1. Code version: v0.2 (package label; no release tag).
2. Repository: https://github.com/Tejeshwar11/PaperPrep ; cite the exact commit for a version-specific link.
3. Reproducible capsule: not yet available. Repository is private; public Binder deployment not configured or tested.
4. Code license: Apache-2.0; see LICENSE. Third-party tools retain their own licenses.
5. Versioning: Git, hosted on GitHub.
6. Languages/tools: Python, TLA+, TLC, Java/OpenJDK, JSON.
7. Requirements: Python 3.10+, Java and TLC JAR; no Python third-party dependencies; no Python compilation step. Checks recorded on Linux.
8. Manual: this README and README.txt.
9. Support: tejesh9606@gmail.com

## Research status
Finite-model case study, not a vendor implementation, performance benchmark or established new security mechanism. The two model encodings share assumptions and authorship workflow. All author details and final declarations remain subject to author review. AI assistance included model/code generation and manuscript writing. No external traffic dataset is required. Novelty work is deferred for supervisor feedback.
