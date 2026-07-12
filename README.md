# schema-migration-simulator

A dependency-free Python CLI for estimating operational risk before applying SQL schema migrations.

## Quick start

```bash
python simulate.py migration.sql --stats table-rows.json
```

It detects irreversible DDL, potential table-lock operations, and large backfills. When table row counts are supplied, it estimates scan duration at a documented conservative throughput. The command emits JSON and exits nonzero on high-risk migrations.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
