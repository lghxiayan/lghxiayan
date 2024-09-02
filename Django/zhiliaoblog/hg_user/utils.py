# -*- coding: utf-8 -*-
import os
from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models

from django.conf import settings


class Message:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=settings.ALIYUN_ACCESS_KEY_ID,
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=settings.ALIYUN_ACCESS_KEY_SECRET
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send_sms(phone_numbers: str, sign_name: str, template_code: str, template_param: str) -> None:
        client = Message.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone_numbers,
            sign_name=sign_name,
            template_code=template_code,
            template_param=template_param
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.send_sms_with_options(send_sms_request, runtime)
            print(f"Response: {resp}")
        except Exception as error:
            print(f"Error: {error}")
