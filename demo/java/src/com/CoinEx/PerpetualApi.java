package com.CoinEx;

import java.awt.HeadlessException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.http.HttpException;


public class PerpetualApi {

	private String secret_key;
	
	private String accessId;
	
	private String url_prex;
	
	public PerpetualApi(String url_prex, String accessId, String secret_key){
		this.accessId = accessId;
		this.secret_key = secret_key;
		this.url_prex = url_prex;
	}
	
	public PerpetualApi(String url_prex){
		this.url_prex = url_prex;
	}

	private final String TICKER_URL = "market/ticker";
	
	private final String DEPTH_URL = "market/depth";
	
	private final String KLINE_URL = "market/kline";
	
	private final String BALANCE_URL = "asset/query";
	
	private final String PENDING_ORDER_URL = "order/pending";
	
	private final String FINISHED_ORDER_URL = "order/finished";

	private final String PUT_LIMIT_URL = "order/put_limit";

	private final String CANCEL_ORDER_URL = "order/cancel";
	
	private enum HTTP_METHOD {
	    GET, POST;
	}
	
	enum ORDER_TYPE {
		BUY("2"), SELL("1");
		
		public final String value;
		private ORDER_TYPE(String value) {
			this.value = value;
		}
		
		public String toString() {
			return this.value;
		}
	}

	private String doRequest(String url, Map<String, String> paramMap, HTTP_METHOD method) throws HeadlessException, IOException, HttpException {
		if (paramMap == null) {
			paramMap = new HashMap<>();
		}
		paramMap.put("timestamp", new Long(System.currentTimeMillis()).toString());
		String params = StringUtil.createLinkString(paramMap);
		
		String authorization = SHA256Util.buildSHA256(params + "&secret_key=" + this.secret_key);
		HttpUtilManager httpUtil = HttpUtilManager.getInstance();
		switch (method) {
		case GET:
			return httpUtil.requestHttpGet(url_prex, url, params, authorization, this.accessId);
			
		case POST:
			return httpUtil.requestHttpPost(url_prex, url, params, authorization, this.accessId);
			
		default:
			return httpUtil.requestHttpGet(url_prex, url, params, authorization, this.accessId);
		}
	}
	
	public String ticker(String market) throws HttpException, IOException {
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
	    return doRequest(TICKER_URL, param, HTTP_METHOD.GET);
	}

	public String depth(String market, String merge, Integer limit) throws HttpException, IOException {
		
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
		param.put("merge", merge);
		param.put("limit", String.valueOf(limit));
	    return doRequest(DEPTH_URL, param, HTTP_METHOD.GET);
	}

	public String kline(String market, String type) throws HttpException, IOException {
		
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
		param.put("type", type);
	    return doRequest(KLINE_URL, param, HTTP_METHOD.GET);
	}

	public String account() throws HttpException, IOException {
		return doRequest(BALANCE_URL, null, HTTP_METHOD.GET);
	}
	
	public String pendingOrder(String market, int page, int account) throws HttpException, IOException {
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
		param.put("page", String.valueOf(page));
		param.put("account", String.valueOf(account));
	    return doRequest(PENDING_ORDER_URL, param, HTTP_METHOD.GET);
	}
	
	public String finishedOrder(String market, String page, String account) throws HttpException, IOException {
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
		param.put("page", page);
		param.put("account", account);
	    return doRequest(FINISHED_ORDER_URL, param, HTTP_METHOD.GET);
	}
	
	public String putLimitOrder(String market, ORDER_TYPE side, float amount, float price) throws HttpException, IOException {
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
		param.put("side", side.toString());
		param.put("amount", String.valueOf(amount));
		param.put("price", String.valueOf(price));
	    return doRequest(PUT_LIMIT_URL, param, HTTP_METHOD.POST);
	}
	
	public String cancelOrder(String market, String orderID) throws HttpException, IOException {
		HashMap<String, String> param = new HashMap<>();
		param.put("market", market);
		param.put("order_id", orderID);
	    return doRequest(CANCEL_ORDER_URL, param, HTTP_METHOD.POST);
	}
}
