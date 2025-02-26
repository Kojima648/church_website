let EPayInWx = function(businessType, businessId, wxOpenId, amount, callback) {
    $.ajax({
        url: edomain + 'api/pay/order',
        type: "post",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            amount: amount,
            businessId: businessId,
            businessType: businessType,
            payType: "wxpay",
            openId: wxOpenId,
            tradeType: "jsapi"
        }),
        success: function (data, dataStatus) {
            WeixinJSBridge.invoke(
                'getBrandWCPayRequest', data.content.detail,
                function (res) {
                    if (res.err_msg == "get_brand_wcpay_request:ok") {
                        callback(true);
                    } else {
                        callback(false);
                    }
                });
        }
    });
}

let EPayInWeb = function(businessType, businessId, amount, callback) {
    $.ajax({
        url: edomain + 'api/pay/order',
        type: "post",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            amount: amount,
            businessId: businessId,
            businessType: businessType,
            payType: "wxpay",
            tradeType: "native"
        }),
        success: function (data, dataStatus) {
            callback(data.content.detail.code_url);
        }
    });
}