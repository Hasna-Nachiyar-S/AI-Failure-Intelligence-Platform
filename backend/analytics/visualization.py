"""Small reusable Matplotlib helpers for exploratory dataset inspection.

These functions are optional research utilities. The production dashboard
renders charts in React from authenticated analysis-history data.
"""

import matplotlib.pyplot as plt


def _require_column(df, column):
    if column not in df.columns:
        raise KeyError(f"Column {column!r} is not present in the dataset.")


def plot_category(df, column):
    """Plot category counts for any available dataset column."""
    _require_column(df, column)
    ax = df[column].value_counts(dropna=False).plot(kind="bar")
    ax.set_title(column)
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.show()
    return ax


def plot_pie(df, column):
    """Plot category proportions without assuming a domain-specific column."""
    _require_column(df, column)
    ax = df[column].value_counts(dropna=False).plot(
        kind="pie",
        autopct="%1.1f%%",
    )
    ax.set_title(column)
    ax.set_ylabel("")
    plt.tight_layout()
    plt.show()
    return ax
