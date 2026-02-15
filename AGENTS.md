# agents.md - Configarr

## Project Overview
**Name:** Configarr
**Purpose:** A declarative configuration-as-code tool for the "Arr" stack (Sonarr, Radarr, Prowlarr). It reconciles a local YAML configuration with the live state of the servers via their REST APIs.
**Guiding Principle:** The YAML file is the "Source of Truth." If it's in the YAML, it should be on the server. If it's on the server but not in the YAML, the tool should (optionally) flag or remove it.

---

## Tech Stack
- **Runtime:** Python 3.13.9
- **Configuration:** YAML (parsed via `PyYAML`)
- **Validation:** `Pydantic V2` (Strict mode preferred)
- **API Clients:** Generated via `openapi-generator` (located in `src/generated/`)
- **Models:** Generated via `datamodel-code-generator`
- **Environment:** `python-dotenv` for local secret management

---

## Project Structure
```text
/
├── config/               # User-facing YAML files
├── src/
│   ├── plugins/          # Plugin system for multi-arr support
│   │   └── sonarr/       # Sonarr plugin
│   │       └── generated/ # API clients (DO NOT MANUALLY EDIT)
│   ├── shared/           # Shared mappers and schemas
│   ├── core/             # Reconciliation loop and diffing logic
│   ├── utils/            # Shared helpers (logging, auth, env)
│   └── main.py           # CLI Entry point
├── .env                  # Private API keys and URLs
└── agents.md             # This file (Agent instructions)