--# For each database:
ALTER DATABASE test_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
--# For each table:
ALTER TABLE message CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SET NAMES utf8mb4;


--ALTER TABLE agency CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE chat CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE contact CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE housematch_hashtag CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE interests CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE participant CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE properties CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE property_and_hashtag CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE transaction CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--# For each column:
--ALTER TABLE message CHANGE content content longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE message CHANGE MessageId MessageId longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE message CHANGE ChatIdFk ChatIdFk longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE message CHANGE Timestamp Timestamp longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--ALTER TABLE message CHANGE ParticipantIdFk ParticipantIdFk longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--show VARIABLES like 'ver%'
--SHOW VARIABLES WHERE test_db.message.content LIKE 'character\_set\_%' OR test_db.message.content LIKE 'collation%';


SET NAMES utf8mb4;
--ALTER TABLE message CONVERT TO CHARACTER SET utf8mb4;

show variables like "collation_%";