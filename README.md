Opening Hand Probability Calculator

A Streamlit-based tool to calculate and visualize the probability of drawing a successful opening hand in card games, with support for multiple card types, mulligans, extra draws, and borderline hands.

Features
1. Flexible Deck Configuration

Track any number of wanted card types (e.g., Land, Ramp, Spells).

Specify the count of each card type in the deck.

Specify the minimum number of each card type required for success.

2. Automatic Deck Size Options

Choose a preset deck size: 100, 60, or 40 cards.

Automatically calculates the Other Cards count based on the deck size and wanted cards.

Hides manual input for Other Cards when a preset deck size is selected.

Custom deck size option:

Allows manual entry of the Other Cards count.

3. Opening Hand and Mulligan Analysis

Specify opening hand size, number of allowed mulligans, and extra draws for borderline hands.

Calculates the probability of drawing a successful opening hand for the first hand and subsequent mulligans.

Shows a mulligan cascade table, displaying the overall chance of success if the user continues through each mulligan.

4. Borderline Hands Analysis

Identifies hands that are one card short of success.

Calculates the probability that a borderline hand can convert into a successful hand with extra draws.

Displays a table showing:

Borderline hand composition.

Probability of drawing that hand.

Probability of converting the hand with extra draws.

Contribution to overall success probability (for demonstration only).

5. User Interface

Streamlit web app with a clean, interactive layout.

Input fields for card names, counts, and success requirements.

Toggle for deck size presets and custom deck configuration.

Output includes tables and percentages for easy readability.

Usage Example

Select number of wanted card types (e.g., 40 for Land and 15 for Ramp).

Fill in card names, deck counts, and success requirements.

Select deck size preset (100, 60, 40) or Custom.

Enter opening hand size, mulligans, and extra draws for borderline hands.

Click Calculate Probabilities to see:

Borderline hands table.

Single-hand success probability.

Mulligan cascade probabilities.

Access the app here: https://handcalculator.streamlit.app/
