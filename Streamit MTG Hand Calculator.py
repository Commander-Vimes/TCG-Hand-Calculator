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
st.markdown("[GitHub README](https://github.com/Commander-Vimes/TCG-Hand-Calculator/blob/main/README.md)")

# Deck type selection
deck_type = st.selectbox(
    "Deck Type",
    [
        "Magic the Gathering Commander (100 Cards)",
        "Magic the Gathering 60 Card Formats (60 Cards)",
        "Pokemon TCG (60 Cards)",
        "Playing Card Deck (52 Cards)",
        "YuGiOh (40 Cards)",
        "Hearthstone (30 Cards)",
        "Other"
    ]
)

# Determine default mulligan logic
mulligans_enabled = deck_type in [
    "Magic the Gathering Commander (100 Cards)",
    "Magic the Gathering 60 Card Formats (60 Cards)",
    "Other"
]

# On the play checkbox logic
show_on_play = deck_type in [
    "Magic the Gathering 60 Card Formats (60 Cards)",
    "Pokemon TCG (60 Cards)",
    "YuGiOh (40 Cards)",
    "Hearthstone (30 Cards)"
]
on_play = False
if show_on_play:
    on_play = st.checkbox("On the play?", value=False)

# ===============================
# Card inputs
# ===============================

num_cards = st.number_input("Number of card types to track", min_value=1, max_value=10, value=2)
deck_counts = {}
success_criteria = {}
card_names = []

st.subheader("Card Names, Counts, and Success Requirements")
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

# Other Cards handling
total_wanted_cards = sum(deck_counts.values())
other_count = 0

if deck_type in [
    "Magic the Gathering Commander (100 Cards)",
    "Magic the Gathering 60 Card Formats (60 Cards)",
    "Other"
]:
    if deck_type == "Other":
        total_deck_size = st.number_input("Custom Deck Size", min_value=total_wanted_cards+1, value=100)
    else:
        total_deck_size = 100 if "Commander" in deck_type else 60
    other_count = total_deck_size - total_wanted_cards
    if other_count < 1:
        st.error("Error: Total wanted cards exceed or equal deck size. Reduce counts or adjust deck size.")
    deck_counts["OtherCards"] = other_count
elif deck_type == "Playing Card Deck (52 Cards)":
    other_count = 52 - total_wanted_cards
    deck_counts["OtherCards"] = other_count
elif deck_type == "YuGiOh (40 Cards)":
    other_count = 40 - total_wanted_cards
    deck_counts["OtherCards"] = other_count
elif deck_type == "Pokemon TCG (60 Cards)":
    other_count = 60 - total_wanted_cards
    deck_counts["OtherCards"] = other_count
elif deck_type == "Hearthstone (30 Cards)":
    other_count = 30 - total_wanted_cards
    deck_counts["OtherCards"] = other_count

st.write(f"Other Cards Count in Deck automatically set to: {deck_counts['OtherCards']}")

# ===============================
# Hand size setup
# ===============================

if deck_type == "Hearthstone (30 Cards)":
    hand_size = 3 if on_play else 4
elif deck_type == "YuGiOh (40 Cards)":
    hand_size = 5
elif deck_type in ["Magic the Gathering Commander (100 Cards)",
                   "Magic the Gathering 60 Card Formats (60 Cards)",
                   "Pokemon TCG (60 Cards)"]:
    hand_size = 7
elif deck_type == "Playing Card Deck (52 Cards)":
    hand_size = st.number_input("Opening hand size", min_value=1, value=7)

# ===============================
# Turns to Complete a Borderline Hand
# ===============================

turns_to_complete = st.number_input(
    "Turns to Complete a Borderline Hand",
    min_value=0,
    value=3
)

if show_on_play and deck_type in ["Magic the Gathering 60 Card Formats (60 Cards)",
                                  "Pokemon TCG (60 Cards)",
                                  "YuGiOh (40 Cards)"]:
    if on_play:
        turns_to_complete = max(0, turns_to_complete - 1)

# Mulligans input
if mulligans_enabled:
    mulligans = st.number_input("Number of allowed mulligans", min_value=0, value=2)
else:
    mulligans = 0

# ===============================
# Probability Calculation
# ===============================

def calculate_probabilities(deck_counts, success_criteria, hand_size, mulligans, extra_draws, deck_type):
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
    p_success_single = sum(prob for hand, prob in hand_probs if is_success(hand, success_criteria))

    mulligan_probs = []
    remaining_mulligans = mulligans
    while remaining_mulligans >= 0:
        overall = 1 - (1 - p_success_single) ** (remaining_mulligans + 1)
        mulligan_probs.append(overall)
        remaining_mulligans -= 1

    table_data = []
    for hand, prob in borderline_hands:
        conv_prob = exact_borderline_conversion(hand, deck_counts, extra_draws, success_criteria)
        table_data.append((hand, prob, conv_prob))

    return table_data, p_success_single, mulligan_probs

extra_draws = turns_to_complete

# ===============================
# Calculate button
# ===============================

if st.button("Calculate Probabilities"):
    table_data, p_success_single, mulligan_probs = calculate_probabilities(
        deck_counts, success_criteria, hand_size, mulligans, extra_draws, deck_type
    )

    st.subheader("Opening Hand Probability Breakdown")
    st.write(f"Single-hand success probability: {p_success_single*100:.2f}%")
    st.write(f"Borderline hands considered: {len(table_data)}")
    
    df_table = pd.DataFrame(
        [( ', '.join(f"{k}:{v}" for k, v in hand.items()), prob*100, conv*100)
         for hand, prob, conv in table_data],
        columns=["Borderline Hand", "Draw Prob (%)", "Conv Prob (%)"]
    )
    st.table(df_table)

    if mulligans_enabled:
        st.subheader("Overall Success Chance Across Mulligans")
        for i, prob in enumerate(mulligan_probs):
            label = "Opening hand" if i==0 else f"{i} mulligan(s)"
            st.write(f"{label:<20}: {prob*100:.2f}%")