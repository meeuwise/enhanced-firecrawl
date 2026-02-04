# Enhanced FireCrawl

Automated SaaS pricing research with JSON extraction. Built for OpenClaw business intelligence.

## Features

- ✅ FireCrawl web search integration
- ✅ Markdown content extraction
- ✅ Multi-source aggregation
- ✅ Cost-optimized for RPi/M4 hardware
- ✅ Environment variable configuration (secure)

## Setup

### 1. Get Your FireCrawl API Key

1. Go to https://www.firecrawl.dev/dashboard
2. Create/copy your API key
3. Keep it safe (never commit to git!)

### 2. Set Environment Variable

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
nano .env
# or
export FIRECRAWL_API_KEY="your-api-key-here"
```

### 3. Run the Script

```bash
python3 firecrawl_search.py "DocuSign pricing"
```

## Security

⚠️ **IMPORTANT**: Never commit API keys to git!

- API keys are loaded from environment variables only
- `.gitignore` prevents accidental commits
- If a key is exposed, revoke it immediately on the dashboard

## Usage Examples

### Basic Search

```bash
python3 firecrawl_search.py "ServiceNow pricing cost"
```

### Search with Limits

```bash
python3 firecrawl_search.py "Salesforce pricing 2026" --limit 10
```

## Output Format

Returns JSON with search results:

```json
{
  "success": true,
  "results": [
    {
      "position": 1,
      "title": "...",
      "url": "...",
      "description": "..."
    }
  ],
  "count": 5,
  "mode": "search"
}
```

## Roadmap

- [ ] JSON extraction (Phase 2)
- [ ] Comparison matrix generation
- [ ] Multi-LLM integration (DeepSeek, Groq, MiniMax)
- [ ] Advanced business research features

## Contributing

Contributions welcome! Please:
1. Never commit API keys
2. Use `.env.example` for configuration examples
3. Test locally before pushing

## License

MIT

## Security Report

**GitGuardian Alert (Feb 4, 2026)**:
- Old API key was exposed in initial commit ✅ FIXED
- Key was immediately revoked ✅ SAFE
- Git history rewritten to remove exposure ✅ CLEANED
- Environment variable setup implemented ✅ SECURE

All issues resolved. Repository is now secure.
