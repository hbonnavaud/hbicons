from colorize import create_new_color


generate_fully_colorized_icons = True
colors = [
    {"value": "a15137", "name": "orange"},
    {"value": "8a6029", "name": "gold"},
    {"value": "3b0a0a", "name": "dark-red"},
    {"value": "428f28", "name": "light-green"},
    {"value": "269680", "name": "cyan"},
    {"value": "2dcbeb", "name": "skyblue"},
    {"value": "12214d", "name": "dark-blue"},
    {"value": "49008a", "name": "purple"},
    {"value": "881f94", "name": "pink"},
    {"value": "590730", "name": "wine-red"},
    {"value": "000000", "name": "black"},
    {"value": "262626", "name": "dark-grey"},
    {"value": "828282", "name": "light-grey"},
    {"value": "cfcfcf", "name": "white"},
    {"value": "c0c0c0", "name": "silver"}
]


for color in colors:
    if generate_fully_colorized_icons:
        create_new_color(color["value"], color["name"] + "-full", full=True)
    create_new_color(color["value"], color["name"], full=False)