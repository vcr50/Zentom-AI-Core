import { LightningElement, wire } from 'lwc';
import { NavigationMixin } from 'lightning/navigation';
import { refreshApex } from '@salesforce/apex';

import getDashboardData from '@salesforce/apex/ZentomDashboardController.getDashboardData';

export default class ZentomDashboard extends NavigationMixin(LightningElement) {
    dateRange = 'LAST_7_DAYS';
    data;
    errorMessage;
    wiredDashboard;

    @wire(getDashboardData, { dateRange: '$dateRange' })
    wiredGetDashboardData(result) {
        this.wiredDashboard = result;
        if (result.data) {
            this.data = result.data;
            this.errorMessage = undefined;
        } else if (result.error) {
            this.data = undefined;
            this.errorMessage = this.reduceError(result.error);
        }
    }

    get topRunbook() {
        return this.data?.summary?.topRunbook || 'None';
    }

    get activeRangeLabel() {
        if (this.dateRange === 'TODAY') {
            return 'Today';
        }
        if (this.dateRange === 'ALL') {
            return 'All time';
        }
        return 'Last 7 days';
    }

    get failedExecutionLabel() {
        const failedRows = (this.data?.recentIncidents || []).filter((row) => row.executionStatus === 'Failed');
        return String(failedRows.length);
    }

    get systemHealthLabel() {
        if (this.errorMessage) {
            return 'Attention';
        }
        if (this.data?.summary?.criticalIncidents > 0 || this.data?.summary?.pendingApprovals > 0) {
            return 'Watch';
        }
        return 'Operational';
    }

    get systemHealthClass() {
        if (this.errorMessage) {
            return 'badge critical-badge';
        }
        if (this.data?.summary?.criticalIncidents > 0 || this.data?.summary?.pendingApprovals > 0) {
            return 'badge warning-badge';
        }
        return 'badge success-badge';
    }

    get orgHealthClass() {
        const status = this.data?.summary?.orgHealthStatus;
        if (status === 'Healthy') {
            return 'health-card health-healthy';
        }
        if (status === 'Stable') {
            return 'health-card health-stable';
        }
        if (status === 'At Risk') {
            return 'health-card health-warning';
        }
        if (status === 'Critical') {
            return 'health-card health-critical';
        }
        return 'health-card health-stable';
    }

    get showLoading() {
        return !this.data && !this.errorMessage;
    }

    get recentIncidents() {
        return this.decorateRows(this.data?.recentIncidents || []);
    }

    get pendingApprovals() {
        return this.decorateRows(this.data?.pendingApprovals || []);
    }

    get recentExecutions() {
        return this.decorateRows(this.data?.recentExecutions || []);
    }

    get recentReplayEvents() {
        return (this.data?.recentReplayEvents || []).map((row) => ({
            ...row,
            createdLabel: this.formatDateTime(row.createdDate),
            decisionClass: `badge ${this.decisionClass(row.decision)}`
        }));
    }

    get recentCasesCreated() {
        return this.decorateRows(this.data?.recentCasesCreated || []);
    }

    get hasRecentIncidents() {
        return this.recentIncidents.length > 0;
    }

    get hasPendingApprovals() {
        return this.pendingApprovals.length > 0;
    }

    get hasRecentExecutions() {
        return this.recentExecutions.length > 0;
    }

    get hasRecentReplayEvents() {
        return this.recentReplayEvents.length > 0;
    }

    get hasRecentCasesCreated() {
        return this.recentCasesCreated.length > 0;
    }

    handleRangeChange(event) {
        this.dateRange = event.target.dataset.range;
        refreshApex(this.wiredDashboard);
    }

    openIncident(event) {
        this[NavigationMixin.Navigate]({
            type: 'standard__recordPage',
            attributes: {
                recordId: event.currentTarget.dataset.id,
                objectApiName: 'Sentinel_Incident__c',
                actionName: 'view'
            }
        });
    }

    openCase(event) {
        this[NavigationMixin.Navigate]({
            type: 'standard__recordPage',
            attributes: {
                recordId: event.currentTarget.dataset.id,
                objectApiName: 'Case',
                actionName: 'view'
            }
        });
    }

    decorateRows(rows) {
        return rows.map((row) => ({
            ...row,
            riskLabel: row.riskScore ? `${row.riskScore} / ${row.riskLevel || 'Unknown'}` : row.riskLevel,
            riskClass: `badge ${this.riskClass(row.riskLevel)}`,
            statusClass: `badge ${this.statusClass(row.status, row.executionStatus)}`,
            executionClass: `badge ${this.statusClass(row.status, row.executionStatus)}`,
            createdLabel: this.formatDate(row.createdDate),
            executedLabel: this.formatDateTime(row.executedAt),
            caseLabel: row.createdCaseNumber ? `Case ${row.createdCaseNumber}` : 'No case'
        }));
    }

    riskClass(riskLevel) {
        if (riskLevel === 'CRITICAL') {
            return 'critical-badge';
        }
        if (riskLevel === 'HIGH') {
            return 'high-badge';
        }
        if (riskLevel === 'MEDIUM') {
            return 'medium-badge';
        }
        return 'low-badge';
    }

    statusClass(status, executionStatus) {
        if (executionStatus === 'Executed') {
            return 'success-badge';
        }
        if (status === 'Approval Required') {
            return 'warning-badge';
        }
        return 'neutral-badge';
    }

    decisionClass(decision) {
        if (decision === 'Rejected') {
            return 'critical-badge';
        }
        if (decision === 'Approved' || decision === 'Executed') {
            return 'success-badge';
        }
        if (decision === 'Pending Approval') {
            return 'warning-badge';
        }
        return 'neutral-badge';
    }

    formatDate(value) {
        return value ? new Date(value).toLocaleDateString() : '';
    }

    formatDateTime(value) {
        return value ? new Date(value).toLocaleString() : '';
    }

    reduceError(error) {
        if (Array.isArray(error?.body)) {
            return error.body.map((item) => item.message).join(', ');
        }
        return error?.body?.message || error?.message || 'Unable to load dashboard.';
    }
}
