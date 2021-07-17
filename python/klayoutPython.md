About Macro Development
+++
Klayout looks for macro in the following places:
	The "macros" or "pymacros" folders in the installation path. The installation path is where the KLayout binary resides. KLayout cannot modify macros that are stored in that path. This is the "global" repository. Usually that repository is shared between all users. An administrator can use this location to install macros globally.
	The "macros" or "pymacros" folders in KLayout's user specific application folder. On Unix that is "~/.klayout/macros". This is the "local" repository. Any user can store his or her own macros here.
	Plain Ruby or Python files can be kept inside "ruby" and "python" directories next to "macros" and "pymacros". In contrast to "macros" and "pymacros", the locations of "ruby" and "python" paths are added to the Ruby or Python search paths. This makes those folders useful for keeping plain Ruby or Python libraries. Generic ".lym" files cannot reside there and those locations are not scanned for autorun macros.
	In addition, further repositories can be given on the command line with the "-j" option. This allows adding development repositories which are under configuration management and contain the latest code for the macros. Those repositories are called "project" repositories.
	Technology folders: each technology folder can carry a "macros" or "pymacros" subfolder where technology-specific macros are kept. See for details about technologies.
	Macros can be kept in packages and installed from a remote repository. See About Packages for details about packages.