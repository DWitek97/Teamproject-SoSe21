Create Table If Not Exists Participant(
	ParticipantId INT PRIMARY KEY NOT NULL,
    Username VARCHAR(30) UNIQUE,
    Password VARCHAR(30),
    Email VARCHAR(30) UNIQUE,
    IsActive BOOLEAN
);

Alter Table Participant Change Column ParticipantId ParticipantId INT(11) NOT NULL Auto_Increment;

Create Table If Not Exists Contact(
	ContactId INT PRIMARY KEY NOT NULL,
    ParticipantIdFk INT,
    Foreign Key (ParticipantIdFk) REFERENCES Participant(ParticipantId),
    Username VARCHAR(30) UNIQUE
);

Alter Table Contact Change Column ContactId ContactId INT(11) NOT NULL Auto_Increment;

Create Table If Not Exists Chat(
	ChatId INT PRIMARY KEY NOT NULL,
    FirstChatParticipantIdFk INT,
    Foreign Key (FirstChatParticipantIdFk) REFERENCES Participant(ParticipantId),
    SecondChatParticipantIdFk INT,
    Foreign Key (SecondChatParticipantIdFk) REFERENCES Participant(ParticipantId)
);

Alter Table Chat Change Column ChatId ChatId INT(11) NOT NULL Auto_Increment;

Create Table If Not Exists Message(
	MessageId INT PRIMARY KEY NOT NULL,
    ChatIdFk INT,
    Foreign Key (ChatIdFk) REFERENCES Chat(ChatId),
    ParticipantIdFk INT,
    Foreign Key (ParticipantIdFk) REFERENCES Participant(ParticipantId),
    Content LONGTEXT,
    Timestamp DATETIME
);

Alter Table Message Change Column MessageId MessageId INT(11) NOT NULL Auto_Increment;

-- avoid 'Field '...' doesn't have a default value' error in linux environment
-- Show Variables like 'sql_mode';
-- Set Global sql_mode='';