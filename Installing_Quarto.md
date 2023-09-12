### On Windows (11 Home)

If typing `quarto.exe --help` says Quarto cannot by found, then:

- Quarto may be installed under `/mnt/c/Users/<Your Username>/AppData/Local/Programs/Quarto/bin`
- Edit the `.bashrc` file in your `$HOME` directory. On Windows I would Google search for the best way to do this: "edit .bashrc file Windows".
- Add the following line at the end of the file:
    `export PATH=/mnt/c/Users/<Your Username>/AppData/Local/Programs/Quarto/bin:$PATH`
- Save the file and run `source .bashrc` in the Terminal.
- You should now be able to run the following command successfull:
    `quarto.exe --help`
- **Note** that the command seems ***not*** to be `quarto`, it’s `quarto.exe`
