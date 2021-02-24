import os
from os.path import sep

icons_folder = os.path.dirname(os.path.abspath("main.py")) + sep + "uis" + sep + "res" + sep + "icons" + sep


def replace_property(stylesheet, key, value):

	index = stylesheet.rfind(key)

	if index == -1:
		return stylesheet + key + ":" + value + ";"
	else:
		index += len(key) + 1
		semicolon = stylesheet.find(";", index)
		return stylesheet[:index] + value + stylesheet[semicolon:]


if __name__ == '__main__':
	test_str = "please update this property's value style: medieval; thanks"
	test_str2 = "nothing to replace here, "
	print(replace_property(test_str, "style", "modern"))
	print(replace_property(test_str2, "ill do it", "anyway"))
