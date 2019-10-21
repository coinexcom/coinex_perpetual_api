package com.CoinEx;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.commons.io.IOUtils;
import org.apache.http.HttpEntity;
import org.apache.http.HttpException;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.conn.ConnectionKeepAliveStrategy;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultConnectionKeepAliveStrategy;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.protocol.HttpContext;

import com.alibaba.fastjson.JSON;


public class HttpUtilManager {

	private static HttpUtilManager instance = new HttpUtilManager();
	private static HttpClient client;
	public  static PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();  
	private static ConnectionKeepAliveStrategy keepAliveStrat = new DefaultConnectionKeepAliveStrategy() {  

	     public long getKeepAliveDuration(  
	            HttpResponse response,  
	            HttpContext context) {  
	        long keepAlive  = super.getKeepAliveDuration(response, context);  
	        
	        if (keepAlive == -1) {  
	            keepAlive = 5000;  
	        }  
	        return keepAlive;  
	    }  
	  
	};
	private HttpUtilManager() {
		client = HttpClients.custom().setConnectionManager(cm).setKeepAliveStrategy(keepAliveStrat).build(); 
	}

	private static RequestConfig requestConfig = RequestConfig.custom()
	        .setSocketTimeout(20000)
	        .setConnectTimeout(20000)
	        .setConnectionRequestTimeout(20000)
	        .build();
	
	
	public static HttpUtilManager getInstance() {
		return instance;
	}

	public HttpClient getHttpClient() {
		return client;
	}

	private HttpPost httpPostMethod(String url, String authorization) {
		HttpPost method = new HttpPost(url);
		method.setHeader("Content-Type", "application/json");
		method.setHeader("Authorization", authorization);
		return method;
	}

	private  HttpRequestBase httpGetMethod(String url, String authorization) {
		HttpGet method = new HttpGet(url);
		method.setHeader("Content-Type", "application/json");
		method.setHeader("Authorization", authorization);
		return method;
	}
	
	public String requestHttpGet(String url_prex, String url, String param, String authorization, String accessId) throws HttpException, IOException{
		
		url=url_prex+url + "?" + param;
		
		HttpRequestBase method = this.httpGetMethod(url, authorization);
		method.setHeader("AccessId", accessId);
		method.setConfig(requestConfig);
		HttpResponse response = client.execute(method);
		HttpEntity entity =  response.getEntity();
		if(entity == null){
			return "";
		}
		InputStream is = null;
		String responseData = "";
		try{
		    is = entity.getContent();
		    responseData = IOUtils.toString(is, "UTF-8");
		}finally{
			if(is!=null){
			    is.close();
			}
		}
		return responseData;
	}
	
	public String requestHttpPost(String url_prex, String url, String params, String authorization, String accessId) throws HttpException, IOException{
		
		url=url_prex+url;
		Logger.getGlobal().log(Level.INFO, url);
		Logger.getGlobal().log(Level.INFO, params);
		HttpPost method = this.httpPostMethod(url, authorization);
		method.setHeader("AccessId", accessId);
		StringEntity sendEntity = new StringEntity(params);
		method.setEntity(sendEntity);
		method.setConfig(requestConfig);
		HttpResponse response = client.execute(method);
		HttpEntity entity =  response.getEntity();
		if(entity == null){
			return "";
		}
		InputStream is = null;
		String responseData = "";
		try{
		    is = entity.getContent();
		    responseData = IOUtils.toString(is, "UTF-8");
		}finally{
			if(is!=null){
			    is.close();
			}
		}
		return responseData;
	}

}

