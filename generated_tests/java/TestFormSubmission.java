/*
 * Auto-generated test script from Excel
 * Test Case: TC004 - Form Submission
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

public class TestFormSubmission {

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

    @Test(description = "Form Submission")
    public void test_form_submission() throws Exception {
        // Step 1: navigate
        driver.get("http://localhost:3000/contact");

        // Step 2: type
        WebElement el2 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("name")));
        el2.clear();
        el2.sendKeys("John Doe");

        // Step 3: type
        WebElement el3 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("email")));
        el3.clear();
        el3.sendKeys("john@example.com");

        // Step 4: type
        WebElement el4 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("message")));
        el4.clear();
        el4.sendKeys("Test message");

        // Step 5: click
        wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//button[@type=\"submit\"]"))).click();

        // Step 6: wait
        Thread.sleep(2000);

        // Step 7: verify_text
        String text7 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".success-message"))).getText();
        Assert.assertTrue(text7.contains("submitted"), "Expected \"submitted\" but got \"" + text7 + "\"");

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
