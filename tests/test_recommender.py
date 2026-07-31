from cafe_mcp_server.recommender import explain_recommendation, list_menu, recommend_coffee


def test_list_menu_returns_static_items():
    menu = list_menu()

    assert len(menu) >= 5
    assert {"id", "name", "style", "milk", "caffeine", "flavor_notes"} <= set(menu[0])


def test_recommend_coffee_prefers_cold_black_high_caffeine():
    recommendation = recommend_coffee(
        mood="smooth iced coffee",
        prefer_milk=False,
        caffeine="high",
        temperature="cold",
    )

    assert recommendation["id"] == "cold_brew"
    assert "matches milk preference" in recommendation["reasons"]


def test_recommend_coffee_prefers_low_caffeine_milk_drink():
    recommendation = recommend_coffee(
        mood="evening gentle creamy",
        prefer_milk=True,
        caffeine="low",
        temperature="hot",
    )

    assert recommendation["id"] == "decaf_latte"
    assert recommendation["caffeine"] == "low"


def test_recommend_coffee_ignores_unknown_choices():
    recommendation = recommend_coffee(caffeine="maximum", temperature="room-temp")

    assert recommendation["id"] == "espresso"
    assert recommendation["score"] == 0


def test_explain_recommendation_for_unknown_id_lists_available_ids():
    explanation = explain_recommendation("unknown")

    assert "Unknown coffee id" in explanation
    assert "espresso" in explanation


def test_explain_recommendation_mentions_top_match():
    explanation = explain_recommendation(
        "cold_brew",
        mood="smooth iced",
        prefer_milk=False,
        caffeine="high",
        temperature="cold",
    )

    assert "Cold Brew" in explanation
    assert "top match" in explanation
