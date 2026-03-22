/*
 * Auto-generated test script from Excel
 * Test Case: TC001 - Valid Login
 * Generated: 2026-03-21 11:02:04
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

public class TestValidLogin {

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

    @Test(description = "Valid Login")
    public void test_valid_login() throws Exception {
        // Step 1: navigate
        driver.get("https://www.saucedemo.com/v1/");

        // Step 2: verify_title
        Assert.assertTrue(driver.getTitle().contains("Swag Labs"));

        // Step 3: type
        WebElement el3 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("user-name")));
        el3.clear();
        el3.sendKeys("standard_user");

        // Step 4: type
        WebElement el4 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("password")));
        el4.clear();
        el4.sendKeys("secret_sauce");

        // Step 5: click
        wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button"))).click();

        // Step 6: wait
        Thread.sleep(2000);

        // Step 7: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("inventory.html"));

        // Step 8: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 9: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/TC001_login_success.png"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
