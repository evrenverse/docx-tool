# Agent evals

The eval generates a synthetic DOCX and exercises the real installed CLI:

1. discover document structure;
2. locate a label;
3. read only its paragraph;
4. apply a transactional edit;
5. verify the output document.

```bash
uv run python evals/run_evals.py
```

The runner emits one JSON result and exits nonzero on failure. It never uses
external documents or network services.
