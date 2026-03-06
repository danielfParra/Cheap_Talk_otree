# Sender-Receiver game

`oTree`: 6.0.11

`python`: 3.12.4

# **📖 Experiment Architecture (Updated March 2026)**

## **1️⃣ Overview**
This experiment has been restructured from a live 2-player interactive game into a **1-player simulation**. All live participants now play exclusively as **Player B (Receivers)**. The actions of Player A (Senders) are simulated using historical data collected from previous experimental sessions.

## **2️⃣ Single-Player Architecture**
- **Group Size**: `players_per_group = None` (Each participant is in their own group of 1).
- **Role Assignment**: Every participant is assigned the role of `Player B` (Receiver).
- **Historical Data Integration**: Instead of waiting for a live Player A to send a message, the system loads historical messages and secret numbers from a pre-generated CSV file (`messages_for_receivers.csv`).

## **3️⃣ Data Mapping & Assignment**
- During `creating_session` (Round 1), each live participant is randomly assigned a unique `sender_code` from `messages_for_receivers.csv`.
- For all 4 rounds, the live participant faces the exact sequence of `secret_number`, `sender_message`, and `sender_choice` of their assigned historical sender.
- Assigned codes are marked `used = 1` in the CSV after session creation to avoid reuse across sessions.
- **Pool exhaustion guard**: if the number of unused codes is smaller than the number of participants in the session, the system falls back to the full pool (all rows) before shuffling, so no two participants in the same session ever share a sender code.

### CSV files
| File | Description |
|---|---|
| `messages_for_receivers.csv` | Active file used by the app. Columns: `code`, `secret_number_R1`–`R24`, `sender_message_R1`–`R24`, `sender_choice_R1`–`R24`, `used` |
| `messages_for_receivers_with_X.csv` | Extended version with additional `X_R1`–`X_R24` columns (extra variable per round, not yet loaded by the app) |

### `sender_choice` values
- `1`–`7`: Sender manually chose that number to send.
- `8`: Sender delegated to the computer (honest — message equals true secret number).

## **4️⃣ Payoffs & Incentives**
- **Decoding Task**: Paid based on a piece-rate (`PIECE_RATE_DECODE` = 500 COP) per correct answer.
- **Sender-Receiver Game**: Quadratic scoring rule; only `PREDEFINED_RECEIVER_ROUNDS` are payoff-relevant. Bonus = `BONUS_AMOUNT` (4000 COP).
- **Honesty Guess** (`HonestyGuess` page): Participant guesses the % of times their assigned sender delegated to the computer. Incentivized with `HONESTY_GUESS_BONUS` (1000 COP) via quadratic scoring.
- **Honesty Certainty** (`HonestyCertainty` page): Follow-up confidence question for the honesty guess.
- **Credulity Guess** (`FollowingGuess` page): Participant guesses the % of times other receivers followed the message when it was 7. Incentivized with `CREDULITY_GUESS_BONUS` (1000 COP).
- **Explanation Task** (`ExplanationTask` page): Participant writes their guessing strategy. A post-session ChatGPT evaluation determines the bonus (`EXPLANATION_BONUS` = 4000 COP).

## **5️⃣ Treatments**

The treatment is set in `settings.py` via the `treatment` key in each session config and stored in `player.participant.treatment`. Assignment happens in `welcome/__init__.py` with a single line:
```python
player.participant.treatment = player.session.config['treatment']
```

Active treatments:

| Treatment | Session name | Description |
|---|---|---|
| `ExpertRep` | `sender_receiver_game_expertrep` | Baseline: receiver enters a direct guess via slider |
| `Belief` | `sender_receiver_game_belief` | Receiver states a belief % about lying; computer computes optimal guess |
| `FixBelief` | `sender_receiver_game_fixbelief` | TBD |
| `NoUncertainty` | `sender_receiver_game_nouncertainty` | TBD |

### **ExpertRep**
The baseline treatment. Player A had the option to delegate message selection to a computer that always sends the true secret number. Player B sees the message and moves a slider to enter a direct guess of the secret number.

### **Belief**
Player B states their **belief about the likelihood that Player A delegated to the computer** (i.e., was honest). The computer then automatically computes and submits the **optimal guess** using the quadratic scoring rule:

$$g^* = p \cdot \text{message} + (1 - p) \cdot 4$$

