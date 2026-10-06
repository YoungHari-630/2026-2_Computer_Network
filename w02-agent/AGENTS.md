# Week 2 HTTP and QUIC Analysis Rules

These rules apply whenever an agent collects, analyzes, or verifies the documents for this assignment.

## Source identity and date

1. Open every local file used in the analysis during the current run. A filename or `source-list.md` entry is not proof of the document's identity.
2. For an RFC, copy the RFC number, title, and date only from that RFC's own header.
3. For a paper or design document, use the title page or the document's own metadata. Record a year only when the opened document explicitly identifies its publication date.
4. A date in a protocol history, cited reference, repository path, or linked document is not the publication date of the current document. If the current document gives no publication date, write `not stated (unverified)`; do not infer a year.

## Claim evidence

5. Every `problem solved`, `key mechanism`, and `what it gave up` entry must include an exact evidence location from the same opened source: an RFC section, document heading, or PDF page and section.
6. A `what it gave up` or trade-off entry is allowed only when the source explicitly states the limitation, cost, restriction, fallback, or exchange. Do not fill a missing trade-off from general networking knowledge or from another linked document.
7. If no direct trade-off evidence exists in that source, write `unsupported — no explicit trade-off stated in this source`. This is preferable to a plausible inference.
8. Do not silently turn an absence of evidence into a positive claim. Preserve `not stated`, `unverified`, and `unsupported` in the output wherever they apply.
9. Do not cite an RFC number, DOI, measured value, section, or page that was not opened and checked in the current run.

## Checks the agent cannot perform

10. If the lecture slides are not present in the workspace, write `Manual check required` for lecture contradictions. Do not guess what the lecture said.
11. Do not pre-fill the student's hand-verification result or error count in `verification-2.md`. The agent's source check and the student's independent check are separate steps.

## Required self-check before completion

Before claiming the analysis is complete, the agent must:

1. List the files in `materials/` and confirm that `source-list.md` has one entry for every file.
2. Confirm that the analysis has exactly one row per source and exactly these columns: identifier, year, problem solved, key mechanism, and what it gave up.
3. Reopen every RFC header and verify its number, title, and date.
4. Reopen every non-RFC title page or document header and verify its identifier and any claimed year.
5. For every mechanism and trade-off claim, locate the cited section, heading, or PDF page in the same source.
6. Search the completed table for claims without evidence locations; either add direct evidence or mark the claim `unsupported`.
7. Confirm that unavailable lecture comparisons remain `Manual check required` and report any item still requiring human verification.

