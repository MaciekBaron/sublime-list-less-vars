sublime-list-less-vars
======================

Simple Sublime 2 plugin for listing LESS variables used in a file.

The default hotkey is <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>L</kbd> (or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd> on Linux).

It displays a list of LESS variables used in your current file allowing you to insert a selected one 
directly into your code. It also supports `@import`ed LESS files so you can use variables defined in 
external files.

Note that the plugin automatically ignores anything which looks like a vendor prefixed statement (e.g. 
`@-webkit-keyframes`) and reserved words (e.g. `@media`, `@import` etc.)

![Screenshot](http://i41.tinypic.com/eajivq.png)

Installation
------------

The plugin will be added to Package Control during the next merger. Until then, simply clone the repo 
into your plugins folder.

