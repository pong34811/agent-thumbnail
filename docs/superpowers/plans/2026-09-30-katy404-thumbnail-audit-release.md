# KATY404 Portfolio Audit Skill v1.0.2 — Follow-up Plan

## Goal
Finish the portfolio-wide review workflow in `katy404-canva-thumbnails`, resolve the quality-review finding, then publish the completed skill changes. Do not release until both skill copies pass independent spec and quality reviews.

## Current state
- A first pass reviewed five final delivery sets using manifests and landscape/portrait review sheets: Aomi (16 files), Tygarina (12), Armigon (32), KT404 (24), and timeline-covers (24), totaling 108 files / 54 orientation pairs.
- Review-sheet analysis found recurring themes: secondary text sometimes competes with the hook; backgrounds can obscure gameplay evidence; avatars may dominate the scene or repeat poses; portrait gaps and edge margins vary; landscape text can sit low near the scrubber.
- The review was portfolio-level, not a full-resolution visual check of every one of the 108 images. Do not describe it as exhaustive native-resolution QC.
- Both `skills/katy404-canva-thumbnails/SKILL.md` and `.agents/skills/katy404-canva-thumbnails/SKILL.md` currently contain uncommitted v1.0.2 edits and are byte-identical.
- Spec review passed. Quality review identified one important gap: the workflow trusts a manifest without explicitly reconciling that manifest with the user's requested scope or checking whether the manifest is stale/incomplete.
- The manifest-scope fix was started but stopped at the user's request. It is not yet verified, committed, pushed, or released.
- Other working-tree changes (`.gitignore`, `IDEA.md`, `AGENTS.md`, `.work/`, `outputs/`, and existing docs) are outside this task and must remain untouched.

## Tasks

1. **Reconcile audit scope before trusting manifests**
   - Compare the requested project/channel and timeline set with manifest entries, current timeline inventory when available, and the relevant output folder.
   - If the manifest is missing, stale, or disagrees with the requested scope, use current project evidence or ask the user to resolve ambiguous final versions.
   - Record unresolved items and do not claim a complete audit until the scope and expected count are reconciled.

2. **Complete portfolio audit instructions**
   - Keep final exports distinct from drafts, alternate versions, crop tests, source frames, and contact-sheet annotations.
   - Count expected landscape and portrait deliverables separately and verify output names/dimensions against the reconciled inventory.
   - Use contact sheets to find cross-set patterns, then inspect individual finals at native and small preview sizes when available; report any coverage limits.
   - Ground findings in filenames and recurrence counts where possible. Do not infer CTR from appearance or views.

3. **Maintain conditional design guidance**
   - Keep gameplay recognizable; prefer local darkening/gradient masks over whole-frame blur.
   - Keep the hook dominant, secondary text clearly subordinate, and portrait spacing/margins intentional.
   - Ensure avatar size and expression support the moment without obscuring the gameplay/story evidence.
   - Use circles/arrows only when they point to supported evidence; never require them on every cover.

4. **Verify and review**
   - Keep the two SKILL.md copies byte-identical at version 1.0.2.
   - Check frontmatter/version, portfolio-scope gate, and `git diff --check`.
   - Run independent spec-compliance review first, then quality review. Fix and re-review any blocking issue.

5. **Publish only scoped files**
   - Stage and commit only the two skill files for the skill release; do not include the plan or unrelated workspace changes unless separately requested.
   - Push `main`, create/push tag `v1.0.2`, create the GitHub Release, then verify the remote commit, tag, and release URL.

## Completion criteria

- Manifest/requested-scope reconciliation is explicit and prevents false completeness claims.
- Both skill copies are identical, verified, and approved by both review stages.
- The release commit contains only the two skill copies; unrelated local changes remain untouched.
- The remote branch, `v1.0.2` tag, and GitHub Release are verified after publication.
