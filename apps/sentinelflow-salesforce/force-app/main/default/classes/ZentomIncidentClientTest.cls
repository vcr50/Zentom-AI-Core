@IsTest
private class ZentomIncidentClientTest {
    private class ZentomIncidentMock implements HttpCalloutMock {
        public HttpResponse respond(HttpRequest request) {
            System.assertEquals('POST', request.getMethod());
            System.assertEquals('application/json', request.getHeader('Content-Type'));
            System.assert(request.getEndpoint().contains('/api/incidents/receive'));

            Map<String, Object> payload =
                (Map<String, Object>) JSON.deserializeUntyped(request.getBody());
            System.assertEquals('FLOW_FAILURE', payload.get('incidentType'));
            System.assertEquals('Salesforce Flow', payload.get('source'));
            System.assertEquals('production', payload.get('environment'));
            System.assertEquals('CREATE_CASE', payload.get('actionType'));

            HttpResponse response = new HttpResponse();
            response.setStatusCode(200);
            response.setBody(
                '{"message":"Incident received successfully",' +
                '"incidentId":123,' +
                '"risk":{"totalScore":95,"riskLevel":"CRITICAL"},' +
                '"policy":{"decision":"HUMAN_APPROVAL_REQUIRED","requiresApproval":true,' +
                '"reason":"Production environment requires human approval"},' +
                '"recommendation":{"summary":"Salesforce Flow failed because Account Owner was missing.",' +
                '"rootCause":"Required owner lookup was null during Flow execution.",' +
                '"recommendedAction":"Create an admin case and review Flow input validation.",' +
                '"confidenceScore":87,"runbookKey":"FLOW_FAILURE_BASIC_RECOVERY",' +
                '"recommendationStatus":"Generated"}}'
            );
            return response;
        }
    }

    @IsTest
    static void sendIncident_postsPayloadToZentomApiAndPersistsResult() {
        ZentomIncidentClient.baseUrlOverride = 'https://example.test';
        Test.setMock(HttpCalloutMock.class, new ZentomIncidentMock());

        Test.startTest();
        ZentomIncidentClient.sendIncident(
            'FLOW_FAILURE',
            'Salesforce Flow',
            'production',
            'Flow failed due to missing Account Owner'
        );
        Test.stopTest();

        Sentinel_Incident__c incident = [
            SELECT Incident_Type__c, Source__c, Environment__c, Risk_Score__c,
                Risk_Level__c, Policy_Decision__c, Policy_Reason__c,
                Zentom_Incident_Id__c, Status__c, AI_Summary__c, Root_Cause__c,
                Recommended_Action__c, AI_Confidence__c, Runbook_Key__c,
                Runbook_Title__c, Runbook_Steps__c, Recommendation_Status__c,
                Approval_Status__c, Execution_Status__c, Next_Action__c
            FROM Sentinel_Incident__c
            LIMIT 1
        ];
        System.assertEquals('FLOW_FAILURE', incident.Incident_Type__c);
        System.assertEquals('Salesforce Flow', incident.Source__c);
        System.assertEquals('production', incident.Environment__c);
        System.assertEquals(95, incident.Risk_Score__c);
        System.assertEquals('CRITICAL', incident.Risk_Level__c);
        System.assertEquals('HUMAN_APPROVAL_REQUIRED', incident.Policy_Decision__c);
        System.assertEquals('Production environment requires human approval', incident.Policy_Reason__c);
        System.assertEquals('123', incident.Zentom_Incident_Id__c);
        System.assertEquals('Approval Required', incident.Status__c);
        System.assertEquals(
            'Salesforce Flow failed because Account Owner was missing.',
            incident.AI_Summary__c
        );
        System.assertEquals(
            'Required owner lookup was null during Flow execution.',
            incident.Root_Cause__c
        );
        System.assertEquals(87, incident.AI_Confidence__c);
        System.assertEquals('FLOW_FAILURE_BASIC_RECOVERY', incident.Runbook_Key__c);
        System.assertEquals('Flow Failure Basic Recovery', incident.Runbook_Title__c);
        System.assert(incident.Runbook_Steps__c.contains('Review the failed Flow interview.'));
        System.assertEquals('Generated', incident.Recommendation_Status__c);
        System.assertEquals('Pending Approval', incident.Approval_Status__c);
        System.assertEquals('Not Started', incident.Execution_Status__c);
        System.assertEquals('Awaiting human approval before execution', incident.Next_Action__c);

        Zentom_Policy_Decision__c policy = [
            SELECT Incident__c, Decision__c, Requires_Approval__c, Reason__c,
                Risk_Score__c, Action_Type__c
            FROM Zentom_Policy_Decision__c
            WHERE Incident__c = :incident.Id
            LIMIT 1
        ];
        System.assertEquals('HUMAN_APPROVAL_REQUIRED', policy.Decision__c);
        System.assertEquals(true, policy.Requires_Approval__c);
        System.assertEquals(95, policy.Risk_Score__c);
        System.assertEquals('CREATE_CASE', policy.Action_Type__c);

        Sentinel_Audit_Log__c auditLog = [
            SELECT Incident__c, Event_Type__c, Decision__c, Created_By_System__c,
                Trace_Id__c
            FROM Sentinel_Audit_Log__c
            WHERE Incident__c = :incident.Id
                AND Event_Type__c = 'ZENTOM_POLICY_EVALUATED'
            LIMIT 1
        ];
        System.assertEquals('ZENTOM_POLICY_EVALUATED', auditLog.Event_Type__c);
        System.assertEquals('HUMAN_APPROVAL_REQUIRED', auditLog.Decision__c);
        System.assertEquals(true, auditLog.Created_By_System__c);
        System.assertEquals('123', auditLog.Trace_Id__c);

        Sentinel_Audit_Log__c runbookAudit = [
            SELECT Event_Type__c, Decision__c
            FROM Sentinel_Audit_Log__c
            WHERE Incident__c = :incident.Id
                AND Event_Type__c = 'RUNBOOK_SELECTED'
            LIMIT 1
        ];
        System.assertEquals('FLOW_FAILURE_BASIC_RECOVERY', runbookAudit.Decision__c);

        List<Sentinel_Audit_Log__c> replayLogs = [
            SELECT Event_Type__c
            FROM Sentinel_Audit_Log__c
            WHERE Incident__c = :incident.Id
                AND Event_Type__c IN (
                    'INCIDENT_RECEIVED',
                    'RISK_CALCULATED',
                    'AI_RECOMMENDATION_GENERATED'
                )
        ];
        System.assertEquals(3, replayLogs.size());
    }
}
