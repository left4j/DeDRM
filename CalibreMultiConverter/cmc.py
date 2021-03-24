import os, json

# Add calibre cli tools to system PATH. If already there, does nothing
os.system("set PATH=%PATH%;C:\Program Files\Calibre2\app\bin")

# Ask the user to input the directory they want the converted files to go to
out_dir = str(input('\n'"Paste the path of the output directory here. If it's the current directory, type cwd"'\n'))
if out_dir == "cwd":
    out_dir = os.getcwd()
    os.system(f'cd "{out_dir}"')
else:
    os.system(f'cd "{out_dir}"')

# Before adding new books, retrieve the existing library ids. Will be used for comparison later
os.system("calibredb list --for-machine > ids_b4.json")

# Get the name of the account currently logged in
usr = os.getlogin()

# Add books downloaded from the Kindle app or Adobe Digital Editions (Google Books) to calibre library. If they're already added, are skipped. 
# This uses the default storage locations. If you changed them, also change the path
os.system(f'calibredb add "C:\\Users\\{usr}\\Documents\\My Kindle Content"')
os.system(f'calibredb add "C:\\Users\\{usr}\\Documents\\My Digital Editions"')

# Output a list of updated library entries into a JSON file
os.system("calibredb list --for-machine > ids.json")

# Read the JSON files, getting the IDs of the newly added books
db_b4 = "ids_b4.json"
db = "ids.json"
data_b4 = json.loads(open(db_b4).read())
data = json.loads(open(db).read())
id_list_b4 = [element['id'] for element in data_b4]
id_list = [element['id'] for element in data]
new_ids = list(set(id_list)-set(id_list_b4))

# Copy the newly added books to the specified directory, following the "title + author" template
for i in new_ids:
    os.system(f'calibredb export {i} --to-dir "{out_dir}" --template "{{title}} - {{authors}}"')

# Delete the now useless JSON files
os.remove("ids_b4.json")
os.remove("ids.json")

# Another version of cd, ensures Python will use the specified path properly
os.chdir(out_dir)

# Scan the contents of the directory
content = os.listdir()

for i in content:
    # Delete useless stuff like standalone cover files and metadata. If you want to keep something from here, just remove its extension from the list
    shit_list = [".jpg", ".png", ".opf", ".xml"]
    if i.endswith(tuple(shit_list)):
        os.remove(i)
    # Get the book title w/o extension
    title = str(os.path.splitext(i)[0])
    # Search for files with extensions used in Kindle books
    ext_list = [".azw", ".azw2", ".azw3", ".azw4", ".mobi", ".kfx"]
    if i.endswith(tuple(ext_list)):
        # Convert the books to EPUB and PDF. Modify according to the formats you want to convert to
        os.system(f'ebook-convert "{i}" "{title}.pdf"')
        os.system(f'ebook-convert "{i}" "{title}.epub"')
        # Remove the original, encrypted book from current directory
        os.remove(i)
    # This bit takes care of EPUB conversion. You can of course add more code to convert to other formats
    elif i.endswith(".epub"):
        os.system(f'ebook-convert "{i}" "{title}.pdf"')
    """
    In case of Google Play books, they come as encrypted PDFs or EPUBs, and for them encryption is removed upon adding to library
    For some reason it's impossible to convert a GPB PDF to anything, it's just stuck forever on 1%. Fortunately the encryption is removed
    so you can just use the PDF itself. That's why there's no code for the PDF extension.
    """
