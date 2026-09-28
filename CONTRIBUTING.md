# Contributing

Thanks for your interest in improving the OmniRun LlamaIndex tools. This project is licensed under
the [Apache License 2.0](./LICENSE); by contributing you agree that your
contribution is licensed under the same terms.

## Developer Certificate of Origin (DCO)

All contributions require a sign-off certifying that you wrote the patch (or
otherwise have the right to submit it under the project's license). We use the
[Developer Certificate of Origin](https://developercertificate.org/) 1.1.

Add a `Signed-off-by` line to every commit:

```
Signed-off-by: Your Name <you@example.com>
```

Git can add this automatically:

```bash
git commit -s -m "your message"
```

Pull requests without a DCO sign-off on each commit cannot be merged.

## Before opening a pull request

Run `ruff check .`, `mypy llama_index_tools_omnirun` and `pytest -q`.

## Related

The OmniRun server itself lives at
[github.com/a14a-org/omnirun](https://github.com/a14a-org/omnirun).
