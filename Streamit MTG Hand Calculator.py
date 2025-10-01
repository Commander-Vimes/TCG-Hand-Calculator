import streamlit as st
import math
from itertools import product
import pandas as pd

# ===============================
# Helper Functions
# ===============================

def C(n, k):
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)

def all_possible_hands(deck_counts, hand_size):
    types = [k for k in deck_counts if deck_counts[k] > 0]
    ranges = [range(0, min(deck_counts[t], hand_size)+1) for t in types]
    hands = []
    for counts in product(*ranges):
        if sum(counts) == hand_size:
            hand = dict(zip(types, counts))
            hands.append(hand)
    return hands

def is_success(hand, success_criteria):
    return all(hand.get(k, 0) >= v for k, v in success_criteria.items() if v > 0)

def is_borderline(hand, success_criteria):
    if is_success(hand, success_criteria):
        return False
    has_exactly_one_below = False
    for k, v in success_criteria.items():
        if v == 0:
            continue
        count = hand.get(k, 0)
        if count > v:
            return False
        if count == v - 1:
            has_exactly_one_below = True
    return has_exactly_one_below

def exact_borderline_conversion(hand, deck_counts, extra_draws, success_criteria):
    needed_cards = {k: max(0, success_criteria[k] - hand.get(k, 0)) for k in success_criteria}
    total_needed = sum(needed_cards.values())
    if total_needed == 0:
        return 1.0
    if total_needed > extra_draws:
        return 0.0

    remaining_deck = {k: deck_counts.get(k,0) - hand.get(k,0) for k in deck_counts}
    types = [k for k in remaining_deck if remaining_deck[k] > 0]
    total_remaining = sum(remaining_deck.values())

    def recur(idx, draws_left, counts_so_far):
        if idx == len(types):
            if draws_left != 0:
                return 0
            for k, req in needed_cards.items():
                if counts_so_far.get(k, 0) < req:
                    return 0
            coeff = 1
            for t, c in counts_so_far.items():
                coeff *= C(remaining_deck[t], c)
            return coeff
        total = 0
        max_draw = min(remaining_deck[types[idx]], draws_left)
        for draw in range(0, max_draw + 1):
            new_counts = counts_so_far.copy()
            new_counts[types[idx]] = draw
            total += recur(idx + 1, draws_left - draw, new_counts)
        return total

    favorable = recur(0, extra_draws, {})
    total_possible = C(total_remaining, extra_draws)
    return favorable / total_possible

# ===============================
# Streamlit App
# ===============================

st.title("Opening Hand Probability Calculator")

# Deck size toggle
deck_size_option = st.selectbox(
    "Deck Size",
    ["100 Card", "60 Card", "40 Card", "Custom"]
)

num_cards = st.number_input("Number of card types to track", min_value=1, max_value=10, value=2)

deck_counts = {}
success_criteria = {}
card_names = []

st.subheader("Card Names, Counts, and Success Requirements")

# Horizontal layout for each card
for i in range(num_cards):
    cols = st.columns(3)
    with cols[0]:
        name = st.text_input(f"Card {i+1} Name", value=f"Card {i+1}", key=f"name_{i}")
    with cols[1]:
        count = st.number_input(f"{name} Count in Deck", min_value=0, value=10, key=f"count_{i}")
    with cols[2]:
        success = st.number_input(f"{name} Required for Success", min_value=0, value=1, key=f"success_{i}")
    
    deck_counts[name] = count
    success_criteria[name] = success
    card_names.append(name)

# Handle OtherCards logic
total_wanted_cards = sum(deck_counts.values())

if deck_size_option != "Custom":
    deck_size_map = {"100 Card": 100, "60 Card": 60, "40 Card": 40}
    total_deck_size = deck_size_map[deck_size_option]
    other_count = total_deck_size - total_wanted_cards
    if other_count < 1:
        st.error(f"Error: Total wanted cards ({total_wanted_cards}) exceed or equal deck size ({total_deck_size}). Please reduce counts or choose Custom deck size.")
        deck_counts["OtherCards"] = 0
    else:
        deck_counts["OtherCards"] = other_count
        st.write(f"Other Cards Count in Deck automatically set to: {deck_counts['OtherCards']}")
else:
    other_count = st.number_input("Other Cards Count in Deck", min_value=0, value=46)
    if other_count < 1:
        st.error("Error: OtherCards must be at least 1.")
    deck_counts["OtherCards"] = other_count

hand_size = st.number_input("Opening hand size", min_value=1, value=7)
mulligans = st.number_input("Number of allowed mulligans", min_value=0, value=2)
extra_draws = st.number_input("Number of extra draws for borderline hands", min_value=0, value=3)

# ===============================
# Probability Calculation
# ===============================

def calculate_probabilities(deck_counts, success_criteria, hand_size, mulligans, extra_draws):
    hands = all_possible_hands(deck_counts, hand_size)
    hand_probs = []
    total_cards = sum(deck_counts.values())

    for hand in hands:
        prob = 1
        remaining_hand_size = hand_size
        for card_type, count in hand.items():
            prob *= C(deck_counts[card_type], count)
            remaining_hand_size -= count
        prob /= C(total_cards, hand_size)
        hand_probs.append((hand, prob))

    borderline_hands = [(hand, prob) for hand, prob in hand_probs if is_borderline(hand, success_criteria)]

    # Overall probability ignoring borderline keeps
    p_success_single = sum(prob for hand, prob in hand_probs if is_success(hand, success_criteria))
    
    # Mulligan cascade (decreasing remaining chance)
    mulligan_probs = []
    remaining_mulligans = mulligans
    while remaining_mulligans >= 0:
        overall = 1 - (1 - p_success_single) ** (remaining_mulligans + 1)
        mulligan_probs.append(overall)
        remaining_mulligans -= 1

    # Borderline table
    table_data = []
    for hand, prob in borderline_hands:
        conv_prob = exact_borderline_conversion(hand, deck_counts, extra_draws, success_criteria)
        table_data.append((hand, prob, conv_prob, prob * conv_prob))

    return table_data, p_success_single, mulligan_probs

if st.button("Calculate Probabilities"):
    table_data, p_success_single, mulligan_probs = calculate_probabilities(
        deck_counts, success_criteria, hand_size, mulligans, extra_draws
    )

    st.subheader("Opening Hand Probability Breakdown")
    st.write(f"Single-hand success probability: {p_success_single*100:.2f}%")
    st.write(f"Borderline hands considered: {len(table_data)}")
    
    df_table = pd.DataFrame(
        [( ', '.join(f"{k}:{v}" for k, v in hand.items()), prob*100, conv*100, contrib*100)
         for hand, prob, conv, contrib in table_data],
        columns=["Borderline Hand", "Draw Prob (%)", "Conv Prob (%)", "Contribution (%)"]
    )
    st.table(df_table)

    st.subheader("Overall Success Chance Across Mulligans")
    for i, prob in enumerate(mulligan_probs):
        label = "Opening hand" if i==0 else f"After {i} mulligan(s)"
        st.write(f"{label:<20}: {prob*100:.2f}%")