Sentinel_Incident__c incident = [
    SELECT Id
    FROM Sentinel_Incident__c
    WHERE Name = 'SI-000008'
    LIMIT 1
];

ZentomExecutionController.executeApprovedAction(incident.Id);
