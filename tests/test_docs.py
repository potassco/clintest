import doctest
import re
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

FENCE = re.compile(r"(?P<indent> *)```(?P<lang>\w*)(?: .*)?")
SNIPPET = re.compile(r'--8<-- "(?P<path>[^":]+):(?P<section>\w+)"')


@dataclass
class Block:
    path: Path
    line: int
    lang: str
    code: str


def section(path: Path, name: str) -> tuple[list[str], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if f"--8<-- [start:{name}]" in line]
    ends = [i for i, line in enumerate(lines) if f"--8<-- [end:{name}]" in line]
    assert len(starts) == len(ends) == 1 and starts[0] < ends[0], f"{path} needs exactly one section {name!r}"
    return lines[starts[0] + 1 : ends[0]], starts[0] + 1


def read_blocks(path: Path, lines: list[str], offset: int = 0) -> Iterator[Block]:
    i = 0
    while i < len(lines):
        if snippet := SNIPPET.fullmatch(lines[i]):
            included = ROOT / snippet["path"]
            yield from read_blocks(included, *section(included, snippet["section"]))
        elif fence := FENCE.fullmatch(lines[i]):
            start = i = i + 1
            while lines[i] != fence["indent"] + "```":
                i += 1
            code = "".join(line.removeprefix(fence["indent"]) + "\n" for line in lines[start:i])
            yield Block(path, offset + start + 1, fence["lang"], code)
        i += 1


def run_python(block: Block, globs: dict, output: Block | None) -> None:
    # The leading newlines make tracebacks point to the block's lines in the Markdown file.
    code = compile("\n" * (block.line - 1) + block.code, str(block.path), "exec")
    try:
        exec(code, globs)  # noqa: S102
    except Exception as error:
        # A block may raise if the following pytb block shows the error.
        if output is None or output.lang != "pytb":
            raise
        assert f"{type(error).__name__}: {error}" == output.code.rstrip("\n"), f"{output.path}:{output.line}"


def run_pycon(block: Block, globs: dict) -> None:
    test = doctest.DocTestParser().get_doctest(block.code, globs, block.path.stem, str(block.path), block.line - 1)
    report: list[str] = []
    results = doctest.DocTestRunner().run(test, out=report.append, clear_globs=False)
    assert not results.failed, "".join(report)


@pytest.mark.parametrize("page", sorted(DOCS.rglob("*.md")), ids=lambda page: str(page.relative_to(ROOT)))
def test_docs(page):
    globs = {"__name__": "__main__"}
    blocks = list(read_blocks(page, page.read_text(encoding="utf-8").splitlines()))
    for block, next_block in pairwise([*blocks, None]):
        if block.lang == "python":
            run_python(block, globs, next_block)
        elif block.lang == "pycon":
            run_pycon(block, globs)
