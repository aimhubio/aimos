# Contributing

Thanks for your interest in helping improve AimOS! 🎉

## Before Contributing

As with most projects, prior to starting to code on a bug fix or feature request, please post in the respective GitHub issue saying you want to volunteer, and then wait for a positive response. And if there is no issue for it yet, create it first.

This helps make sure:
1. Two people aren't working on the same thing.
2. This is something maintainers believe should be implemented/fixed.
3. Any API, UI, or deeper architectural changes that need to be implemented have been fully thought through by the community together with AimOS maintainers.

Please follow [AimOS Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md) in all your interactions with the project.

## Governance

This section describes governance processes we follow in developing AimOS.

### Persons of Interest

#### Authors

- Gev Soghomonyan ([SGevorg](https://github.com/SGevorg))
- Gor Arakelyan ([gorarakelyan](https://github.com/gorarakelyan))

#### Maintainers

- Albert Torosyan ([alberttorosyan](https://github.com/alberttorosyan))
- Karen Hambardzumyan ([mahnerak](https://github.com/mahnerak))
- Karo Muradyan ([KaroMourad](https://github.com/KaroMourad))
- Mihran Vanyan ([mihran113](https://github.com/mihran113))

### Releases

We release a new minor version (e.g., 1.0.0) every three to four week and patch releases on demand. The minor versions contain new features, bugfixes and also all previous bugfixes included in previous patch releases. With every release, we publish a [CHANGELOG](./CHANGELOG.md) where we list enhancements and fixes. The versioning scheme we use is [SemVer](http://semver.org/).

## Contribution Process

The AimOS contribution process starts with filing a GitHub issue. AimoS defines six categories of issues: enhancements (feature requests), bug reports, code health improvements, peformance improvements, tests, questions.

AimOS maintainers actively triage and respond to GitHub issues. In general, we recommend waiting for feedback from an AimOS maintainer or community member before proceeding to implement a feature or patch. This is particularly important for significant changes, and will typically be labeled during triage with `phase / exploring`.

After you have agreed upon an implementation strategy for your feature or patch with an AimOS maintainer, the next step is to introduce your changes as a pull request against the AimOS Repository.

Once your pull request against the AimOS Repository has been merged, your corresponding changes will be automatically included in the next AimOS release. Every change is listed in the [AimOS release notes](https://github.com/aimhubio/aimos/releases) and [CHANGELOG](./CHANGELOG.md).

Congratulations, you have just contributed to AimOS. We appreciate your contribution!

## Developing and Testing

The majority of the AimOS product areas is developed in Python/Cython. This includes the Storage, SDK, Tracking Server, CLI, API. AimOS UI is a Web app mostly built with TypeScript and React.

### Developing Storage/SDK/CLI

Most of the backend components, including SDK, Storage, Web APIs and CLI are developed using Python/Cython.
In order to start development you must install AimOS dependencies, and the aimos package itself, in editable mode.
```shell
pip install -e .
```

Verify that AimOS installed properly by running
```shell
aimos version
```
or by importing AimOS in python REPL
```python
import aimos
```

#### Style Guide
AimOS follows PEP8 standard for style guide and uses `flake8` as a style checker. Style checks enforced
as a check on GitHub Actions when new PR opened.

#### Testing Requirements

New unit-tests must be added along with the code changes. In order to setup the testing environment
```shell
cd tests/unit_tests
pip install -r requirements.txt
```

AimOS python code unit-tests are located at `tests/unit_tests` directory. Unit-tests are written in Python's `unittest` package style.
[Pytest](https://docs.pytest.org) is used as a test runner/discovery tool. To make sure unit-tests are not failing run
```shell
pytest tests/unit_tests
```

### Developing UI

AimOS UI is written in TypeScript. `npm` is required to build AimOS UI and to run in DEV mode.
You can verify that `npm` is on the PATH by running `npm -v`, and
[install npm](https://www.npmjs.com/get-npm) if needed.

#### Style Guide

We use Prettier to autoformat code on presubmit.

#### Launching the Development UI

Before running the AimOS UI dev server or building a distributable wheel, install npm
dependencies via:

```shell
cd src/aimcore/web/ui
npm install
```

Then you can start the dev server:

```shell
npm start
```

AimOS UI will show logged data in at [http://localhost:3000](http://localhost:3000).

#### Adding New Components

To start building a new component you can run following command:

```shell
npm run crc 'ComponentName'
```


If you want to add a component inside UI kit you can run following command:

```shell
npm run crc-kit 'ComponentName'
```

These command will create a folder named `ComponentName` with all the necessary files.

## Writing Docs

AimOS documentation is built using [Sphix](https://www.sphinx-doc.org) and is hosted at Read the Docs.
The documentation sources are located at `docs/` directory. In order to build documentation locally
run the following commands
```shell
cd docs
pip install -r requirements.txt
make html
```

Documentation will be available at `docs/build/html/index.html` on your local machine.
