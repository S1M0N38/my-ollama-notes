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

- Command line interface: in a new terminal run `./ollama run ...`
- [REST API](https://github.com/ollama/ollama/blob/main/docs/api.md): perform HTTP requests to `localhost:11434`
- [ollama-python](https://github.com/ollama/ollama-python): Ollama Python library's API, a wrapper around the REST API

## Notes

In order to have fast inference, the models must fit into the GPU memory. (The underlying inference engine is [llama.cpp](https://github.com/ggerganov/llama.cpp), which is able to run entire/partial models on CPU as well, but it is orders of magnitude slower.)

So the most limiting factor in the choice of model is the amount of VRAM available on the GPU.

- **Small** (\< 13B)
  - [llama3:8b](https://ollama.com/library/llama3)
  - [gemma:7b](https://ollama.com/library/gemma)
  - [mistral:7b](https://ollama.com/library/mistral)
  - [wizardlm2:7b](https://ollama.com/library/wizardlm2)
  - ...
- **Medium** (13B - 70B)
  - [llama3:70b](https://ollama.com/library/llama3)
  - [command-r:35b](https://ollama.com/library/command-r)
  - [mixtral:8x7b](https://ollama.com/library/mixtral)
  - ...
- **Large** (>70B)
  - [command-r-plus:104b](https://ollama.com/library/command-r-plus)
  - [mixtral:8x22b](https://ollama.com/library/mixtral)
  - [wizardlm2:8x22b](https://ollama.com/library/wizardlm2)
  - ...

**MoE vs Dense**: Some of the models express the number of parameters as a multiplication (e.g. `mixtral:8x7b`). These models are referred to as Mixture of Experts (MoE) and at inference time, a routing network is used to select a subset of the experts to run (e.g. 2 out of 8) for each token. This effectively reduces the number of parameters used in each forward pass, making token generation faster with minimal loss in performance compared to dense models.

**Quantization**: To run reasonably large models on a single GPU, the models are quantized with various precisions and methods. When pulling models with a simple tag (e.g. `ollama pull mistral`), it defaults to pulling the model with 4-bit quantization. See the Ollama website for all the available tags for each model.

**Model Format**: Under the hood, Ollama makes use of llama.cpp which requires its custom format for model weights and specifications: `.gguf`. The tags follow the `gguf` naming scheme.

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

How many tokens per second can the model process when given a prompt?

![Plot prompt eval speed](https://github.com/S1M0N38/my-ollama-notes/blob/main/benchmarks/plot_prompt_eval.svg?raw=true)
