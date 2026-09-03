# Xsection Generator

This is a tool to generate a basic xsection code.

The [XSection](https://codeberg.org/klayoutmatthias/xsection) is a add-on module of [KLayout](https://www.klayout.de/), free layout editor/viewer.
XSection can help user to draw the cross-section view of where ruler-tool marked.

## Features

- Modern GUI-based workflow
- Save/open setting of project
- Automatically generate XSection script (.xs)
- z direction scaling
- Support Deposit, Grow, and Etch processes
- Option to generate snapshots for every process step

## XSection Scripts

If you want to modify the generated script with more actions, such as customize the masks or materials by ```AND```, ```OR```, or more methods, please refer to the official documents.

You can find more information about the scripts as following:

- [Project description](https://klayoutmatthias.codeberg.page/xsection/doc-html/)
- [Introduction into writing XS files](https://klayoutmatthias.codeberg.page/xsection/doc-html/DocIntro.html)
- [Methods and elements](https://klayoutmatthias.codeberg.page/xsection/doc-html/DocReference.html#layers_file-method)
  - [Grow](https://klayoutmatthias.codeberg.page/xsection/doc-html/DocGrow.html)
  - [Etch](https://klayoutmatthias.codeberg.page/xsection/doc-html/DocEtch.html)

## Requirements

- Python 3.10+
- CustomTkinter [github](https://github.com/tomschimansky/customtkinter), [Official website](https://customtkinter.tomschimansky.com/)
- CTkListbox [github](https://github.com/Akascape/CTkListbox)
- CTkMenuBar [github](https://github.com/Akascape/CTkMenuBar)

Use pip to install requirements:

```shell
pip install -r requirements.txt
```
