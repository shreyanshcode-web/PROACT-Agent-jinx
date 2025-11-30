"""Base prompt infrastructure for Jinx.

All prompt modules should expose a callable that returns the prompt string.
We provide a small abstract base class to standardise this pattern and make
future extensions (e.g. loading from files, templating, localisation) easier.
"""

from __future__ import annotations

import abc
from typing import Any, Dict


class BasePrompt(abc.ABC):
    """Abstract base class for prompt providers.

    Sub‑classes must implement :meth:`load` which returns the raw prompt
    string.  The :meth:`render` method can be overridden to perform
    templating – by default it simply returns the loaded prompt.
    """

    @abc.abstractmethod
    def load(self) -> str:
        """Return the raw prompt text.

        Implementations should keep this method side‑effect free – it is
        called each time the prompt is needed.
        """

    def render(self, **context: Any) -> str:
        """Render the prompt using *context*.

        The default implementation performs a simple ``str.format``
        substitution, allowing placeholders like ``{variable}`` in the
        prompt text.  Sub‑classes can override for more sophisticated
        templating engines.
        """
        raw = self.load()
        try:
            return raw.format(**context)
        except Exception:
            # If formatting fails we fall back to the raw prompt – this
            # prevents the agent from crashing due to a missing key.
            return raw
