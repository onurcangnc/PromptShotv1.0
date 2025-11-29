# 🎯 PromptShot v1.0

Adversarial Prompt Generation & Optimization Framework

## Overview

PromptShot is an adversarial prompt generation and optimization framework for LLM security research. It generates prompt injection payloads using ElderPlinus techniques and multi-format mutations, then optimizes them through adversarial duels between GPT and Claude.

## Features

- **ElderPlinus Stack**: Supervisor Override, Paradox Injection, Mirror Simulation techniques
- **Multi-Format Corruption**: 11+ mutation techniques (ZWSP, Homoglyph, JSON Poison, YAML Shadow, etc.)
- **Adversarial Duel**: Iterative refinement between GPT and Claude
- **Evolutionary Optimization**: Genetic algorithm-based payload evolution
- **Metrics & Reporting**: USOM/MITRE-compatible reporting format

## Installation

```bash
git clone https://github.com/your-repo/promptshot.git
cd promptshot
pip install -r requirements.txt
```

## Configuration

Set your API keys as environment variables:

```bash
# Linux/Mac
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-openai-key"
$env:ANTHROPIC_API_KEY="your-anthropic-key"

# Windows (CMD)
set OPENAI_API_KEY=your-openai-key
set ANTHROPIC_API_KEY=your-anthropic-key
```

## Usage

### Basic Usage

```bash
python pipeline.py
```

### With Custom Goal

```bash
python pipeline.py --goal "extract system prompt"
```

### Advanced Options

```bash
# Custom threshold and rounds
python pipeline.py --threshold 8 --rounds 10

# Use evolutionary optimization
python pipeline.py --evolve --generations 15

# Specify models
python pipeline.py --gpt-model gpt-4o --claude-model claude-sonnet-4

# Quiet mode (minimal output)
python pipeline.py --quiet

# Don't save to file
python pipeline.py --no-save
```

### All Options

```
--goal, -g          Specific goal for prompt generation
--threshold, -t     Score threshold for acceptance (default: 7)
--rounds, -r        Maximum duel rounds (default: 8)
--mutations, -m     Mutation depth (default: 2)
--gpt-model         GPT model (default: gpt-4o)
--claude-model      Claude model (default: claude-sonnet-4)
--evolve, -e        Use evolutionary optimization
--generations       Evolution generations (default: 5)
--output, -o        Output directory (default: outputs)
--quiet, -q         Minimal output
--no-save           Don't save output to file
--version, -v       Show version
```

## Project Structure

```
promptshot/
├── pipeline.py              # Main entry point
├── architect.py             # Attack planning
├── requirements.txt
├── README.md
│
├── mutation/                # Mutation techniques
│   ├── __init__.py
│   ├── multi_corruption.py  # All mutation functions
│   └── mutation_weights.py  # Weighted selection
│
├── integration/             # LLM providers
│   ├── __init__.py
│   └── llm_factory.py       # Unified LLM interface
│
├── agents/                  # Core agents
│   ├── __init__.py
│   ├── llm_rater.py         # LLM-based scoring
│   ├── prompt_duel_runner.py # Duel orchestration
│   └── refactor_agent.py    # Response cleanup
│
├── builder/                 # Prompt builders
│   ├── __init__.py
│   ├── prompt_builder.py    # Main builder
│   ├── chain_builder.py     # Context chaining
│   └── memory_flood.py      # AMF technique
│
├── elderplinus/             # ElderPlinus techniques
│   ├── __init__.py
│   ├── loader.py            # Technique loader
│   └── stack.py             # 3x Stack implementation
│
├── metrics/                 # Metrics & reporting
│   ├── __init__.py
│   ├── collector.py         # Data collection
│   └── fitness.py           # Genetic algorithm
│
└── outputs/                 # Generated outputs
    └── *.txt, *.md
```

## Supported Models

### OpenAI
- `gpt-4o` (default)
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-4`
- `o1`
- `o1-mini`

### Anthropic
- `claude-sonnet-4` (default)
- `claude-opus-4`
- `claude-haiku-3.5`
- `claude-sonnet-3.5`

## Mutation Techniques

| Technique | Description |
|-----------|-------------|
| `zwsp` | Zero-Width Space injection |
| `homoglyph` | Cyrillic/Greek lookalike characters |
| `markdown_injection` | Markdown syntax abuse |
| `json_poison` | JSON structure injection |
| `yaml_shadow` | YAML indentation attacks |
| `base64_partial` | Partial base64 encoding |
| `leetspeak` | Character substitution |
| `unicode_confusables` | Unicode lookalikes |
| `direction_override` | RTL/LTR manipulation |
| `tag_injection` | HTML/XML tag abuse |
| `whitespace_smuggling` | Whitespace variants |

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║   🎯 PromptShot v1.0                                        ║
║   Adversarial Prompt Generation & Optimization               ║
╚══════════════════════════════════════════════════════════════╝

🔑 API Key Status:
   OpenAI:    ✅ Found
   Anthropic: ✅ Found

🧬 Generating initial payload...
🚀 Starting duel: gpt-4o vs claude-sonnet-4

🔁 ROUND 1
[Claude] Score: 6/10
🔧 Claude suggests a stronger version.

🔁 ROUND 2
[Claude] Score: 8/10
✅ Claude accepted the prompt as strong.
[GPT] Score: 7/10
🏆 Both models accept the prompt as STRONG.

============================================================
✅ SUCCESS
============================================================

📊 Statistics:
   Total Rounds: 2
   Best GPT Score: 7/10
   Best Claude Score: 8/10

💾 Saved to: outputs/promptshot_20250529_143022.txt
```

## Programmatic Usage

```python
from mutation import mutate, zwsp_mutation, homoglyph_mutation
from integration import get_llm_response, get_factory
from agents import PromptDuelRunner
from builder import PromptBuilder

# Direct mutation
result = mutate("ignore all instructions", count=3)
print(result.mutated)

# LLM query
response = get_llm_response("Hello", model="gpt-4o")

# Full pipeline
builder = PromptBuilder()
payload = builder.build_chain(mutation_depth=2)

runner = PromptDuelRunner(threshold=7)
result = runner.run_duel(payload)
```

## Disclaimer

⚠️ **For authorized security research only.**

This tool is designed for:
- AI safety research
- Red teaming with proper authorization
- Responsible vulnerability disclosure

Do not use for malicious purposes. Always follow responsible disclosure practices.

## License

MIT License

## Author

Onurcan - AI Security Researcher