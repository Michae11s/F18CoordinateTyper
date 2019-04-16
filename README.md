# F18CoordinateTyper
Written By Kyle Michaels
feel free to build with:
'''
pyinstaller .\\JDAMCoordsTyper.spec
'''

## Notes
- **MAKE SURE JDAM IS ALREADY SELECTED ON MDI STORES PAGE**
- **MAKE SURE TGT UFC IS NOT BOXED**
- **Use Delay Spin Wheel to Set the Amount of Time to Tab Back into Game**
## Takes 4 JDAM Coords in the form:
```
LAT
LONG
ALT
LAT
LONG
ALT
LAT
LONG
ALT
LAT
LONG
ALT
```
Where the lat long and alt are pure numbers with positive designating North and East and negative designating South and West
Expects PP1-4 to be vertical with no headers/footers

# ::KEYBINDS MUST INCLUDE::
```
   NUM 0-9         UFC 0-9
   ENTER           UFC ENTER (NOT numEnter, regular enter)
   LALT+NUM1-5     UFC Option Select 1-5
   LCTRL+NUM1-4    LEFT MDI PB 6-9
   LCTRL+NUM6      LEFT MDI PB 18
   LCTRL+NUM7      LEFT MDI PB 4
   LCTRL+NUM8      LEFT MDI PB 11
   LCTRL+NUM9      LEFT MDI PB 14
```
