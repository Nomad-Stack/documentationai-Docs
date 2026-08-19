# NomadBill Documentation

This repository contains the NomadBill product documentation for [documentation.ai](https://documentation.ai): user guides, help center articles, changelog, and the OpenAPI spec.

NomadBill is a multi-currency invoicing and bookkeeping product for freelancers, digital nomads, and global businesses.

## What lives here

| Path | Role |
| --- | --- |
| `documentation.json` | Site config: name, colors, logos, and the full multilingual navigation (tabs, groups, page titles, paths). |
| `en/` | English source docs. Mirror this structure for every other language. |
| `de/`, `es/`, `fr/`, … | Localized copies of the same files (same relative paths and filenames). |
| `*/api-reference/openapi.yaml` | OpenAPI spec for the API Reference tab in each language. |

Helper scripts such as `translate_pt.py` are local translation utilities, not part of the published docs.

## Languages

Each language is a top-level folder. Navigation in `documentation.json` uses the same locale prefix (`en/…`, `de/…`, …).

| Code | Language |
| --- | --- |
| `en` | English |
| `de` | German |
| `es` | Spanish |
| `fr` | French |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |
| `tr` | Turkish |
| `ar` | Arabic |
| `hi` | Hindi |
| `zh` | Chinese |
| `ja` | Japanese |
| `ko` | Korean |
| `id` | Indonesian |
| `th` | Thai |

## Folder layout (per language)

Every locale follows this tree:

```text
<lang>/
  introduction.mdx
  quickstart.mdx
  features.mdx
  integrations.mdx
  changelog.mdx
  help-center.mdx
  api-reference/
    openapi.yaml
  help-center/
    faq/how-to-create-invoice.mdx
    troubleshooting/invoice-email-not-sent.mdx
    guides/add-client.mdx
  user-guide/
    dashboard.mdx
    customers.mdx
    products.mdx
    invoicing.mdx
    quotes.mdx
    incoming-invoices.mdx
    bank-sync.mdx
    email-intelligence.mdx
    pdf-templates.mdx
    custom-fields.mdx
    team-management.mdx
    settings.mdx
```

Pages are MDX. Internal links must keep the **file path** (for example `/en/user-guide/invoicing`), not a translated slug. Only visible titles and body copy are localized.

## Navigation

`documentation.json` → `navigation.languages` lists every language in the language switcher. Each language has the same tabs:

- Documentation (Getting Started, Core Concepts, User Guide, Advanced)
- API Reference (OpenAPI)
- Help Center (FAQs, Troubleshooting, Guides)
- Changelog

If you add, rename, or remove a page, update:

1. The MDX/YAML file in **every** locale folder, and
2. The matching `path` / `openapi` entries under **every** language in `documentation.json`.
