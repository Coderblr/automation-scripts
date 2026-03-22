/*
 * Auto-generated test script from Excel
 * Test Case: TC005 - Navigation Test
 * Generated: 2026-03-21 10:30:26
 */

package com.automation.tests;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.*;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.time.Duration;

public class TestNavigationTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeMethod
    public void setUp() {
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--no-sandbox", "--disable-dev-shm-usage");
        driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        wait = new WebDriverWait(driver, Duration.ofSeconds(20));
    }

    @Test(description = "Navigation Test")
    public void test_navigation_test() throws Exception {
        // Step 1: navigate
        driver.get("http://localhost:3000");

        // Step 2: click
        wait.until(ExpectedConditions.elementToBeClickable(By.linkText("About"))).click();

        // Step 3: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("/about"));

        // Step 4: go_back
        driver.navigate().back();

        // Step 5: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("localhost:3000"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
