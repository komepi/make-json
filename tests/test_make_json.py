
import pytest
import sys, os
from collections import OrderedDict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from make_json.app import DICT2JSON, JSON2DICT, ShapingDict

def mock_exchange(data):
    return '"{}"'.format(data)

class TestShapingDict:
    def test_init(self):
        sd = ShapingDict(indent=1,mode=1,is_shaping=True)
        assert sd.indent == 1
        assert sd.mode == 1
        assert sd.is_shaping == True
        assert sd.newline_str == "\n"
        assert sd.exchange_config == {"true":{"to":"True","from":"true"},"false":{"to":"False","from":"false"},"null":{"to":"None","from":"null"}}

        sd = ShapingDict(indent=2,mode=2,is_shaping=False)
        assert sd.indent == 2
        assert sd.mode == 2
        assert sd.is_shaping == False
        assert sd.newline_str == ""
        assert sd.exchange_config == {"true":{"to":"true","from":"True"},"false":{"to":"false","from":"False"},"null":{"to":"null","from":"None"}}

        
    def test_convert_ordereddict2dict(self):
        data = {'a': OrderedDict([('b', OrderedDict([('c', 3), ('d', 4)])), ('e', [OrderedDict([('f', 6), ('g', 7)]), OrderedDict([('h', 8), ('i', 9)])]), ('j', [10.1, 10.2]), ('k', {'l': 12, 'n': 13})])}
        test = {"a":{"b":{"c":3,"d":4},"e":[{"f":6,"g":7},{"h":8,"i":9}],"j":[10.1,10.2],"k":{"l":12,"n":13}}}
        sd = ShapingDict(2,DICT2JSON)
        result = sd._convert_ordereddict2dict(data)
        assert result == test
    
    def test_convert(self, mocker):
        sd = ShapingDict(2,DICT2JSON)
        data = "not dict or list or OrderedDict"
        with pytest.raises(Exception) as e:
            sd.convert(data)
        assert str(e.value) == '辞書型に形式があっていない'
        convert_dict = "after convert dict"
        convert_list = "after convert list"
        mocker.patch("make_json.app.ShapingDict.dicts",return_value=convert_dict)
        mocker.patch("make_json.app.ShapingDict.lists",return_value=convert_list)
        
        data = "[1,2,3]"
        result = sd.convert(data)
        assert result == convert_list
        data = "{'a':1,'b':2}"
        result = sd.convert(data)
        assert result == convert_dict
        
    def test_dicts(self,mocker):
        mocker.patch("make_json.app.ShapingDict.exchange", side_effect=mock_exchange)
        
        data = {"key1":"value1","key2":"value2","key3":{"key31":"value31","key32":"value32"},"key4":["test41","test42"],"key5":"value5"}
        mode = DICT2JSON
        
        # is_shaping=True
        def mock_lists(value,result,indent):
            return result + '[\n    "test41",\n    "test42"\n  ]'
        mocker.patch("make_json.app.ShapingDict.lists", side_effect = mock_lists)
        sd = ShapingDict(2,mode,is_shaping=True)
        result = ""
        result = sd.dicts(data, result,0)
        test = '{\n  "key1": "value1",\n  "key2": "value2",\n  "key3": {\n    "key31": "value31",\n    "key32": "value32"\n  },\n  "key4": [\n    "test41",\n    "test42"\n  ],\n  "key5": "value5"\n}'
        assert result == test

        # is_shaping=False
        def mock_lists(value,result,indent):
            return result + '["test41","test42"]'
        mocker.patch("make_json.app.ShapingDict.lists", side_effect = mock_lists)
        sd = ShapingDict(2,mode,is_shaping=False)
        result=""
        result = sd.dicts(data, result,0)
        test = '{"key1": "value1","key2": "value2","key3": {"key31": "value31","key32": "value32"},"key4": ["test41","test42"],"key5": "value5"}'
        assert result == test
    
    def test_lists(self, mocker):
        mocker.patch("make_json.app.ShapingDict.exchange", side_effect=mock_exchange)
        mode = DICT2JSON
        data = ["test1", "test2", {"key1":"value1", "key2":"value2"},["test11","test12"],"test3"]
        
        # is_shaping=True

        def mock_dicts(value,result,indent):
            return result + '{\n    "key1": "value1",\n    "key2": "value2"\n  }'
        mocker.patch("make_json.app.ShapingDict.dicts", side_effect = mock_dicts)
        sd = ShapingDict(2,mode,is_shaping=True)
        result = ""
        result = sd.lists(data, result)
        test = '[\n  "test1",\n  "test2",\n  {\n    "key1": "value1",\n    "key2": "value2"\n  },\n  [\n    "test11",\n    "test12"\n  ],\n  "test3"\n]'
        assert result == test

        
        def mock_dicts(value,result,indent):
            return result + '{"key1": "value1","key2": "value2"}'
        mocker.patch("make_json.app.ShapingDict.dicts", side_effect = mock_dicts)
        sd = ShapingDict(2,mode,is_shaping=False)
        result=""
        result = sd.lists(data, result)
        test = '["test1","test2",{"key1": "value1","key2": "value2"},["test11","test12"],"test3"]'
        assert result == test

    str_data = [True, False, None, "true", "false", "null", "", "1", "abc", 1, 1.1]
    result_dict2json = ['true', 'false', 'null', 'true', 'false', 'null', '""', '"1"', '"abc"', '1', '1.1']
    result_json2dict = ['True', 'False', 'None', 'True', 'False', 'None', '""', '"1"', '"abc"', '1', '1.1']
    @pytest.mark.parametrize(('datas', 'result', 'mode'),
                         [
                             (str_data, result_dict2json, DICT2JSON),
                             (str_data, result_json2dict, JSON2DICT)
                         ])
    def test_exchange(self,datas,result,mode):
        tests = list()
        sd = ShapingDict(2,mode)
        for data in datas:
            tests.append(sd.exchange(data))
        assert tests == result