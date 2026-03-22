/*
 * Auto-generated test script from Excel
 * Test Case: TC003 - Locked Out User
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

public class TestLockedOutUser {

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

    @Test(description = "Locked Out User")
    public void test_locked_out_user() throws Exception {
        // Step 1: navigate
        driver.get("https://www.saucedemo.com/v1/");

        // Step 2: type
        WebElement el2 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("user-name")));
        el2.clear();
        el2.sendKeys("locked_out_user");

        // Step 3: type
        WebElement el3 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("password")));
        el3.clear();
        el3.sendKeys("secret_sauce");

        // Step 4: click
        wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button"))).click();

        // Step 5: wait
        Thread.sleep(1000);

        // Step 6: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 7: verify_text
        String text7 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("h3[data-test=\"error\"]"))).getText();
        Assert.assertTrue(text7.contains("locked out"), "Expected \"locked out\" but got \"" + text7 + "\"");

        // Step 8: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/TC003_locked_out_error.png"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
