import os


def generate_reference_md(project_name, output_file):
    """
    指定したプロジェクトの全モジュールを列挙し、reference.md を生成します。

    Args:
        project_name (str): プロジェクトのトップレベルモジュール名。
        output_file (str): 出力するMarkdownファイルのパス。
    """
    modules = []
    for root, _, files in os.walk(project_name):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)
                module = module_path.replace("/", ".").replace("\\", ".")[:-3]
                if module.startswith(project_name):
                    modules.append(module)

    with open(output_file, "w") as f:
        f.write("# API Reference\n\n")
        for module in modules:
            f.write(f"## モジュール: {module}\n\n")
            f.write(f"::: {module}\n\n")


def execute_generate_reference_recursively(base_directory, output_file="reference.md"):
    """
    指定ディレクトリ配下のすべての .py ファイルを対象に reference.md を生成します。

    Args:
        base_directory (str): 探索を開始するディレクトリのパス。
        output_file (str): 出力するMarkdownファイルの名前。
    """
    # プロジェクト名をディレクトリ名から推定
    project_name = os.path.basename(os.path.abspath(base_directory))
    
    # 出力ファイルのフルパス
    output_file_path = output_file
     
    print(f"Generating API reference for project: {project_name}")
    print(f"Output file: {output_file_path}")
    
    # generate_reference_md を実行
    generate_reference_md(project_name, output_file_path)
    print("API reference generation completed.")


# 実行例
if __name__ == "__main__":
    base_directory = "./app"  # 対象ディレクトリを指定
    execute_generate_reference_recursively(base_directory, "./docs/reference.md")
