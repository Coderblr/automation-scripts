/*
 * Auto-generated test script from Excel
 * Test Case: TC001 - Login Test
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

public class TestLoginTest {

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

    @Test(description = "Login Test")
    public void test_login_test() throws Exception {
        // Step 1: navigate
        driver.get("http://localhost:3000/login");

        // Step 2: type
        WebElement el2 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username")));
        el2.clear();
        el2.sendKeys("testuser");

        // Step 3: type
        WebElement el3 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("password")));
        el3.clear();
        el3.sendKeys("testpass123");

        // Step 4: click
        wait.until(ExpectedConditions.elementToBeClickable(By.id("login-btn"))).click();

        // Step 5: wait
        Thread.sleep(2000);

        // Step 6: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("/dashboard"));

        // Step 7: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/login_success.png"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
