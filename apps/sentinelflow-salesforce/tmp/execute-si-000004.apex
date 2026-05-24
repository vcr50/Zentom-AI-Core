Sentinel_Incident__c incident = [
    SELECT Id
    FROM Sentinel_Incident__c
    WHERE Name = 'SI-000004'
    LIMIT 1
];

ZentomExecutionController.executeApprovedAction(incident.Id);
