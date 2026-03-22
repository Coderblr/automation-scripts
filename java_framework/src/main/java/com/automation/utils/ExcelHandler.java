package com.automation.utils;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.*;

public class ExcelHandler {

    private final String filePath;

    public ExcelHandler(String filePath) {
        this.filePath = filePath;
    }

    public List<Map<String, String>> readTestCases(String sheetName) throws IOException {
        List<Map<String, String>> testSteps = new ArrayList<>();

        try (FileInputStream fis = new FileInputStream(new File(filePath));
             Workbook workbook = new XSSFWorkbook(fis)) {

            Sheet sheet = (sheetName != null && !sheetName.isEmpty())
                    ? workbook.getSheet(sheetName)
                    : workbook.getSheetAt(0);

            if (sheet == null) {
                throw new IllegalArgumentException("Sheet not found: " + sheetName);
            }

            Row headerRow = sheet.getRow(0);
            List<String> headers = new ArrayList<>();
            for (Cell cell : headerRow) {
                headers.add(getCellValue(cell));
            }

            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;

                Map<String, String> rowData = new LinkedHashMap<>();
                for (int j = 0; j < headers.size(); j++) {
                    Cell cell = row.getCell(j);
                    rowData.put(headers.get(j), cell != null ? getCellValue(cell) : "");
                }

                String action = rowData.getOrDefault("Action", "").trim();
                if (action.isEmpty()) continue;

                String runFlag = rowData.getOrDefault("Run", "Yes").trim().toLowerCase();
                if (runFlag.equals("no") || runFlag.equals("n") || runFlag.equals("false")) continue;

                testSteps.add(rowData);
            }
        }

        System.out.println("Loaded " + testSteps.size() + " test steps from: " + filePath);
        return testSteps;
    }

    public List<Map<String, String>> readTestCases() throws IOException {
        return readTestCases(null);
    }

    public Map<String, List<Map<String, String>>> getTestCasesGrouped(String sheetName) throws IOException {
        List<Map<String, String>> allSteps = readTestCases(sheetName);
        Map<String, List<Map<String, String>>> grouped = new LinkedHashMap<>();

        for (Map<String, String> step : allSteps) {
            String tcId = step.getOrDefault("Test_Case_ID", "Unknown");
            grouped.computeIfAbsent(tcId, k -> new ArrayList<>()).add(step);
        }

        return grouped;
    }

    public Map<String, List<Map<String, String>>> getTestCasesGrouped() throws IOException {
        return getTestCasesGrouped(null);
    }

    private String getCellValue(Cell cell) {
        if (cell == null) return "";
        switch (cell.getCellType()) {
            case STRING: return cell.getStringCellValue();
            case NUMERIC: return String.valueOf((int) cell.getNumericCellValue());
            case BOOLEAN: return String.valueOf(cell.getBooleanCellValue());
            case FORMULA: return cell.getCellFormula();
            default: return "";
        }
    }
}
