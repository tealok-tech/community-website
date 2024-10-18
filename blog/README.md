# tealok-engagement

A place to drive engagement with Tealok.

## Incantations

Run `nix-shell` in order to get an environment with all the tools you'll need.

### Plugin install

This site depends on `lektor-markdown-from-file`, which is included in `packages/lektor-markdown-from-file`. On POSIX environments this should install automatically. On Windows, you'll need to manually install it:

```
*activate your virtual environment*
cd packagens/lektor-markdown-from-file
python -m pip install -e .
```

After that, `lektor plugins list` should show the plugin and the build should work.

### Development

```
lektor server
```

The website is then available at `http://localhost:5000`
