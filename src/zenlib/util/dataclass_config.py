"""
Dataclass config mixin

Used to load config from a toml file with ChainMap based resolution
"""

from collections import ChainMap
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Mapping, TypeAlias

from zenlib.util.parse_toml import parse_toml

ConfigSource: TypeAlias = str | Path | Mapping[str, Any]


def _load_config_source(config_source: ConfigSource, allow_missing_file: bool = False) -> dict[str, Any]:
    """Loads a particular config source.
    If it's already a Mapping, return it.

    If it's a string/path, load the file

    If allow_missing_file is true, do not raise an exception for missing files and return an empty dict
    """

    if isinstance(config_source, Mapping):
        return dict(config_source)

    try:
        config_source = Path(config_source).expanduser()
        return parse_toml(config_source)
    except FileNotFoundError as e:
        if allow_missing_file:
            return {}
        else:
            raise e


@dataclass
class DataclassConfigMixIn:
    def _load_config(
        self,
        configs: list[ConfigSource],
        allow_missing_file: bool = False,
        allow_missing_config: list[str] | None = None,
    ):
        """
        Reads the passed config sources.
        If they are paths/strings, attempts to load the file paths
        Any additional args will be used as additional config loading layers.
        The first specified layer takes the highest precedence

        If allow_missing_file is True, missing files errors will be ignored.
        If allow_missing_config is defined, allow init if those values are None and there is not specified config
        """
        missing_fields = [f.name for f in fields(self) if getattr(self, f.name) is None]
        if not missing_fields:
            return

        config_chain: ChainMap[str, Any] = ChainMap(
            *[_load_config_source(config, allow_missing_file=allow_missing_file) for config in configs]
        )

        allow_missing_config = allow_missing_config or []

        for name in missing_fields:
            value = config_chain.get(name)
            # If the value is not defined in the config chain, raise an error if it's required
            if value is None:
                if name not in allow_missing_config:
                    raise ValueError(f"Missing required config value: {name}")
                continue

            setattr(self, name, value)
