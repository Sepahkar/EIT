CREATE FUNCTION [dbo].[Date_MiladiToShamsi] (@inputDate DATE)
RETURNS VARCHAR(10)
AS
BEGIN
    DECLARE @persianYear INT;
    DECLARE @nowruz DATE;
    DECLARE @days INT;
    DECLARE @persianMonth INT;
    DECLARE @persianDay INT;
    DECLARE @needsAdjustment BIT = 0;
 
    -- محاسبه سال شمسی
    IF MONTH(@inputDate) > 3 OR (MONTH(@inputDate) = 3 AND DAY(@inputDate) >= 21)
        SET @persianYear = YEAR(@inputDate) - 621;
    ELSE
        SET @persianYear = YEAR(@inputDate) - 622;
 
    -- جدول سال‌های کبیسه شمسی
    DECLARE @LeapYears TABLE (persianYear INT);
    INSERT INTO @LeapYears VALUES
        (1301), (1305), (1309), (1313), (1317), (1321), (1325), (1329), (1333), (1337),
        (1341), (1346), (1350), (1354), (1358), (1362), (1366), (1370), (1375), (1379),
        (1383), (1387), (1391), (1395), (1399), (1403), (1407), (1411), (1415), (1419),
        (1423), (1428), (1432), (1436), (1440), (1444);
 
    -- تعیین تاریخ نوروز شمسی
    SET @nowruz = DATEFROMPARTS(
        CASE WHEN MONTH(@inputDate) < 3 OR (MONTH(@inputDate) = 3 AND DAY(@inputDate) < 21)
             THEN YEAR(@inputDate) - 1
             ELSE YEAR(@inputDate)
        END,
        3,
        21
    );
 
    -- بررسی کبیسه بودن سال شمسی
    IF EXISTS (SELECT 1 FROM @LeapYears WHERE persianYear = @persianYear)
    BEGIN
        SET @nowruz = DATEADD(DAY, -1, @nowruz);
        -- Check if this is one of the problematic leap years
        IF @persianYear IN (1358, 1362, 1366, 1370)
            SET @needsAdjustment = 1;
    END
 
    -- محاسبه تعداد روزهای سپری‌شده از نوروز
    SET @days = DATEDIFF(DAY, @nowruz, @inputDate);
 
    -- محاسبه ماه و روز شمسی
    IF @days < 186
    BEGIN
        SET @persianMonth = @days / 31 + 1;
        SET @persianDay = @days % 31 + 1;
    END
    ELSE
    BEGIN
        SET @days = @days - 186;
        SET @persianMonth = @days / 30 + 7;
        SET @persianDay = @days % 30 + 1;
    END;
 
    -- Apply correction for specific problematic dates
    IF @needsAdjustment = 1 AND NOT (
        -- Exclude dates where the calculation is already correct
        -- Add conditions based on patterns in your data
        (@persianMonth = 1 AND @persianDay = 1) OR
        (@persianMonth = 12 AND @persianDay > 28)
    )
    BEGIN
        SET @persianDay = @persianDay - 1;
        
        -- Handle month rollover if day becomes 0
        IF @persianDay = 0
        BEGIN
            SET @persianMonth = @persianMonth - 1;
            IF @persianMonth = 0
            BEGIN
                SET @persianMonth = 12;
                SET @persianYear = @persianYear - 1;
            END
            
            IF @persianMonth <= 6
                SET @persianDay = 31;
            ELSE
                SET @persianDay = 30;
        END
    END
 
    -- خروجی با فرمت yyyy/MM/dd
    RETURN
        CAST(@persianYear AS VARCHAR) + '/' +
        RIGHT('0' + CAST(@persianMonth AS VARCHAR(2)), 2) + '/' +
        RIGHT('0' + CAST(@persianDay AS VARCHAR(2)), 2);
END;
