import os

def fetch_packagejson_and_contents():
    all_files = []
    # ファイルを開き、内容を読み込む
    try:
        with open("./front/package.json", 'r', encoding='utf-8') as file:
            content = file.read()
            all_files.append("- filename:./front/package.json")
            all_files.append("```")
            all_files.append(content)
            all_files.append("```")
            all_files.append("")
    except (UnicodeDecodeError, IOError):
        print("Error reading ./front/package.json. It may not be a text file or might have encoding issues.")
    return '\n'.join(str(elem) for elem in all_files)


def fetch_files_and_contents(directory):
    all_files = []
    
    # os.walk()を使用してディレクトリを再帰的に走査
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # ファイルの完全なパスを取得
            file_path = os.path.join(root, filename)
            
            # ファイルを開き、内容を読み込む
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    all_files.append(f"- filename:{file_path}")
                    all_files.append(f"```")
                    all_files.append(content)
                    all_files.append("```")
                    all_files.append("")
            except (UnicodeDecodeError, IOError):
                print(f"Error reading {file_path}. It may not be a text file or might have encoding issues.")

    return '\n'.join(str(elem) for elem in all_files) 

# 使用例
directory = '/path/to/directory'
files_contents = fetch_files_and_contents(directory)
print(files_contents)

if __name__ == '__main__':
    kekka = fetch_files_and_contents("./front/src")
    print(kekka)
    print(len(kekka))

    print(fetch_packagejson_and_contents())