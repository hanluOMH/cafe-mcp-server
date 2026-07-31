"""Pure Python coffee recommendation logic."""

from __future__ import annotations

from typing import Any

from .coffee_data import COFFEE_MENU

CoffeeItem = dict[str, Any]


def list_menu() -> list[CoffeeItem]:
    """Return a copy of the static coffee menu."""
    return [item.copy() for item in COFFEE_MENU]


def find_coffee(coffee_id: str) -> CoffeeItem | None:
    """Find a coffee by its stable id."""
    normalized_id = coffee_id.strip().lower().replace(" ", "_")
    return next((item.copy() for item in COFFEE_MENU if item["id"] == normalized_id), None)


def recommend_coffee(
    mood: str = "",
    prefer_milk: bool | None = None,
    caffeine: str | None = None,
    temperature: str | None = None,
) -> CoffeeItem:
    """Recommend one menu item from simple preference signals.

    The scoring intentionally stays deterministic and explainable for a demo.
    """
    desired_caffeine = _normalize_choice(caffeine, {"low", "medium", "high"})
    desired_temperature = _normalize_choice(temperature, {"hot", "cold"})
    mood_terms = _tokenize(mood)

    scored = []
    for item in COFFEE_MENU:
        score = 0
        reasons: list[str] = []

        if prefer_milk is not None and item["milk"] == prefer_milk:
            score += 3
            reasons.append("matches milk preference")

        if desired_caffeine and item["caffeine"] == desired_caffeine:
            score += 3
            reasons.append(f"matches {desired_caffeine} caffeine")

        if desired_temperature and item["style"] == desired_temperature:
            score += 2
            reasons.append(f"matches {desired_temperature} drink preference")

        flavor_matches = _matching_terms(mood_terms, item["flavor_notes"] + item["best_for"])
        if flavor_matches:
            score += 2 * len(flavor_matches)
            reasons.append("matches mood terms: " + ", ".join(flavor_matches))

        if not reasons:
            reasons.append("works as a balanced default")

        scored.append((score, item["name"], item, reasons))

    score, _, best_item, reasons = max(scored, key=lambda entry: (entry[0], -_tie_breaker(entry[2])))
    recommendation = best_item.copy()
    recommendation["score"] = score
    recommendation["reasons"] = reasons
    return recommendation


def explain_recommendation(
    coffee_id: str,
    mood: str = "",
    prefer_milk: bool | None = None,
    caffeine: str | None = None,
    temperature: str | None = None,
) -> str:
    """Explain why a selected coffee can fit the supplied preferences."""
    item = find_coffee(coffee_id)
    if item is None:
        available = ", ".join(menu_item["id"] for menu_item in COFFEE_MENU)
        return f"Unknown coffee id '{coffee_id}'. Available ids: {available}."

    recommended = recommend_coffee(
        mood=mood,
        prefer_milk=prefer_milk,
        caffeine=caffeine,
        temperature=temperature,
    )

    details = [
        f"{item['name']} is {item['description'][0].lower() + item['description'][1:]}",
        f"It is a {item['style']} drink with {item['caffeine']} caffeine.",
        "Flavor notes: " + ", ".join(item["flavor_notes"]) + ".",
    ]

    if recommended["id"] == item["id"]:
        details.append("It is the top match for the provided preferences.")
    else:
        details.append(f"For those preferences, the top match is {recommended['name']}.")

    return " ".join(details)


def _normalize_choice(value: str | None, allowed: set[str]) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized if normalized in allowed else None


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in text.lower().replace("-", " ").replace(",", " ").split()
        if token
    }


def _matching_terms(terms: set[str], phrases: list[str]) -> list[str]:
    matches: list[str] = []
    for phrase in phrases:
        phrase_terms = _tokenize(phrase)
        if terms & phrase_terms:
            matches.append(phrase)
    return matches


def _tie_breaker(item: CoffeeItem) -> int:
    return COFFEE_MENU.index(next(menu_item for menu_item in COFFEE_MENU if menu_item["id"] == item["id"]))
