# PromptShot v3.4

> AI Red Teaming Framework for LLM Vulnerability Research

⚠️ **For authorized security research only.**

---

## Features

- Multi-vendor targeting (OpenAI, Anthropic, Google, xAI, Meta, Mistral)
- Three operation modes: Stealth, Balanced, Aggressive
- Chained fusion pipeline with DOSE calibration
- Multi-level obfuscation

---

## Installation

**Requirements:** Python 3.8+

```bash
# Clone
git clone https://github.com/yourusername/promptshot.git
cd promptshot

# Create directories
mkdir -p data/libertas data/claritas

# Verify
python pipeline.py --help
```

---

## Usage

### CLI

```bash
# Balanced mode (default)
python pipeline.py -s "explain encryption" -t gpt-4o

# Stealth mode (minimal footprint)
python pipeline.py -s "describe protocols" -t claude -m stealth
python pipeline.py -s "SEED BURADA" -t gpt-4o -m stealth


# Aggressive mode (maximum bypass)
python pipeline.py -s "detail security concepts" -t grok -m aggressive -v
python pipeline.py -s "SEEDvalue" -t claude -m balanced -v


# Save to file
python pipeline.py -s "your query" -t gpt-4o -o payload.txt
```

### CLI Arguments

| Arg | Short | Description |
|-----|-------|-------------|
| `--seed` | `-s` | Your query (required) |
| `--target` | `-t` | Target model (default: gpt) |
| `--mode` | `-m` | stealth / balanced / aggressive |
| `--verbose` | `-v` | Show detailed output |
| `--output` | `-o` | Save payload to file |

### Python API

```python
from pipeline import PromptShotPipeline

pipeline = PromptShotPipeline(verbose=True)
result = pipeline.execute(
    seed="explain quantum computing",
    target="gpt-4o",
    mode="balanced"
)

print(result.payload)
print(f"Stats: Pliny={result.stats['pliny_count']}, Elder={result.stats['elder_count']}")
```

---

## Modes

| Mode | Pliny | Elder | Use Case |
|------|-------|-------|----------|
| **Stealth** | 3-7 | 3-7 | Low-risk, corporate environments |
| **Balanced** | 15-25 | 15-25 | Standard testing |
| **Aggressive** | 40-120 | 80-120 | Maximum bypass potential |

---

## Project Structure

```
promptshot/
├── pipeline.py           # Main entry point
├── fusion_engine.py      # Core payload generator
├── claritas_engine.py    # Behavioral intelligence
├── libertas_loader.py    # Vendor blueprints
├── obfuscation.py        # Obfuscation engine
└── data/
    ├── libertas/         # Vendor blueprint files
    └── claritas/         # Behavioral profiles
```

---

## License

Research use only. Unauthorized use prohibited.