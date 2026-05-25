public with sharing class SentinelFlowSlackAlertService {
    public enum AlertType {
        CRITICAL_INCIDENT,
        APPROVAL_REQUIRED,
        ACTION_EXECUTED,
        CASE_CREATED,
        ORG_HEALTH_WATCH,
        DELIVERY_ISSUE
    }

    public class AlertMessage {
        public AlertType alertType;
        public String text;
        public String salesforceUrl;
        public Map<String, Object> payload;
    }

    public static AlertMessage formatAlert(AlertType alertType, Id incidentId) {
        if (alertType == null) {
            throw new SentinelFlowSlackAlertException('Alert type is required.');
        }

        if (incidentId == null) {
            throw new SentinelFlowSlackAlertException('Incident id is required.');
        }

        Sentinel_Incident__c incident = [
            SELECT Id, Name, Incident_Type__c, Risk_Score__c, Risk_Level__c,
                Policy_Decision__c, Recommended_Action__c, Runbook_Key__c,
                Approval_Status__c, Execution_Status__c, Execution_Action__c,
                Executed_At__c, Created_Case__c, Created_Case__r.CaseNumber,
                Status__c, CreatedDate
            FROM Sentinel_Incident__c
            WHERE Id = :incidentId
            LIMIT 1
        ];

        return formatAlert(alertType, incident);
    }

    @TestVisible
    static AlertMessage formatAlert(AlertType alertType, Sentinel_Incident__c incident) {
        if (alertType == null) {
            throw new SentinelFlowSlackAlertException('Alert type is required.');
        }

        if (incident == null || incident.Id == null) {
            throw new SentinelFlowSlackAlertException('Incident is required.');
        }

        AlertMessage message = new AlertMessage();
        message.alertType = alertType;
        message.salesforceUrl = buildRecordUrl(incident.Id);
        message.text = buildText(alertType, incident, message.salesforceUrl);
        message.payload = buildPayload(alertType, incident, message.text);
        return message;
    }

    private static String buildText(
        AlertType alertType,
        Sentinel_Incident__c incident,
        String incidentUrl
    ) {
        String alertTypeName = String.valueOf(alertType);

        if (alertTypeName == 'CRITICAL_INCIDENT') {
            return 'SentinelFlow critical incident\n' +
                baseIncidentLines(incident) +
                '\nReview in Salesforce: ' + incidentUrl;
        }

        if (alertTypeName == 'APPROVAL_REQUIRED') {
            return 'SentinelFlow clearance required\n' +
                'Incident: ' + safe(incident.Name) + '\n' +
                'Risk: ' + riskLabel(incident) + '\n' +
                'Recommended action: ' + safe(firstNonBlank(incident.Execution_Action__c, incident.Recommended_Action__c)) + '\n' +
                'Runbook: ' + safe(incident.Runbook_Key__c) + '\n\n' +
                'Review in Salesforce: ' + incidentUrl;
        }

        if (alertTypeName == 'ACTION_EXECUTED') {
            return 'SentinelFlow cleared action executed\n' +
                'Incident: ' + safe(incident.Name) + '\n' +
                'Action: ' + safe(incident.Execution_Action__c) + '\n' +
                'Status: ' + safe(incident.Execution_Status__c) + '\n' +
                'Executed at: ' + formatDateTime(incident.Executed_At__c) + '\n\n' +
                'View execution evidence: ' + incidentUrl;
        }

        if (alertTypeName == 'CASE_CREATED') {
            return 'SentinelFlow case created\n' +
                'Incident: ' + safe(incident.Name) + '\n' +
                'Case: ' + safe(caseLabel(incident)) + '\n' +
                'Action: ' + safe(incident.Execution_Action__c) + '\n\n' +
                'Open Incident: ' + incidentUrl;
        }

        if (alertTypeName == 'ORG_HEALTH_WATCH') {
            return 'SentinelFlow org health watch\n' +
                'Status: ' + safe(incident.Status__c) + '\n' +
                'Risk: ' + riskLabel(incident) + '\n' +
                'Reason: Review current SentinelFlow Command Center posture.\n\n' +
                'Open Command Center: ' + getSalesforceBaseUrl();
        }

        return 'SentinelFlow alert delivery issue\n' +
            'Context: Slack alert delivery requires review\n' +
            'Status: Safe failure context only\n\n' +
            'Review system health: ' + getSalesforceBaseUrl();
    }

    private static String baseIncidentLines(Sentinel_Incident__c incident) {
        return 'Incident: ' + safe(incident.Name) + '\n' +
            'Type: ' + safe(incident.Incident_Type__c) + '\n' +
            'Risk: ' + riskLabel(incident) + '\n' +
            'Policy: ' + safe(incident.Policy_Decision__c) + '\n' +
            'Runbook: ' + safe(incident.Runbook_Key__c) + '\n';
    }

    private static Map<String, Object> buildPayload(
        AlertType alertType,
        Sentinel_Incident__c incident,
        String text
    ) {
        Map<String, Object> payload = new Map<String, Object>();
        payload.put('text', text);
        payload.put('eventType', String.valueOf(alertType));
        payload.put('incidentName', safe(incident.Name));
        payload.put('incidentType', safe(incident.Incident_Type__c));
        payload.put('riskScore', incident.Risk_Score__c);
        payload.put('riskLevel', safe(incident.Risk_Level__c));
        payload.put('policyDecision', safe(incident.Policy_Decision__c));
        payload.put('runbookKey', safe(incident.Runbook_Key__c));
        payload.put('approvalStatus', safe(incident.Approval_Status__c));
        payload.put('executionStatus', safe(incident.Execution_Status__c));
        payload.put('salesforceRecordUrl', buildRecordUrl(incident.Id));
        return payload;
    }

    private static String buildRecordUrl(Id recordId) {
        return getSalesforceBaseUrl() + '/lightning/r/' + String.valueOf(recordId) + '/view';
    }

    private static String getSalesforceBaseUrl() {
        return URL.getOrgDomainUrl().toExternalForm();
    }

    private static String riskLabel(Sentinel_Incident__c incident) {
        String score = incident.Risk_Score__c == null ? 'Unknown' : String.valueOf(incident.Risk_Score__c.setScale(0));
        return score + ' / ' + safe(incident.Risk_Level__c);
    }

    private static String caseLabel(Sentinel_Incident__c incident) {
        if (incident.Created_Case__r != null && !String.isBlank(incident.Created_Case__r.CaseNumber)) {
            return incident.Created_Case__r.CaseNumber;
        }

        return incident.Created_Case__c == null ? 'No case' : String.valueOf(incident.Created_Case__c);
    }

    private static String firstNonBlank(String primaryValue, String fallbackValue) {
        return String.isBlank(primaryValue) ? fallbackValue : primaryValue;
    }

    private static String formatDateTime(Datetime value) {
        return value == null ? 'Not reported' : value.formatGmt('yyyy-MM-dd HH:mm:ss \'UTC\'');
    }

    private static String safe(Object value) {
        return value == null || String.isBlank(String.valueOf(value)) ? 'Not reported' : String.valueOf(value);
    }

    public class SentinelFlowSlackAlertException extends Exception {}
}
