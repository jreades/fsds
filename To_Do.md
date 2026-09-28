# To Do — 2026/27

Tracks what needs doing, session by session, before and during teaching. Review scope for 2026-09-25: **weeks 1–5 in full**. Weeks 6–12 were only skimmed via their session pages.

## How to use this file

**Type**

- **[R]** Readings / learning outcomes: edits to `sessions/weekN.qmd`. No recording impact.
- **[V]** Video: the Reveal.js deck of a *pre-recorded* lecture changed, so the MP4 must be rebuilt with `flip`, and possibly some audio re-recorded.
- **[A]** Assessment / guidance: clarifications about assessments, expectations, or how to study.
- **[L]** Live-only deck (1.x, 2.6–2.8, 4.4, 4.5, 6.0, 10.2): not recorded, so it can be edited freely.

**Priority / effort**

- **P1**: wrong, or contradicts the assessment. Students will copy it or be misled. **P2**: poorly specified or confusing, or a high-value enhancement. **P3**: cosmetic.
- **S** ≈ under 15 min · **M** ≈ under 1 hr · **L** = over 1 hr, or needs recording.
- Within each week, items are ordered **P1 → P3**, and by effort (S first) within the same priority. Each week's items are due **before that week is taught** unless tagged *Summer*.

### Recording fields for [V] items

| Field | Meaning |
|---|---|
| Slide (seq) | Slide title, and its **Sequence** number in the cut table in `fsds-private/ffmpeg/lessons.md` |
| Change | One sentence on what changes on the slide |
| Audio | `none` = visual only, rebuild the PNGs · `re-record` = replace an existing segment · `new` = add a new segment |
| Script | What to change in `fsds-private/scripts/<talk>.md` |

### How `flip` handles changes

- `ffmpeg/project.toml` maps each talk to its audio track. The per-slide cut times are the markdown table under `## <track>` in `ffmpeg/lessons.md`. **Sequence = the PNG index** exported by decktape.
- **Visual-only fix:** re-export the deck and re-merge. The audio cuts don't change.
- **End slide (the cheap way to add a recap):** insert the new slide **straight after the last narrated slide and before *Additional Resources***.
  - Its PNG index is then *last narrated seq + 1*, so add one row with that sequence and the times of the narration you appended to the M4A.
  - *Additional Resources* and *Thank You* aren't in the cut tables (the outro replaces Thank You), so nothing else needs renumbering.
  - The suggested sequence numbers below assume this placement. Check them against the `_png` export.
- **Mid-deck insertion:** every later row's Sequence goes up by 1 (see 6.2).
- The title slide is replaced by `flip`'s generated intro, so title-slide metadata (e.g. `date-as-string`) is **web-only**.

### Suggested end-slide pattern (about 45–60 s of narration)

`## Recap & Next` containing:

- three bullets on what should stick;
- one retrieval question to answer without looking ("Without scrolling back: …");
- one line on where this shows up next (practical, next talk, assessment).

Where a lecture has an error in its *narration*, the end slide can also carry a short correction ("One clarification…"), so the segment doesn't need re-recording.

---

## Before term starts (this week)

> **Merge blocker:** `assessments/index.qmd` already includes the draft `_ai_policy.qmd`. Before merging to `master` and publishing, resolve every `[CHECK]` marker (D6). Check with `grep -n CHECK assessments/_ai_policy.qmd`, which should print nothing.

A checklist that pulls together the P1s below, each tagged with its week.

- [ ] **Decisions D1–D6** below (assessment structure and AI policy). D1–D5 are done but not committed. D6 is blocked on UCL guidance.
- [x] **[A] P1 M** Align 1.1, 4.5, `assessments/index.qmd`, `peer.qmd` and `group.qmd` once D1–D5 are decided (committed in 6460ea1).
- [x] **[L] P1 S** Replaced hard-coded `date-as-string` with `date: last-modified` + `date-format: "Do MMMM YYYY"` in `lectures/_metadata.yml`; `inc/title-slide.html` now prints `$date$` (uncommitted).
- [x] **[L] P1 S** Replace the stale `QRCode for CASA0013 Group Signup (25_26).png` in 4.4 and 4.5.
- [x] **[A] P1 S** Setup docs from Asana: Podman RAM (`podman machine init --cpus 4 --memory 8192`), the macOS `containers.conf` fix, and the rootful/`keep-id` permissions workaround (Week 1).
- [ ] **[R] P1 S** Week 2–4 session-page errors (see each week).
- [ ] **[V] P1** Visual-only rebuilds for **2.1, 2.2, 2.3** (Week 2 is taught first). Weeks 3–5 can follow in term.

