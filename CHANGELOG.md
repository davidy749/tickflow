# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0]

### Added

- Data loaders `read_trades` / `read_quotes` that normalise to a canonical schema.
- Bar sampling: `time_bars`, `tick_bars`, `volume_bars`, `dollar_bars`.
- Realized volatility: `realized_variance`, `realized_volatility`, `bipower_variation`,
  `jump_variation`.
- Microstructure metrics: `roll_spread`, `amihud_illiquidity`.
- Command-line interface with `rv` and `bars` subcommands.

[Unreleased]: https://github.com/davidy749/tickflow/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/davidy749/tickflow/releases/tag/v0.1.0
