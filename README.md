# make-json
文字列の辞書型を整形します。
また、JSONをpythonの辞書型に、もしくはその逆に変換します。

## 辞書型の整形
以下のように整形します。
 * 整形前
    ```
    {'a':None,'b':{'c':'test1','d':2},'e':[{'f':[1,2,3],'g':1,'h':{'i':1,'j':2}}]}
    ```
 * 整形後
    ```
    {
      "a": None,
      "b": {
        "c": "test1",
        "d": "2"
      },
      "e": [
        {
          "f": [
            "1",
            "2",
            "3"
          ],
          "g": "1",
          "h": {
            "i": "1",
            "j": "2"
          }
        }
      ]
    }
    ```

## JSON ⇔ python
以下にしたがって文字列を変換します。
|JSON|Python|
|:--|:--|
|true|True|
|false|False|
|null|None|

## 使用方法
コマンドラインにコマンドを打ち込むことで使用します。
```cmd
$ make_json "{'a':1,'b':2}" d
{
  "a": "1",
  "b": "2"
}
```
コマンドライン引数として第一に変換したい文字列、第二にモードを入力します。入力できるモードは以下の通りです。
|記号|意味|
|:--|:--|
|d|pythonの辞書型に変換|
|j|jsonに変換|
また、第一の文字列にはファイル名を指定することもできます。その場合、オプションとして`--file`もしくは`-f`が必要です。このときそのファイルは変換したい文字列１行のみである場合があります。
またオプションとして整形時のインデントのスペース数を指定することができます。デフォルトでは2です。`-indent`で整数を指定してください。以下例。
```
$ make_json input.txt d -f -indent 4
{
    "a": "1",
    "b": "2"
}
```