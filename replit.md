# Tourism Projections Extractor

## Overview
A Python CLI tool that uses AI (Hugging Face Llama 3.1) to automatically extract future tourism projections from official documents. It downloads PDFs and web pages, classifies them, and extracts structured forecast data.

## Project Structure
```
src/
├── config.py      # HF API configuration and credentials
├── extract.py     # Document classification and data extraction
├── parser.py      # PDF and HTML parsing utilities  
├── search.py      # Document URL sources per country
├── pipeline.py    # Main orchestration script
└── test.py        # API connection test
```

## Setup Requirements
1. **Hugging Face Token**: Get from https://huggingface.co/settings/tokens
2. Create `.env` file with: `HF_TOKEN=your_token_here`

## Running
- **Main Pipeline**: `cd src && python pipeline.py`
- **Test API**: `cd src && python test.py`

## Output
Results saved to `classification_results.json` with extracted projections.

## Adding Countries
1. Add URLs to `HARDCODED_SOURCES` in `src/search.py`
2. Update `countries` list in `src/pipeline.py`
