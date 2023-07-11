import json
from pathlib import Path

import numpy as np
import pytest
from click.testing import CliRunner
from scipy.stats import spearmanr

from findlike import cli

reference = "Hurricane Irene was a long-lived Cape Verde hurricane during the 2005 Atlantic hurricane season. The storm formed near Cape Verde on August 4 and crossed the Atlantic, turning northward around Bermuda before being absorbed by an extratropical cyclone while situated southeast of Newfoundland. Irene proved to be a difficult storm to forecast due to oscillations in strength. After almost dissipating on August 10, Irene peaked as a Category 2 hurricane on August 16. Irene persisted for 14 days as a tropical system, the longest duration of any storm of the 2005 season. It was the ninth named storm and fourth hurricane of the record-breaking season."
candidates = [
    "In 2023, a sizable earthquake dubbed the 'Goliath Quake' occurred in the Pacific Ring of Fire. The seismic activity started near Japan on July 16 and sent shockwaves across the Pacific, leading to tsunamis in several coastal regions before dissipating on July 24. Forecasting the earthquake's impact was a complex task due to the frequent aftershocks. After a series of smaller tremors, the earthquake peaked with a magnitude of 8.9 on July 20. The quake lasted for 8 days, the longest seismic activity recorded in the 21st century. It was one of the most powerful earthquakes in recent history.",
    "In 2005, a significant weather phenomenon occurred, called Irene. It started near an island in the Atlantic, had a fluctuating strength that perplexed many, and made a significant journey. Mid-August saw it nearly disappear, only to gain more power later. Its two-week presence was quite a record for that year's weather.",
    "The year 2005 saw a remarkable weather event known as Irene. This system started near Cape Verde and took a significant journey across the Atlantic. Its unpredictable behavior made it hard for weather experts to track. Around the middle of August, it was on the brink of disappearance but regained strength to reach Category 2. With a record fortnight-long presence, it was one of the noteworthy occurrences in that year's weather activities.",
    "In 2005, the weather system named Irene made news. Born near Cape Verde, it made a long journey across the Atlantic, took a turn near Bermuda, and eventually merged with another system southeast of Newfoundland. Irene's unpredictable nature and varying strength made it a challenge for forecasters. Around mid-August, it almost vanished but came back stronger to peak as a Category 2 storm on August 16. Its fortnight-long presence as a cyclone set a record that year, marking it as a significant occurrence in the season.",
    "In 2005, a storm that took the spotlight was Irene. This storm was born close to Cape Verde and moved across the Atlantic, adjusting its path near Bermuda. It ended its journey southeast of Newfoundland when another weather system absorbed it. Irene's power varied significantly, making its tracking quite challenging. It almost disappeared in mid-August, only to rise again and peak at Category 2 on August 16. Its two-week duration as a cyclone was noteworthy, as it lasted longer than any other storm in the season, becoming the ninth storm to be named and fourth major system of the year.",
    "In 2005, a noteworthy event was the emergence of a storm named Irene. Its origin was close to Cape Verde, and it traveled across the Atlantic, deviating its path near Bermuda. An extratropical cyclone absorbed it southeast of Newfoundland. Irene had irregular power levels, making it a complex system to track. By August 10, it was on the verge of disappearing but then strengthened to become a Category 2 storm on August 16. It was a tropical cyclone for two weeks, which was longer than any other storm that year, marking it as the fourth significant system and ninth to be named in the season.",
    "In the bustling Atlantic hurricane season of 2005, a notable entity was Irene. Originating near Cape Verde, it journeyed across the Atlantic and made a significant shift near Bermuda. It ended its run southeast of Newfoundland, being absorbed by an extratropical cyclone. Its fluctuating strength made forecasting Irene a challenge. It almost disappeared mid-August, but it reappeared stronger, reaching Category 2 on August 16. The storm persisted as a tropical cyclone for 14 days, longer than any other storm that season, making it the fourth significant storm and ninth one to be named.",
    "During the active 2005 Atlantic hurricane season, a notable storm was Hurricane Irene. It started near Cape Verde and navigated across the Atlantic, making a sharp turn near Bermuda. Eventually, it got integrated into an extratropical cyclone southeast of Newfoundland. Predicting Irene was challenging due to its varying strength. Around August 10, it almost disappeared but ascended to a Category 2 hurricane on August 16. Lasting for 14 days as a tropical cyclone, Irene was the longest enduring storm of the 2005 season, which saw it as the fourth hurricane and ninth named storm.",
    "The 2005 Atlantic hurricane season had a significant long-lasting hurricane called Irene, which began its journey close to Cape Verde. It moved across the Atlantic and swerved northward near Bermuda. Finally, an extratropical cyclone engulfed it while it was southeast of Newfoundland. Forecasters found Irene challenging to predict due to its fluctuating strength. Though it was about to vanish on August 10, it re-emerged as a Category 2 hurricane on August 16. Irene was a tropical cyclone for 14 days, the most extended period for any storm in the 2005 season, making it the fourth hurricane and ninth named storm of the season.",
    "In the 2005 Atlantic hurricane season, Hurricane Irene, originating from Cape Verde, was a hurricane of extended duration. The system initiated near Cape Verde on August 4, progressing across the Atlantic, then veered north near Bermuda, eventually being consumed by an extratropical cyclone while located southeast of Newfoundland. Irene was known for its unpredictable strength changes, making it hard to predict. On August 10, the hurricane nearly vanished but rose again as a Category 2 storm on August 16. With a duration of 14 days as a tropical cyclone, Irene outlasted all other storms of the 2005 season, making it the ninth named storm and fourth hurricane of that remarkable season.",
    "Hurricane Irene was an enduring Cape Verde hurricane in the Atlantic hurricane season of 2005. The hurricane developed close to Cape Verde on the 4th of August, traversed the Atlantic, and took a northerly turn around Bermuda before an extratropical cyclone absorbed it while it was southeast of Newfoundland. Irene's forecast was challenging due to its fluctuating intensity. On August 10, it nearly dissipated but later reached its peak as a Category 2 hurricane on August 16. The hurricane remained a tropical system for 14 days, which was the longest for any storm during that season. It was the season's ninth named storm and the fourth hurricane in an extraordinarily active season.",
]
scores = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]

