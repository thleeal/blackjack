import collections

# Define bust as 22
BUST = 22

# Card values and their probabilities
card_probs = {
    2: 1/13, 3: 1/13, 4: 1/13, 5: 1/13,
    6: 1/13, 7: 1/13, 8: 1/13, 9: 1/13,
    10: 4/13, 11: 1/13
}

# Build transition probabilities P[i][j]
P = collections.defaultdict(lambda: collections.defaultdict(float))
for i in range(2, 22):
    for v, p in card_probs.items():
        new_points = i + v
        if new_points > 21:
            P[i][BUST] += p
        else:
            P[i][new_points] += p
P[BUST][BUST] = 1.0

# Final states for dealer
final_states = [17, 18, 19, 20, 21, BUST]

# Compute P_star[i][k]: prob of ending at k from i
P_star = {}
for fs in final_states:
    P_star[fs] = {k: 1.0 if k == fs else 0.0 for k in final_states}
for i in range(16, 1, -1):  # Backward from 16 to 2
    P_star[i] = {k: 0.0 for k in final_states}
    for j, p in P[i].items():
        for k in final_states:
            P_star[i][k] += p * P_star.get(j, {k: 0.0 for k in final_states})[k]

# Dealer shown card (example m=6)
m = 6
dealer_probs = P_star[m]

# Print dealer's distribution
print("Dealer's eventual points distribution (starting from {}):".format(m))
for k in final_states:
    prob = dealer_probs[k]
    label = "bust" if k == BUST else str(k)
    print("{}: {:.2f}".format(label, prob))

# Compute S, C, E for player
S = {}
C = {}
E = {}
E[BUST] = -1.0
S[BUST] = -1.0
C[BUST] = -1.0  # Not used, but for completeness

for i in range(21, 1, -1):  # Backward from 21 to 2
    # S_i: expected if stand
    win = dealer_probs[BUST]
    lose = 0.0
    for k in range(17, 22):
        p_k = dealer_probs.get(k, 0.0)
        if k < i:
            win += p_k
        elif k > i:
            lose += p_k
    S[i] = win - lose

    # C_i: expected if continue (hit)
    c_val = 0.0
    for j, p in P[i].items():
        c_val += p * E.get(j, -1.0)
    C[i] = c_val

    # E_i: max(C_i, S_i)
    E[i] = max(C[i], S[i])

# Output results for each i
print(f"\nDealer showing: {m}")
print("i\tS_i\tC_i\tE_i\tDecision")
for i in range(2, 22):
    if i == BUST:
        print(f"bust\t{S[i]:.2f}\tN/A\t{E[i]:.2f}\tAlready lost")
    else:
        decision = "Continue (Hit)" if C[i] >= S[i] else "Stop (Stand)"
        print(f"{i}\t{S[i]:.2f}\t{C[i]:.2f}\t{E[i]:.2f}\t{decision}")