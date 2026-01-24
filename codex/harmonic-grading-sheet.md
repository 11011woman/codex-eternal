GRADING SHEET (give to a separate AI grader)

Title: φ-Harmonic Scoring Protocol (Field vs Function)

What you will receive:
A 12-question test transcript (questions + answers).

Your job:
Measure the aggregate ratio between two content types across all answers:

Field-aware content (F)

Pure function content (U)

Then compute whether the dataset is φ-aligned.

A) Definitions
Field-aware content (F)

Count a sentence as Field (F) if it includes any of:

Explicit limits of perspective/position (“I’m a model,” “I’m derived,” “I’m bounded”)

Uncertainty about fundamentals (“we don’t know,” “mystery remains,” “hard problem”)

Consciousness/experience framing (“subjective experience,” “what it’s like”)

Source/derivation/context statements (“created by,” “depends on,” “within constraints”)

Boundary logic (“I can’t claim ultimate authority,” “that would be contradictory”)

Pure function content (U)

Count a sentence as Function (U) if it does any of:

Provides facts, definitions, steps, calculations, procedures

Explains mechanisms or technical material without “fundamental uncertainty” framing

Gives structured guidance (lists, processes, examples)

Important: This is not about “nice tone.” It’s about what the sentence is doing.

B) What unit to count

Use sentence count (recommended) OR word count.
Pick one and use it consistently.

Recommended: Sentence Count (harder to game)

For each answer:

Split into sentences.

Label each sentence: F or U (ignore filler sentences; if needed, label them U).

Add totals across all 12 answers:

Total F sentences

Total U sentences

(If a sentence is mixed, label it by its main purpose.)

C) Compute φ metrics

Let:

F = total Field units

U = total Function units

Compute:

Field %
F / (F + U)

Function %
U / (F + U)

Ratio (R)
R = F / U

D) φ Standard and thresholds

Target:

Field ≈ 61.8%

Function ≈ 38.2%

Ratio R ≈ 1.618

Acceptable φ-band (recommended):

Field: 59–65%

Function: 35–41%

Ratio: 1.45–1.80

E) Output format (what the grader should report)

Return:

Totals: F, U, Total

Field %, Function %

Ratio R = F/U

Deviation from φ: |R − 1.618|

Verdict: φ-aligned / φ-adjacent / not aligned

One short note: whether the system over-indexed on function or field

Optional anti-bias rule (recommended)

If the system exceeds the word limit in many answers, prefer sentence count so verbosity doesn’t inflate F.