std_args = ["-F", "json", "-s", "-h", "-m", len(scores)]


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def create_directory(tmp_path):
    for i, candidate in enumerate(candidates):
        file = tmp_path / f"file_{i:02d}.txt"
        file.write_text(candidate)
    reference_file = tmp_path / "reference.txt"
    reference_file.write_text(reference)
    return str(tmp_path)


@pytest.fixture
def create_directory_with_non_text(tmp_path):
    for i, candidate in enumerate(candidates):
        file = tmp_path / f"file_{i:02d}.000"
        file.write_text(candidate)
    reference_file = tmp_path / "reference.000"
    reference_file.write_text(reference)
    return str(tmp_path)


@pytest.mark.parametrize("format", cli.FORMATTER_CLASSES.keys())
def test_formats(runner, create_directory, format):
    reference_path = Path(create_directory) / "reference.txt"
    result = runner.invoke(
        cli.cli,
        [str(reference_path), "-d", create_directory, "-F", format, *std_args],
    )
    assert result.exit_code == 0

    json_data = json.loads(result.output.strip())
    assert len(json_data) == len(scores)


@pytest.mark.parametrize("algorithm", cli.ALGORITHM_CLASSES.keys())
def test_algorithms(runner, create_directory, algorithm):
    reference_path = Path(create_directory) / "reference.txt"
    result = runner.invoke(
        cli.cli,
        [
            str(reference_path),
            "-d",
            create_directory,
            "-a",
            algorithm,
            *std_args,
        ],
    )
    json_data = json.loads(result.output.strip())
    pairs = [(item["score"], item["target"]) for item in json_data]
    sorted_pairs = sorted(pairs, key=lambda x: x[1])[::-1]
    output_scores = [float(x[0]) for x in sorted_pairs]
    corr = round(spearmanr(output_scores, scores)[0], 2)
    assert corr >= 0.95


def test_other_extensions(runner, create_directory_with_non_text):
    reference_path = Path(create_directory_with_non_text) / "reference.000"
    result = runner.invoke(
        cli.cli,
        [
            str(reference_path),
            "-d",
            create_directory_with_non_text,
            "-f",
            "*.000",
            *std_args,
        ],
    )
    assert "000" in result.output.strip()


@pytest.mark.parametrize("algorithm", cli.ALGORITHM_CLASSES.keys())
def test_query(runner, create_directory, algorithm):
    result = runner.invoke(
        cli.cli,
        [
            "-q",
            reference,
            "-d",
            create_directory,
            "-a",
            algorithm,
            *std_args,
        ],
    )
    json_data = json.loads(result.output.strip())

    output_scores = [float(x["score"]) for x in json_data]
    assert spearmanr(output_scores, scores)[0] > 0.99
