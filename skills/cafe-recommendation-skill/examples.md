# Cafe Recommendation Examples

## Cold black coffee

User:

> I want something cold, smooth, and high caffeine. No milk.

Tool call:

```json
{
  "mood": "cold smooth",
  "prefer_milk": false,
  "caffeine": "high",
  "temperature": "cold"
}
```

Expected answer:

Recommend Cold Brew because it is cold, black, high caffeine, and matches smooth flavor notes.

## Gentle evening coffee

User:

> I want a creamy coffee for the evening, but not much caffeine.

Tool call:

```json
{
  "mood": "creamy evening",
  "prefer_milk": true,
  "caffeine": "low",
  "temperature": "hot"
}
```

Expected answer:

Recommend Decaf Latte because it is a hot milk drink with low caffeine and a mild creamy profile.

## Menu request

User:

> What coffees are available?

Tool call:

```json
{}
```

Expected answer:

Call `list_coffee_menu` and summarize the available options with their style, milk flag, and caffeine level.
