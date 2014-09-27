DROP TABLE IF EXISTS "NotificationHistory";
CREATE TABLE "NotificationHistory" (
    "notificationType" VARCHAR      NOT NULL COLLATE "default",
    "notificationTime" TIMESTAMP(6) NOT NULL
)
WITH (OIDS = FALSE);
ALTER TABLE "NotificationHistory" OWNER TO "sepgroup";

COMMENT ON TABLE "NotificationHistory" IS 'Used for tracking automatic notifications. @author Daniel Zhang (張道博)';

ALTER TABLE "NotificationHistory" ADD PRIMARY KEY ("notificationType", "notificationTime") NOT DEFERRABLE INITIALLY IMMEDIATE;
