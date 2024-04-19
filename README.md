# My ollama notes

![Ollama taking notes](https://github.com/S1M0N38/my-ollama-notes/blob/main/ollama-taking-notes.jpg?raw=true)

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
  - `llama3:8b`
  - `gemma:7b`
  - `mistral:7b`
  - `wizardlm2:7b`
  - ...
- **Medium** (13B - 70B)
  - `llama3:70b`
  - `command-r:35b`
  - `mixtral:8x7b`
  - ...
- **Large** (>70B)
  - `command-r-plus:104b`
  - `mixtral:8x22b`
  - `wizardlm2:8x22b`
  - ...

**MoE vs Dense**: Some of the models express the number of parameters as a multiplication (e.g. `mixtral:8x7b`). These models are referred to as Mixture of Experts (MoE) and at inference time, a routing network is used to select a subset of the experts to run (e.g. 2 out of 8) for each token. This effectively reduces the number of parameters used in each forward pass, making token generation faster with minimal loss in performance compared to dense models.

**Quantization**: To run reasonably large models on a single GPU, the models are quantized with various precisions and methods. When pulling models with a simple tag (e.g. `ollama pull mistral`), it defaults to pulling the model with 4-bit quantization. See the Ollama website for all the available tags for each model.

**Model Format**: Under the hood, Ollama makes use of llama.cpp which requires its custom format for model weights and specifications: `.gguf`. The tags follow the `gguf` naming scheme.

## Benchmarks

The following table was produced by running `benchmarks.py` on a machine with:

- **CPU**: AMD EPYC-Rome (14 cores)
- **GPU**: NVIDIA A6000 (48 GB)
- **RAM**: 92 GB

| model                           | eval speed \[tokens/s\] | total duration \[ms\] | prompt duration \[ms\] | eval duration \[ms\] | eval count \[tokens\] |
| ------------------------------- | ----------------------: | --------------------: | ---------------------: | -------------------: | --------------------: |
| llama3:8b-instruct-q4_0         |                 82.5672 |              4.792919 |               0.031767 |             4.626534 |                   382 |
| gemma:7b-instruct-v1.1-q4_0     |                 79.8138 |             15.619711 |               0.084908 |             3.119762 |                   249 |
| mistral:7b-instruct-v0.2-q4_0   |                102.1478 |             10.525652 |               0.078379 |             1.488040 |                   152 |
| wizardlm2:7b-q4_0               |                 99.5369 |             14.505660 |               0.080251 |             5.867169 |                   584 |
| llama3:70b-instruct-q4_0        |                 14.8496 |             83.692734 |               0.422259 |            26.869336 |                   399 |
| command-r:35b-v0.1-q4_0         |                 26.3358 |             48.755652 |               0.208876 |            11.239446 |                   296 |
| mixtral:8x7b-instruct-v0.1-q4_0 |                 50.0879 |             50.029504 |               0.127328 |             4.532030 |                   227 |
