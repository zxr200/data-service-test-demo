import pytest
from unittest.mock import patch,MagicMock
from data_service import DataService

#测试类
class TestDataService:

    @pytest.fixture
    def data_service(self):
        return DataService()

    @pytest.fixture
    def valid_dataset(self):
        return {'name':'sales_data','rows':1000,'source':'database'}

    @pytest.mark.parametrize("dataset,expected_success,expected_message",[
        ({'name':'sales_data','rows':1000,'source':'db'},True,"数据集验证成功"),
        ({'name':'','rows':1000,'source':'db'},False,"数据集名称不能为空"),
        ({'name':'a','rows':1000,'source':'db'},False,"数据集名称至少为2个字符"),
        ({'name':'sales','rows':None,'source':'db'},False,"数据行数不能为空"),
        ({'name':'sales','rows':-1,'source':'db'},False,"数据行数必须大于0"),
        ({'name':'sales','rows':1000001,'source':'db'},False,"数据行数不能大于1000000"),
        ({'name':'sales','rows':1000,'source':''},False,"数据源不能为空")
    ])

    def test_validate_dataset(self,data_service,dataset,expected_success,expected_message):
        success,message=data_service.validate_dataset(dataset)
        assert success==expected_success
        assert message==expected_message

    @pytest.mark.parametrize("mock_status,expected_success,expected_message",[
        (200,True,"数据处理成功"),
        (500,False,"数据处理失败，状态码：500"),
    ])
    @patch('data_service.requests.post')
    def test_process_dataset_with_mock(self,mock_post,data_service,valid_dataset,mock_status,
                                       expected_success,expected_message):
        mock_response=MagicMock()
        mock_response.status_code=mock_status
        mock_post.return_value=mock_response

        success,message=data_service.process_dataset(valid_dataset)

        assert success==expected_success
        assert message==expected_message

        mock_post.assert_called_once_with(
            'https://api.data-service.com/analyze',
            json=valid_dataset,
            timeout=5
        )

    @patch('data_service.requests.post')
    def test_process_dataset_timeout(self,mock_post,data_service,valid_dataset):
        mock_post.side_effect=TimeoutError("API调用超时")

        success,message=data_service.process_dataset(valid_dataset)

        assert success is False
        assert "超时" in message
