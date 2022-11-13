from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def chunks(iterable: Iterable[T], size: int) -> Generator[list[T], None, None]:
    """Yields chunks of size 'size' from a iterable."""

    _iterable = iter(iterable)
    while True:
        elements = []
        for _ in range(size):
            try:
                elements.append(next(_iterable))
            except StopIteration:
                break

        if not len(elements):
            break

        yield elements
