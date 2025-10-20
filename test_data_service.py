import pytest
from unittest.mock import patch,MagicMock
from data_service import DataService #导入要测试的类DataService

#测试类
class TestDataService:

    @pytest.fixture
    def data_service(self): #data_service()创建一个DataService实例，供多个测试使用
        return DataService()

    @pytest.fixture
    def valid_dataset(self):#valid_dataset()提供一个有效的测试数据集
        return {'name':'sales_data','rows':1000,'source':'database'}

    #参数化测试装饰器
    #第一个参数是变量名dataset,expected_success,expected_message
    #第二个参数是测试用例表
    @pytest.mark.parametrize("dataset,expected_success,expected_message",[
        ({'name':'sales_data','rows':1000,'source':'db'},True,"数据集验证成功"),
        ({'name':'','rows':1000,'source':'db'},False,"数据集名称不能为空"),
        ({'name':'a','rows':1000,'source':'db'},False,"数据集名称至少为2个字符"),
        ({'name':'sales','rows':None,'source':'db'},False,"数据行数不能为空"),
        ({'name':'sales','rows':-1,'source':'db'},False,"数据行数必须大于0"),
        ({'name':'sales','rows':1000001,'source':'db'},False,"数据行数不能大于1000000"),
        ({'name':'sales','rows':1000,'source':''},False,"数据源不能为空")
    ]) #7个测试用例
    #test_validate_dataset()对validate_dataset()进行测试
    def test_validate_dataset(self,data_service,dataset,expected_success,expected_message):
        success,message=data_service.validate_dataset(dataset)#调用validate_dataset()处理测试数据
        #检查实际结果与期望结果是否一致
        assert success==expected_success
        assert message==expected_message

    #测试正常的响应情况
    @pytest.mark.parametrize("mock_status,expected_success,expected_message",[
        (200,True,"数据处理成功"),
        (500,False,"数据处理失败，状态码：500"),
    ]) #2个测试用例
    @patch('data_service.requests.post') #把真实的requests.post替换成模拟的mock_post
    def test_process_dataset_with_mock(self,mock_post,data_service,valid_dataset,mock_status,
                                       expected_success,expected_message):#参数顺序：1.patch参数 2.Fixture参数 3.参数化参数
        mock_response=MagicMock() #创建一个假的响应对象
        mock_response.status_code=mock_status #status_code固有属性 设置假响应的状态码
        mock_post.return_value=mock_response #return_value固有属性 让模拟的post方法返回假响应

        success,message=data_service.process_dataset(valid_dataset)#调用process_dataset()

        #测试代码能否正常响应
        assert success==expected_success
        assert message==expected_message

        #验证是否用了正确的参数调用的post方法
        #          断言   被调用  一次  带着这些参数   assert_called_once_with固有方法
        mock_post.assert_called_once_with(
            'https://api.data-service.com/analyze',
            json=valid_dataset,
            timeout=5
        )


    #测试超时情况
    @patch('data_service.requests.post')
    def test_process_dataset_timeout(self,mock_post,data_service,valid_dataset):
        mock_post.side_effect=TimeoutError("API调用超时")#side_effect是固有属性
                                                       #让模拟的post方法抛出超时异常
        success,message=data_service.process_dataset(valid_dataset)#调用process_dataset()

        #测试代码能否正确处理超时情况
        assert success is False
        assert "超时" in message
