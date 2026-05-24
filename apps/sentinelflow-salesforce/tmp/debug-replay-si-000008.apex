Sentinel_Incident__c incident = [
    SELECT Id
    FROM Sentinel_Incident__c
    WHERE Name = 'SI-000008'
    LIMIT 1
];

List<ZentomReplayController.ReplayTimelineItem> timeline =
    ZentomReplayController.getReplayTimeline(incident.Id);

System.debug('Timeline Size: ' + timeline.size());
for (ZentomReplayController.ReplayTimelineItem item : timeline) {
    System.debug(item.eventType + ' | ' + item.decision + ' | ' + item.traceId);
}
