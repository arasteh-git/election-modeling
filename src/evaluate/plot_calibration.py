"""Draw docs/img/calibration_errors.png from the existing calibration.

Run from the repository root:

    python -m src.evaluate.plot_calibration

Plots values computed by src/evaluate/calibration.py (h = 14); it adds no
new model quantities.
"""
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.evaluate.calibration import error_summary, run_calibration

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'docs/img/calibration_errors.png'
HALFLIFE = 14

SURFACE = '#fcfcfb'
INK = '#0b0b0b'
INK_2 = '#52514e'
GRID = '#e4e3df'
CYCLES = [  # (cycle, label, color) in fixed categorical order
    ('2018', '2018', '#2a78d6'),
    ('2020', '2020', '#eb6834'),
    ('2024', 'Texas 2024 (1 race)', '#1baf7a'),
]


def style(ax, title):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc='left', color=INK, fontsize=11, pad=10)
    ax.grid(axis='y', color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)
    ax.set_xlabel('Days before Election Day', color=INK_2, fontsize=9)
    ax.set_xlim(45, 4)  # time runs left to right toward the election
    ax.set_xticks([42, 28, 14, 7])


def plot(errors, output=OUTPUT):
    by_horizon = error_summary(errors, 'horizon')
    by_cycle = error_summary(errors, ['cycle', 'horizon'])

    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4.2), facecolor=SURFACE,
                                      gridspec_kw={'width_ratios': [1.35, 1], 'wspace': 0.32})

    style(left, 'Mean signed error (actual − poll average, D − R points)')
    left.axhline(0, color=INK_2, linewidth=1)
    for cycle, label, color in CYCLES:
        series = by_cycle.loc[cycle, 'mean_error']
        left.plot(series.index, series.values, color=color, linewidth=2, marker='o', markersize=5)
        left.annotate(label, (series.index[0], series.values[0]), xytext=(6, 0),
                      textcoords='offset points', va='center', fontsize=9, color=INK)
    overall = by_horizon['mean_error']
    left.plot(overall.index, overall.values, color=INK, linewidth=2, linestyle='--', marker='o', markersize=5)
    left.annotate('All races', (overall.index[0], overall.values[0]), xytext=(6, 0),
                  textcoords='offset points', va='center', fontsize=9, color=INK)
    left.set_ylim(-8, 2)
    left.set_xlim(45, -6)  # room for direct labels on the right
    left.set_xticks([42, 28, 14, 7])
    left.text(0, -0.2, 'Below zero: polls overstated the Democrat. No bias shift is applied (Decision 016).',
              transform=left.transAxes, fontsize=8, color=INK_2)

    style(right, 'RMSE = σ used for the forecast, all races')
    rmse = by_horizon['rmse']
    right.plot(rmse.index, rmse.values, color=INK, linewidth=2, marker='o', markersize=5)
    for horizon, value in rmse.items():
        right.annotate(f'{value:.2f}', (horizon, value), xytext=(0, 8), textcoords='offset points',
                       ha='center', fontsize=9, color=INK)
    right.set_ylim(0, 9)
    right.text(0, -0.2, 'Races at 42 / 28 / 14 / 7 days: 47 / 50 / 50 / 50. Half-life h = 14.',
               transform=right.transAxes, fontsize=8, color=INK_2)

    fig.suptitle('Senate polling error, 2018 / 2020 / Texas 2024 calibration', x=left.get_position().x0, ha='left',
                 color=INK, fontsize=12, fontweight='bold', y=1.0)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200, bbox_inches='tight', facecolor=SURFACE)
    plt.close(fig)
    return output


if __name__ == '__main__':
    errors, _ = run_calibration(HALFLIFE)
    print(plot(errors))
