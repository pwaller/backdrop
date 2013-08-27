import logging
import xlrd
import datetime
from backdrop.core.errors import ParseError
from backdrop.core.timeutils import utc

class ExcelError(object):
    def __init__(self, description):
        self.description = description

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.description == other.description

    def __ne__(self, other):
        return not self.__eq__(other)

EXCEL_ERROR = ExcelError("error in cell")

def parse_excel(incoming_data):
    book = xlrd.open_workbook(file_contents=incoming_data.read())

    for sheet in book.sheets():
        yield _extract_rows(sheet, book)


def _extract_rows(sheet, book):
    for i in range(sheet.nrows):
            yield _extract_values(sheet.row(i), book)


def _extract_values(row, book):
    return [_extract_cell_value(cell, book) for cell in row]


def _extract_cell_value(cell, book):
    if cell.ctype == xlrd.XL_CELL_DATE:
        time_tuple = xlrd.xldate_as_tuple(cell.value, book.datemode)
        return utc(datetime.datetime(*time_tuple)).isoformat()
    elif cell.ctype == xlrd.XL_CELL_ERROR:
        logging.warn("Encountered errors in cells when parsing excel file")
        return EXCEL_ERROR
    return cell.value
