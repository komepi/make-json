
import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from make_json.app import DICT2JSON, JSON2DICT, ShapingDict

str_data = ["True", "False", "None", "true", "false", "null", "", "1", "abc"]
result_dict2json = ['true', 'false', 'null', 'true', 'false', 'null', '""', '1', '"abc"']
result_json2dict = ['True', 'False', 'None', 'True', 'False', 'None', '""', '1', '"abc"']

@pytest.mark.parametrize(('datas', 'result', 'mode'),
                         [
                             (str_data, result_dict2json, DICT2JSON),
                             (str_data, result_json2dict, JSON2DICT)
                         ])
def test_exchange(datas, result, mode):
    tests = list()
    sd = ShapingDict(2,mode)
    for data in datas:
        tests.append(sd.exchange(data))
    assert tests == result

def mock_exchange(data):
    return '"{}"'.format(data)

def test_lists(mocker):
    mode = DICT2JSON
    sd = ShapingDict(2,mode)
    data = ["test1", "test2", {"key1":"value1", "key2":"value2"},["test11","test12"],"test3"]
    test = ""
    def mock_dicts(value,result,indent):
        return result + '{\n    "key1": "value2",\n    "key2": "value2"\n  }'
    mocker.patch("make_json.app.ShapingDict.exchange", side_effect=mock_exchange)
    mocker.patch("make_json.app.ShapingDict.dicts", side_effect = mock_dicts)
    test = sd.lists(data, test)
    result = '[\n  "test1",\n  "test2",\n  {\n    "key1": "value2",\n    "key2": "value2"\n  },\n  [\n    "test11",\n    "test12"\n  ],\n  "test3"\n]'
    assert test == result

def test_dicts(mocker):
    data = {"key1":"value1","key2":"value2","key3":{"key31":"value31","key32":"value32"},"key4":["test41","test42"],"key5":"value5"}
    test = ""
    mode = DICT2JSON
    sd = ShapingDict(2,mode)
    def mock_lists(value,result,indent):
        return result + '[\n    "test41",\n    "test42"\n  ]'
    mocker.patch("make_json.app.ShapingDict.exchange", side_effect=mock_exchange)
    mocker.patch("make_json.app.ShapingDict.lists", side_effect = mock_lists)
    test = sd.dicts(data, test,0)
    result = '{\n  "key1": "value1",\n  "key2": "value2",\n  "key3": {\n    "key31": "value31",\n    "key32": "value32"\n  },\n  "key4": [\n    "test41",\n    "test42"\n  ],\n  "key5": "value5"\n}'
    assert test == result

def test_dict2json(mocker):
    mode = DICT2JSON
    data = "not dict or list"
    sd = ShapingDict(2,mode)
    with pytest.raises(Exception) as e:
        sd.dict2json(data)
    assert str(e.value) == '辞書型に形式があっていない'
    result_lists = "result from lists"
    result_dicts = "result from dicts"
    mocker.patch("make_json.app.ShapingDict.lists", return_value = result_lists)
    mocker.patch("make_json.app.ShapingDict.dicts", return_value = result_dicts)
    
    data_list = "[1,2,3]"
    test_list = sd.dict2json(data_list)
    assert test_list == result_lists
    
    data_dict = "{1:1,2:2,3:3}"
    test_dict = sd.dict2json(data_dict)
    assert test_dict == result_dicts