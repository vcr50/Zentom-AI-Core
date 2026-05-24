Sentinel_Incident__c incident = [
    SELECT Id
    FROM Sentinel_Incident__c
    WHERE Approval_Status__c = 'Pending Approval'
    ORDER BY CreatedDate DESC
    LIMIT 1
];

ZentomApprovalController.approveIncident(incident.Id);
