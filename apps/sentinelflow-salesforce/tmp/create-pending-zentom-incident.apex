insert new Sentinel_Incident__c(
    Incident_Type__c = 'FLOW_FAILURE',
    Source__c = 'Salesforce Flow',
    Environment__c = 'production',
    Error_Message__c = 'Flow failed due to missing Account Owner',
    Risk_Score__c = 95,
    Risk_Level__c = 'CRITICAL',
    Policy_Decision__c = 'HUMAN_APPROVAL_REQUIRED',
    Policy_Reason__c = 'Production environment requires human approval',
    Status__c = 'Approval Required',
    AI_Summary__c = 'Salesforce Flow failed because Account Owner was missing.',
    Root_Cause__c = 'Required owner lookup was null during Flow execution.',
    Recommended_Action__c = 'Create an admin case and review Flow input validation.',
    AI_Confidence__c = 87,
    Runbook_Key__c = 'FLOW_FAILURE_BASIC_RECOVERY',
    Recommendation_Status__c = 'Generated',
    Approval_Status__c = 'Pending Approval',
    Next_Action__c = 'Awaiting human approval before execution'
);
