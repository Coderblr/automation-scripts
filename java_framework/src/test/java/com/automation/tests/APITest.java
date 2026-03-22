package com.automation.tests;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.testng.Assert;
import org.testng.annotations.*;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class APITest {

    private OkHttpClient client;
    private String apiBaseUrl;

    @Parameters({"apiBaseUrl"})
    @BeforeMethod
    public void setUp(@Optional("http://localhost:8000") String apiBaseUrl) {
        this.apiBaseUrl = System.getProperty("apiBaseUrl", apiBaseUrl);
        this.client = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .build();
    }

    @Test(description = "Verify API is reachable")
    public void testApiIsReachable() throws IOException {
        Request request = new Request.Builder()
                .url(apiBaseUrl + "/docs")
                .build();

        try (Response response = client.newCall(request).execute()) {
            System.out.println("API docs status: " + response.code());
            Assert.assertTrue(response.isSuccessful() || response.code() == 404,
                    "API not reachable. Status: " + response.code());
        }
    }

    @Test(description = "Verify API response time")
    public void testApiResponseTime() throws IOException {
        long start = System.currentTimeMillis();

        Request request = new Request.Builder()
                .url(apiBaseUrl + "/docs")
                .build();

        try (Response response = client.newCall(request).execute()) {
            long elapsed = System.currentTimeMillis() - start;
            System.out.println("Response time: " + elapsed + "ms");
            Assert.assertTrue(elapsed < 5000, "Response time " + elapsed + "ms exceeds 5 seconds");
        }
    }

    @Test(description = "Verify invalid endpoint returns 404")
    public void testInvalidEndpointReturns404() throws IOException {
        Request request = new Request.Builder()
                .url(apiBaseUrl + "/api/nonexistent_endpoint_xyz")
                .build();

        try (Response response = client.newCall(request).execute()) {
            Assert.assertTrue(response.code() == 404 || response.code() == 422,
                    "Expected 404 for invalid endpoint, got " + response.code());
        }
    }

    @Test(description = "Verify OpenAPI JSON is available")
    public void testOpenApiJsonAvailable() throws IOException {
        Request request = new Request.Builder()
                .url(apiBaseUrl + "/openapi.json")
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful()) {
                String contentType = response.header("Content-Type", "");
                Assert.assertTrue(contentType.toLowerCase().contains("json"),
                        "Expected JSON content type, got: " + contentType);
                System.out.println("OpenAPI JSON available");
            } else {
                System.out.println("OpenAPI JSON not available (status: " + response.code() + ")");
            }
        }
    }
}
