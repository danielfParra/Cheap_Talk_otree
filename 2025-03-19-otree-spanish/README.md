# Sender-Receiver game

`oTree`: 5.11.1

`python`: 3.12.4

# **📖 Matching Procedure in the Experiment**  

## **1️⃣ Overview**  
This experiment involves **pairing participants into sender-receiver groups** based on dynamically assigned pools. The matching process ensures structured and randomized pairings while maintaining consistency across rounds.  

## **2️⃣ Pool Assignment**  
Participants are assigned to **pools** in the consent stage, which allows structured matching in later rounds. Each pool contains **only one type of participant**:  
- **Player A (Senders) are assigned to pools 1, 2, 3, etc.**  
- **Player B (Receivers) are assigned to pools 4, 5, 6, etc.**  

This separation ensures that each sender is always matched with a receiver from a different pool.  

## **3️⃣ Matching Rules**  
- **Each sender pool is always matched with a fixed receiver pool**:  
  - Pool **1** ↔ Pool **3**  
  - Pool **2** ↔ Pool **4**  
  - (For larger groups, Pool 1 ↔ Pool 4, Pool 2 ↔ Pool 5, etc.)  
- **Players within each pool are shuffled every round** to ensure they do not always face the same opponent.  

## **4️⃣ Handling Different Group Sizes**  
The experiment dynamically adapts to different participant counts:  

| **Total Participants (n)** | **Number of Pools** | **Players per Pool** | **Pool Matching** |
|----------------|--------------|----------------|----------------|
| 2 (Testing Mode) | No pools | 1 group of 2 | oTree auto-matching |
| 16 | 4 pools | 4 per pool | Pool 1 ↔ Pool 3, Pool 2 ↔ Pool 4 |
| 20 | 4 pools | 5 per pool | Pool 1 ↔ Pool 3, Pool 2 ↔ Pool 4 |
| 24 | 6 pools | 4 per pool | Pool 1 ↔ Pool 4, Pool 2 ↔ Pool 5, Pool 3 ↔ Pool 6 |
| 30 | 6 pools | 5 per pool | Pool 1 ↔ Pool 4, Pool 2 ↔ Pool 5, Pool 3 ↔ Pool 6 |

## **5️⃣ Special Case: `n=2` (No Pools)**  
When there are **only 2 participants**, pool assignment is skipped, and oTree **automatically matches them**.  

## **6️⃣ Matching Procedure in Each Round**  
1. **Players are assigned to pools in the consent app** based on participant count.  
2. **In the sender-receiver game, players are grouped based on fixed pool pairings.**  
3. **Players within each pool are shuffled every round** for randomization.  
4. **oTree ensures that each sender is always matched with a receiver.**  
5. **If `n=2`, pools are ignored, and oTree handles pairing automatically.**  

## **7️⃣ Summary**  
✔ **Dynamic pool assignment ensures structured matching.**  
✔ **Senders and receivers are always paired from different pools.**  
✔ **Randomization within pools prevents repetition of pairings.**  
✔ **The experiment adapts automatically to different participant counts.**  
