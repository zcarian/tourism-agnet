# Tourism Projections Extractor

An AI-powered tool that automatically extracts future tourism projections (visitor arrivals and revenue forecasts) from official tourism documents.

## What It Does

This tool:
1. Fetches official tourism documents from configured URLs (PDF or HTML)
2. Uses an LLM (Llama 3.1) to classify if documents contain future projections
3. Extracts structured data: projected years, visitor numbers, and revenue figures
4. Saves results to a JSON file for analysis

## Quick Start

### 1. Get a Hugging Face Token

1. Create an account at [huggingface.co](https://huggingface.co)
2. Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Create a new token with "Read" permissions
4. Copy the token

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to keep dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

You'll know it's active when you see `(venv)` at the start of your terminal prompt.

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```
HF_TOKEN=your_huggingface_token_here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Test Your Setup

Run the test script to verify everything works:

```bash
python src/test.py
```

You should see: `tourism agent HF OK`

### 6. Run the Pipeline

```bash
python src/pipeline.py
```

Results are saved to `classification_results.json`.

## Project Structure

```
src/
├── config.py      # API configuration and credentials
├── extract.py     # Document classification and data extraction
├── parser.py      # PDF and HTML parsing utilities
├── search.py      # Document URL sources (add more countries here!)
├── pipeline.py    # Main orchestration script
└── test.py        # API connection test
```

## Adding More Countries

Edit `src/search.py` and add URLs to the `HARDCODED_SOURCES` dictionary:

```python
HARDCODED_SOURCES = {
    "USA": ["https://..."],
    "Spain": ["https://..."],
    "France": ["https://your-new-url-here.pdf"],  # Add new countries!
}
```

Then update the `countries` list in `src/pipeline.py`:

```python
countries = ["USA", "Spain", "France"]
```

## Output Format

The pipeline generates `classification_results.json` with entries like:

```json
{
  "country": "USA",
  "url": "https://...",
  "status": "ok",
  "classification": {
    "contains_projections": true,
    "projection_type": "arrivals",
    "years_mentioned": [2025, 2026],
    "confidence": 0.95
  },
  "extracted": {
    "projections": [
      {
        "indicator": "arrivals",
        "year": 2025,
        "value": 90000000,
        "unit": "visitors"
      }
    ]
  }
}
```

## Requirements

- Python 3.10+
- Hugging Face account with API access
- Internet connection for API calls and document downloads

## Troubleshooting

**"HF_TOKEN not set" error**
- Make sure you created a `.env` file with your token
- Check there are no extra spaces around the token

**"Model not found" or 403 errors**
- Some models require accepting terms on Hugging Face
- Visit the model page and accept any required agreements

**PDF parsing errors**
- Some PDFs are image-based and can't be parsed
- The tool will skip these and continue with other documents

## License

MIT
