# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.0]

### Added

- `realized_semivariance` for the downside/upside split of realized variance.
- Range-based volatility estimators `parkinson` and `garman_klass`.
- `two_scale_rv` and `realized_kernel` noise-robust estimators.
- HAR feature builder `har_features`.
- Order-book utilities, Lee-Mykland jump test and execution benchmarks.

## [0.1.0]

### Added

- Data loaders `read_trades` / `read_quotes` that normalise to a canonical schema.
- Bar sampling: `time_bars`, `tick_bars`, `volume_bars`, `dollar_bars`.
- Realized volatility: `realized_variance`, `realized_volatility`, `bipower_variation`,
  `jump_variation`.
- Microstructure metrics: `roll_spread`, `amihud_illiquidity`.
- Command-line interface with `rv` and `bars` subcommands.

[Unreleased]: https://github.com/davidy749/tickflow/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/davidy749/tickflow/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/davidy749/tickflow/releases/tag/v0.1.0
