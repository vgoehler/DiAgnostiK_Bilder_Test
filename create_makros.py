import re
import os

ignore_dirs = ['Collections']

makros_setup = '''<!--
author: Volker Göhler, Niklas Werner
email: volker.goehler@informatik.tu-freiberg
version: 0.2.0
repository: https://github.com/vgoehler/DiAgnostiK_Bilder_Test 

@diagnostik_url: https://raw.githubusercontent.com/vgoehler/DiAgnostiK_Bilder_Test/refs/heads/main/img

@diagnostik_image: <img src="@0/@1" alt="@1" style="height: @2rem">
'''

location = 'https://raw.githubusercontent.com/vgoehler/DiAgnostiK_Bilder_Test/refs/heads/main/makros.md'

how_to_use = f'''
# Link zu LiaScript

[![LiaScript Course](https://raw.githubusercontent.com/LiaScript/LiaScript/master/badges/course.svg)](https://liascript.github.io/course/?{location})

[![LiaScript LiveEditor](https://raw.githubusercontent.com/LiaScript/LiaScript/refs/heads/development/badges/editor.svg)](https://liascript.github.io/LiveEditor/?/show/file/{location})



> Diese Datei ist automatisch generiert und enthält Makros für die DiAgnostiK-Bilder.

# Anleitung

Der Befehl zum einbinden eines Bildes lautet `@<Bereich>.<Name>(Größe)`
Hängt man statt der Größe `.src` an den Befehl an, so wird der Link zum Bild angezeigt.
Der Bereich ist der Ordnername, in dem sich das Bild befindet.
Der Name ist der Dateiname ohne Endung.
Alle Bilder sowie ihre Bereiche und die Befehle um sie zu laden sind in den Tabellen weiter unten abgebildet.
Die Größe ist in Zeilen angegeben, die das Bild hoch sein soll.
Die Anzeige benötigt LiaScript!

## Beispiel

`@Brandschutzzeichen.Brandbekaempfung(10)`

@Brandschutzzeichen.Brandbekaempfung(10)

`@Brandschutzzeichen.Brandbekaempfung.src`

@Brandschutzzeichen.Brandbekaempfung.src

`@Gefahrstoffe.Explosiv(10)`

@Gefahrstoffe.Explosiv(10)

`@Gefahrstoffe.Explosiv.src`

@Gefahrstoffe.Explosiv.src

## Bereiche und Befehle

Im Nachfolgenden sind alle Bilder aller Bereiche und passende Befehle aufgelistet, die in dieser Sammlung enthalten sind.
'''

UMLAUT_MAP = {
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'
}

def process_folders(base_path):
    img_path = os.path.join(base_path, 'img')
    makros = [makros_setup]
    showcase = [how_to_use]

    for entry in os.listdir(img_path):
        full_path = os.path.join(img_path, entry)

        if os.path.isdir(full_path) and entry not in ignore_dirs:
            showcase.append(f"\n### {entry}\n\n|Bild|Name|Befehl|\n|---|---|---|")
            process_file(full_path, makros, showcase)

    makros.append("\n-->\n")

    return "\n".join(makros) + "\n".join(showcase)

def process_file(parent_folder, makros, showcase):
    """This writes a makro and a showcase for all files in a given folder."""
    for item in os.listdir(parent_folder):
        filename = get_name(item)
        entry = os.path.basename(parent_folder)
        makros.append("")
        makros.append(f'@{entry}.{filename}.src: @diagnostik_url/{entry}/{item}')
        makros.append(f'@{entry}.{filename}: @diagnostik_image(@diagnostik_url,{entry}/{item},@0)')

        showcase.append(f"|@{entry}.{filename}(10)|`{item}`|`@{entry}.{filename}(10)`|")

def get_name(filepath):
    """this returns the name of the image file without the extension."""
    filename = os.path.splitext(os.path.basename(filepath))[0]
    pattern = '[' + ''.join(map(re.escape, UMLAUT_MAP.keys())) + ']'
    filename = re.sub(pattern, replace_umlaut, filename)
    return re.sub(r'[^a-zA-Z0-9_]', '_', filename)

def replace_umlaut(match):
            char = match.group(0)
            return UMLAUT_MAP.get(char, char)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = process_folders(current_dir)
    makros_path = os.path.join(current_dir, "makros.md")
    with open(makros_path, "w", encoding="utf-8") as f:
        f.write(text)
