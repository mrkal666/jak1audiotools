import os
import argparse
import subprocess

# Path to JakAudioTool_cmd.exe. Change This.
executable_path = "JakAudioTool_cmd.exe"

# Removes the extesion from filename
def remove_extension(filename):
    if filename.endswith(".vag"):
        return filename[:-4]  # Remove the last 4 characters (".vag")
    else:
        return filename

# Combines all .vag files into one big file
def combine_files(directory, output_file):
    fileStart = 0
    with open(output_file, 'wb') as outfile:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as infile:
                    file_data = infile.read()
                    outfile.write(file_data)
                    print(f"False;{remove_extension(filename)};{int(fileStart / 2048)}")
                    append_to_file(os.environ.get("TEMP") + "\\jak1vagdir.txt", f"False;{remove_extension(filename)};{int(fileStart / 2048)}\n")
                    fileStart += len(file_data)

    print("Files combined successfully!")

# Adds text to a text file
def append_to_file(file_path, string_to_append):
    with open(file_path, 'a') as file:
        file.write(string_to_append)

parser = argparse.ArgumentParser(description="Creates JAK VAGWAD files")


parser.add_argument("-d", dest="directory_path", required=True, 
                    help="Directory that contains .vag files", metavar="DIRECTORY")

parser.add_argument("-wad", dest="output_file_path", required=True, 
                    help="VAGWAD output file path", metavar="FILE")

parser.add_argument("-vagdir", dest="vagdir", required=True, 
                    help="VAGDIR.ayb output file path", metavar="FILE")

args = parser.parse_args()

if os.path.exists(os.environ.get("TEMP") + "\\jak1vagdir.txt"):
    os.remove(os.environ.get("TEMP") + "\\jak1vagdir.txt")
    print("File deleted.")
else:
    print("File does not exist.")
combine_files(args.directory_path, args.output_file_path)
arguments = [os.environ.get("TEMP") + "\\jak1vagdir.txt", args.vagdir]
subprocess.run([executable_path] + arguments)

