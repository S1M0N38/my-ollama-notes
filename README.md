<div align="center">

# My ollama notes

![Figure from Ollama blog post about embeddings](https://github.com/S1M0N38/my-ollama-notes/blob/main/ollama-taking-notes.svg?raw=true "Figure from ollama.com/blog/embedding-models")

</div>

[Ollama](https://ollama.com/) is one of the simplest ways to run Large Language Models (LLMs) on your hardware.

Follow the installation guide on the official website or, if you are on Linux, simply download the single binary and make it executable:

```bash
curl -L https://ollama.com/download/ollama-linux-amd64 -o ollama
curl +x ollama
```

Then start the Ollama server (and keep it running in the background):

```bash
./ollama serve
```

Now you can interact with the Ollama server in various ways:

- [Command line interface](https://github.com/ollama/ollama/blob/main/README.md#quickstart): In a new terminal, run ./ollama run --help
- [REST API](https://github.com/ollama/ollama/blob/main/docs/api.md): Perform HTTP requests to `localhost:11434`
- [ollama-python](https://github.com/ollama/ollama-python): Ollama's Python library API, a wrapper around the REST API
- [Open WebUI](https://docs.openwebui.com/): A ChatGPT-like web interface for Ollama

## Notes

In order to have fast inference, the models must fit into the GPU memory. (The underlying inference engine is [llama.cpp](https://github.com/ggerganov/llama.cpp), which is able to run entire/partial models on CPU as well, but it is orders of magnitude slower.)

**Size**: The most limiting factor in the choice of model is the amount of VRAM available on the GPU. For practical purposes, the models can be categorized into three groups based on the number of parameters. *Small* models can be run on a single consumer GPU (possibly locally on a laptop). *Medium* models usually require dedicated hardware with a decent amount of VRAM (e.g. > 40 GB). *Large* models require high-end GPU/s (80 GB or more combined VRAM). We assume the models are quantized to 4-bit precision (see later).

- *Small* (\< 13B)
  - [llama3:8b](https://ollama.com/library/llama3)
  - [gemma:7b](https://ollama.com/library/gemma)
  - [mistral:7b](https://ollama.com/library/mistral)
  - [wizardlm2:7b](https://ollama.com/library/wizardlm2)
  - ...
- *Medium* (13B - 70B)
  - [llama3:70b](https://ollama.com/library/llama3)
  - [command-r:35b](https://ollama.com/library/command-r)
  - [mixtral:8x7b](https://ollama.com/library/mixtral)
  - ...
- *Large* (>70B)
  - [command-r-plus:104b](https://ollama.com/library/command-r-plus)
  - [mixtral:8x22b](https://ollama.com/library/mixtral)
  - [wizardlm2:8x22b](https://ollama.com/library/wizardlm2)
  - ...

**MoE vs Dense**: Some of the models express the number of parameters as a multiplication (e.g. `mixtral:8x7b`). These models are referred to as Mixture of Experts (MoE) and at inference time, a routing network is used to select a subset of the experts to run (e.g. 2 out of 8) for each token. This effectively reduces the number of parameters used in each forward pass, making token generation faster with minimal loss in performance compared to dense models.

**Quantization**: To run reasonably large models on a single GPU, the models are quantized with various precisions and methods. When pulling models with a simple tag (e.g. `ollama pull mistral`), it defaults to pulling the model with 4-bit quantization. See the Ollama website for all the available tags for each model.

**Model Format**: Under the hood, Ollama makes use of llama.cpp which requires its custom format for model weights and specifications: `.gguf`. The tags follow the `gguf` naming scheme.

**License**: Various models are released under different licenses. For example, models from Mistral are released under the "Apache 2.0" license, a very permissive license. The models from the Command-R series are released under the "CC-BY-NC" license, which is more restrictive, limiting the use of the models for commercial purposes (unless you purchase a commercial license).

**Capabilities**: Different models excel at different tasks: code generation, multi-language understanding, reasoning capabilities, RAG performance, tool usage, and context length, just to name a few. Some respond in a more casual and engaging manner, while others are more formal and informative.

## Benchmarks

Benchmarking model performance and capabilities is quite challenging. In addition to the usual metrics on popular datasets (MMLU, GPQA, HumanEval, GSM-8K, etc.), the [chat bot arena](https://chat.lmsys.org/?leaderboard) provides an ELO-based ranking based on human evaluations of the generated text. Another resource for LLM public perception is the [LocalLLaMa](https://www.reddit.com/r/LocalLLaMA/) subreddit.

Below are some speed benchmarks for several base models available on Ollama. The plots were produced by running `benchmarks.py` on a machine equipped with:

- **CPU**: AMD EPYC-Rome (14 cores)
- **GPU**: NVIDIA A6000 (48 GB)
- **RAM**: 92 GB

### Eval Speed

How many tokens per second can the model generate in an autoregressive setting?

![Plot eval speed](https://github.com/S1M0N38/my-ollama-notes/blob/main/benchmarks/plot_eval.svg?raw=true)

### Prompt Eval Speed

How fast (in tokens/s) can the model process a given prompt?

![Plot prompt eval speed](https://github.com/S1M0N38/my-ollama-notes/blob/main/benchmarks/plot_prompt_eval.svg?raw=true)

## Model Choice

Even though the model zoo can be overwhelming with new models released regularly, finding a good model for your use case can be broken down into a few steps:

1. **Technical Limitations**: It must run at the required speed (size, MoE vs Dense).
1. **License Limitations**: It can be used for the intended purpose (license).
1. **Capabilities**: It should be good at the intended task (capabilities).

Once you have identified a model or models that meet your requirements, you can further "optimize" your choice by considering the following:

- **Quantization**: Move to a less quantized model if you have spare VRAM (while keeping an eye on the speed).
- **Fine-tuned version**: The LLM community often releases fine-tuned versions of the base models for specific tasks (e.g., uncensored models, improved prompt following capabilities, etc.).
- **Inference engine**: Ollama is easy to start with, but there exist more performant inference engines than llama.cpp (exllamav2, vllm, etc.). See [here](https://www.reddit.com/r/LocalLLaMA/comments/1anb2fz/guide_to_choosing_quants_and_engines/) and [here](https://www.reddit.com/r/LocalLLaMA/comments/1c9mn1n/whats_the_fastest_local_inference_engine_right/).
