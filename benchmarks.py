import ollama
import csv


messages = [
    {
        "role": "user",
        "content": "Why is the sky blue?",
    }
]

models = [
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


# Open the CSV file in write mode
with open("benchmarks.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(
        [
            "model",
            "eval speed [tokens/s]",
            "total duration [ms]",
            "prompt duration [ms]",
            "eval duration [ms]",
            "eval count [tokens]",
        ]
    )

    # Iterate over the models
    for model in models:
        # ollama.pull(model)
        response = ollama.chat(
            model=model,
            messages=messages,
        )

        assert response["done"]

        model_name = response["model"]
        total_duration = response["total_duration"] / 1e9
        prompt_duration = response["prompt_eval_duration"] / 1e9
        eval_count = response["eval_count"]
        eval_duration = response["eval_duration"] / 1e9
        eval_speed = eval_count / eval_duration

        writer.writerow(
            [
                model_name,
                eval_speed,
                total_duration,
                prompt_duration,
                eval_duration,
                eval_count,
            ]
        )
