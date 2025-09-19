# Usage

## Common commands

```bash
# Dev env
pixi install

# Lint / format / test
pre-commit run --all-files
pixi run test

# Docs
pixi run docs-serve
mike deploy 0.1 latest && mike set-default latest
```

- [ ] Write more docs
- [x] Enable Material theme
- [x] Wire mkdocstrings & charts
