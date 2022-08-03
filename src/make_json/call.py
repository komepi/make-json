import argparse
from pathlib import Path
from make_json.app import ShapingDict, JSON2DICT, DICT2JSON

def main():
    parser = argparse.ArgumentParser(description=Descriptions.program)
    parser.add_argument('input', type=str, help=Descriptions.input)
    parser.add_argument('mode', choices=['d', 'j'],help=Descriptions.mode)
    parser.add_argument('--file','-f',action='store_true', help=Descriptions.file)
    parser.add_argument('-indent', type=int, default=2, help=Descriptions.indent)
    args = parser.parse_args()
    if args.mode == 'd':
        mode = JSON2DICT
    elif args.mode == 'j':
        mode = DICT2JSON
    if args.file:
        path = Path(args.input)
        if path.exists() and path.is_file():
            with open(path, "r") as f:
                data = f.read()
        else:
            raise Exception("ファイルが存在しません")
    else:
        data = args.input
    change_tool = ShapingDict(args.indent, mode)
    result = change_tool.dict2json(data)
    print(result)
    
class Descriptions:
    program = \
    "これは辞書型の文字列を整形するプログラムです。以下の変換に対応しています。\n"+\
    " * pythonやjsonの辞書型を整形する\n"+\
    " * pythonからjson、jsonからpythonの辞書型に変換し整形する\n"+\
    " 後者の変換では以下の処理をしています\n"+\
    "例）jsonからpythonの辞書型にする場合\n"+\
    " * true->True, false->False, null->Noneの変換"
    
    input = "変換する文字列、もしくは文字列が格納されたテキストファイル。この時テキストファイルは変換する文字列１行のみが格納されたものにしてください"
    mode = "pythonの辞書型にするのか、jsonの辞書型にするのか。pythonの場合はd、jsonの場合はjを指定"
    file = "inputに指定したものがファイル名なのか文字列なのか。ファイル名の場合はこのオプションを追加"
    indent = "整形した際に、空白をいくつにするか。"
if __name__ == "__main__":
    main()