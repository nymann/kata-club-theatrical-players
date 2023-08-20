import math
from dataclasses import dataclass
from typing import Any


@dataclass
class Play:
    name: str
    type: str


@dataclass
class Performance:
    play: Play
    audience: int


def statement(invoice: dict[str, Any], plays: dict[str, Any]) -> str:
    performances: list[Performance] = []
    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        play = Play(name=play["name"], type=play["type"])
        performances.append(Performance(play=play, audience=perf["audience"]))

    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount: float) -> str:
        return f"${amount:0,.2f}"

    for perf in performances:
        play = perf.play
        this_amount = price_for_performance(perf)
        result += f" {play.name}: {format_as_dollars(this_amount/100)} ({perf.audience} seats)\n"
        total_amount += this_amount

        volume_credits += max(perf.audience - 30, 0)
        if "comedy" == play.type:
            volume_credits += math.floor(perf.audience / 5)

    result += f"Amount owed is {format_as_dollars(total_amount/100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result


def price_for_performance(performance: Performance) -> float:
    play = performance.play

    if play.type == "tragedy":
        return price_for_tragedy(performance.audience)
    if play.type == "comedy":
        return price_for_comedy(performance.audience)
    raise ValueError(f"unknown type: {play.type}")


def price_for_tragedy(audience: int) -> float:
    this_amount = 40000
    if audience > 30:
        this_amount += 1000 * (audience - 30)
    return this_amount


def price_for_comedy(audience: int) -> float:
    this_amount = 30000
    if audience > 20:
        this_amount += 10000 + 500 * (audience - 20)
    return this_amount + 300 * audience
