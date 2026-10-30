from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Equipment(BaseModel):
    id: str
    name: str
    kind: Literal["weapon", "armor"]
    slot: Literal["weapon", "head", "chest", "arms", "waist", "legs"]
    attack: float = Field(default=0, ge=0)
    defense: float = Field(default=0, ge=0)
    affinity: float = Field(default=0, ge=-100, le=100)
    element: float = Field(default=0, ge=0)
    skills: dict[str, int] = Field(default_factory=dict)


class Target(BaseModel):
    id: str
    name: str
    physical_resistance: float = Field(ge=0, le=0.9)
    elemental_resistance: float = Field(ge=0, le=0.9)


class Catalog(BaseModel):
    equipment: list[Equipment]
    targets: list[Target]


class BuildRequest(BaseModel):
    weapon_id: str
    armor_ids: list[str] = Field(default_factory=list, max_length=5)
    target_id: str

    @field_validator("armor_ids")
    @classmethod
    def unique_armor(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("Cada armadura deve aparecer apenas uma vez.")
        return value


class BuildResult(BaseModel):
    weapon: str
    armor: list[str]
    target: str
    estimated_damage: float
    total_defense: float
    score: float
    skills: dict[str, int]
    explanation: list[str]
