# How I worked with AI

I built this with Claude (code, docs, the Archify diagram) and ChatGPT (only to
make practice images). I used Claude as a pair programmer: it suggested things,
I questioned them, tested every step on my laptop, and made the calls.

## Full chat history

- Claude (whole project, from my very first prompt): https://claude.ai/share/f46f20c1-ff1f-4451-8274-ea4c9f6bbc4c
- ChatGPT (practice image generation): [paste ChatGPT share link here]

---

## Decision 1: Web app with Flask, split into small files

AI suggested: an offline app, without fixing the structure yet
I decided: Flask, with every job in its own file (`aligner.py`, `comparator.py`,
`storage.py`, one JS file per step) instead of one big script
Why: easier to read, test and explain in the interview. The image logic in
`core/` has no Flask code, so I can test it from the terminal.
Evidence: project structure in README, `tools/run_samples.py`

## Decision 2: Build in small steps, test each one before the next

AI suggested: it started giving several files at once (a whole "Step 6" with 4 parts)
I decided: one small step at a time, explanation first, then code, then I run
it and show the output before the next step
Why: I wanted to understand every file I push, and catch errors early. This
caught real problems: an unsaved file, a missing `storage.py`, and wrong upload steps.
Evidence: chat excerpt #1, commit history (one commit per step)

## Decision 3: Checking that our local API doesn't break the "no online APIs" rule

AI suggested: Flask routes under `/api` for the page to call
I decided: I stopped and questioned it, because the brief says no APIs. We
agreed the rule means online services (Gemini, OpenAI, cloud). Our routes run
on `127.0.0.1` and never leave the laptop. I also made sure the UI uses no CDN.
Why: breaking the offline rule would fail the task
Evidence: chat excerpt #1, README "Runs fully offline" section

## Decision 4: No model training

AI suggested: compare each named box with the reference (no training)
I first wanted: to add more cluttered boards and train a model
I decided: not to train. The reviewers name parts live on a board the app has
never seen, so a model trained on my boards wouldn't know their parts.
Why: comparing against their own reference works on any board, and training
would have taken the whole day with no clear gain
Evidence: chat excerpt #2, RESEARCH.md options table

## Decision 5: Test on a second, dense board

AI suggested: a second board as a test
I decided: a much busier board with tiny parts, and a test where a small
capacitor is missing, without changing any setting
Why: one simple board isn't proof. I wanted to know it works on a different board.
Evidence: `sample_images/board2/`, 3 / 3 correct with the same 0.35 threshold

## Decision 6: Fix overlapping labels before anything else

AI suggested: moving on to a label fix in the results image
I decided: stop, and fix what I saw first. On the dense board, part names in
Step 2 covered each other ("GREEN LED" showed as "GREEN I").
Why: the reviewers will name parts on their own board in the demo, so this
would show up live. Now boxes show numbers that match the list, and the full
name only appears on hover.
Evidence: chat excerpt #3, `static/js/step2.js`

## Decision 7: Don't trust AI-generated images, check them

AI suggested: prompts to generate practice images with ChatGPT
I decided: check every image in code against the reference before using it
Why: ChatGPT sometimes changed the wrong part. One edit removed an LED instead
of the small capacitor I asked for. The check caught it and I regenerated it.
Evidence: `sample_images/PROMPTS.md`

## Decision 8: Short, human docs

AI suggested: long, detailed docs with many tables
I decided: shorter docs written the way I'd explain it, first person
Why: reviewers read many repos. Short and clear is better than long and generic.
Evidence: RESEARCH.md was cut to about half after my feedback

---

## Chat excerpt #1

> me: i dont able to understand 6b and for further codes i doubt because in the
> pdf it say dont use api so firstly clear this then provide me
> DONT PROVIDE ALL THE CODES IN ONE GO. PROVIDE ME CODES step WISE AS SOON AS ANY
> step COMPLETED. I WILL PROVIDE YOU MY OUTPUT, CHECK MY OUTPUT IF THAT IS CORRECT
> THEN PROVIDE ME CODE FOR NEXT step. and before giving me code explain it why and
> what you are doing
>
> AI: Our code does not break the rule. The key word is online... Our "API" is
> just how the web page talks to Flask on the same laptop... From now on I'll
> follow your rule: one small step at a time, an explanation before each piece of
> code, and I wait for your output before giving the next step.

## Chat excerpt #2

> me: i think i should add more cluster pcb board pics and train them also
>
> AI: I'd advise against training... At the demo, the reviewers upload their own
> board and name their own parts live. A trained model only knows the boards and
> parts it was trained on... So use cluttered boards for testing, not training.
>
> me: Generate 1 cluttered board and 2-3 test images with small parts removed.
> Run them through the app as it is. No code change. provide me promt

## Chat excerpt #3

> me: FIRSTLY BEFORE CHANGING ANYTHING SEE THIS FIRST
> [screenshot of Step 2 with overlapping part names on the dense board]
>
> AI: I see it. In Step 2, the labels of small parts that sit close together
> overlap each other... each box shows only its small number, and the box you
> hover shows its full name.