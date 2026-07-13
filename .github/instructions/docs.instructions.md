---
applyTo: "**"
---
# Docs File Standards

Rules for user-facing files created in `docs/` folders across all topics.

---

## CSV Files

### Date Format — MANDATORY

**ALL date fields in CSV files MUST use ISO 8601 format: `YYYY-MM-DD`**

```csv
# ✅ CORRECT
purchase_date
2025-05-15
2026-04-09

# ❌ WRONG — never use these formats
05/15/25
05/15/2025
May 15, 2025
15-05-2025
```

This applies to every date column regardless of what it's named (`purchase_date`, `date`, `start_date`, `end_date`, etc.).

### Unknown / Missing Values

Use `??` for unknown values, never leave a field blank without reason.

```csv
purchase_date,purchase_price
??,??
2025-05-15,"$850 + Tax"
```

## Column Naming

- Use `snake_case` for all column headers
- No spaces in column names

### String Quoting

- Wrap values containing commas, semicolons, or quotes in double quotes
- Use semicolons (`;`) as delimiter within a notes field (not commas)

```csv
notes
"Came with 18-55mm lens; 24.2MP; 1080p video"
```

### Inventory CSV Schema

Standard schema for gear/equipment inventory files:

```
year,make,model,type,color,serial_number,purchase_location,purchase_date,purchase_price,notes
```

- `year` — Model year (integer, e.g. `2025`)
- `make` — Manufacturer (e.g. `Canon`, `Nikon`)
- `model` — Model name/number
- `type` — Category (e.g. `Camera`, `Lens`, `Accessory`)
- `color` — Color if relevant, else leave empty
- `serial_number` — Device serial number
- `purchase_location` — Store or URL (e.g. `bestbuy.com`, `Costco`)
- `purchase_date` — ISO 8601: `YYYY-MM-DD`, or `??` if unknown
- `purchase_price` — Dollar amount with tax note (e.g. `"$850 + Tax"`)
- `notes` — Semicolon-separated details (bundle contents, specs, purpose)
