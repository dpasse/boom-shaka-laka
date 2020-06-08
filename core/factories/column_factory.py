from ..models.column import Column


def create_column(
  order: int,
  min_label_length: int,
  max_label_length: int,
  max_unit_length: int,
  max_number_of_label_parts: int
) -> Column:
  column = Column()
  column.order = order
  column.min_label_length = min_label_length
  column.max_label_length = max_label_length
  column.max_unit_length = max_unit_length
  column.max_number_of_label_parts = max_number_of_label_parts

  return column
