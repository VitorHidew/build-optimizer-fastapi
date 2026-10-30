import pytest

from app.data import load_catalog
from app.engine import evaluate, optimize
from app.models import BuildRequest


def test_catalog_contains_only_fictional_examples():
    catalog = load_catalog()
    assert len(catalog.equipment) == 13
    assert len(catalog.targets) == 3


def test_evaluate_returns_explainable_score():
    result = evaluate(
        load_catalog(),
        BuildRequest(
            weapon_id="w_lamina_alvorada",
            armor_ids=["a_elmo_vigia", "a_peitoral_rocha"],
            target_id="t_fera_cinzenta",
        ),
    )
    assert result.estimated_damage > 0
    assert result.total_defense == pytest.approx(102.82)
    assert len(result.explanation) == 4


def test_duplicate_armor_slot_is_rejected():
    with pytest.raises(ValueError, match="slot head"):
        evaluate(
            load_catalog(),
            BuildRequest(
                weapon_id="w_lamina_alvorada",
                armor_ids=["a_elmo_vigia", "a_capuz_faisca"],
                target_id="t_fera_cinzenta",
            ),
        )


def test_optimizer_selects_complete_build():
    result = optimize(load_catalog(), "t_serpe_cristal")
    assert len(result.armor) == 5
    assert result.score > 0
