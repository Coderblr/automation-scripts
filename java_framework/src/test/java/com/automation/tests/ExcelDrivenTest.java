package com.automation.tests;

import com.automation.base.BaseDriver;
import com.automation.utils.ConfigReader;
import com.automation.utils.ExcelHandler;
import com.automation.utils.KeywordEngine;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.*;

import java.io.File;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.apache.commons.io.FileUtils;

public class ExcelDrivenTest {

    private WebDriver driver;
    private KeywordEngine engine;
    private String browser;

    @Parameters({"browser", "excelPath"})
    @BeforeClass
    public void setUp(@Optional("") String browser,
                      @Optional("") String excelPath) {
        this.browser = (browser != null && !browser.isEmpty()) ? browser : ConfigReader.getBrowser();
        System.out.println("\n============================================================");
        System.out.println("  JAVA AUTOMATION FRAMEWORK - SauceDemo Test Execution");
        System.out.println("  Browser : " + this.browser.toUpperCase());
        System.out.println("  Base URL: " + ConfigReader.getBaseUrl());
        System.out.println("============================================================\n");

        driver = BaseDriver.createDriver(this.browser, ConfigReader.isHeadless());
        engine = new KeywordEngine(driver);
    }

    @Parameters({"excelPath"})
    @Test(description = "Run all test cases from Excel file")
    public void runExcelTestCases(@Optional("") String excelPath) throws Exception {
        if (excelPath == null || excelPath.isEmpty()) {
            excelPath = ConfigReader.getExcelPath();
        }

        File excelFile = new File(excelPath);
        if (!excelFile.exists()) {
            excelFile = new File("../" + excelPath);
        }
        if (!excelFile.exists()) {
            excelFile = new File("../test_data/test_cases.xlsx");
        }

        System.out.println("Excel file: " + excelFile.getAbsolutePath());

        ExcelHandler handler = new ExcelHandler(excelFile.getAbsolutePath());
        Map<String, List<Map<String, String>>> testCases = handler.getTestCasesGrouped("Test Cases");

        List<String> failures = new ArrayList<>();
        int totalTCs = testCases.size();
        int tcIndex = 0;

        for (Map.Entry<String, List<Map<String, String>>> entry : testCases.entrySet()) {
            String tcId = entry.getKey();
            List<Map<String, String>> steps = entry.getValue();
            String tcName = steps.get(0).getOrDefault("Test_Case_Name", "Unknown");
            tcIndex++;

            System.out.println("\n" + "=".repeat(60));
            System.out.println("  [" + tcIndex + "/" + totalTCs + "] " + tcId + " - " + tcName);
            System.out.println("=".repeat(60));

            engine.clearBrowserState();

            boolean tcPassed = true;
            for (Map<String, String> step : steps) {
                try {
                    engine.executeStep(step);
                    System.out.println("  PASS | Step " + step.get("Step_No") + ": " + step.get("Action"));
                } catch (Exception e) {
                    System.err.println("  FAIL | Step " + step.get("Step_No") + ": " + step.get("Action") + " -> " + e.getMessage());
                    captureScreenshot(tcId);
                    tcPassed = false;
                    break;
                }
            }

            System.out.println("  Result: " + (tcPassed ? "PASSED" : "FAILED"));

            if (!tcPassed) {
                failures.add(tcId + ": " + tcName);
            }
        }

        System.out.println("\n" + "=".repeat(60));
        System.out.println("  EXECUTION SUMMARY");
        System.out.println("  Total : " + totalTCs);
        System.out.println("  Passed: " + (totalTCs - failures.size()));
        System.out.println("  Failed: " + failures.size());
        System.out.println("=".repeat(60));

        if (!failures.isEmpty()) {
            Assert.fail(failures.size() + " test case(s) failed:\n  - " + String.join("\n  - ", failures));
        }
    }

    private void captureScreenshot(String testCaseId) {
        try {
            File dir = new File("../reports/screenshots");
            dir.mkdirs();
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            File dest = new File(dir, testCaseId + "_" + timestamp + ".png");
            FileUtils.copyFile(src, dest);
            System.out.println("  Screenshot: " + dest.getAbsolutePath());
        } catch (Exception e) {
            System.err.println("  Screenshot failed: " + e.getMessage());
        }
    }

    @AfterClass
    public void tearDown() {
        if (driver != null) {
            driver.quit();
            System.out.println("\nBrowser closed. Test execution complete.");
        }
    }
}
