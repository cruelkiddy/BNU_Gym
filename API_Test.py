from fateadm_api import FateadmApi
def Return_Valid_Num():
    pd_id =     # pd信息
    pd_key =
    app_id =      # 开发者分成用的账号
    app_key =
    # 识别类型
    pred_type = "20400"
    api = FateadmApi(app_id, app_key, pd_id, pd_key)
    # 查询余额
    balance = api.QueryBalcExtend()   # 直接返余额
    # api.QueryBalc()

# 通过文件形式识别：暂时跳过识别验证码

    file_name = "Kaptcha.png"
    result = api.PredictFromFileExtend(pred_type,file_name)   # 直接返回识别结果
    return result

'''rsp = api.PredictFromFile(pred_type, file_name)  # 返回详细识别结果

just_flag = False
if just_flag:
    if rsp.ret_code == 0:
        #识别的结果如果与预期不符，可以调用这个接口将预期不符的订单退款
        # 退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
        api.Justice( rsp.request_id)
#card_id         = "123"
#card_key        = "123"
#充值
#api.Charge(card_id, card_key)
print(rsp.pred_rsp.value)
'''