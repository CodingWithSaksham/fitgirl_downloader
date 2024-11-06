from os import listdir


def print_txt_files():
    txt_dir = [file for file in listdir() if file.endswith(".txt")]
    for i in txt_dir:
        print(i)

def format_filename():
    print_txt_files()
    user_input = input("Enter file name from the above text files: ")
    if not user_input.startswith("./"):
        user_input = f"./{user_input}"  # Prepend './' if missing
    if not user_input.endswith(".txt"):
        user_input = f"{user_input}.txt"  # Append '.txt' if missing
    return user_input