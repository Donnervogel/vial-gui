from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QPlainTextEdit

from protocol.constants import VIAL_PROTOCOL_DYNAMIC, VIAL_PROTOCOL_KEY_OVERRIDE, VIAL_PROTOCOL_ADVANCED_MACROS, \
    VIAL_PROTOCOL_EXT_MACROS, VIAL_PROTOCOL_QMK_SETTINGS


class AboutKeyboard(QDialog):

    def want_min_vial_fw(self, ver):
        if self.keyboard.sideload:
            return "unsupported - sideloaded keyboard"
        if self.keyboard.vial_protocol < 0:
            return "unsupported - VIA keyboard"
        if self.keyboard.vial_protocol < ver:
            return "unsupported - Vial firmware too old"
        return "unsupported - disabled in firmware"

    def about_tap_dance(self):
        if self.keyboard.tap_dance_count > 0:
            return str(self.keyboard.tap_dance_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_DYNAMIC)

    def about_combo(self):
        if self.keyboard.combo_count > 0:
            return str(self.keyboard.combo_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_DYNAMIC)

    def about_key_override(self):
        if self.keyboard.key_override_count > 0:
            return str(self.keyboard.key_override_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_KEY_OVERRIDE)

    def about_macro_delays(self):
        if self.keyboard.vial_protocol >= VIAL_PROTOCOL_ADVANCED_MACROS:
            return "yes"
        return self.want_min_vial_fw(VIAL_PROTOCOL_ADVANCED_MACROS)

    def about_macro_ext_keycodes(self):
        if self.keyboard.vial_protocol >= VIAL_PROTOCOL_EXT_MACROS:
            return "yes"
        return self.want_min_vial_fw(VIAL_PROTOCOL_EXT_MACROS)

    def about_qmk_settings(self):
        if self.keyboard.vial_protocol >= VIAL_PROTOCOL_QMK_SETTINGS:
            if len(self.keyboard.supported_settings) == 0:
                return "disabled in firmware"
            return "yes"
        return self.want_min_vial_fw(VIAL_PROTOCOL_QMK_SETTINGS)

    def __init__(self, device):
        super().__init__()

        self.keyboard = device.keyboard
        self.setWindowTitle("About {}".format(device.title()))

        text = ""
        desc = device.desc
        text += "Manufacturer: {}\n".format(desc["manufacturer_string"])
        text += "Product: {}\n".format(desc["product_string"])
        text += "\n"

        text += "IMI protocol: {}\n".format(self.keyboard.vial_protocol)
        text += "IMIl keyboard ID: {:08X}\n".format(self.keyboard.keyboard_id)
        text += "\n"

        text += "Macro entries: {}\n".format(self.keyboard.macro_count)
        text += "Macro memory: {} bytes\n".format(self.keyboard.macro_memory)
        text += "Tap Dance entries: {}\n".format(self.about_tap_dance())
        text += "Combo entries: {}\n".format(self.about_combo())

        font = QFont("monospace")
        font.setStyleHint(QFont.TypeWriter)
        textarea = QPlainTextEdit()
        textarea.setReadOnly(True)
        textarea.setFont(font)

        textarea.setPlainText(text)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(textarea)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
