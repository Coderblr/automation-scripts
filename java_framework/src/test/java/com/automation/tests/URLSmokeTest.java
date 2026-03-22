package com.automation.tests;

import com.automation.base.BaseDriver;
import com.automation.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.testng.Assert;
import org.testng.annotations.*;

import java.util.List;

public class URLSmokeTest {

    private WebDriver driver;
    private BasePage page;
    private String testUrl;

    @Parameters({"browser", "baseUrl"})
    @BeforeMethod
    public void setUp(@Optional("chrome") String browser,
                      @Optional("http://localhost:3000") String baseUrl) {
        driver = BaseDriver.createDriver(browser);
        page = new BasePage(driver);
        testUrl = System.getProperty("testUrl", baseUrl);
    }

    @Test(description = "Verify page loads successfully")
    public void testPageLoads() {
        page.navigateTo(testUrl);
        Assert.assertNotNull(driver.getTitle(), "Page failed to load");
        System.out.println("Page loaded. Title: " + driver.getTitle());
    }

    @Test(description = "Verify page title is not empty")
    public void testPageTitleExists() {
        page.navigateTo(testUrl);
        String title = driver.getTitle();
        Assert.assertFalse(title.trim().isEmpty(), "Page title is empty");
        System.out.println("Page title: " + title);
    }

    @Test(description = "Verify page has content")
    public void testPageHasContent() {
        page.navigateTo(testUrl);
        WebElement body = driver.findElement(By.tagName("body"));
        String bodyText = body.getText();
        Assert.assertFalse(bodyText.trim().isEmpty(), "Page body is empty");
        System.out.println("Page has " + bodyText.length() + " characters of content");
    }

    @Test(description = "Verify no broken images")
    public void testNoBrokenImages() {
        page.navigateTo(testUrl);
        @SuppressWarnings("unchecked")
        List<String> brokenImages = (List<String>) page.executeJs(
                "var images = document.querySelectorAll('img');" +
                "var broken = [];" +
                "images.forEach(function(img) {" +
                "  if (!img.complete || img.naturalHeight === 0) { broken.push(img.src); }" +
                "});" +
                "return broken;"
        );
        Assert.assertEquals(brokenImages.size(), 0,
                "Found " + brokenImages.size() + " broken images: " + brokenImages);
    }

    @Test(description = "Verify page loads within 10 seconds")
    public void testPageLoadPerformance() {
        page.navigateTo(testUrl);
        Long loadTime = (Long) page.executeJs(
                "return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;"
        );
        System.out.println("Page load time: " + loadTime + "ms");
        Assert.assertTrue(loadTime < 10000, "Page load time " + loadTime + "ms exceeds 10 seconds");
    }

    @Test(description = "Capture page screenshot")
    public void testTakeScreenshot() {
        page.navigateTo(testUrl);
        String path = page.takeScreenshot("smoke_test_java");
        Assert.assertNotNull(path, "Screenshot was not saved");
        System.out.println("Screenshot saved: " + path);
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
