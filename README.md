Opening Hand Probability Calculator

This Streamlit app allows you to calculate the probability of drawing a successful (defined by the user) opening hand across multiple TCGs. It supports a variety of deck types, mulligan rules, and game-specific mechanics such as being on the play, turn-based draws, and borderline hand conversions (chance to convert hands that are nearly good enough into successful hands by drawing a card each turn for a set number of turns).

The tool is designed for competitive players, deck builders, and mathematicians interested in quantifying consistency and mulligan strategy.

The tool does not consider things like colour of cards or mana value (MTG) whether you will hit a basic pokemon in your opening hand if you are not specifying one as a wanted card (Pokemon) early draw engines or any cards that cycle for free in any of these card games. As such it is generally useful only to specific strategies like combo or decks with very specific ramp points that need to consistently hit a set of similar cards by turn x). Examples at the bottom of this README but I don't play every TCG covered by this app so I likely have missed some valuable use cases other players would have.

You can combine multiple different wanted cards up to 10 (but obviously trying to find 10 different cards by turn 2 in Hearthstone isn't happening and will just result in a 0% chance for everything, however the option is there), meaning more complex strategies can be modelled but do take some creativity in how you catagorise your wanted cards.

A few terms are worth explaining here:

Borderline hands: These are hands that nearly match what you need and are shown with a conversion chance based on how many turns you have to draw after you keep a borderline hand. This can be useful to identify hands it is better to stick with and trust to the top of the deck by comparing it with the first hand chance and the overall chance given the remaining mulligans. For example if you had 4 mulligans remaining in MTG Commander because you were willing to mulligan down to 5 you may not want to keep a borderline hand as the chance of hitting what you need with a mulligan is higher. However if you only had 1 mulligan remaining it may be better to stick with the borderline hand you have instead of risking a redraw.

Turns to complete a borderline hand: This metric shows the chance of each borderline hand completing in that many turns so a value of 2 will give 2 draws in most formats if you are not on the play and 1 if you are on the play. This is different for example in Hearthstone and is accounted for in each format to work correctly with their rules. If you're using this in MTG Commander for example you'd want to set it to at least 1 in most cases as everyone draws on their first turn so unless you're trying to combo in your first upkeep you will always see one card. If you set this to 0 or to 1 while on the play in TCGs that prevent your first draw on the play all borderline hands will have a 0% chance to complete as you are not drawing any cards after your mulligan phase.

The Other deck type: This is mostly left in to preserve the original version of this app. It contains very few QoL or automated features which can allow for more complex and niche calculations but does require a good understanding of how to use the tool. If for example you had a card that stripped all of X type of card from your deck and then draw 3 cards you could use the custom parameters to graph this specific niche situation. It is also useful for players of games I have not made deck types for such as Fire and Blood or Legends of Runeterra. Do bear in mind though that there is no custom logic in this mode except that it uses the London mulligan system (I picked this as MTG is my main TCG and I expect this part of the tool to see very little use, if you do not want to use mulligans just set the value to 0). If a game has a complex mulligan phase or draws multiple cards per turn etc this tool will be extremely unwieldy or impossible to use.

Overall Success Chance Across Mulligans: This one is hard to word in a way that makes sense and so may seem confusing. What it is doing is showing the chance as you take that action that remains if you took all your mulligans (the number you set as the number of acceptable mulligans) that one of them will be a successful hand. So if you see:

Opening hand : 71.58% - This was your chance before you drew your opening hand that either that hand or one of all remaining mulligans would be successful

1 mulligan(s) : 56.77% - This is your chance that if you take this mulligan and all subsequent mulligans one of those hands will be successful

2 mulligan(s) : 34.25% - This is your chance that if you take this mulligan and all subsequent mulligans one of those hands will be successful

This section is not considering the chances of drawing good borderline hands, it is solely looking for hands that are successful as they are drawn.

You can use this feature to compare with borderline hand conversion chance for accurate analysis on what hands you should be keeping and when. For example if you had a borderline hand selection like this:

Idx Borderline Hand Draw Prob (%) Conv Prob (%)

0 Land:0, Ramp:0, OtherCards:7 0.3344 0.0000 

1 Land:1, Ramp:0, OtherCards:6 2.3406 7.9944 

2 Land:2, Ramp:0, OtherCards:5 6.6793 27.0579 

3 Land:2, Ramp:1, OtherCards:4 11.1321 79.7828 

4 Land:3, Ramp:0, OtherCards:4 10.0719 39.0603

We can see that the Borderline Hand with Index 3 has a 79% conversion rate (in this case by turn 3 as that is what I specified) so if I want the hand by turn 3 and it doesn't matter if I get it earlier it would be better for me to keep 2 lands 1 ramp than to mulligan even when I have a free mulligan left to take (such as in EDH) 56.77% vs 79.78%. Comparatively it would only make sense to keep a 3 land 0 ramp (Index 4) after I have already used my first mulligan 34.23% vs 39.06%. This example doesn't consider the possibility of drawing a borderline hand and then the chance of converting it if you did take the mulligan instead of staying with the borderline hand, but as the draw probability of the Borderline Hands are listed this can be estimated or calculated seperately if that level of precision is important.

Another more accurate but more manual method would be to take the Single-hand success probability in this case 34.25% and add the draw probability add the probabilities of the hands that are better or as good as the one you have and that will tell you your chance on a single mulligan to get an equal or better hand. So if we had an Index 3 Borderline we would take 34.25% + 11.13% = 45.36% meaning a single mulligan has a 54.64% chance to decrease in value.

The above examples should hopefully show both examples of how to use the tool and its limitations. It is not intended to use the borderline hands in its mulligan calculations, they are there as a guideline to help advise when to mulligan and when to keep a hand that is "good enough".

Features

Supports multiple deck types and rulesets:

Magic: The Gathering (Commander & 60-card formats)

Pokémon TCG

Yu-Gi-Oh

Hearthstone

Standard 52-card decks

Arbitrary “Other” formats

Customizable deck composition: Input card categories, deck counts, and success requirements.

Automatic “Other Cards” calculation: Ensures the deck always sums to its legal size.

Success and Borderline hand classification:

Success = all success criteria are met immediately.

Borderline = a hand that is just short of meeting success (e.g., missing one land, missing one combo piece).

Borderline hand conversion probability: Calculates the chance of fixing borderline hands by a chosen turn (simulating extra draws).

Adjusts automatically if you are on the play in formats where that matters.

Mulligan system: Supports repeated mulligans for formats like Magic. Computes cumulative success chance across mulligans.

Detailed breakdown tables: Shows borderline hands, their raw probability, and the chance of converting them by your specified turn.

General Workflow

Choose your deck type Select from supported formats. This determines default deck sizes, mulligan systems, and hand sizes.

Define tracked cards Input card names, counts, and the number required for a “successful” hand.

Set mulligans and turn window

Number of mulligans (if supported by the format).

Number of turns to try converting borderline hands.

Run calculations See probabilities for immediate success, borderline hands, and cumulative mulligan outcomes.

Deck Type Rules and Explanations Magic: The Gathering (Commander — 100 Cards)

Deck Size: Fixed at 100.

Opening Hand: Always 7 cards.

Mulligans: Multiple mulligans supported (London mulligan modeled as independent redraws).

Borderline Conversion: Adjusted by number of turns to draw into missing cards.

Magic: The Gathering (60 Card Formats)

Deck Size: Fixed at 60.

Opening Hand: 7 cards.

On the Play?: Checkbox reduces effective extra draws by 1 (since you skip your first draw).

Mulligans: Multiple mulligans supported.

Pokémon TCG (60 Cards)

Deck Size: Fixed at 60.

Opening Hand: 7 cards.

On the Play?: Checkbox reduces effective extra draws by 1 (since no turn-1 draw on the play).

Mulligans: Not modeled (Pokémon mulligan rules are compulsory and opponent-dependent).

Yu-Gi-Oh (40 Cards)

Deck Size: Fixed at 40.

Opening Hand: 5 cards.

On the Play?: Checkbox reduces effective extra draws by 1 (no turn-1 draw on the play).

Mulligans: Not supported.

Hearthstone (30 Cards)

Deck Size: Fixed at 30.

Opening Hand: Automatically set — 3 cards if on the play, 4 if going second.

Mulligans: Supported only once (Hearthstone mulligan is a single redraw phase).

Reasoning: Hearthstone’s unique mulligan and asymmetric hand sizes are hard-coded to match the real game.

Playing Card Deck (52 Cards)

Deck Size: Fixed at 52.

Opening Hand: User-defined via input box.

Mulligans: Not supported.

Reasoning: Provides flexibility for modeling card game variants outside of TCGs (e.g., Poker probabilities).

Other (Custom Deck Size)

Deck Size: User-defined.

Opening Hand: User-defined.

Mulligans: Fully supported with configurable count.

Reasoning: Designed for less common games or custom probability analysis.

Example Use Cases

MTG Commander: Probability of starting with ≥3 lands and ≥1 ramp spell as well as computing chance of seeing those cards by a specific turn such as turn 4 for 4 mana ramp spells, accounting for two mulligans.

Pokémon TCG: Probability of opening with at least one Basic Pokémon, or hitting an evolution by turn 2.

Hearthstone: Compare success rates between going first and second with specific opening card requirements for combo based strategies.

Custom: Model arbitrary card games by defining deck size, hand size, and success conditions. Also useful to measure very specific circumstances such as finding cards with draw spells when a certain number of cards have been already removed from your deck. Using this deck type requires some creativity and understanding off the tool.

Notes from the creator:

This app was created by a novice coder heavily utilising generative AI and was mostly made for me and my friends to help us build more consistent EDH decks, in the end the app seemed useful and was fun to work on so I added extra features and then felt I may as well make it public in case someone runs across this repo and finds it useful to them. As such the code is sloppy in places and due to my limited mathematical background I have not been able to verify with certainty that the calculations it makes are always correct, though I have done my best with comparative samples and using known values to prove it is at least somewhat accurate most of the time. I hope the app is useful to a couple of people despite all this!

(also I am a total beginner with GitHub so if the way I have organised the repo and releases is wrong I'd appreciate constructive criticism)
