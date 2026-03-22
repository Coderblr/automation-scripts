package com.automation.utils;

import com.automation.base.BasePage;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;

import java.util.Map;

/**
 * Keyword-Driven Engine for Java.
 * Reads action keywords from Excel and executes Selenium operations.
 * Supports ${variable} placeholders that resolve from config.ini.
 */
public class KeywordEngine {

    private final WebDriver driver;
    private final BasePage page;

    public KeywordEngine(WebDriver driver) {
        this.driver = driver;
        this.page = new BasePage(driver);
    }

    public void executeStep(Map<String, String> step) throws Exception {
        String action = step.getOrDefault("Action", "").trim().toLowerCase();
        String locatorType = step.getOrDefault("Locator_Type", "").trim();
        String locatorValue = ConfigReader.resolveVariables(step.getOrDefault("Locator_Value", "").trim());
        String testData = ConfigReader.resolveVariables(step.getOrDefault("Test_Data", "").trim());
        String expected = ConfigReader.resolveVariables(step.getOrDefault("Expected_Result", "").trim());

        System.out.println("  Executing: " + action + " | " + locatorType + "=" + locatorValue +
                " | Data: " + testData + " | Expected: " + expected);

        switch (action) {
            case "navigate": case "go_to_url": case "open_url":
                String url = !testData.isEmpty() ? testData : locatorValue;
                page.navigateTo(url);
                break;

            case "click":
                page.click(locatorType, locatorValue);
                break;

            case "type": case "send_keys": case "enter_text":
                page.typeText(locatorType, locatorValue, testData);
                break;

            case "clear":
                page.clearField(locatorType, locatorValue);
                break;

            case "select_dropdown": case "select":
                page.selectDropdown(locatorType, locatorValue, testData);
                break;

            case "verify_text": case "assert_text":
                page.verifyText(locatorType, locatorValue, !expected.isEmpty() ? expected : testData);
                break;

            case "verify_title": case "assert_title":
                page.verifyTitle(!expected.isEmpty() ? expected : testData);
                break;

            case "verify_url":
                page.verifyUrlContains(!expected.isEmpty() ? expected : testData);
                break;

            case "verify_element_present":
                if (!page.isElementPresent(locatorType, locatorValue)) {
                    throw new AssertionError("Element not present: " + locatorType + "=" + locatorValue);
                }
                break;

            case "verify_element_visible":
                if (!page.isElementVisible(locatorType, locatorValue)) {
                    throw new AssertionError("Element not visible: " + locatorType + "=" + locatorValue);
                }
                break;

            case "hover": case "mouse_over":
                page.hover(locatorType, locatorValue);
                break;

            case "double_click":
                page.doubleClick(locatorType, locatorValue);
                break;

            case "right_click":
                page.rightClick(locatorType, locatorValue);
                break;

            case "wait": case "sleep":
                double seconds = !testData.isEmpty() ? Double.parseDouble(testData) :
                        !locatorValue.isEmpty() ? Double.parseDouble(locatorValue) : 2;
                page.waitSeconds(seconds);
                break;

            case "scroll_down":
                int downPixels = !testData.isEmpty() ? Integer.parseInt(testData) : 500;
                page.scrollDown(downPixels);
                break;

            case "scroll_up":
                int upPixels = !testData.isEmpty() ? Integer.parseInt(testData) : 500;
                page.scrollUp(upPixels);
                break;

            case "scroll_to_element":
                page.scrollToElement(locatorType, locatorValue);
                break;

            case "switch_frame":
                page.switchToFrame(locatorType, locatorValue);
                break;

            case "switch_default":
                page.switchToDefaultContent();
                break;

            case "accept_alert":
                page.acceptAlert();
                break;

            case "dismiss_alert":
                page.dismissAlert();
                break;

            case "take_screenshot": case "screenshot":
                String screenshotName = !testData.isEmpty() ? testData : locatorValue;
                page.takeScreenshot(screenshotName);
                break;

            case "refresh":
                page.refresh();
                break;

            case "go_back":
                page.goBack();
                break;

            case "open_browser": case "close_browser":
                break;

            default:
                throw new UnsupportedOperationException("Unknown action: " + action);
        }
    }

    /**
     * Clear browser state between test cases (cookies, localStorage, sessionStorage).
     */
    public void clearBrowserState() {
        try {
            driver.manage().deleteAllCookies();
            ((JavascriptExecutor) driver).executeScript("window.localStorage.clear();");
            ((JavascriptExecutor) driver).executeScript("window.sessionStorage.clear();");
        } catch (Exception e) {
            // Ignore errors during cleanup
        }
    }
}
