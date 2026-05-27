import { LightningElement, api, wire } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';

import STATUS_FIELD from '@salesforce/schema/Sentinel_Incident__c.AI_Reasoning_Status__c';
import CONFIDENCE_FIELD from '@salesforce/schema/Sentinel_Incident__c.AI_Confidence__c';
import EXPLANATION_FIELD from '@salesforce/schema/Sentinel_Incident__c.AI_Explanation__c';
import RISK_REASON_FIELD from '@salesforce/schema/Sentinel_Incident__c.Risk_Reason__c';
import POLICY_REASON_FIELD from '@salesforce/schema/Sentinel_Incident__c.Policy_Reason__c';
import RUNBOOK_REASON_FIELD from '@salesforce/schema/Sentinel_Incident__c.Runbook_Reason__c';
import MEMORY_USED_FIELD from '@salesforce/schema/Sentinel_Incident__c.Memory_Used__c';
import ORCHESTRATION_MODE_FIELD from '@salesforce/schema/Sentinel_Incident__c.Orchestration_Mode__c';
import BRAIN_VERSION_FIELD from '@salesforce/schema/Sentinel_Incident__c.Brain_Version__c';

const FIELDS = [
    STATUS_FIELD, CONFIDENCE_FIELD, EXPLANATION_FIELD, 
    RISK_REASON_FIELD, POLICY_REASON_FIELD, RUNBOOK_REASON_FIELD,
    MEMORY_USED_FIELD, ORCHESTRATION_MODE_FIELD, BRAIN_VERSION_FIELD
];

export default class ZentomAiExplanationPanel extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    incident;

    get status() { return getFieldValue(this.incident.data, STATUS_FIELD); }
    get confidence() { return getFieldValue(this.incident.data, CONFIDENCE_FIELD); }
    get explanation() { return getFieldValue(this.incident.data, EXPLANATION_FIELD); }
    get riskReason() { return getFieldValue(this.incident.data, RISK_REASON_FIELD); }
    get policyReason() { return getFieldValue(this.incident.data, POLICY_REASON_FIELD); }
    get runbookReason() { return getFieldValue(this.incident.data, RUNBOOK_REASON_FIELD); }
    get memoryUsed() { return getFieldValue(this.incident.data, MEMORY_USED_FIELD) ? 'Yes' : 'No'; }
    get orchestrationMode() { return getFieldValue(this.incident.data, ORCHESTRATION_MODE_FIELD); }
    get brainVersion() { return getFieldValue(this.incident.data, BRAIN_VERSION_FIELD); }

    get hasData() {
        return this.incident && this.incident.data;
    }
}
