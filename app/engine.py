from itertools import product

from app.models import BuildRequest, BuildResult, Catalog, Equipment, Target


def _select(catalog: Catalog, request: BuildRequest) -> tuple[Equipment, list[Equipment], Target]:
    equipment = {item.id: item for item in catalog.equipment}
    targets = {item.id: item for item in catalog.targets}

    weapon = equipment.get(request.weapon_id)
    if not weapon or weapon.kind != "weapon":
        raise ValueError("Arma fictícia não encontrada.")

    armor: list[Equipment] = []
    used_slots: set[str] = set()
    for item_id in request.armor_ids:
        item = equipment.get(item_id)
        if not item or item.kind != "armor":
            raise ValueError(f"Armadura fictícia não encontrada: {item_id}")
        if item.slot in used_slots:
            raise ValueError(f"Mais de uma armadura selecionada para o slot {item.slot}.")
        used_slots.add(item.slot)
        armor.append(item)

    target = targets.get(request.target_id)
    if not target:
        raise ValueError("Alvo fictício não encontrado.")
    return weapon, armor, target


def evaluate(catalog: Catalog, request: BuildRequest) -> BuildResult:
    weapon, armor, target = _select(catalog, request)
    skills: dict[str, int] = {}
    for item in [weapon, *armor]:
        for skill, level in item.skills.items():
            skills[skill] = skills.get(skill, 0) + level

    attack_bonus = 1 + min(skills.get("ímpeto", 0), 5) * 0.03
    affinity_factor = 1 + (weapon.affinity / 100) * 0.25
    physical = weapon.attack * attack_bonus * affinity_factor * (1 - target.physical_resistance)
    elemental = weapon.element * (1 + min(skills.get("foco elemental", 0), 5) * 0.04)
    elemental *= 1 - target.elemental_resistance
    damage = max(0, physical + elemental)
    defense = sum(item.defense for item in armor)
    defense *= 1 + min(skills.get("guarda", 0), 5) * 0.02
    score = damage + defense * 0.2

    explanation = [
        f"Dano físico considera ataque, afinidade e resistência de {target.name}.",
        "Dano elemental é calculado separadamente e somado ao dano físico.",
        "A pontuação combina dano estimado com 20% da defesa total.",
        "Os valores são fictícios e servem apenas para demonstrar o algoritmo.",
    ]
    return BuildResult(
        weapon=weapon.name,
        armor=[item.name for item in armor],
        target=target.name,
        estimated_damage=round(damage, 2),
        total_defense=round(defense, 2),
        score=round(score, 2),
        skills=skills,
        explanation=explanation,
    )


def optimize(catalog: Catalog, target_id: str) -> BuildResult:
    weapons = [item for item in catalog.equipment if item.kind == "weapon"]
    armor_by_slot = {
        slot: [item for item in catalog.equipment if item.kind == "armor" and item.slot == slot]
        for slot in ("head", "chest", "arms", "waist", "legs")
    }
    if not weapons or any(not items for items in armor_by_slot.values()):
        raise ValueError("O catálogo fictício não possui opções suficientes para otimização.")

    best: BuildResult | None = None
    for weapon in weapons:
        for armor in product(*(armor_by_slot[slot] for slot in armor_by_slot)):
            result = evaluate(
                catalog,
                BuildRequest(weapon_id=weapon.id, armor_ids=[item.id for item in armor], target_id=target_id),
            )
            if best is None or result.score > best.score:
                best = result
    assert best is not None
    return best
