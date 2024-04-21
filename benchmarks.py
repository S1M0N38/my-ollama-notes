import ollama
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path


MESSAGE_LIMIT = None

MODELS = [
    # Small
    "llama3:8b-instruct-q4_0",
    "gemma:7b-instruct-v1.1-q4_0",
    "mistral:7b-instruct-v0.2-q4_0",
    "wizardlm2:7b-q4_0",
    # Medium
    "llama3:70b-instruct-q4_0",
    "command-r:35b-v0.1-q4_0",
    "mixtral:8x7b-instruct-v0.1-q4_0",
    # Large
    # add here large models to test ...
]

AVAILABLE_MODELS = [model["model"] for model in ollama.list()["models"]]
[ollama.pull(model) for model in MODELS if model not in AVAILABLE_MODELS]

COLUMNS = [
    "model",
    "total_duration",
    "load_duration",
    "prompt_eval_count",
    "prompt_eval_duration",
    "eval_count",
    "eval_duration",
]


BENCHMARKS_PATH = Path("benchmarks")
EVAL_PATH = BENCHMARKS_PATH / "benchmarks_eval.csv"
PROMPT_EVAL_PATH = BENCHMARKS_PATH / "benchmarks_prompt_eval.csv"

with open(BENCHMARKS_PATH / "messages.json") as f:
    MESSAGES = json.load(f)


def benchmark_eval(model: str, df: pd.DataFrame) -> None:
    messages = MESSAGES["eval_messages"][:MESSAGE_LIMIT]
    for message in tqdm(messages):
        df.loc[len(df)] = ollama.chat(
            model=model,
            messages=[message],
        )


def benchmark_prompt_eval(model: str, df: pd.DataFrame) -> None:
    messages = MESSAGES["prompt_eval_messages"][:MESSAGE_LIMIT]
    for message in tqdm(messages):
        df.loc[len(df)] = ollama.chat(
            model=model,
            messages=[message],
        )


def benchmarks() -> None:
    # Eval Benchmark
    if not EVAL_PATH.exists():
        eval_df = pd.DataFrame(columns=COLUMNS)
        for model in MODELS:
            benchmark_eval(model, eval_df)
            eval_df.to_csv(EVAL_PATH, index=False)

    # Prompt Eval Benchmark
    if not PROMPT_EVAL_PATH.exists():
        prompt_eval_df = pd.DataFrame(columns=COLUMNS)
        for model in MODELS:
            benchmark_prompt_eval(model, prompt_eval_df)
            prompt_eval_df.to_csv(PROMPT_EVAL_PATH, index=False)


def plot(df: pd.DataFrame, plot_path: Path) -> None:
    # Set the theme and color palette
    sns.set_theme(style="whitegrid")
    gray_color = "#787878"  # A mid-tone gray

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(8, len(MODELS) * 0.6))
    sns.barplot(
        x="speed",
        y="model",
        data=df,
        ax=ax,
        hue="model",
        edgecolor=gray_color,
    )

    # Set labels
    ax.set_xlabel("tokens/s", color=gray_color)
    ax.set_ylabel("", color=gray_color)

    # Set tick parameters
    ax.tick_params(axis="x", colors=gray_color)
    ax.tick_params(axis="y", colors=gray_color)

    # Set the background color of the plot to None (transparent)
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Remove axes' frames for aesthetics
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Customize grid lines to the same shade of gray
    ax.xaxis.grid(True, color=gray_color, linestyle="-", linewidth=0.75)
    ax.yaxis.grid(False)

    # Save the plot with a transparent background
    plt.savefig(
        plot_path,
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
    )


def plots() -> None:
    # Eval Plot
    df = pd.read_csv(EVAL_PATH)
    df["speed"] = df["eval_count"] / df["eval_duration"] * 1e9
    plot(df, BENCHMARKS_PATH / "plot_eval.svg")

    # Eval Plot
    df = pd.read_csv(PROMPT_EVAL_PATH)
    df["speed"] = df["prompt_eval_count"] / df["prompt_eval_duration"] * 1e9
    plot(df, BENCHMARKS_PATH / "plot_prompt_eval.svg")


def main() -> None:
    benchmarks()
    plots()


if __name__ == "__main__":
    main()
