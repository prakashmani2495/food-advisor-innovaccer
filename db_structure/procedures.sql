CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_CheckUserAccessByUserID`(IN P_EmailID VARCHAR(255))
BEGIN
	IF (SELECT 1=1 FROM UserAccess WHERE Email_ID = P_EmailID) THEN
	BEGIN
		SELECT 
		UserAccess_ID
		,FullName
		,`Password`
		FROM UserAccess 
		WHERE Email_ID = P_EmailID 
		AND IsActive = 'Y'
		LIMIT 1;
	END;

	END IF;
END;


CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_CreateNewUser`(IN P_Name VARCHAR(255), IN P_Mail VARCHAR(255), IN P_Password VARCHAR(255))
BEGIN
	IF (SELECT 1 = 1 FROM UserAccess WHERE Email_ID = P_Mail) THEN 
		BEGIN 
			SELECT
				'warning' AS `status`,
				'Email ID that you submitted already exists.' AS `desc`;
		END;

	ELSE 
		BEGIN
			INSERT INTO	UserAccess (
				FullName,
				Email_ID,
				Password,
				IsActive,
				LastModifiedBy,
				LastModifiedDate )
			VALUES(
				P_Name,
				P_Mail,
				P_Password,
				'Y',
				'SYSTEM',
				NOW() );

			IF (SELECT 1 = 1 FROM UserAccess WHERE Email_ID = P_Mail ) THEN 
				BEGIN 
					SELECT 'success' AS `status`,
						'You have successfully registered, Please Sign In.' AS `desc`;
				END;

			ELSE 
				BEGIN 
					SELECT
						'error' AS `status`,
						'Somethin went wrong, Please contact system Administrator.' AS `desc`;
				END;
			END IF;
		END;
	END IF;
END;


CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_CreateUserSession`(IN P_UID VARCHAR(255), IN P_UserID INT, IN P_AccessJTI TEXT, IN P_RefreshJTI TEXT)
BEGIN
	INSERT INTO UserSession
	(Session_ID, UserAccess_ID, AccessToken, RefreshToken, SessionEnd)
	VALUES(P_UID, P_UserID, P_AccessJTI, P_RefreshJTI, DATE_ADD(NOW(), INTERVAL 2 DAY));

END;


CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_GetDenyTokenList`()
BEGIN
	SELECT rs.Token FROM RevokeSession AS rs 
	INNER JOIN UserSession AS us
	ON rs.Session_ID = us.Session_ID 
	WHERE us.SessionEnd > NOW();
END;


CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_PopulateDietPlan`(IN P_EmailID VARCHAR(255))
BEGIN
	
	CREATE TEMPORARY TABLE RawDietPlan
	SELECT ud.ID, ud.UserAccess_ID, ud.TargetBMI, ud.TargetDay, ud.TargetWeek, dc.`Day`, dc.`Time`, dc.DietFood, dc.`Order` FROM (
		SELECT ID, UserAccess_ID, IsActive
		, 24 AS TargetBMI
		, CASE WHEN BMI > 25 THEN (round(((BMI-24)*10)/7)+1)*7
				WHEN BMI <= 25 THEN (round(((24-BMI)*10)/7)+1)*7 END AS TargetDay
		, CASE WHEN BMI > 25 THEN round(((BMI-24)*10)/7)+1
				WHEN BMI <= 25 THEN round(((24-BMI)*10)/7)+1 END AS TargetWeek
		, CASE WHEN BMI > 25 THEN 24
				WHEN BMI <= 25 THEN 19 END AS DietMapper
		FROM UserDetails 
	) as ud
	INNER JOIN DietChart dc 
	ON dc.BMI = ud.DietMapper
	INNER JOIN UserAccess ua 
	ON ud.UserAccess_ID = ua.UserAccess_ID 
	WHERE ud.IsActive = 1 AND dc.IsActive = 1
	AND ua.Email_ID = P_EmailID;

	SELECT UserAccess_ID INTO @AccessID FROM food_advisor.UserAccess ua WHERE ua.Email_ID = P_EmailID;

	SELECT TargetWeek, 1, 0, TargetBMI INTO @TargetWeek, @counter, @dayadd, @TargetBMI FROM RawDietPlan LIMIT 1;
	

	CREATE TEMPORARY TABLE FinalDietPlan (
		ID INT NOT NULL, 
		UserAccess_ID INT NOT NULL, 
		TargetBMI INT NOT NULL, 
		TargetDay INT NOT NULL, 
		TargetWeek INT NOT NULL, 
		`Day` INT NOT NULL, 
		`Time` VARCHAR(45) NOT NULL, 
		DietFood TEXT NOT NULL, 
		`Order` INT NOT NULL
	);
	
	WHILE @counter <= @TargetWeek DO
        INSERT INTO FinalDietPlan(ID, UserAccess_ID, TargetBMI, TargetDay, TargetWeek, `Day`, `Time`, DietFood, `Order`)
        SELECT ID, UserAccess_ID, TargetBMI, TargetDay, TargetWeek, `Day`+@dayadd, `Time`, DietFood, `Order` FROM RawDietPlan;
        SET @counter = @counter + 1;
       	SET @dayadd = @dayadd + 7;
    END WHILE;
   
   	INSERT INTO food_advisor.DietPlan
	(UserAccess_ID, UserDetails_ID, DayNumber, DietDate, DietTime, DietOrder, DietFood)
	SELECT UserAccess_ID, ID, `Day`, DATE(DATE_ADD(NOW(), INTERVAL `Day` DAY)), `Time`, `Order`, DietFood FROM FinalDietPlan;

	SELECT MIN(DietDate), MAX(DietDate) INTO @MinDate, @MaxDate FROM DietPlan WHERE UserAccess_ID = @AccessID;

	UPDATE food_advisor.UserDetails
	SET TargetDays = @TargetWeek*7,
		TargetBMI = @TargetBMI,
		DietStarts = @MinDate,
		DietEnds = @MaxDate
	WHERE UserAccess_ID = @AccessID;
   
   	DROP TABLE RawDietPlan;
   	DROP TABLE FinalDietPlan;

END;


CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_RevokeUserAccess`(IN P_UserID VARCHAR(255), IN P_AccessJTI TEXT)
BEGIN
	
	SELECT UserAccess_ID INTO @UserID FROM food_advisor.UserAccess WHERE Email_ID = P_UserID;

	INSERT INTO food_advisor.RevokeSession (Session_ID, `Type`, Token)	
	SELECT Session_ID, 
			'access',
			AccessToken 
	FROM LM_Auth.UserSession
	WHERE UserAccess_ID = @UserID
	AND AccessToken = P_AccessJTI
	AND IsActive = 1
	AND IsLogOut = 0
	UNION 
	SELECT Session_ID, 
			'refresh',
			RefreshToken 
	FROM LM_Auth.UserSession
	WHERE UserAccess_ID = @UserID
	AND AccessToken = P_AccessJTI
	AND IsActive = 1
	AND IsLogOut = 0;

	UPDATE food_advisor.UserSession
	SET IsActive = 0
	, IsLogOut = 1
	WHERE UserAccess_ID = @UserID
	AND AccessToken = P_AccessJTI;

	select 'success' as logout;
	

END;


CREATE DEFINER=`etl_admin`@`%` PROCEDURE `food_advisor`.`SP_UpdateUserDetails`(
	IN P_EmailID VARCHAR(255), 
	IN P_Age INT,
	IN P_Gender VARCHAR(45),
	IN P_Height INT,
	IN P_Weight INT,
	IN P_Activity TEXT,
	IN P_Medical TEXT,
	IN P_BMI FLOAT
)
BEGIN
	
	SELECT UserAccess_ID INTO @AccessID FROM food_advisor.UserAccess ua WHERE ua.Email_ID = P_EmailID;

	UPDATE food_advisor.UserDetails 
	SET IsActive = 0
	WHERE UserAccess_ID = @AccessID;

	INSERT INTO food_advisor.UserDetails
	(UserAccess_ID, Age, Gender, Height, Weight, MedicalCondition, DailyActivity, BMI, IsActive, LastModified)
	SELECT @AccessID, P_Age, P_Gender, P_Height, P_Weight, P_Medical, P_Activity, P_BMI, b'1', CURRENT_TIMESTAMP;

	CALL `SP_PopulateDietPlan`(P_EmailID);
	
	SELECT 1 as `flag`;

	
END;