where $p$ is the stated belief (fraction honest/delegated) and $4$ is the unconditional mean of the secret number. The belief is stored in `player.belief_honest_pct` (0–100 integer, `initial=0`). The optimal guess is computed server-side in `ReceiverGuess.before_next_page` and written to `player.receiver_guess`. The belief slider starts at 0% (left) and only reveals the submit button once the participant moves it. On timeout without interaction, `belief_honest_pct` remains 0, so the computer submits `g* = 4` (no trust). The decoding step is skipped for this treatment.

### **FixBelief**
TBD.

### **NoUncertainty**
TBD.

## **6️⃣ Page Sequence**

```
PreviousExperimentInfo → instructions1 → instructions2 → TimeLimit → Decode (always hidden)
→ instructions3 → instructions4
→ role_info                  [includes BeliefTransition content for Belief treatment]
→ ControlQuestions ×5       [round 1, repeats until all correct]
→ TutorialIntro
→ ReceiverTutorial          [ExpertRep only, round 1]
→ BeliefTutorial            [Belief only, round 1]
→ start_page
→ Round_number → ReceiverGuess → Results    [every round]
→ HonestyGuess → HonestyCertainty → FollowingGuess → ExplanationTask   [last round only]
```

Key per-treatment differences:

| Page | ExpertRep | Belief |
|---|---|---|
| `role_info` | standard role page | includes BeliefTransition content (explains belief task & formula via modal) |
| `ReceiverTutorial` | shown (direct-guess slider + intro.js tour) | hidden |
| `BeliefTutorial` | hidden | shown (belief slider + intro.js tour with optimal-guess step) |
| `ReceiverGuess` form fields | `receiver_guess`, `guess_confirmed` | `receiver_guess`, `guess_confirmed`, `belief_honest_pct` |
| `Results` feedback | Guess shown directly | Stated belief % + computer's optimal guess both shown |
| `ControlQuestions` Q_task answer | "Adivinar el número secreto" | "Reportar mi creencia sobre cuántas veces el Jugador A delegó al computador" |

## **7️⃣ Key Pages**

### `PreviousExperimentInfo.html`
Uses arrow-reveal blocks (same pattern as `instructions1.html`). Three sections:
1. Always visible: context about the previous experiment (Player A/B roles, delegation).
2. Arrow 1 → "Your Task Today": describes today's task; for Belief, a treatment-conditional paragraph explains that they will report a belief % instead of a direct guess.
3. Arrow 2 → "About the Instructions Below": why to read the historical instructions carefully. Reveals the Next button.

### `BeliefTransition.html`
Its content is integrated into `role_info.html`, shown conditionally for Belief participants. The legacy `BeliefTransition` file/class remains in the repository but is not included in `page_sequence`. The integrated block explains:
- The previous experiment had Player B guess directly; today's task is different.
- They will report a belief about the likelihood that Player A delegated to the computer.
- The computer submits the **guess that maximises their bonus** given that belief — so they should report their true belief.
- The formula $g^* = p \times m + (1-p) \times 4$ is hidden behind a "Show the formula" modal button.

### `BeliefTutorial.html`
Interactive intro.js-guided tutorial for the belief slider (replaces `ReceiverTutorial` for Belief). Tour steps:
1. Introduction
2. Left-pane reminder
3. Round number
4. Player A's message
5. Belief slider — **blocked** until participant moves it; unblocks Next on first interaction
6. Optimal guess card — shows the computed guess after the slider is moved
7. Submit button

### `ReceiverGuess.html` (Belief decision screen)
In Belief treatment, the Spanish elicitation is framed as a **probability/likelihood** question (not “how often”): participants report the percentage probability that Player A delegated to the computer. The UI then displays the implied optimal guess and submits it on confirmation.

### `ControlQuestions.html`
`Q_task` is now treatment-aware:
- ExpertRep: correct answer = *"Adivinar el número secreto"*; options list = `O_task`
- Belief: correct answer = *"Reportar mi creencia sobre cuántas veces el Jugador A delegó al computador"*; options list = `O_task_Belief` (no "Adivinar" option shown)
- Hint (`H_task_Belief`) explains the belief mechanism on wrong answer.

## **8️⃣ Survey**
The final survey (`survey` app) collects: `age`, `gender`, `education`, `student`, `experiments`, `reasoning`, `chosen_role`. The fundaciones opinion table was removed. All fields are in Spanish.

## **9️⃣ Obsolete Features (Removed)**
- **Live Matching Protocol**: Pool-based matching system removed; no live Player As.
- **Wait Pages**: All synchronization wait pages removed.
- **Sender UI**: Pages for Player A actions removed from the page sequence.
- **Babbling / Decode treatments**: Removed from all logic and templates. Only `ExpertRep`, `Belief`, `FixBelief`, `NoUncertainty` are active.
