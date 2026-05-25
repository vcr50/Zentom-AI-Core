@IsTest
private class SentinelFlowSlackAlertServiceTest {
    @IsTest
    static void formatAlert_buildsCriticalIncidentMessage() {
        Sentinel_Incident__c incident = createIncident('Approval Required', 'Pending Approval', 'Not Started');

        SentinelFlowSlackAlertService.AlertMessage message =
            SentinelFlowSlackAlertService.formatAlert(
                SentinelFlowSlackAlertService.AlertType.CRITICAL_INCIDENT,
                incident.Id
            );

        System.assertEquals(SentinelFlowSlackAlertService.AlertType.CRITICAL_INCIDENT, message.alertType);
        System.assert(message.text.contains('SentinelFlow critical incident'));
        System.assert(message.text.contains('Incident: SI-'));
        System.assert(message.text.contains('Risk: 95 / CRITICAL'));
        System.assert(message.text.contains('Policy: HUMAN_APPROVAL_REQUIRED'));
        System.assert(message.text.contains('Review in Salesforce:'));
        assertNoUnsafeActionText(message.text);
        assertNoSecretText(message.text);
        System.assertEquals('CRITICAL_INCIDENT', message.payload.get('eventType'));
        System.assertEquals('FLOW_FAILURE', message.payload.get('incidentType'));
    }

    @IsTest
    static void formatAlert_buildsApprovalRequiredMessage() {
        Sentinel_Incident__c incident = createIncident('Approval Required', 'Pending Approval', 'Not Started');

        SentinelFlowSlackAlertService.AlertMessage message =
            SentinelFlowSlackAlertService.formatAlert(
                SentinelFlowSlackAlertService.AlertType.APPROVAL_REQUIRED,
                incident.Id
            );

        System.assert(message.text.contains('SentinelFlow clearance required'));
        System.assert(message.text.contains('Recommended action: Create an admin case'));
        System.assert(message.text.contains('Review in Salesforce:'));
        assertNoUnsafeActionText(message.text);
        assertNoSecretText(message.text);
    }

    @IsTest
    static void formatAlert_buildsExecutedAndCaseMessages() {
        Case createdCase = new Case(Subject = 'Slack alert case', Status = 'New', Origin = 'Web');
        insert createdCase;

        Sentinel_Incident__c incident = createIncident('Action Created', 'Approved', 'Executed');
        incident.Execution_Action__c = 'CREATE_CASE';
        incident.Executed_At__c = System.now();
        incident.Created_Case__c = createdCase.Id;
        update incident;

        SentinelFlowSlackAlertService.AlertMessage executed =
            SentinelFlowSlackAlertService.formatAlert(
                SentinelFlowSlackAlertService.AlertType.ACTION_EXECUTED,
                incident.Id
            );
        System.assert(executed.text.contains('SentinelFlow cleared action executed'));
        System.assert(executed.text.contains('Action: CREATE_CASE'));
        assertNoUnsafeActionText(executed.text);

        SentinelFlowSlackAlertService.AlertMessage caseCreated =
            SentinelFlowSlackAlertService.formatAlert(
                SentinelFlowSlackAlertService.AlertType.CASE_CREATED,
                incident.Id
            );
        System.assert(caseCreated.text.contains('SentinelFlow case created'));
        System.assert(caseCreated.text.contains('Open Incident:'));
        assertNoUnsafeActionText(caseCreated.text);
        assertNoSecretText(caseCreated.text);
    }

    @IsTest
    static void formatAlert_handlesNullInputs() {
        Boolean missingTypeThrown = false;
        try {
            SentinelFlowSlackAlertService.formatAlert(null, createIncident('Approval Required', 'Pending Approval', 'Not Started').Id);
        } catch (SentinelFlowSlackAlertService.SentinelFlowSlackAlertException e) {
            missingTypeThrown = true;
        }
        System.assert(missingTypeThrown, 'Missing alert type should throw a controlled exception.');

        Boolean missingIdThrown = false;
        try {
            SentinelFlowSlackAlertService.formatAlert(
                SentinelFlowSlackAlertService.AlertType.CRITICAL_INCIDENT,
                (Id) null
            );
        } catch (SentinelFlowSlackAlertService.SentinelFlowSlackAlertException e) {
            missingIdThrown = true;
        }
        System.assert(missingIdThrown, 'Missing incident id should throw a controlled exception.');
    }

    private static Sentinel_Incident__c createIncident(String status, String approvalStatus, String executionStatus) {
        Sentinel_Incident__c incident = new Sentinel_Incident__c(
            Incident_Type__c = 'FLOW_FAILURE',
            Source__c = 'Salesforce Flow',
            Environment__c = 'production',
            Error_Message__c = 'Flow failed due to missing Account Owner',
            Risk_Score__c = 95,
            Risk_Level__c = 'CRITICAL',
            Policy_Decision__c = 'HUMAN_APPROVAL_REQUIRED',
            Policy_Reason__c = 'Production environment requires human approval',
            Status__c = status,
            AI_Summary__c = 'Salesforce Flow failed because Account Owner was missing.',
            Root_Cause__c = 'Required owner lookup was null during Flow execution.',
            Recommended_Action__c = 'Create an admin case and review Flow input validation.',
            AI_Confidence__c = 87,
            Runbook_Key__c = 'FLOW_FAILURE_BASIC_RECOVERY',
            Runbook_Title__c = 'Flow Failure Basic Recovery',
            Runbook_Steps__c = '1. Review the failed Flow interview.',
            Recommendation_Status__c = approvalStatus == 'Approved' ? 'Approved' : 'Generated',
            Approval_Status__c = approvalStatus,
            Execution_Status__c = executionStatus
        );
        insert incident;
        return incident;
    }

    private static void assertNoUnsafeActionText(String value) {
        String lowerValue = value.toLowerCase();
        System.assert(!lowerValue.contains('approve in slack'), 'Slack message must not approve in Slack.');
        System.assert(!lowerValue.contains('reject in slack'), 'Slack message must not reject in Slack.');
        System.assert(!lowerValue.contains('execute in slack'), 'Slack message must not execute in Slack.');
        System.assert(!lowerValue.contains('remediate in slack'), 'Slack message must not remediate in Slack.');
    }

    private static void assertNoSecretText(String value) {
        System.assert(!value.contains('xoxb-'), 'Slack bot token pattern must not appear.');
        System.assert(!value.contains('hooks.slack.com/services'), 'Slack webhook URL must not appear.');
        System.assert(!value.contains('sid='), 'Salesforce session id pattern must not appear.');
        System.assert(!value.contains('SLACK_WEBHOOK_URL'), 'Secret environment variable name must not appear in message.');
    }
}
