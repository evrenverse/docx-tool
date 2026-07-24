from hypothesis import given
from hypothesis import strategies as st

from docx_tool.commands.read import _parse_cells, _parse_indices


@given(st.lists(st.integers(min_value=1, max_value=100_000), min_size=1, max_size=100))
def test_one_based_indices_round_trip(indices):
    specification = ",".join(str(index) for index in indices)

    assert _parse_indices(specification, "--paragraphs") == indices


@given(
    st.lists(
        st.tuples(
            st.integers(min_value=1, max_value=10_000),
            st.integers(min_value=1, max_value=10_000),
        ),
        min_size=1,
        max_size=100,
    )
)
def test_table_cells_round_trip(cells):
    specification = ",".join(f"{row}:{column}" for row, column in cells)

    assert _parse_cells(specification) == cells
