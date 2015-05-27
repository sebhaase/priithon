# Priithon
Priithon is a platform for image analysis and image analysis algorithm development.

While the focus here is on algorithm development, it makes it very easy to develop applications that would not require any programming skills, i.e. making "end user" biologist's or astronomer's applications.

Priithon is easy to install: download a single zip archive and unpack. (It requires Python to be installed. More info is on the PriithonWiki.(FIXME LINK))

# Target audience
While Priithon is mainly used (by myself) as a daily work horse for looking at microscope images of some cell nuclei or other biology, there are many aspects that are not primarily geared for my own benefit:

- I want others to be able to install Priithon with minimal effort.

  This means:
  - Simple one-step unpacking of a package file
  - No system administrator permissions, or system knowledge, is required

- It is easy to make custom application, that allow someone to perform advanced image analysis tasks, who does not have any prior training in programming or scripting

- It is the best platform I know, to teach (complete) programming novices some basic skills in scripting
  - The Python programming language is generally considered clean and easy to learn
  - The PyShell interface gives helpful function descriptions and pop-up lists of available functions as you type

- Transparent modular multi-tier design going from interactive explorations to algorithms to scientist-oriented applications
 1. Priithon sessions are (auto-) saved into text files, documenting every step of interactive explorations
 2. Copy and paste into a Python-module file creates reusable functions
 3. Functions are then fine-tuned into cleanly parametrized algorithms
 4. Simple GUI interfaces visualize the set of "most-used" parameters and allow execution per mouse-click
 5. Organizing multiple GUI windows with few-line setup functions into a "drag-into-Priithon-to-execute" script file

# Documentation (old)
 - [PriithonHandbook](https://rawgit.com/sebhaase/priithon/master/priithon_docs/PriithonHandbook.html)
 - [PriithonTutorials](https://rawgit.com/sebhaase/priithon/master/priithon_docs/PriithonTutorials.html)
 - [PriithonModules epydoc](https://rawgit.com/sebhaase/priithon/master/priithon_docs/PriithonEpydoc/index.html)

# priithon
Automatically exported from code.google.com/p/priithon