## Decisions needed

- [x] **D1: Exam.** 1.1 and `_variables.yml` drop the Open-Book Exam (no `quiz-*` vars), but **4.5 still presents it** as Assessment #1 and references `assess.quiz-weight/date/time`, which are now undefined. *Assumed:* the exam is gone.
- [x] **D2: Peer evaluation, one part or two?** 1.1 gives one date (`peer1-date`). 4.5, `assessments/index.qmd` and `peer.qmd` give two (self on 23 Dec, peer on 12 Jan). Also, 4.5 says the self-evaluation is due "several days *before* the final submission", but `peer1-date` (23 Dec) is the day *after* `group-date` (22 Dec).
- [x] **D3: Group size.** `group.qmd` says "*no more* than four". 4.5 says a group of under four may be merged "to make a 'full strength' group of up to five".
- [x] **D4: Name of the written component.** It's "Briefing Document" (1.1), "Content" (4.5, `group.qmd`) and, previously, "Structured Report". Pick one and use it everywhere, including on Moodle.
- [x] **D5: In-class draft presentations.** 4.5 says groups present a draft answer "starting in Week 7". 4.4 says "the iterative process that begins in Week 6". Is this still happening with the briefing format? If so, which week?
- [ ] **D6: AI-use policy.** ⏸ **BLOCKED: waiting on guidance for text that complies with UCL's AI categories.** Draft in `assessments/_ai_policy.qmd` (not rendered until included). Resolve its `[CHECK]` markers, then include it in `index.qmd`. Links to `../assessments/index.qmd#use-of-ai` are already in 1.1 (slide + notes), 2.7 (callout) and 4.5 (Resources); uncommitted. Items that depend on it: `assessments/index.qmd` (the policy itself), then 1.1 notes (Week 1), 2.7 (Week 2) and 4.5 (Week 4), which should link to it. There is currently no single statement of the policy:
  - 1.1 notes: "It's how you will do your work. Unquestionably."
  - 2.7: using an LLM as co-author "is still considered plagiarism".
  - The `Group_Work.qmd` declaration permits declared use.
  - The 4.5 exam text also covers it.
  - Asana also has "Why we're not using AI in this course" and "Communicate why we don't include a Claude subscription".
  - Suggest one short policy on `assessments/index.qmd` (mapped to UCL's AI categories), with 1.1, 2.7 and 4.5 linking to it.

---

## Module-wide

- [x] **[L] P1 S** Deck dates now come from `last-modified` (see the "Before term starts" checklist).
- [ ] **[R] P2 M** Asana: *"tasks and assignments for each class [should be] clearly stated before the reading material"*. Add a short **"This week, before class"** checklist at the top of each `weekN.qmd` (watch X, read Y, do Z), rather than having it split between Readings, Pre-Recorded and Practical. Do weeks 1–5 now and the rest in term. **Done for weeks 1–12** (uncommitted). Reading week is deliberately left alone: its objectives and 'Past student performance…' list already serve as a checklist.
- [ ] **[R] P2 M** Learning objectives for weeks 2–4 aren't measurable ("An understanding of how none of this all that new"). Rewrite them with verbs (explain / use / choose / diagnose) that map onto that week's talks and practical. Suggestions under each week.
- [x] **[A] P3 S** Asana: signpost Code Camp to non-CASA students (Moodle and the module description).
- [x] **[A]** `sessions/index.qmd`: the reading Template instruction was removed (done on branch). No `weekN.qmd` references it either. Confirm that's intended.
- [x] **[A]** `sessions/index.qmd`: clarified practical group swaps (done on branch).
- [ ] *Summer* **[V] P3 L** Alt text is missing on many lecture images (e.g. the 5.4 book cover, 3.2 `Alice.png`, 3.4 `phd101212s.gif`). This is also on Asana. It's visual-only, but touches every deck.

---

## Week 1 — Setting Up

**Session page**

- [x] **[R] P3 S** Typos: "tools that you'll need to across" → "need across"; "negotating" → "negotiating".

**Live decks**

- [x] **[A] P1 M** 1.1 Getting Started: align the assessment list with D1–D5. Currently it lists the peer evaluation with one date, and the "Assessment logic" bullets are now on the slide rather than in the notes (confirm that's intended).
- [x] **[A] P1 S** 1.1 notes (The Challenges): rewrite "It's how you will do your work. Unquestionably." to match D6.
- [x] **[L] P1 S** 1.2 footnote typo: "disagree what what you are about say" → "disagree with what you are about to say".
- [x] **[L] P2 M** 1.2 has a large **uncommitted** rework (~370 lines). Review it and commit.
- [x] **[L]** 1.1, 1.2, 1.4: typo, wording and markup fixes (done on branch).

**Setup pages** (from Asana)

- [x] **[A] P1 S** Podman: set RAM/CPUs at `podman machine init` and document the macOS `containers.conf` change and the rootful/`--userns=keep-id:gid=20` permissions workaround.

## Week 2 — Foundations (Pt. 1)

**Session page**

- [ ] **[R] P1 S** Learning objective 2 is garbled ("An understanding of how none of this all that new"). Overview typo: "intelligen".
  - Suggested LOs: (1) use variables, types, operators, conditions, lists and loops to solve short problems; (2) read Python error messages to find syntax errors; (3) explain why current debates about data volume and computation have precedents (Burton, Donoho).
- [ ] **[R] P2 S** "Dykstra" → "Dijkstra" (twice, in Connections).
- [ ] **[R] P2 S** The practical's Connections list "Ensuring that you are set up with Git/GitHub", but Git is taught in Week 3 (3.4). Move it or reword.

**2.1 Python: the Basics (Part 1): [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Common Mistakes (16) | **P1** `x > = str(y)` is a SyntaxError → `x >= str(y)` | none | none |
| Danger, Will Robinson! (15) | **P1** Comment "x and z are now both set to 10" → "x and y" | none | none |
| …But Not All Words Are Allowed (7) | **P1** The keyword table is Python 2: `print` and `exec` are no longer keywords, and `True`, `False`, `None`, `nonlocal`, `async` and `await` are missing. Also, Python *will* complain (SyntaxError). Replace it with the `keyword.kwlist` output. | none (the narration doesn't list the words) | optional: "Python may let you do this" is true only for built-ins like `type` and `int`, which is what the script says. OK. |
| Using Strings to Output Information (11) | P3 "three ways output" → "three ways to output" | none | none |
| Strings Are Different (10) | P3 `HelloHello` → `'HelloHello'`. The two slides share a title; rename the second one "Comparing Strings" | none | none |
| Notes only | P3 "ininstance" → "isinstance" (the script is already correct); "As we'll see in Week 4" → Week 5 | none | none |

**2.2 Python: the Basics (Part 2): [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| For Example (4) | **P1** Missing `)` in `print("x is not less than y"` (this bug is unintentional, unlike the deliberate errors on later slides) | none | none |
| Conditions & Consequences (2/3) | P3 "you'll often needs" → "need" | none | none |

**2.3 Lists: [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Slicing & Dicing Lists (9) | **P1** Syntax given as `list[ <start_idx>, <end_idx> ]` → `list[<start_idx>:<end_idx>]` | none (the narration already says "colon") | none |
| Appending (21) | **P1** A stray leading space before the 2nd `append` would raise IndentationError | none | none |
| Test Yourself (26) | P3 "You will have seen the answer to this in Code Camp". Not everyone has, so add "(or see `not in`)" | none | none |
| Notes only | P3 "waht" | none | none |

**2.4 Iteration: [V], optional visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Step 1: The 'Outer Loop' (9) | P3 The output is shown with quotes (`'Rose'`) but `print` gives `Rose` (Step 2 is already correct). The commented-out `print(h)` has lost its indentation. | none | none |
| Step 2 (11), Recap (13) | P3 "We know change it" → "now"; "collection items" → "collection of items" | none | none |

**2.5 The Command Line: [V], end slide recommended**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| **New end slide (18)**, before Additional Resources | **P2** "Where you'll use this": the terminal *inside JupyterLab/Podman* is the same shell, and its file browser shows the same `pwd`/`ls` view (Asana item). `git` in Week 3 uses exactly these commands. Retrieval question: *what does `|` do, and what does `>` do?* | **new** (~45 s) | Add a `## Recap & Next` section after *Getting Help* |
| A (Complex) Example (16) | P2 A `docker … conda env export` example, but the module now uses Podman and no conda env. Summer: swap in a Podman equivalent (re-record 16). For now, mention it on the end slide ("this was the Docker-era version…"). | *Summer* re-record | — |
| The Answer? (4) | P3 `proj4/6` → `PROJ` | none | none |
| Chaining (13), Files (7) notes | P3 "much useful" → "much more useful"; "unique memorable" → "unique and memorable" | none | none |
| Anatomy of a Command (5) | P3 Check the `bit.ly/2vrUFKi` link still resolves | — | — |

**Live decks**

- [ ] **[L] P2 S** 2.7 On Writing: Asana says the AI material in Week 2 was "possibly belabour[ed]". Trim it, keep the slopsquatting point, and link to D6.
- [x] **[L]** 2.6 What We Do: table typos fixed and Git links moved to 3.4 (done on branch).
- [x] **[R]** `week2.qmd`: accessible title added to the Graham-Cumming video (done on branch).

## Week 3 — Foundations (Pt. 2)

**Session page**

- [x] **[R] P1 S** Overview: "We will also be looking to the Unix Shell/Terminal", but that was Week 2 (2.5). This week is Git.
- [x] **[R] P1 S** Practical: "how functions … can be collected into reusable packages" is **Week 4's** practical text (it's duplicated there). Replace it with nested data structures (DOLs, LOLs).
- [ ] **[R] P2 S** LO1 is vague. Suggested LOs: (1) choose between a list, dict, LOL or DOL for a given dataset and justify the choice; (2) access nested values by chaining indexes and keys; (3) use `add` / `commit` / `push` / `pull` to version a notebook on GitHub.
- [ ] **[R] P2 M** Asana: "Need to update summary of chapter 6 of Data Feminism" (the study guide).
- [x] **[R] P3 S** The LOLs row says "Notes" instead of "Slides". Typo: "minortised".
- [ ] **[A] P2 S** Asana: review the Moodle quiz for this week or next (the "markdown one in week 3 or 4" has questionable answers).

**3.1 Dictionaries: [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Deliberately Similar (4) | **P1** `print(cities[2])` is commented "Prints London", but the chunk is **executed** and prints *Paris*. Use `cities[1]`. The dict also gives Paris 837442 (SF's population) → 2229621 (also on Iterating, seq 9). | none | none |
| So: Key -> Value (3) | **P1** `lookup(52.1)` → `lookup[52.1]` | none | none |
| Danger, Will Robinson! (13) + Iterating notes (9) | **P1** "Dictionaries are **unordered**". Since Python 3.7 dicts keep insertion order. The **script already says** "Python is quite unusual in returning elements in the order in which they were inserted", so only the slide and notes are wrong. Reword to: "Python keeps insertion order, but most languages don't, so don't rely on order for *meaning*." | none | Sync the `.qmd` notes with the script |
| Getting Values (cont'd) (7) | P3 `if not c:` also fires when the value is `0`. Prefer `if c is None:` | none | none |

**3.2 LOLs: [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Making This Useful (8), LOLs of LOLs (11) | **P1** New York's longitude is `74.0059` → **`-74.0059`**; London's is `0.1275` → **`-0.1275`** (both are west of Greenwich). Tokyo's UTC offset is `+8` → **`+9`**. The same data appears in 3.3 and 4.1. | none (the narration doesn't read the numbers) | none |
| Putting It Together (6) | P2 "access `j` in list `i` using … `i[j]`": in `for j in i`, `j` is a *value*, not an index. Reword to use `idx` names. | none | none |
| Notes only | P3 "How you print" → "How would you print"; "more then" → "than" | none | none |
| *Optional* end slide (13) | P2 Recap: a list of lists is a table without column names; next talk: DOLs fix that | new | — |

**3.3 DOLs to Data: [V], end slide recommended**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| All `ds1`/`ds2`/`cities` slides (2, 3, 6–9) | **P1** The same longitude and Tokyo time-zone fixes as 3.2 | none | none |
| How is _that_ easier??? (9) | **P2** The narration claims this lookup is fast with "no iteration" and that "adding more rows doesn't make it much slower". But `list.index()` *is* a linear scan. The slide's lead-in ("we can use any immutable thing as a key") also doesn't connect to the example. | *Summer* re-record 9. **For now**, correct it on the end slide. | Fix points 1 and 3 in the script |
| **New end slide (11)**, before Additional Resources | **P2** "Recap & Next": a DOL *is* a DataFrame in miniature, so this is how pandas works (Week 6). One clarification: `.index()` still searches the list, and pandas adds a proper index to make lookups fast. Retrieval question: *get Tokyo's time zone in one line.* | **new** (~60 s) | Add `## Recap & Next` |

**3.4 Git: [V], end slide recommended**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| **New end slide (21)**, after Cheat Sheets | **P2** "Pull before you push": the most common student error is a rejected push. Also note that GitHub's default branch is `main`, whereas the slides show `master`. For the group project, one person creates the private repo (4.5). Links to Asana "Git improvements" and coordinating with Andy Mac. | **new** (~45 s) | Add `## Recap & Next` |
| Working on a Project (13) | P3 The commit message in the command doesn't match the output shown ("…README." vs "…README Markdown file.") | none | none |
| Getting Started (10), Working on a File (11) notes, Workflow (18) | P3 Typos: "achive", "commiting", "instantaeous", "or you GitHub account" | none | none |
| Additional Resources (not narrated) | P3 The Personal Access Tokens link points to an "about apps" page → use `docs.github.com/en/authentication/…/managing-your-personal-access-tokens` | none | none |
| *Summer* | Asana: short screen-capture video on the *purpose* of Git/GitHub (create repo → add/commit/push/pull → a conflict). Asana also has "consider removing Git" (see the Summer section) | L | — |

## Week 4 — Reduce, Reuse, Recycle

**Session page**

- [x] **[R] P1 S** The Overview repeats Week 3's paragraph verbatim ("This week we also start to move beyond Code Camp… The next two weeks…"). Delete it or rewrite it.
- [x] **[R] P1 S** The Code Camp "Packages" link points to `Functions.html`.
- [ ] **[R] P2 S** Study guide: "Why do they suggest that you shouldn't *never* use the 'god trick'?" The double negative reads as a typo. Suggest "…why they don't say you should *never* use the 'god trick'".
- [x] **[R] P3 S** "In this week's session will provide" → "This week's session will provide"; "resuable".

**4.1 Functions: [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Complicating Things… (12) | **P1** The `ds2` longitude and Tokyo time-zone fixes (as 3.2) | none | none |
| So What Does a Function Look like? (4) | P3 "All function 'calls' looking" → "look" | none | none |
| Getting Information Out (10) | P3 The output is shown as `'Hello New Programmers!'` with quotes, but `print` gives no quotes | none | none |

**4.2 Decorators: [V], end slide recommended**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Modifying the Function (3) | P2 `print("  + Defining hello!")` runs when `hello` is *called*, not when it's defined, so it reinforces the wrong mental model. → "+ Running hello!" | none (check the script doesn't read it out) | — |
| Some Applications 1 (13) | P2 `*args, **kwargs` appear with no explanation. Add one line on the slide. | none | — |
| **New end slide (17)**, before Additional Resources | **P2** "Where you'll meet these": `@property`, `@classmethod` and `@staticmethod` next week (5.2); `@functools.cache` for slow data calls. Retrieval question: *what does `@better` do to `hello`?* | **new** (~45 s) | Add `## Recap & Next` |
| There's More / Benefits (15, 16) | P3 "performend", "behavour", "lots, lost more", "COding" (in resources) | none | none |

**4.3 Packages: [V], end slide recommended**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| So… (6) | **P2** "things that start with `__` are 'private' … things that start *and* end with `__` are metadata". The convention is `_x` = internal, `__x` = name-mangled, and `__x__` = special ("dunder"). The script repeats the error ("underscores around them … are private"). | none for the slide text; *Summer* re-record 6 | Fix the script |
| Why Namespaces Matter (7) notes | P2 "Python doesn't have a 'main' programme namespace". It does: `__main__`, which 5.4 then uses in `if __name__ == '__main__'`. | none (it's in the notes only, so check whether it was narrated) | — |
| Popular Packages (3) | P2 No `pandas`, `geopandas` or `matplotlib`, and it lists `os` where the module is moving to `pathlib` (see the 5.3 "It's a Choice" slide and the private TODO) | none | none |
| **New end slide (12)**, before Additional Resources | **P2** "A package is just `.py` files": notebooks (`.ipynb`) can't be imported, and this is what trips people up in the Week 5 practical (Asana item). Where our packages come from: the Podman image. Plus the `__` correction. Retrieval question: *after `from math import pi`, does `math.pi` work?* | **new** (~60 s) | Add `## Recap & Next` |
| Misc. | P3 PySAL alias `ps` is outdated (`libpysal`, `esda`); `python.readthedocs.io` → `docs.python.org`; TutorialsPoint link has no `https://`; "This import" → "imports" | none | none |

**Live decks**

- [ ] **[A] P1 M** 4.5 Assessments: delete the Assessment #1 (exam) section (D1), renumber the rest, and fix the peer-evaluation timing (D2), group size (D3), name (D4) and draft-presentation week (D5). Also: the template link has a double slash (`{{< var module.web >}}/assessments/…`), and the signup QR is from 25_26.
- [ ] **[A] P1 S** 4.4 Group Working: "begins in Week 6" (D5); the signup QR is from 25_26.
- [ ] **[A] P2 M** Asana: "Need to find space to talk about what a briefing might look like". 4.5 is the natural place: show one good example page from `content.qmd`'s examples.
- [ ] **[A] P3 S** `assessments/group.qmd`: "Contnent", "create a exploratory", "to to" (the last two are also in 4.5).

## Week 5 — Objects

**Session page**

- [ ] **[R] P3 S** Etherington question: "…whether they improve our understanding of both" (both what?). Also, LO3 describes the *practical*; that's fine, but the other LOs describe the talks. Consider splitting them.

**5.1 Methods**: no action needed. P3 typo "insantiated" (seq 4) if rebuilding anyway.

**5.2 Classes: [V], visual-only rebuild**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| The Constructor (6) | **P1** The aside says the parameters `sauce`/`cheese` "are the **same** as the instance variables … because they occupy different namespaces" → "are **not** the same" | none (not in the script) | none |
| Class Definition (5) | P2 `/opt/conda/lib/python3.7/site-packages` is a Python 3.7 / conda path. Replace it with `python -c "import site; print(site.getsitepackages())"` | none | The script has a similar stale path (line 51) |
| Recap (12) | P2 "All methods *have* to have `self`", but three slides later `@staticmethod` has no `self`. Add "(except static methods)". Also `(<parent class)` → `(<parent class>)`. | none | Script line 148 says the same |
| Class and Static Methods (16) | P3 `isAdult` uses `age > 18`, so 18-year-olds aren't adults → `>=` | none | none |
| Pizza slides (4–11) | P3 `class pizza(object)` is the Python 2 idiom and not CapWords; "chillis" and "chilis" are both used. *Summer* only, because it touches many slides. | none | — |

**5.3 Object-Oriented Design: [V], optional end slide**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Classes vs Packages (5) | P2 "Functionally, a class and a package are indistinguishable". The slide itself says "Ugh…". The script's version (the *import/access syntax* is the same) is better. Put that wording on the slide. | none | — |
| Key Concepts notes (2) | P2 The "polymorphism" definition given is really Liskov substitution. Polymorphism = the same method name behaving appropriately for each class (e.g. `len()` on str, list, dict). "`movingpandas` extends `geopandas`" is a loose claim (it wraps rather than subclasses). | *Summer* re-record 2 | Fix the script |
| *Optional* end slide (8) | P2 "Why this matters for you": you'll *use* classes (DataFrame, GeoDataFrame) far more than you'll write them, starting next week. | new | — |
| Tree of Vehicles notes (4) | P3 "buing" | none | none |

**5.4 Errors: [V], end slide recommended**

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| Challenge 1 (4) | **P2** The output shown is from old Python. Since 3.10 this example gives `SyntaxError: '(' was never closed` on the right line, which weakens the point being made. Either show the modern message and say *"newer Python is better at this, but not always"*, or pick an example that still misleads (e.g. a missing `:` inside a dict literal). | none if you only update the output; *Summer* re-record 4 | — |
| So Errors can be Trapped (9) / Trapping (10) | P2 Bare `except:` is taught with no caveat. Add "prefer `except Exception:`". It catches `KeyboardInterrupt` otherwise. | none | — |
| Collaboration & CI (20) | P2 The notes say "TravisCI was free for FOSS". It's GitHub Actions now. Defining integration testing as "running all tests for multiple components" is loose. | *Summer* re-record 20 | Fix the script |
| **New end slide (22)**, after the book-cover slide | **P2** "Reading an error, bottom-up": last line = type + message, then find *your* file in the traceback, then look one line above. Link to the Debugging Manifesto (seq 14). Also the GitHub Actions correction. Asana/private TODO: "update exceptions stuff to support assessment, better coding". Retrieval question: *what prints, and in what order, in the Raising Hell example?* | **new** (~60 s) | Add `## Recap & Next` |
| Misc. | P3 "Test-Based Development" → "Test-Driven Development"; "explict"; the doctest `square(-1) → 2` is a deliberate failure but isn't signposted; the book cover needs alt text | none | none |

## Week 6

### 6.2 Randomness: [V], new mid-deck segment (done on branch, needs recording)

| Slide (seq) | Change | Audio | Script |
|---|---|---|---|
| **How Seeds Work** (new, between seq 16 *Back to Randomness* and seq 17 *Seeds and State*) | New mermaid diagram of the PRNG as a "tape", showing `seed` / `getstate()` / `setstate()` | **new** (~30–40 s) | The narration already exists in `scripts/6.2-Randomness.md` but sits **in the wrong place** (after *Aaaand Repeat (chart)*). Move it to between *Back to Randomness* and *Seeds and State*. Typo "valueoff" → "value off" (also in the `.qmd` notes). |
| Seeds and State (seq 17→18) | none | optional trim | The new slide now covers "setting a seed sets the state", so optionally drop the first two sentences here (that would mean re-recording this segment) |

- [ ] Cut table: add row `17 How Seeds Work`, and renumber *Seeds and State* 17→18 and *Question* 18→19.
- [ ] Record the new segment and add it to the *Randomness* M4A.
- [ ] Check the mermaid diagram exports to PNG via decktape (it renders client-side, so allow render time).
- [ ] Commit the uncommitted `6.2-Randomness.qmd` change.

## Weeks 7–12 (skimmed via session pages only)

- [ ] **[R] P2 S** Week 8: learning objective 6 is empty. The week also leans on Miller:2015; Asana suggests moving it forward or replacing it with the "LLMs in Urban Planning" reading.
- [ ] **[R] P2 S** Week 7: the reading key `Bunday:0000` has no year, so check the bib entry.
- [ ] **[R] P3 S** Week 12: "classifcation".
- [ ] Full review of the week 6–12 decks: *after term starts*.
- [x] **[A] P2 S** Reading week LO2, "Start to work on the first few questions of the group assessment", sits awkwardly with 4.5/`group.qmd`: "Do *not* start … the data analysis … until we have covered Pandas in Week 6". Suggest rewording to "Start a literature scan for the group assessment".
- [x] **[R]** `week11.qmd`: callout heading levels normalised (done on branch).
- [x] **[R]** `reading_week.qmd`: accessible titles added to the embedded videos (done on branch).

## Summer 2027 (not before teaching)

- Re-record the segments flagged *Summer* above: 2.5 (16), 3.3 (9), 4.3 (6), 5.3 (2), 5.4 (4, 20). Then remove the matching "clarification" lines from the end slides.
- Asana "Big rethinks": the sequencing of Podman / Terminal / Git (Week 1 terminal, Week 2 Git, Week 3 Podman); whether to keep Git at all versus a stronger focus on prompting; an "Applications" slide and reading for each week; a 'simple world' 16×16 grid for teaching.
- Asana: a short video on the *purpose* of Docker/Podman (shared with QM).
- 5.2 pizza example: rename it to `Pizza` and drop `(object)` across all slides.
- Alt text across all decks.
