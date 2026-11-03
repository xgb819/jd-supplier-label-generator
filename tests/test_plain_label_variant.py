import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from gui_app import (
    SupplierLabelGeneratorWindow,
    get_label_sheet_columns,
    unique_label_output_path,
)


class PlainLabelVariantTests(unittest.TestCase):
    def test_detects_variant_without_69_and_sn_columns(self):
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(["商品编号", "玩具店铺", "编号", "合计"])

        self.assertEqual(
            get_label_sheet_columns(worksheet),
            {"sku": 1, "brand": 2, "number": 3},
        )

    def test_duplicate_number_uses_incrementing_suffix(self):
        with tempfile.TemporaryDirectory() as folder:
            first = Path(unique_label_output_path(folder, "9.SG216PRO"))
            first.touch()
            second = Path(unique_label_output_path(folder, "9.SG216PRO"))
            second.touch()
            third = Path(unique_label_output_path(folder, "9.SG216PRO"))

            self.assertEqual(first.name, "9.SG216PRO.pld")
            self.assertEqual(second.name, "9.SG216PRO_2.pld")
            self.assertEqual(third.name, "9.SG216PRO_3.pld")

    def test_default_sheet_settings_no_longer_include_propeller_mapping(self):
        mapping = SupplierLabelGeneratorWindow.init_sheet_mapping(None)
        self.assertEqual(set(mapping), {"3C", "玩具"})


if __name__ == "__main__":
    unittest.main()
