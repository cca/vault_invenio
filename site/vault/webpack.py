"""JS/CSS Webpack bundles for VAULT."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={"vault-test": "./js/vault/test.js"},
        ),
    },
)
