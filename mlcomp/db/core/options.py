class PaginatorOptions:
    def __init__(self, sort_column: str, sort_descending: bool, page_number:int, page_size:int):
        self.sort_column = sort_column
        self.sort_descending = sort_descending
        self.page_number = page_number
        self.page_size = page_size

        assert (sort_column and sort_order) or (not sort_column and not sort_order), 'Specify both sort_column and sort_descending'
        assert (page_number and page_size) or (not page_number and not page_size), 'Specify both page_number and page_size'