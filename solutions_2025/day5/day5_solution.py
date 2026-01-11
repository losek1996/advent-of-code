from typing import TypeAlias

from pydantic import BaseModel


Id: TypeAlias = int
RANGE_SIGN = "-"


class FreshIngredientsRange(BaseModel):
    min: Id
    max: Id


class Ingredients(BaseModel):
    fresh_ingredients_ranges: list[FreshIngredientsRange]
    available_ingredients_ids: list[Id]


def parse_data(data: list[str]) -> Ingredients:
    fresh_ingredients_ranges = []
    available_ingredients_ids = []
    for row in data:
        if RANGE_SIGN in row:
            min_range, max_range = row.split(RANGE_SIGN)
            fresh_ingredients_ranges.append(
                FreshIngredientsRange(
                    min=Id(min_range),
                    max=Id(max_range),
                )
            )
        elif row:
            available_ingredients_ids.append(Id(row))

    return Ingredients(
        fresh_ingredients_ranges=fresh_ingredients_ranges,
        available_ingredients_ids=available_ingredients_ids,
    )


def count_available_and_fresh_ingredients(ingredients: Ingredients) -> int:
    return len(get_fresh_available_ingredients(ingredients))


def count_fresh_ingredients(ingredients: Ingredients) -> int:
    fresh_ingredients_ranges = sorted(
        ingredients.fresh_ingredients_ranges, key=lambda x: (x.min, -x.max)
    )
    ranges_without_overlaps = [fresh_ingredients_ranges[0]]
    for fresh_ingredients_range in fresh_ingredients_ranges[1:]:
        previous_fresh_ingredients_range = ranges_without_overlaps[-1]
        if fresh_ingredients_range.min <= previous_fresh_ingredients_range.max:
            ranges_without_overlaps[-1] = FreshIngredientsRange(
                min=previous_fresh_ingredients_range.min,
                max=max(
                    previous_fresh_ingredients_range.max, fresh_ingredients_range.max
                ),
            )
        else:
            ranges_without_overlaps.append(fresh_ingredients_range)

    return sum(r.max - r.min + 1 for r in ranges_without_overlaps)


def get_fresh_available_ingredients(ingredients: Ingredients) -> list[Id]:
    fresh_available_ingredients_ids = []
    for ingredient_id in ingredients.available_ingredients_ids:
        for fresh_ingredients_range in ingredients.fresh_ingredients_ranges:
            if (
                fresh_ingredients_range.min
                <= ingredient_id
                <= fresh_ingredients_range.max
            ):
                fresh_available_ingredients_ids.append(ingredient_id)
                break

    return fresh_available_ingredients_ids
