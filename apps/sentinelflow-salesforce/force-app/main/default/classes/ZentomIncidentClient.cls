public with sharing class ZentomIncidentClient {
    private static final String CALLOUT_MODE_NAMED_CREDENTIAL = 'NAMED_CREDENTIAL';
    private static final String CALLOUT_MODE_REMOTE_SITE = 'REMOTE_SITE';
    private static final String ZENTOM_NAMED_CREDENTIAL = 'Zentom_API';

    @TestVisible private static String baseUrlOverride;
    @TestVisible private static String calloutModeOverride;

    @future(callout=true)
    public static void sendIncident(
        String incidentType,
        String source,
        String environment,
        String errorMessage
    ) {
        Http http = new Http();
        HttpRequest request = new HttpRequest();
        Map<String, Object> payload = buildPayload(incidentType, source, environment, errorMessage);
        String requestBody = JSON.serialize(payload);

        request.setEndpoint(getApiEndpoint());
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setBody(requestBody);

        try {
            HttpResponse response = http.send(request);
            System.debug('Zentom API Response Status: ' + response.getStatusCode());
            System.debug('Zentom API Response Body: ' + response.getBody());

            if (response.getStatusCode() >= 200 && response.getStatusCode() < 300) {
                persistZentomResult(payload, requestBody, response.getBody());
            }
        } catch (Exception e) {
            System.debug('Zentom API Callout Failed: ' + e.getMessage());
        }
    }

    private static Map<String, Object> buildPayload(
        String incidentType,
        String source,
        String environment,
        String errorMessage
    ) {
        Map<String, Object> payload = new Map<String, Object>();
        payload.put('orgId', UserInfo.getOrganizationId());
        payload.put('incidentType', incidentType);
        payload.put('source', source);
        payload.put('environment', environment);
        payload.put('errorMessage', errorMessage);
        payload.put('confidence', 85);
        payload.put('actionType', 'CREATE_CASE');
        return payload;
    }

    private static String getApiEndpoint() {
        String baseUrl = baseUrlOverride;
        String calloutMode = calloutModeOverride;

        if (String.isBlank(baseUrl) || String.isBlank(calloutMode)) {
            List<Zentom_Setting__mdt> settings = [
                SELECT Base_URL__c, Callout_Mode__c
                FROM Zentom_Setting__mdt
                WHERE Is_Active__c = true
                ORDER BY DeveloperName
                LIMIT 1
            ];

            if (!settings.isEmpty()) {
                if (String.isBlank(baseUrl)) {
                    baseUrl = settings[0].Base_URL__c;
                }

                if (String.isBlank(calloutMode)) {
                    calloutMode = settings[0].Callout_Mode__c;
                }
            }
        }

        if (String.isBlank(calloutMode)) {
            calloutMode = CALLOUT_MODE_REMOTE_SITE;
        }

        if (calloutMode == CALLOUT_MODE_NAMED_CREDENTIAL) {
            return 'callout:' + ZENTOM_NAMED_CREDENTIAL + '/api/incidents/receive';
        }

        if (calloutMode != CALLOUT_MODE_REMOTE_SITE) {
            throw new ZentomConfigurationException('Unsupported Zentom callout mode: ' + calloutMode);
        }

        if (String.isBlank(baseUrl)) {
            throw new ZentomConfigurationException('No active Zentom_Setting__mdt Base_URL__c is configured.');
        }

        if (baseUrl.endsWith('/')) {
            baseUrl = baseUrl.left(baseUrl.length() - 1);
        }

        return baseUrl + '/api/incidents/receive';
    }

    private static void persistZentomResult(
        Map<String, Object> requestPayload,
        String requestBody,
        String responseBody
    ) {
        Map<String, Object> responsePayload =
            (Map<String, Object>) JSON.deserializeUntyped(responseBody);
        Map<String, Object> risk = asMap(responsePayload.get('risk'));
        Map<String, Object> policy = asMap(responsePayload.get('policy'));
        Map<String, Object> recommendation = asMap(responsePayload.get('recommendation'));

        Boolean requiresApproval = asBoolean(policy.get('requiresApproval'));
        String status = requiresApproval == true ? 'Approval Required' : 'Analyzed';
        String approvalStatus = requiresApproval == true ? 'Pending Approval' : 'Not Required';
        String decision = asString(policy.get('decision'));
        String runbookKey = asString(recommendation.get('runbookKey'));
        ZentomRunbookService.RunbookResult runbook =
            ZentomRunbookService.resolve(runbookKey, asString(requestPayload.get('incidentType')));

        Sentinel_Incident__c incident = new Sentinel_Incident__c(
            Incident_Type__c = asString(requestPayload.get('incidentType')),
            Source__c = asString(requestPayload.get('source')),
            Environment__c = asString(requestPayload.get('environment')),
            Error_Message__c = asString(requestPayload.get('errorMessage')),
            Risk_Score__c = asDecimal(risk.get('totalScore')),
            Risk_Level__c = asString(risk.get('riskLevel')),
            Policy_Decision__c = decision,
            Policy_Reason__c = asString(policy.get('reason')),
            Zentom_Incident_Id__c = asString(responsePayload.get('incidentId')),
            Status__c = status,
            AI_Summary__c = asString(recommendation.get('summary')),
            Root_Cause__c = asString(recommendation.get('rootCause')),
            Recommended_Action__c = asString(recommendation.get('recommendedAction')),
            AI_Confidence__c = asDecimal(recommendation.get('confidenceScore')),
            Runbook_Key__c = runbook != null ? runbook.runbookKey : runbookKey,
            Runbook_Title__c = runbook != null ? runbook.title : null,
            Runbook_Description__c = runbook != null ? runbook.description : null,
            Runbook_Steps__c = runbook != null ? runbook.steps : null,
            Recommendation_Status__c = asString(recommendation.get('recommendationStatus')),
            Approval_Status__c = approvalStatus,
            Execution_Status__c = 'Not Started',
            Next_Action__c = requiresApproval == true
                ? 'Awaiting human approval before execution'
                : 'No approval required'
        );
        insert incident;

        insert new Sentinel_Audit_Log__c(
            Incident__c = incident.Id,
            Event_Type__c = 'INCIDENT_RECEIVED',
            Request_Payload__c = truncateLongText(requestBody),
            Decision__c = 'RECEIVED',
            Created_By_System__c = true,
            Trace_Id__c = asString(responsePayload.get('incidentId'))
        );

        insert new Sentinel_Audit_Log__c(
            Incident__c = incident.Id,
            Event_Type__c = 'RISK_CALCULATED',
            Response_Payload__c = truncateLongText(JSON.serialize(risk)),
            Decision__c = asString(risk.get('riskLevel')),
            Created_By_System__c = true,
            Trace_Id__c = asString(responsePayload.get('incidentId'))
        );

        insert new Zentom_Policy_Decision__c(
            Incident__c = incident.Id,
            Decision__c = decision,
            Requires_Approval__c = requiresApproval == true,
            Reason__c = asString(policy.get('reason')),
            Risk_Score__c = asDecimal(risk.get('totalScore')),
            Action_Type__c = asString(requestPayload.get('actionType'))
        );

        insert new Sentinel_Audit_Log__c(
            Incident__c = incident.Id,
            Event_Type__c = 'ZENTOM_POLICY_EVALUATED',
            Request_Payload__c = truncateLongText(requestBody),
            Response_Payload__c = truncateLongText(responseBody),
            Decision__c = decision,
            Created_By_System__c = true,
            Trace_Id__c = asString(responsePayload.get('incidentId'))
        );

        insert new Sentinel_Audit_Log__c(
            Incident__c = incident.Id,
            Event_Type__c = 'AI_RECOMMENDATION_GENERATED',
            Response_Payload__c = truncateLongText(JSON.serialize(recommendation)),
            Decision__c = asString(recommendation.get('recommendationStatus')),
            Created_By_System__c = true,
            Trace_Id__c = asString(responsePayload.get('incidentId'))
        );

        if (runbook != null) {
            insert new Sentinel_Audit_Log__c(
                Incident__c = incident.Id,
                Event_Type__c = 'RUNBOOK_SELECTED',
                Decision__c = runbook.runbookKey,
                Response_Payload__c = runbook.steps,
                Created_By_System__c = true,
                Trace_Id__c = asString(responsePayload.get('incidentId'))
            );
        }
    }

    private static Map<String, Object> asMap(Object value) {
        if (value instanceof Map<String, Object>) {
            return (Map<String, Object>) value;
        }

        return new Map<String, Object>();
    }

    private static String asString(Object value) {
        return value == null ? null : String.valueOf(value);
    }

    private static Decimal asDecimal(Object value) {
        if (value == null) {
            return null;
        }

        if (value instanceof Decimal) {
            return (Decimal) value;
        }

        if (value instanceof Integer) {
            return Decimal.valueOf((Integer) value);
        }

        if (value instanceof Long) {
            return Decimal.valueOf((Long) value);
        }

        if (value instanceof Double) {
            return Decimal.valueOf(String.valueOf(value));
        }

        return Decimal.valueOf(String.valueOf(value));
    }

    private static Boolean asBoolean(Object value) {
        if (value instanceof Boolean) {
            return (Boolean) value;
        }

        return value != null && String.valueOf(value).equalsIgnoreCase('true');
    }

    private static String truncateLongText(String value) {
        if (value == null || value.length() <= 32768) {
            return value;
        }

        return value.left(32768);
    }

    public class ZentomConfigurationException extends Exception {}
}
