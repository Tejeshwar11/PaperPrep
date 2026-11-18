NETWORK SECURITY RESEARCH PACKAGE — VERSION 0.2
Regenerated 16 November 2026; model checks executed 14 November 2026

Status: verified finite-model case study; submission metadata and contribution
positioning remain open. This package is not a novelty certificate, acceptance
prediction or evidence of a vendor vulnerability. Supervisor approval to proceed
was reported by the user; final approval of this revised version is not assumed.

START HERE
1. Read Network_Security_Research_Draft.pdf.
2. Read SUBMISSION_READINESS.txt and NOVELTY_AND_VENUES.txt.
3. Reproduce the model checks below and inspect the counterexample logs.
4. Complete AUTHOR_DETAILS.txt and choose the venue before final formatting.

CONTENTS
- Network_Security_Research_Draft.pdf: manuscript in the previous paper's layout.
- editable_source/manuscript.tex: editable neutral LaTeX manuscript; not a
  journal-specific template. figure-1.pdf and figure-2.pdf are vector figures.
- extended_model.py: complete Python finite-state enumerator.
- FirewallEpochs.tla: corresponding TLA+ specification.
- *_count.cfg: full state enumeration configurations.
- *_e7_safety.cfg: safety/invariant configurations at bound seven.
- evidence/: actual checker outputs and cross-check summaries.
- pilot/: original Boolean model and actual results.
- SOURCE_MANIFEST.json: SHA-256 checksums of the packaged scientific files.
- AUTHOR_DETAILS.txt: required factual information to complete.
- COVER_LETTER_DRAFT.txt: unfinished cover letter; not sent.

REPRODUCE PYTHON
Requires Python 3.10+ and no third-party modules. From this directory run:
  python3 extended_model.py > reproduced_python_results.json
Compare to evidence/python_results.json. The code asserts the expected safe and
unsafe outcomes and the generation-order invariant for the protected design.

REPRODUCE TLC
Download the tool from the official TLA+ project:
https://github.com/tlaplus/tlaplus/releases/download/v1.8.0/tla2tools.jar
Observed build: TLC2 Version 2026.11.06.222357 (rev: d8fb231).
Observed SHA-256:
e1f11b75c4b5bc4478ba0ac5cb6ae28e40a01b0016bc33e0aa97da22dfdbcd7f
The URL alone does not pin bytes; check the hash and report any mismatch.
This run used OpenJDK 21.0.13, one TLC worker and a 512 MB heap.
  python3 run_tlc.py /absolute/path/to/tla2tools.jar
The runner writes configurations/logs and checks all 25 distinct-state counts
against the Python output. It also checks five safety outcomes at epoch bound
seven. It intentionally expects counterexamples for four weakened variants.
A nonzero TLC outcome for an intentionally unsafe variant is not a test failure.

EVIDENCE SUMMARY
Epoch bounds 1,2,3,5,7; five designs at each bound. All distinct-state counts match
across Python and TLC. The largest bound represents four deny changes and three
reauthorizations after the initial permit. At that bound:
E0 local acknowledgement: 6446 states; 160 violating states.
E1 volatile receipt: 2372 states; 30 violating states.
E2 regressive policy: 1379 states; 20 violating states.
E3 session bypass: 776 states; 20 violating states.
E4 protected: 383 states; zero violating states.
Violation totals are from complete Python enumeration. TLC safety runs stop at
the first counterexample; their state totals are not the enumeration totals.
Raw TLC-generated counts differ from Python edge counts; only distinct states
are compared. These are not attack probabilities or performance statistics.

BOUNDARIES
One mutable target; other traffic is only an implicit unaffected control.
Updates are serialized. There is one primary crash and at most one atomic
backup restart; no repeated restart, split brain or lost durable storage.
Messages are authentic and can replay old issued generations. Receipt delivery
is idealized; there is no network authentication implementation. No liveness,
traffic-speed, device-performance, or universal deployment guarantee is claimed.
The manual order argument is not a machine-checked unbounded proof. Both model
encodings were created in the same workflow; matching them does not constitute
independent human replication. No collected dataset or training data are used.

EDITABLE MANUSCRIPT
Compile manuscript.tex from its directory using a complete LaTeX installation.
It includes standard article/geometry, Times fonts, amsmath/amssymb, graphicx,
longtable/booktabs/array and hyperref packages. The neutral source is for editing
and later conversion into the selected venue's official template. The review PDF
retains the supervisor-approved visual format; the venue may require another.

AI ASSISTANCE AND RESPONSIBILITY
AI assistance covered model formulation, code/specification generation, analysis,
writing and formatting; it was not limited to proofreading. Disclosure wording
must reflect the actual work and selected venue policy. Human authors must read,
understand, validate and accept responsibility for every submission claim.

SOURCE VALIDATION LIMITATION
The review PDF was generated and visually verified. The neutral LaTeX source
was exported but could not be compiled in this environment: the local TeX
installation lacks its format files and the alternate engine bundle download
returned HTTP 403. It must be compiled and checked before any source submission.
The mathematical definitions in the PDF are the reviewed version.
